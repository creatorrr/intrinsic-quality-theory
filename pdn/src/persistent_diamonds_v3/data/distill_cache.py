"""Cached narrator code-sequence dataset for distillation (Stage 3).

Pre-computes code indices once and stores them on disk so repeated
training runs skip the expensive world-model + narrator forward passes.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import Dataset

from persistent_diamonds_v3.models import DiscreteNarrator, ModularSSMWorldModel


def _cache_key(
    objective_npz_path: str | Path,
    corpus_path: str | Path,
    world_model: ModularSSMWorldModel,
    narrator: DiscreteNarrator,
) -> str:
    """Deterministic hash from corpus + model parameter checksums."""
    h = hashlib.sha256()
    h.update(Path(corpus_path).read_bytes())
    h.update(str(Path(objective_npz_path).stat().st_size).encode())
    # Include a fingerprint of model weights for invalidation
    for name, param in list(world_model.named_parameters())[:4]:
        h.update(name.encode())
        h.update(param.data.cpu().numpy().tobytes()[:256])
    for name, param in list(narrator.named_parameters())[:4]:
        h.update(name.encode())
        h.update(param.data.cpu().numpy().tobytes()[:256])
    return h.hexdigest()[:16]


def build_code_cache(
    corpus_path: str | Path,
    objective_npz_path: str | Path,
    world_model: ModularSSMWorldModel,
    narrator: DiscreteNarrator,
    cache_dir: str | Path,
    *,
    device: str = "cpu",
) -> Path:
    """Encode all corpus items and persist code indices to an .npz file.

    Returns the path to the cache file.  If a valid cache already exists
    (matching hash), it is returned immediately without recomputation.
    """
    cache_dir = Path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)

    key = _cache_key(objective_npz_path, corpus_path, world_model, narrator)
    cache_path = cache_dir / f"codes_{key}.npz"
    manifest_path = cache_dir / f"codes_{key}.json"

    if cache_path.exists() and manifest_path.exists():
        return cache_path

    records = [
        json.loads(line)
        for line in Path(corpus_path).read_text().splitlines()
        if line.strip()
    ]
    payload = np.load(str(objective_npz_path))
    observations = torch.from_numpy(payload["observations"]).float()

    world_model = world_model.to(device).eval()
    narrator_model = narrator.to(device).eval()

    all_codes: list[np.ndarray] = []
    trajectory_indices: list[int] = []

    with torch.no_grad():
        for record in records:
            traj_idx = int(record["trajectory_index"])
            obs = observations[traj_idx : traj_idx + 1].to(device)
            world_out = world_model(obs)
            states = world_out.states

            step_indices: list[torch.Tensor] = []
            for t in range(states.size(1)):
                start = max(0, t + 1 - narrator_model.window_size)
                out = narrator_model(states[:, start : t + 1])
                step_indices.append(out.code_indices)

            code_seq = torch.stack(step_indices, dim=1).squeeze(0).cpu().numpy()
            all_codes.append(code_seq)
            trajectory_indices.append(traj_idx)

    np.savez(
        cache_path,
        codes=np.array(all_codes),
        trajectory_indices=np.array(trajectory_indices),
    )

    manifest_path.write_text(
        json.dumps(
            {
                "cache_key": key,
                "num_items": len(all_codes),
                "corpus_path": str(corpus_path),
                "objective_npz_path": str(objective_npz_path),
            },
            indent=2,
        )
    )

    return cache_path


class CachedNarratorTextDataset(Dataset):
    """Dataset that loads pre-computed code indices from cache."""

    def __init__(
        self,
        cache_path: str | Path,
        corpus_path: str | Path,
        tokenizer,
        *,
        max_text_length: int = 256,
    ):
        cache = np.load(str(cache_path))
        self.all_codes = torch.from_numpy(cache["codes"]).long()

        self.records = [
            json.loads(line)
            for line in Path(corpus_path).read_text().splitlines()
            if line.strip()
        ]
        if len(self.records) != self.all_codes.shape[0]:
            raise ValueError(
                f"Cache has {self.all_codes.shape[0]} items but corpus has "
                f"{len(self.records)} records — cache is stale."
            )

        self.tokenizer = tokenizer
        self.max_text_length = max_text_length

    def __len__(self) -> int:
        return len(self.records)

    def __getitem__(self, idx: int) -> dict[str, torch.Tensor]:
        record = self.records[idx]
        codes = self.all_codes[idx]

        tokenized = self.tokenizer(
            record["text"],
            truncation=True,
            max_length=self.max_text_length,
            padding="max_length",
            return_tensors="pt",
        )

        return {
            "code_indices": codes,
            "input_ids": tokenized["input_ids"].squeeze(0),
            "attention_mask": tokenized["attention_mask"].squeeze(0),
        }
