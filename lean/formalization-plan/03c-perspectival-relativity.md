# Phase 3c: Perspectival Relativity and Democracy of Diamonds

**Phase:** 03 - Composition & Unity Functional
**Track:** Structural Properties
**Depends on:** 01d (state presheaf), 03a (composition), 03b (unity)
**Unlocks:** 04a (self-threads)

---

## Goal

Formalize the central structural commitment of IQT: perspectival relativity. Quality is relative to the region (scale, position, extent) of a bounded diamond, with no privileged "view from nowhere." Multiple overlapping regions bear quality simultaneously.

## What to Formalize

### 1. Quality at Every Region

```lean
/-- Every region has quality. This is Filter 0 of IQT's three-filter hierarchy.
    There is no exclusion step selecting "the" conscious region. -/
theorem quality_universal (N : LocalNet Reg) (ω : CompatibleFamily N) :
    ∀ D : Reg, Nonempty (StateSpace N D) := by
  intro D
  exact ⟨ω.state D⟩
```

### 2. Consistency Across Scales (Presheaf Coherence)

```lean
/-- Qualities at nested scales are consistent: restriction from larger to smaller
    region recovers the smaller region's quality. This is the presheaf condition. -/
theorem quality_consistent (N : LocalNet Reg) (ω : CompatibleFamily N)
    {D₁ D₂ : Reg} (h : D₁ ≤ D₂) :
    StateSpace.restrict N h (ω.state D₂) = ω.state D₁ :=
  ω.compatible h
```

### 3. Non-Redundancy Across Scales

```lean
/-- Larger regions contain structure absent from sub-regions.
    The state on D₂ is NOT determined by the state on D₁ when D₁ < D₂.
    (The extension set has more than one element.) -/
-- This is the content of Phase 03a, extension_nonunique.
```

### 4. No Exclusion Principle

```lean
/-- IQT's democracy of diamonds: there is no selection step that picks one region
    as "the" conscious one. Every region has quality (Filter 0).
    Contrast with IIT's exclusion postulate. -/
-- This is a definitional property: Quality and Unity are defined for ALL regions.
-- No `max_unity_region` selection function is defined or needed.

/-- Multiple overlapping regions can simultaneously have high unity. -/
theorem democracy_compatible (N : LocalNet Reg) (ω : CompatibleFamily N)
    (D₁ D₂ : Reg) (h₁ : D₁ ≤ D₂)
    (hU₁ : unity N ω D₁ parts₁ > threshold)
    (hU₂ : unity N ω D₂ parts₂ > threshold) :
    -- Both statements can hold simultaneously. No contradiction.
    True := trivial
```

### 5. Scale-Dependent Content

```lean
/-- As diamond scale increases, the algebra grows (by isotony), supporting
    observables absent from sub-algebras. Cross-regional correlators become
    available. This is the formal basis for "novel phenomenological dimensions." -/
theorem algebra_grows (N : LocalNet Reg) {D₁ D₂ : Reg} (h : D₁ ≤ D₂)
    (hStrict : D₁ ≠ D₂) :
    -- The embedding is injective but not surjective in general
    -- (A(D₁) is a proper subalgebra of A(D₂))
    Function.Injective (N.embed h) := N.embed_injective h
```

### 6. Intrinsicness Principle (Section 1.3)

```lean
/-- The Intrinsicness Principle: quality at D depends only on the algebra-state pair
    at D, up to physically induced isomorphism. Two systems with isomorphic
    (A(D), ω_D) have the same quality at that scale. -/
-- This is a meta-principle constraining when qualities are "the same."
-- Formalized as: quality is determined by the isomorphism class of (A, ω).

def qualityEquiv (N₁ N₂ : LocalNet Reg) (ω₁ : CompatibleFamily N₁)
    (ω₂ : CompatibleFamily N₂) (D : Reg) : Prop :=
  ∃ (φ : StarAlgIso (N₁.algebra D) (N₂.algebra D)),
    ω₂.state D = restrictState φ.symm.toStarAlgHom (ω₁.state D)
```

## Acceptance Criteria

- [ ] `quality_universal` stated (trivial from presheaf structure)
- [ ] `quality_consistent` stated (= presheaf condition)
- [ ] Democracy of diamonds: no exclusion function defined, documented
- [ ] `qualityEquiv` (isomorphism-invariant quality comparison) defined
- [ ] Three-qubit example: show D=A and D=ABC have different quality content

## Notes

- Box 2.A in the paper: "No privileged reference frame; no 'true quality' — only qualities-relative-to-diamonds."
- The disanalogy with special relativity: "In SR, frame-independent invariants exist. In IQT the 'invariant' is not a shared quality but the consistency condition: local qualities form a coherent presheaf."
- Finite multiplicity: "Because spacetime is discrete (a causal set), the number of sub-diamonds is combinatorially large but finite."
