# Formalizing IQT: A Roadmap for Lean/PhysLean and Coq

**Boboo — February 2026**

-----

## 1. What's Actually Provable vs. What's a Postulate

Before touching a proof assistant, we need to sort IQT's claims into three bins:

**Bin A — Mathematical theorems (fully formalizable).** These are derivable from AQFT axioms with no consciousness language. The Constraint Convergence proposition (§1.1) lives here. So do the properties of the unity functional U (§3.3), the composition theorem sketch (§3.2), and the algebraic facts about Type III₁ factors, Reeh-Schlieder, Haag duality from §0.

**Bin B — Bridge hypotheses with mathematical content (partially formalizable).** The effective-theory framework (§2.6) has a formalizable core: the embedding ι is an injective *-homomorphism, and the conditional expectation E_eff is CPTP. The coarse-graining monotonicity (P3) is a theorem about quantum mutual information under CPTP maps. The self-thread persistence conditions and narrative operator constraints have mathematical skeletons that can be axiomatized even if the neuroscience is empirical.

**Bin C — Metaphysical postulates (axiomatizable but not provable).** Quality Identity (QI), the Intrinsicness Principle, and the identification of phenomenal quality with the algebra-state pair. These get formalized as axioms in a foundational theory — you can prove things *from* them, but you can't prove them.

The formalization project is about making Bins A and B machine-checked, and making Bin C precise enough that its consequences are derivable.

-----

## 2. The Landscape of Available Tools

### 2.1 Lean 4 / Mathlib / PhysLean

**What exists today:**

- Mathlib has C*-algebra basics: `CStarAlgebra`, `CStarRing`, Hilbert C*-modules (`CStarModule`), some spectral theory, and substantial functional analysis infrastructure (Banach spaces, bounded operators, etc.)
- Mathlib has von Neumann entropy for finite-dimensional systems via `MeasureTheory` and linear algebra
- Mathlib has category theory (functors, presheaves, natural transformations) — relevant for the presheaf formulation IQT hints at in §7
- PhysLean has Wick's theorem formalized, basic QFT operator structures, and index notation. It's explicitly designed to be flexible about axiomatizations
- Mathlib does NOT have: nets of local algebras, Haag-Kastler axioms, causal set theory, modular theory of von Neumann algebras, or Type III factor classification

**The gap:** The core AQFT machinery that IQT rests on — local nets, isotony as a functorial property, the Reeh-Schlieder theorem, Type III₁ structure — is not formalized anywhere. This is both the main obstacle and the main opportunity. Formalizing even the Haag-Kastler axioms in Lean would be a standalone contribution to mathematical physics.

### 2.2 Coq / MathComp

**What exists today:**

- MathComp has strong finite group theory, linear algebra over arbitrary fields
- CoqQ (Zhou et al.) formalizes finite-dimensional quantum mechanics: Hilbert spaces, quantum gates, density matrices, partial trace
- Modal logic embeddings exist in Coq (Benzmüller & Paleo's higher-order modal logic framework, QRC₁ formalization)
- Less category theory infrastructure than Mathlib

**The gap:** Same AQFT gap as Lean. But Coq's modal logic tools are more mature — relevant for formalizing the perspectival/modal aspects of IQT.

### 2.3 The Dable-Heath et al. Paper (PhysRevD 101, 065013)

This is critical context. Dable-Heath, Fewster, Rejzner & Woods (2020) construct pAQFT models on causal sets using perturbative methods. They provide:

- Discretized wave operators on causal sets (including a "preferred past" proposal)
- Classical free and interacting field theory models on fixed causal sets
- Relative Cauchy evolution for observables sensitive to background changes
- Deformation quantization via pAQFT methods
- The SJ (Sorkin-Johnston) state as a distinguished quantum state

This paper is the closest thing to a rigorous construction of AQFT on causal sets — exactly the mathematical substrate IQT's §2.0 assumes. Formalizing its constructions would simultaneously ground IQT and contribute to causal set QFT.

-----

## 3. Formalization Strategy: Three Tracks

### Track 1: Core AQFT in Lean (Foundation Layer)

This is the heavy lift. Build the Haag-Kastler net structure in Lean, leveraging Mathlib's existing C*-algebra and category theory.

**Phase 1a — Nets of algebras on posets (3-6 months)**

```
-- The type of a net of C*-algebras on a directed poset of regions
structure LocalNet (R : Type*) [PartialOrder R] where
  algebra : R → CStarAlgebra
  -- Isotony: inclusion of regions gives *-homomorphism of algebras
  isotony : ∀ {D₁ D₂ : R}, D₁ ≤ D₂ → StarAlgHom (algebra D₁) (algebra D₂)
  -- Functoriality: composing inclusions commutes
  isotony_comp : ∀ {D₁ D₂ D₃ : R} (h₁₂ : D₁ ≤ D₂) (h₂₃ : D₂ ≤ D₃),
    isotony (le_trans h₁₂ h₂₃) = (isotony h₂₃).comp (isotony h₁₂)
```

This is a presheaf on the poset of regions — Mathlib's category theory library handles the abstract structure, but instantiating it for C*-algebras requires connecting the algebra and category layers.

**Phase 1b — Causal structure and microcausality (2-4 months)**

```
-- Causal set: locally finite partial order
structure CausalSet where
  events : Type*
  [inst_partial : PartialOrder events]
  [inst_finite : LocallyFiniteOrder events]

-- Causal diamond
def CausalDiamond (C : CausalSet) (p q : C.events) (h : p ≤ q) : Set C.events :=
  {x | p ≤ x ∧ x ≤ q}

-- Spacelike separation
def SpacelikeSep (C : CausalSet) (x y : C.events) : Prop :=
  ¬(x ≤ y) ∧ ¬(y ≤ x)

-- Microcausality axiom on a net
def Microcausal (N : LocalNet R) (sep : R → R → Prop) : Prop :=
  ∀ D₁ D₂, sep D₁ D₂ →
    ∀ (a : N.algebra D₁) (b : N.algebra D₂),
      -- commutation in the ambient algebra
      N.isotony (le_sup_left) a * N.isotony (le_sup_right) b =
      N.isotony (le_sup_right) b * N.isotony (le_sup_left) a
```

**Phase 1c — States, restrictions, and the algebra-state pair (2-3 months)**

```
-- State on a C*-algebra: positive normalized linear functional
structure CStarState (A : CStarAlgebra) where
  functional : A →ₗ[ℂ] ℂ
  positive : ∀ a, 0 ≤ functional (star a * a)
  normalized : functional 1 = 1

-- Restriction of a global state to a local algebra
def restrict_state {N : LocalNet R} (ω : CStarState (N.quasilocal))
    (D : R) : CStarState (N.algebra D) :=
  { functional := ω.functional.comp (N.isotony (le_quasilocal D))
    positive := ...
    normalized := ... }

-- The algebra-state pair (IQT's quality)
structure Quality (N : LocalNet R) (D : R) where
  alg : N.algebra D
  state : CStarState (N.algebra D)
```

**Phase 1d — The Constraint Convergence Proposition (1-2 months)**

This is the crown jewel of Track 1 — formalizing §1.1's proof that any intrinsic-nature assignment satisfying Constraints 1-4 is naturally equivalent to D ↦ (A(D), ω_D).

```
-- Intrinsic nature assignment
structure IntrinsicNatureAssignment (N : LocalNet R) where
  assign : R → Type*
  -- Constraint 1: Completeness
  complete : ∀ D, ∀ A ∈ N.algebra D,
    -- I(D) determines ω_D(A)
    determines_expectation (assign D) A
  -- Constraint 2: Isotony
  iso : ∀ D₁ D₂, D₁ ≤ D₂ → recoverable (assign D₁) (assign D₂)
  -- Constraint 3: Covariance
  covar : ∀ g : NetAutomorphism N, ∀ D,
    assign (g.map D) = g.act (assign D)
  -- Constraint 4: Perspectival completeness
  local : ∀ D, depends_only_on (assign D) (N.algebra D)

-- The theorem
theorem constraint_convergence (N : LocalNet R) (I : IntrinsicNatureAssignment N) :
    NatEquiv I.assign (fun D => Quality N D) := by
  ...
```

The proof sketch in the paper is clean enough to formalize: Constraint 1 implies I(D) determines ω_D, Constraint 4 implies I(D) depends only on (A(D), ω_D), Constraint 2 forces compatibility with restriction, Constraint 3 gives equivariance.

### Track 2: Finite-Dimensional IQT in Coq (Rapid Prototyping)

While Track 1 builds the infinite-dimensional foundation, Track 2 formalizes IQT's finite-dimensional toy models in Coq using CoqQ's existing quantum mechanics library. This gets results fast.

**Phase 2a — Three-qubit toy model (1-2 months)**

Using CoqQ's density matrix formalism, formalize §2.4:

```coq
(* The three-qubit GHZ and mixture states *)
Definition ghz : Density (ℂ^8) := ...
Definition mix : Density (ℂ^8) := ...

(* Local algebras via partial trace *)
Definition local_A (ρ : Density (ℂ^8)) : Density (ℂ^2) := ptrace_BC ρ.
Definition local_AB (ρ : Density (ℂ^8)) : Density (ℂ^4) := ptrace_C ρ.

(* Theorem: same local qualities, different global quality *)
Theorem same_marginals_different_global :
  local_A ghz = local_A mix ∧
  local_A (swap_AB ghz) = local_A (swap_AB mix) ∧  (* B marginal *)
  ghz ≠ mix.

(* Unity functional *)
Definition mutual_info (ρ_AB : Density (ℂ^4))
    (ρ_A : Density (ℂ^2)) (ρ_B : Density (ℂ^2)) : ℝ :=
  von_neumann_entropy ρ_A + von_neumann_entropy ρ_B - von_neumann_entropy ρ_AB.

Definition unity (ρ : Density (ℂ^8)) : ℝ :=
  min_over_bipartitions (fun bip => mutual_info (marginal bip ρ) ...).

(* Theorem: U vanishes for product states *)
Theorem unity_zero_product : ∀ ρ_A ρ_B ρ_C,
  unity (tensor3 ρ_A ρ_B ρ_C) = 0.

(* Theorem: coarse-graining monotonicity *)
Theorem unity_monotone_coarsegrain : ∀ ρ E,
  CPTP E → unity (apply_channel E ρ) ≤ unity ρ.
```

**Phase 2b — Composition theorem for finite dimensions (2-3 months)**

Formalize the extension set Ext(ω₁, ω₂) and prove it's generally not a singleton:

```coq
(* Extension set: global states compatible with given marginals *)
Definition ext_set (ρ_A : Density (ℂ^n)) (ρ_B : Density (ℂ^m))
    : Set (Density (ℂ^(n*m))) :=
  { ρ_AB | ptrace_B ρ_AB = ρ_A ∧ ptrace_A ρ_AB = ρ_B }.

(* The extension set is generally not a singleton *)
Theorem ext_not_singleton :
  ∃ ρ_A ρ_B, ¬ Subsingleton (ext_set ρ_A ρ_B).
```

This connects to the quantum marginal problem (Klyachko 2004) — there's a body of work on which marginals are compatible with which global states.

**Phase 2c — Modal logic layer for perspectival relativity (3-4 months)**

This is where Coq's modal logic tools come in. IQT's perspectival relativity has a natural modal reading: "quality is relative to a region D" is structurally similar to "truth is relative to a possible world w." The poset of diamonds is a Kripke frame.

```coq
(* Kripke frame: diamonds ordered by inclusion *)
Record QualityFrame := {
  diamonds : Type;
  includes : diamonds → diamonds → Prop;
  includes_po : PreOrder includes;

  (* Each diamond has an algebra and state *)
  quality : diamonds → AlgStatePair;

  (* Accessibility = inclusion *)
  accessible := includes;
}.

(* Modal operators *)
(* □φ at D means: φ holds at all sub-diamonds of D *)
(* ◇φ at D means: φ holds at some sub-diamond of D *)

(* The isotony principle as a modal axiom *)
(* If observable A has value v at D, then A has value v at any D' ⊇ D *)
Axiom isotony_modal : ∀ D D' A v,
  includes D D' → holds_at D (obs_has_value A v) →
  holds_at D' (obs_has_value A v).

(* Perspectival completeness as a modal principle *)
(* Quality at D is determined by what's true at D alone *)
Axiom perspectival_completeness : ∀ D φ,
  holds_at D φ ↔ locally_determined D φ.
```

The modal logic encoding makes IQT's "no view from nowhere" claim formally precise. It also enables reasoning about the interplay between different scales — the nesting of diamonds becomes accessibility in the Kripke frame.

### Track 3: Effective Theory Bridge in Lean (Connecting to Experiments)

This track formalizes §2.6's effective-theory framework — the bridge from fundamental algebras to neural-scale observables.

**Phase 3a — CPTP maps and data processing inequality (1-2 months)**

Mathlib already has some of this. The key theorem:

```
-- Data processing inequality (the formal core of P3)
theorem dpi_mutual_info {A B : FiniteDimCStarAlgebra}
    (E : CPTPMap A B) (ρ : State (A ⊗ A')) :
    mutual_info (E.apply_left ρ) ≤ mutual_info ρ := by
  ...
```

**Phase 3b — Effective algebra as subalgebra (2-3 months)**

```
-- The embedding ι : A_eff ↪ A_fund
structure EffectiveTheoryBridge (N : LocalNet R) (D : R) where
  eff_algebra : FiniteDimCStarAlgebra
  embedding : StarAlgHom eff_algebra (N.algebra D)
  injective : Function.Injective embedding
  -- Physical locality: respects net structure
  local : ∀ D' ≤ D, ∀ a ∈ eff_algebra,
    localized_in D' (embedding a) → a ∈ eff_subalgebra D'
  -- Effective state by restriction
  eff_state (ω : CStarState (N.algebra D)) : CStarState eff_algebra :=
    restrict_along_embedding ω embedding

-- Coarse-graining monotonicity for effective quality
theorem eff_quality_conservative (bridge : EffectiveTheoryBridge N D)
    (ω : CStarState (N.algebra D)) :
    info_content (bridge.eff_state ω) ≤ info_content ω := by
  apply dpi_mutual_info
  exact bridge.conditional_expectation.cptp
```

**Phase 3c — Formalizing the metrics P, K, R (2-3 months)**

Define the empirical metrics as functionals on the effective state:

```
-- Thread persistence metric
def persistence_metric (j : Module) (w : TimescaleWindow)
    (ρ : EffectiveState) : ℝ :=
  temporal_mutual_info j w ρ * effective_dimensionality j w ρ

-- Cross-module coherence
def coherence_metric (j l : Module) (ρ : EffectiveState) : ℝ :=
  dwpli j l ρ  -- debiased weighted phase-lag index

-- Readout dominance
def readout_dominance (prefrontal motor : Module) (ρ : EffectiveState) : ℝ :=
  transfer_entropy prefrontal motor ρ
```

-----

## 4. Recommended Approach: Start with Lean, Supplement with Coq

**Primary: Lean 4 + Mathlib + PhysLean.** The reasons:

1. Mathlib's C*-algebra library is already ahead of MathComp for operator algebras
1. PhysLean is explicitly designed for physics formalizations and welcomes contributions
1. Lean's tactic language and type class system handle the algebraic hierarchy naturally
1. The category-theoretic infrastructure for presheaves is mature
1. AI-assisted proving (DeepSeek-Prover, AlphaProof) is most advanced for Lean

**Secondary: Coq for modal logic proofs.** Use Coq specifically for:

1. The perspectival relativity encoding via Kripke semantics
1. Quick prototyping of finite-dimensional toy models using CoqQ
1. Any reasoning that benefits from MathComp's strong decidability/computation support

**Interoperability:** The two proof assistants can't directly share proofs, but they can share *statements*. A theorem proven in Coq can be axiomatized in Lean (and vice versa) with a clear note that the proof exists in the other system. Long-term, translation tools (e.g., Lean-Coq bridges via intermediate representations) may make this seamless.

-----

## 5. What Gets Proven at Each Stage

### Stage 1 (Months 1-6): Foundations

|Theorem                                |Tool|Status           |
|---------------------------------------|----|-----------------|
|Haag-Kastler axioms as a Lean structure|Lean|New formalization|
|Causal diamond lattice on finite posets|Lean|New formalization|
|Three-qubit toy model (§2.4)           |Coq |Uses CoqQ        |
|U vanishes for product states (P1)     |Coq |Uses CoqQ        |
|Data processing inequality             |Lean|Extends Mathlib  |

### Stage 2 (Months 6-12): Core Theorems

|Theorem                                 |Tool|Status                  |
|----------------------------------------|----|------------------------|
|Constraint Convergence (§1.1)           |Lean|The main target         |
|Extension set non-singleton (§3.2)      |Coq |Quantum marginal problem|
|Coarse-graining monotonicity (P3)       |Lean|DPI application         |
|Perspectival relativity as Kripke frame |Coq |Modal logic encoding    |
|Effective algebra inherits net structure|Lean|New result              |

### Stage 3 (Months 12-18): Bridge to Experiments

|Theorem                                          |Tool|Status                        |
|-------------------------------------------------|----|------------------------------|
|CPTP embedding preserves algebraic structure     |Lean|New formalization             |
|Metrics P, K, R as functionals on effective state|Lean|Definitions + basic properties|
|Toy pipeline (§4.5.1) — partial trace chain      |Coq |Uses CoqQ                     |
|Narrative operator constraints as type class     |Lean|Axiomatization                |

-----

## 6. The Hard Parts (Where You'll Get Stuck)

**Type III₁ factors.** IQT's §1.2 discussion of why physically induced isomorphisms are needed relies on Connes' classification: all hyperfinite Type III₁ factors are abstractly isomorphic. Formalizing this is a multi-year project. The workaround: axiomatize the classification result and derive consequences. The finite-dimensional toy models don't need it.

**Reeh-Schlieder theorem.** The proof uses the edge-of-the-wedge theorem and analytic continuation. Formalizing this requires complex analysis infrastructure that Mathlib has partially but not completely. Again, axiomatize and move on for now.

**The pAQFT construction on causal sets.** Dable-Heath et al.'s construction is rigorous but technically dense — discretized wave operators, deformation quantization, the SJ state. Formalizing even the free field case on a finite causal set would be a substantial project. Priority: formalize the *structure* (nets on posets with the right properties) rather than the *construction* (how to build specific models).

**Gauge superselection.** IQT's §0.3 is honest about this being open. Don't try to formalize QED — stay with gauge-free examples (free scalar field, free Maxwell field) and the finite-dimensional models.

-----

## 7. What This Buys IQT

A successful formalization campaign delivers:

1. **Machine-verified constraint convergence.** The claim that the algebra-state pair is the *unique* candidate satisfying Constraints 1-4 becomes a theorem, not a proof sketch. Reviewers can check it by running `lean --run`.
1. **Precise failure conditions.** Formalizing the bridge hypotheses makes explicit exactly where the theory can fail. If a property doesn't follow from the axioms, the proof assistant will tell you — potentially revealing hidden assumptions.
1. **Interoperability with IIT formalization efforts.** If IIT's Φ is also formalized (there's interest in the IIT community), the formal comparison between U and Φ — which IQT §3.3 leaves as an open question — becomes a well-posed mathematical problem.
1. **Credibility signal.** A consciousness theory with machine-checked mathematical content would be unprecedented. It separates IQT from theories that rely on informal mathematical analogies.
1. **Forced precision on the narrative operator.** IQT's §4.5 acknowledges N is the weakest link. Trying to formalize it — even the toy pipeline — will force decisions about what exactly N's type signature is, what its input/output spaces are, and what constraints it satisfies. The proof assistant won't let you hand-wave.

-----

## 8. Concrete Next Steps

1. **Open a PhysLean issue** proposing the Haag-Kastler axioms as a formalization target. The PhysLean community is receptive and the axioms are clean mathematics — no consciousness controversy needed.
1. **Fork CoqQ and build the three-qubit toy model.** This is a weekend project that produces a working artifact.
1. **Write the `LocalNet` structure in Lean** as a proof-of-concept. Even without proofs, getting the type signatures right is clarifying.
1. **Contact Fewster/Rejzner** (authors of the causal set pAQFT paper) about whether they'd be interested in a formalization collaboration. They're at York and active in the community.
1. **Pre-register the formalization targets** alongside the experimental protocols. "We will prove Theorem X in Lean by date Y" is a commitment with the same epistemic structure as pre-registering an experiment.
