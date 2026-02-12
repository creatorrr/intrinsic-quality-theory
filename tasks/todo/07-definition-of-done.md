# Definition of Done

## Hard Constraints
1. No bypass: all task/report/control outputs depend on narrator channel only.
2. Narrator bitrate cap is discrete and explicitly computed; tests cover expected rate and non-leakage.
3. World state continuity persists across episode boundaries; long unbroken runs are supported.
4. Grounded autonomy is rewarded only conditional on maintained task competence.
5. Overlap primitive exists architecturally and is exercised in evaluation/protocols.
6. Every reported metric has at least one adversarial test.

## Protocols
1. Protocol 1 analogue runnable via CLI and emits JSON artifacts.
2. Protocol 2 analogue runnable via CLI and emits JSON artifacts.
3. Protocol 3 analogue runnable via CLI and emits JSON artifacts.

## Metrics
- Bundle includes `P`, `K`, `R`, `U`, `tau_eff` (or clearly documented replacements), plus adversarial checks.

## Training
1. Stage 1, 2, 3 runnable via CLI.
2. Stage 4 (embodied grounding) runnable end-to-end on at least one environment.
3. Baselines/controls can be executed and compared.

## Reproducibility
1. Outputs written to a consistent artifact directory structure.
2. Artifacts include config, git revision, dataset manifest hashes, and metric/protocol results.
3. Tests cover key invariants and at least one smoke run per stage.
