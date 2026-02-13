# Phase 6c: Protocol 3 — Psychedelic Temporal Phenomenology

**Phase:** 06 - Empirical Protocol Predictions
**Track:** Experimental Predictions (Diamond Geometry Test)
**Depends on:** 05b (metrics), 04a (self-threads)
**Unlocks:** Nothing (terminal prediction task)

---

## Goal

State IQT's formal predictions for Protocol 3 (Section 5.3): the shape of the effective causal diamond determines the character of temporal experience. Different psychedelic compounds should shift the persistence peak in predictable, compound-specific ways.

## What to Formalize

### 1. Persistence Curve Shape

```lean
/-- The persistence curve P_j(w) as a function of window width w.
    The peak position of this curve tracks the effective temporal
    integration window. -/
noncomputable def persistenceCurve
    (bridge : EffectiveBridge Reg N_fund)
    (ω : CompatibleFamily N_fund)
    (j : Module) : ℝ → ℝ :=
  fun w => persistence bridge ω j w

/-- Peak position: the window width w* at which P_j is maximized. -/
noncomputable def peakPosition
    (curve : ℝ → ℝ) : ℝ :=
  -- argmax_w P_j(w)
  sorry
```

### 2. Compound-Specific Predictions

```lean
/-- Psychedelic compound type. -/
inductive Compound
  | psilocybin    -- 5-HT2A agonist
  | ketamine      -- NMDA antagonist
  | dmt           -- 5-HT2A agonist (short-acting)
  | midazolam     -- GABAa agonist (active control)
  | baseline      -- no drug

/-- IQT PREDICTION 3a (Psilocybin): Peak shifts toward LONGER windows.
    Enhanced recurrent coupling → larger temporal depth → expanded present.
    The "time dilates" phenomenology. -/
def prediction_psilocybin
    (peak : Compound → ℝ) : Prop :=
  peak Compound.psilocybin > peak Compound.baseline

/-- IQT PREDICTION 3b (Ketamine): Peak shifts toward SHORTER windows.
    Disrupted recurrent coupling → smaller temporal depth → fragmented time.
    The "time fragments" phenomenology. -/
def prediction_ketamine
    (peak : Compound → ℝ) : Prop :=
  peak Compound.ketamine < peak Compound.baseline

/-- IQT PREDICTION 3c (DMT): Curve FLATTENS — no preferred timescale.
    Flattened timescale hierarchy → time dissolves.
    The peak height drops but no single dominant shift direction. -/
def prediction_dmt
    (curve : Compound → ℝ → ℝ) : Prop :=
  -- The variance of the curve decreases: it becomes flat.
  curveVariance (curve Compound.dmt) < curveVariance (curve Compound.baseline)

/-- IQT PREDICTION 3d (Midazolam, active control):
    Curve scales VERTICALLY without shifting the peak.
    Dissociates arousal from integration-window changes.
    The peak position stays the same; only the amplitude changes. -/
def prediction_midazolam
    (peak : Compound → ℝ) (amplitude : Compound → ℝ) : Prop :=
  |peak Compound.midazolam - peak Compound.baseline| < shift_threshold ∧
  amplitude Compound.midazolam < amplitude Compound.baseline
```

### 3. The Mapping: Diamond Geometry → Temporal Phenomenology

```lean
/-- The shape-phenomenology mapping (Section 2.7):
    Diamond geometry determines experience character.
    - Spatially wide + temporally shallow → panoramic space + fleeting time
    - Wider temporal depth → expanded present
    - Narrower temporal depth → fragmented time
    - Flat timescale hierarchy → dissolved time -/
-- This is the conceptual bridge between:
--   1. The effective diamond's shape (temporal depth parameter)
--   2. The persistence curve's peak position
--   3. The reported temporal phenomenology
```

### 4. Self-Report Correlation

```lean
/-- The peak position should correlate with self-reported temporal experience
    across compounds. -/
def prediction_selfreport_correlation
    (peak : Compound → ℝ)
    (temporal_report : Compound → ℝ) : Prop :=
  pearsonCorrelation peak temporal_report > correlation_threshold
```

### 5. Failure Condition

```lean
/-- FAILURE CONDITION for Protocol 3:
    Peak position does not differ across compounds, OR shows no correlation
    with self-reported temporal experience. -/
def failure_condition_protocol3
    (peak : Compound → ℝ)
    (temporal_report : Compound → ℝ) : Prop :=
  -- No difference across compounds
  (∀ c : Compound, |peak c - peak Compound.baseline| < shift_threshold) ∨
  -- No correlation with self-report
  |pearsonCorrelation peak temporal_report| < correlation_threshold
```

### 6. Uniqueness of This Prediction

```lean
/-- Neither IIT nor GNW generates multi-scale temporal structure predictions
    in this form. This is a unique discriminating prediction of IQT. -/
-- IIT: Phi is defined on the cause-effect structure, not on temporal geometry.
-- GNW: Workspace dynamics without structural account of passage.
-- IQT: Temporal phenomenology derived from diamond geometry via identity thesis.
```

## Acceptance Criteria

- [ ] `Compound` type defined
- [ ] Four compound-specific predictions compile
- [ ] `peakPosition` function defined (even noncomputable)
- [ ] Self-report correlation prediction stated
- [ ] Failure condition formally stated
- [ ] Uniqueness of prediction documented

## Notes

- Section 5.3: "IQT predicts that the peak of the multi-scale persistence curve tracks the effective temporal integration window."
- Protocol 3 requires psychedelic research licensing (Section 7).
- The midazolam control is crucial: it dissociates arousal from integration-window changes.
- Section 2.7: "Change the shape and you change the experience. Psilocybin widens temporal depth (time dilates). Ketamine narrows it (time fragments). DMT flattens the timescale hierarchy (time dissolves)."
