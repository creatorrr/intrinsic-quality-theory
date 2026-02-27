"""Tests for Phase 5: size presets, infra config, and artifact validation."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import torch

from persistent_diamonds_v3.config import (
    InfraConfig,
    PRESET_NAMES,
    PersistentDiamondsConfig,
)
from persistent_diamonds_v3.models import DiscreteNarrator, ModularSSMWorldModel
from persistent_diamonds_v3.training.infra import (
    apply_activation_checkpointing,
    autocast_context,
    build_accelerator,
    maybe_accumulate_step,
)

# ---------------------------------------------------------------------------
# Preset tests
# ---------------------------------------------------------------------------


def test_preset_names():
    assert PRESET_NAMES == ("small", "medium", "large")


def test_from_preset_small():
    cfg = PersistentDiamondsConfig.from_preset("small")
    assert cfg.world_model.latent_dim == 256
    assert cfg.world_model.module_count == 4
    assert cfg.world_model.hidden_dim == 128
    assert cfg.narrator.codebook_size == 256
    assert cfg.narrator.codes_per_step == 4
    assert cfg.report_head.model_dim == 128
    assert cfg.report_head.layer_count == 2
    assert cfg.train.max_steps == 1000


def test_from_preset_medium():
    cfg = PersistentDiamondsConfig.from_preset("medium")
    assert cfg.world_model.latent_dim == 1024
    assert cfg.world_model.module_count == 6
    assert cfg.narrator.codebook_size == 512
    assert cfg.report_head.model_dim == 256
    assert cfg.report_head.layer_count == 4
    assert cfg.train.max_steps == 5000


def test_from_preset_large_matches_defaults():
    cfg_large = PersistentDiamondsConfig.from_preset("large")
    cfg_default = PersistentDiamondsConfig()
    assert cfg_large.world_model.latent_dim == cfg_default.world_model.latent_dim
    assert cfg_large.narrator.codebook_size == cfg_default.narrator.codebook_size
    assert cfg_large.report_head.layer_count == cfg_default.report_head.layer_count
    assert cfg_large.train.max_steps == cfg_default.train.max_steps


def test_from_preset_invalid():
    import pytest

    with pytest.raises(ValueError, match="Unknown preset"):
        PersistentDiamondsConfig.from_preset("tiny")


def test_preset_produces_buildable_models():
    """All presets should produce valid model configurations."""
    for name in PRESET_NAMES:
        cfg = PersistentDiamondsConfig.from_preset(name)
        world = ModularSSMWorldModel(
            input_dim=cfg.world_model.input_dim,
            latent_dim=cfg.world_model.latent_dim,
            module_count=cfg.world_model.module_count,
            overlap_ratio=cfg.world_model.overlap_ratio,
            hidden_dim=cfg.world_model.hidden_dim,
        )
        narrator = DiscreteNarrator(
            latent_dim=cfg.world_model.latent_dim,
            hidden_dim=cfg.narrator.hidden_dim,
            window_size=cfg.narrator.window_size,
            update_hz=cfg.narrator.update_hz,
            codebook_size=cfg.narrator.codebook_size,
            codes_per_step=cfg.narrator.codes_per_step,
            code_dim=cfg.narrator.code_dim,
        )

        # Verify shapes through a forward pass.
        x = torch.randn(2, 8, cfg.world_model.input_dim)
        out = world(x)
        assert out.states.shape == (2, 8, cfg.world_model.latent_dim), f"preset={name}"

        window = torch.randn(2, cfg.narrator.window_size, cfg.world_model.latent_dim)
        nout = narrator(window)
        expected_dim = cfg.narrator.codes_per_step * cfg.narrator.code_dim
        assert nout.narrator_state.shape == (2, expected_dim), f"preset={name}"


def test_presets_scale_monotonically():
    """Small < medium < large in terms of latent_dim."""
    cfgs = [PersistentDiamondsConfig.from_preset(n) for n in PRESET_NAMES]
    dims = [c.world_model.latent_dim for c in cfgs]
    assert dims[0] < dims[1] < dims[2]


# ---------------------------------------------------------------------------
# InfraConfig tests
# ---------------------------------------------------------------------------


def test_infra_defaults():
    cfg = InfraConfig()
    assert cfg.bf16 is False
    assert cfg.gradient_accumulation_steps == 1
    assert cfg.activation_checkpointing is False
    assert cfg.use_accelerate is False


def test_infra_yaml_roundtrip():
    cfg = PersistentDiamondsConfig()
    cfg.infra.bf16 = True
    cfg.infra.gradient_accumulation_steps = 4
    cfg.infra.activation_checkpointing = True

    with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w", delete=False) as f:
        cfg.to_yaml(f.name)
        loaded = PersistentDiamondsConfig.from_yaml(f.name)

    assert loaded.infra.bf16 is True
    assert loaded.infra.gradient_accumulation_steps == 4
    assert loaded.infra.activation_checkpointing is True
    assert loaded.infra.use_accelerate is False


def test_preset_yaml_roundtrip():
    """Preset → YAML → reload should preserve values."""
    cfg = PersistentDiamondsConfig.from_preset("small")

    with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w", delete=False) as f:
        cfg.to_yaml(f.name)
        loaded = PersistentDiamondsConfig.from_yaml(f.name)

    assert loaded.world_model.latent_dim == 256
    assert loaded.narrator.codebook_size == 256
    assert loaded.train.max_steps == 1000


# ---------------------------------------------------------------------------
# Infra utility tests
# ---------------------------------------------------------------------------


def test_autocast_context_noop():
    infra = InfraConfig(bf16=False)
    ctx = autocast_context(torch.device("cpu"), infra)
    with ctx:
        x = torch.randn(2, 2)
        y = x @ x.T
        assert y.dtype == torch.float32


def test_autocast_context_bf16():
    infra = InfraConfig(bf16=True)
    ctx = autocast_context(torch.device("cpu"), infra)
    with ctx:
        x = torch.randn(4, 4)
        y = x @ x.T
        assert y.dtype == torch.bfloat16


def test_maybe_accumulate_step_immediate():
    """With accum=1, every step should trigger an optimizer step."""
    model = torch.nn.Linear(4, 2)
    opt = torch.optim.SGD(model.parameters(), lr=0.01)
    infra = InfraConfig(gradient_accumulation_steps=1)

    x = torch.randn(2, 4)
    loss = model(x).sum()
    opt.zero_grad(set_to_none=True)
    stepped = maybe_accumulate_step(opt, loss, step=0, infra=infra)
    assert stepped is True


def test_maybe_accumulate_step_delayed():
    """With accum=4, only every 4th step triggers."""
    model = torch.nn.Linear(4, 2)
    opt = torch.optim.SGD(model.parameters(), lr=0.01)
    infra = InfraConfig(gradient_accumulation_steps=4)

    results = []
    for i in range(8):
        x = torch.randn(2, 4)
        loss = model(x).sum()
        if i % 4 == 0:
            opt.zero_grad(set_to_none=True)
        stepped = maybe_accumulate_step(opt, loss, step=i, infra=infra)
        results.append(stepped)

    # Steps 3, 7 should be True (0-indexed: (3+1)%4==0, (7+1)%4==0)
    assert results == [False, False, False, True, False, False, False, True]


def test_activation_checkpointing_noop_when_disabled():
    """Should not error when disabled."""
    model = torch.nn.Sequential(torch.nn.Linear(4, 4), torch.nn.ReLU())
    infra = InfraConfig(activation_checkpointing=False)
    apply_activation_checkpointing(model, infra)
    # Forward should still work.
    x = torch.randn(2, 4)
    y = model(x)
    assert y.shape == (2, 4)


def test_activation_checkpointing_enabled():
    """When enabled, forward should still produce correct output."""
    model = torch.nn.Sequential(
        torch.nn.Linear(4, 8),
        torch.nn.ReLU(),
        torch.nn.Linear(8, 4),
    )
    infra = InfraConfig(activation_checkpointing=True)

    # Get reference output before checkpointing.
    x = torch.randn(2, 4)
    ref = model(x).detach().clone()

    apply_activation_checkpointing(model, infra)

    # Output should be the same (functionally equivalent).
    out = model(x)
    assert torch.allclose(ref, out, atol=1e-5)


def test_build_accelerator_returns_none_when_disabled():
    infra = InfraConfig(use_accelerate=False)
    assert build_accelerator(infra) is None


# ---------------------------------------------------------------------------
# Artifact validation tests
# ---------------------------------------------------------------------------


def test_validate_artifacts_missing_dir(tmp_path: Path):
    """Import and run the validation script logic."""
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
    from validate_artifacts import validate

    errors = validate(tmp_path / "nonexistent")
    assert any("does not exist" in e for e in errors)


def test_validate_artifacts_empty_dir(tmp_path: Path):
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
    from validate_artifacts import validate

    errors = validate(tmp_path)
    assert len(errors) > 0
    assert any("Missing" in e for e in errors)


def test_validate_artifacts_complete(tmp_path: Path):
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
    from validate_artifacts import validate

    # Create all expected files.
    for name in [
        "world_stage1.pt", "world_stage2.pt", "narrator_stage2.pt",
        "world_stage4.pt", "narrator_stage4.pt", "control_stage4.pt",
    ]:
        (tmp_path / name).write_bytes(b"\x00" * 100)

    (tmp_path / "pdv3.yaml").write_text("world_model: {}")

    (tmp_path / "eval_metrics.json").write_text(json.dumps({
        "tau_eff": 1.0, "unity": 0.5, "readout_dominance": 0.3,
        "coherence": 0.8, "persistence": [],
    }))
    (tmp_path / "protocol1.json").write_text(json.dumps({
        "fragmentation_detected": True, "conditions": [],
    }))
    (tmp_path / "protocol2.json").write_text(json.dumps({
        "dual_high_persistence": False,
        "tripartite_o_information": 0.1,
        "perturbation_containment": 0.5,
    }))
    (tmp_path / "protocol3.json").write_text(json.dumps({
        "peak_shift_detected": True, "conditions": [],
    }))
    (tmp_path / "stage4_result.json").write_text(json.dumps({
        "final_loss": 0.5, "mean_episode_reward": 1.0,
        "mean_episode_length": 10.0, "goal_rate": 0.5, "steps": 100,
    }))

    errors = validate(tmp_path)
    assert errors == [], f"Unexpected errors: {errors}"
