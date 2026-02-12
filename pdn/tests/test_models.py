import torch

from persistent_diamonds_v3.models import DiscreteNarrator, ModularSSMWorldModel, ReportHead


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
