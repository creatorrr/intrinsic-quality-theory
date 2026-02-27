#!/usr/bin/env python3
"""validate_artifacts.py – Validate PDV3 training artifact schema.

Usage:
    python scripts/validate_artifacts.py ARTIFACT_DIR

Checks that all expected output files exist and conform to the expected
JSON schema.  Returns exit code 0 on success, 1 on any failure.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# --- Expected artifact manifest ---

CHECKPOINT_FILES = [
    "world_stage1.pt",
    "world_stage2.pt",
    "narrator_stage2.pt",
    "world_stage4.pt",
    "narrator_stage4.pt",
    "control_stage4.pt",
]

JSON_SCHEMAS: dict[str, dict[str, type]] = {
    "eval_metrics.json": {
        "tau_eff": (int, float),
        "unity": (int, float),
        "readout_dominance": (int, float),
        "coherence": (int, float),
        "persistence": list,
    },
    "protocol1.json": {
        "fragmentation_detected": bool,
        "conditions": list,
    },
    "protocol2.json": {
        "dual_high_persistence": bool,
        "tripartite_o_information": (int, float),
        "perturbation_containment": (int, float),
    },
    "protocol3.json": {
        "peak_shift_detected": bool,
        "conditions": list,
    },
    "stage4_result.json": {
        "final_loss": (int, float),
        "mean_episode_reward": (int, float),
        "mean_episode_length": (int, float),
        "goal_rate": (int, float),
        "steps": int,
    },
}


def _check_json(path: Path, schema: dict[str, type]) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text())
    except (json.JSONDecodeError, OSError) as exc:
        return [f"{path.name}: failed to read JSON: {exc}"]

    for key, expected_type in schema.items():
        if key not in data:
            errors.append(f"{path.name}: missing key {key!r}")
            continue
        if not isinstance(data[key], expected_type):
            errors.append(
                f"{path.name}: key {key!r} expected {expected_type}, "
                f"got {type(data[key]).__name__}"
            )
    return errors


def validate(artifact_dir: Path) -> list[str]:
    errors: list[str] = []

    if not artifact_dir.is_dir():
        return [f"Artifact directory does not exist: {artifact_dir}"]

    # Check checkpoint files.
    for name in CHECKPOINT_FILES:
        p = artifact_dir / name
        if not p.exists():
            errors.append(f"Missing checkpoint: {name}")
        elif p.stat().st_size == 0:
            errors.append(f"Empty checkpoint: {name}")

    # Check JSON artifacts.
    for name, schema in JSON_SCHEMAS.items():
        p = artifact_dir / name
        if not p.exists():
            errors.append(f"Missing JSON artifact: {name}")
        else:
            errors.extend(_check_json(p, schema))

    # Config should be present.
    if not (artifact_dir / "pdv3.yaml").exists():
        errors.append("Missing config: pdv3.yaml")

    return errors


def main() -> None:
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} ARTIFACT_DIR", file=sys.stderr)
        sys.exit(2)

    artifact_dir = Path(sys.argv[1])
    errors = validate(artifact_dir)

    if errors:
        print(f"FAIL – {len(errors)} issue(s):")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print(f"OK – all artifacts valid in {artifact_dir}")
        sys.exit(0)


if __name__ == "__main__":
    main()
