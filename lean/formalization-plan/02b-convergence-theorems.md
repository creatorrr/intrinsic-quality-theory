# Phase 2b: Constraint Convergence Theorems (Weak and Strong)

**Phase:** 02 - Constraint Convergence Theorem
**Track:** Core Theorem (Track 1) — THE CROWN JEWEL
**Depends on:** 02a (assignments + constraints), 01d (state presheaf)
**Unlocks:** 02c, 02d

---

## Goal

Prove the two convergence propositions from Section 1.1. These are the central formal results of IQT: any admissible intrinsic-nature assignment either collapses to the state presheaf modulo operational equivalence (weak form) or is naturally isomorphic to it (strong form).

## What to Formalize

### 1. Weak Convergence (Proposition 1)

> Let (I, δ) satisfy C1, C2, and C4w. The quotient I/∼ embeds naturally into Ω.

```lean
/-- The quotient presheaf I_hat := I / OpEquiv. -/
def QuotientPresheaf (X : IntrinsicAssignment Reg N) : Reg → Type :=
  fun D => Quotient (OpEquiv.setoid X D)

/-- Restriction descends to the quotient. -/
def QuotientPresheaf.restrict (X : IntrinsicAssignment Reg N)
    {D₁ D₂ : Reg} (h : D₁ ≤ D₂) :
    QuotientPresheaf X D₂ → QuotientPresheaf X D₁ := by
  -- Key step: show that restriction sends OpEquiv-equivalent elements
  -- to OpEquiv-equivalent elements. This follows from naturality of δ.
  sorry

/-- The quotient presheaf is a presheaf (restriction is functorial). -/
theorem QuotientPresheaf.is_presheaf (X : IntrinsicAssignment Reg N) :
    -- identity law
    (∀ D (q : QuotientPresheaf X D), QuotientPresheaf.restrict X (le_refl D) q = q) ∧
    -- composition law
    (∀ {D₁ D₂ D₃} (h₁₂ : D₁ ≤ D₂) (h₂₃ : D₂ ≤ D₃) (q : QuotientPresheaf X D₃),
      QuotientPresheaf.restrict X h₁₂ (QuotientPresheaf.restrict X h₂₃ q) =
      QuotientPresheaf.restrict X (le_trans h₁₂ h₂₃) q) := by
  sorry

/-- The induced decoding map on the quotient. -/
def QuotientPresheaf.δ_hat (X : IntrinsicAssignment Reg N) (D : Reg) :
    QuotientPresheaf X D → StateSpace N D := by
  -- Descend δ_D to the quotient using the fact that
  -- OpEquiv-equivalent elements have the same image under δ.
  sorry

/-- PROPOSITION 1 (Weak Convergence):
    δ_hat is a natural monomorphism: componentwise injective
    and compatible with restriction. -/
theorem weak_convergence (X : IntrinsicAssignment Reg N) :
    -- (i) Injectivity at each component
    (∀ D, Function.Injective (QuotientPresheaf.δ_hat X D)) ∧
    -- (ii) Naturality
    (∀ {D₁ D₂} (h : D₁ ≤ D₂) (q : QuotientPresheaf X D₂),
      QuotientPresheaf.δ_hat X D₁ (QuotientPresheaf.restrict X h q) =
      StateSpace.restrict N h (QuotientPresheaf.δ_hat X D₂ q)) := by
  sorry
```

**Proof strategy:**
- Injectivity: By construction. If `δ_hat [x] = δ_hat [y]`, then `δ x = δ y`, so `x ~ y`, so `[x] = [y]`.
- Naturality: Inherited from naturality of `δ` and functoriality of restriction on the quotient.

### 2. Strong Convergence (Proposition 2)

> Let (I, δ) satisfy C1, C2, and C4s. Then δ is a natural monomorphism. If additionally δ is componentwise surjective, then I ≅ Ω.

```lean
/-- PROPOSITION 2 (Strong Convergence):
    Under NoJunk, δ is a natural monomorphism.
    With surjectivity, it is a natural isomorphism. -/
theorem strong_convergence (X : IntrinsicAssignment Reg N)
    (hInj : NoJunk X)
    (hSurj : ∀ D, Function.Surjective (X.δ D)) :
    ∀ D, Function.Bijective (X.δ D) :=
  fun D => ⟨hInj D, hSurj D⟩

/-- The natural isomorphism I ≅ Ω under NoJunk + surjectivity. -/
def convergence_iso (X : IntrinsicAssignment Reg N)
    (hInj : NoJunk X) (hSurj : ∀ D, Function.Surjective (X.δ D)) :
    ∀ D, X.I D ≃ StateSpace N D :=
  fun D => Equiv.ofBijective (X.δ D) (strong_convergence X hInj hSurj D)

/-- The isomorphism is natural: commutes with restriction. -/
theorem convergence_natural (X : IntrinsicAssignment Reg N)
    (hInj : NoJunk X) (hSurj : ∀ D, Function.Surjective (X.δ D))
    {D₁ D₂ : Reg} (h : D₁ ≤ D₂) (x : X.I D₂) :
    (convergence_iso X hInj hSurj D₁) (X.restrict h x) =
    StateSpace.restrict N h ((convergence_iso X hInj hSurj D₂) x) := by
  -- This is just the naturality of δ, which is given.
  exact X.natural h x
```

**Proof strategy:** The paper says "The proofs are deliberately short." Indeed:
- Injectivity = C4s
- Surjectivity = given hypothesis
- Bijection = injectivity + surjectivity
- Naturality = given (field of `IntrinsicAssignment`)

### 3. Corollary: Actual-World Specialization

```lean
/-- If i is a section and decoded content matches the physical state,
    then the actual intrinsic descriptor at D is identified with ω_D. -/
theorem actual_world (X : IntrinsicAssignment Reg N)
    (hInj : NoJunk X) (hSurj : ∀ D, Function.Surjective (X.δ D))
    (i : Section X) (ω : CompatibleFamily N)
    (match_physical : ∀ D, X.δ D (i.assign D) = ω.state D) :
    ∀ D, (convergence_iso X hInj hSurj D) (i.assign D) = ω.state D :=
  match_physical
```

### 4. Independence from C3

```lean
/-- Neither convergence theorem uses covariance (C3).
    C3 constrains which assignments are physically admissible
    but does not narrow the mathematical form. -/
-- (This is documented, not proved — it's a meta-observation about the proofs above.)
```

## Acceptance Criteria

- [ ] `QuotientPresheaf` compiles and has functorial restriction
- [ ] `weak_convergence` (Proposition 1) is stated and proved
- [ ] `strong_convergence` (Proposition 2) is stated and proved
- [ ] `convergence_iso` provides the natural isomorphism
- [ ] `actual_world` corollary is stated and proved
- [ ] No use of C3 (covariance) in any proof — verify by inspection

## Notes

- The paper says (Section 1.1): "The proofs are deliberately short. The mathematical content is a straightforward application of the first isomorphism theorem (for Prop 1) and the definition of bijection (for Prop 2). The work of the argument is not in the proofs but in the formulation."
- The value of formalization is forcing type signatures and naturality conditions to be explicit.
- This is Appendix B's `convergence_strong` theorem, fully expanded.

## Difficulty Assessment

Low to moderate. The proofs themselves are simple. The difficulty is:
1. Getting the type signatures to compile (Phase 01 dependencies)
2. Working with Lean's `Quotient` API for the weak form
3. Managing the universe levels if using Mathlib categories
