# Phase 6b: Protocol 2 — Overlapping Parcellations (Direct Overlap Test)

**Phase:** 06 - Empirical Protocol Predictions
**Track:** Experimental Predictions (Primary IIT Contrast)
**Depends on:** 05b (metrics), 04a (self-threads), 03c (perspectival relativity)
**Unlocks:** Nothing (terminal prediction task)

---

## Goal

State IQT's formal predictions for Protocol 2 (Section 5.2): the direct test of democracy of diamonds vs. IIT's exclusion postulate. Two overlapping brain regions performing independent tasks should both sustain high-persistence dynamics simultaneously.

## What to Formalize

### 1. Overlapping Region Setup

```lean
/-- Two overlapping parcellations sharing physical substrate (lateral parietal cortex). -/
structure OverlapSetup where
  -- Region A: visual association + lateral parietal (V4/IT + LIP)
  regionA : Module
  -- Region B: spatial attention + lateral parietal (SPL + LIP)
  regionB : Module
  -- Overlap zone: electrodes in both A and B (LIP)
  overlap : Set (Fin numElectrodes)
  overlap_in_A : overlap ⊆ regionA.electrodes
  overlap_in_B : overlap ⊆ regionB.electrodes
  overlap_nonempty : overlap.Nonempty  -- minimum 5 electrodes
  -- Exclusive zones
  exclusiveA : Set (Fin numElectrodes) := regionA.electrodes \ overlap
  exclusiveB : Set (Fin numElectrodes) := regionB.electrodes \ overlap
```

### 2. IQT Prediction: Coexisting Overlapping Self-Threads

```lean
/-- IQT PREDICTION 2a (Observational): Both regions maintain high persistence
    independently during concurrent tasks. -/
def prediction_independent_persistence
    (P : Module → ℝ) (setup : OverlapSetup) : Prop :=
  P setup.regionA > persistence_threshold ∧
  P setup.regionB > persistence_threshold

/-- IQT PREDICTION 2b (Synergy): The overlap zone does NOT create synergistic
    binding between the exclusive zones. Tripartite O-information near zero
    or positive, indicating redundancy-dominated, not synergy-dominated. -/
def prediction_no_synergy
    (oInfo : OverlapSetup → ℝ) (setup : OverlapSetup) : Prop :=
  oInfo setup ≥ -synergy_threshold  -- O-info ≥ 0 means redundancy-dominated

/-- IQT PREDICTION 2c (Perturbational — MOST DECISIVE):
    Single-pulse electrical stimulation (SPES) in Region A's exclusive electrodes
    does NOT evoke responses in Region B's exclusive electrodes.
    If the pulse stays contained while both regions perform complex tasks,
    the regions are causally semi-autonomous. -/
def prediction_spes_containment
    (spes_propagation : Module → Module → ℝ) (setup : OverlapSetup) : Prop :=
  spes_propagation setup.regionA setup.regionB < spes_threshold
```

### 3. Failure Condition

```lean
/-- FAILURE CONDITION for Protocol 2:
    SPES propagates uniformly across both regions, OR persistence metrics
    show anti-correlated switching dynamics (when A is high, B is low). -/
def failure_condition_protocol2
    (spes_propagation : Module → Module → ℝ)
    (P : Module → ℝ → ℝ)  -- P as function of time
    (setup : OverlapSetup) : Prop :=
  -- Either SPES propagates uniformly
  spes_propagation setup.regionA setup.regionB > spes_threshold ∨
  -- Or persistence shows anti-correlated switching
  pearsonCorrelation
    (fun t => P setup.regionA t)
    (fun t => P setup.regionB t) < -switching_threshold
```

### 4. Contrast with Exclusion (IIT)

```lean
/-- IIT's exclusion postulate predicts that only one complex (A∪B) is conscious.
    The "union complex" escape route: IIT proponent could grant independent
    task responses while maintaining A∪B is the single conscious complex.
    The synergy metric (2b) distinguishes:
    - "Two semi-autonomous loci" (IQT): O-info ≥ 0
    - "One irreducible complex with modular responses" (IIT): O-info < 0 -/
-- The SPES result is the most decisive: if a focal pulse stays contained
-- while both regions independently perform complex tasks, exclusion is
-- difficult to maintain.
```

### 5. Connection to Democracy of Diamonds

```lean
/-- Protocol 2 directly tests perspectival relativity (Phase 03c) at Level 1.
    If both overlapping regions sustain independent self-threads (Phase 04a)
    with low cross-propagation, this is evidence for democracy over exclusion. -/
-- Success: two overlapping SelfThreads coexist, each causally semi-autonomous.
-- Failure: regions are causally coupled, consistent with a single complex.
```

## Acceptance Criteria

- [ ] `OverlapSetup` structure compiles
- [ ] Three prediction types (observational, synergy, perturbational) compile
- [ ] Failure condition formally stated
- [ ] IIT contrast documented
- [ ] Connection to democracy of diamonds (Phase 03c) documented

## Notes

- Section 5.2: "This protocol directly targets the overlap divergence between IQT and IIT's exclusion postulate."
- "The SPES result is the most decisive. If a focal electrical pulse in Region A stays contained while both regions independently perform complex tasks, the regions are causally semi-autonomous."
- Protocol 2 requires iEEG patients (epilepsy surgery monitoring).
- This is the primary axis of divergence from IIT.
