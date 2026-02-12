from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import torch
from torch import nn


@dataclass(slots=True)
class WorldModelOutput:
    states: torch.Tensor
    final_state: torch.Tensor


class ModuleDynamics(nn.Module):
    """Single module dynamics for an overlapping state slice."""

    def __init__(self, input_dim: int, state_dim: int, hidden_dim: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim + state_dim, hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, state_dim),
        )

    def forward(self, input_t: torch.Tensor, state_t: torch.Tensor) -> torch.Tensor:
        return self.net(torch.cat([input_t, state_t], dim=-1))


class ModularSSMWorldModel(nn.Module):
    """Overlapping modular recurrent world model with heterogeneous timescales."""

    def __init__(
        self,
        input_dim: int,
        latent_dim: int,
        module_count: int,
        overlap_ratio: float,
        hidden_dim: int,
    ):
        super().__init__()
        self.input_dim = input_dim
        self.latent_dim = latent_dim
        self.module_count = module_count

        self.module_slices = self._build_module_slices(latent_dim, module_count, overlap_ratio)
        self.modules_dyn = nn.ModuleList(
            [
                ModuleDynamics(
                    input_dim=input_dim,
                    state_dim=end - start,
                    hidden_dim=hidden_dim,
                )
                for (start, end) in self.module_slices
            ]
        )

        # Log-uniform initialization (roughly 1 to 1000-step timescales).
        taus = torch.logspace(0, 3, steps=latent_dim)
        decays = torch.exp(-1.0 / taus).clamp(0.5, 0.999)
        self._decay_raw = nn.Parameter(torch.log(decays / (1.0 - decays)))

        self.register_buffer("_persistent_state", torch.zeros(1, latent_dim), persistent=False)

    @staticmethod
    def _build_module_slices(
        latent_dim: int,
        module_count: int,
        overlap_ratio: float,
    ) -> list[tuple[int, int]]:
        if module_count < 1:
            raise ValueError("module_count must be >= 1")
        base_width = max(8, latent_dim // module_count)
        overlap = int(base_width * overlap_ratio)
        step = max(1, base_width - overlap)

        slices: list[tuple[int, int]] = []
        for idx in range(module_count):
            start = idx * step
            end = start + base_width
            if idx == module_count - 1:
                end = latent_dim
            if end > latent_dim:
                end = latent_dim
                start = max(0, end - base_width)
            slices.append((start, end))

        return slices

    @property
    def decay(self) -> torch.Tensor:
        return torch.sigmoid(self._decay_raw)

    def reset_persistent_state(self, batch_size: int = 1, device: torch.device | None = None) -> None:
        state = torch.zeros(batch_size, self.latent_dim, device=device or self._persistent_state.device)
        self._persistent_state = state

    def step(
        self,
        input_t: torch.Tensor,
        state_t: torch.Tensor,
    ) -> torch.Tensor:
        if input_t.ndim != 2 or state_t.ndim != 2:
            raise ValueError("Expected `input_t` and `state_t` as [B, D] tensors.")

        batch = input_t.size(0)
        updates = torch.zeros(batch, self.latent_dim, device=input_t.device, dtype=input_t.dtype)
        counts = torch.zeros(self.latent_dim, device=input_t.device, dtype=input_t.dtype)

        for (start, end), module in zip(self.module_slices, self.modules_dyn, strict=True):
            local_state = state_t[:, start:end]
            local_update = module(input_t, local_state)
            updates[:, start:end] += local_update
            counts[start:end] += 1.0

        counts = torch.where(counts == 0, torch.ones_like(counts), counts)
        mean_update = updates / counts.unsqueeze(0)

        decay = self.decay.unsqueeze(0).to(dtype=input_t.dtype)
        next_state = decay * state_t + (1.0 - decay) * mean_update
        return next_state

    def forward(
        self,
        inputs: torch.Tensor,
        *,
        initial_state: torch.Tensor | None = None,
        persist_state: bool = False,
    ) -> WorldModelOutput:
        if inputs.ndim != 3:
            raise ValueError("Expected `inputs` as [B, T, D].")
        if inputs.size(-1) != self.input_dim:
            raise ValueError(f"Expected input dim {self.input_dim}, got {inputs.size(-1)}")

        batch, steps, _ = inputs.shape
        if initial_state is None:
            if self._persistent_state.size(0) != batch:
                self.reset_persistent_state(batch_size=batch, device=inputs.device)
            state_t = self._persistent_state.to(inputs.device)
        else:
            state_t = initial_state

        state_seq: list[torch.Tensor] = []
        for t in range(steps):
            state_t = self.step(inputs[:, t], state_t)
            state_seq.append(state_t)

        final_state = state_t
        if persist_state:
            self._persistent_state = final_state.detach()

        return WorldModelOutput(states=torch.stack(state_seq, dim=1), final_state=final_state)

    def iter_module_views(self, states: torch.Tensor) -> Iterable[torch.Tensor]:
        """Yield per-module views of a latent state tensor [B, T, D] or [B, D]."""
        if states.ndim not in {2, 3}:
            raise ValueError("Expected state tensor with 2 or 3 dimensions.")

        for start, end in self.module_slices:
            if states.ndim == 3:
                yield states[:, :, start:end]
            else:
                yield states[:, start:end]
