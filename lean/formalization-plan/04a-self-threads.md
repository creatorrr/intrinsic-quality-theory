# Phase 4a: Self-Threads (Filter 1 Experience)

**Phase:** 04 - Self-Threads & Narrative Operator
**Track:** Consciousness Filters
**Depends on:** 01d (state presheaf), 03b (unity functional), 03c (perspectival relativity)
**Unlocks:** 04b (narrative operator), 05b (metric formalization)

---

## Goal

Formalize self-threads from Section 4.4: directed families of overlapping diamonds whose qualities persist over time and are causally semi-autonomous. Self-threads are the Filter 1 criterion for *experience* (as distinguished from mere quality at Filter 0).

## What to Formalize

### 1. Temporal Sequences of Diamonds

A self-thread is indexed by a time parameter. Each element is a region (effective diamond), and successive regions overlap:

```lean
/-- A temporal sequence of regions: a family of diamonds indexed by time steps. -/
structure TemporalChain (Reg : Type) [Preorder Reg] where
  -- Time steps (e.g., ℕ or a discrete ordered set)
  time : Type
  [time_order : LinearOrder time]
  -- A diamond at each time step
  diamond : time → Reg
```

### 2. Persistence Condition

The quality-stream maintains coherence across successive temporal slices. In the paper, this means the states at successive times are "close" (high temporal mutual information):

```lean
/-- Persistence: a measure of how well quality is maintained across time steps.
    In finite dimensions, this is related to the fidelity or mutual information
    between successive states. -/
class Persistent (N : LocalNet Reg) (ω : CompatibleFamily N)
    (chain : TemporalChain Reg) where
  -- Temporal coherence: quality at time t constrains quality at time t+1
  -- (The precise metric is defined in Phase 05b; here we state the structure.)
  persistence : chain.time → ℝ
  -- Persistence stays above a threshold for a sustained period
  sustained : ∀ t, persistence t > persistence_threshold
```

### 3. Causal Semi-Autonomy (Markov Blanket Analogue)

The interior's future is approximately independent of the exterior, conditioned on its boundary:

```lean
/-- Causal semi-autonomy: the self-thread's future depends primarily on its own past,
    not on external factors. This is the formal analogue of a Markov blanket. -/
class CausallySemiAutonomous (N : LocalNet Reg) (ω : CompatibleFamily N)
    (chain : TemporalChain Reg) where
  -- The conditional mutual information between interior future and exterior,
  -- given the boundary, is below a threshold.
  autonomy : chain.time → ℝ
  semi_autonomous : ∀ t, autonomy t > autonomy_threshold
```

### 4. Self-Thread Definition

```lean
/-- A self-thread: a temporal chain of diamonds that is both persistent and
    causally semi-autonomous. This is Filter 1 (Experience). -/
structure SelfThread (Reg : Type) [Preorder Reg] (N : LocalNet Reg)
    (ω : CompatibleFamily N) extends TemporalChain Reg where
  persistent : Persistent N ω toTemporalChain
  autonomous : CausallySemiAutonomous N ω toTemporalChain
```

### 5. Effective Temporal Depth

The self-thread's integration window determines the "specious present":

```lean
/-- The effective temporal depth of a self-thread: the timescale over which
    persistence is maintained. This determines the specious-present duration. -/
noncomputable def temporalDepth (st : SelfThread Reg N ω) : ℝ :=
  -- The longest timescale w at which persistence P(w) remains above threshold.
  sorry
```

### 6. Three-Filter Hierarchy

```lean
/-- Filter 0: Quality. Every region has it. Universal. -/
-- (This is Phase 03c: quality_universal.)

/-- Filter 1: Experience. Requires a self-thread (persistence + autonomy). -/
def hasExperience (N : LocalNet Reg) (ω : CompatibleFamily N)
    (chain : TemporalChain Reg) : Prop :=
  ∃ st : SelfThread Reg N ω, st.toTemporalChain = chain

/-- Filter 2: Report. Requires a narrative operator with readout dominance.
    (Defined in Phase 04b.) -/
```

### 7. Overlap of Self-Threads

```lean
/-- Two self-threads can overlap in space while being semi-autonomous.
    This is the democracy of diamonds at Filter 1.
    (Protocol 2 tests this prediction.) -/
def overlapping (st₁ st₂ : SelfThread Reg N ω) : Prop :=
  ∃ t₁ t₂, st₁.diamond t₁ = st₂.diamond t₂ ∨
    st₁.diamond t₁ ≤ st₂.diamond t₂ ∨
    st₂.diamond t₂ ≤ st₁.diamond t₁

/-- Overlapping self-threads can coexist. No exclusion postulate. -/
-- (This is a property of the definition: nothing prevents two self-threads
--  from overlapping.)
```

## Acceptance Criteria

- [ ] `TemporalChain` structure compiles
- [ ] `Persistent` and `CausallySemiAutonomous` typeclasses compile
- [ ] `SelfThread` structure compiles
- [ ] `temporalDepth` is defined (even if noncomputable/sorry)
- [ ] `hasExperience` predicate at Filter 1 is defined
- [ ] Overlap of self-threads is definable

## Notes

- The paper says (Section 4.4): "A self-thread is a directed family whose qualities maintain coherence across successive temporal slices: sustained across timescales much longer than the individual diamond's duration."
- The precise metrics (TMI, d_eff, P_j) are defined in Phase 05. Here we set up the abstract structure.
- This is a semi-formal layer: the paper acknowledges that the narrative operator (Phase 04b) is "the weakest link" and a theoretical schema rather than a rigorous model.
