# Phase 1a: Preorder / Poset of Regions

**Phase:** 01 - AQFT Foundations & Infrastructure
**Track:** Core Mathematical Infrastructure
**Depends on:** Nothing (root task)
**Unlocks:** 01b, 01c, 01d, 02a, 02b

---

## Goal

Define the region structure `(Reg, <=)` that underpins the entire formalization. In IQT, bounded spacetime regions (causal diamonds) form a directed poset under inclusion. All algebraic and presheaf structures are indexed over this poset.

## What to Formalize

### 1. Region Type with Preorder

```lean
-- Regions as an abstract type with a preorder (reflexive + transitive).
-- Antisymmetry (making it a poset) is optional but assumed in the paper.
variable (Reg : Type) [Preorder Reg]
```

### 2. Directedness

The paper assumes `(Reg, <=)` is directed: for any two regions D1, D2 there exists a region D3 with D1 <= D3 and D2 <= D3 (their causal completion). This is used in the composition story (Section 3).

```lean
-- Directedness: any two regions have an upper bound.
class Directed (Reg : Type) [Preorder Reg] where
  upper_bound : ∀ D₁ D₂ : Reg, ∃ D₃, D₁ ≤ D₃ ∧ D₂ ≤ D₃
```

### 3. Finite Multiplicity (Optional)

IQT notes that in causal-set spacetime, the number of sub-diamonds in any bounded region is finite (Box 2.A). This may be useful later for constructive proofs.

```lean
-- Optional: finite sub-diamond structure.
class FinitelyBounded (Reg : Type) [Preorder Reg] where
  finite_sub : ∀ D : Reg, Finite { D' : Reg // D' ≤ D }
```

## Mathlib Resources

- `Mathlib.Order.Preorder` for `Preorder` typeclass
- `Mathlib.Order.Directed` for directed sets
- `Mathlib.Order.PartialOrder` if antisymmetry is needed

## Acceptance Criteria

- [ ] `Reg` is a `Preorder` that compiles with Lean 4 + Mathlib
- [ ] `Directed` class is stated and usable
- [ ] At least one concrete instance: finite lattice of sub-diamonds (e.g., powerset of a finite set ordered by inclusion) to serve as a test case
- [ ] Toy instance with 3-4 nested regions for smoke tests

## Notes

- Keep the definition abstract. The paper explicitly says the framework does not require causal sets specifically — any theory with local algebras and state restrictions works (Section 2.0).
- The concrete "causal diamond" interpretation is a model, not the definition.
