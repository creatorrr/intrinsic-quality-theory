# Phase 1d: The State Presheaf

**Phase:** 01 - AQFT Foundations & Infrastructure
**Track:** Core Mathematical Infrastructure
**Depends on:** 01a (regions), 01b (C*-algebras), 01c (net of algebras)
**Unlocks:** 02a, 02b, 03a

---

## Goal

Define the state presheaf `Omega : Reg^op -> Type` and the quality object `Q(D) = (A(D), omega_D)`. This is the mathematical object that IQT identifies with phenomenal quality. The state presheaf is also the convergence target of the constraint argument.

## What to Formalize

### 1. The State Presheaf

Given a local net `N : LocalNet Reg`, define the contravariant functor sending each region to its space of states, with restriction maps given by pullback along isotony embeddings:

```lean
/-- States on the algebra of region D. -/
def StateSpace (N : LocalNet Reg) (D : Reg) : Type :=
  CStarState (N.algebra D)

/-- Restriction: given D₁ ≤ D₂, pull back a state from A(D₂) to A(D₁). -/
def StateSpace.restrict (N : LocalNet Reg) {D₁ D₂ : Reg} (h : D₁ ≤ D₂)
    (ω : StateSpace N D₂) : StateSpace N D₁ :=
  restrictState (N.embed h) ω

/-- The state presheaf Ω as a contravariant functor. -/
structure StatePresheaf (N : LocalNet Reg) where
  obj : Reg → Type := StateSpace N
  map : ∀ {D₁ D₂}, D₁ ≤ D₂ → StateSpace N D₂ → StateSpace N D₁ :=
    fun h ω => StateSpace.restrict N h ω
  map_id : ∀ D (ω : StateSpace N D), map (le_refl D) ω = ω
  map_comp : ∀ {D₁ D₂ D₃} (h₁₂ : D₁ ≤ D₂) (h₂₃ : D₂ ≤ D₃) (ω : StateSpace N D₃),
    map h₁₂ (map h₂₃ ω) = map (le_trans h₁₂ h₂₃) ω
```

### 2. Presheaf Laws

Prove that restriction satisfies functoriality:
- `restrict (le_refl D) ω = ω` (identity)
- `restrict h₁₂ (restrict h₂₃ ω) = restrict (le_trans h₁₂ h₂₃) ω` (composition)

These follow from `LocalNet.embed_id` and `LocalNet.embed_comp`.

### 3. Compatible State Families (Global Sections)

A compatible family of local states (a section of the state presheaf) represents the actual physical state of the world:

```lean
/-- A compatible family of local states: a section of the state presheaf.
    This assigns a state to each region, consistently with restriction. -/
structure CompatibleFamily (N : LocalNet Reg) where
  state : ∀ D : Reg, StateSpace N D
  compatible : ∀ {D₁ D₂ : Reg} (h : D₁ ≤ D₂),
    StateSpace.restrict N h (state D₂) = state D₁
```

### 4. The Quality Object

```lean
/-- The quality of a region D is the algebra-state pair. -/
structure Quality (N : LocalNet Reg) (ω : CompatibleFamily N) (D : Reg) where
  algebra : CStarAlg := N.algebra D
  localState : CStarState (N.algebra D) := ω.state D
```

### 5. Categorical Formulation (Alternative)

Using Mathlib's category theory:

```lean
/-- The state presheaf as a functor Regᵒᵖ ⥤ Type. -/
def Ω (N : LocalNet Reg) : Regᵒᵖ ⥤ Type where
  obj := fun D => CStarState (N.algebra (unop D))
  map := fun f ρ => restrictState (N.embed f.unop.le) ρ
  map_id := by ... -- follows from embed_id
  map_comp := by ... -- follows from embed_comp
```

## Acceptance Criteria

- [ ] `StateSpace` and `restrict` compile
- [ ] Functoriality proofs (id, comp) discharge
- [ ] `CompatibleFamily` structure compiles
- [ ] `Quality` structure compiles
- [ ] Toy model: three-qubit example with explicit density matrices as states, showing restriction = partial trace

## Verification Examples

### Three-Qubit Toy (Section 2.4)

- Regions: A, B, C, AB, AC, BC, ABC
- Algebras: `M₂`, `M₂`, `M₂`, `M₄`, `M₄`, `M₄`, `M₈`
- GHZ state: ρ_ABC = |GHZ⟩⟨GHZ|
- Restricted state: ρ_A = Tr_{BC}(ρ_ABC) = I/2
- Verify: `restrict (A ≤ ABC) ρ_ABC = ρ_A`

## Notes

- The state presheaf is the convergence target of the constraint argument (Phase 2). Getting this right is essential.
- The paper's Section 1.1 says: "When the net is fixed as background structure, the varying data is the local state ω_D, and Q(D) is determined by the section D ↦ ω_D of the state presheaf."
- In the categorical formulation from `constraint-convergence.md`, this is `Ω : Regᵒᵖ ⥤ Type`.
