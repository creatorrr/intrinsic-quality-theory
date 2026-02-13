from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import yaml

DEFAULT_TEACHER_MODEL = "Qwen/Qwen3-8B"
DEFAULT_TEACHER_MODEL_FALLBACKS = ("Qwen/Qwen3-8B", "Qwen/Qwen3-8B-Instruct")


@dataclass(slots=True)
class WorldModelConfig:
    latent_dim: int = 4096
    input_dim: int = 256
    module_count: int = 6
    overlap_ratio: float = 0.25
    hidden_dim: int = 2048
    action_dim: int = 0


@dataclass(slots=True)
class NarratorConfig:
    window_size: int = 10
    update_hz: int = 10
    world_step_hz: int = 100
    hidden_dim: int = 512
    codebook_size: int = 1024
    codes_per_step: int = 8
    code_dim: int = 64


@dataclass(slots=True)
class ControlHeadConfig:
    action_dim: int = 16
    hidden_dim: int = 256


@dataclass(slots=True)
class ReportHeadConfig:
    vocab_size: int = 32000
    model_dim: int = 512
    layer_count: int = 6
    head_count: int = 8
    ff_dim: int = 2048
    dropout: float = 0.1
    max_seq_len: int = 2048


@dataclass(slots=True)
class Stage2LossWeights:
    jepa: float = 1.0
    task: float = 1.0
    cpc: float = 1.0
    vicreg: float = 0.2
    autonomy: float = 0.5
    rate_distortion: float = 1.0
    selfpred_narrator: float = 0.5
    selfpred_world: float = 0.5


@dataclass(slots=True)
class DistillationConfig:
    teacher_model_name: str = DEFAULT_TEACHER_MODEL
    teacher_model_fallbacks: tuple[str, ...] = DEFAULT_TEACHER_MODEL_FALLBACKS
    temperature: float = 2.0
    alpha_kl: float = 0.8
    alpha_ce: float = 0.2
    learning_rate: float = 3e-4
    batch_size: int = 8
    max_steps: int = 1000
    gradient_clip_norm: float = 1.0
    use_flash_attention_if_available: bool = True
    # Intermediate-state hidden alignment
    hidden_alignment: bool = False
    alpha_hidden: float = 0.1
    hidden_projection_dim: int = 256
    # Cached narrator code-sequence path (skip recompute when set)
    code_cache_dir: str = ".cache/pdv3/distill_codes"


@dataclass(slots=True)
class Stage4Config:
    """Embodied grounding (Stage 4) hyperparameters."""

    env_name: str = "gridworld"
    grid_size: int = 8
    max_episode_steps: int = 64
    episodes_per_epoch: int = 32
    gamma: float = 0.99
    gae_lambda: float = 0.95
    entropy_coeff: float = 0.01
    value_coeff: float = 0.5
    grounded_autonomy_coeff: float = 0.5
    narrator_consistency_coeff: float = 0.3
    gradient_clip_norm: float = 1.0


@dataclass(slots=True)
class DataConfig:
    cache_dir: str = ".cache/pdv3/objectives"
    default_num_sequences: int = 512
    default_sequence_length: int = 256
    feature_dim: int = 256


@dataclass(slots=True)
class TrainConfig:
    device: str = "cuda"
    learning_rate: float = 3e-4
    weight_decay: float = 1e-2
    max_steps: int = 10000


@dataclass(slots=True)
class InfraConfig:
    """Training infrastructure switches for scaling beyond toy runs."""

    bf16: bool = False
    gradient_accumulation_steps: int = 1
    activation_checkpointing: bool = False
    use_accelerate: bool = False


PRESET_NAMES = ("small", "medium", "large")


@dataclass(slots=True)
class PersistentDiamondsConfig:
    world_model: WorldModelConfig = field(default_factory=WorldModelConfig)
    narrator: NarratorConfig = field(default_factory=NarratorConfig)
    control_head: ControlHeadConfig = field(default_factory=ControlHeadConfig)
    report_head: ReportHeadConfig = field(default_factory=ReportHeadConfig)
    stage2_weights: Stage2LossWeights = field(default_factory=Stage2LossWeights)
    distillation: DistillationConfig = field(default_factory=DistillationConfig)
    stage4: Stage4Config = field(default_factory=Stage4Config)
    data: DataConfig = field(default_factory=DataConfig)
    train: TrainConfig = field(default_factory=TrainConfig)
    infra: InfraConfig = field(default_factory=InfraConfig)

    @classmethod
    def from_preset(cls, name: str) -> "PersistentDiamondsConfig":
        """Create a configuration from a named preset (small/medium/large)."""
        if name not in PRESET_NAMES:
            raise ValueError(f"Unknown preset {name!r}. Choose from {PRESET_NAMES}.")
        if name == "small":
            return cls(
                world_model=WorldModelConfig(
                    latent_dim=256, input_dim=64, module_count=4,
                    overlap_ratio=0.25, hidden_dim=128,
                ),
                narrator=NarratorConfig(
                    window_size=10, update_hz=10, world_step_hz=100,
                    hidden_dim=128, codebook_size=256, codes_per_step=4, code_dim=32,
                ),
                control_head=ControlHeadConfig(action_dim=16, hidden_dim=64),
                report_head=ReportHeadConfig(
                    vocab_size=32000, model_dim=128, layer_count=2,
                    head_count=4, ff_dim=512, max_seq_len=512,
                ),
                data=DataConfig(
                    default_num_sequences=128, default_sequence_length=64, feature_dim=64,
                ),
                train=TrainConfig(max_steps=1000),
            )
        if name == "medium":
            return cls(
                world_model=WorldModelConfig(
                    latent_dim=1024, input_dim=128, module_count=6,
                    overlap_ratio=0.25, hidden_dim=512,
                ),
                narrator=NarratorConfig(
                    window_size=10, update_hz=10, world_step_hz=100,
                    hidden_dim=256, codebook_size=512, codes_per_step=8, code_dim=32,
                ),
                control_head=ControlHeadConfig(action_dim=16, hidden_dim=128),
                report_head=ReportHeadConfig(
                    vocab_size=32000, model_dim=256, layer_count=4,
                    head_count=4, ff_dim=1024, max_seq_len=1024,
                ),
                data=DataConfig(
                    default_num_sequences=256, default_sequence_length=128, feature_dim=128,
                ),
                train=TrainConfig(max_steps=5000),
            )
        # large: doc-reference defaults
        return cls()

    @classmethod
    def from_yaml(cls, path: str | Path) -> "PersistentDiamondsConfig":
        raw = yaml.safe_load(Path(path).read_text())
        return cls(
            world_model=WorldModelConfig(**raw.get("world_model", {})),
            narrator=NarratorConfig(**raw.get("narrator", {})),
            control_head=ControlHeadConfig(**raw.get("control_head", {})),
            report_head=ReportHeadConfig(**raw.get("report_head", {})),
            stage2_weights=Stage2LossWeights(**raw.get("stage2_weights", {})),
            distillation=DistillationConfig(**raw.get("distillation", {})),
            stage4=Stage4Config(**raw.get("stage4", {})),
            data=DataConfig(**raw.get("data", {})),
            train=TrainConfig(**raw.get("train", {})),
            infra=InfraConfig(**raw.get("infra", {})),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_yaml(self, path: str | Path) -> None:
        Path(path).write_text(yaml.safe_dump(self.to_dict(), sort_keys=False))
