# Phase 1b: C*-Algebras and States

**Phase:** 01 - AQFT Foundations & Infrastructure
**Track:** Core Mathematical Infrastructure
**Depends on:** 01a (regions)
**Unlocks:** 01c, 01d, 02a

---

## Goal

Define or bind to the C*-algebra infrastructure needed for IQT. The central objects are unital C*-algebras and states (positive normalized linear functionals) on them. Mathlib has partial C*-algebra support; PhysLean may add physics-specific structures. The gap analysis and binding strategy is the main deliverable.

## What to Formalize

### 1. C*-Algebra (Use Mathlib's Existing Definitions)

Mathlib provides:
- `Analysis.NormedSpace.Star.CStarAlgebra` (or its successor in current Mathlib)
- Star algebras, Banach algebras, norm conditions

Identify the Mathlib type corresponding to a unital C*-algebra and alias it for IQT use.

### 2. States on a C*-Algebra

The paper defines (Appendix B):

```lean
structure CStarState (B : CStarAlg) where
  toFun : B →ₗ[ℂ] ℂ       -- linear functional
  pos   : ∀ a, 0 ≤ toFun (star a * a)  -- positivity
  norm  : toFun 1 = 1       -- normalization
```

This is not yet bundled in Mathlib. Tasks:
- Check if `Mathlib.Analysis.InnerProductSpace.Positive` or `Mathlib.Analysis.NormedSpace.Star` provides ingredients
- Define `CStarState` as a structure
- Prove basic properties: linearity, positivity of identity, Cauchy-Schwarz for states

### 3. Star-Algebra Homomorphisms

Needed for isotony embeddings. Mathlib has `StarAlgHom`. Verify it provides:
- `*`-preservation: `φ(a*) = φ(a)*`
- Multiplicativity: `φ(ab) = φ(a)φ(b)`
- Unit preservation: `φ(1) = 1`

### 4. State Restriction (Pullback)

Given an injective `*`-homomorphism `ι : A(D₁) ↪ A(D₂)` and a state `ω` on `A(D₂)`, the restricted state is `ω ∘ ι`. This is the fundamental operation underlying the state presheaf.

```lean
def restrictState {B₁ B₂ : CStarAlg} (ι : B₁ →⋆ₐ[ℂ] B₂) (ω : CStarState B₂) : CStarState B₁ :=
  { toFun := ω.toFun.comp ι.toLinearMap
    pos := ... -- follows from ι preserving star and product
    norm := ... -- follows from ι preserving 1
  }
```

## Mathlib/PhysLean Resources

- `Mathlib.Analysis.NormedSpace.Star.Basic`
- `Mathlib.Algebra.Star.Basic`
- `Mathlib.Algebra.Algebra.Hom`
- `PhysLean` — check if it provides any AQFT-relevant structures

## Acceptance Criteria

- [ ] Working alias/wrapper for Mathlib's C*-algebra type
- [ ] `CStarState` structure compiles
- [ ] `restrictState` compiles and satisfies the pullback property
- [ ] Proof that restriction of a state is a state
- [ ] Finite-dimensional instance: `Matrix n n ℂ` as a C*-algebra with trace-state as example

## Challenges

- Mathlib's C*-algebra library is under active development; the API may be in flux
- The paper operates at a level of abstraction (general C*-algebras) but the concrete examples (Section 0) and neural applications (Section 2.6) use finite-dimensional algebras. Consider providing both an abstract interface and a finite-dimensional specialization.
- Type III factors (Section 0.1) are beyond Mathlib's current scope. Flag but do not attempt.

## Notes

- The paper explicitly notes (Appendix B): "Mathlib does not bundle [CStarState] as a type yet; define as a structure."
- For the finite-dimensional toy model (Section 2.4), states correspond to density matrices. Providing a `DensityMatrix` ↔ `CStarState` bridge for `Matrix n n ℂ` is valuable.
