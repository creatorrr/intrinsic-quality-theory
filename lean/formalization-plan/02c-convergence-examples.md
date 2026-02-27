# Phase 2c: Convergence on Concrete Examples

**Phase:** 02 - Constraint Convergence Theorem
**Track:** Verification & Testing
**Depends on:** 02b (convergence theorems), 01e (toy models)
**Unlocks:** Nothing (terminal verification task)

---

## Goal

Instantiate the convergence theorems on concrete, finite-dimensional models to verify correctness. This serves as both a smoke test for the abstract theorems and a pedagogical demonstration.

## What to Formalize

### 1. Trivial Instance: I = Omega

The identity assignment `I(D) = StateSpace(D)`, `δ = id`, `restrict = state restriction` trivially satisfies all constraints and is its own convergence target.

```lean
/-- The identity assignment: I = Ω, δ = id. -/
def identityAssignment (N : LocalNet Reg) : IntrinsicAssignment Reg N where
  I := StateSpace N
  restrict := StateSpace.restrict N
  restrict_id := StateSpace.restrict_id N
  restrict_comp := StateSpace.restrict_comp N
  δ := fun D ω => ω
  natural := fun h x => rfl

/-- The identity assignment satisfies NoJunk. -/
theorem identityAssignment_noJunk (N : LocalNet Reg) :
    NoJunk (identityAssignment N) := by
  intro D x y hxy
  exact hxy

/-- Strong convergence on the identity assignment is trivial. -/
example (N : LocalNet Reg) :
    ∀ D, Function.Bijective ((identityAssignment N).δ D) :=
  strong_convergence (identityAssignment N)
    (identityAssignment_noJunk N)
    (fun D => Function.surjective_id)
```

### 2. Junk Instance: I = Omega x Bool

This is the canonical counterexample to C4s (Section 1.1): attaching an operationally invisible bit.

```lean
/-- The junk assignment: I(D) = StateSpace(D) × Bool, δ = fst. -/
def junkAssignment (N : LocalNet Reg) : IntrinsicAssignment Reg N where
  I := fun D => StateSpace N D × Bool
  restrict := fun h (ω, b) => (StateSpace.restrict N h ω, b)
  δ := fun D (ω, _) => ω
  natural := fun h (ω, b) => by simp [StateSpace.restrict]
  ...

/-- The junk assignment does NOT satisfy NoJunk. -/
theorem junkAssignment_not_noJunk (N : LocalNet Reg) (D : Reg)
    (hne : Nonempty (StateSpace N D)) :
    ¬ NoJunk (junkAssignment N) := by
  intro h
  obtain ⟨ω⟩ := hne
  have := h D (show (junkAssignment N).δ D (ω, true) = (junkAssignment N).δ D (ω, false) from rfl)
  -- (ω, true) ≠ (ω, false), contradiction
  sorry

/-- But weak convergence still works: the quotient collapses the Bool. -/
theorem junkAssignment_weak_convergence (N : LocalNet Reg) :
    ∀ D, Function.Injective (QuotientPresheaf.δ_hat (junkAssignment N) D) := by
  sorry
```

### 3. Three-Qubit Instantiation

Apply the convergence theorem to the three-qubit net from Phase 01e:

```lean
/-- The identity assignment on the three-qubit net converges. -/
example : ∀ D : ThreeQubitRegion,
    Function.Bijective ((identityAssignment threeQubitNet).δ D) := by
  exact strong_convergence ...
```

### 4. Custom Assignment on Three Qubits

Define a non-trivial intrinsic assignment on the three-qubit net (e.g., density matrices plus classical labels) and show convergence after quotienting.

## Acceptance Criteria

- [ ] Identity assignment instantiates `IntrinsicAssignment` and `NoJunk`
- [ ] Junk assignment instantiates `IntrinsicAssignment` but NOT `NoJunk`
- [ ] Weak convergence demonstrated on junk assignment
- [ ] Strong convergence demonstrated on identity assignment
- [ ] At least one theorem instantiated on `threeQubitNet`

## Notes

- These examples validate that the abstract machinery works on concrete objects.
- The paper explicitly discusses the "I × {0,1}" counterexample (Section 1.1) as motivation for C4s.
- The three-qubit model is the paper's main pedagogical example (Section 2.4).
