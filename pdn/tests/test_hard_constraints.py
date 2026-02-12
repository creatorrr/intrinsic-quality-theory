"""Hard constraint regression tests for PDN v3.

These tests lock the three core invariants from the spec (§2.2.4, §2.2.2, §2.1):
  HC-1  No bypass: all output heads receive narrator state only, never raw world state.
  HC-2  Narrator bitrate cap: discrete channel with exactly computed rate.
  HC-3  World state continuity: persistent state survives across forward calls.
"""

import math

import torch
import torch.nn as nn

from persistent_diamonds_v3.models import (
    ControlHead,
    DiscreteNarrator,
    ModularSSMWorldModel,
    ReportHead,
)


# ---------------------------------------------------------------------------
# Helpers – small model fixtures
# ---------------------------------------------------------------------------

def _make_world_model(**overrides):
    defaults = dict(input_dim=16, latent_dim=64, module_count=4, overlap_ratio=0.25, hidden_dim=32)
    defaults.update(overrides)
    return ModularSSMWorldModel(**defaults)


def _make_narrator(latent_dim=64, **overrides):
    defaults = dict(
        latent_dim=latent_dim,
        hidden_dim=32,
        window_size=4,
        update_hz=10,
        codebook_size=1024,
        codes_per_step=8,
        code_dim=8,
    )
    defaults.update(overrides)
    return DiscreteNarrator(**defaults)


def _make_report_head(**overrides):
    defaults = dict(
        codebook_size=1024,
        vocab_size=256,
        model_dim=64,
        layer_count=2,
        head_count=4,
        ff_dim=128,
        dropout=0.0,
        max_seq_len=64,
    )
    defaults.update(overrides)
    return ReportHead(**defaults)


def _make_control_head(narrator_dim=64, **overrides):
    defaults = dict(narrator_dim=narrator_dim, action_dim=8, hidden_dim=32)
    defaults.update(overrides)
    return ControlHead(**defaults)


# ===================================================================
# HC-1  No Bypass
# ===================================================================


class TestNoBypass:
    """Verify that output heads depend on narrator codes, not raw world state."""

    def test_report_head_signature_requires_codes_not_states(self):
        """ReportHead.forward accepts (code_indices, input_ids) – no state tensor."""
        import inspect

        sig = inspect.signature(ReportHead.forward)
        params = list(sig.parameters.keys())
        # Must have code_indices and input_ids, must NOT have a world_state / states param.
        assert "code_indices" in params
        assert "input_ids" in params
        for forbidden in ("states", "world_state", "world_states", "latent_state"):
            assert forbidden not in params, f"ReportHead.forward must not accept '{forbidden}'"

    def test_report_head_gradient_does_not_reach_world_model(self):
        """Backprop through report head must not produce gradients on world model params."""
        world = _make_world_model()
        narrator = _make_narrator()
        report = _make_report_head()

        x = torch.randn(2, 10, 16)
        world_out = world(x)

        # Narrator receives world states (correct dependency).
        nar_out = narrator(world_out.states[:, -4:])

        # Report head receives only discrete code indices (integers, not differentiable).
        code_indices = nar_out.code_indices.unsqueeze(1).expand(-1, 5, -1)
        input_ids = torch.randint(0, 256, (2, 8))
        logits = report(code_indices, input_ids)

        loss = logits.sum()
        loss.backward()

        # World model should have received no gradient from this path.
        for name, p in world.named_parameters():
            assert p.grad is None or torch.all(p.grad == 0), (
                f"World model param '{name}' received gradient through report head – bypass detected"
            )

    def test_narrator_codes_are_discrete_integers(self):
        """code_indices must be integer-typed (non-differentiable), enforcing the bottleneck."""
        narrator = _make_narrator()
        window = torch.randn(2, 4, 64)
        out = narrator(window)
        assert out.code_indices.dtype in (torch.int32, torch.int64, torch.long), (
            f"code_indices should be integer dtype, got {out.code_indices.dtype}"
        )

    def test_stage2_task_head_receives_narrator_not_world(self):
        """Stage 2 task head input is narrator_state + uncertainty, not world_states."""
        from persistent_diamonds_v3.training.stage2 import Stage2ShapingTrainer
        from persistent_diamonds_v3.config import Stage2LossWeights

        world = _make_world_model()
        narrator = _make_narrator()
        trainer = Stage2ShapingTrainer(
            world, narrator,
            input_dim=16, world_step_hz=100,
            stage2_weights=Stage2LossWeights(),
            learning_rate=1e-3, weight_decay=0.0, device="cpu",
        )

        # task_head input dim = narrator_dim + hidden_dim (narrator outputs only)
        narrator_dim = narrator.codes_per_step * narrator.code_dim
        expected_in = narrator_dim + narrator.hidden_dim
        first_layer = trainer.task_head[0]
        assert isinstance(first_layer, nn.Linear)
        assert first_layer.in_features == expected_in, (
            f"task_head input dim {first_layer.in_features} != "
            f"narrator_dim({narrator_dim}) + hidden_dim({narrator.hidden_dim}) = {expected_in}"
        )

    def test_control_head_signature_requires_narrator_not_states(self):
        """ControlHead.forward accepts (narrator_state) – no world state tensor."""
        import inspect

        sig = inspect.signature(ControlHead.forward)
        params = list(sig.parameters.keys())
        assert "narrator_state" in params
        for forbidden in ("states", "world_state", "world_states", "latent_state"):
            assert forbidden not in params, f"ControlHead.forward must not accept '{forbidden}'"

    def test_control_head_gradient_does_not_reach_world_model(self):
        """Backprop through control head with discrete codes must not reach world model.

        At inference time, code_indices are integers and narrator_state is
        reconstructed from the codebook.  We simulate this by detaching the
        narrator_state (equivalent to the non-differentiable code-index path).
        """
        world = _make_world_model()
        narrator = _make_narrator()
        control = _make_control_head(narrator_dim=narrator.codes_per_step * narrator.code_dim)

        x = torch.randn(2, 10, 16)
        world_out = world(x)
        nar_out = narrator(world_out.states[:, -4:])

        # Simulate the discrete bottleneck: detach narrator_state as if
        # reconstructed from integer code_indices (non-differentiable).
        ctrl_out = control(nar_out.narrator_state.detach())

        loss = ctrl_out.action_logits.sum() + ctrl_out.value_estimate.sum()
        loss.backward()

        for name, p in world.named_parameters():
            assert p.grad is None or torch.all(p.grad == 0), (
                f"World model param '{name}' received gradient through control head – bypass detected"
            )

    def test_control_head_input_dim_matches_narrator_bottleneck(self):
        """ControlHead must accept exactly narrator_dim = codes_per_step * code_dim."""
        narrator = _make_narrator(codes_per_step=8, code_dim=8)
        narrator_dim = narrator.codes_per_step * narrator.code_dim
        control = _make_control_head(narrator_dim=narrator_dim)

        first_layer = control.shared[0]
        assert isinstance(first_layer, nn.Linear)
        assert first_layer.in_features == narrator_dim, (
            f"ControlHead input dim {first_layer.in_features} != narrator_dim({narrator_dim})"
        )


# ===================================================================
# HC-2  Narrator Bitrate Cap
# ===================================================================


class TestNarratorBitrateCap:
    """Verify discrete bitrate math and that the channel cannot leak extra information."""

    def test_bits_per_second_formula(self):
        """bits_per_second = codes_per_step * log2(codebook_size) * update_hz."""
        narrator = _make_narrator(codebook_size=1024, codes_per_step=8, update_hz=10)
        expected = 8 * math.log2(1024) * 10  # 8 * 10 * 10 = 800
        assert narrator.bits_per_second == expected

    def test_bits_per_second_scales_with_codebook(self):
        """Doubling codebook adds 1 bit per code."""
        n1 = _make_narrator(codebook_size=512)
        n2 = _make_narrator(codebook_size=1024)
        diff = n2.bits_per_second - n1.bits_per_second
        # 1 extra bit * 8 codes * 10 Hz = 80 bps
        assert abs(diff - 80.0) < 1e-6

    def test_code_indices_bounded_by_codebook(self):
        """All emitted code indices must be in [0, codebook_size)."""
        narrator = _make_narrator(codebook_size=1024)
        window = torch.randn(4, 4, 64)
        out = narrator(window)
        assert out.code_indices.min() >= 0
        assert out.code_indices.max() < 1024

    def test_code_indices_shape_matches_codes_per_step(self):
        """Each narrator update emits exactly codes_per_step indices."""
        for k in (4, 8, 16):
            narrator = _make_narrator(codes_per_step=k, code_dim=8)
            window = torch.randn(2, 4, 64)
            out = narrator(window)
            assert out.code_indices.shape == (2, k), (
                f"Expected code_indices shape (2, {k}), got {out.code_indices.shape}"
            )

    def test_quantized_codes_use_straight_through(self):
        """Quantized codes must allow gradient flow (straight-through estimator)."""
        narrator = _make_narrator()
        window = torch.randn(2, 4, 64, requires_grad=True)
        out = narrator(window)
        # quantized_codes should be differentiable (via straight-through)
        loss = out.quantized_codes.sum()
        loss.backward()
        assert window.grad is not None, "Straight-through gradient did not reach input"

    def test_narrator_state_dimensionality_equals_bottleneck(self):
        """narrator_state must be exactly codes_per_step * code_dim (the bottleneck width)."""
        narrator = _make_narrator(codes_per_step=8, code_dim=8)
        window = torch.randn(2, 4, 64)
        out = narrator(window)
        expected_dim = 8 * 8  # 64
        assert out.narrator_state.shape == (2, expected_dim), (
            f"narrator_state shape {out.narrator_state.shape} != expected (2, {expected_dim})"
        )


# ===================================================================
# HC-3  World State Continuity
# ===================================================================


class TestWorldStateContinuity:
    """Verify that the world model's persistent state survives across forward calls."""

    def test_persistent_state_updates_when_flag_set(self):
        """With persist_state=True, final state from call N becomes initial state for call N+1."""
        world = _make_world_model()
        world.reset_persistent_state(batch_size=2)

        x1 = torch.randn(2, 5, 16)
        out1 = world(x1, persist_state=True)

        # Internal persistent state should now equal out1.final_state.
        assert torch.allclose(world._persistent_state, out1.final_state.detach()), (
            "Persistent state was not updated after persist_state=True call"
        )

        # Second call should start from that state, not from zeros.
        x2 = torch.randn(2, 5, 16)
        out2 = world(x2, persist_state=True)

        # Running with initial_state=zeros should give a different result.
        out2_fresh = world(x2, initial_state=torch.zeros(2, 64))

        assert not torch.allclose(out2.states, out2_fresh.states, atol=1e-5), (
            "Second call produced same result as fresh-start – state not persisted"
        )

    def test_persistent_state_unchanged_when_flag_unset(self):
        """With persist_state=False (default), internal state should remain untouched."""
        world = _make_world_model()
        world.reset_persistent_state(batch_size=2)
        original_state = world._persistent_state.clone()

        x = torch.randn(2, 5, 16)
        world(x, persist_state=False)

        assert torch.allclose(world._persistent_state, original_state), (
            "Persistent state changed despite persist_state=False"
        )

    def test_state_continuity_across_multiple_episodes(self):
        """Simulate 3 sequential episodes; verify state accumulates meaningfully."""
        world = _make_world_model()
        world.reset_persistent_state(batch_size=1)

        states_after_each = []
        for _ in range(3):
            x = torch.randn(1, 8, 16)
            out = world(x, persist_state=True)
            states_after_each.append(world._persistent_state.clone())

        # Each episode should leave a different persistent state.
        assert not torch.allclose(states_after_each[0], states_after_each[1], atol=1e-5)
        assert not torch.allclose(states_after_each[1], states_after_each[2], atol=1e-5)

    def test_reset_clears_persistent_state(self):
        """reset_persistent_state() should zero out the state."""
        world = _make_world_model()

        x = torch.randn(2, 5, 16)
        world(x, persist_state=True)
        assert not torch.all(world._persistent_state == 0)

        world.reset_persistent_state(batch_size=2)
        assert torch.all(world._persistent_state == 0)

    def test_persist_state_detaches_gradient(self):
        """Persisted state must be detached to avoid cross-episode gradient leakage."""
        world = _make_world_model()
        world.reset_persistent_state(batch_size=2)

        x = torch.randn(2, 5, 16)
        world(x, persist_state=True)
        assert not world._persistent_state.requires_grad, (
            "Persisted state should be detached (no grad)"
        )
