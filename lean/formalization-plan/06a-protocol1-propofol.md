# Phase 6a: Protocol 1 — Titrated Propofol Anesthesia Predictions

**Phase:** 06 - Empirical Protocol Predictions
**Track:** Experimental Predictions
**Depends on:** 05b (metrics), 04a (self-threads)
**Unlocks:** Nothing (terminal prediction task)

---

## Goal

State IQT's formal predictions for Protocol 1 (Section 5.1): titrated propofol anesthesia should produce multi-component fragmentation of self-threads, not single-locus degradation.

## What to Formalize

### 1. Propofol Concentration Parameter

```lean
/-- Propofol concentration levels: c₀ (baseline) to c₉ (loss of consciousness). -/
def PropConc := Fin 10

/-- Ordering on concentrations: higher index = deeper anesthesia. -/
instance : LE PropConc := ⟨fun a b => a.val ≤ b.val⟩
```

### 2. Module-Specific Persistence Under Anesthesia

```lean
/-- The persistence of each module as a function of propofol concentration.
    P_j(c_k): persistence of module j at concentration step k. -/
noncomputable def persistenceAtConc
    (bridge : EffectiveBridge Reg N_fund)
    (ω : PropConc → CompatibleFamily N_fund)  -- state depends on concentration
    (j : Module) (k : PropConc) : ℝ :=
  persistenceAUC bridge (ω k) j standardWindows
```

### 3. IQT Prediction: Multi-Component Fragmentation

```lean
/-- IQT PREDICTION 1a: Modules decline at different rates.
    Prefrontal declines earliest; primary sensory declines last. -/
def prediction_differential_decline
    (P : Module → PropConc → ℝ) (prefrontal sensory : Module) : Prop :=
  ∃ k : PropConc,
    P prefrontal k < persistence_threshold ∧
    P sensory k > persistence_threshold

/-- IQT PREDICTION 1b: Partial fragmentation at intermediate depths.
    Some modules retain high P while others have collapsed. -/
def prediction_partial_fragmentation
    (P : Module → PropConc → ℝ) (modules : List Module) : Prop :=
  ∃ k : PropConc, ∃ m₁ m₂ : Module,
    m₁ ∈ modules ∧ m₂ ∈ modules ∧
    P m₁ k > persistence_threshold ∧
    P m₂ k < persistence_threshold

/-- IQT PREDICTION 1c: Conditional independence at intermediate depths.
    Perturbations to module A do not propagate to module B. -/
def prediction_conditional_independence
    (P : Module → PropConc → ℝ)
    (propagation_effect : Module → Module → PropConc → ℝ) : Prop :=
  ∃ k : PropConc, ∃ m₁ m₂ : Module,
    P m₁ k > persistence_threshold ∧
    P m₂ k > persistence_threshold ∧
    propagation_effect m₁ m₂ k < propagation_threshold  -- partial η² < 0.05
```

### 4. Failure Condition

```lean
/-- FAILURE CONDITION for Protocol 1:
    P_j decline in parallel across all modules in ≥80% of subjects.
    Within-subject Pearson r > 0.9 across module pairs. -/
def failure_condition_protocol1
    (P : Module → PropConc → ℝ) (modules : List Module) : Prop :=
  ∀ m₁ m₂ : Module, m₁ ∈ modules → m₂ ∈ modules →
    pearsonCorrelation (fun k => P m₁ k) (fun k => P m₂ k) > 0.9

/-- If the failure condition holds, IQT's bridge hypothesis
    (multi-component self-threads) is falsified. -/
-- Note: this falsifies the CONJUNCTION (QI ∧ bridge ∧ operationalization),
-- not QI alone.
```

### 5. Contrast with Single-Locus Views

```lean
/-- Single-locus prediction (IIT/GNW-compatible):
    All modules decline in lockstep, with no partially-fragmented intermediate state.
    Equivalent to failure_condition_protocol1. -/
-- If data matches this pattern, it supports single-locus views over IQT's democracy.
```

## Acceptance Criteria

- [ ] Prediction types for differential decline, partial fragmentation, and conditional independence compile
- [ ] Failure condition is formally stated
- [ ] Contrast with single-locus prediction documented
- [ ] Connection to self-thread formalism (Phase 04a) documented

## Notes

- Section 5.1: "AUC_P_j metrics decline at different rates and thresholds across modules. Prefrontal declines earliest; primary sensory modules decline last."
- The failure condition is: "Within-subject correlation of persistence trajectories > 0.9 across module pairs in 80%+ of subjects."
- Confound controls: propofol-induced frontal alpha (controlled by P = TMI × d_eff), pharmacokinetic non-uniformity (controlled by sevoflurane replication).
