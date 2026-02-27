"""Protocol analogue runners for IQT evaluation.

Protocol 1: Titrated degradation — reduce recurrent gain in steps, measure per-module
    persistence fragmentation.
Protocol 2: Overlap test — run concurrent tasks on overlapping world-model modules,
    measure perturbation containment and tripartite O-information.
Protocol 3: Timescale manipulation — scale the world-model's decay constants to widen,
    narrow, or dissolve the effective integration window, track persistence-peak shift.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field

import torch

from persistent_diamonds_v3.evaluation.metrics import (
    adversarial_coherence_noise,
    adversarial_persistence_split,
    adversarial_readout_dominance,
    adversarial_shuffle_unity,
    adversarial_tau_eff_flat,
    cross_module_coherence,
    persistence_curve,
    readout_dominance,
    tau_eff,
    unity_functional,
)
from persistent_diamonds_v3.models import DiscreteNarrator, ModularSSMWorldModel


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

DEFAULT_LAGS: list[int] = [1, 2, 4, 8, 16, 32]


def _run_world_model(
    world: ModularSSMWorldModel,
    obs: torch.Tensor,
    *,
    actions: torch.Tensor | None = None,
) -> torch.Tensor:
    """Run the world model and return states [B, T, D]."""
    with torch.no_grad():
        out = world(obs, actions=actions)
    return out.states


def _run_narrator_rollout(
    narrator: DiscreteNarrator,
    world_states: torch.Tensor,
    world_step_hz: int,
) -> torch.Tensor:
    """Run narrator over world states and return narrator_state per step [B, T, N]."""
    stride = max(1, int(round(world_step_hz / max(1, narrator.update_hz))))
    B, T, _ = world_states.shape
    narrator_dim = narrator.codes_per_step * narrator.code_dim
    all_states: list[torch.Tensor] = []
    hidden: torch.Tensor | None = None
    current: torch.Tensor | None = None

    with torch.no_grad():
        for t in range(T):
            if t == 0 or t % stride == 0:
                start = max(0, t + 1 - narrator.window_size)
                window = world_states[:, start : t + 1]
                out = narrator(window, hidden_state=hidden)
                hidden = out.hidden_state
                current = out.narrator_state
            if current is None:
                current = torch.zeros(B, narrator_dim, device=world_states.device)
            all_states.append(current)

    return torch.stack(all_states, dim=1)


# ---------------------------------------------------------------------------
# Adversarial-check helper (shared across protocols)
# ---------------------------------------------------------------------------

@dataclass(slots=True)
class AdversarialChecks:
    persistence_split_margin: float = 0.0
    unity_real: float = 0.0
    unity_shuffled: float = 0.0
    unity_pass: bool = False
    coherence_real_mean: float = 0.0
    coherence_noise_mean: float = 0.0
    coherence_pass: bool = False
    readout_real: float = 0.0
    readout_shuffled: float = 0.0
    readout_pass: bool = False
    tau_eff_real: int = 0
    tau_eff_noise: int = 0
    tau_eff_pass: bool = False


def _run_adversarial_checks(
    world_states: torch.Tensor,
    module_states: list[torch.Tensor],
    lags: list[int],
    *,
    narrator_states: torch.Tensor | None = None,
    readout_states: torch.Tensor | None = None,
) -> AdversarialChecks:
    checks = AdversarialChecks()

    # Persistence split: first half of dims as "relevant", second as "irrelevant"
    d = world_states.size(-1)
    rel = world_states[..., : d // 2].contiguous()
    irr = world_states[..., d // 2 :].contiguous()
    if rel.size(-1) >= 2 and irr.size(-1) >= 2:
        checks.persistence_split_margin = adversarial_persistence_split(rel, irr, lag=lags[0])

    # Unity
    checks.unity_real, checks.unity_shuffled = adversarial_shuffle_unity(world_states)
    checks.unity_pass = checks.unity_real > checks.unity_shuffled

    # Coherence
    real_k, noise_k = adversarial_coherence_noise(module_states)
    checks.coherence_real_mean = float(sum(real_k.values()) / max(1, len(real_k))) if real_k else 0.0
    checks.coherence_noise_mean = float(sum(noise_k.values()) / max(1, len(noise_k))) if noise_k else 0.0
    checks.coherence_pass = checks.coherence_real_mean > checks.coherence_noise_mean

    # Readout dominance
    if narrator_states is not None and readout_states is not None:
        checks.readout_real, checks.readout_shuffled = adversarial_readout_dominance(
            narrator_states, readout_states
        )
        checks.readout_pass = checks.readout_real > checks.readout_shuffled

    # tau_eff
    checks.tau_eff_real, checks.tau_eff_noise = adversarial_tau_eff_flat(world_states, lags)
    checks.tau_eff_pass = checks.tau_eff_real > checks.tau_eff_noise

    return checks


# ===================================================================
# Protocol 1: Titrated Degradation
# ===================================================================


@dataclass(slots=True)
class Protocol1StepResult:
    gain_factor: float
    per_module_persistence: list[float]
    coherence: dict[str, float]
    unity: float
    tau_eff: int
    readout_dominance: float


@dataclass(slots=True)
class Protocol1Result:
    steps: list[Protocol1StepResult]
    adversarial: AdversarialChecks
    fragmentation_detected: bool


def run_protocol1(
    world: ModularSSMWorldModel,
    narrator: DiscreteNarrator,
    obs: torch.Tensor,
    *,
    gain_factors: list[float] | None = None,
    lags: list[int] | None = None,
    world_step_hz: int = 100,
) -> Protocol1Result:
    """Protocol 1 analogue: titrated degradation of recurrent gain.

    Reduces the world-model's recurrent gain (decay parameter) in discrete
    steps and measures per-module persistence, coherence, and readout dominance
    at each step.  The IQT prediction is multi-component fragmentation:
    different modules should lose persistence at different rates.
    """
    if gain_factors is None:
        gain_factors = [1.0, 0.8, 0.6, 0.4, 0.2, 0.1, 0.0]
    if lags is None:
        lags = DEFAULT_LAGS

    original_decay_raw = world._decay_raw.data.clone()
    step_results: list[Protocol1StepResult] = []

    for gain in gain_factors:
        # Scale the decay raw parameter to reduce recurrent gain.
        # gain=1.0 is baseline; gain=0.0 fully removes recurrence.
        world._decay_raw.data = original_decay_raw * gain

        world_states = _run_world_model(world, obs)
        module_views = list(world.iter_module_views(world_states))

        # Per-module persistence: take max persistence across lags for each module.
        per_module_p: list[float] = []
        for mv in module_views:
            if mv.size(-1) < 2:
                per_module_p.append(0.0)
                continue
            curve = persistence_curve(mv, lags)
            per_module_p.append(max(r.persistence for r in curve) if curve else 0.0)

        k = cross_module_coherence(module_views)
        u = unity_functional(world_states)
        te = tau_eff(persistence_curve(world_states, lags))

        nar_states = _run_narrator_rollout(narrator, world_states, world_step_hz)
        r = readout_dominance(nar_states, world_states)

        step_results.append(Protocol1StepResult(
            gain_factor=gain,
            per_module_persistence=per_module_p,
            coherence=k,
            unity=u,
            tau_eff=te,
            readout_dominance=r,
        ))

    # Restore original weights
    world._decay_raw.data = original_decay_raw

    # Adversarial checks at baseline (first step)
    baseline_states = _run_world_model(world, obs)
    baseline_modules = list(world.iter_module_views(baseline_states))
    baseline_nar = _run_narrator_rollout(narrator, baseline_states, world_step_hz)
    adv = _run_adversarial_checks(
        baseline_states, baseline_modules, lags,
        narrator_states=baseline_nar, readout_states=baseline_states,
    )

    # Fragmentation detection: check if modules lose persistence at different rates.
    # Compare the baseline persistence ranking to the lowest-gain persistence ranking.
    fragmentation = False
    if len(step_results) >= 2:
        baseline_p = step_results[0].per_module_persistence
        degraded_p = step_results[-1].per_module_persistence
        if len(baseline_p) >= 2 and len(degraded_p) >= 2:
            # At baseline, most modules should have nonzero persistence.
            # At deep degradation, some modules should retain more than others.
            baseline_spread = max(baseline_p) - min(baseline_p)
            degraded_spread = max(degraded_p) - min(degraded_p)
            # Fragmentation if spread increases (heterogeneous degradation)
            # or if the ranking changes meaningfully.
            fragmentation = degraded_spread > baseline_spread * 0.5 or any(
                p > 0.1 * max(baseline_p) for p in degraded_p
            )

    return Protocol1Result(
        steps=step_results,
        adversarial=adv,
        fragmentation_detected=fragmentation,
    )


# ===================================================================
# Protocol 2: Overlap Test
# ===================================================================


@dataclass(slots=True)
class Protocol2Result:
    region_a_persistence: list[float]
    region_b_persistence: list[float]
    overlap_persistence: list[float]
    cross_coherence: dict[str, float]
    perturbation_containment: float
    tripartite_o_information: float
    adversarial: AdversarialChecks
    dual_high_persistence: bool


def _tripartite_o_information(
    a: torch.Tensor,
    b: torch.Tensor,
    o: torch.Tensor,
    eps: float = 1e-6,
) -> float:
    """Approximate tripartite O-information: Ω(A; B; O).

    Ω < 0 indicates synergy-dominated (consistent with a single irreducible
    complex spanning A∪O∪B).  Ω > 0 indicates redundancy (consistent with
    semi-independent regions sharing resources via the overlap zone).

    Uses a Gaussian-entropy approximation for tractability.
    """
    def _gaussian_entropy(x: torch.Tensor) -> float:
        flat = x.reshape(-1, x.size(-1)).float()
        n, d = flat.shape
        if n < 2 or d < 1:
            return 0.0
        flat = flat - flat.mean(0, keepdim=True)
        cov = flat.T @ flat / max(1, n - 1) + eps * torch.eye(d, device=flat.device)
        sign, logabsdet = torch.linalg.slogdet(cov)
        if sign.item() <= 0:
            return 0.0
        return 0.5 * float(logabsdet.item())

    h_a = _gaussian_entropy(a)
    h_b = _gaussian_entropy(b)
    h_o = _gaussian_entropy(o)
    h_ab = _gaussian_entropy(torch.cat([a, b], dim=-1))
    h_ao = _gaussian_entropy(torch.cat([a, o], dim=-1))
    h_bo = _gaussian_entropy(torch.cat([b, o], dim=-1))
    h_abo = _gaussian_entropy(torch.cat([a, b, o], dim=-1))

    # O-information: Ω = TC - DTC
    # For three variables: Ω = (H(A) + H(B) + H(O)) - (H(AB) + H(AO) + H(BO)) + H(ABO)
    # Negative Ω → synergy, Positive Ω → redundancy
    omega = (h_a + h_b + h_o) - (h_ab + h_ao + h_bo) + h_abo
    return float(omega)


def run_protocol2(
    world: ModularSSMWorldModel,
    narrator: DiscreteNarrator,
    obs: torch.Tensor,
    *,
    lags: list[int] | None = None,
    world_step_hz: int = 100,
    perturbation_scale: float = 1.0,
) -> Protocol2Result:
    """Protocol 2 analogue: overlap test with perturbation propagation.

    Identifies two overlapping module regions (A and B) in the world model
    and tests whether both simultaneously sustain independent high-persistence
    dynamics.  Also measures perturbation containment and tripartite
    O-information over the overlap zone.
    """
    if lags is None:
        lags = DEFAULT_LAGS

    slices = world.module_slices
    n_modules = len(slices)
    if n_modules < 2:
        raise ValueError("Protocol 2 requires at least 2 world-model modules.")

    # Pick two adjacent modules that overlap.
    idx_a, idx_b = 0, 1
    start_a, end_a = slices[idx_a]
    start_b, end_b = slices[idx_b]

    # Define overlap zone.
    overlap_start = max(start_a, start_b)
    overlap_end = min(end_a, end_b)

    # Run baseline.
    world_states = _run_world_model(world, obs)

    region_a = world_states[..., start_a:end_a]
    region_b = world_states[..., start_b:end_b]
    overlap = world_states[..., overlap_start:overlap_end] if overlap_end > overlap_start else region_a[..., :1]

    # Per-region persistence
    def _max_persistence(s: torch.Tensor) -> list[float]:
        if s.size(-1) < 2:
            return [0.0]
        curve = persistence_curve(s, lags)
        return [r.persistence for r in curve]

    p_a = _max_persistence(region_a)
    p_b = _max_persistence(region_b)
    p_o = _max_persistence(overlap)

    # Cross coherence between the two regions.
    k = cross_module_coherence([region_a, region_b])

    # Perturbation containment: perturb region A at a single timestep
    # and measure propagation to region B's exclusive zone.
    obs_perturbed = obs.clone()
    t_pert = obs.size(1) // 2
    obs_perturbed[:, t_pert] += perturbation_scale * torch.randn_like(obs_perturbed[:, t_pert])

    perturbed_states = _run_world_model(world, obs_perturbed)
    # B's exclusive zone = [start_b:end_b] minus the overlap.
    b_exclusive_start = overlap_end
    b_exclusive_end = end_b
    if b_exclusive_end <= b_exclusive_start:
        b_exclusive_start = start_b
        b_exclusive_end = overlap_start

    delta_b_exclusive = (
        perturbed_states[..., b_exclusive_start:b_exclusive_end]
        - world_states[..., b_exclusive_start:b_exclusive_end]
    )
    containment = float(1.0 / (1.0 + delta_b_exclusive.abs().mean().item()))

    # Tripartite O-information
    # Flatten time for the Gaussian-entropy computation.
    a_excl = world_states[..., start_a:overlap_start] if overlap_start > start_a else region_a[..., :1]
    b_excl = world_states[..., overlap_end:end_b] if end_b > overlap_end else region_b[..., :1]
    omega = _tripartite_o_information(a_excl, b_excl, overlap)

    # Adversarial checks
    module_views = list(world.iter_module_views(world_states))
    nar_states = _run_narrator_rollout(narrator, world_states, world_step_hz)
    adv = _run_adversarial_checks(
        world_states, module_views, lags,
        narrator_states=nar_states, readout_states=world_states,
    )

    # Both regions maintain high persistence?
    max_p_a = max(p_a) if p_a else 0.0
    max_p_b = max(p_b) if p_b else 0.0
    threshold = 0.01  # minimal persistence threshold
    dual_high = max_p_a > threshold and max_p_b > threshold

    return Protocol2Result(
        region_a_persistence=p_a,
        region_b_persistence=p_b,
        overlap_persistence=p_o,
        cross_coherence=k,
        perturbation_containment=containment,
        tripartite_o_information=omega,
        adversarial=adv,
        dual_high_persistence=dual_high,
    )


# ===================================================================
# Protocol 3: Timescale Manipulation
# ===================================================================


@dataclass(slots=True)
class Protocol3ConditionResult:
    condition: str
    scale_factor: float
    persistence_curve: list[dict[str, float]]
    peak_lag: int
    peak_persistence: float
    auc_persistence: float
    unity: float


@dataclass(slots=True)
class Protocol3Result:
    conditions: list[Protocol3ConditionResult]
    adversarial: AdversarialChecks
    peak_shift_detected: bool


def run_protocol3(
    world: ModularSSMWorldModel,
    narrator: DiscreteNarrator,
    obs: torch.Tensor,
    *,
    lags: list[int] | None = None,
    world_step_hz: int = 100,
    conditions: dict[str, float] | None = None,
) -> Protocol3Result:
    """Protocol 3 analogue: timescale manipulation and peak-shift analysis.

    Scales the world-model's decay timescales to simulate widening (psilocybin
    analogue), narrowing (ketamine analogue), and dissolving (DMT analogue) the
    effective integration window.  Tracks the shift in the persistence-curve
    peak lag.
    """
    if lags is None:
        lags = DEFAULT_LAGS
    if conditions is None:
        conditions = {
            "baseline": 1.0,
            "widened": 2.0,      # psilocybin analogue: longer timescales
            "narrowed": 0.5,     # ketamine analogue: shorter timescales
            "dissolved": 0.1,    # DMT analogue: collapsed timescale hierarchy
        }

    original_decay_raw = world._decay_raw.data.clone()
    condition_results: list[Protocol3ConditionResult] = []

    for name, scale in conditions.items():
        # Scale the decay timescales.
        # For widening: increase decay (slower forgetting) -> shift peak to longer lags.
        # For narrowing: decrease decay (faster forgetting) -> shift peak to shorter lags.
        # For dissolving: flatten the timescale distribution -> no clear peak.
        if name == "dissolved":
            # Flatten: set all decay raws to the same value (mean).
            world._decay_raw.data = original_decay_raw.mean().expand_as(original_decay_raw) * scale
        else:
            world._decay_raw.data = original_decay_raw * scale

        world_states = _run_world_model(world, obs)
        curve = persistence_curve(world_states, lags)
        te = tau_eff(curve)
        peak_p = max((r.persistence for r in curve), default=0.0)
        # AUC via trapezoid approximation
        auc = 0.0
        for i in range(len(curve) - 1):
            dt = curve[i + 1].lag - curve[i].lag
            auc += 0.5 * (curve[i].persistence + curve[i + 1].persistence) * dt
        u = unity_functional(world_states)

        condition_results.append(Protocol3ConditionResult(
            condition=name,
            scale_factor=scale,
            persistence_curve=[
                {"lag": r.lag, "temporal_mi": r.temporal_mi, "effective_dim": r.effective_dim, "persistence": r.persistence}
                for r in curve
            ],
            peak_lag=te,
            peak_persistence=peak_p,
            auc_persistence=auc,
            unity=u,
        ))

    # Restore
    world._decay_raw.data = original_decay_raw

    # Adversarial checks at baseline
    baseline_states = _run_world_model(world, obs)
    module_views = list(world.iter_module_views(baseline_states))
    nar_states = _run_narrator_rollout(narrator, baseline_states, world_step_hz)
    adv = _run_adversarial_checks(
        baseline_states, module_views, lags,
        narrator_states=nar_states, readout_states=baseline_states,
    )

    # Peak-shift detection: does tau_eff change across conditions?
    peak_lags = [c.peak_lag for c in condition_results]
    peak_shift = len(set(peak_lags)) > 1

    return Protocol3Result(
        conditions=condition_results,
        adversarial=adv,
        peak_shift_detected=peak_shift,
    )


# ---------------------------------------------------------------------------
# JSON serialisation helper
# ---------------------------------------------------------------------------

def result_to_dict(result: Protocol1Result | Protocol2Result | Protocol3Result) -> dict:
    """Convert any protocol result to a JSON-serialisable dict."""
    return asdict(result)
