import Mathlib.Order.Directed
import Mathlib.Data.Set.Finite.Basic

/-!
# Regions — Phase 01a

Bounded spacetime regions form the index set for IQT's algebraic and presheaf
structures. This file defines:

1. **Region typeclass assumptions**: `Preorder` + `IsDirected` (upward).
2. **`FinitelyBounded`**: optional finite-sub-diamond axiom from Box 2.A.
3. **Concrete instances** for smoke tests:
   - `RegionFin n`: a finite linear chain of `n` nested regions.
   - `RegionPowerset α`: powerset of a finite type, ordered by inclusion.

## Design notes

The paper (Section 2.0) says: "the framework does not require causal sets
specifically — any theory with local algebras and state restrictions works."
We therefore keep `Reg` abstract — a `Type` with `Preorder` and `IsDirected`.
Concrete causal-diamond models are instances, not the definition.

Mathlib provides `IsDirected α (· ≤ ·)` in `Mathlib.Order.Directed`, so we
use that directly rather than rolling a custom class.
-/

-- ============================================================================
-- § 1. Region Assumptions
-- ============================================================================

/-- Bundle of assumptions IQT places on the region index set.
    A `RegionSystem` is any preordered type that is upward-directed
    and nonempty. -/
class RegionSystem (Reg : Type*) extends Preorder Reg where
  directed : IsDirected Reg (· ≤ ·)
  nonempty : Nonempty Reg

attribute [instance] RegionSystem.directed RegionSystem.nonempty

-- ============================================================================
-- § 2. FinitelyBounded (Optional)
-- ============================================================================

/-- IQT Box 2.A: in causal-set spacetime every bounded region contains
    finitely many sub-diamonds. This is extra structure, not required for
    the convergence theorems, but useful for constructive arguments. -/
class FinitelyBounded (Reg : Type*) [Preorder Reg] where
  finite_sub : ∀ D : Reg, Set.Finite { D' : Reg | D' ≤ D }

-- ============================================================================
-- § 3. Concrete Instance: Finite Linear Chain
-- ============================================================================

/-- A finite linear chain of `n` nested regions, ordered by `≤` on `Fin n`.
    Models the simplest case: a sequence of nested diamonds D₀ ⊆ D₁ ⊆ … ⊆ Dₙ₋₁. -/
abbrev RegionFin (n : ℕ) := Fin n

/-- `Fin n` for `n ≥ 1` is upward-directed: `max i j` is an upper bound. -/
instance regionFinDirected (n : ℕ) [NeZero n] :
    IsDirected (RegionFin n) (· ≤ ·) where
  directed a b := ⟨max a b, le_max_left a b, le_max_right a b⟩

instance regionFinSystem (n : ℕ) [h : NeZero n] :
    RegionSystem (RegionFin n) where
  directed := regionFinDirected n
  nonempty := ⟨⟨0, Nat.pos_of_ne_zero h.ne⟩⟩

instance regionFinFinitelyBounded (n : ℕ) :
    FinitelyBounded (RegionFin n) where
  finite_sub _ := Set.Finite.subset (Set.finite_univ) (Set.subset_univ _)

-- ============================================================================
-- § 4. Concrete Instance: Powerset Lattice
-- ============================================================================

/-- Powerset of a finite type, ordered by inclusion. This models the lattice
    of all sub-diamonds of a finite causal set. -/
abbrev RegionPowerset (α : Type*) := Set α

/-- The powerset is upward-directed: the union of any two sets is an upper bound. -/
instance regionPowersetDirected (α : Type*) :
    IsDirected (RegionPowerset α) (· ≤ ·) where
  directed a b := ⟨a ∪ b, Set.subset_union_left, Set.subset_union_right⟩

instance regionPowersetSystem (α : Type*) :
    RegionSystem (RegionPowerset α) where
  directed := regionPowersetDirected α
  nonempty := ⟨∅⟩

-- ============================================================================
-- § 5. Smoke-Test Examples
-- ============================================================================

section SmokeTests

/-- Three nested regions: D₀ ⊆ D₁ ⊆ D₂. -/
example : RegionSystem (RegionFin 3) := inferInstance

/-- Directedness: any two regions in Fin 3 have an upper bound. -/
example : IsDirected (RegionFin 3) (· ≤ ·) := inferInstance

/-- Powerset of a 3-element type forms a region system. -/
example : RegionSystem (RegionPowerset (Fin 3)) := inferInstance

/-- FinitelyBounded holds for the finite chain. -/
example : FinitelyBounded (RegionFin 4) := inferInstance

end SmokeTests
