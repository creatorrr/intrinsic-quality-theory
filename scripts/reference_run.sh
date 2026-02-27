#!/usr/bin/env bash
# reference_run.sh – End-to-end PDV3 training pipeline.
#
# Usage:
#   ./scripts/reference_run.sh [PRESET] [ARTIFACT_DIR]
#
# PRESET      : small | medium | large  (default: small)
# ARTIFACT_DIR: where checkpoints and results go  (default: artifacts/<preset>)
#
# Runs: data → stage1 → stage2 → stage4 → evaluate → protocols 1-3
# (Stage 3 / distillation is skipped by default since it requires a teacher model.)

set -euo pipefail

PRESET="${1:-small}"
ARTIFACT_DIR="${2:-artifacts/${PRESET}}"
CONFIG_PATH="${ARTIFACT_DIR}/pdv3.yaml"

echo "=== PDV3 Reference Run ==="
echo "Preset:     ${PRESET}"
echo "Artifacts:  ${ARTIFACT_DIR}"
echo ""

mkdir -p "${ARTIFACT_DIR}"

echo "--- init-config (${PRESET}) ---"
pdv3 init-config --config-path "${CONFIG_PATH}" --preset "${PRESET}"

echo ""
echo "--- prepare-data ---"
pdv3 prepare-data --config-path "${CONFIG_PATH}"

echo ""
echo "--- train-stage1 ---"
pdv3 train-stage1 --config-path "${CONFIG_PATH}" \
    --checkpoint-path "${ARTIFACT_DIR}/world_stage1.pt"

echo ""
echo "--- train-stage2 ---"
pdv3 train-stage2 --config-path "${CONFIG_PATH}" \
    --world-checkpoint "${ARTIFACT_DIR}/world_stage1.pt" \
    --save-dir "${ARTIFACT_DIR}"

echo ""
echo "--- train-stage4 ---"
pdv3 train-stage4 --config-path "${CONFIG_PATH}" \
    --world-checkpoint "${ARTIFACT_DIR}/world_stage2.pt" \
    --narrator-checkpoint "${ARTIFACT_DIR}/narrator_stage2.pt" \
    --save-dir "${ARTIFACT_DIR}"

echo ""
echo "--- evaluate ---"
pdv3 evaluate --config-path "${CONFIG_PATH}" \
    --world-checkpoint "${ARTIFACT_DIR}/world_stage2.pt" \
    > "${ARTIFACT_DIR}/eval_metrics.json"
echo "Saved: ${ARTIFACT_DIR}/eval_metrics.json"

echo ""
echo "--- protocols ---"
pdv3 protocol1 --config-path "${CONFIG_PATH}" \
    --world-checkpoint "${ARTIFACT_DIR}/world_stage2.pt" \
    --narrator-checkpoint "${ARTIFACT_DIR}/narrator_stage2.pt" \
    --output-path "${ARTIFACT_DIR}/protocol1.json"

pdv3 protocol2 --config-path "${CONFIG_PATH}" \
    --world-checkpoint "${ARTIFACT_DIR}/world_stage2.pt" \
    --narrator-checkpoint "${ARTIFACT_DIR}/narrator_stage2.pt" \
    --output-path "${ARTIFACT_DIR}/protocol2.json"

pdv3 protocol3 --config-path "${CONFIG_PATH}" \
    --world-checkpoint "${ARTIFACT_DIR}/world_stage2.pt" \
    --narrator-checkpoint "${ARTIFACT_DIR}/narrator_stage2.pt" \
    --output-path "${ARTIFACT_DIR}/protocol3.json"

echo ""
echo "=== Reference run complete ==="
echo "Artifacts in: ${ARTIFACT_DIR}"
ls -lh "${ARTIFACT_DIR}"
