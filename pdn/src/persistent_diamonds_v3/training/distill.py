from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset
from tqdm.auto import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer

from persistent_diamonds_v3.config import DistillationConfig
from persistent_diamonds_v3.models import DiscreteNarrator, ModularSSMWorldModel, ReportHead


@dataclass(slots=True)
class DistillationResult:
    final_loss: float
    teacher_model_name: str
    steps: int


def build_synthetic_distillation_corpus(
    objective_npz_path: str | Path,
    output_jsonl: str | Path,
    *,
    num_examples: int = 2000,
    seed: int = 17,
) -> Path:
    """Generate a reusable code->text corpus from objective trajectories."""

    payload = np.load(objective_npz_path)
    observations = payload["observations"]
    task_signal = payload["task_signal"]

    rng = np.random.default_rng(seed)
    n = observations.shape[0]
    out_path = Path(output_jsonl)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with out_path.open("w") as f:
        for _ in range(num_examples):
            i = int(rng.integers(0, n))
            seq = observations[i]
            signal = float(task_signal[i].mean())
            mean_abs = float(np.abs(seq).mean())
            volatility = float(np.std(seq[1:] - seq[:-1]))

            text = (
                "Report the current system narrative. "
                f"Mean internal magnitude is {mean_abs:.3f}. "
                f"Dynamic volatility is {volatility:.3f}. "
                f"Grounded task coupling is {signal:.3f}."
            )

            record = {
                "trajectory_index": i,
                "text": text,
            }
            f.write(json.dumps(record) + "\n")

    return out_path


class NarratorTextDataset(Dataset):
    def __init__(
        self,
        corpus_path: str | Path,
        objective_npz_path: str | Path,
        world_model: ModularSSMWorldModel,
        narrator: DiscreteNarrator,
        tokenizer,
        *,
        device: str,
        max_text_length: int = 256,
    ):
        self.records = [json.loads(line) for line in Path(corpus_path).read_text().splitlines() if line.strip()]
        payload = np.load(objective_npz_path)
        self.observations = torch.from_numpy(payload["observations"]).float()

        self.world_model = world_model.to(device).eval()
        self.narrator = narrator.to(device).eval()
        self.tokenizer = tokenizer
        self.max_text_length = max_text_length
        self.device = torch.device(device)

    def __len__(self) -> int:
        return len(self.records)

    @torch.no_grad()
    def _encode_codes(self, trajectory_index: int) -> torch.Tensor:
        obs = self.observations[trajectory_index : trajectory_index + 1].to(self.device)
        world = self.world_model(obs)
        states = world.states

        indices = []
        for t in range(states.size(1)):
            start = max(0, t + 1 - self.narrator.window_size)
            out = self.narrator(states[:, start : t + 1])
            indices.append(out.code_indices)
        code_seq = torch.stack(indices, dim=1).squeeze(0).cpu()
        return code_seq

    def __getitem__(self, idx: int) -> dict[str, torch.Tensor]:
        record = self.records[idx]
        codes = self._encode_codes(int(record["trajectory_index"]))
        tokenized = self.tokenizer(
            record["text"],
            truncation=True,
            max_length=self.max_text_length,
            padding="max_length",
            return_tensors="pt",
        )

        return {
            "code_indices": codes,
            "input_ids": tokenized["input_ids"].squeeze(0),
            "attention_mask": tokenized["attention_mask"].squeeze(0),
        }


class DistillationTrainer:
    """Distill report head from Qwen3-8B teacher (or configured fallback)."""

    def __init__(
        self,
        report_head: ReportHead,
        config: DistillationConfig,
        *,
        device: str,
    ):
        self.device = torch.device(device)
        self.report_head = report_head.to(self.device)
        self.config = config

        self.teacher_model, self.teacher_name = self._load_teacher(config)
        self.teacher_model.to(self.device).eval()

        self.optimizer = torch.optim.AdamW(
            self.report_head.parameters(),
            lr=config.learning_rate,
            weight_decay=1e-2,
        )

    def _load_teacher(self, config: DistillationConfig):
        candidates = [config.teacher_model_name, *config.teacher_model_fallbacks]
        errors: list[str] = []

        for model_name in candidates:
            try:
                kwargs = {}
                if self.device.type == "cuda":
                    kwargs["torch_dtype"] = torch.bfloat16
                    if config.use_flash_attention_if_available:
                        kwargs["attn_implementation"] = "flash_attention_2"
                teacher = AutoModelForCausalLM.from_pretrained(model_name, **kwargs)
                return teacher, model_name
            except Exception as exc:  # pragma: no cover - depends on runtime/model availability.
                errors.append(f"{model_name}: {exc}")

        detail = "\n".join(errors)
        raise RuntimeError(f"Failed to load teacher model candidates.\n{detail}")

    def train(self, dataset: Dataset) -> DistillationResult:
        if len(dataset) == 0:
            raise ValueError("Distillation received an empty dataset.")
        loader = DataLoader(dataset, batch_size=self.config.batch_size, shuffle=True, drop_last=False)
        final_loss = 0.0
        steps = 0

        progress = tqdm(total=self.config.max_steps, desc="stage3-distill")
        while steps < self.config.max_steps:
            for batch in loader:
                if steps >= self.config.max_steps:
                    break

                code_indices = batch["code_indices"].to(self.device)
                input_ids = batch["input_ids"].to(self.device)
                attention_mask = batch["attention_mask"].to(self.device)

                with torch.no_grad():
                    teacher_logits = self.teacher_model(
                        input_ids=input_ids,
                        attention_mask=attention_mask,
                    ).logits

                student_logits = self.report_head(
                    code_indices=code_indices,
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                )

                student_step = student_logits[:, :-1]
                teacher_step = teacher_logits[:, :-1]
                labels = input_ids[:, 1:]

                temp = self.config.temperature
                loss_kl = F.kl_div(
                    F.log_softmax(student_step / temp, dim=-1),
                    F.softmax(teacher_step / temp, dim=-1),
                    reduction="batchmean",
                ) * (temp**2)

                loss_ce = F.cross_entropy(
                    student_step.reshape(-1, student_step.size(-1)),
                    labels.reshape(-1),
                    ignore_index=0,
                )

                loss = self.config.alpha_kl * loss_kl + self.config.alpha_ce * loss_ce

                self.optimizer.zero_grad(set_to_none=True)
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.report_head.parameters(), self.config.gradient_clip_norm)
                self.optimizer.step()

                final_loss = float(loss.item())
                steps += 1
                progress.update(1)
                progress.set_postfix(loss=f"{final_loss:.4f}", teacher=self.teacher_name)

                if steps >= self.config.max_steps:
                    break

        progress.close()
        return DistillationResult(final_loss=final_loss, teacher_model_name=self.teacher_name, steps=steps)


def load_tokenizer(config: DistillationConfig):
    model_name = config.teacher_model_name
    candidates = [model_name, *config.teacher_model_fallbacks]
    errors: list[str] = []
    for name in candidates:
        try:
            tokenizer = AutoTokenizer.from_pretrained(name)
            if tokenizer.pad_token_id is None and tokenizer.eos_token_id is not None:
                tokenizer.pad_token = tokenizer.eos_token
            return tokenizer
        except Exception as exc:  # pragma: no cover - runtime/network dependent.
            errors.append(f"{name}: {exc}")
    raise RuntimeError("Failed to load tokenizer for teacher candidates:\n" + "\n".join(errors))
