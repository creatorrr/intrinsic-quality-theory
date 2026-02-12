# Phase 0: Lock Scope

## Goal
Create an explicit, testable gap checklist against `pdn/persistent_diamonds_v3.docx`, and lock core hard constraints with regression tests.

## Tasks
1. Create `docs/pdv3_gap_checklist.md` with one row per spec item and status (`implemented`, `partial`, `missing`).
2. Add tests for hard constraints:
   - `no bypass` (outputs depend only on narrator channel, not raw world state path).
   - narrator bitrate cap behavior and expected rate math.
   - persistent world state continuity across batches/episodes.
3. Ensure test invocation works without manual env hacks from repo conventions.

## Files To Touch
- `docs/pdv3_gap_checklist.md` (new)
- `pdn/tests/test_models.py`
- `pdn/tests/test_objective_store.py`
- `pdn/pyproject.toml` (if test path/config updates are needed)

## Exit Criteria
- Gap checklist exists and is complete enough to drive implementation tracking.
- Constraint tests are in CI/pytest and passing.
- Team can run tests with a single documented command.
