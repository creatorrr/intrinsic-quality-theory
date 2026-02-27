#!/usr/bin/env bash
# protocol_sweep.sh – Run all three protocols across multiple checkpoints.
#
# Usage:
#   ./scripts/protocol_sweep.sh CONFIG_PATH CHECKPOINT_DIR [OUTPUT_DIR]
#
# Expects checkpoint pairs like:
#   CHECKPOINT_DIR/world_stage1.pt  + CHECKPOINT_DIR/narrator_stage2.pt
#   CHECKPOINT_DIR/world_stage2.pt  + CHECKPOINT_DIR/narrator_stage2.pt
#   CHECKPOINT_DIR/world_stage4.pt  + CHECKPOINT_DIR/narrator_stage4.pt
#
# Each checkpoint pair gets a full protocol1/2/3 run.

set -euo pipefail

CONFIG_PATH="${1:?Usage: protocol_sweep.sh CONFIG_PATH CHECKPOINT_DIR [OUTPUT_DIR]}"
CKPT_DIR="${2:?Usage: protocol_sweep.sh CONFIG_PATH CHECKPOINT_DIR [OUTPUT_DIR]}"
OUT_DIR="${3:-${CKPT_DIR}/protocol_sweep}"

mkdir -p "${OUT_DIR}"

# Pairs: (label, world_ckpt, narrator_ckpt)
declare -a LABELS=()
declare -a WORLD_CKPTS=()
declare -a NARRATOR_CKPTS=()

if [ -f "${CKPT_DIR}/world_stage1.pt" ]; then
    LABELS+=("stage1")
    WORLD_CKPTS+=("${CKPT_DIR}/world_stage1.pt")
    # Stage 1 has no narrator yet; pass empty string
    NARRATOR_CKPTS+=("")
fi

if [ -f "${CKPT_DIR}/world_stage2.pt" ] && [ -f "${CKPT_DIR}/narrator_stage2.pt" ]; then
    LABELS+=("stage2")
    WORLD_CKPTS+=("${CKPT_DIR}/world_stage2.pt")
    NARRATOR_CKPTS+=("${CKPT_DIR}/narrator_stage2.pt")
fi

if [ -f "${CKPT_DIR}/world_stage4.pt" ] && [ -f "${CKPT_DIR}/narrator_stage4.pt" ]; then
    LABELS+=("stage4")
    WORLD_CKPTS+=("${CKPT_DIR}/world_stage4.pt")
    NARRATOR_CKPTS+=("${CKPT_DIR}/narrator_stage4.pt")
fi

if [ ${#LABELS[@]} -eq 0 ]; then
    echo "No checkpoint pairs found in ${CKPT_DIR}" >&2
    exit 1
fi

echo "=== Protocol Sweep ==="
echo "Config:      ${CONFIG_PATH}"
echo "Checkpoints: ${#LABELS[@]} pairs found"
echo ""

for i in "${!LABELS[@]}"; do
    label="${LABELS[$i]}"
    wc="${WORLD_CKPTS[$i]}"
    nc="${NARRATOR_CKPTS[$i]}"

    echo "--- ${label} ---"

    nc_args=()
    if [ -n "${nc}" ]; then
        nc_args=(--narrator-checkpoint "${nc}")
    fi

    for proto in protocol1 protocol2 protocol3; do
        out_file="${OUT_DIR}/${label}_${proto}.json"
        echo "  ${proto} -> ${out_file}"
        pdv3 "${proto}" \
            --config-path "${CONFIG_PATH}" \
            --world-checkpoint "${wc}" \
            "${nc_args[@]}" \
            --output-path "${out_file}" 2>&1 | tail -n 2
    done
    echo ""
done

echo "=== Sweep complete ==="
echo "Results in: ${OUT_DIR}"
ls -lh "${OUT_DIR}"
