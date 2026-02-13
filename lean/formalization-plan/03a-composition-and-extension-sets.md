# Phase 3a: Composition Problem and Extension Sets

**Phase:** 03 - Composition & Unity Functional
**Track:** Composition Theory
**Depends on:** 01c (net of algebras), 01d (state presheaf), 01e (toy models)
**Unlocks:** 03b (unity functional)

---

## Goal

Formalize the composition problem from Section 3.1-3.2: given the states of two subregions, characterize the set of possible joint states. This is the mathematical formulation of "the whole is more than the sum of its parts."

## What to Formalize

### 1. Marginal Consistency

Given regions D₁, D₂ with D₁ ≤ D (and D₂ ≤ D), a state on A(D) is *consistent* with states ω₁ on A(D₁) and ω₂ on A(D₂) if its restrictions match:

```lean
/-- A state on the composite region consistent with given marginals. -/
def ConsistentState (N : LocalNet Reg) {D₁ D₂ D : Reg}
    (h₁ : D₁ ≤ D) (h₂ : D₂ ≤ D)
    (ω₁ : StateSpace N D₁) (ω₂ : StateSpace N D₂) : Type :=
  { ω : StateSpace N D //
    StateSpace.restrict N h₁ ω = ω₁ ∧
    StateSpace.restrict N h₂ ω = ω₂ }
```

### 2. Extension Set

The extension set is the collection of all consistent joint states:

```lean
/-- The extension set: all states on D consistent with marginals ω₁, ω₂.
    From Section 3.2: Ext(ω₁, ω₂; D) is generally not a singleton. -/
def ExtensionSet (N : LocalNet Reg) {D₁ D₂ D : Reg}
    (h₁ : D₁ ≤ D) (h₂ : D₂ ≤ D)
    (ω₁ : StateSpace N D₁) (ω₂ : StateSpace N D₂) : Set (StateSpace N D) :=
  { ω | StateSpace.restrict N h₁ ω = ω₁ ∧ StateSpace.restrict N h₂ ω = ω₂ }
```

### 3. Non-Uniqueness of Extensions

The key observation from Section 3.1: knowing the parts does not determine the whole. Different extensions correspond to different correlation structures.

```lean
/-- The extension set can have more than one element.
    (Demonstrated on the three-qubit model.) -/
theorem extension_nonunique :
    ∃ (ω₁ : StateSpace threeQubitNet ThreeQubitRegion.A)
      (ω₂ : StateSpace threeQubitNet ThreeQubitRegion.B),
    Set.Nontrivial (ExtensionSet threeQubitNet
      (show ThreeQubitRegion.A ≤ ThreeQubitRegion.AB from ...)
      (show ThreeQubitRegion.B ≤ ThreeQubitRegion.AB from ...)
      ω₁ ω₂) := by
  -- The GHZ state and the maximally mixed state have the same single-qubit marginals
  -- but are different states on AB.
  sorry
```

### 4. Composition Datum (Open Problem)

The paper identifies this as an open problem (Section 3.4): characterize the minimal data D_comp such that ω₁ + ω₂ + D_comp uniquely determines the joint state. This is related to the quantum marginal problem.

```lean
/-- The composition datum: additional information needed to select
    a unique element of the extension set.
    STATUS: Open problem. The type is left abstract. -/
def CompositionDatum (N : LocalNet Reg) {D₁ D₂ D : Reg}
    (h₁ : D₁ ≤ D) (h₂ : D₂ ≤ D)
    (ω₁ : StateSpace N D₁) (ω₂ : StateSpace N D₂) : Type := sorry
```

### 5. Cross-Boundary Correlators

The "missing ingredient" between parts and whole is the pattern of mixed correlators:

```lean
/-- Cross-boundary correlations: the expectation values of observables
    in A(D) that are not in the image of A(D₁) or A(D₂).
    These "belong to the whole but not to either part." -/
-- (This is a conceptual marker; the formal content is in the
-- extension set definition above.)
```

## Acceptance Criteria

- [ ] `ConsistentState` and `ExtensionSet` compile
- [ ] `extension_nonunique` is stated on the three-qubit model
- [ ] The distinction between "determined by parts" vs "requires composition datum" is formally clear
- [ ] The open-problem status of `CompositionDatum` is documented

## Notes

- The paper says (Section 3.1): "The restrictions ω₁ and ω₂ do not determine ω_D. The missing information is the pattern of mixed correlators."
- This connects to the quantum marginal problem (Klyachko 2004, Schilling et al. 2013).
- For finite-dimensional systems, the extension set is a convex body.
