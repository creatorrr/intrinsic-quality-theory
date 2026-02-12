from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import nn


@dataclass(slots=True)
class ControlOutput:
    action_logits: torch.Tensor
    value_estimate: torch.Tensor


class ControlHead(nn.Module):
    """MLP control head producing action logits and value estimates.

    Receives **narrator state only** (the discrete bottleneck output ``b_t``),
    enforcing the no-bypass hard constraint (HC-1): no path from raw world
    state ``z_t`` to action outputs exists.
    """

    def __init__(
        self,
        narrator_dim: int,
        action_dim: int,
        hidden_dim: int,
    ):
        super().__init__()
        self.narrator_dim = narrator_dim
        self.action_dim = action_dim

        self.shared = nn.Sequential(
            nn.Linear(narrator_dim, hidden_dim),
            nn.SiLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.SiLU(),
        )
        self.action_head = nn.Linear(hidden_dim, action_dim)
        self.value_head = nn.Linear(hidden_dim, 1)

    def forward(self, narrator_state: torch.Tensor) -> ControlOutput:
        """narrator_state: [B, narrator_dim] or [B, T, narrator_dim]."""
        h = self.shared(narrator_state)
        return ControlOutput(
            action_logits=self.action_head(h),
            value_estimate=self.value_head(h),
        )
