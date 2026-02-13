# Phase 2a: Intrinsic-Nature Assignments and Constraints

**Phase:** 02 - Constraint Convergence Theorem
**Track:** Core Theorem (Track 1)
**Depends on:** 01a, 01b, 01c, 01d
**Unlocks:** 02b, 02c

---

## Goal

Define the `IntrinsicAssignment` structure and the four constraints (C1-C4) from Section 1.1. This is the setup for the convergence theorem — the central formal result of IQT.

## What to Formalize

### 1. Intrinsic-Nature Assignment

From Section 1.1 and Appendix B: an intrinsic-nature assignment is a presheaf `I` with a natural transformation `delta` into the state presheaf:

```lean
/-- An intrinsic-nature assignment on a local net.
    I(D) = candidate descriptors for region D.
    δ_D : I(D) → Ω(D) = the decoding map (what operational content the descriptor implies). -/
structure IntrinsicAssignment (Reg : Type) [Preorder Reg] (N : LocalNet Reg) where
  -- Descriptor presheaf
  I : Reg → Type
  -- Restriction maps (presheaf structure on I)
  restrict : ∀ {D₁ D₂ : Reg}, D₁ ≤ D₂ → I D₂ → I D₁
  -- Presheaf identity law
  restrict_id : ∀ (D : Reg) (x : I D), restrict (le_refl D) x = x
  -- Presheaf composition law
  restrict_comp : ∀ {D₁ D₂ D₃ : Reg} (h₁₂ : D₁ ≤ D₂) (h₂₃ : D₂ ≤ D₃) (x : I D₃),
    restrict h₁₂ (restrict h₂₃ x) = restrict (le_trans h₁₂ h₂₃) x
  -- Decoding map
  δ : ∀ D : Reg, I D → StateSpace N D
  -- Naturality of δ: decoding commutes with restriction
  natural : ∀ {D₁ D₂ : Reg} (h : D₁ ≤ D₂) (x : I D₂),
    δ D₁ (restrict h x) = StateSpace.restrict N h (δ D₂ x)
```

### 2. Constraint 1: Operational Completeness

> "The intrinsic nature of D determines all measurement statistics internal to D."

This is automatic from the definition: `δ_D(x)` is a state on `A(D)`, which assigns an expectation value to every observable. No separate axiom needed — it is built into `δ : I D → StateSpace N D`.

Document this explicitly as a lemma:

```lean
/-- C1 is automatic: every descriptor determines a complete state. -/
theorem C1_automatic (X : IntrinsicAssignment Reg N) (D : Reg) (x : X.I D) :
    X.δ D x ∈ Set.range (X.δ D) := ⟨x, rfl⟩
```

### 3. Constraint 2: Isotony (Restriction Compatibility)

> "I is a presheaf and δ is natural."

This is the `restrict` and `natural` fields of `IntrinsicAssignment`. Already built in.

### 4. Constraint 3: Covariance

> "I and δ are G-equivariant."

This requires the `NetCovariance` structure from 01c:

```lean
/-- C3: Equivariance of the intrinsic assignment under symmetries. -/
structure Covariant (X : IntrinsicAssignment Reg N)
    (G : Type) [Group G] (cov : NetCovariance Reg N G) where
  act : ∀ (g : G) (D : Reg), X.I D → X.I (cov.act_region g D)
  equivariant : ∀ (g : G) (D : Reg) (x : X.I D),
    X.δ (cov.act_region g D) (act g D x) =
    restrictState (cov.act_algebra g D).symm.toStarAlgHom (X.δ D x)
```

**Important:** C3 does NOT participate in the convergence theorem. It filters physically admissible assignments but does not narrow the mathematical form.

### 5. Constraint 4w: Weak Locality

> "I is a presheaf evaluated on the poset of regions."

Already built into the `IntrinsicAssignment` definition. Document explicitly.

### 6. Constraint 4s: Strong / No-Junk Extensionality

> "The decoding map is componentwise injective."

```lean
/-- C4s (No-Junk): decoding is injective at each region.
    Two descriptors yielding the same operational content are identical. -/
def NoJunk (X : IntrinsicAssignment Reg N) : Prop :=
  ∀ D : Reg, Function.Injective (X.δ D)
```

### 7. Operational Equivalence

```lean
/-- Operational equivalence: two descriptors that decode to the same state. -/
def OpEquiv (X : IntrinsicAssignment Reg N) (D : Reg) (x y : X.I D) : Prop :=
  X.δ D x = X.δ D y

/-- OpEquiv is an equivalence relation. -/
instance : IsEquiv (X.I D) (OpEquiv X D) := ...
```

### 8. Sections (Actual-World Assignment)

```lean
/-- A section of the intrinsic assignment: the actual intrinsic nature at each region. -/
structure Section (X : IntrinsicAssignment Reg N) where
  assign : ∀ D : Reg, X.I D
  compatible : ∀ {D₁ D₂ : Reg} (h : D₁ ≤ D₂),
    X.restrict h (assign D₂) = assign D₁
```

## Acceptance Criteria

- [ ] `IntrinsicAssignment` structure compiles with all presheaf laws
- [ ] `NoJunk` predicate compiles
- [ ] `OpEquiv` is an equivalence relation
- [ ] `Section` structure compiles
- [ ] Trivial instance: `I = Ω`, `δ = id` satisfies all constraints including `NoJunk`
- [ ] Counterexample structure: `I = Ω × Bool`, `δ = fst` satisfies C1-C3+C4w but NOT C4s

## Notes

- The paper says (Section 1.1): "This packaging is deliberately neutral. It says nothing about consciousness, nothing about the internal constitution of the descriptors."
- The constraints do the work of elimination — the assignment structure is maximally general.
- C3 is included for completeness but is not used in the convergence proofs.
