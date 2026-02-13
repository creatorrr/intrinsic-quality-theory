# Phase 4b: Narrative Operator (Filter 2 Report)

**Phase:** 04 - Self-Threads & Narrative Operator
**Track:** Consciousness Filters
**Depends on:** 04a (self-threads)
**Unlocks:** 05b (metric formalization)

---

## Goal

Formalize the narrative operator N from Section 4.5: the Filter 2 structure that bridges self-thread quality to reportable experience. N compresses a quality trajectory into a self-model that controls a readout channel.

**Caveat:** The paper explicitly says N is "the weakest link" and "a schema, not a model." The formalization here captures the type-level structure, not a biophysically realistic implementation.

## What to Formalize

### 1. The Five-Step Pipeline (Section 4.5.1)

The narrative operator is a composition of five standard operations:

```lean
/-- Step 1: Physical state trajectory.
    At each time t, the self-thread's diamond has a full state. -/
def physicalTrajectory (st : SelfThread Reg N ω) :
    st.time → StateSpace N (st.diamond ·) :=
  fun t => ω.state (st.diamond t)

/-- Step 2: Coarse-graining to interface variables.
    Extract sensory, motor, and cross-boundary joint states via partial trace. -/
structure InterfaceVariables where
  sensory : Type
  motor : Type
  cross_boundary : Type

def coarseGrain (fullState : StateSpace N D) : InterfaceVariables := sorry

/-- Step 3: Bayesian filtering to belief state.
    Compress the history of interface variables into a sufficient statistic
    for predicting future sensory input. -/
structure BeliefState (dim : ℕ) where
  state : Fin dim → ℝ  -- low-dimensional representation

def bayesianFilter (history : List InterfaceVariables) : BeliefState dim := sorry

/-- Step 4: Self-model extraction.
    Extract slowly varying features of the belief-state trajectory.
    This is recursive: the self-model influences action, which changes
    sensory input, which updates the belief state. -/
structure SelfModel where
  model : Type
  -- Recursive self-reference
  contains_self : model → Prop

def extractSelfModel (trajectory : List (BeliefState dim)) : SelfModel := sorry

/-- Step 5: Report coupling.
    The self-model drives motor output. Readout dominance measures
    how much the self-model controls the report channel. -/
def reportCoupling (sm : SelfModel) (motor : Type) : ℝ := sorry
```

### 2. The Narrative Operator (Composed)

```lean
/-- The narrative operator N: maps evolving restrictions along a self-thread
    to an internal generative model. N : Quality-trajectory → Self-model. -/
structure NarrativeOperator (Reg : Type) [Preorder Reg] (N : LocalNet Reg)
    (ω : CompatibleFamily N) where
  -- The underlying self-thread
  thread : SelfThread Reg N ω
  -- Dimensionality reduction (coarse-graining + filtering)
  compress : (thread.time → StateSpace N (thread.diamond ·)) → SelfModel
  -- Report coupling strength
  readout_dominance : ℝ
  -- Filter 2 threshold: readout dominance must exceed a threshold
  is_filter2 : readout_dominance > readout_threshold
```

### 3. Readout Dominance

```lean
/-- Readout dominance R: directed information from the self-model to motor output.
    R = DI(self-model → motor).
    Filter 2 (Report) requires R > R_threshold. -/
def readoutDominance (narr : NarrativeOperator Reg N ω) : ℝ :=
  narr.readout_dominance

/-- A self-thread is Filter 2 iff it has a narrative operator with sufficient
    readout dominance. -/
def hasReport (N' : LocalNet Reg) (ω : CompatibleFamily N')
    (chain : TemporalChain Reg) : Prop :=
  ∃ narr : NarrativeOperator Reg N' ω,
    narr.thread.toTemporalChain = chain ∧ narr.is_filter2
```

### 4. Formal Properties (Section 4.5)

```lean
/-- Dimensionality reduction: the self-model has fewer degrees of freedom
    than the raw quality trajectory. -/
-- (Built into the compress function: input is high-dimensional, output is SelfModel.)

/-- Finite-memory updating: the narrative window is nested within the
    self-thread's effective temporal depth. -/
-- The narrator's "specious present" is ≤ the self-thread's temporal depth.

/-- Recursive self-reference: the self-model contains a representation of itself. -/
-- Built into SelfModel.contains_self.
```

### 5. Role Constraint

```lean
/-- N is a Filter 2 (report) construction: it does NOT manufacture Filter 1 experience.
    It compresses, tracks, and routes an already-existing self-thread's quality
    trajectory into a form usable for prediction, control, and report. -/
-- This is a definitional constraint: NarrativeOperator requires a SelfThread
-- as a prerequisite. N cannot exist without an underlying self-thread.
```

## Acceptance Criteria

- [ ] `NarrativeOperator` structure compiles
- [ ] Five-step pipeline types are sketched (even with `sorry`)
- [ ] `readoutDominance` and `hasReport` compile
- [ ] The Filter 0/1/2 hierarchy is complete: `quality_universal` (Phase 03c), `hasExperience` (Phase 04a), `hasReport` (Phase 04b)
- [ ] Role constraint documented: N requires pre-existing self-thread

## Notes

- The paper says (Section 4.5): "N is the weakest link. We state this plainly."
- The toy pipeline (Section 4.5.1) uses 6 qubits: sensory (2), internal (2), motor (2). This is "not a brain, but a proof that the pipeline has definite mathematical structure."
- The formalization here captures the TYPE STRUCTURE, not a computational implementation. A biophysically realistic N is an open problem (Section 7).
- For a full formalization, the five pipeline steps would need to be connected end-to-end. For now, stating their types and the overall NarrativeOperator structure suffices.
