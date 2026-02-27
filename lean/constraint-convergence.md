# IQT §1.1 — Constraint Convergence

This document contains:

1. The **original Constraint Convergence sketch** from the formalization roadmap (Phase 1d).
2. A **formal rewrite** in proof-assistant-friendly form that eliminates hidden assumptions.
3. A **Lean-ready skeleton** matching the rewrite.
4. A **change log** explaining what changed and why.

---

## 1. Original Sketch (Phase 1d)

> The crown jewel of Track 1 — formalizing §1.1's proof that any intrinsic-nature
> assignment satisfying Constraints 1–4 is naturally equivalent to D ↦ (A(D), ω_D).

```lean
-- Intrinsic nature assignment
structure IntrinsicNatureAssignment (N : LocalNet R) where
  assign : R → Type*
  -- Constraint 1: Completeness
  complete : ∀ D, ∀ A ∈ N.algebra D,
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

> Proof sketch from the paper: Constraint 1 ⟹ I(D) determines ω_D;
> Constraint 4 ⟹ I(D) depends only on (A(D), ω_D);
> Constraint 2 forces compatibility with restriction;
> Constraint 3 gives equivariance.

---

## 2. Formal Rewrite

### 2.1 The Constraint Argument

IQT's identity thesis is constrained, not stipulated. To make that claim proof-assistant-grade
we separate:

1. A **mathematical convergence theorem** about what any admissible "intrinsic description"
   must reduce to.
2. A **metaphysical identity postulate** that links the converged mathematical object to
   phenomenal quality.

### 2.2 Setup

Let $(\mathsf{Reg}, \le)$ be a directed poset of bounded regions, with $D_1 \le D_2$ read
as "$D_1 \subseteq D_2$".

Let
$$\mathcal{A} : \mathsf{Reg} \to \mathsf{C^*Alg}$$
be a net of unital $C^*$-algebras with **isotony embeddings**
$$\iota_{12} : \mathcal{A}(D_1) \hookrightarrow \mathcal{A}(D_2)
  \quad \text{whenever } D_1 \le D_2,$$
functorial in the sense $\iota_{23}\circ \iota_{12}=\iota_{13}$ and $\iota_{DD}=\mathrm{id}$.

Let $\omega$ be a compatible family of local states $\{\omega_D\}$ on this net:
$$\omega_D : \mathcal{A}(D) \to \mathbb{C}
  \quad\text{is a state, and}\quad
  \omega_{D_1} = \omega_{D_2}\circ \iota_{12}\ \text{for all } D_1 \le D_2.$$

Define the **state presheaf**
$$\Omega : \mathsf{Reg}^{op} \to \mathsf{Type}$$
by
$$\Omega(D) := \mathrm{State}(\mathcal{A}(D)),
  \qquad
  \Omega(\iota_{12})(\rho) := \rho\circ \iota_{12}.$$

Define the **quality object** at $D$ as:
$$Q(D) := (\mathcal{A}(D),\ \omega_D).$$

### 2.3 Intrinsic-Nature Assignments

An intrinsic-nature assignment on the net is:

1. A presheaf $I : \mathsf{Reg}^{op} \to \mathsf{Type}$, and
2. A natural transformation (the **decoding map**)
   $$\delta : I \Rightarrow \Omega.$$

Intuitively:
- Elements of $I(D)$ are candidate "intrinsic nature" descriptors for region $D$.
- $\delta_D(x)$ is the local state on $\mathcal{A}(D)$ operationally implied by descriptor $x$.
- Naturality of $\delta$ encodes compatibility with restriction.

To talk about the *actual* world, pick a **section** $i$ of $I$:
$$i_D \in I(D)\ \text{for each }D,
  \quad \text{such that } I(\iota_{12})(i_{D_2}) = i_{D_1}.$$
Then the actual operational content is $\delta_D(i_D)$.

### 2.4 Constraints 1–4

**C1 (Completeness).** The decoding map lands in local states: for every $D$ and
$x\in I(D)$, $\delta_D(x)\in \Omega(D)$.

**C2 (Isotony).** $I$ is a presheaf and $\delta$ is natural:
$$\delta_{D_1}\!\big(I(\iota_{12})(x)\big)
  \;=\; \delta_{D_2}(x)\circ \iota_{12}.$$

**C3 (Covariance).** Given $G$ acting on regions with net covariance
$\alpha_{g,D} : \mathcal{A}(D) \xrightarrow{\cong} \mathcal{A}(gD)$,
require $I$ and $\delta$ to be $G$-equivariant:
$$\delta_{gD}(g\cdot x)
  \;=\; \delta_D(x)\circ \alpha_{g,D}^{-1}.$$

**C4w (Weak locality).** $I$ is indexed by $D$ and restricts along inclusions
(already built into the presheaf structure).

**C4s (Strong / no-junk extensionality).** Decoding is injective at each region:
$$\forall D,\ \forall x,y\in I(D),\quad
  \delta_D(x)=\delta_D(y)\ \Rightarrow\ x=y.$$

C4s rules out trivial counterexamples like "local state + an irrelevant tag bit".

### 2.5 Weak Convergence (Operational Form)

**Proposition.** Let $(I,\delta)$ satisfy C1–C3 and C4w. Define
$$x \sim_D y \;\;:\Longleftrightarrow\;\; \delta_D(x)=\delta_D(y).$$
Let $\widehat{I}(D) := I(D)/{\sim_D}$ with induced
$\widehat{\delta}_D : \widehat{I}(D)\to \Omega(D)$.

Then:
1. $\widehat{I}$ is a presheaf $\mathsf{Reg}^{op}\to\mathsf{Type}$, and
2. $\widehat{\delta} : \widehat{I} \Rightarrow \Omega$ is a **natural monomorphism**.

*Proof sketch.* $\widehat{\delta}_D$ is injective by construction. Naturality follows
from naturality of $\delta$ and functoriality of restriction. $\square$

**Interpretation.** Without no-junk, any admissible intrinsic descriptor collapses to the
local state up to operational equivalence.

### 2.6 Strong Convergence (Isomorphism Form)

**Proposition.** Assume $(I,\delta)$ satisfies C1–C3 and C4s. Then
$\delta : I \Rightarrow \Omega$ is a natural monomorphism.
If additionally every local state is representable (componentwise surjectivity),
$$\forall D,\ \text{Surj}(\delta_D),$$
then $\delta$ is a **natural isomorphism**:
$$I \;\cong\; \Omega.$$

*Proof.* Injectivity is C4s. Surjectivity gives bijection on each component;
naturality is given. $\square$

**Interpretation.** If intrinsic nature contains exactly the information needed to fix all
internal measurement statistics (no more, no less), then it is equivalent to the local
state assignment.

### 2.7 Actual-World Specialization

**Corollary.** Let $i$ be a section. Then $\delta\circ i$ is a compatible family of states.
If the theory stipulates that decoded content matches the physical state family $\omega$, then:
$$\forall D,\quad \delta_D(i_D)=\omega_D.$$

### 2.8 Quality Identity (Interpretive Postulate)

Everything above is mathematics. IQT's extra step is:

> **Quality Identity (QI).** For each bounded region $D$, phenomenal quality is identified
> with the converged physical object $Q(D)=(\mathcal{A}(D),\omega_D)$.

QI is an axiom connecting a primitive $\mathrm{PhenQual}(D)$ to $Q(D)$.
It is not derivable from C1–C4.

---

## 3. Lean Skeleton

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
  map := fun D₁ D₂ h ρ => ρ.comp (A.map h.unop)
  map_id := by sorry
  map_comp := by sorry }

/-- An intrinsic-nature assignment: a presheaf with a decoding map into Ω. -/
structure IntrinsicAssignment :=
  (I : Regᵒᵖ ⥤ Type)
  (δ : I ⟶ Ω Reg A)

/-- Strong perspectival completeness: δ is componentwise injective. -/
def NoJunk (X : IntrinsicAssignment Reg A) : Prop :=
  ∀ D, Function.Injective (X.δ.app D)

/-- Operational equivalence at each region. -/
def opEq (X : IntrinsicAssignment Reg A) (D : Regᵒᵖ)
    (x y : X.I.obj D) : Prop :=
  X.δ.app D x = X.δ.app D y

-- TODO: Quotient presheaf I_hat
-- TODO: Weak convergence theorem
-- TODO: Strong convergence theorem
```

---

## 4. Change Log

| Original | Rewrite | Why |
|---|---|---|
| `NatEquiv` to `Quality` assumed implicitly | Weak theorem (quotient embeds) + strong theorem (iso under NoJunk + surjectivity) | Original hid a "no junk" assumption; now explicit |
| Opaque predicates (`determines_expectation`, `depends_only_on`) | Decoding map into states + naturality | Directly expressible in Lean; no interpretive ambiguity |
| Covariance stated informally | Explicit pullback-of-states equation | Checkable by the proof assistant |
| Mathematics and metaphysics interleaved | QI is a separate postulate | Essential for proof-assistant sanity and intellectual clarity |

---

### Citation

> We model candidate intrinsic-nature assignments as presheaves of descriptors equipped with
> a natural decoding map into the presheaf of local states. Under restriction-compatibility
> and covariance, any such assignment collapses to the decoded local state up to operational
> equivalence; with an explicit no-junk axiom, the assignment is naturally isomorphic to the
> state presheaf.
