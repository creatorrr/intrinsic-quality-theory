from __future__ import annotations

import hashlib
import json
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

import numpy as np
import torch
from torch.utils.data import Dataset

ObjectiveName = Literal[
    "persistence",
    "autonomy",
    "compression",
    "self_prediction",
    "mixed",
]


@dataclass(slots=True)
class ObjectiveRequest:
    objective: ObjectiveName = "mixed"
    num_sequences: int = 512
    sequence_length: int = 256
    feature_dim: int = 256
    seed: int = 17
    source_path: str | None = None


@dataclass(slots=True)
class ObjectiveMaterialization:
    request: ObjectiveRequest
    dataset_path: Path
    manifest_path: Path
    reused: bool


class ObjectiveTensorDataset(Dataset):
    """Torch dataset backed by cached `.npz` objective files."""

    def __init__(self, npz_path: str | Path):
        payload = np.load(npz_path)
        self.observations = torch.from_numpy(payload["observations"])
        self.targets = torch.from_numpy(payload["targets"])
        self.external_drive = torch.from_numpy(payload["external_drive"])
        self.task_signal = torch.from_numpy(payload["task_signal"])

    def __len__(self) -> int:
        return int(self.observations.shape[0])

    def __getitem__(self, idx: int) -> dict[str, torch.Tensor]:
        return {
            "observations": self.observations[idx],
            "targets": self.targets[idx],
            "external_drive": self.external_drive[idx],
            "task_signal": self.task_signal[idx],
        }


class IQTObjectiveDataStore:
    """Caches objective data so runs can reuse exact datasets or generate them on demand."""

    DATA_FILENAME = "data.npz"
    MANIFEST_FILENAME = "manifest.json"

    def __init__(self, cache_dir: str | Path):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def materialize(
        self,
        request: ObjectiveRequest,
        *,
        force_generate: bool = False,
    ) -> ObjectiveMaterialization:
        run_key = self._request_key(request)
        target_dir = self.cache_dir / f"{request.objective}-{run_key}"
        dataset_path = target_dir / self.DATA_FILENAME
        manifest_path = target_dir / self.MANIFEST_FILENAME

        if dataset_path.exists() and manifest_path.exists() and not force_generate:
            return ObjectiveMaterialization(
                request=request,
                dataset_path=dataset_path,
                manifest_path=manifest_path,
                reused=True,
            )

        target_dir.mkdir(parents=True, exist_ok=True)

        if request.source_path:
            self._materialize_from_source(request, dataset_path)
        else:
            arrays = self._generate_objective_arrays(request)
            np.savez_compressed(dataset_path, **arrays)

        manifest = {
            "request": asdict(request),
            "dataset": str(dataset_path),
            "dataset_sha256": self._sha256(dataset_path),
        }
        manifest_path.write_text(json.dumps(manifest, indent=2))

        return ObjectiveMaterialization(
            request=request,
            dataset_path=dataset_path,
            manifest_path=manifest_path,
            reused=False,
        )

    def list_cached(self) -> list[Path]:
        return sorted(self.cache_dir.glob(f"*/{self.DATA_FILENAME}"))

    @staticmethod
    def _request_key(request: ObjectiveRequest) -> str:
        raw = json.dumps(asdict(request), sort_keys=True).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()[:16]

    @staticmethod
    def _sha256(path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def _materialize_from_source(self, request: ObjectiveRequest, destination: Path) -> None:
        source = Path(request.source_path or "")
        if not source.exists():
            raise FileNotFoundError(f"Source path not found: {source}")

        if source.suffix == ".npz":
            shutil.copy2(source, destination)
            return

        if source.suffix == ".npy":
            observations = np.load(source)
            if observations.ndim != 3:
                raise ValueError("Expected source `.npy` to have shape [N, T, D].")
            arrays = self._build_targets_from_observations(observations)
            np.savez_compressed(destination, **arrays)
            return

        raise ValueError(
            "Unsupported source format. Use `.npz` for reusable full payloads or `.npy` [N,T,D] arrays."
        )

    def _generate_objective_arrays(self, request: ObjectiveRequest) -> dict[str, np.ndarray]:
        rng = np.random.default_rng(request.seed)
        n = request.num_sequences
        t = request.sequence_length
        d = request.feature_dim

        observations = self._multi_timescale_latents(rng, n=n, t=t, d=d)
        external_drive = rng.normal(0.0, 0.5, size=(n, t, d)).astype(np.float32)

        if request.objective in {"autonomy", "mixed"}:
            # Keep internal dynamics dominant but still grounded in external signal.
            observations = (0.75 * observations + 0.25 * external_drive).astype(np.float32)
        elif request.objective == "compression":
            observations = self._low_rank_compressible_view(observations, rank=max(8, d // 8), rng=rng)
        elif request.objective == "self_prediction":
            observations = self._add_self_predictive_loops(observations)

        arrays = self._build_targets_from_observations(observations)
        arrays["external_drive"] = external_drive

        if request.objective in {"autonomy", "mixed"}:
            arrays["task_signal"] = self._task_signal_from_observation(observations, external_drive)
        else:
            arrays["task_signal"] = self._task_signal_from_observation(observations, 0.5 * external_drive)

        return arrays

    @staticmethod
    def _build_targets_from_observations(observations: np.ndarray) -> dict[str, np.ndarray]:
        targets = np.zeros_like(observations)
        targets[:, :-1] = observations[:, 1:]
        targets[:, -1] = observations[:, -1]
        return {
            "observations": observations.astype(np.float32),
            "targets": targets.astype(np.float32),
            "external_drive": np.zeros_like(observations, dtype=np.float32),
            "task_signal": np.zeros((observations.shape[0], observations.shape[1], 1), dtype=np.float32),
        }

    @staticmethod
    def _multi_timescale_latents(
        rng: np.random.Generator,
        *,
        n: int,
        t: int,
        d: int,
    ) -> np.ndarray:
        x = np.zeros((n, t, d), dtype=np.float32)
        slow = rng.normal(0.0, 0.15, size=(n, d)).astype(np.float32)
        mid = rng.normal(0.0, 0.15, size=(n, d)).astype(np.float32)
        fast = rng.normal(0.0, 0.15, size=(n, d)).astype(np.float32)

        for step in range(t):
            slow = 0.995 * slow + rng.normal(0.0, 0.01, size=(n, d)).astype(np.float32)
            mid = 0.97 * mid + rng.normal(0.0, 0.04, size=(n, d)).astype(np.float32)
            fast = 0.85 * fast + rng.normal(0.0, 0.12, size=(n, d)).astype(np.float32)
            x[:, step] = slow + mid + fast

        return x

    @staticmethod
    def _low_rank_compressible_view(
        observations: np.ndarray,
        *,
        rank: int,
        rng: np.random.Generator,
    ) -> np.ndarray:
        d = observations.shape[-1]
        basis = rng.normal(0.0, 1.0, size=(d, rank)).astype(np.float32)
        coeffs = observations @ basis
        recon = coeffs @ basis.T
        return recon / np.sqrt(rank)

    @staticmethod
    def _add_self_predictive_loops(observations: np.ndarray) -> np.ndarray:
        out = observations.copy()
        out[:, 1:] = 0.8 * out[:, :-1] + 0.2 * out[:, 1:]
        return out

    @staticmethod
    def _task_signal_from_observation(
        observations: np.ndarray,
        external_drive: np.ndarray,
    ) -> np.ndarray:
        corr = (observations * external_drive).mean(axis=-1, keepdims=True)
        norm = np.tanh(corr)
        return norm.astype(np.float32)
