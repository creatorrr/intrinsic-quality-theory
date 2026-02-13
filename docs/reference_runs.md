# PDV3 Reference Runs

## Size Presets

PDV3 ships three configuration presets aligned to the doc specification:

| Parameter | Small | Medium | Large (default) |
|---|---|---|---|
| `world_model.latent_dim` | 256 | 1024 | 4096 |
| `world_model.module_count` | 4 | 6 | 6 |
| `world_model.hidden_dim` | 128 | 512 | 2048 |
| `world_model.input_dim` | 64 | 128 | 256 |
| `narrator.hidden_dim` | 128 | 256 | 512 |
| `narrator.codebook_size` | 256 | 512 | 1024 |
| `narrator.codes_per_step` | 4 | 8 | 8 |
| `narrator.code_dim` | 32 | 32 | 64 |
| `report_head.model_dim` | 128 | 256 | 512 |
| `report_head.layer_count` | 2 | 4 | 6 |
| `data.default_num_sequences` | 128 | 256 | 512 |
| `train.max_steps` | 1000 | 5000 | 10000 |

Generate a preset config:

```bash
pdv3 init-config --preset small
pdv3 init-config --preset medium --config-path pdv3-medium.yaml
```

## Training Infrastructure Flags

All `train-*` commands accept these optional flags:

| Flag | Description |
|---|---|
| `--preset NAME` | Use a named size preset (overrides config file) |
| `--bf16` | Enable bfloat16 mixed-precision training |
| `--grad-accum N` | Accumulate gradients over N micro-batches |
| `--activation-ckpt` | Enable activation checkpointing (trade compute for memory) |
| `--use-accelerate` | Use HuggingFace Accelerate for distributed training |

These flags override the corresponding `infra:` section in the YAML config.

## Full Reference Run

Run the complete pipeline with a single script:

```bash
# Toy run (fastest, for CI / smoke tests)
./scripts/reference_run.sh small artifacts/small

# Development run
./scripts/reference_run.sh medium artifacts/medium

# Doc-scale run
./scripts/reference_run.sh large artifacts/large
```

The script executes: `init-config → prepare-data → stage1 → stage2 → stage4 → evaluate → protocol1/2/3`.

## Protocol Sweep

Run all three protocols across every available checkpoint:

```bash
./scripts/protocol_sweep.sh artifacts/small/pdv3.yaml artifacts/small
```

## Artifact Validation

Validate that a run produced all expected outputs:

```bash
python scripts/validate_artifacts.py artifacts/small
```

## Expected Output Structure

After a complete reference run, the artifact directory contains:

```
artifacts/<preset>/
├── pdv3.yaml                 # Frozen config for reproducibility
├── world_stage1.pt           # Stage 1 JEPA world model checkpoint
├── world_stage2.pt           # Stage 2 shaped world model
├── narrator_stage2.pt        # Stage 2 narrator checkpoint
├── world_stage4.pt           # Stage 4 embodied world model
├── narrator_stage4.pt        # Stage 4 narrator
├── control_stage4.pt         # Stage 4 control head
├── stage4_result.json        # Stage 4 training metrics
├── eval_metrics.json         # IQT bundle metrics (tau_eff, unity, etc.)
├── protocol1.json            # Protocol 1 results (fragmentation)
├── protocol2.json            # Protocol 2 results (overlap / O-information)
├── protocol3.json            # Protocol 3 results (timescale / peak-shift)
└── protocol_sweep/           # (optional) cross-checkpoint protocol results
    ├── stage1_protocol1.json
    ├── stage2_protocol1.json
    ├── ...
    └── stage4_protocol3.json
```

### JSON Schemas

**eval_metrics.json**
```json
{
  "tau_eff": <float>,
  "unity": <float>,
  "readout_dominance": <float>,
  "coherence": <float>,
  "persistence": [
    {"lag": <int>, "temporal_mi": <float>, "effective_dim": <float>, "persistence": <float>}
  ]
}
```

**protocol1.json**
```json
{
  "fragmentation_detected": <bool>,
  "conditions": [{"gain_factor": <float>, "tau_eff": <float>, ...}]
}
```

**protocol2.json**
```json
{
  "dual_high_persistence": <bool>,
  "tripartite_o_information": <float>,
  "perturbation_containment": <float>,
  ...
}
```

**protocol3.json**
```json
{
  "peak_shift_detected": <bool>,
  "conditions": [{"condition": <str>, "peak_lag": <int>, "auc_persistence": <float>}]
}
```

**stage4_result.json**
```json
{
  "final_loss": <float>,
  "mean_episode_reward": <float>,
  "mean_episode_length": <float>,
  "goal_rate": <float>,
  "steps": <int>
}
```
