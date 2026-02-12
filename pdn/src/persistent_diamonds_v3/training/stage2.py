from __future__ import annotations

from dataclasses import dataclass

import torch
import torch.nn.functional as F
from torch import nn
from torch.utils.data import DataLoader
from tqdm.auto import tqdm

from persistent_diamonds_v3.config import Stage2LossWeights
from persistent_diamonds_v3.models import DiscreteNarrator, ModularSSMWorldModel
from persistent_diamonds_v3.models.control_head import ControlHead


@dataclass(slots=True)
class Stage2Result:
    final_loss: float
    final_rate_bits_per_sec: float
    steps: int


def info_nce_multiscale(states: torch.Tensor, horizons: tuple[int, ...] = (1, 4, 8, 16)) -> torch.Tensor:
    losses: list[torch.Tensor] = []
    temperature = 0.1

    for h in horizons:
        if states.size(1) <= h:
            continue
        anchor = states[:, :-h].reshape(-1, states.size(-1))
        positive = states[:, h:].reshape(-1, states.size(-1))
        negative = positive[torch.randperm(positive.size(0), device=states.device)]

        anchor = F.normalize(anchor, dim=-1)
        positive = F.normalize(positive, dim=-1)
        negative = F.normalize(negative, dim=-1)

        pos_sim = torch.sum(anchor * positive, dim=-1) / temperature
        neg_sim = torch.sum(anchor * negative, dim=-1) / temperature
        logits = torch.stack([pos_sim, neg_sim], dim=-1)
        labels = torch.zeros(logits.size(0), dtype=torch.long, device=states.device)
        losses.append(F.cross_entropy(logits, labels))

    if not losses:
        return states.new_tensor(0.0)
    return torch.stack(losses).mean()


def vicreg_loss(states: torch.Tensor) -> torch.Tensor:
    x = states.reshape(-1, states.size(-1))
    x = x - x.mean(dim=0, keepdim=True)

    std = torch.sqrt(x.var(dim=0) + 1e-4)
    std_loss = torch.mean(F.relu(1.0 - std))

    cov = (x.T @ x) / max(1, x.size(0) - 1)
    off_diag = cov - torch.diag(torch.diag(cov))
    cov_loss = off_diag.pow(2).mean()

    return std_loss + 0.1 * cov_loss


class Stage2ShapingTrainer:
    """Stage 2 structural shaping with robust IQT proxies."""

    def __init__(
        self,
        world_model: ModularSSMWorldModel,
        narrator: DiscreteNarrator,
        *,
        input_dim: int,
        world_step_hz: int,
        stage2_weights: Stage2LossWeights,
        learning_rate: float,
        weight_decay: float,
        device: str,
        control_head: ControlHead | None = None,
        control_weight: float = 0.5,
    ):
        self.device = torch.device(device)
        self.world_model = world_model.to(self.device)
        self.narrator = narrator.to(self.device)
        self.control_head = control_head.to(self.device) if control_head is not None else None
        self.control_weight = control_weight
        self.weights = stage2_weights
        self.narrator_update_stride = max(1, int(round(world_step_hz / max(1, narrator.update_hz))))

        narrator_dim = narrator.codes_per_step * narrator.code_dim
        latent_dim = world_model.latent_dim

        self.task_head = nn.Sequential(
            nn.Linear(narrator_dim + narrator.hidden_dim, narrator.hidden_dim),
            nn.SiLU(),
            nn.Linear(narrator.hidden_dim, 1),
        ).to(self.device)

        self.obs_predictor = nn.Sequential(
            nn.Linear(latent_dim, latent_dim),
            nn.SiLU(),
            nn.Linear(latent_dim, input_dim),
        ).to(self.device)

        self.world_self_predictor = nn.Sequential(
            nn.Linear(latent_dim, latent_dim),
            nn.SiLU(),
            nn.Linear(latent_dim, latent_dim),
        ).to(self.device)

        self.rd_decoder = nn.Sequential(
            nn.Linear(narrator_dim, narrator.hidden_dim),
            nn.SiLU(),
            nn.Linear(narrator.hidden_dim, latent_dim),
        ).to(self.device)

        params = (
            list(self.world_model.parameters())
            + list(self.narrator.parameters())
            + list(self.task_head.parameters())
            + list(self.obs_predictor.parameters())
            + list(self.world_self_predictor.parameters())
            + list(self.rd_decoder.parameters())
        )
        if self.control_head is not None:
            params += list(self.control_head.parameters())

        self.optimizer = torch.optim.AdamW(
            params,
            lr=learning_rate,
            weight_decay=weight_decay,
        )

    def _run_narrator_rollout(self, world_states: torch.Tensor):
        _, steps, _ = world_states.shape
        step_states: list[torch.Tensor] = []
        step_uncertainties: list[torch.Tensor] = []
        update_states: list[torch.Tensor] = []
        update_preds: list[torch.Tensor] = []
        update_codes: list[torch.Tensor] = []
        vq_losses: list[torch.Tensor] = []
        hidden_state: torch.Tensor | None = None
        current_state: torch.Tensor | None = None
        current_uncertainty: torch.Tensor | None = None

        for t in range(steps):
            should_update = t == 0 or (t % self.narrator_update_stride == 0)
            if should_update:
                start = max(0, t + 1 - self.narrator.window_size)
                window = world_states[:, start : t + 1]
                out = self.narrator(window, hidden_state=hidden_state)
                hidden_state = out.hidden_state
                current_state = out.narrator_state
                current_uncertainty = out.uncertainty

                update_states.append(out.narrator_state)
                update_preds.append(out.predicted_next_state)
                update_codes.append(out.code_indices)
                vq_losses.append(out.vq_loss)

            if current_state is None or current_uncertainty is None:
                raise RuntimeError("Narrator rollout expected initialized state.")
            step_states.append(current_state)
            step_uncertainties.append(current_uncertainty)

        narrator_dim = self.narrator.codes_per_step * self.narrator.code_dim
        bsz = world_states.size(0)
        if update_states:
            state_updates = torch.stack(update_states, dim=1)
            pred_updates = torch.stack(update_preds, dim=1)
            code_updates = torch.stack(update_codes, dim=1)
        else:  # pragma: no cover - steps>=1 in practice.
            state_updates = world_states.new_zeros((bsz, 0, narrator_dim))
            pred_updates = world_states.new_zeros((bsz, 0, narrator_dim))
            code_updates = torch.zeros(
                (bsz, 0, self.narrator.codes_per_step),
                device=world_states.device,
                dtype=torch.long,
            )
        vq_mean = torch.stack(vq_losses).mean() if vq_losses else world_states.new_tensor(0.0)

        return {
            "state_per_step": torch.stack(step_states, dim=1),
            "uncertainty_per_step": torch.stack(step_uncertainties, dim=1),
            "state_updates": state_updates,
            "pred_updates": pred_updates,
            "codes": code_updates,
            "vq_loss": vq_mean,
        }

    def _grounded_autonomy_loss(
        self,
        world_states: torch.Tensor,
        external_drive: torch.Tensor,
        task_loss: torch.Tensor,
        task_threshold: float = 0.2,
    ) -> torch.Tensor:
        if task_loss.item() > task_threshold:
            return world_states.new_tensor(0.0)

        internal_var = world_states.var()
        external_var = external_drive.var()
        ratio = internal_var / (internal_var + external_var + 1e-6)
        return -torch.log(ratio + 1e-6)

    def _actual_rate_bits_per_sec(self, code_indices: torch.Tensor) -> float:
        flat = code_indices.detach().reshape(-1)
        hist = torch.bincount(flat, minlength=self.narrator.codebook_size).float()
        probs = hist / hist.sum().clamp(min=1.0)
        entropy = -(probs[probs > 0] * torch.log2(probs[probs > 0])).sum()
        bits_per_code = float(entropy.item())
        return bits_per_code * self.narrator.codes_per_step * self.narrator.update_hz

    def train(self, dataset, *, batch_size: int, max_steps: int, persist_state: bool = True) -> Stage2Result:
        if len(dataset) == 0:
            raise ValueError("Stage 2 received an empty dataset.")
        loader = DataLoader(dataset, batch_size=batch_size, shuffle=not persist_state, drop_last=False)
        final_loss = 0.0
        final_rate = 0.0
        steps = 0

        if persist_state:
            self.world_model.reset_persistent_state(batch_size=batch_size, device=self.device)

        progress = tqdm(total=max_steps, desc="stage2-shaping")
        while steps < max_steps:
            for batch in loader:
                if steps >= max_steps:
                    break

                observations = batch["observations"].to(self.device)
                targets = batch["targets"].to(self.device)
                external_drive = batch["external_drive"].to(self.device)
                task_signal = batch["task_signal"].to(self.device)

                world = self.world_model(observations, persist_state=persist_state)
                world_states = world.states

                narrator = self._run_narrator_rollout(world_states)
                narrator_state = narrator["state_per_step"]
                narrator_uncertainty = narrator["uncertainty_per_step"]
                narrator_updates = narrator["state_updates"]
                narrator_pred = narrator["pred_updates"]
                code_indices = narrator["codes"]

                jepa_pred = self.obs_predictor(world_states)
                loss_jepa = F.mse_loss(jepa_pred, targets)

                task_features = torch.cat([narrator_state, narrator_uncertainty], dim=-1)
                task_pred = self.task_head(task_features)
                loss_task = F.mse_loss(task_pred, task_signal)

                loss_cpc = info_nce_multiscale(world_states)
                loss_vicreg = vicreg_loss(world_states)
                loss_auto = self._grounded_autonomy_loss(world_states, external_drive, loss_task)

                rd_pred = self.rd_decoder(narrator_state[:, :-1])
                rd_target = world_states[:, 1:].detach()
                distortion = F.mse_loss(rd_pred, rd_target)

                rate_bits = self._actual_rate_bits_per_sec(code_indices)
                target_rate = self.narrator.bits_per_second
                rate_penalty = torch.tensor(
                    rate_bits / max(1.0, target_rate),
                    device=self.device,
                    dtype=distortion.dtype,
                )
                loss_rd = distortion + 0.01 * rate_penalty + narrator["vq_loss"]

                if narrator_updates.size(1) > 1:
                    loss_sp_n = F.mse_loss(narrator_pred[:, :-1], narrator_updates[:, 1:].detach())
                else:
                    loss_sp_n = world_states.new_tensor(0.0)
                world_sp = self.world_self_predictor(world_states[:, :-1])
                loss_sp_w = F.mse_loss(world_sp, world_states[:, 1:].detach())

                # Control head loss: action-entropy regularised value prediction.
                # The control head receives narrator state ONLY (no-bypass).
                if self.control_head is not None:
                    ctrl = self.control_head(narrator_state)
                    # Value prediction trained against task signal magnitude.
                    loss_ctrl = F.mse_loss(
                        ctrl.value_estimate,
                        task_signal.mean(dim=-1, keepdim=True).expand_as(ctrl.value_estimate),
                    )
                    # Entropy bonus: encourage exploration in action space.
                    action_probs = F.softmax(ctrl.action_logits, dim=-1)
                    action_entropy = -(action_probs * torch.log(action_probs + 1e-8)).sum(dim=-1).mean()
                    loss_ctrl = loss_ctrl - 0.01 * action_entropy
                else:
                    loss_ctrl = world_states.new_tensor(0.0)

                total = (
                    self.weights.jepa * loss_jepa
                    + self.weights.task * loss_task
                    + self.weights.cpc * loss_cpc
                    + self.weights.vicreg * loss_vicreg
                    + self.weights.autonomy * loss_auto
                    + self.weights.rate_distortion * loss_rd
                    + self.weights.selfpred_narrator * loss_sp_n
                    + self.weights.selfpred_world * loss_sp_w
                    + self.control_weight * loss_ctrl
                )

                self.optimizer.zero_grad(set_to_none=True)
                total.backward()
                torch.nn.utils.clip_grad_norm_(self.world_model.parameters(), 1.0)
                torch.nn.utils.clip_grad_norm_(self.narrator.parameters(), 1.0)
                self.optimizer.step()

                final_loss = float(total.item())
                final_rate = float(rate_bits)
                steps += 1

                progress.update(1)
                progress.set_postfix(loss=f"{final_loss:.4f}", rate=f"{final_rate:.1f}bps")

                if steps >= max_steps:
                    break

        progress.close()
        return Stage2Result(final_loss=final_loss, final_rate_bits_per_sec=final_rate, steps=steps)
