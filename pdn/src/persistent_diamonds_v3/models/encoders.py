from __future__ import annotations

from abc import ABC, abstractmethod

import torch
from torch import nn


class ModalityEncoder(ABC, nn.Module):
    """Base interface for modality encoders.

    Encoders produce *perturbations* (additive deltas) to the world-model
    input, not complete representations.  This keeps the world model's
    latent dynamics dominant while allowing sensory grounding.
    """

    @abstractmethod
    def forward(self, raw: torch.Tensor) -> torch.Tensor:
        """Map raw modality input to a perturbation vector of shape [B, input_dim]."""
        ...

    @property
    @abstractmethod
    def output_dim(self) -> int:
        """Dimensionality of the perturbation vector (must match world-model input_dim)."""
        ...


class TextEncoder(ModalityEncoder):
    """Wraps a frozen embedding table and projects to world-model input_dim.

    The embedding weights are frozen by default (``freeze=True``).  The
    projection layer is trainable and maps embeddings to perturbation space.
    """

    def __init__(
        self,
        vocab_size: int,
        embed_dim: int,
        input_dim: int,
        *,
        freeze: bool = True,
    ):
        super().__init__()
        self._input_dim = input_dim
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        if freeze:
            self.embedding.weight.requires_grad_(False)
        self.projection = nn.Sequential(
            nn.Linear(embed_dim, input_dim),
            nn.Tanh(),
        )

    @property
    def output_dim(self) -> int:
        return self._input_dim

    def forward(self, token_ids: torch.Tensor) -> torch.Tensor:
        """token_ids: [B] or [B, S] -> perturbation [B, input_dim]."""
        emb = self.embedding(token_ids)
        if emb.ndim == 3:
            emb = emb.mean(dim=1)
        return self.projection(emb)


class VisionEncoder(ModalityEncoder):
    """Lightweight vision encoder stub.

    Accepts a flat feature vector (e.g. from a frozen ViT backbone) and
    projects it to a perturbation of the world-model input.
    """

    def __init__(self, feature_dim: int, input_dim: int):
        super().__init__()
        self._input_dim = input_dim
        self.net = nn.Sequential(
            nn.Linear(feature_dim, input_dim),
            nn.SiLU(),
            nn.Linear(input_dim, input_dim),
            nn.Tanh(),
        )

    @property
    def output_dim(self) -> int:
        return self._input_dim

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        """features: [B, feature_dim] -> perturbation [B, input_dim]."""
        return self.net(features)


class ProprioRewardEncoder(ModalityEncoder):
    """Encodes proprioceptive signals and scalar rewards into perturbations."""

    def __init__(self, proprio_dim: int, input_dim: int):
        super().__init__()
        self._input_dim = input_dim
        self.net = nn.Sequential(
            nn.Linear(proprio_dim, input_dim),
            nn.SiLU(),
            nn.Linear(input_dim, input_dim),
            nn.Tanh(),
        )

    @property
    def output_dim(self) -> int:
        return self._input_dim

    def forward(self, proprio: torch.Tensor) -> torch.Tensor:
        """proprio: [B, proprio_dim] -> perturbation [B, input_dim]."""
        return self.net(proprio)
