import torch

from persistent_diamonds_v3.models import (
    ControlHead,
    DiscreteNarrator,
    ModularSSMWorldModel,
    ProprioRewardEncoder,
    ReportHead,
    TextEncoder,
    VisionEncoder,
)


def test_world_model_shapes():
    model = ModularSSMWorldModel(
        input_dim=16,
        latent_dim=64,
        module_count=4,
        overlap_ratio=0.25,
        hidden_dim=32,
    )
    x = torch.randn(2, 10, 16)
    out = model(x)
    assert out.states.shape == (2, 10, 64)
    assert out.final_state.shape == (2, 64)


def test_narrator_shapes_and_rate():
    narrator = DiscreteNarrator(
        latent_dim=64,
        hidden_dim=32,
        window_size=4,
        update_hz=10,
        codebook_size=1024,
        codes_per_step=8,
        code_dim=8,
    )
    state_window = torch.randn(2, 4, 64)
    out = narrator(state_window)

    assert out.code_indices.shape == (2, 8)
    assert out.narrator_state.shape == (2, 64)
    assert narrator.bits_per_second == 800.0


def test_report_head_forward():
    report = ReportHead(
        codebook_size=1024,
        vocab_size=1024,
        model_dim=64,
        layer_count=2,
        head_count=4,
        ff_dim=128,
        dropout=0.0,
        max_seq_len=64,
    )

    code_indices = torch.randint(0, 1024, (2, 10, 8))
    input_ids = torch.randint(0, 1024, (2, 12))
    logits = report(code_indices, input_ids)

    assert logits.shape == (2, 12, 1024)


# --- Action-conditioned world model tests ---


def test_world_model_action_conditioning_shapes():
    model = ModularSSMWorldModel(
        input_dim=16,
        latent_dim=64,
        module_count=4,
        overlap_ratio=0.25,
        hidden_dim=32,
        action_dim=8,
    )
    x = torch.randn(2, 10, 16)
    actions = torch.randn(2, 10, 8)
    out = model(x, actions=actions)
    assert out.states.shape == (2, 10, 64)
    assert out.final_state.shape == (2, 64)


def test_world_model_action_conditioning_differs_from_no_action():
    model = ModularSSMWorldModel(
        input_dim=16,
        latent_dim=64,
        module_count=4,
        overlap_ratio=0.25,
        hidden_dim=32,
        action_dim=8,
    )
    x = torch.randn(2, 10, 16)
    actions = torch.randn(2, 10, 8)

    out_with = model(x, actions=actions, initial_state=torch.zeros(2, 64))
    out_without = model(x, initial_state=torch.zeros(2, 64))

    # With action_dim>0 and no action provided, the model should still work
    # (modules receive no action tensor) but results should differ from
    # providing explicit actions.
    assert not torch.allclose(out_with.states, out_without.states, atol=1e-5)


def test_world_model_backward_compat_no_action_dim():
    """action_dim=0 (default) preserves the original interface."""
    model = ModularSSMWorldModel(
        input_dim=16,
        latent_dim=64,
        module_count=4,
        overlap_ratio=0.25,
        hidden_dim=32,
    )
    assert model.action_dim == 0
    x = torch.randn(2, 10, 16)
    out = model(x)
    assert out.states.shape == (2, 10, 64)


# --- Encoder tests ---


def test_text_encoder_shapes():
    enc = TextEncoder(vocab_size=1000, embed_dim=64, input_dim=16)
    # Single token per sample
    ids = torch.randint(0, 1000, (4,))
    pert = enc(ids)
    assert pert.shape == (4, 16)

    # Sequence of tokens
    ids_seq = torch.randint(0, 1000, (4, 5))
    pert_seq = enc(ids_seq)
    assert pert_seq.shape == (4, 16)


def test_text_encoder_frozen_by_default():
    enc = TextEncoder(vocab_size=100, embed_dim=32, input_dim=16)
    assert not enc.embedding.weight.requires_grad


def test_text_encoder_perturbation_bounded():
    """Tanh output should be in [-1, 1]."""
    enc = TextEncoder(vocab_size=100, embed_dim=32, input_dim=16)
    ids = torch.randint(0, 100, (8, 3))
    pert = enc(ids)
    assert pert.min() >= -1.0
    assert pert.max() <= 1.0


def test_vision_encoder_shapes():
    enc = VisionEncoder(feature_dim=128, input_dim=16)
    features = torch.randn(4, 128)
    pert = enc(features)
    assert pert.shape == (4, 16)


def test_proprio_reward_encoder_shapes():
    enc = ProprioRewardEncoder(proprio_dim=12, input_dim=16)
    proprio = torch.randn(4, 12)
    pert = enc(proprio)
    assert pert.shape == (4, 16)


# --- ControlHead tests ---


def test_control_head_shapes_2d():
    head = ControlHead(narrator_dim=64, action_dim=8, hidden_dim=32)
    narrator_state = torch.randn(2, 64)
    out = head(narrator_state)
    assert out.action_logits.shape == (2, 8)
    assert out.value_estimate.shape == (2, 1)


def test_control_head_shapes_3d():
    """ControlHead should handle temporal sequences [B, T, D]."""
    head = ControlHead(narrator_dim=64, action_dim=8, hidden_dim=32)
    narrator_state = torch.randn(2, 10, 64)
    out = head(narrator_state)
    assert out.action_logits.shape == (2, 10, 8)
    assert out.value_estimate.shape == (2, 10, 1)


def test_control_head_gradient_flows():
    head = ControlHead(narrator_dim=64, action_dim=8, hidden_dim=32)
    narrator_state = torch.randn(2, 64, requires_grad=True)
    out = head(narrator_state)
    loss = out.action_logits.sum() + out.value_estimate.sum()
    loss.backward()
    assert narrator_state.grad is not None
