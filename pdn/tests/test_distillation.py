"""Phase 3 tests: distillation hidden alignment + code cache correctness."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import torch
import pytest

from persistent_diamonds_v3.config import DistillationConfig
from persistent_diamonds_v3.data.distill_cache import (
    CachedNarratorTextDataset,
    build_code_cache,
    _cache_key,
)
from persistent_diamonds_v3.models import DiscreteNarrator, ModularSSMWorldModel, ReportHead
from persistent_diamonds_v3.training.distill import (
    DistillationResult,
    NarratorTextDataset,
    build_synthetic_distillation_corpus,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _small_world_narrator():
    world = ModularSSMWorldModel(
        input_dim=16,
        latent_dim=64,
        module_count=2,
        overlap_ratio=0.25,
        hidden_dim=32,
    )
    narrator = DiscreteNarrator(
        latent_dim=64,
        hidden_dim=32,
        window_size=4,
        update_hz=10,
        codebook_size=32,
        codes_per_step=4,
        code_dim=8,
    )
    return world, narrator


def _make_objective_npz(tmp_path: Path, *, n: int = 8, t: int = 10, d: int = 16) -> Path:
    rng = np.random.default_rng(42)
    observations = rng.normal(size=(n, t, d)).astype(np.float32)
    targets = np.roll(observations, -1, axis=1)
    external_drive = rng.normal(size=(n, t, d)).astype(np.float32)
    task_signal = rng.normal(size=(n, t, 1)).astype(np.float32)

    path = tmp_path / "data.npz"
    np.savez(
        path,
        observations=observations,
        targets=targets,
        external_drive=external_drive,
        task_signal=task_signal,
    )
    return path


def _make_corpus(tmp_path: Path, npz_path: Path, *, num: int = 4) -> Path:
    corpus_path = tmp_path / "corpus.jsonl"
    build_synthetic_distillation_corpus(npz_path, corpus_path, num_examples=num, seed=0)
    return corpus_path


class _FakeTokenizer:
    """Minimal tokenizer stub for tests (avoids HuggingFace dependency)."""

    pad_token_id = 0

    def __call__(self, text, **kwargs):
        max_length = kwargs.get("max_length", 32)
        ids = [hash(c) % 100 + 1 for c in text[:max_length]]
        ids = ids + [0] * (max_length - len(ids))
        mask = [1 if tok != 0 else 0 for tok in ids]
        return {
            "input_ids": torch.tensor([ids[:max_length]], dtype=torch.long),
            "attention_mask": torch.tensor([mask[:max_length]], dtype=torch.long),
        }

    def __len__(self):
        return 200


# ---------------------------------------------------------------------------
# Config tests
# ---------------------------------------------------------------------------

class TestDistillationConfigDefaults:
    def test_hidden_alignment_defaults_off(self):
        cfg = DistillationConfig()
        assert cfg.hidden_alignment is False
        assert cfg.alpha_hidden == 0.1
        assert cfg.hidden_projection_dim == 256

    def test_code_cache_dir_has_default(self):
        cfg = DistillationConfig()
        assert cfg.code_cache_dir == ".cache/pdv3/distill_codes"


# ---------------------------------------------------------------------------
# DistillationResult extended fields
# ---------------------------------------------------------------------------

class TestDistillationResult:
    def test_result_includes_loss_breakdown(self):
        r = DistillationResult(
            final_loss=0.5,
            teacher_model_name="test",
            steps=10,
            final_loss_kl=0.3,
            final_loss_ce=0.1,
            final_loss_hidden=0.1,
        )
        assert r.final_loss_kl == 0.3
        assert r.final_loss_ce == 0.1
        assert r.final_loss_hidden == 0.1

    def test_result_backward_compat(self):
        r = DistillationResult(final_loss=0.5, teacher_model_name="test", steps=10)
        assert r.final_loss_kl == 0.0
        assert r.final_loss_hidden == 0.0


# ---------------------------------------------------------------------------
# Code cache tests
# ---------------------------------------------------------------------------

class TestCodeCache:
    def test_build_cache_creates_npz(self, tmp_path):
        world, narrator = _small_world_narrator()
        npz_path = _make_objective_npz(tmp_path)
        corpus_path = _make_corpus(tmp_path, npz_path)
        cache_dir = tmp_path / "cache"

        cache_path = build_code_cache(
            corpus_path=corpus_path,
            objective_npz_path=npz_path,
            world_model=world,
            narrator=narrator,
            cache_dir=cache_dir,
            device="cpu",
        )

        assert cache_path.exists()
        assert cache_path.suffix == ".npz"

        data = np.load(cache_path)
        assert "codes" in data
        assert "trajectory_indices" in data

    def test_cache_is_deterministically_reused(self, tmp_path):
        """Calling build_code_cache twice returns the same path without recomputing."""
        world, narrator = _small_world_narrator()
        npz_path = _make_objective_npz(tmp_path)
        corpus_path = _make_corpus(tmp_path, npz_path)
        cache_dir = tmp_path / "cache"

        path1 = build_code_cache(
            corpus_path=corpus_path,
            objective_npz_path=npz_path,
            world_model=world,
            narrator=narrator,
            cache_dir=cache_dir,
            device="cpu",
        )

        # Record modification time
        mtime1 = path1.stat().st_mtime

        path2 = build_code_cache(
            corpus_path=corpus_path,
            objective_npz_path=npz_path,
            world_model=world,
            narrator=narrator,
            cache_dir=cache_dir,
            device="cpu",
        )

        assert path1 == path2
        # File should NOT have been rewritten
        assert path2.stat().st_mtime == mtime1

    def test_cache_key_changes_with_different_models(self, tmp_path):
        world1, narrator1 = _small_world_narrator()
        world2, narrator2 = _small_world_narrator()

        # Perturb model 2 weights
        with torch.no_grad():
            for p in world2.parameters():
                p.add_(1.0)

        npz_path = _make_objective_npz(tmp_path)
        corpus_path = _make_corpus(tmp_path, npz_path)

        key1 = _cache_key(npz_path, corpus_path, world1, narrator1)
        key2 = _cache_key(npz_path, corpus_path, world2, narrator2)
        assert key1 != key2

    def test_cache_shape_correctness(self, tmp_path):
        world, narrator = _small_world_narrator()
        npz_path = _make_objective_npz(tmp_path, n=8, t=10)
        corpus_path = _make_corpus(tmp_path, npz_path, num=4)
        cache_dir = tmp_path / "cache"

        cache_path = build_code_cache(
            corpus_path=corpus_path,
            objective_npz_path=npz_path,
            world_model=world,
            narrator=narrator,
            cache_dir=cache_dir,
            device="cpu",
        )

        data = np.load(cache_path)
        codes = data["codes"]
        # 4 corpus items, each with T=10 timesteps, K=4 codes per step
        assert codes.shape[0] == 4
        assert codes.shape[1] == 10  # timesteps
        assert codes.shape[2] == narrator.codes_per_step

    def test_cached_codes_match_online(self, tmp_path):
        """Cached codes should exactly match codes computed on the fly."""
        world, narrator = _small_world_narrator()
        npz_path = _make_objective_npz(tmp_path, n=8, t=10)
        corpus_path = _make_corpus(tmp_path, npz_path, num=3)
        cache_dir = tmp_path / "cache"

        cache_path = build_code_cache(
            corpus_path=corpus_path,
            objective_npz_path=npz_path,
            world_model=world,
            narrator=narrator,
            cache_dir=cache_dir,
            device="cpu",
        )

        # Load cached codes
        cached_codes = torch.from_numpy(np.load(cache_path)["codes"]).long()

        # Compute codes online using the NarratorTextDataset path
        tokenizer = _FakeTokenizer()
        online_ds = NarratorTextDataset(
            corpus_path=corpus_path,
            objective_npz_path=npz_path,
            world_model=world,
            narrator=narrator,
            tokenizer=tokenizer,
            device="cpu",
            max_text_length=32,
        )

        for i in range(len(online_ds)):
            item = online_ds[i]
            online_codes = item["code_indices"]
            torch.testing.assert_close(cached_codes[i], online_codes)


# ---------------------------------------------------------------------------
# CachedNarratorTextDataset tests
# ---------------------------------------------------------------------------

class TestCachedNarratorTextDataset:
    def test_dataset_len_and_shapes(self, tmp_path):
        world, narrator = _small_world_narrator()
        npz_path = _make_objective_npz(tmp_path)
        corpus_path = _make_corpus(tmp_path, npz_path, num=4)
        cache_dir = tmp_path / "cache"
        max_text_len = 32

        cache_path = build_code_cache(
            corpus_path=corpus_path,
            objective_npz_path=npz_path,
            world_model=world,
            narrator=narrator,
            cache_dir=cache_dir,
            device="cpu",
        )

        tokenizer = _FakeTokenizer()
        ds = CachedNarratorTextDataset(
            cache_path=cache_path,
            corpus_path=corpus_path,
            tokenizer=tokenizer,
            max_text_length=max_text_len,
        )

        assert len(ds) == 4

        item = ds[0]
        assert "code_indices" in item
        assert "input_ids" in item
        assert "attention_mask" in item
        assert item["input_ids"].shape == (max_text_len,)
        assert item["attention_mask"].shape == (max_text_len,)

    def test_stale_cache_raises(self, tmp_path):
        """If corpus and cache lengths differ, raise ValueError."""
        world, narrator = _small_world_narrator()
        npz_path = _make_objective_npz(tmp_path)
        corpus_path = _make_corpus(tmp_path, npz_path, num=4)
        cache_dir = tmp_path / "cache"

        cache_path = build_code_cache(
            corpus_path=corpus_path,
            objective_npz_path=npz_path,
            world_model=world,
            narrator=narrator,
            cache_dir=cache_dir,
            device="cpu",
        )

        # Append extra record to corpus to trigger mismatch
        with corpus_path.open("a") as f:
            f.write(json.dumps({"trajectory_index": 0, "text": "extra"}) + "\n")

        tokenizer = _FakeTokenizer()
        with pytest.raises(ValueError, match="cache is stale"):
            CachedNarratorTextDataset(
                cache_path=cache_path,
                corpus_path=corpus_path,
                tokenizer=tokenizer,
            )


# ---------------------------------------------------------------------------
# Hidden alignment projection shape tests
# ---------------------------------------------------------------------------

class TestHiddenAlignmentShapes:
    def test_projection_output_matches_student_dim(self):
        """The hidden projection should map teacher_dim -> student model_dim."""
        teacher_dim = 768
        student_dim = 64
        proj_dim = 128

        projection = torch.nn.Sequential(
            torch.nn.Linear(teacher_dim, proj_dim),
            torch.nn.SiLU(),
            torch.nn.Linear(proj_dim, student_dim),
        )

        teacher_hidden = torch.randn(2, 10, teacher_dim)
        projected = projection(teacher_hidden)
        assert projected.shape == (2, 10, student_dim)

    def test_mse_alignment_loss_is_scalar(self):
        """MSE loss between projected teacher and student memory should be a scalar."""
        student_dim = 64
        batch, seq_len = 2, 10

        projected = torch.randn(batch, seq_len, student_dim)
        student_memory = torch.randn(batch, seq_len, student_dim)

        loss = torch.nn.functional.mse_loss(projected, student_memory)
        assert loss.ndim == 0
        assert loss.item() >= 0.0

    def test_report_head_code_embedding_shape(self):
        """code_embedding(code_indices).mean(dim=2) should give [B, S, model_dim]."""
        report = ReportHead(
            codebook_size=32,
            vocab_size=200,
            model_dim=64,
            layer_count=2,
            head_count=4,
            ff_dim=128,
            dropout=0.0,
            max_seq_len=64,
        )

        code_indices = torch.randint(0, 32, (2, 10, 4))
        memory = report.code_embedding(code_indices).mean(dim=2)
        assert memory.shape == (2, 10, 64)
