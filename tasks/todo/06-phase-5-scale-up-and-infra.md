# Phase 5: Scale-Up and Infra

## Goal
Add configuration presets and training infrastructure to reach doc-scale experiments and produce reproducible protocol artifacts.

## Tasks
1. Add size presets (`small/medium/large`) and align parameter ranges to doc reference.
2. Add training infra switches:
   - bf16 support,
   - gradient accumulation,
   - activation checkpointing,
   - optional `accelerate` integration.
3. Add benchmark scripts:
   - reference run scripts,
   - protocol runs across checkpoints,
   - artifact schema validation.
4. Document exact commands and expected output structure.

## Files To Touch
- `pdn/src/persistent_diamonds_v3/config.py`
- `pdn/src/persistent_diamonds_v3/training/*`
- `pdn/src/persistent_diamonds_v3/cli.py`
- `pdn/pyproject.toml` (optional deps, tooling)
- `scripts/` (new)
- `docs/` (new reference run docs)

## Exit Criteria
- Presets exist and produce expected model sizes.
- Training can scale beyond toy runs without code changes.
- Benchmarks and protocol artifacts are consistently generated and validated.
