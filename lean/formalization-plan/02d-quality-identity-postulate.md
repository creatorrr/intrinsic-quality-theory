# Phase 2d: Quality Identity Postulate (QI)

**Phase:** 02 - Constraint Convergence Theorem
**Track:** Interpretive Layer
**Depends on:** 02b (convergence theorems)
**Unlocks:** 03a, 04a, 05a

---

## Goal

State the Quality Identity postulate as a formal axiom. QI is NOT a theorem — it is the metaphysical bridge from mathematics to phenomenology. The formalization must clearly separate the mathematical convergence result (proved) from the identity postulate (axiomatized).

## What to Formalize

### 1. Phenomenal Quality as a Primitive

```lean
/-- Phenomenal quality: an abstract primitive type associated to each region.
    QI identifies this with the algebra-state pair. This is NOT derivable. -/
opaque PhenQual (D : Reg) : Type

/-- The Quality Identity postulate: phenomenal quality IS the local state.
    This is an axiom, not a theorem. -/
axiom quality_identity (N : LocalNet Reg) (ω : CompatibleFamily N) (D : Reg) :
    PhenQual D ≃ StateSpace N D
```

### 2. Alternative: QI as a Structure

Rather than using `axiom`, model QI as an additional structure that a theory can adopt or not:

```lean
/-- A theory that adopts the Quality Identity postulate. -/
structure QITheory (Reg : Type) [Preorder Reg] extends LocalNet Reg where
  -- The actual state of the world
  state : CompatibleFamily toLocalNet
  -- QI: phenomenal quality at D is identified with the local state at D
  quality : ∀ D, ω.state D   -- "the quality at D is the local state at D"
```

### 3. Scope Hygiene Lemma

The paper insists on separating what is proved from what is postulated:

```lean
/-- The convergence theorem is mathematics.
    QI is a separate postulate connecting the converged object to phenomenal quality.
    This comment documents the logical separation. -/

/-- What the math proves: any admissible intrinsic assignment reduces to Ω. -/
-- (This is Proposition 2 from Phase 02b)

/-- What QI adds: Ω _is_ phenomenal quality. -/
-- (This is the axiom above)

/-- What QI does NOT prove: that consciousness exists, or that any specific system
    is conscious. Those are Level 1/2 questions addressed in Phase 04. -/
```

## Acceptance Criteria

- [ ] QI is stated as an axiom or opaque structure, clearly separated from theorems
- [ ] The logical independence of QI from the convergence theorems is documented
- [ ] The three-level distinction (Level 0: Quality, Level 1: Experience, Level 2: Report) is sketched as types or propositions

## Notes

- The paper says (Section 1.1): "QI is an axiom connecting a primitive PhenQual(D) to Q(D). It is not derivable from C1-C4."
- The formalization should make this crystal clear. A reader of the Lean code should immediately see: convergence = theorem, QI = postulate.
- This task is lightweight in terms of Lean code but conceptually important for the structure of the formalization.
