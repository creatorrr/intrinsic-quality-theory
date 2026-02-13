# Phase 1c: Net of Local Algebras (Haag-Kastler Axioms)

**Phase:** 01 - AQFT Foundations & Infrastructure
**Track:** Core Mathematical Infrastructure
**Depends on:** 01a (regions), 01b (C*-algebras)
**Unlocks:** 01d, 02a, 02b, 03a

---

## Goal

Define the net of local algebras `A : Reg -> CStarAlg` with isotony embeddings, forming the Haag-Kastler framework. This is the central mathematical structure from which all of IQT's formalism derives.

## What to Formalize

### 1. Local Net Structure

A local net assigns to each region a C*-algebra and to each inclusion an embedding:

```lean
structure LocalNet (Reg : Type) [Preorder Reg] where
  -- Assignment of C*-algebra to each region
  algebra : Reg → CStarAlg
  -- Isotony: inclusion of regions gives algebra embeddings
  embed : ∀ {D₁ D₂ : Reg}, D₁ ≤ D₂ → StarAlgHom (algebra D₁) (algebra D₂)
  -- Functoriality: identity
  embed_id : ∀ (D : Reg), embed (le_refl D) = StarAlgHom.id
  -- Functoriality: composition
  embed_comp : ∀ {D₁ D₂ D₃ : Reg} (h₁₂ : D₁ ≤ D₂) (h₂₃ : D₂ ≤ D₃),
    embed (le_trans h₁₂ h₂₃) = (embed h₂₃).comp (embed h₁₂)
  -- Injectivity of embeddings (subalgebra inclusion)
  embed_injective : ∀ {D₁ D₂ : Reg} (h : D₁ ≤ D₂),
    Function.Injective (embed h)
```

### 2. Microcausality (Optional for Core Theorem)

Spacelike-separated algebras commute. This requires a notion of spacelike separation on `Reg`, which is additional structure beyond the poset. The constraint convergence theorem does NOT use microcausality, so this is deferrable.

```lean
-- Optional: spacelike separation relation
class HasCausalStructure (Reg : Type) [Preorder Reg] where
  spacelike : Reg → Reg → Prop
  -- Microcausality axiom
  commute : ∀ {D₁ D₂ : Reg}, spacelike D₁ D₂ →
    ∀ (a₁ : algebra D₁) (a₂ : algebra D₂),
      embed_to_union a₁ * embed_to_union a₂ = embed_to_union a₂ * embed_to_union a₁
```

### 3. Covariance (Group Action)

Required for Constraint 3 but NOT for the convergence theorem:

```lean
-- Covariance: a group G acts on regions and on the net compatibly
structure NetCovariance (Reg : Type) [Preorder Reg]
    (N : LocalNet Reg) (G : Type) [Group G] where
  act_region : G → Reg → Reg
  act_algebra : ∀ (g : G) (D : Reg), StarAlgIso (N.algebra D) (N.algebra (act_region g D))
  -- Compatibility with the group law
  act_comp : ∀ g₁ g₂ D, act_region (g₁ * g₂) D = act_region g₁ (act_region g₂ D)
  -- Naturality with embeddings
  natural : ∀ (g : G) {D₁ D₂} (h : D₁ ≤ D₂),
    (act_algebra g D₂).toStarAlgHom.comp (N.embed h) =
    (N.embed (show act_region g D₁ ≤ act_region g D₂ from ...)).comp (act_algebra g D₁).toStarAlgHom
```

### 4. Categorical Reformulation (Alternative)

The paper notes that the net is a covariant functor `Reg -> CStarAlgCat`. If using Mathlib's category theory library:

```lean
-- Using Mathlib categories
variable (A : Reg ⥤ CStarAlgCat)
```

Decide whether to use the bundled `LocalNet` structure or the categorical formulation. The categorical version is more elegant but may be harder to work with for concrete proofs.

## Mathlib Resources

- `Mathlib.CategoryTheory.Functor` for functorial formulation
- `Mathlib.Algebra.Star.Hom` for star-algebra homomorphisms
- `Mathlib.Order.Category.Preorder` for viewing `Reg` as a category

## Acceptance Criteria

- [ ] `LocalNet` structure compiles
- [ ] Functoriality of embeddings (id and comp) is provable
- [ ] Concrete instance: three-qubit toy model from Section 2.4 (algebras = matrix algebras for subsystems)
- [ ] Concrete instance: finite lattice net (powerset ordered by inclusion, matrix algebras of varying size)

## Design Decisions

1. **Bundled vs unbundled:** The `LocalNet` structure bundles everything. An alternative is to use typeclasses. Bundled is simpler for a first pass.
2. **Categorical vs direct:** The skeleton in `constraint-convergence.md` uses `Reg ⥤ CStarAlgCat`. The paper's Appendix B uses direct function + separate embedding. Either works; choose based on what compiles more easily.
3. **Injectivity:** The paper assumes embeddings are injective (subalgebra inclusions). This is crucial for the convergence theorem and should be baked in.

## Notes

- The paper explicitly states (Section 2.0): "Net existence: A satisfying isotony and microcausality" as the first specific assumption. Isotony is the essential one for the convergence theorem.
- Microcausality and covariance are needed for physical interpretation but not for the mathematical convergence result. They can be added later.
