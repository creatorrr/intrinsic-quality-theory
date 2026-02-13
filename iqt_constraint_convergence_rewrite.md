# IQT §1.1 Constraint Convergence — Original Draft + Formal Rewrite (Lean/Coq-Ready)

**Prepared for Boboo (Diwank) — February 2026**

This file contains:

1. The **original Constraint Convergence material** as it appears in your roadmap draft (Phase 1d).
2. A **full rewrite** of the section into a proof-assistant-friendly form that avoids hidden assumptions.
3. A **Lean-ready skeleton** that matches the rewrite.
4. A concise **change log** explaining what changed and why.

> Note: This document focuses on the **Constraint Convergence / §1.1** component you asked to rewrite. It does **not** rewrite the rest of the roadmap unless you explicitly request that too.

---

## Part I — Original (from your roadmap draft)

### Phase 1d — The Constraint Convergence Proposition (1–2 months)

> This is the crown jewel of Track 1 — formalizing §1.1’s proof that any intrinsic-nature assignment satisfying Constraints 1-4 is naturally equivalent to D ↦ (A(D), ω_D).

```lean
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

> The proof sketch in the paper is clean enough to formalize: Constraint 1 implies I(D) determines ω_D, Constraint 4 implies I(D) depends only on (A(D), ω_D), Constraint 2 forces compatibility with restriction, Constraint 3 gives equivariance.

---

## Part II — Proposed rewrite (fully formalizable, no hidden assumptions)

### 1.1 The Constraint Argument (formal version)

IQT’s identity thesis is meant to be constrained, not stipulated. The right way to make that claim proof-assistant-grade is to separate:

1. a **mathematical convergence theorem** about what any admissible “intrinsic description” must reduce to, and  
2. a **metaphysical identity postulate** that links the converged mathematical object to phenomenal quality.

### Setup

Let \((\mathsf{Reg}, \le)\) be a directed poset of bounded regions, with \(D_1 \le D_2\) read as “\(D_1 \subseteq D_2\)”.

Let
\[
\mathcal{A} : \mathsf{Reg} \to \mathsf{C^*Alg}
\]
be a net of unital \(C^*\)-algebras with **isotony embeddings**
\[
\iota_{12} : \mathcal{A}(D_1) \hookrightarrow \mathcal{A}(D_2)\quad \text{whenever } D_1 \le D_2,
\]
functorial in the sense \(\iota_{23}\circ \iota_{12}=\iota_{13}\) and \(\iota_{DD}=\mathrm{id}\).

Let \(\omega\) be a compatible family of local states \(\{\omega_D\}\) on this net:
\[
\omega_D : \mathcal{A}(D) \to \mathbb{C}
\quad\text{is a state, and}\quad
\omega_{D_1} = \omega_{D_2}\circ \iota_{12}\ \text{for all } D_1 \le D_2.
\]
(Equivalently, \(\omega\) is a state on the quasilocal algebra, but compatibility is the only property needed here.)

Define the **state presheaf**
\[
\Omega : \mathsf{Reg}^{op} \to \mathsf{Type}
\]
by
\[
\Omega(D) := \mathrm{State}(\mathcal{A}(D)),
\qquad
\Omega(\iota_{12})(\rho) := \rho\circ \iota_{12}.
\]

Define the **quality object** at \(D\) as:
\[
Q(D) := (\mathcal{A}(D),\ \omega_D).
\]

---

### Intrinsic-nature assignments as a presheaf with a decoding map

To make “intrinsic nature determines all internal measurement outcomes” precise, treat an intrinsic-nature assignment as a *presheaf of descriptors* equipped with a *decoding* operation into the operationally testable object (a local state).

**Definition (Intrinsic-nature presheaf).**  
An intrinsic-nature assignment on the net is:

1. a presheaf \(I : \mathsf{Reg}^{op} \to \mathsf{Type}\), and  
2. a natural transformation (the **decoding map**)
   \[
   \delta : I \Rightarrow \Omega.
   \]

Intuitively:
- elements of \(I(D)\) are candidate “intrinsic nature” descriptors for region \(D\),
- \(\delta_D(x)\) is the local state on \(\mathcal{A}(D)\) operationally implied by descriptor \(x\),
- naturality of \(\delta\) encodes compatibility with restriction.

To talk about the *actual* world, optionally pick a **section** \(i\) of \(I\):
\[
i_D \in I(D)\ \text{for each }D,\quad \text{such that } I(\iota_{12})(i_{D_2}) = i_{D_1}.
\]
Then the “actual operational content” is \(\delta_D(i_D)\). (In IQT you want \(\delta_D(i_D)=\omega_D\).)

---

### Constraints 1–4 (formalizable statements)

#### Constraint 1 — Completeness (operational determinacy)

- **C1.** The decoding map lands in local states: for every \(D\) and \(x\in I(D)\), \(\delta_D(x)\in \Omega(D)\).

(Operationally, \(\delta_D(x)(A)\) is the expectation implied by \(x\) for observable \(A\in \mathcal{A}(D)\).)

#### Constraint 2 — Isotony (restriction)

- **C2.** \(I\) is a presheaf and \(\delta\) is natural, so restriction commutes with decoding:
  \[
  \delta_{D_1}\!\big(I(\iota_{12})(x)\big) \;=\; \delta_{D_2}(x)\circ \iota_{12}.
  \]

This is the precise, checkable content of “restriction preserves expectations”.

#### Constraint 3 — Covariance (equivariance under symmetries)

Let \(G\) act on regions, and suppose the net is \(G\)-covariant: for each \(g\in G\) and region \(D\),
\[
\alpha_{g,D} : \mathcal{A}(D) \overset{\cong}{\longrightarrow} \mathcal{A}(gD)
\]
natural in \(D\) and compatible with inclusions.

- **C3.** \(I\) is \(G\)-equivariant and \(\delta\) is \(G\)-equivariant:
  \[
  \delta_{gD}(g\cdot x) \;=\; \delta_D(x)\circ \alpha_{g,D}^{-1}.
  \]

#### Constraint 4 — Perspectival completeness (the subtle one)

The informal phrase “\(I(D)\) depends only on \((\mathcal{A}(D),\omega_D)\)” is not strong enough to imply an isomorphism theorem unless you prevent **redundant invisible structure**.

So we split it into two versions.

- **C4w (weak/locality).** \(I\) is only indexed by \(D\) and restricts along inclusions.  
  (This is already built into “\(I\) is a presheaf over \(\mathsf{Reg}\)”.)

- **C4s (strong/no-junk extensionality).** Decoding is injective at each region:
  \[
  \forall D,\ \forall x,y\in I(D),\quad \delta_D(x)=\delta_D(y)\ \Rightarrow\ x=y.
  \]

C4s is the *exact* condition that rules out trivial counterexamples like “local state + an irrelevant tag bit”.

---

### Proposition (Constraint Convergence — weak / operational form)

**Proposition (Constraint Convergence, operational form).**  
Let \((I,\delta)\) satisfy C1–C3 and C4w. Define an operational equivalence relation:
\[
x \sim_D y \quad:\Longleftrightarrow\quad \delta_D(x)=\delta_D(y).
\]
Let \(\widehat{I}(D) := I(D)/{\sim_D}\) and let \(\widehat{\delta}_D : \widehat{I}(D)\to \Omega(D)\) be induced by \(\delta_D\).

Then:

1. \(\widehat{I}\) is a presheaf \(\mathsf{Reg}^{op}\to\mathsf{Type}\), and  
2. \(\widehat{\delta} : \widehat{I} \Rightarrow \Omega\) is a **natural monomorphism** (injective componentwise).

*Proof sketch.* By definition, \(\widehat{\delta}_D\) is injective. Naturality follows from naturality of \(\delta\) and functoriality of restriction. \(\square\)

**Interpretation.** Without “no-junk,” the provable content is: any admissible intrinsic descriptor collapses to the local state **up to operational equivalence**.

---

### Proposition (Constraint Convergence — strong / isomorphism form)

**Proposition (Constraint Convergence, isomorphism form).**  
Assume \((I,\delta)\) satisfies C1–C3 and the strong axiom C4s. Then \(\delta : I \Rightarrow \Omega\) is a **natural monomorphism**. If additionally every local state is representable (componentwise surjectivity),
\[
\forall D,\ \text{Surj}(\delta_D),
\]
then \(\delta\) is a natural isomorphism:
\[
I \;\cong\; \Omega.
\]

*Proof.* Injectivity is C4s. Surjectivity gives bijection on each component; naturality is given. \(\square\)

**Interpretation.** If intrinsic nature contains **exactly** the information needed to fix all internal measurement statistics (no more and no less), then it is equivalent to the local state assignment.

---

### Corollary (actual-world specialization)

Let \(i\) be a section (an “actual intrinsic nature” assignment). Then \(\delta\circ i\) is a compatible family of states on the net. If the theory stipulates that the decoded operational content matches the physical state family \(\omega\), then:
\[
\forall D,\quad \delta_D(i_D)=\omega_D.
\]

---

### Remark (interpretive postulate: QI)

Everything above is mathematical. It does **not** say anything about consciousness.

IQT’s extra step is:

> **Quality Identity (QI).** For each bounded region \(D\), phenomenal quality is identified with the converged physical object \(Q(D)=(\mathcal{A}(D),\omega_D)\) (or equivalently, with \(\omega_D\) as a state on \(\mathcal{A}(D)\), given the net).

Formally, QI is an **axiom/schema** connecting a primitive \(\mathrm{PhenQual}(D)\) to \(Q(D)\). It is not derivable from C1–C4.

---

## Part III — Lean-ready skeleton matching the rewrite

Below is a shape that matches the rewrite: presheaf + decoding natural transformation + optional no-junk + quotient.

```lean
/-- Regions form a preorder (poset if antisymmetry). -/
variable (Reg : Type) [Preorder Reg]

/-- A covariant net of C*-algebras over regions. -/
variable (A : Reg ⥤ CStarAlgCat)

/-- States on a C*-algebra. -/
def State (X : CStarAlgCat) : Type := CStarState X

/-- The contravariant presheaf of states induced by inclusions. -/
def Ω : Regᵒᵖ ⥤ Type :=
{ obj := fun D => State (A.obj (unop D))
  map := fun D₁ D₂ h ρ => ρ.comp (A.map h.unop)  -- restriction
  map_id := by
    -- prove restriction along id is id
    ...
  map_comp := by
    -- prove restriction respects composition
    ... }

/-- An intrinsic-nature assignment is a presheaf with a natural transformation into Ω. -/
structure IntrinsicAssignment :=
  (I : Regᵒᵖ ⥤ Type)
  (δ : I ⟶ Ω Reg A)

/-- Strong perspectival completeness = no-junk: δ is componentwise injective. -/
def NoJunk (X : IntrinsicAssignment Reg A) : Prop :=
  ∀ D, Function.Injective (X.δ.app D)

/-- Operational equivalence relation at each region. -/
def opEq (X : IntrinsicAssignment Reg A) (D : Regᵒᵖ) (x y : X.I.obj D) : Prop :=
  X.δ.app D x = X.δ.app D y

/-- Quotient presheaf by operational equivalence (implementation requires Quot + functoriality proofs). -/
-- def I_hat (X : IntrinsicAssignment Reg A) : Regᵒᵖ ⥤ Type := ...

/-- Weak convergence: quotient embeds naturally into Ω. -/
-- theorem constraint_convergence_weak (X : IntrinsicAssignment Reg A) :
--   ∃ (δ̂ : I_hat X ⟶ Ω Reg A), (∀ D, Function.Injective (δ̂.app D)) := by
--   ...

/-- Strong convergence: if NoJunk and δ is componentwise surjective, δ is a nat iso. -/
-- theorem constraint_convergence_strong (X : IntrinsicAssignment Reg A) :
--   NoJunk Reg A X →
--   (∀ D, Function.Surjective (X.δ.app D)) →
--   Nonempty (X.I ≅ Ω Reg A) := by
--   ...
```

---

## Part IV — Change log (what changed, and why it matters)

### 1) “NatEquiv to Quality” → **universal property / quotient**
Your original theorem sketch implicitly assumed “no junk”: that `assign D` contains *only* the operational content. In general it could contain extra tags and still satisfy the informal constraints.

**Fix:** we provide:
- a **weak theorem** (always true): quotient by operational equivalence embeds in the state presheaf, and
- a **strong theorem**: you only get a natural isomorphism if you explicitly assume **NoJunk** (injective decoding) and usually surjectivity as well.

### 2) Constraints phrased as meta-predicates → **presheaf + naturality**
Instead of opaque predicates like `determines_expectation` and `depends_only_on`, we encode:
- operational determinacy as a decoding map into states,
- isotony as naturality of that decoding under restriction.

This is directly expressible in Lean/Coq and removes interpretive ambiguity.

### 3) Covariance gets the correct “pullback of states” equation
The proper covariance condition for states is:
\[
\omega_{gD} = \omega_D \circ \alpha_{g,D}^{-1}.
\]
This is now explicit, and thus checkable.

### 4) The metaphysics is cleanly separated (QI is a postulate)
The mathematical convergence result doesn’t “prove consciousness.” It proves a uniqueness/definability claim about operational content. QI is then an additional axiom.

This separation is essential for intellectual hygiene *and* for proof-assistant sanity.

---

## Appendix — How to cite this section in your paper

If you want a tight phrasing:

> “We model candidate intrinsic-nature assignments as presheaves of descriptors equipped with a natural decoding map into the presheaf of local states. Under restriction-compatibility and covariance, any such assignment collapses to the decoded local state up to operational equivalence; with an explicit no-junk axiom, the assignment is naturally isomorphic to the state presheaf.”

---

*End of file.*
