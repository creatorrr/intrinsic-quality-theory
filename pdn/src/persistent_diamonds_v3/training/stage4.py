"""Stage 4 – Embodied Grounding.

Trains the world model, narrator, and control head in a closed-loop
interaction with a gridworld environment.  The control head receives
narrator state only (no-bypass), selects actions, and the resulting
trajectories are used to update all three components jointly.

Loss components
---------------
- **Value prediction**: MSE between control-head value estimates and
  GAE-computed returns.
- **Policy gradient**: REINFORCE-style loss with GAE advantages, plus
  entropy regularisation.
- **Narrator consistency**: Self-prediction loss on narrator state
  transitions under real action sequences.
- **Grounded-autonomy bonus**: Rewards internal variance dominance
  once task performance exceeds a threshold.
"""

from __future__ import annotations

from dataclasses import dataclass

import torch
import torch.nn.functional as F
from torch import nn
from tqdm.auto import tqdm

from persistent_diamonds_v3.config import Stage4Config
from persistent_diamonds_v3.data.env.gridworld import GridWorld, GridWorldConfig
from persistent_diamonds_v3.models.control_head import ControlHead
from persistent_diamonds_v3.models.narrator import DiscreteNarrator
from persistent_diamonds_v3.models.world_model import ModularSSMWorldModel


@dataclass(slots=True)
class Stage4Result:
    final_loss: float
    mean_episode_reward: float
    mean_episode_length: float
    goal_rate: float
    steps: int


@dataclass(slots=True)
class _Transition:
    observation: torch.Tensor
    action: int
    reward: float
    done: bool
    log_prob: torch.Tensor
    value: torch.Tensor
    narrator_state: torch.Tensor


class Stage4EmbodiedTrainer:
    """Closed-loop embodied training with narrator-mediated control."""

    def __init__(
        self,
        world_model: ModularSSMWorldModel,
        narrator: DiscreteNarrator,
        control_head: ControlHead,
        *,
        stage4_cfg: Stage4Config,
        input_dim: int,
        learning_rate: float,
        weight_decay: float,
        device: str,
    ):
        self.device = torch.device(device)
        self.world_model = world_model.to(self.device)
        self.narrator = narrator.to(self.device)
        self.control_head = control_head.to(self.device)
        self.cfg = stage4_cfg

        # Observation adapter: project env obs to world-model input_dim.
        env_tmp = GridWorld(GridWorldConfig(grid_size=stage4_cfg.grid_size))
        self.env_obs_dim = env_tmp.obs_dim
        self.obs_adapter = nn.Sequential(
            nn.Linear(self.env_obs_dim, input_dim),
            nn.SiLU(),
            nn.Linear(input_dim, input_dim),
            nn.Tanh(),
        ).to(self.device)

        params = (
            list(self.world_model.parameters())
            + list(self.narrator.parameters())
            + list(self.control_head.parameters())
            + list(self.obs_adapter.parameters())
        )
        self.optimizer = torch.optim.AdamW(
            params, lr=learning_rate, weight_decay=weight_decay,
        )

    def _collect_episode(self, env: GridWorld) -> list[_Transition]:
        """Roll out one episode, collecting transitions."""
        obs = env.reset().to(self.device)
        transitions: list[_Transition] = []
        hidden_state: torch.Tensor | None = None

        # Initialise world model state for batch-size 1.
        state_t = torch.zeros(1, self.world_model.latent_dim, device=self.device)

        for _ in range(self.cfg.max_episode_steps):
            # Encode observation and step world model.
            input_t = self.obs_adapter(obs.unsqueeze(0))  # [1, input_dim]
            state_t = self.world_model.step(input_t, state_t)

            # Run narrator on the current state (window of 1).
            narrator_out = self.narrator(
                state_t.unsqueeze(1),  # [1, 1, latent_dim]
                hidden_state=hidden_state,
            )
            hidden_state = narrator_out.hidden_state
            narrator_state = narrator_out.narrator_state  # [1, narrator_dim]

            # Control head selects action.
            ctrl = self.control_head(narrator_state)
            action_dist = torch.distributions.Categorical(logits=ctrl.action_logits.squeeze(0))
            action = action_dist.sample()
            log_prob = action_dist.log_prob(action)

            transitions.append(
                _Transition(
                    observation=obs,
                    action=int(action.item()),
                    reward=0.0,  # filled after step
                    done=False,
                    log_prob=log_prob,
                    value=ctrl.value_estimate.squeeze(),
                    narrator_state=narrator_state.squeeze(0),
                )
            )

            result = env.step(int(action.item()))
            transitions[-1].reward = result.reward
            transitions[-1].done = result.done

            if result.done:
                break
            obs = result.observation.to(self.device)

        return transitions

    def _compute_gae(
        self,
        rewards: list[float],
        values: list[torch.Tensor],
        dones: list[bool],
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """Compute GAE advantages and discounted returns."""
        n = len(rewards)
        advantages = torch.zeros(n, device=self.device)
        gae = torch.tensor(0.0, device=self.device)

        for t in reversed(range(n)):
            next_value = values[t + 1] if t + 1 < n and not dones[t] else torch.tensor(0.0, device=self.device)
            delta = rewards[t] + self.cfg.gamma * next_value.detach() - values[t].detach()
            mask = 0.0 if dones[t] else 1.0
            gae = delta + self.cfg.gamma * self.cfg.gae_lambda * mask * gae
            advantages[t] = gae

        returns = advantages + torch.stack([v.detach() for v in values])
        return advantages, returns

    def _grounded_autonomy_metric(
        self,
        narrator_states: torch.Tensor,
        rewards: torch.Tensor,
    ) -> torch.Tensor:
        """Encourage internal-variance dominance when task performance is adequate."""
        mean_reward = rewards.mean()
        if mean_reward.item() < 0.0:
            # Task performance not yet adequate.
            return narrator_states.new_tensor(0.0)

        internal_var = narrator_states.var()
        reward_var = rewards.var() + 1e-6
        ratio = internal_var / (internal_var + reward_var + 1e-6)
        return -torch.log(ratio + 1e-6)

    def train(
        self,
        *,
        max_steps: int,
        env_config: GridWorldConfig | None = None,
    ) -> Stage4Result:
        env_config = env_config or GridWorldConfig(
            grid_size=self.cfg.grid_size,
            max_episode_steps=self.cfg.max_episode_steps,
        )
        env = GridWorld(env_config)

        steps = 0
        final_loss = 0.0
        episode_rewards: list[float] = []
        episode_lengths: list[int] = []
        goal_hits: list[bool] = []

        progress = tqdm(total=max_steps, desc="stage4-embodied")

        while steps < max_steps:
            # Collect a batch of episodes.
            batch_transitions: list[list[_Transition]] = []
            for _ in range(self.cfg.episodes_per_epoch):
                if steps >= max_steps:
                    break
                episode = self._collect_episode(env)
                batch_transitions.append(episode)

                ep_reward = sum(t.reward for t in episode)
                episode_rewards.append(ep_reward)
                episode_lengths.append(len(episode))
                goal_hits.append(episode[-1].done and episode[-1].reward > 0.5)

            if not batch_transitions:
                break

            # Compute loss over the batch.
            total_policy_loss = torch.tensor(0.0, device=self.device)
            total_value_loss = torch.tensor(0.0, device=self.device)
            total_narrator_loss = torch.tensor(0.0, device=self.device)
            total_grounded = torch.tensor(0.0, device=self.device)
            total_entropy = torch.tensor(0.0, device=self.device)
            count = 0

            for episode in batch_transitions:
                if len(episode) < 2:
                    continue

                rewards = [t.reward for t in episode]
                values = [t.value for t in episode]
                dones = [t.done for t in episode]
                log_probs = torch.stack([t.log_prob for t in episode])
                narrator_states = torch.stack([t.narrator_state for t in episode])

                advantages, returns = self._compute_gae(rewards, values, dones)
                advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

                # Policy gradient loss.
                policy_loss = -(log_probs * advantages.detach()).mean()

                # Value loss.
                value_preds = torch.stack(values)
                value_loss = F.mse_loss(value_preds, returns)

                # Narrator consistency: self-prediction across adjacent steps.
                narrator_pred = narrator_states[:-1]
                narrator_target = narrator_states[1:].detach()
                narrator_loss = F.mse_loss(narrator_pred, narrator_target)

                # Grounded-autonomy bonus.
                reward_tensor = torch.tensor(rewards, device=self.device, dtype=torch.float32)
                grounded_loss = self._grounded_autonomy_metric(narrator_states, reward_tensor)

                # Entropy bonus.
                # We can't recompute the full distribution cheaply, so we use
                # the approximation: H ≈ -mean(log_prob).
                entropy = -log_probs.mean()

                total_policy_loss = total_policy_loss + policy_loss
                total_value_loss = total_value_loss + value_loss
                total_narrator_loss = total_narrator_loss + narrator_loss
                total_grounded = total_grounded + grounded_loss
                total_entropy = total_entropy + entropy
                count += 1

            if count == 0:
                continue

            total_policy_loss = total_policy_loss / count
            total_value_loss = total_value_loss / count
            total_narrator_loss = total_narrator_loss / count
            total_grounded = total_grounded / count
            total_entropy = total_entropy / count

            loss = (
                total_policy_loss
                + self.cfg.value_coeff * total_value_loss
                + self.cfg.narrator_consistency_coeff * total_narrator_loss
                + self.cfg.grounded_autonomy_coeff * total_grounded
                - self.cfg.entropy_coeff * total_entropy
            )

            self.optimizer.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.world_model.parameters(), self.cfg.gradient_clip_norm)
            torch.nn.utils.clip_grad_norm_(self.narrator.parameters(), self.cfg.gradient_clip_norm)
            torch.nn.utils.clip_grad_norm_(self.control_head.parameters(), self.cfg.gradient_clip_norm)
            self.optimizer.step()

            final_loss = float(loss.item())
            steps += 1
            progress.update(1)

            mean_r = sum(episode_rewards[-self.cfg.episodes_per_epoch:]) / max(1, len(episode_rewards[-self.cfg.episodes_per_epoch:]))
            gr = sum(goal_hits[-self.cfg.episodes_per_epoch:]) / max(1, len(goal_hits[-self.cfg.episodes_per_epoch:]))
            progress.set_postfix(
                loss=f"{final_loss:.4f}",
                reward=f"{mean_r:.3f}",
                goal=f"{gr:.2f}",
            )

        progress.close()

        mean_ep_reward = sum(episode_rewards) / max(1, len(episode_rewards))
        mean_ep_length = sum(episode_lengths) / max(1, len(episode_lengths))
        goal_rate = sum(goal_hits) / max(1, len(goal_hits))

        return Stage4Result(
            final_loss=final_loss,
            mean_episode_reward=mean_ep_reward,
            mean_episode_length=mean_ep_length,
            goal_rate=goal_rate,
            steps=steps,
        )
