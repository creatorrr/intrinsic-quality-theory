# Phase 3b: The Unity Functional

**Phase:** 03 - Composition & Unity Functional
**Track:** Composition Theory
**Depends on:** 03a (composition), 01e (toy models)
**Unlocks:** 04a (self-threads), 05b (metric formalization)

---

## Goal

Formalize the unity functional U(D) from Section 3.3 — the measure of how much a diamond's quality exceeds the sum of its parts. U is defined as the minimum quantum mutual information over all bipartitions.

## What to Formalize

### 1. Von Neumann Entropy (Finite-Dimensional)

```lean
/-- Von Neumann entropy of a density matrix: S(ρ) = -Tr(ρ log ρ). -/
noncomputable def vonNeumannEntropy (ρ : DensityMatrix n) : ℝ :=
  -(ρ.mat * ρ.mat.log).trace.re
  -- Or via eigenvalues: -∑ λ_i * log(λ_i)
```

### 2. Quantum Mutual Information

```lean
/-- Quantum mutual information for a bipartition A|B of region D.
    I(A:B) = S(ρ_A) + S(ρ_B) - S(ρ_AB). -/
noncomputable def quantumMutualInfo
    (ρ_AB : DensityMatrix (n * m))
    (ρ_A : DensityMatrix n) (ρ_B : DensityMatrix m) : ℝ :=
  vonNeumannEntropy ρ_A + vonNeumannEntropy ρ_B - vonNeumannEntropy ρ_AB
```

### 3. Bipartitions of a Region

```lean
/-- A bipartition of region D into subregions D₁, D₂. -/
structure Bipartition (Reg : Type) [Preorder Reg] (D : Reg) where
  D₁ : Reg
  D₂ : Reg
  sub₁ : D₁ ≤ D
  sub₂ : D₂ ≤ D
  -- D is the causal completion of D₁ ∪ D₂ (the smallest region containing both)
  covers : ∀ D' : Reg, D₁ ≤ D' → D₂ ≤ D' → D ≤ D'
```

### 4. Correlation Excess

```lean
/-- Correlation excess for a specific bipartition:
    the quantum mutual information I(D₁ : D₂). -/
noncomputable def correlationExcess (N : LocalNet Reg)
    (ω : CompatibleFamily N) (D : Reg) (bp : Bipartition Reg D) : ℝ :=
  quantumMutualInfo
    (stateToMatrix (ω.state D))
    (stateToMatrix (ω.state bp.D₁))
    (stateToMatrix (ω.state bp.D₂))
```

### 5. The Unity Functional

```lean
/-- The unity functional U(D): minimum correlation excess over all bipartitions.
    U(D; ω) = min_{bipartitions} I(D₁ : D₂).
    From Section 3.3: "the minimum over all bipartitions." -/
noncomputable def unity (N : LocalNet Reg) (ω : CompatibleFamily N)
    (D : Reg) (partitions : Set (Bipartition Reg D)) : ℝ :=
  ⨅ bp ∈ partitions, correlationExcess N ω D bp
```

### 6. Properties of U

From Section 3.3 (P1-P4):

```lean
/-- P1: U vanishes for product states. -/
theorem unity_vanishes_product (N : LocalNet Reg) (ω : CompatibleFamily N)
    (D : Reg) (bp : Bipartition Reg D)
    (h : isProductState (ω.state D) bp) :
    correlationExcess N ω D bp = 0 := by
  sorry

/-- P2: U increases with cross-boundary dependence.
    (This is a property of quantum mutual information.) -/

/-- P3: Coarse-graining monotonicity.
    U at the effective scale ≤ U at the fundamental scale.
    Follows from the data-processing inequality. -/
theorem unity_coarsegraining_monotone
    (N_fund N_eff : LocalNet Reg) (ω : CompatibleFamily N_fund)
    (embed : ∀ D, StarAlgHom (N_eff.algebra D) (N_fund.algebra D))
    (D : Reg) (bp : Bipartition Reg D) :
    correlationExcess N_eff (coarseGrain ω embed) D bp ≤
    correlationExcess N_fund ω D bp := by
  sorry

/-- P4: Compatible with democracy.
    U is defined for every diamond. Multiple overlapping diamonds can
    simultaneously have high U. No exclusion step. -/
-- (This is a property of the definition, not a theorem to prove.)
```

### 7. Toy Model Values

```lean
/-- Three-qubit GHZ state: U = 1 bit. -/
theorem unity_ghz :
    unity threeQubitNet ghzFamily ThreeQubitRegion.ABC allBipartitions = 1 := by
  sorry

/-- Three-qubit product state: U = 0. -/
theorem unity_product :
    unity threeQubitNet productFamily ThreeQubitRegion.ABC allBipartitions = 0 := by
  sorry
```

## Acceptance Criteria

- [ ] `vonNeumannEntropy` defined for finite-dimensional density matrices
- [ ] `quantumMutualInfo` defined
- [ ] `Bipartition` structure compiles
- [ ] `unity` functional defined as infimum over bipartitions
- [ ] P1 (vanishing for products) stated and proved or outlined
- [ ] P3 (coarse-graining monotonicity) stated
- [ ] Toy values for GHZ and product states stated

## Challenges

- Von Neumann entropy requires matrix logarithm or eigenvalue decomposition — Mathlib support may be limited
- The `noncomputable` tag is expected for entropy-related definitions
- The infimum over bipartitions requires the set of bipartitions to be well-behaved (finite or filtered)

## Notes

- The paper explicitly scopes U to finite dimensions: "The definition uses von Neumann entropy, which is well-defined for the effective finite-dimensional algebra."
- At the fundamental level (Type III algebras), U would require Araki relative entropy — flagged as an open problem (Section 3.4).
- The distinction from IIT's Phi: "U is defined on the state, not on the cause-effect structure. U does not trigger exclusion."
