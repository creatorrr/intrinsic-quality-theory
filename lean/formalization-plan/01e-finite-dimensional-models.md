# Phase 1e: Finite-Dimensional Toy Models

**Phase:** 01 - AQFT Foundations & Infrastructure
**Track:** Concrete Instances & Testing
**Depends on:** 01a, 01b, 01c, 01d
**Unlocks:** 02c (convergence on concrete examples), 03b (unity functional computation)

---

## Goal

Build concrete finite-dimensional instances of the abstract AQFT framework to serve as test beds. The paper's Section 2.4 provides a three-qubit toy model that illustrates isotony, perspectival relativity, and the composition problem. Formalizing it provides:

1. Smoke tests for all Phase 01 definitions
2. Concrete examples for Phase 02 convergence proofs
3. Computable unity functional values for Phase 03

## What to Formalize

### 1. Matrix Algebra as C*-Algebra

```lean
/-- Matrix algebra M_n(ℂ) as a C*-algebra.
    Mathlib should provide this via `Matrix.instCStarAlgebra` or similar. -/
instance : CStarAlgebra (Matrix (Fin n) (Fin n) ℂ) := ...
```

### 2. Density Matrices as States

```lean
/-- A density matrix: positive semidefinite, trace 1. -/
structure DensityMatrix (n : ℕ) where
  mat : Matrix (Fin n) (Fin n) ℂ
  pos : mat.PosSemidef
  trace_one : mat.trace = 1

/-- Every density matrix induces a C*-state via ω(A) = Tr(ρA). -/
def DensityMatrix.toState (ρ : DensityMatrix n) : CStarState (Matrix (Fin n) (Fin n) ℂ) :=
  { toFun := fun A => (ρ.mat * A).trace
    pos := ...   -- Tr(ρ · a*a) ≥ 0 by positive semidefiniteness
    norm := ...  -- Tr(ρ · I) = Tr(ρ) = 1
  }
```

### 3. Partial Trace as State Restriction

```lean
/-- Partial trace over the second subsystem. -/
def partialTrace₂ (ρ : DensityMatrix (n * m)) : DensityMatrix n := ...

/-- Partial trace corresponds to state restriction via the subalgebra embedding. -/
theorem partialTrace_eq_restrict (ρ : DensityMatrix (n * m))
    (ι : Matrix (Fin n) (Fin n) ℂ →⋆ₐ[ℂ] Matrix (Fin (n*m)) (Fin (n*m)) ℂ) :
    (partialTrace₂ ρ).toState = restrictState ι ρ.toState := by
  sorry
```

### 4. Three-Qubit Toy Model (Section 2.4)

```lean
/-- The three-qubit region poset: {A, B, C, AB, BC, AC, ABC}. -/
inductive ThreeQubitRegion
  | A | B | C | AB | BC | AC | ABC

/-- Inclusion ordering. -/
instance : Preorder ThreeQubitRegion := ...

/-- The local net for three qubits: each region gets the appropriate matrix algebra. -/
def threeQubitNet : LocalNet ThreeQubitRegion := ...

/-- GHZ state. -/
def ghzState : DensityMatrix 8 := ...

/-- Maximally mixed state. -/
def mixedState : DensityMatrix 8 := ...

/-- Key result: GHZ and mixed have identical single-qubit reductions. -/
theorem local_quality_equal :
    restrictState ι_A_ABC (ghzState.toState) =
    restrictState ι_A_ABC (mixedState.toState) := by
  sorry

/-- Key result: GHZ and mixed differ on the full three-qubit algebra. -/
theorem global_quality_different :
    ghzState.toState ≠ mixedState.toState := by
  sorry
```

## Acceptance Criteria

- [ ] `DensityMatrix` type compiles with positivity and trace-1 conditions
- [ ] `toState` conversion from density matrix to C*-state works
- [ ] Partial trace is defined and proven equivalent to algebraic restriction
- [ ] `ThreeQubitRegion` poset compiles
- [ ] `threeQubitNet` instantiates `LocalNet`
- [ ] The two key theorems (`local_quality_equal`, `global_quality_different`) are stated

## Notes

- The paper says (Section 2.4): "Same local qualities, different global quality: Both states yield ρ_A = I/2. Yet ρ_ABC differs: tripartite coherence is present in the GHZ state and absent in the mixture."
- This is the simplest non-trivial demonstration of perspectival relativity and composition via correlation structure.
- These concrete instances will be reused in Phase 03 (unity functional) and Phase 02 (testing convergence on a concrete net).
