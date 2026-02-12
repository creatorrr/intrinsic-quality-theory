from __future__ import annotations

import torch
from torch import nn


class ReportHead(nn.Module):
    """Small decoder that verbalizes narrator codes into text."""

    def __init__(
        self,
        codebook_size: int,
        vocab_size: int,
        model_dim: int,
        layer_count: int,
        head_count: int,
        ff_dim: int,
        dropout: float,
        max_seq_len: int,
    ):
        super().__init__()
        self.max_seq_len = max_seq_len
        self.model_dim = model_dim

        self.code_embedding = nn.Embedding(codebook_size, model_dim)
        self.token_embedding = nn.Embedding(vocab_size, model_dim)
        self.position_embedding = nn.Embedding(max_seq_len, model_dim)

        decoder_layer = nn.TransformerDecoderLayer(
            d_model=model_dim,
            nhead=head_count,
            dim_feedforward=ff_dim,
            dropout=dropout,
            batch_first=False,
            activation="gelu",
        )
        self.decoder = nn.TransformerDecoder(decoder_layer, num_layers=layer_count)
        self.lm_head = nn.Linear(model_dim, vocab_size, bias=False)

    def forward(
        self,
        code_indices: torch.Tensor,
        input_ids: torch.Tensor,
        *,
        attention_mask: torch.Tensor | None = None,
    ) -> torch.Tensor:
        if code_indices.ndim != 3:
            raise ValueError("Expected `code_indices` as [B, S, K].")
        if input_ids.ndim != 2:
            raise ValueError("Expected `input_ids` as [B, T].")

        batch, seq_len = input_ids.shape
        if seq_len > self.max_seq_len:
            raise ValueError(f"Input length {seq_len} exceeds max_seq_len={self.max_seq_len}")

        code_memory = self.code_embedding(code_indices).mean(dim=2)
        memory = code_memory.transpose(0, 1)

        positions = torch.arange(seq_len, device=input_ids.device).unsqueeze(0).expand(batch, -1)
        token_repr = self.token_embedding(input_ids) + self.position_embedding(positions)
        tgt = token_repr.transpose(0, 1)

        causal_mask = torch.triu(
            torch.ones(seq_len, seq_len, device=input_ids.device, dtype=torch.bool),
            diagonal=1,
        )

        key_padding_mask = None
        if attention_mask is not None:
            key_padding_mask = attention_mask == 0

        out = self.decoder(
            tgt=tgt,
            memory=memory,
            tgt_mask=causal_mask,
            tgt_key_padding_mask=key_padding_mask,
        )
        logits = self.lm_head(out.transpose(0, 1))
        return logits

    @torch.no_grad()
    def generate(
        self,
        code_indices: torch.Tensor,
        *,
        bos_token_id: int,
        eos_token_id: int,
        max_new_tokens: int = 128,
    ) -> torch.Tensor:
        batch = code_indices.size(0)
        tokens = torch.full((batch, 1), bos_token_id, device=code_indices.device, dtype=torch.long)

        for _ in range(max_new_tokens):
            logits = self.forward(code_indices, tokens)
            next_token = logits[:, -1].argmax(dim=-1, keepdim=True)
            tokens = torch.cat([tokens, next_token], dim=1)
            if torch.all(next_token == eos_token_id):
                break

        return tokens
