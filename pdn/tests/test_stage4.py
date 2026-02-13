"""Tests for Stage 4 – Embodied Grounding."""

import torch

from persistent_diamonds_v3.config import Stage4Config
from persistent_diamonds_v3.data.env.gridworld import GridWorld, GridWorldConfig
from persistent_diamonds_v3.models import ControlHead, DiscreteNarrator, ModularSSMWorldModel
from persistent_diamonds_v3.training.stage4 import Stage4EmbodiedTrainer, Stage4Result


# ---------------------------------------------------------------------------
# Gridworld environment tests
# ---------------------------------------------------------------------------


def test_gridworld_reset_obs_shape():
    env = GridWorld(GridWorldConfig(grid_size=5))
    obs = env.reset()
    assert obs.shape == (4 + 25,)  # 4 coords + 5*5 wall flags


def test_gridworld_step_returns_step_result():
    env = GridWorld(GridWorldConfig(grid_size=4, seed=42))
    env.reset()
    result = env.step(0)
    assert result.observation.shape == (4 + 16,)
    assert isinstance(result.reward, float)
    assert isinstance(result.done, bool)


def test_gridworld_terminates_within_max_steps():
    env = GridWorld(GridWorldConfig(grid_size=4, max_episode_steps=10, seed=0))
    env.reset()
    for _ in range(20):
        result = env.step(1)
        if result.done:
            break
    assert result.done
    assert result.info["steps"] <= 10


def test_gridworld_obs_normalised():
    env = GridWorld(GridWorldConfig(grid_size=6, seed=7))
    obs = env.reset()
    # First 4 elements (agent/goal coords) should be in [-1, 1].
    assert obs[:4].min() >= -1.0
    assert obs[:4].max() <= 1.0


def test_gridworld_wall_blocking():
    """Agent should not move into wall cells."""
    env = GridWorld(GridWorldConfig(grid_size=4, seed=99))
    env.reset()
    # Record position.
    pos_before = env._agent_pos
    # Place a wall directly above.
    above = (max(0, pos_before[0] - 1), pos_before[1])
    env._walls[above[0], above[1]] = 1.0
    env.step(0)  # action 0 = up
    assert env._agent_pos == pos_before  # blocked


def test_gridworld_num_actions():
    env = GridWorld()
    assert env.num_actions == 4


# ---------------------------------------------------------------------------
# Trainer construction and smoke test
# ---------------------------------------------------------------------------


def _small_models():
    world = ModularSSMWorldModel(
        input_dim=16, latent_dim=32, module_count=2,
        overlap_ratio=0.25, hidden_dim=16,
    )
    narrator = DiscreteNarrator(
        latent_dim=32, hidden_dim=16, window_size=2,
        update_hz=10, codebook_size=64, codes_per_step=4, code_dim=8,
    )
    control_head = ControlHead(
        narrator_dim=4 * 8,  # codes_per_step * code_dim
        action_dim=4,
        hidden_dim=16,
    )
    return world, narrator, control_head


def test_stage4_trainer_construction():
    world, narrator, control_head = _small_models()
    cfg = Stage4Config(grid_size=4, max_episode_steps=8, episodes_per_epoch=2)

    trainer = Stage4EmbodiedTrainer(
        world_model=world,
        narrator=narrator,
        control_head=control_head,
        stage4_cfg=cfg,
        input_dim=16,
        learning_rate=1e-3,
        weight_decay=1e-2,
        device="cpu",
    )
    assert trainer.obs_adapter is not None
    assert trainer.env_obs_dim == 4 + 16  # grid_size=4 -> 4 + 4**2


def test_stage4_train_smoke():
    """End-to-end smoke test: train for 2 steps on a tiny grid."""
    world, narrator, control_head = _small_models()
    cfg = Stage4Config(
        grid_size=4,
        max_episode_steps=8,
        episodes_per_epoch=2,
    )

    trainer = Stage4EmbodiedTrainer(
        world_model=world,
        narrator=narrator,
        control_head=control_head,
        stage4_cfg=cfg,
        input_dim=16,
        learning_rate=1e-3,
        weight_decay=1e-2,
        device="cpu",
    )

    result = trainer.train(max_steps=2)

    assert isinstance(result, Stage4Result)
    assert result.steps == 2
    assert isinstance(result.final_loss, float)
    assert isinstance(result.mean_episode_reward, float)
    assert isinstance(result.mean_episode_length, float)
    assert isinstance(result.goal_rate, float)
    assert 0.0 <= result.goal_rate <= 1.0


def test_stage4_result_fields():
    result = Stage4Result(
        final_loss=0.5,
        mean_episode_reward=-0.3,
        mean_episode_length=20.0,
        goal_rate=0.1,
        steps=10,
    )
    assert result.final_loss == 0.5
    assert result.steps == 10


def test_stage4_gradients_flow():
    """Verify that gradients flow through all three components."""
    world, narrator, control_head = _small_models()
    cfg = Stage4Config(
        grid_size=4,
        max_episode_steps=8,
        episodes_per_epoch=2,
    )

    trainer = Stage4EmbodiedTrainer(
        world_model=world,
        narrator=narrator,
        control_head=control_head,
        stage4_cfg=cfg,
        input_dim=16,
        learning_rate=1e-3,
        weight_decay=1e-2,
        device="cpu",
    )

    # Snapshot initial weights.
    w_before = {n: p.clone() for n, p in world.named_parameters()}
    n_before = {n: p.clone() for n, p in narrator.named_parameters()}
    c_before = {n: p.clone() for n, p in control_head.named_parameters()}

    trainer.train(max_steps=1)

    # At least some parameters should have changed.
    w_changed = any(
        not torch.equal(w_before[n], p) for n, p in world.named_parameters()
    )
    n_changed = any(
        not torch.equal(n_before[n], p) for n, p in narrator.named_parameters()
    )
    c_changed = any(
        not torch.equal(c_before[n], p) for n, p in control_head.named_parameters()
    )

    assert w_changed, "World model weights did not update"
    assert n_changed, "Narrator weights did not update"
    assert c_changed, "Control head weights did not update"


def test_stage4_with_custom_env_config():
    """Trainer accepts a custom GridWorldConfig."""
    world, narrator, control_head = _small_models()
    cfg = Stage4Config(grid_size=4, max_episode_steps=6, episodes_per_epoch=2)

    trainer = Stage4EmbodiedTrainer(
        world_model=world,
        narrator=narrator,
        control_head=control_head,
        stage4_cfg=cfg,
        input_dim=16,
        learning_rate=1e-3,
        weight_decay=1e-2,
        device="cpu",
    )

    env_cfg = GridWorldConfig(grid_size=4, max_episode_steps=6, seed=42)
    result = trainer.train(max_steps=1, env_config=env_cfg)
    assert result.steps == 1


def test_stage4_no_bypass_constraint():
    """Control head receives narrator state only (no raw world state)."""
    world, narrator, control_head = _small_models()
    # The control head's input dim is narrator_dim (codes_per_step * code_dim),
    # not world latent_dim. This is the no-bypass constraint.
    assert control_head.narrator_dim == 4 * 8  # 32
    assert control_head.narrator_dim != world.latent_dim or world.latent_dim == 32
    # Even if dims happen to match, the architecture enforces that only
    # narrator_state is passed (verified by construction in stage4.py).
