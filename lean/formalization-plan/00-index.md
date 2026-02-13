# IQT Lean Formalization Plan — Master Index

**Version:** 1.0
**Date:** February 2026
**Target:** Lean 4.27.0 + Mathlib + PhysLean
**Source Theory:** IQT v1.8.1 (iqt.md)

---

## Overview

This plan breaks the Lean formalization of Intrinsic Quality Theory into **6 phases** and **17 task files**, organized from foundational infrastructure through the core theorem to empirical predictions. Each file contains:

- Goal and scope
- Lean skeleton code with type signatures
- Dependency graph
- Acceptance criteria
- Difficulty notes

## Phase Dependency Graph

```
Phase 01: AQFT Foundations
  01a (Regions) ──┬──→ 01c (Net of Algebras) ──→ 01d (State Presheaf) ──→ 01e (Toy Models)
                  │                                       │
  01b (C*-Alg) ──┘                                        │
                                                          ↓
Phase 02: Constraint Convergence ────────────────────────────
  02a (Assignments) ──→ 02b (Convergence Thms) ──→ 02c (Examples)
                                  │
                                  └──→ 02d (QI Postulate)
                                                          ↓
Phase 03: Composition & Unity ──────────────────────────────
  03a (Extension Sets) ──→ 03b (Unity Functional)
                                  │
  03c (Perspectival Relativity) ←─┘
                                                          ↓
Phase 04: Self-Threads & Narrative ─────────────────────────
  04a (Self-Threads) ──→ 04b (Narrative Operator)
                                  │
  04c (Classic Problems) ←────────┘
                                                          ↓
Phase 05: Effective Theory Bridge ──────────────────────────
  05a (Bridge Structure) ──→ 05b (Metric Signatures)
                                                          ↓
Phase 06: Protocol Predictions ─────────────────────────────
  06a (Protocol 1: Propofol)
  06b (Protocol 2: Overlap)
  06c (Protocol 3: Psychedelic Temporal)
```

## File Listing

### Phase 01 — AQFT Foundations & Infrastructure

| File | Title | Difficulty | Key Deliverable |
|------|-------|------------|-----------------|
| [01a](01a-preorder-poset-of-regions.md) | Preorder / Poset of Regions | Low | `Reg` with `Preorder` + `Directed` |
| [01b](01b-cstar-algebras-and-states.md) | C*-Algebras and States | Medium | `CStarState` + `restrictState` |
| [01c](01c-net-of-algebras.md) | Net of Local Algebras | Medium | `LocalNet` with isotony embeddings |
| [01d](01d-state-presheaf.md) | The State Presheaf | Medium | `StatePresheaf` Omega + `CompatibleFamily` |
| [01e](01e-finite-dimensional-models.md) | Finite-Dimensional Models | Medium | Three-qubit toy model, `DensityMatrix` |

### Phase 02 — Constraint Convergence Theorem

| File | Title | Difficulty | Key Deliverable |
|------|-------|------------|-----------------|
| [02a](02a-intrinsic-nature-assignments.md) | Intrinsic Assignments + Constraints | Medium | `IntrinsicAssignment`, `NoJunk`, C1-C4 |
| [02b](02b-convergence-theorems.md) | Convergence Theorems (Weak + Strong) | **Core** | Propositions 1 and 2 proved |
| [02c](02c-convergence-examples.md) | Convergence on Concrete Examples | Low | Identity, junk, three-qubit instantiations |
| [02d](02d-quality-identity-postulate.md) | Quality Identity Postulate | Low | QI as axiom, scope separation |

### Phase 03 — Composition & Unity Functional

| File | Title | Difficulty | Key Deliverable |
|------|-------|------------|-----------------|
| [03a](03a-composition-and-extension-sets.md) | Composition Problem + Extension Sets | Medium | `ExtensionSet`, non-uniqueness theorem |
| [03b](03b-unity-functional.md) | Unity Functional U | High | `vonNeumannEntropy`, `unity`, P1-P4 |
| [03c](03c-perspectival-relativity.md) | Perspectival Relativity | Low | Democracy of diamonds, `qualityEquiv` |

### Phase 04 — Self-Threads & Narrative Operator

| File | Title | Difficulty | Key Deliverable |
|------|-------|------------|-----------------|
| [04a](04a-self-threads.md) | Self-Threads (Filter 1) | Medium | `SelfThread`, persistence + autonomy |
| [04b](04b-narrative-operator.md) | Narrative Operator (Filter 2) | Medium | `NarrativeOperator`, five-step pipeline |
| [04c](04c-classic-problem-resolutions.md) | Classic Problem Resolutions | Low | Mary's Room, regress, subject selection |

### Phase 05 — Effective Theory Bridge

| File | Title | Difficulty | Key Deliverable |
|------|-------|------------|-----------------|
| [05a](05a-effective-theory-bridge.md) | Effective-Theory Bridge | Medium | `EffectiveBridge`, coarse-graining |
| [05b](05b-empirical-metrics.md) | Empirical Metric Signatures | Medium | P_j, K_jl, R type signatures |

### Phase 06 — Empirical Protocol Predictions

| File | Title | Difficulty | Key Deliverable |
|------|-------|------------|-----------------|
| [06a](06a-protocol1-propofol.md) | Protocol 1: Propofol | Low | Fragmentation predictions + failure condition |
| [06b](06b-protocol2-overlap.md) | Protocol 2: Overlap | Low | Democracy vs exclusion predictions |
| [06c](06c-protocol3-psychedelic-temporal.md) | Protocol 3: Psychedelic Temporal | Low | Peak-shift predictions + failure condition |

## Recommended Execution Order

### Critical Path (Phases 01-02): The Convergence Theorem

This is the minimum viable formalization — proving the central mathematical result:

```
01a → 01b → 01c → 01d → 02a → 02b
```

Estimated scope: ~6 files, ~1000-2000 lines of Lean.

### Extended Path: Add Concrete Models + Composition

```
01e → 02c (instantiate convergence on toy models)
03a → 03b (unity functional, needs von Neumann entropy)
03c (perspectival relativity — lightweight)
```

### Full Path: Complete Theory Architecture

```
04a → 04b → 04c (self-threads + narrative operator)
05a → 05b (effective bridge + metrics)
06a, 06b, 06c (protocol predictions — mostly type-level)
```

## Infrastructure Notes

### Current State

- **Lean version:** 4.27.0
- **Dependencies:** PhysLean (HEPLean), Mathlib v4.27.0
- **Existing code:** `IQT.lean` (root), `IQT/Hello.lean` (smoke test)
- **Existing analysis:** `constraint-convergence.md` (formal rewrite + skeleton)

### Key Mathlib Gaps

1. **CStarState** — not bundled in Mathlib (noted in Appendix B)
2. **Star-algebra categories** — partial support; may need custom `CStarAlgCat`
3. **Von Neumann entropy** — not in Mathlib; needed for Phase 03b
4. **Matrix logarithm / eigendecomposition** — partial support

### Parallel Work Streams

Tasks within a phase can be parallelized where dependencies allow:
- Phase 01: (01a, 01b) in parallel, then (01c, 01d) in parallel, then 01e
- Phase 02: 02a first, then (02b, 02d) in parallel, then 02c
- Phase 03: (03a, 03c) in parallel, then 03b
- Phase 06: (06a, 06b, 06c) all in parallel

## Relation to Existing Files

- `lean/constraint-convergence.md` — Phase 2 rewrite and skeleton. The plan files extend and decompose this into implementation-ready tasks.
- `lean/IQT/Hello.lean` — Phase 01 smoke test (already passing).
- `iqt.md` Section 1.1 — Primary source for Phase 02.
- `iqt.md` Appendix B — Type signatures referenced throughout.
