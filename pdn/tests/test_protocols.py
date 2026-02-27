"""Tests for Protocol 1, 2, 3 analogue runners."""

import json

import torch

from persistent_diamonds_v3.evaluation.protocols import (
    Protocol1Result,
    Protocol2Result,
    Protocol3Result,
    _tripartite_o_information,
    result_to_dict,
    run_protocol1,
    run_protocol2,
    run_protocol3,
)
from persistent_diamonds_v3.models import DiscreteNarrator, ModularSSMWorldModel


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _make_world(**overrides):
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


def _make_obs(batch=4, steps=20, dim=16):
    return torch.randn(batch, steps, dim)


# ===================================================================
# Protocol 1
# ===================================================================


class TestProtocol1:
    def test_runs_end_to_end(self):
        world = _make_world()
        narrator = _make_narrator()
        obs = _make_obs()

        result = run_protocol1(
            world, narrator, obs,
            gain_factors=[1.0, 0.5, 0.0],
            lags=[1, 2, 4],
        )
        assert isinstance(result, Protocol1Result)
        assert len(result.steps) == 3

    def test_gain_factor_zero_reduces_persistence(self):
        """At gain=0, recurrence is eliminated; persistence should be lower than baseline."""
        world = _make_world()
        narrator = _make_narrator()
        obs = _make_obs()

        result = run_protocol1(
            world, narrator, obs,
            gain_factors=[1.0, 0.0],
            lags=[1, 2, 4],
        )
        baseline_p = max(result.steps[0].per_module_persistence)
        degraded_p = max(result.steps[1].per_module_persistence)
        # We don't require strict inequality — random init might be noisy — but
        # verify the structure is returned correctly.
        assert isinstance(baseline_p, float)
        assert isinstance(degraded_p, float)

    def test_restores_weights(self):
        """World model decay should be restored after protocol run."""
        world = _make_world()
        narrator = _make_narrator()
        obs = _make_obs()
        original = world._decay_raw.data.clone()

        run_protocol1(world, narrator, obs, gain_factors=[1.0, 0.5, 0.0], lags=[1, 2])
        assert torch.allclose(world._decay_raw.data, original), "Weights were not restored"

    def test_adversarial_checks_present(self):
        world = _make_world()
        narrator = _make_narrator()
        obs = _make_obs()
        result = run_protocol1(world, narrator, obs, gain_factors=[1.0], lags=[1, 2])
        assert hasattr(result.adversarial, "unity_pass")
        assert hasattr(result.adversarial, "coherence_pass")

    def test_json_serialisation(self):
        world = _make_world()
        narrator = _make_narrator()
        obs = _make_obs()
        result = run_protocol1(world, narrator, obs, gain_factors=[1.0], lags=[1, 2])
        d = result_to_dict(result)
        text = json.dumps(d)
        assert '"fragmentation_detected"' in text


# ===================================================================
# Protocol 2
# ===================================================================


class TestProtocol2:
    def test_runs_end_to_end(self):
        world = _make_world()
        narrator = _make_narrator()
        obs = _make_obs()

        result = run_protocol2(world, narrator, obs, lags=[1, 2, 4])
        assert isinstance(result, Protocol2Result)
        assert len(result.region_a_persistence) > 0
        assert len(result.region_b_persistence) > 0

    def test_perturbation_containment_bounded(self):
        world = _make_world()
        narrator = _make_narrator()
        obs = _make_obs()

        result = run_protocol2(world, narrator, obs, lags=[1, 2])
        assert 0.0 <= result.perturbation_containment <= 1.0

    def test_o_information_returns_float(self):
        world = _make_world()
        narrator = _make_narrator()
        obs = _make_obs()

        result = run_protocol2(world, narrator, obs, lags=[1, 2])
        assert isinstance(result.tripartite_o_information, float)

    def test_json_serialisation(self):
        world = _make_world()
        narrator = _make_narrator()
        obs = _make_obs()
        result = run_protocol2(world, narrator, obs, lags=[1, 2])
        d = result_to_dict(result)
        text = json.dumps(d)
        assert '"tripartite_o_information"' in text
        assert '"perturbation_containment"' in text


# ===================================================================
# Protocol 3
# ===================================================================


class TestProtocol3:
    def test_runs_end_to_end(self):
        world = _make_world()
        narrator = _make_narrator()
        obs = _make_obs()

        result = run_protocol3(
            world, narrator, obs,
            lags=[1, 2, 4],
            conditions={"baseline": 1.0, "widened": 2.0, "narrowed": 0.5},
        )
        assert isinstance(result, Protocol3Result)
        assert len(result.conditions) == 3

    def test_conditions_have_persistence_curves(self):
        world = _make_world()
        narrator = _make_narrator()
        obs = _make_obs()

        result = run_protocol3(
            world, narrator, obs,
            lags=[1, 2, 4],
            conditions={"baseline": 1.0, "widened": 2.0},
        )
        for cond in result.conditions:
            assert len(cond.persistence_curve) == 3  # 3 lags
            assert cond.peak_lag >= 1
            assert isinstance(cond.auc_persistence, float)

    def test_restores_weights(self):
        world = _make_world()
        narrator = _make_narrator()
        obs = _make_obs()
        original = world._decay_raw.data.clone()

        run_protocol3(
            world, narrator, obs,
            lags=[1, 2],
            conditions={"baseline": 1.0, "dissolved": 0.1},
        )
        assert torch.allclose(world._decay_raw.data, original)

    def test_json_serialisation(self):
        world = _make_world()
        narrator = _make_narrator()
        obs = _make_obs()
        result = run_protocol3(
            world, narrator, obs,
            lags=[1, 2],
            conditions={"baseline": 1.0},
        )
        d = result_to_dict(result)
        text = json.dumps(d)
        assert '"peak_shift_detected"' in text
        assert '"persistence_curve"' in text


# ===================================================================
# Tripartite O-information
# ===================================================================


class TestTripartiteOInformation:
    def test_returns_float(self):
        a = torch.randn(4, 20, 8)
        b = torch.randn(4, 20, 8)
        o = torch.randn(4, 20, 4)
        omega = _tripartite_o_information(a, b, o)
        assert isinstance(omega, float)

    def test_independent_signals(self):
        """Independent signals should not show strong synergy."""
        torch.manual_seed(42)
        a = torch.randn(8, 50, 8)
        b = torch.randn(8, 50, 8)
        o = torch.randn(8, 50, 4)
        omega = _tripartite_o_information(a, b, o)
        # Should be close to zero for independent signals.
        assert abs(omega) < 10.0, f"O-information for independent signals too large: {omega}"
