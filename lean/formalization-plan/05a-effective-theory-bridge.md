# Phase 5a: The Effective-Theory Bridge

**Phase:** 05 - Effective Theory Bridge
**Track:** Neural-Scale Formalism
**Depends on:** 01c (net of algebras), 01d (state presheaf)
**Unlocks:** 05b (metric formalization), 06a-06c (protocol predictions)

---

## Goal

Formalize the effective-theory schema from Section 2.6: the bridge from fundamental AQFT to neural-scale observables. This is how IQT connects to experiment. The effective neural algebra is a finite-dimensional C*-subalgebra of the fundamental algebra, obtained by coarse-graining.

## What to Formalize

### 1. Effective Algebra Embedding

The key structure is an injective *-homomorphism from the effective algebra into the fundamental one:

```lean
/-- The effective-theory bridge: an embedding of a finite-dimensional effective algebra
    into the fundamental local algebra. -/
structure EffectiveBridge (Reg : Type) [Preorder Reg]
    (N_fund : LocalNet Reg) where
  -- The effective (neural-scale) net
  N_eff : LocalNet Reg
  -- Embedding: injective *-homomorphism at each region
  embed : ∀ D : Reg, StarAlgHom (N_eff.algebra D) (N_fund.algebra D)
  -- Injectivity: the embedding is faithful (subalgebra inclusion)
  injective : ∀ D, Function.Injective (embed D)
  -- Compatibility with isotony: the embeddings commute with restriction
  natural : ∀ {D₁ D₂ : Reg} (h : D₁ ≤ D₂) (a : N_eff.algebra D₁),
    N_fund.embed h (embed D₁ a) = embed D₂ (N_eff.embed h a)
```

### 2. Effective State via Restriction

```lean
/-- The effective state is defined by restriction along the embedding. -/
def effectiveState (bridge : EffectiveBridge Reg N_fund)
    (ω : CompatibleFamily N_fund) : CompatibleFamily bridge.N_eff where
  state := fun D => restrictState (bridge.embed D) (ω.state D)
  compatible := by
    -- Follows from compatibility of ω and naturality of the embedding.
    sorry
```

### 3. Effective Quality

```lean
/-- The effective quality at D: the algebra-state pair at effective scale. -/
def effectiveQuality (bridge : EffectiveBridge Reg N_fund)
    (ω : CompatibleFamily N_fund) (D : Reg) :
    Quality bridge.N_eff (effectiveState bridge ω) D where
  algebra := bridge.N_eff.algebra D
  localState := (effectiveState bridge ω).state D
```

### 4. Three Physical Constraints on the Bridge

From Section 2.6, the coarse-graining is constrained by:

```lean
/-- Physical locality: the effective algebra respects causal structure.
    An observable in one region cannot be mapped to a different region. -/
-- This is the naturality condition in EffectiveBridge above.

/-- Quantum consistency (algebraic structure preservation):
    The embedding preserves products and adjoints. -/
-- This is built into StarAlgHom: it preserves multiplication and *.

/-- Instrumental reality: generators of the effective algebra correspond
    to quantities the instruments physically measure. -/
-- This is a meta-constraint, not formalizable purely in Lean.
-- It constrains the choice of bridge, not its mathematical properties.
```

### 5. Information Loss Under Coarse-Graining

```lean
/-- Coarse-graining can only lose information, never create correlations.
    Data-processing inequality for the embedding map. -/
theorem coarsegraining_information_loss (bridge : EffectiveBridge Reg N_fund)
    (ω : CompatibleFamily N_fund) (D : Reg) :
    -- The effective state has less (or equal) information than the fundamental state.
    -- Formalized via quantum mutual information:
    -- I_eff(A:B) ≤ I_fund(A:B) for any bipartition.
    sorry
```

### 6. Approximate Properties

The paper is explicit that the effective algebra satisfies AQFT properties only approximately:

```lean
/-- The effective algebra satisfies isotony exactly (by construction). -/
-- (Built into N_eff being a LocalNet.)

/-- The effective algebra satisfies microcausality approximately.
    At neural scales, spacelike separation is approximate. -/
-- This is a qualitative property; not formalized as a theorem.

/-- The effective algebra satisfies covariance approximately.
    Neural observables respect spatial symmetries approximately. -/
-- Also qualitative; flagged for documentation.
```

## Acceptance Criteria

- [ ] `EffectiveBridge` structure compiles
- [ ] `effectiveState` derives effective-scale states from fundamental states
- [ ] `effectiveQuality` assembles the effective algebra-state pair
- [ ] The three physical constraints (locality, quantum consistency, instrumental reality) are documented
- [ ] Information loss property stated
- [ ] Concrete example: a toy coarse-graining (e.g., 8-dimensional algebra → 4-dimensional)

## Notes

- Section 2.6: "The effective algebra is still a local algebra. It satisfies isotony, approximate microcausality, and covariance."
- This bridge is the weakest structural element acknowledged by the paper (Section 7): "The jump from AQFT to neural-scale metrics is the weakest structural element."
- The paper uses standard effective-field-theory reasoning (Wilson 1975, Polchinski 1984) to motivate the bridge.
- The formalization captures the STRUCTURE of the bridge, not a specific biophysical implementation.
