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
class PersistentDiamondsConfig:
    world_model: WorldModelConfig = field(default_factory=WorldModelConfig)
    narrator: NarratorConfig = field(default_factory=NarratorConfig)
    report_head: ReportHeadConfig = field(default_factory=ReportHeadConfig)
    stage2_weights: Stage2LossWeights = field(default_factory=Stage2LossWeights)
    distillation: DistillationConfig = field(default_factory=DistillationConfig)
    data: DataConfig = field(default_factory=DataConfig)
    train: TrainConfig = field(default_factory=TrainConfig)

    @classmethod
    def from_yaml(cls, path: str | Path) -> "PersistentDiamondsConfig":
        raw = yaml.safe_load(Path(path).read_text())
        return cls(
            world_model=WorldModelConfig(**raw.get("world_model", {})),
            narrator=NarratorConfig(**raw.get("narrator", {})),
            report_head=ReportHeadConfig(**raw.get("report_head", {})),
            stage2_weights=Stage2LossWeights(**raw.get("stage2_weights", {})),
            distillation=DistillationConfig(**raw.get("distillation", {})),
            data=DataConfig(**raw.get("data", {})),
            train=TrainConfig(**raw.get("train", {})),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_yaml(self, path: str | Path) -> None:
        Path(path).write_text(yaml.safe_dump(self.to_dict(), sort_keys=False))
