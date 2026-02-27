# Phase 5b: Empirical Metric Type Signatures

**Phase:** 05 - Effective Theory Bridge
**Track:** Neural-Scale Formalism
**Depends on:** 05a (effective bridge), 04a (self-threads), 03b (unity functional)
**Unlocks:** 06a-06c (protocol predictions)

---

## Goal

Define the type signatures for IQT's three core empirical metrics (P, K, R) from Section 5.0.1. These metrics are computable functionals of the effective state and serve as the interface between the formalism and experimental data.

## What to Formalize

### 1. Thread-Persistence Metric P_j(w)

From Section 5.0.1: `P_j(w) = TMI_j(w) * d_eff_j(w)`

```lean
/-- Temporal mutual information between successive windows of width w
    for module j. TMI measures predictability. -/
noncomputable def temporalMutualInfo
    (bridge : EffectiveBridge Reg N_fund)
    (ω : CompatibleFamily N_fund)
    (j : Module) (w : ℝ) : ℝ := sorry

/-- Effective dimensionality via participation ratio of the covariance
    eigenspectrum. d_eff measures signal complexity/richness. -/
noncomputable def effectiveDimensionality
    (bridge : EffectiveBridge Reg N_fund)
    (ω : CompatibleFamily N_fund)
    (j : Module) (w : ℝ) : ℝ := sorry

/-- Thread-persistence metric: the product TMI × d_eff.
    Rewards structured, high-dimensional stability.
    "Predictable AND complex." -/
noncomputable def persistence
    (bridge : EffectiveBridge Reg N_fund)
    (ω : CompatibleFamily N_fund)
    (j : Module) (w : ℝ) : ℝ :=
  temporalMutualInfo bridge ω j w * effectiveDimensionality bridge ω j w

/-- Multi-scale persistence summary: area under the P(w) curve. -/
noncomputable def persistenceAUC
    (bridge : EffectiveBridge Reg N_fund)
    (ω : CompatibleFamily N_fund)
    (j : Module) (windows : List ℝ) : ℝ :=
  -- ∫ P_j(w) dw approximated over the window list
  sorry
```

### 2. Cross-Module Coherence Metric K_jl

```lean
/-- Cross-module coherence: phase synchronization between modules j and l.
    Uses debiased weighted phase-lag index (dwPLI).
    Approximates cross-boundary correlator strength. -/
noncomputable def crossModuleCoherence
    (bridge : EffectiveBridge Reg N_fund)
    (ω : CompatibleFamily N_fund)
    (j l : Module) : ℝ := sorry

/-- K_jl is a proxy for the quantum mutual information between modules. -/
-- Connection: high K across all module pairs implies high unity U
-- for the brain-scale diamond.
```

### 3. Readout Dominance Metric R

```lean
/-- Readout dominance: directed information from prefrontal (narrative self-thread)
    to motor cortex (report channel).
    R = DI(prefrontal → motor). -/
noncomputable def readoutDominance_metric
    (bridge : EffectiveBridge Reg N_fund)
    (ω : CompatibleFamily N_fund)
    (prefrontal motor : Module) : ℝ := sorry
```

### 4. Connection to Formal Structures

Document how the metrics relate to the abstract formalism:

```lean
/-- P_j approximates self-thread persistence for module j.
    High P_j(w) for a range of w means module j sustains a structured quality-stream.
    (Connection: Phase 04a SelfThread.persistent.) -/

/-- K_jl approximates cross-boundary correlator strength between modules j and l.
    High K across module pairs implies high unity of the brain-scale diamond.
    (Connection: Phase 03b unity functional.) -/

/-- R approximates the readout dominance of the narrative self-thread.
    High R means the narrative operator controls the report channel.
    (Connection: Phase 04b NarrativeOperator.readout_dominance.) -/
```

### 5. Metric Properties

```lean
/-- TMI confound control: propofol increases raw TMI (slow oscillations)
    but collapses d_eff (low-dimensional). The product P = TMI × d_eff
    correctly declines under anesthesia. -/
-- This is a design property of the metric, not a provable theorem.

/-- K is robust to volume conduction via debiased phase-lag index. -/
-- Property of the dwPLI estimator.

/-- R uses directed information, not correlation, to capture causal flow. -/
-- Property of the transfer entropy / Granger causality estimator.
```

### 6. Module Type

```lean
/-- A cortical module: a subset of electrodes / effective observables.
    Section 5.0.1 uses J = 5 modules: visual, auditory, somatosensory,
    prefrontal/executive, default-mode. -/
structure Module where
  name : String
  electrodes : Set (Fin numElectrodes)
  -- The module's effective algebra is a subalgebra of the full effective algebra
  subalgebra : StarAlgHom moduleAlgebra fullAlgebra
```

## Acceptance Criteria

- [ ] `persistence` (P_j), `crossModuleCoherence` (K_jl), and `readoutDominance_metric` (R) type signatures compile
- [ ] `temporalMutualInfo` and `effectiveDimensionality` are factored out
- [ ] `persistenceAUC` multi-scale summary is defined
- [ ] `Module` structure is defined
- [ ] Connections to abstract structures (self-threads, unity, narrative operator) are documented

## Notes

- The paper says (Section 5.0.1): "P rewards structured, high-dimensional stability — predictable AND complex. This avoids the confound where anesthetic-induced slow oscillations increase raw predictability."
- All metrics are computed at the effective scale (Phase 05a). They are "computable functionals of the restricted state ω_eff."
- The specific estimators (dwPLI, participation ratio, transfer entropy) are signal-processing choices, not formal mathematical structures. The Lean formalization captures the type-level interface, not the estimator implementation.
