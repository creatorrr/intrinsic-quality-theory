from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

import numpy as np
import torch


@dataclass(slots=True)
class PersistenceResult:
    lag: int
    temporal_mi: float
    effective_dim: float
    persistence: float


@dataclass(slots=True)
class IQTMetricBundle:
    persistence: list[PersistenceResult]
    coherence: dict[str, float]
    unity: float
    tau_eff: int
    readout_dominance: float


def _flatten_time(x: torch.Tensor) -> torch.Tensor:
    if x.ndim != 3:
        raise ValueError("Expected tensor of shape [B, T, D].")
    return x.reshape(-1, x.size(-1))


def effective_dimension(states: torch.Tensor, eps: float = 1e-8) -> float:
    flat = _flatten_time(states)
    centered = flat - flat.mean(dim=0, keepdim=True)
    cov = centered.T @ centered / max(1, centered.size(0) - 1)
    eigvals = torch.linalg.eigvalsh(cov).clamp(min=eps)
    participation_ratio = eigvals.sum().pow(2) / eigvals.pow(2).sum().clamp(min=eps)
    return float(participation_ratio.item())


def temporal_mi_proxy(states: torch.Tensor, lag: int, eps: float = 1e-6) -> float:
    if lag <= 0:
        raise ValueError("lag must be > 0")
    if states.size(1) <= lag:
        return 0.0

    a = states[:, :-lag].reshape(-1, states.size(-1))
    b = states[:, lag:].reshape(-1, states.size(-1))

    a = (a - a.mean(dim=0, keepdim=True)) / (a.std(dim=0, keepdim=True, unbiased=False) + eps)
    b = (b - b.mean(dim=0, keepdim=True)) / (b.std(dim=0, keepdim=True, unbiased=False) + eps)

    rho = torch.nan_to_num((a * b).mean(dim=0), nan=0.0).clamp(min=-0.999, max=0.999)
    mi_dims = -0.5 * torch.log1p(-rho.pow(2) + eps)
    return float(mi_dims.mean().item())


def persistence_curve(states: torch.Tensor, lags: list[int]) -> list[PersistenceResult]:
    d_eff = effective_dimension(states)
    results: list[PersistenceResult] = []
    for lag in lags:
        tmi = temporal_mi_proxy(states, lag)
        results.append(
            PersistenceResult(
                lag=lag,
                temporal_mi=tmi,
                effective_dim=d_eff,
                persistence=tmi * d_eff,
            )
        )
    return results


def cross_module_coherence(module_states: list[torch.Tensor]) -> dict[str, float]:
    pooled = [m.mean(dim=1) for m in module_states]
    out: dict[str, float] = {}
    for i, j in combinations(range(len(pooled)), 2):
        a = pooled[i].mean(dim=-1, keepdim=True)
        b = pooled[j].mean(dim=-1, keepdim=True)
        if a.size(0) < 2 or b.size(0) < 2:
            out[f"K_{i}_{j}"] = 0.0
            continue
        a = (a - a.mean(dim=0, keepdim=True)) / (a.std(dim=0, keepdim=True, unbiased=False) + 1e-6)
        b = (b - b.mean(dim=0, keepdim=True)) / (b.std(dim=0, keepdim=True, unbiased=False) + 1e-6)
        corr = torch.nan_to_num((a * b).mean(dim=0), nan=0.0).clamp(min=-0.999, max=0.999)
        mi = -0.5 * torch.log1p(-corr.pow(2) + 1e-6)
        out[f"K_{i}_{j}"] = float(mi.mean().item())
    return out


def unity_functional(states: torch.Tensor, samples: int = 12) -> float:
    d = states.size(-1)
    if d < 2:
        return 0.0

    rng = np.random.default_rng(0)
    flat = _flatten_time(states)
    values: list[float] = []

    for _ in range(samples):
        perm = rng.permutation(d)
        split = rng.integers(low=max(1, d // 4), high=max(2, 3 * d // 4))
        left = torch.tensor(perm[:split], device=flat.device)
        right = torch.tensor(perm[split:], device=flat.device)

        a = flat[:, left].mean(dim=-1, keepdim=True)
        b = flat[:, right].mean(dim=-1, keepdim=True)

        a = (a - a.mean()) / (a.std() + 1e-6)
        b = (b - b.mean()) / (b.std() + 1e-6)

        rho = (a * b).mean().clamp(min=-0.999, max=0.999)
        mi = -0.5 * torch.log1p(-rho.pow(2) + 1e-6)
        values.append(float(mi.item()))

    return float(min(values)) if values else 0.0


def tau_eff(persistence: list[PersistenceResult]) -> int:
    if not persistence:
        return 0
    return max(persistence, key=lambda p: p.persistence).lag


def compute_iqt_bundle(
    states: torch.Tensor,
    module_states: list[torch.Tensor],
    lags: list[int],
    *,
    narrator_states: torch.Tensor | None = None,
    readout_states: torch.Tensor | None = None,
) -> IQTMetricBundle:
    p_curve = persistence_curve(states, lags)
    coherence = cross_module_coherence(module_states)
    u = unity_functional(states)
    if narrator_states is not None and readout_states is not None:
        r = readout_dominance(narrator_states, readout_states)
    else:
        r = 0.0
    return IQTMetricBundle(
        persistence=p_curve,
        coherence=coherence,
        unity=u,
        tau_eff=tau_eff(p_curve),
        readout_dominance=r,
    )


def adversarial_persistence_split(
    relevant_states: torch.Tensor,
    irrelevant_states: torch.Tensor,
    lag: int,
) -> float:
    """Positive margin indicates persistence is concentrated in relevant state."""
    p_rel = temporal_mi_proxy(relevant_states, lag) * effective_dimension(relevant_states)
    p_irrel = temporal_mi_proxy(irrelevant_states, lag) * effective_dimension(irrelevant_states)
    return float(p_rel - p_irrel)


def readout_dominance(
    narrator_states: torch.Tensor,
    readout_states: torch.Tensor,
    lag: int = 1,
    eps: float = 1e-6,
) -> float:
    """Readout dominance R: directed-information proxy from narrator to readout.

    Measures how much the narrator state at time *t* predicts the readout state
    at *t+lag* beyond the readout's own self-prediction.  Approximated via the
    difference in linear-regression residual variance (Granger-style).
    """
    if narrator_states.ndim != 3 or readout_states.ndim != 3:
        raise ValueError("Expected [B, T, D] tensors for narrator_states and readout_states.")
    T = narrator_states.size(1)
    if T <= lag:
        return 0.0

    # Flatten batch and time -> (N, D)
    y = readout_states[:, lag:].reshape(-1, readout_states.size(-1))
    y_past = readout_states[:, :-lag].reshape(-1, readout_states.size(-1))
    x = narrator_states[:, :-lag].reshape(-1, narrator_states.size(-1))

    # Normalise
    y = (y - y.mean(0, keepdim=True)) / (y.std(0, keepdim=True) + eps)
    y_past = (y_past - y_past.mean(0, keepdim=True)) / (y_past.std(0, keepdim=True) + eps)
    x = (x - x.mean(0, keepdim=True)) / (x.std(0, keepdim=True) + eps)

    # Restricted model: predict y from y_past only
    # Use simple ridge regression: beta = (X^T X + lambda I)^{-1} X^T y
    lam = 1e-3
    I_r = torch.eye(y_past.size(-1), device=y.device, dtype=y.dtype)
    beta_r = torch.linalg.solve(y_past.T @ y_past + lam * I_r, y_past.T @ y)
    resid_r = y - y_past @ beta_r
    var_r = resid_r.var(dim=0).mean()

    # Full model: predict y from [y_past, x]
    full = torch.cat([y_past, x], dim=-1)
    I_f = torch.eye(full.size(-1), device=y.device, dtype=y.dtype)
    beta_f = torch.linalg.solve(full.T @ full + lam * I_f, full.T @ y)
    resid_f = y - full @ beta_f
    var_f = resid_f.var(dim=0).mean()

    # R = log(var_restricted / var_full)  (Granger causality statistic)
    R = float(torch.log(var_r / (var_f + eps) + eps).item())
    return max(0.0, R)


def adversarial_shuffle_unity(states: torch.Tensor) -> tuple[float, float]:
    real_u = unity_functional(states)
    shuffled = states[:, torch.randperm(states.size(1), device=states.device)]
    shuffled_u = unity_functional(shuffled)
    return real_u, shuffled_u


def adversarial_coherence_noise(
    module_states: list[torch.Tensor],
) -> tuple[dict[str, float], dict[str, float]]:
    """Adversarial check for K: coherence on real vs. independent-noise modules.

    Returns (real_coherence, noise_coherence). Real should dominate noise.
    """
    real_k = cross_module_coherence(module_states)
    noise_modules = [torch.randn_like(m) for m in module_states]
    noise_k = cross_module_coherence(noise_modules)
    return real_k, noise_k


def adversarial_readout_dominance(
    narrator_states: torch.Tensor,
    readout_states: torch.Tensor,
    lag: int = 1,
) -> tuple[float, float]:
    """Adversarial check for R: real vs. time-shuffled narrator.

    Returns (real_R, shuffled_R). Real should dominate shuffled.
    """
    real_r = readout_dominance(narrator_states, readout_states, lag=lag)
    perm = torch.randperm(narrator_states.size(1), device=narrator_states.device)
    shuffled_nar = narrator_states[:, perm]
    shuffled_r = readout_dominance(shuffled_nar, readout_states, lag=lag)
    return real_r, shuffled_r


def adversarial_tau_eff_flat(
    states: torch.Tensor,
    lags: list[int],
) -> tuple[int, int]:
    """Adversarial check for tau_eff: real vs. temporally-white noise.

    Returns (real_tau_eff, noise_tau_eff). Real should have a meaningful
    peak lag while noise should have no preferred timescale.
    """
    real_curve = persistence_curve(states, lags)
    real_tau = tau_eff(real_curve)
    noise = torch.randn_like(states)
    noise_curve = persistence_curve(noise, lags)
    noise_tau = tau_eff(noise_curve)
    return real_tau, noise_tau
