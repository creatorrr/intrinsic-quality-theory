from __future__ import annotations

from dataclasses import dataclass
import math

import torch
from torch import nn


@dataclass(slots=True)
class NarratorOutput:
    code_indices: torch.Tensor
    quantized_codes: torch.Tensor
    narrator_state: torch.Tensor
    uncertainty: torch.Tensor
    predicted_next_state: torch.Tensor
    vq_loss: torch.Tensor
    hidden_state: torch.Tensor


class MultiCodeVectorQuantizer(nn.Module):
    def __init__(self, codebook_size: int, code_dim: int, commitment_weight: float = 0.25):
        super().__init__()
        self.codebook_size = codebook_size
        self.code_dim = code_dim
        self.commitment_weight = commitment_weight
        self.embedding = nn.Parameter(torch.randn(codebook_size, code_dim) * 0.02)

    def forward(self, queries: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        # queries: [B, K, C]
        distances = (
            queries.pow(2).sum(dim=-1, keepdim=True)
            + self.embedding.pow(2).sum(dim=-1).view(1, 1, -1)
            - 2.0 * torch.einsum("bkc,nc->bkn", queries, self.embedding)
        )
        code_indices = distances.argmin(dim=-1)
        quantized = self.embedding[code_indices]

        commit_loss = (queries.detach() - quantized).pow(2).mean()
        codebook_loss = (queries - quantized.detach()).pow(2).mean()
        vq_loss = codebook_loss + self.commitment_weight * commit_loss

        quantized_st = queries + (quantized - queries).detach()
        return code_indices, quantized_st, vq_loss


class DiscreteNarrator(nn.Module):
    """Windowed narrator with explicit discrete bitrate cap and self-model heads."""

    def __init__(
        self,
        latent_dim: int,
        hidden_dim: int,
        window_size: int,
        update_hz: int,
        codebook_size: int,
        codes_per_step: int,
        code_dim: int,
    ):
        super().__init__()
        self.latent_dim = latent_dim
        self.hidden_dim = hidden_dim
        self.window_size = window_size
        self.update_hz = update_hz
        self.codes_per_step = codes_per_step
        self.codebook_size = codebook_size
        self.code_dim = code_dim

        self.window_gru = nn.GRU(
            input_size=latent_dim,
            hidden_size=hidden_dim,
            batch_first=True,
        )
        self.query_projection = nn.Linear(hidden_dim, codes_per_step * code_dim)
        self.quantizer = MultiCodeVectorQuantizer(codebook_size=codebook_size, code_dim=code_dim)

        bottleneck_dim = codes_per_step * code_dim
        self.uncertainty_head = nn.Sequential(
            nn.Linear(latent_dim + bottleneck_dim, hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, hidden_dim),
        )
        self.self_prediction_head = nn.Sequential(
            nn.Linear(bottleneck_dim, hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, bottleneck_dim),
        )

    @property
    def bits_per_second(self) -> float:
        return float(self.codes_per_step * math.log2(self.codebook_size) * self.update_hz)

    def forward(
        self,
        state_window: torch.Tensor,
        *,
        hidden_state: torch.Tensor | None = None,
    ) -> NarratorOutput:
        if state_window.ndim != 3:
            raise ValueError("Expected state window as [B, W, D].")
        if state_window.shape[1] > self.window_size:
            state_window = state_window[:, -self.window_size :]
        if state_window.size(-1) != self.latent_dim:
            raise ValueError(f"Expected latent dim {self.latent_dim}, got {state_window.size(-1)}")

        gru_out, final_hidden = self.window_gru(state_window, hidden_state)
        last_hidden = final_hidden[-1]

        queries = self.query_projection(last_hidden).view(-1, self.codes_per_step, self.code_dim)
        code_indices, quantized_codes, vq_loss = self.quantizer(queries)
        narrator_state = quantized_codes.flatten(start_dim=1)

        last_world_state = state_window[:, -1]
        uncertainty = self.uncertainty_head(torch.cat([last_world_state, narrator_state], dim=-1))
        predicted_next_state = self.self_prediction_head(narrator_state)

        return NarratorOutput(
            code_indices=code_indices,
            quantized_codes=quantized_codes,
            narrator_state=narrator_state,
            uncertainty=uncertainty,
            predicted_next_state=predicted_next_state,
            vq_loss=vq_loss,
            hidden_state=final_hidden,
        )
