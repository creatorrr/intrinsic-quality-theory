"""Training infrastructure utilities for scaling beyond toy runs.

Provides helpers for:
- bf16 autocast contexts
- Gradient accumulation stepping
- Activation checkpointing wrappers
- Optional ``accelerate`` integration
"""

from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING

import torch
from torch import nn

if TYPE_CHECKING:
    from persistent_diamonds_v3.config import InfraConfig


def autocast_context(device: torch.device, infra: InfraConfig) -> contextlib.AbstractContextManager:
    """Return an autocast context manager when bf16 is enabled, otherwise a no-op."""
    if infra.bf16:
        dtype = torch.bfloat16
        device_type = "cuda" if device.type == "cuda" else "cpu"
        return torch.autocast(device_type=device_type, dtype=dtype)
    return contextlib.nullcontext()


def maybe_accumulate_step(
    optimizer: torch.optim.Optimizer,
    loss: torch.Tensor,
    step: int,
    infra: InfraConfig,
    *,
    scaler: torch.amp.GradScaler | None = None,
    max_grad_norm: float | None = None,
    parameters: list[nn.Parameter] | None = None,
) -> bool:
    """Backward pass with optional gradient accumulation.

    Returns *True* when an optimiser step was actually taken (i.e. the
    accumulation boundary was reached).
    """
    accum = max(1, infra.gradient_accumulation_steps)
    scaled_loss = loss / accum

    if scaler is not None:
        scaler.scale(scaled_loss).backward()
    else:
        scaled_loss.backward()

    if (step + 1) % accum != 0:
        return False

    if scaler is not None:
        if max_grad_norm is not None and parameters:
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(parameters, max_grad_norm)
        scaler.step(optimizer)
        scaler.update()
    else:
        if max_grad_norm is not None and parameters:
            torch.nn.utils.clip_grad_norm_(parameters, max_grad_norm)
        optimizer.step()

    optimizer.zero_grad(set_to_none=True)
    return True


def apply_activation_checkpointing(model: nn.Module, infra: InfraConfig) -> None:
    """Wrap eligible sub-modules with activation checkpointing when enabled."""
    if not infra.activation_checkpointing:
        return

    from torch.utils.checkpoint import checkpoint  # noqa: F401

    # Patch forward methods of nn.Sequential children to use checkpointing.
    for name, module in model.named_modules():
        if isinstance(module, nn.Sequential) and len(list(module.children())) > 1:
            _orig_forward = module.forward

            def _make_ckpt_forward(orig):
                def _ckpt_forward(*args, **kwargs):
                    return torch.utils.checkpoint.checkpoint(orig, *args, use_reentrant=False, **kwargs)
                return _ckpt_forward

            module.forward = _make_ckpt_forward(_orig_forward)


def build_accelerator(infra: InfraConfig):
    """Build an ``accelerate.Accelerator`` when enabled, else return *None*."""
    if not infra.use_accelerate:
        return None

    try:
        from accelerate import Accelerator
    except ImportError as exc:
        raise ImportError(
            "accelerate is required when infra.use_accelerate=True. "
            "Install with: pip install 'persistent-diamonds-v3[training]'"
        ) from exc

    mixed_precision = "bf16" if infra.bf16 else "no"
    return Accelerator(
        gradient_accumulation_steps=infra.gradient_accumulation_steps,
        mixed_precision=mixed_precision,
    )
