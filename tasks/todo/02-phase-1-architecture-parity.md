# Phase 1: Architecture Parity

## Goal
Match the architecture-level gaps called out in the doc: modality encoders, action conditioning, and an explicit control head wired through narrator-only outputs.

## Tasks
1. Add encoder interfaces and first implementations:
   - text encoder wrapper,
   - vision encoder stub,
   - proprio/reward encoder stub.
2. Add action conditioning to world-model transition interfaces and training data flow.
3. Add explicit `ControlHead` module for action logits/value estimates from narrator outputs only.
4. Update Stage 2 training to use `ControlHead` and keep no-bypass guarantees.

## Files To Touch
- `pdn/src/persistent_diamonds_v3/models/world_model.py`
- `pdn/src/persistent_diamonds_v3/models/control_head.py` (new)
- `pdn/src/persistent_diamonds_v3/models/__init__.py`
- `pdn/src/persistent_diamonds_v3/training/stage2.py`
- `pdn/src/persistent_diamonds_v3/cli.py`
- `pdn/src/persistent_diamonds_v3/data/objectives.py` (if action fields are added)
- `pdn/tests/test_models.py`

## Exit Criteria
- Action-conditioned world model path exists and is tested.
- Control head exists and receives narrator-side inputs only.
- No-bypass invariants remain true under tests.
