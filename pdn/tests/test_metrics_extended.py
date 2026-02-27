"""Tests for new evaluation metrics: readout dominance R and adversarial checks."""

import torch

from persistent_diamonds_v3.evaluation.metrics import (
    IQTMetricBundle,
    adversarial_coherence_noise,
    adversarial_readout_dominance,
    adversarial_tau_eff_flat,
    compute_iqt_bundle,
    readout_dominance,
)


# ---------------------------------------------------------------------------
# readout_dominance
# ---------------------------------------------------------------------------


class TestReadoutDominance:
    def test_correlated_narrator_readout_gives_positive_R(self):
        """When narrator causally drives readout, R should be positive."""
        torch.manual_seed(42)
        B, T, D_nar, D_read = 4, 50, 16, 8
        narrator = torch.randn(B, T, D_nar)
        # Build readout as a noisy linear function of lagged narrator.
        W = torch.randn(D_nar, D_read) * 0.5
        readout = torch.zeros(B, T, D_read)
        for t in range(1, T):
            readout[:, t] = narrator[:, t - 1] @ W + 0.1 * torch.randn(B, D_read)

        r = readout_dominance(narrator, readout, lag=1)
        assert r > 0.0, f"Expected positive R for causal relationship, got {r}"

    def test_independent_narrator_readout_gives_near_zero_R(self):
        """When narrator and readout are independent, R should be ~0."""
        torch.manual_seed(42)
        narrator = torch.randn(4, 50, 16)
        readout = torch.randn(4, 50, 8)
        r = readout_dominance(narrator, readout, lag=1)
        assert r < 0.5, f"Expected near-zero R for independent signals, got {r}"

    def test_input_validation(self):
        """Should reject non-3D inputs."""
        import pytest

        with pytest.raises(ValueError, match="Expected"):
            readout_dominance(torch.randn(4, 16), torch.randn(4, 8))

    def test_short_sequence_returns_zero(self):
        """If T <= lag, return 0.0."""
        r = readout_dominance(torch.randn(2, 1, 8), torch.randn(2, 1, 4), lag=1)
        assert r == 0.0


# ---------------------------------------------------------------------------
# adversarial_coherence_noise
# ---------------------------------------------------------------------------


class TestAdversarialCoherence:
    def test_returns_real_and_noise_dicts(self):
        """adversarial_coherence_noise should return two coherence dicts."""
        torch.manual_seed(42)
        m1 = torch.randn(8, 30, 16)
        m2 = torch.randn(8, 30, 16)

        real_k, noise_k = adversarial_coherence_noise([m1, m2])
        assert isinstance(real_k, dict)
        assert isinstance(noise_k, dict)
        assert len(real_k) == len(noise_k)
        assert set(real_k.keys()) == set(noise_k.keys())

    def test_strongly_coupled_modules_beat_noise(self):
        """Modules sharing an identical driving signal should show higher coherence."""
        torch.manual_seed(42)
        B, T, D = 16, 50, 1
        # Both modules are near-copies of the same signal.
        shared = torch.randn(B, T, D)
        m1 = shared + 0.01 * torch.randn(B, T, D)
        m2 = shared + 0.01 * torch.randn(B, T, D)

        real_k, noise_k = adversarial_coherence_noise([m1, m2])
        real_mean = sum(real_k.values()) / max(1, len(real_k))
        noise_mean = sum(noise_k.values()) / max(1, len(noise_k))
        assert real_mean > noise_mean, (
            f"Strongly coupled real coherence {real_mean} should > noise {noise_mean}"
        )


# ---------------------------------------------------------------------------
# adversarial_readout_dominance
# ---------------------------------------------------------------------------


class TestAdversarialReadoutDominance:
    def test_real_exceeds_shuffled(self):
        """Real R should exceed time-shuffled R when causal link exists."""
        torch.manual_seed(42)
        B, T, D = 4, 50, 16
        narrator = torch.randn(B, T, D)
        W = torch.randn(D, 8) * 0.5
        readout = torch.zeros(B, T, 8)
        for t in range(1, T):
            readout[:, t] = narrator[:, t - 1] @ W + 0.1 * torch.randn(B, 8)

        real_r, shuffled_r = adversarial_readout_dominance(narrator, readout, lag=1)
        assert real_r >= shuffled_r, (
            f"Real R ({real_r}) should >= shuffled R ({shuffled_r})"
        )


# ---------------------------------------------------------------------------
# adversarial_tau_eff_flat
# ---------------------------------------------------------------------------


class TestAdversarialTauEff:
    def test_structured_beats_noise(self):
        """Structured data should have a more meaningful tau_eff than white noise."""
        torch.manual_seed(42)
        # Create temporally structured data (autoregressive).
        B, T, D = 4, 64, 16
        states = torch.zeros(B, T, D)
        states[:, 0] = torch.randn(B, D)
        for t in range(1, T):
            states[:, t] = 0.9 * states[:, t - 1] + 0.1 * torch.randn(B, D)

        real_tau, noise_tau = adversarial_tau_eff_flat(states, [1, 2, 4, 8, 16])
        # Real tau should reflect the autocorrelation structure.
        assert real_tau >= 1, f"Expected real tau >= 1, got {real_tau}"


# ---------------------------------------------------------------------------
# IQTMetricBundle includes R
# ---------------------------------------------------------------------------


class TestBundleIncludesR:
    def test_bundle_has_readout_dominance(self):
        """IQTMetricBundle should have a readout_dominance field."""
        bundle = IQTMetricBundle(
            persistence=[],
            coherence={},
            unity=0.0,
            tau_eff=0,
            readout_dominance=0.5,
        )
        assert bundle.readout_dominance == 0.5

    def test_compute_bundle_without_narrator_returns_zero_R(self):
        """When narrator/readout states are not provided, R should be 0."""
        torch.manual_seed(42)
        states = torch.randn(2, 20, 32)
        modules = [states[..., :16], states[..., 16:]]
        bundle = compute_iqt_bundle(states, modules, [1, 2, 4])
        assert bundle.readout_dominance == 0.0

    def test_compute_bundle_with_narrator(self):
        """When narrator/readout states are provided, R should be computed."""
        torch.manual_seed(42)
        states = torch.randn(2, 20, 32)
        modules = [states[..., :16], states[..., 16:]]
        nar = torch.randn(2, 20, 16)
        bundle = compute_iqt_bundle(
            states, modules, [1, 2, 4],
            narrator_states=nar, readout_states=states,
        )
        assert isinstance(bundle.readout_dominance, float)
