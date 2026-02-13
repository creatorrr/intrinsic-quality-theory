"""Minimal gridworld environment for embodied grounding (Stage 4).

The agent navigates a 2-D grid to reach a goal.  Observations are flat
vectors encoding [agent_row, agent_col, goal_row, goal_col, ...wall_flags...]
normalised to [-1, 1].  The reward is sparse: +1 on reaching the goal,
-0.01 per step otherwise.

Four discrete actions: 0=up, 1=right, 2=down, 3=left.
"""

from __future__ import annotations

from dataclasses import dataclass

import torch


@dataclass(slots=True)
class GridWorldConfig:
    grid_size: int = 8
    max_episode_steps: int = 64
    seed: int | None = None


@dataclass(slots=True)
class StepResult:
    observation: torch.Tensor
    reward: float
    done: bool
    info: dict


NUM_ACTIONS = 4

# Movement deltas indexed by action id.
_DELTAS = ((-1, 0), (0, 1), (1, 0), (0, -1))


class GridWorld:
    """Lightweight gridworld with no external dependencies."""

    def __init__(self, config: GridWorldConfig | None = None):
        config = config or GridWorldConfig()
        self.grid_size = config.grid_size
        self.max_episode_steps = config.max_episode_steps
        self._rng = torch.Generator()
        if config.seed is not None:
            self._rng.manual_seed(config.seed)
        else:
            self._rng.seed()

        self.num_actions = NUM_ACTIONS
        # obs_dim = 4 (agent_row, agent_col, goal_row, goal_col) + grid_size**2 wall bits
        self.obs_dim = 4 + self.grid_size ** 2

        # State
        self._agent_pos: tuple[int, int] = (0, 0)
        self._goal_pos: tuple[int, int] = (0, 0)
        self._walls: torch.Tensor = torch.zeros(self.grid_size, self.grid_size)
        self._step_count: int = 0

    def _random_pos(self) -> tuple[int, int]:
        r = int(torch.randint(0, self.grid_size, (1,), generator=self._rng).item())
        c = int(torch.randint(0, self.grid_size, (1,), generator=self._rng).item())
        return (r, c)

    def _scatter_walls(self, density: float = 0.1) -> None:
        self._walls = (torch.rand(self.grid_size, self.grid_size, generator=self._rng) < density).float()
        # Ensure agent and goal positions are clear.
        self._walls[self._agent_pos[0], self._agent_pos[1]] = 0.0
        self._walls[self._goal_pos[0], self._goal_pos[1]] = 0.0

    def _obs(self) -> torch.Tensor:
        norm = max(1, self.grid_size - 1)
        agent = torch.tensor(
            [self._agent_pos[0] / norm * 2 - 1, self._agent_pos[1] / norm * 2 - 1],
            dtype=torch.float32,
        )
        goal = torch.tensor(
            [self._goal_pos[0] / norm * 2 - 1, self._goal_pos[1] / norm * 2 - 1],
            dtype=torch.float32,
        )
        walls_flat = self._walls.reshape(-1)
        return torch.cat([agent, goal, walls_flat])

    def reset(self) -> torch.Tensor:
        """Reset the environment and return the initial observation."""
        self._agent_pos = self._random_pos()
        self._goal_pos = self._random_pos()
        while self._goal_pos == self._agent_pos:
            self._goal_pos = self._random_pos()
        self._scatter_walls()
        self._step_count = 0
        return self._obs()

    def step(self, action: int) -> StepResult:
        """Take one step and return (obs, reward, done, info)."""
        dr, dc = _DELTAS[action % NUM_ACTIONS]
        nr = max(0, min(self.grid_size - 1, self._agent_pos[0] + dr))
        nc = max(0, min(self.grid_size - 1, self._agent_pos[1] + dc))

        # Block movement into walls.
        if self._walls[nr, nc] > 0.5:
            nr, nc = self._agent_pos

        self._agent_pos = (nr, nc)
        self._step_count += 1

        reached_goal = self._agent_pos == self._goal_pos
        timed_out = self._step_count >= self.max_episode_steps
        done = reached_goal or timed_out
        reward = 1.0 if reached_goal else -0.01

        return StepResult(
            observation=self._obs(),
            reward=reward,
            done=done,
            info={"reached_goal": reached_goal, "steps": self._step_count},
        )
