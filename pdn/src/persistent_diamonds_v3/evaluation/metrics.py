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


def compute_iqt_bundle(states: torch.Tensor, module_states: list[torch.Tensor], lags: list[int]) -> IQTMetricBundle:
    p_curve = persistence_curve(states, lags)
    coherence = cross_module_coherence(module_states)
    unity = unity_functional(states)
    return IQTMetricBundle(
        persistence=p_curve,
        coherence=coherence,
        unity=unity,
        tau_eff=tau_eff(p_curve),
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


def adversarial_shuffle_unity(states: torch.Tensor) -> tuple[float, float]:
    real_u = unity_functional(states)
    shuffled = states[:, torch.randperm(states.size(1), device=states.device)]
    shuffled_u = unity_functional(shuffled)
    return real_u, shuffled_u
