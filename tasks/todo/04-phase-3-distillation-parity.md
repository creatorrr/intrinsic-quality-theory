# Phase 3: Distillation Parity

## Goal
Bring Stage 3 closer to spec by adding intermediate-state alignment and improving distillation data throughput.

## Tasks
1. Add optional intermediate-state alignment loss (teacher-to-student projected hidden states).
2. Add cached narrator code-sequence dataset path so codes are not recomputed per item during training.
3. Add config toggles and weights for new distillation terms.
4. Add tests for shape correctness and deterministic cache reuse behavior.

## Files To Touch
- `pdn/src/persistent_diamonds_v3/training/distill.py`
- `pdn/src/persistent_diamonds_v3/config.py`
- `pdn/src/persistent_diamonds_v3/data/distill_cache.py` (new)
- `pdn/src/persistent_diamonds_v3/cli.py`
- `pdn/tests/` (new distillation/cache tests)

## Exit Criteria
- Distillation supports KL + CE + optional hidden alignment.
- Cached code paths are available and verifiably reused.
- Stage 3 runtime is improved on repeated runs.
