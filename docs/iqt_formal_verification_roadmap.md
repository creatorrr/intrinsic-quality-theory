# Formal Verification Roadmap: IQT Postulates in Lean/PhysLean and Coq/Modal Logic

## 1. Executive Summary

This document charts a path for rigorously proving (or machine-checking) the postulates and theorems of Intrinsic Quality Theory (IQT v1.7.0) using interactive theorem provers. We evaluate two complementary approaches:

- **Lean 4 / PhysLean / Mathlib** — for the algebraic-structural core (C\*-algebras, nets of local algebras, state restrictions, the constraint convergence proposition)
- **Coq / Modal Logic** — for the metaphysical and modal content (the Quality Identity postulate, intrinsicness principle, perspectival relativity, and the three-level hierarchy)

The strategies are complementary, not competing. Lean/Mathlib excels at the mathematical infrastructure IQT inherits from AQFT. Coq/modal logic excels at formalizing the philosophical architecture and the "if-then" structure connecting postulates to consequences.

---

## 2. Inventory of IQT Claims by Formal Character

### 2.1 Mathematical Theorems (provable from AQFT axioms)

These are results IQT *inherits* from established mathematics — they are theorems, not postulates. A formal proof would verify IQT's mathematical foundation is sound.

| ID | Claim | Source | Character |
|----|-------|--------|-----------|
| **T1** | Local algebras R(D) for free scalar field form a net satisfying isotony, microcausality, Haag duality | §0.1 | Theorem (AQFT) |
| **T2** | R(D) is a Type III₁ factor in Connes classification | §0.1 | Theorem (Araki 1964, Fredenhagen 1985) |
| **T3** | Vacuum vector Ω is cyclic and separating (Reeh-Schlieder) | §0.1 | Theorem |
| **T4** | Coherent state ω_α differs from vacuum ω_0 on R(D) when α\|_D ≠ 0 | §0.1 | Theorem (computation) |
| **T5** | State restriction is well-defined and compatible with isotony | §0.1, §2.3 | Theorem |
| **T6** | All hyperfinite Type III₁ factors are abstractly isomorphic (Connes classification) | §1.2 | Theorem |
| **T7** | Quantum mutual information is non-increasing under CPTP maps (data-processing inequality) | §3.3 (P3) | Theorem |
| **T8** | Unity functional U(D) vanishes for product states | §3.3 (P1) | Theorem (direct computation) |
| **T9** | U(D) increases with cross-boundary dependence | §3.3 (P2) | Theorem |
| **T10** | Constraint Convergence Proposition: any intrinsic-nature assignment satisfying C1-C4 is naturally equivalent to D ↦ (A(D), ω_D) | §1.1 | Theorem (given AQFT axioms + C1-C4) |

### 2.2 Metaphysical Postulates (axioms requiring formalization, not proof)

These are IQT's core bets — they cannot be derived from physics alone. Formal verification here means: *formalizing them precisely and proving that the claimed consequences follow*.

| ID | Postulate | Source | Character |
|----|-----------|--------|-----------|
| **P1** | **Quality Identity (QI)**: The intrinsic nature of a bounded spacetime region — the local algebra-state pair (A(D), ω_D) — is phenomenal quality | §1.1 | Metaphysical identity axiom |
| **P2** | **Intrinsicness Principle**: Two situations are intrinsically identical for D iff they agree on Q(D) = (A(D), ω_D) up to net-induced \*-isomorphism | §1.3 | Metaphysical commitment |
| **P3** | **Democracy of Diamonds**: Every bounded spacetime region bears quality; no exclusion principle selects a unique "conscious" region | §2.5, §4.4 | Structural commitment |
| **P4** | **Perspectival Relativity**: Quality is relative to the region; there is no "view from nowhere" | §2.5 | Structural commitment |

### 2.3 Bridge Hypotheses (empirically revisable, formally derivable from P1-P4)

| ID | Hypothesis | Source | Character |
|----|-----------|--------|-----------|
| **B1** | Self-threads (Level 1) = temporally persistent, causally semi-autonomous quality-streams | §4.4 | Functional definition |
| **B2** | Narrative operators (Level 2) = self-threads with dominant readout access and recursive self-modeling | §4.5 | Functional definition |
| **B3** | Shape-phenomenology mapping: diamond geometry determines experience character | §2.6-2.7 | Derived claim (from QI + diamond geometry) |
| **B4** | Composition via correlation structure: the "glue" is cross-boundary correlators, not a binding force | §3.1 | Derived claim (from AQFT extension problem) |

### 2.4 Open Mathematical Problems

| ID | Problem | Source | Status |
|----|---------|--------|--------|
| **O1** | Boundary data problem: What is the minimal composition datum C such that (Q_1, Q_2, C) determines Q_{1∪2}? | §3.4, §7 | Open |
| **O2** | Presheaf/sheaf formulation of quality functor on the poset of causal diamonds | §7 | Natural but open |
| **O3** | Fundamental-level unity functional using modular-theoretic tools (Araki relative entropy) | §3.3, §7 | Open |
| **O4** | Rigorous construction of AQFT net on causal sets satisfying Haag-Kastler analogues | §2.0, §7 | Active research (Dable-Heath, Fewster, Rejzner, Woods 2020) |

---

## 3. Strategy A: Lean 4 / PhysLean / Mathlib

### 3.1 What Exists Today

**Mathlib (as of early 2026):**
- **C\*-algebras**: `CStarAlgebra` and `NonUnitalCStarAlgebra` classes are fully defined. Star algebras, star subalgebras, and closure properties are available.
- **Continuous Functional Calculus**: Fully formalized by Dedecker & Loreaux (2025) — the first such formalization in any proof assistant. This is the most fundamental construction in operator algebra theory.
- **Hilbert C\*-modules**: Formalized via `CStarModule`.
- **Von Neumann algebras**: `Mathlib.Analysis.VonNeumannAlgebra` module exists but is less developed than C\*-algebra support. Type classification (III₁ etc.) is not yet formalized.
- **Category theory**: Extensive — functors, natural transformations, limits, colimits, adjunctions.
- **Presheaves and sheaves**: Well-developed. `TopCat.Presheaf C X` defined as `(Opens X)ᵒᵖ ⥤ C`. Grothendieck topologies, sites, and sheaf conditions formalized. The infrastructure for IQT's quality-as-presheaf picture exists.
- **Quantum information**: The Lean-QuantumInfo library has 1000+ theorems including density matrices, quantum channels, entropy.

**PhysLean (as of early 2026):**
- Covers electromagnetism, QM, particle physics, statistical mechanics, and perturbative QFT.
- **Wick's theorem** formalized (May 2025) — the first result from perturbative QFT in any proof assistant.
- Weyl algebras and Wightman functions are NOT yet formalized.
- Haag-Kastler axioms (AQFT net structure) are NOT yet formalized.
- Causal set structures are NOT yet formalized.
- PhysLean is explicitly *not* tied to axiomatic QFT — it accommodates multiple approaches.

**Dable-Heath, Fewster, Rejzner & Woods (PhysRevD 101, 065013, 2020):**
- Constructs pAQFT models on causal sets using discretized wave operators.
- Defines the SJ state as a quantum state on free theory.
- Builds interacting models via deformation quantization.
- This is the mathematical foundation IQT §2.0 cites for "AQFT on causal sets." The paper provides the construction; formalizing it in Lean would directly ground IQT's mathematical substrate.

### 3.2 What Must Be Built

The formalization proceeds in layers, from the mathematical bedrock upward.

#### Layer 0: Algebraic Infrastructure (extends Mathlib)

```
-- Target: ~3-6 months for experienced Lean contributor
-- Dependencies: Mathlib CStarAlgebra, VonNeumannAlgebra

1. Von Neumann algebra classification
   - Formalize Type I, II, III factors
   - Prove Type III₁ characterization (Connes classification)
   - This is substantial but well-defined mathematics

2. Modular theory (Tomita-Takesaki)
   - Modular automorphism group σ^ω_t
   - KMS condition
   - Araki relative entropy S(ω | φ)
   - Required for fundamental-level unity functional (O3)

3. Normal states and GNS construction
   - GNS representation from a state on a C*-algebra
   - Faithful representations
   - Cyclic and separating vectors
```

#### Layer 1: AQFT Net Structure (new PhysLean module)

```
-- Target: ~3-6 months
-- Dependencies: Layer 0

1. Haag-Kastler axioms as a Lean structure
   structure HaagKastlerNet (S : Type*) [PartialOrder S] where
     algebra : S → Type*                    -- D ↦ A(D)
     [cstar : ∀ D, CStarAlgebra (algebra D)]
     inclusion : ∀ {D₁ D₂}, D₁ ≤ D₂ → (algebra D₁) →⋆ₐ (algebra D₂)  -- isotony
     commute : ∀ {D₁ D₂}, SpacelikeSeparated D₁ D₂ →
       ∀ (a : algebra D₁) (b : algebra D₂), Commute (embed a) (embed b)  -- microcausality

2. State restrictions
   def restrict (ω : State (algebra D₂)) (h : D₁ ≤ D₂) : State (algebra D₁)

3. Net-induced *-isomorphisms
   -- The equivalence relation on algebra-state pairs
   -- that respects only physically induced identifications

4. Haag duality
   -- R(D)' = R(D') where D' is the causal complement

5. Reeh-Schlieder property
   -- Vacuum Ω is cyclic and separating for R(D)
```

#### Layer 2: IQT-Specific Definitions (new IQT module)

```
-- Target: ~2-3 months
-- Dependencies: Layers 0-1

1. Quality as algebra-state pair
   def Quality (net : HaagKastlerNet S) (D : S) (ω : GlobalState net) :=
     ⟨net.algebra D, restrict ω D⟩  -- up to net-induced *-iso

2. The constraint argument (Prop §1.1)
   -- Formalize Constraints C1-C4 as predicates
   -- Prove: any assignment satisfying C1-C4 is naturally equivalent
   -- to D ↦ (A(D), ω_D)
   -- THIS IS THE KEY THEOREM TO FORMALIZE

3. Intrinsicness Principle (axiom, not theorem)
   axiom intrinsicness_principle :
     ∀ D ω₁ ω₂, Quality net D ω₁ = Quality net D ω₂ →
       IntrinsicallyIdentical D ω₁ ω₂

4. Unity functional
   def unity (D : S) (ω : State (algebra D)) : ℝ≥0 :=
     ⨅ (π : Bipartition D), mutualInformation (restrict ω π.left) (restrict ω π.right)

5. Properties of U
   theorem unity_vanishes_product : IsProduct ω π → unity D ω = 0
   theorem unity_monotone_coarsegraining : unity_eff D ω ≤ unity D ω
```

#### Layer 3: Causal Sets (extends PhysLean, connects to Dable-Heath et al.)

```
-- Target: ~4-6 months (hardest layer)
-- Dependencies: Layers 0-2

1. Causal set as locally finite partial order
   structure CausalSet where
     carrier : Type*
     [inst : PartialOrder carrier]
     [locally_finite : LocallyFiniteOrder carrier]

2. Double cones / Alexandrov sets
   def doubleCone (p q : C) (h : p ≤ q) : Set C :=
     {x | p ≤ x ∧ x ≤ q}

3. Discretized wave operators (following Dable-Heath et al. 2020)
   -- The "preferred past" construction
   -- Retarded/advanced Green functions on causal sets

4. Free field algebra on causal set diamonds
   -- Weyl algebra generated by W(f) for test functions on causal set
   -- Verify Haag-Kastler axioms

5. SJ state construction
```

### 3.3 What Can Be Proved in Lean

| Claim | Feasibility | Dependencies | Notes |
|-------|-------------|--------------|-------|
| **T10** (Constraint Convergence) | **HIGH** — purely algebraic argument | Layer 2 | The crown jewel. A clean proof from C1-C4 to uniqueness of algebra-state pair. |
| **T7** (Data-processing inequality) | **HIGH** — known result | Lean-QuantumInfo or Mathlib | May already be partially formalized |
| **T8** (U vanishes for products) | **HIGH** — direct computation | Layer 2 | Straightforward |
| **T5** (State restriction compatibility) | **HIGH** — standard AQFT | Layer 1 | Follows from net axioms |
| **T1** (Net properties for free field) | **MEDIUM** — requires Weyl algebra construction | Layer 1 + Layer 3 | Substantial but well-understood |
| **T2** (Type III₁) | **LOW-MEDIUM** — deep result, needs modular theory | Layer 0 | Connes classification is a major undertaking |
| **T3** (Reeh-Schlieder) | **LOW** — requires distributional analysis | Layer 0 + Layer 1 | Needs Wightman function theory |
| **B4** (Composition = correlation) | **MEDIUM** — quantum marginal problem | Layer 2 | Partial results in finite dim |
| **O2** (Quality as presheaf) | **MEDIUM** — infrastructure exists | Layer 2 + Mathlib presheaves | Mathlib has presheaf machinery; just needs the IQT-specific functor |

### 3.4 Recommended Lean Attack Order

```
Phase 1 (Months 1-3): "Prove the constraint argument"
├── Define HaagKastlerNet structure (simplified, finite-dimensional first)
├── Define Constraints C1-C4 as Lean predicates
├── Prove Constraint Convergence (T10) in finite dimensions
├── Define Quality, Unity functional
└── Prove U properties (T7, T8, T9) using Lean-QuantumInfo

Phase 2 (Months 3-6): "Build the presheaf picture"
├── Define Quality functor Q : Diamonds^op → C*Alg×State
├── Prove it forms a presheaf (using Mathlib presheaf infrastructure)
├── Prove isotony = functoriality
├── Prove Intrinsicness Principle is consistent with net structure
└── Connect to extension problem (B4) in finite dimensions

Phase 3 (Months 6-12): "Ground in AQFT"
├── Formalize Weyl algebra in PhysLean
├── Construct free scalar field net
├── Verify Haag-Kastler axioms (T1)
├── Prove T4 (coherent vs vacuum states differ locally)
└── Connect to Dable-Heath et al. causal set construction

Phase 4 (Months 12-18): "Deep structural results"
├── Tomita-Takesaki modular theory in Mathlib
├── Connes classification (T2, T6) — partial, Type III characterization
├── Araki relative entropy → fundamental unity functional (O3)
└── Reeh-Schlieder (T3) — aspirational
```

---

## 4. Strategy B: Coq / Modal Logic

### 4.1 Why Modal Logic?

IQT has a rich modal structure that the algebraic formalization in Lean doesn't capture:

- **Perspectival relativity** (§2.5) is a claim about *possible perspectives* — different diamonds as different "possible worlds" from which quality is assessed
- **The Intrinsicness Principle** (§1.3) is a modal claim: what is *necessarily* intrinsic to D vs *contingently* extrinsic
- **Quality Identity** (§1.1) is an identity claim across two descriptions — formally analogous to modal identity (Kripke's necessary a posteriori)
- **The three-level hierarchy** (Quality → Experience → Report) involves modal operators: "necessarily has quality" (Level 0) vs "contingently has experience" (Level 1)
- **Democracy vs Exclusion** — IIT's exclusion postulate is a modal claim about what's *possible*; IQT's democracy is the denial of that modal constraint

### 4.2 What Exists Today

**Coq Modal Logic Libraries:**
- **S5 formalization** (University of Groningen): Kripke frames as records `(W, R, V)` with S5 = equivalence relation. Soundness and completeness proved. Hilbert system as proof system.
- **Henkin-style completeness** (Doczal & Smolka): Constructive completeness proof for extensions of K. First formalization of S5 completeness of its kind.
- **Quantified modal logic** (arXiv:2206.03358): Based on MathComp/SSReflect. Extends beyond propositional to first-order modal logic.

### 4.3 The IQT Modal Framework

We define a modal logic `IQT-ML` whose models are nets of local algebras:

```
-- Kripke-style semantics where "worlds" are diamonds

World := Diamond  -- bounded spacetime regions
R := ⊆            -- accessibility = inclusion (isotony)

-- This gives S4 (reflexive + transitive), not S5
-- IQT needs S4 for nesting, not S5

-- Propositions are predicates on algebra-state pairs
Prop_IQT := (Algebra × State) → Prop

-- Modal operators
□ φ  at D  :=  ∀ D' ⊇ D, φ(Q(D'))    -- "necessarily φ" = φ holds at all containing diamonds
◇ φ  at D  :=  ∃ D' ⊇ D, φ(Q(D'))    -- "possibly φ" = φ holds at some containing diamond

-- IQT-specific operators
■ φ  at D  :=  ∀ D' ⊆ D, φ(Q(D'))    -- "intrinsically φ" = φ holds at all sub-diamonds
◆ φ  at D  :=  ∃ D' ⊆ D, φ(Q(D'))    -- "somewhere within φ" = φ holds at some sub-diamond
```

### 4.4 What Can Be Proved in Coq

#### A. Metatheorems about IQT's logical structure

| Claim | Formalization | Feasibility |
|-------|---------------|-------------|
| Constraint Convergence is valid in all IQT models | Model-theoretic proof | **HIGH** |
| QI + Democracy entails no exclusion | □(Quality(D)) for all D, so ¬∃ unique D with □(Conscious(D)) | **HIGH** |
| Intrinsicness Principle is consistent with isotony | If Q(D₁) = Q(D₂) under net-iso, then ■φ(D₁) ↔ ■φ(D₂) | **HIGH** |
| Level hierarchy is well-founded | Level 0 ⊃ Level 1 ⊃ Level 2, each with additional modal conditions | **HIGH** |
| Composition underdetermination | ◆φ(D₁) ∧ ◆φ(D₂) ↛ ◆φ(D₁∪D₂) — knowing parts doesn't determine whole | **HIGH** |
| Perspectival relativity: no absolute quality | ¬∃ φ such that φ is frame-independent across all diamonds | **MEDIUM** |
| Democracy ↔ ¬Exclusion (formal equivalence) | ∀D. Quality(D) ↔ ¬(∃! D*. Conscious(D*) ∧ ∀D≠D*. ¬Conscious(D)) | **HIGH** |

#### B. Derivation of consequences from postulates

```
-- The key metatheorems to prove:

1. QI + Isotony → Perspectival Relativity
   -- If quality = algebra-state pair and algebras nest,
   -- then quality is relative to diamond

2. QI + Democracy + Correlation Structure → Composition
   -- If every diamond has quality and quality includes correlators,
   -- then composition = extension problem

3. QI + Self-Thread Definition → Subject Selection Dissolution
   -- If quality is universal and "subject" = persistent quality-stream,
   -- then "which system is conscious?" becomes empirical, not metaphysical

4. QI + Diamond Geometry + Finite Bandwidth → Temporal Phenomenology
   -- If quality = algebra-state pair and the algebra depends on
   -- diamond shape, then temporal integration window determines
   -- temporal experience character

5. QI + Intrinsicness Principle → Mary's Room Resolution
   -- If quality = physical state and Mary's visual cortex has never
   -- instantiated Q_red, then seeing red = gaining a new quality class
```

### 4.5 Recommended Coq Attack Order

```
Phase 1 (Months 1-2): "Set up the modal framework"
├── Define Diamond, Net, Quality as Coq inductive types
├── Define Kripke semantics with diamonds-as-worlds
├── Define □, ◇, ■, ◆ operators
├── Prove basic modal properties (S4 for inclusion order)
└── Encode QI, Intrinsicness Principle, Democracy as axioms

Phase 2 (Months 2-4): "Prove the metatheorems"
├── Prove QI + Isotony → Perspectival Relativity
├── Prove Democracy ↔ ¬Exclusion (formal)
├── Prove Level hierarchy well-foundedness
├── Prove composition underdetermination
└── Prove Intrinsicness consistency with net structure

Phase 3 (Months 4-6): "Bridge hypotheses as derived theorems"
├── Formalize self-thread as modal predicate (persistence + autonomy)
├── Formalize narrative operator as sufficient statistic schema
├── Prove: QI + self-thread → subject selection dissolution
├── Prove: QI + diamond geometry → temporal phenomenology (qualitative)
└── Prove: Intrinsicness → Mary's Room resolution

Phase 4 (Months 6-9): "Connect to Lean formalization"
├── Define extraction function from Lean algebraic models to Coq modal models
├── Prove: any Lean model satisfying HaagKastlerNet is a valid IQT-ML model
├── Verify consistency: postulates encoded in Coq are consistent with
│   theorems proved in Lean
└── Joint verification: algebraic + modal proofs cover all of §1-§4
```

---

## 5. Bridging the Two Approaches

The Lean and Coq formalizations target different aspects of IQT:

```
                    IQT Theory
                        │
           ┌────────────┴────────────┐
           │                         │
    Mathematical Core          Philosophical Architecture
    (Lean 4 / PhysLean)       (Coq / Modal Logic)
           │                         │
    ├── C*-algebras             ├── QI as axiom
    ├── Haag-Kastler net        ├── Intrinsicness Principle
    ├── State restrictions      ├── Democracy ↔ ¬Exclusion
    ├── Constraint Convergence  ├── Level hierarchy
    ├── Unity functional        ├── Perspectival relativity
    ├── Presheaf structure      ├── Consequence derivation
    └── Causal set QFT          └── Modal metatheorems
           │                         │
           └────────────┬────────────┘
                        │
              Extraction Functor
              (Lean model → Coq model)
```

The **extraction functor** is the key bridge: given a concrete algebraic model in Lean (e.g., a free scalar field net on Minkowski space), extract a Coq modal model where each diamond becomes a world and quality becomes the interpreted content. This ensures the modal reasoning about postulates is grounded in the algebraic reality.

---

## 6. Connection to Dable-Heath, Fewster, Rejzner & Woods (PhysRevD 101, 065013)

This paper is directly relevant because it provides the **only existing construction** of pAQFT on causal sets — exactly the mathematical substrate IQT §2.0 requires. Key points for formalization:

1. **Discretized wave operators**: Their construction of retarded/advanced Green functions on causal sets gives computable versions of the causal propagator σ(f,g) that appears in IQT §0.1. Formalizing this in Lean would ground the Weyl algebra on causal sets.

2. **The "preferred past" proposal**: Their new wave operator based on a preferred past is the kind of structure IQT needs for its effective-theory bridge — it provides a natural coarse-graining direction.

3. **Relative Cauchy evolution**: Their framework for how observables respond to changes in the background causal set connects to IQT's covariance axiom (Constraint 3 in §1.1).

4. **SJ state**: The Sorkin-Johnston state provides a distinguished vacuum-like state on causal sets, directly relevant to IQT's vacuum state ω_0 on discrete spacetime.

5. **Interacting models**: Their deformation quantization construction is the first to produce interacting QFT on causal sets — essential for IQT's claim that the formalism extends beyond free fields.

**Formalization priority**: The free-field construction from this paper (discretized wave operator → classical field algebra → deformation quantization → quantum field algebra → SJ state) is a concrete, finite-dimensional target for Lean formalization. It would give IQT its first machine-verified example of a complete quality assignment on a causal set.

---

## 7. Difficulty Assessment and Risk Matrix

| Component | Lean Difficulty | Coq Difficulty | Risk | Mitigation |
|-----------|----------------|----------------|------|------------|
| Constraint Convergence (T10) | Medium | Medium | Low | Well-defined algebraic argument; can start with finite-dim |
| Quality as Presheaf (O2) | Low-Medium | N/A | Low | Mathlib presheaf infra exists |
| Unity Functional Properties | Medium | N/A | Low | Finite-dim version straightforward |
| QI ↔ ¬Exclusion | N/A | Low | Low | Clean modal argument |
| Level Hierarchy | N/A | Low | Low | Definitional |
| Haag-Kastler Net in Lean | Medium-High | N/A | Medium | No prior art; needs careful type design |
| Type III₁ Classification | Very High | N/A | High | Major research-level formalization |
| Reeh-Schlieder | Very High | N/A | High | Needs distributional analysis in Lean |
| Causal Set QFT (Layer 3) | Very High | N/A | High | Active research area; formalizing Dable-Heath et al. |
| Shape→Phenomenology derivation | N/A | Medium-High | Medium | Requires formalizing "algebra richness" |
| Extraction Functor | High | High | High | Novel; connects two proof assistants |

---

## 8. Minimum Viable Formalization (6-month target)

If resources are limited, the highest-impact subset is:

### In Lean:
1. **Define `HaagKastlerNet` structure** (finite-dimensional version)
2. **Formalize Constraints C1-C4** as predicates on nets
3. **Prove Constraint Convergence (T10)** — this is IQT's mathematical backbone
4. **Define Quality functor and prove it's a presheaf** — connects to category theory
5. **Define Unity functional and prove P1-P3** — the composition story

### In Coq:
1. **Define IQT-ML** (modal logic with diamonds-as-worlds)
2. **Encode QI, Democracy, Intrinsicness as axioms**
3. **Prove: QI + Isotony → Perspectival Relativity**
4. **Prove: Democracy ↔ ¬Exclusion**
5. **Prove: QI + Democracy + Correlation → Composition dissolution**

This MVF would establish:
- The constraint argument is machine-verified (Lean)
- The postulate-to-consequence derivations are machine-verified (Coq)
- The presheaf structure is formally established (Lean)
- The IQT vs IIT divergence (exclusion) is formally characterized (Coq)

---

## 9. Open Questions for the Formalization Program

1. **Which Lean version to target?** Lean 4 with Mathlib4 nightly is the clear choice given PhysLean compatibility.

2. **Should the Coq modal logic use deep or shallow embedding?** Deep embedding (formulas as inductive types) enables metatheoretic reasoning; shallow embedding (propositions as Coq Props over a Kripke structure) is simpler for consequence derivation. Recommend: shallow embedding for Phase 1-2, with deep embedding for Phase 3 metatheorems.

3. **Finite-dimensional first?** Yes. IQT's effective neural algebra (§2.6) is explicitly finite-dimensional. Starting there avoids the hardest functional analysis. The constraint argument works in finite dimensions. The toy model (§2.4, three qubits) is an immediate target.

4. **Connection to Kleiner & Tull (2021)?** Their category-theoretic framework for consciousness theories maps naturally onto the presheaf formalization. The quality functor Q : Diamonds^op → C\*Alg is a concrete instance of their general scheme. This could facilitate formal comparison between IQT and IIT within a shared mathematical language.

5. **Can AI assist?** PhysLean's design philosophy explicitly welcomes AI-assisted formalization. Lean 4's tactic mode is well-suited to LLM-guided proof search. The constraint convergence proof sketch in §1.1 is detailed enough to guide automated translation.

---

## 10. References

### Formalization Tools
- [PhysLean: Digitalizing Physics in Lean 4](https://physlean.com/)
- [PhysLean GitHub](https://github.com/HEPLean/PhysLean)
- [Mathlib4 C\*-Algebra Module](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Analysis/CStarAlgebra/Classes.html)
- [Mathlib4 Presheaf Module](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Topology/Sheaves/Presheaf.html)
- [Dedecker & Loreaux — The Continuous Functional Calculus in Lean](https://arxiv.org/abs/2501.15639)
- [Tooby-Smith — A Perspective on Interactive Theorem Provers in Physics](https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202517294)

### Coq Modal Logic
- [Formalization of modal logic S5 in Coq (BSc thesis, Groningen)](https://fse.studenttheses.ub.rug.nl/28482/)
- [Henkin-style Completeness Proof for S5 in Coq](https://philarchive.org/archive/BENAHC-2)
- [Towards a Coq Formalization of Quantified Modal Logic](https://arxiv.org/pdf/2206.03358)

### Physics
- [Dable-Heath, Fewster, Rejzner & Woods — Algebraic Classical and Quantum Field Theory on Causal Sets (PhysRevD 101, 065013)](https://arxiv.org/abs/1908.01973)
- [Fewster & Verch — Algebraic QFT in Curved Spacetimes](https://arxiv.org/abs/1504.00586)
- [Kleiner & Tull — The Mathematical Structure of IIT](https://doi.org/10.3389/fams.2020.602973)

### IQT
- IQT v1.7.0 (this repository: `iqt_v1_7_0.md`)
