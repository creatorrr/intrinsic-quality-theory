# Phase 2: Evaluation and Protocol Analogues

## Goal
Close evaluation gaps by adding missing metrics and protocol runners with adversarial checks for each metric in use.

## Tasks
1. Extend metric bundle to include readout dominance `R` and keep `P/K/U/tau_eff`.
2. Implement protocol runners:
   - Protocol 1 analogue: titrated degradation.
   - Protocol 2 analogue: overlap test, perturbation propagation, tripartite O-information.
   - Protocol 3 analogue: timescale manipulation and peak-shift analysis.
3. Add adversarial checks for every reported metric, including explicit pass/fail thresholds in outputs.
4. Add CLI commands to run each protocol and emit reproducible JSON artifacts.

## Files To Touch
- `pdn/src/persistent_diamonds_v3/evaluation/metrics.py`
- `pdn/src/persistent_diamonds_v3/evaluation/protocols.py` (new)
- `pdn/src/persistent_diamonds_v3/evaluation/__init__.py`
- `pdn/src/persistent_diamonds_v3/cli.py`
- `pdn/tests/` (new protocol/metric tests)

## Exit Criteria
- CLI can run protocol analogues end-to-end.
- Output JSON includes metric values and adversarial check outcomes.
- Metrics are validated by tests on synthetic/known-control cases.
