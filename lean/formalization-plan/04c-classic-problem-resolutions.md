# Phase 4c: Classic Problem Resolutions

**Phase:** 04 - Self-Threads & Narrative Operator
**Track:** Philosophical Applications (Lightweight)
**Depends on:** 02d (QI), 03c (perspectival relativity), 04a (self-threads), 04b (narrative operator)
**Unlocks:** Nothing (terminal documentation task)

---

## Goal

State (not necessarily prove in full) how the formalized framework resolves classic consciousness problems from Section 4. These are primarily type-level observations showing that the formal machinery makes certain problems dissoluble.

## What to Formalize

### 1. Infinite Regress (Section 4.1)

> "Every observer is a bounded region with quality determined by its own algebra-state pair. The regress terminates at the qualon."

```lean
/-- No infinite regress: quality at D is determined by (A(D), ω_D).
    It does not require an external observer.
    The quality IS the state; no further "observer of the observer" is needed. -/
theorem no_regress (N : LocalNet Reg) (ω : CompatibleFamily N) (D : Reg) :
    -- The quality at D is fully specified by the algebra-state pair.
    -- No reference to any other region or observer is required.
    ∃! q, q = ω.state D := ⟨ω.state D, rfl, fun _ h => h.symm⟩
```

### 2. Mary's Room (Section 4.2)

> "Mary gains a new quality — a new element in her own presheaf of local states — not a new proposition about the world."

```lean
/-- Mary's Room: the gain is instantiation of a new quality, not new information.
    Before: no diamond in Mary's brain has state in equivalence class Q_red.
    After: a new diamond D has quality ω_D in class Q_red.
    The quality equivalence class is a well-defined mathematical object (Phase 03c). -/
-- Formalized as: the range of Mary's quality presheaf expands to include
-- a new isomorphism class of algebra-state pairs.
```

### 3. Subject Selection Dissolution (Section 4.4)

> "All diamonds have quality (Level 0). The interesting question is which diamonds sustain self-threads (Level 1) and which control report (Level 2)."

```lean
/-- The subject selection problem is dissolved by the three-level hierarchy.
    Level 0: Every region has quality (quality_universal).
    Level 1: Self-threads have experience (hasExperience).
    Level 2: Narrative operators have report (hasReport).
    There is no need for a metaphysical "selector" picking "the" subject. -/
-- The hierarchy is: quality_universal → hasExperience → hasReport
-- Each level is strictly narrower: Level 2 ⊂ Level 1 ⊂ Level 0.
```

### 4. Substrate Dependence (Section 4.3)

```lean
/-- Substrate dependence: distinct substrates typically instantiate distinct qualities,
    even under similar functional organization. Two systems have the same quality iff
    their algebra-state pairs are isomorphic (Intrinsicness Principle). -/
-- This follows from qualityEquiv (Phase 03c): quality comparison is via
-- StarAlgIso between the algebras + state matching.
```

### 5. Split-Brain (Box 4.A)

```lean
/-- Post-callosotomy: hemispheres are disjoint (non-overlapping) regions.
    Both can sustain independent self-threads. The left hemisphere's continued
    report of unity is evidence that the narrator's self-model has not been
    updated, not evidence of actual unity. -/
-- Formalized as: two disjoint SelfThreads with independent NarrativeOperators.
-- The left narrator's self-model may contain stale data.
```

## Acceptance Criteria

- [ ] Each resolution is stated as a comment or lightweight theorem
- [ ] The three-level hierarchy (Level 0/1/2) is explicitly documented
- [ ] The resolutions reference the formal structures from earlier phases
- [ ] No new heavy Lean code — this is primarily a documentation/structuring task

## Notes

- These are NOT deep formal proofs. They are observations that the type structure makes certain problems structurally dissoluble.
- The paper says (Section 4): "IQT dissolves the Hard Problem at Level 0 by the identity thesis. The interesting scientific questions live at Levels 1 and 2."
- This phase exists to show that the formalization has explanatory reach beyond the convergence theorem.
