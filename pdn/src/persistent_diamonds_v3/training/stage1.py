from __future__ import annotations

import copy
from dataclasses import dataclass

import torch
import torch.nn.functional as F
from torch import nn
from torch.utils.data import DataLoader
from tqdm.auto import tqdm

from persistent_diamonds_v3.models import ModularSSMWorldModel


@dataclass(slots=True)
class Stage1Result:
    final_loss: float
    steps: int


class Stage1JEPATrainer:
    """Stage 1 JEPA-style predictive training for the persistent world model."""

    def __init__(
        self,
        world_model: ModularSSMWorldModel,
        *,
        latent_dim: int,
        learning_rate: float,
        weight_decay: float,
        device: str,
        ema_decay: float = 0.99,
    ):
        self.world_model = world_model.to(device)
        self.device = torch.device(device)
        self.ema_decay = ema_decay

        self.target_world_model = copy.deepcopy(world_model).to(device)
        self.target_world_model.eval()
        for param in self.target_world_model.parameters():
            param.requires_grad_(False)

        self.predictor = nn.Sequential(
            nn.Linear(latent_dim, latent_dim),
            nn.SiLU(),
            nn.Linear(latent_dim, latent_dim),
        ).to(self.device)

        self.optimizer = torch.optim.AdamW(
            list(self.world_model.parameters()) + list(self.predictor.parameters()),
            lr=learning_rate,
            weight_decay=weight_decay,
        )

    def _update_ema_target(self) -> None:
        with torch.no_grad():
            for target_param, online_param in zip(
                self.target_world_model.parameters(),
                self.world_model.parameters(),
                strict=True,
            ):
                target_param.data.mul_(self.ema_decay).add_(online_param.data, alpha=1.0 - self.ema_decay)

    def train(
        self,
        dataset,
        *,
        batch_size: int,
        max_steps: int,
        horizon: int = 4,
        persist_state: bool = True,
    ) -> Stage1Result:
        if len(dataset) == 0:
            raise ValueError("Stage 1 received an empty dataset.")
        loader = DataLoader(dataset, batch_size=batch_size, shuffle=not persist_state, drop_last=False)
        steps = 0
        final_loss = 0.0

        if persist_state:
            self.world_model.reset_persistent_state(batch_size=batch_size, device=self.device)
            self.target_world_model.reset_persistent_state(batch_size=batch_size, device=self.device)

        progress = tqdm(total=max_steps, desc="stage1-jepa")
        while steps < max_steps:
            for batch in loader:
                if steps >= max_steps:
                    break

                observations = batch["observations"].to(self.device)
                online_outputs = self.world_model(observations, persist_state=persist_state)
                online_states = online_outputs.states
                with torch.no_grad():
                    target_outputs = self.target_world_model(observations, persist_state=persist_state)
                target_states = target_outputs.states

                if online_states.size(1) <= horizon:
                    continue

                pred = self.predictor(online_states[:, :-horizon])
                target = target_states[:, horizon:].detach()

                loss = F.mse_loss(pred, target)
                self.optimizer.zero_grad(set_to_none=True)
                loss.backward()
                self.optimizer.step()
                self._update_ema_target()

                final_loss = float(loss.item())
                steps += 1
                progress.update(1)
                progress.set_postfix(loss=f"{final_loss:.4f}")

                if steps >= max_steps:
                    break

        progress.close()
        return Stage1Result(final_loss=final_loss, steps=steps)
