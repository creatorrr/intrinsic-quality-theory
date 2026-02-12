# Phase 4: Embodied Grounding

## Goal
Implement the optional embodied stage to enforce grounded autonomy through closed-loop action consequences.

## Tasks
1. Add Stage 4 training loop for environment interaction.
2. Integrate at least one simple environment (gridworld/minigrid-style) and define observation/action adapters.
3. Train with narrator-mediated control and collect grounded-autonomy metrics under real action loops.
4. Add CLI command for Stage 4 training/evaluation and artifact export.

## Files To Touch
- `pdn/src/persistent_diamonds_v3/training/stage4.py` (new)
- `pdn/src/persistent_diamonds_v3/training/__init__.py`
- `pdn/src/persistent_diamonds_v3/data/env/` (new env adapters)
- `pdn/src/persistent_diamonds_v3/cli.py`
- `pdn/tests/` (stage4 smoke/integration tests)

## Exit Criteria
- Stage 4 runs end-to-end on at least one embodied environment.
- Metrics show grounded-autonomy behavior under closed-loop interactions.
- Training and eval artifacts are reproducible.
