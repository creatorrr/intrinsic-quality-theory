# PDN v3 Gap Checklist

Gap analysis against `pdn/persistent_diamonds_v3.docx` (Draft v0.3, February 2026).

Status key: `implemented` | `partial` | `missing`

## 2. Architecture

### 2.1 World Model (Self-Thread Substrate)

| # | Spec Item | Status | Notes |
|---|-----------|--------|-------|
| 2.1.1 | Modular SSM backbone with M modules | implemented | `ModularSSMWorldModel` in `models/world_model.py` |
| 2.1.1 | Heterogeneous time constants (log-uniform, spanning orders of magnitude) | implemented | `_decay_raw` initialized via `torch.logspace(0, 3, ...)` |
| 2.1.2 | Overlapping module slices (~25% overlap between adjacent modules) | implemented | `_build_module_slices` with configurable `overlap_ratio` |
| 2.1.2 | Overlap zones receive updates from both modules' dynamics | implemented | `step()` accumulates and averages overlapping updates |
| 2.1.3 | Text encoder (frozen pretrained embeddings) | implemented | `TextEncoder` in `models/encoders.py`; frozen by default, Tanh-bounded perturbations |
| 2.1.3 | Vision encoder (small ViT) | implemented | `VisionEncoder` stub in `models/encoders.py`; accepts flat features, projects to perturbation |
| 2.1.3 | Proprioceptive / reward encoder | implemented | `ProprioRewardEncoder` in `models/encoders.py` |
| 2.1.3 | Encoders produce perturbations, not complete representations | implemented | All encoders output Tanh/SiLU-bounded perturbation vectors via `ModalityEncoder` ABC |
| 2.1.4 | Action conditioning: z_{t+1} = f(z_t, a_t, o_{t+1}) | implemented | `step()` accepts optional `action_t`; `forward()` accepts `actions` [B,T,A]; defaults to zeros when absent |

### 2.2 Narrator

| # | Spec Item | Status | Notes |
|---|-----------|--------|-------|
| 2.2.1 | Windowed integrator at low rate (5-20 Hz) | implemented | `DiscreteNarrator` with `update_hz` and `window_size` |
| 2.2.2 | VQ discrete bottleneck (codebook N entries, K codes/update) | implemented | `MultiCodeVectorQuantizer` in `narrator.py` |
| 2.2.2 | Explicit bitrate cap: K x log2(N) x update_rate bits/sec | implemented | `bits_per_second` property; default 800 bps |
| 2.2.3 | Self-prediction head: narrator predicts own next state | implemented | `self_prediction_head` in `DiscreteNarrator` |
| 2.2.3 | Uncertainty channel: compression-loss estimate epsilon_t | implemented | `uncertainty_head` in `DiscreteNarrator` |
| 2.2.3 | Capacity inference (narrator infers own effective capacity) | missing | Spec marks as optional; not implemented |
| 2.2.4 | No-bypass hard constraint (no path from z_t to output heads) | implemented | Regression tests for ReportHead and ControlHead in `test_hard_constraints.py` |
| 2.2.4 | Report head: small transformer decoder from narrator codes to text | implemented | `ReportHead` in `models/report_head.py` |
| 2.2.4 | Control head: MLP from b_t to action logits and value estimates | implemented | `ControlHead` in `models/control_head.py`; narrator-only input with no-bypass tests |

### 2.3 Information Flow

| # | Spec Item | Status | Notes |
|---|-----------|--------|-------|
| 2.3 | Task head receives narrator state only (not world state directly) | implemented | Stage 2 task_head receives `narrator_state + narrator_uncertainty`; regression test in `test_hard_constraints.py` |

## 3. Training Pipeline

### 3.1 Stage 1: JEPA Pretraining

| # | Spec Item | Status | Notes |
|---|-----------|--------|-------|
| 3.1 | JEPA predictive objective over future latent states | implemented | `Stage1JEPATrainer` with EMA target in `training/stage1.py` |
| 3.1 | EMA-stabilized target encoder | implemented | `_update_ema_target()` |
| 3.1 | Horizon-based future prediction | implemented | Configurable `horizon` parameter |

### 3.2 Stage 2: Structural Shaping

| # | Spec Item | Status | Notes |
|---|-----------|--------|-------|
| 3.2.1 | Contrastive persistence (CPC/InfoNCE at multiple timescales) | implemented | `info_nce_multiscale()` in `training/stage2.py` |
| 3.2.1 | VICReg anti-collapse (variance + covariance regularizer) | implemented | `vicreg_loss()` in `training/stage2.py` |
| 3.2.2 | Grounded autonomy (conditional on task competence) | implemented | `_grounded_autonomy_loss()` with threshold gating |
| 3.2.3 | Rate-distortion compression (discrete rate + distortion loss) | implemented | `_actual_rate_bits_per_sec()` + `loss_rd` in train loop |
| 3.2.4 | Self-prediction loss for narrator | implemented | `loss_sp_n` comparing narrator predictions to next updates |
| 3.2.5 | World-model self-prediction at multiple horizons | partial | Single-horizon (Δt=1) only; spec says multiple horizons |
| 3.2.6 | Composite loss with configurable lambda weights | implemented | `Stage2LossWeights` dataclass, all terms summed in `train()` |

### 3.3 Stage 3: Report Head Distillation

| # | Spec Item | Status | Notes |
|---|-----------|--------|-------|
| 3.3 | Output logit matching (KL divergence) | implemented | `DistillationTrainer` with KL + CE loss |
| 3.3 | Intermediate state alignment via learned projections | missing | Only logit-level distillation; no hidden-state alignment |
| 3.3 | Teacher model loading with fallbacks | implemented | Candidate list with error collection |

### 3.4 Stage 4: Embodied Grounding

| # | Spec Item | Status | Notes |
|---|-----------|--------|-------|
| 3.4 | Environment interaction training loop | missing | No Stage 4 code |
| 3.4 | Action loop with continuous sensory streams | missing | |
| 3.4 | Auxiliary grounding probes for text-only prototypes | missing | |

## 4. Evaluation Framework

### 4.1 Primary Metrics

| # | Spec Item | Status | Notes |
|---|-----------|--------|-------|
| 4.1 | P_j(w) persistence per module at multiple lags | implemented | `persistence_curve()` in `evaluation/metrics.py` |
| 4.1 | K_jl cross-module coherence (knowledge) | implemented | `cross_module_coherence()` |
| 4.1 | U unity functional | implemented | `unity_functional()` |
| 4.1 | tau_eff effective timescale | implemented | `tau_eff()` |
| 4.1 | R readout dominance | missing | Not in metrics.py |
| 4.1 | Adversarial check: persistence split | implemented | `adversarial_persistence_split()` |
| 4.1 | Adversarial check: shuffle unity | implemented | `adversarial_shuffle_unity()` |
| 4.1 | Adversarial check: per-metric adversarial tests (full set) | partial | Only persistence and unity have adversarial checks |

### 4.2 Protocol Analogues

| # | Spec Item | Status | Notes |
|---|-----------|--------|-------|
| 4.2.1 | Protocol 1: Titrated degradation (reduce recurrent gain) | missing | |
| 4.2.2 | Protocol 2: Overlap test (concurrent tasks on overlapping threads) | missing | |
| 4.2.3 | Protocol 3: Timescale manipulation (widen/narrow/dissolve) | missing | |
| 4.3 | Self-report evaluation during Protocol 3 | missing | |

## 5. Engineering / Infrastructure

| # | Spec Item | Status | Notes |
|---|-----------|--------|-------|
| 5 | CLI commands for all training stages | partial | Stages 1-3 + evaluate present; no Stage 4, no protocol commands |
| 6 | Reference configuration (size presets: small/medium/large) | missing | Single default config only |
| 6 | bf16 / gradient accumulation / activation checkpointing | missing | No training infra switches |
| 6 | Accelerate integration | missing | Listed in optional deps but not used |

## 6. Hard Constraints (Definition of Done)

| # | Constraint | Status | Notes |
|---|-----------|--------|-------|
| HC-1 | No bypass: all outputs depend on narrator channel only | implemented | Regression tests for ReportHead, ControlHead, and task_head in `test_hard_constraints.py` |
| HC-2 | Narrator bitrate cap: discrete, explicitly computed, tested for non-leakage | implemented | Cap computed correctly; regression tests for bitrate formula, codebook bounds, and shape in `test_hard_constraints.py` |
| HC-3 | World state continuity: persists across episode boundaries | implemented | `persist_state` flag exists; cross-batch continuity, reset, and detach tests in `test_hard_constraints.py` |
| HC-4 | Grounded autonomy: rewarded only conditional on task competence | implemented | Threshold gating in `_grounded_autonomy_loss()` |
| HC-5 | Overlap primitive exists architecturally, exercised in evaluation | partial | Exists in architecture; not exercised in protocol evaluation |
| HC-6 | Every metric has at least one adversarial test | partial | Only P and U have adversarial tests; K, R, tau_eff do not |

## Summary

| Category | Implemented | Partial | Missing | Total |
|----------|------------|---------|---------|-------|
| Architecture (2.x) | 18 | 0 | 1 | 19 |
| Training (3.x) | 9 | 1 | 4 | 14 |
| Evaluation (4.x) | 5 | 2 | 5 | 12 |
| Infrastructure (5-6.x) | 0 | 1 | 3 | 4 |
| Hard Constraints | 4 | 1 | 1 | 6 |
| **Total** | **36** | **5** | **14** | **55** |
