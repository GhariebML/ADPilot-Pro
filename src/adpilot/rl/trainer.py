"""PPO Trainer with Generalized Advantage Estimation, Checkpointing, and Model Versioning."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

from .environment import CampaignOptimizationEnv
from .models import PPOActorCriticNetwork

logger = logging.getLogger(__name__)


class PPOTrainer:
    """Trains PPO actor-critic network on campaign simulation environments with GAE and clipped objectives."""

    def __init__(
        self,
        env: Optional[CampaignOptimizationEnv] = None,
        state_dim: int = 10,
        action_dim: int = 5,
        hidden_dim: int = 64,
        lr: float = 3e-4,
        gamma: float = 0.99,
        gae_lambda: float = 0.95,
        clip_epsilon: float = 0.20,
        value_coef: float = 0.50,
        entropy_coef: float = 0.01,
        max_grad_norm: float = 0.50,
        device: str = "cpu",
    ) -> None:
        self.env = env or CampaignOptimizationEnv()
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.gamma = gamma
        self.gae_lambda = gae_lambda
        self.clip_epsilon = clip_epsilon
        self.value_coef = value_coef
        self.entropy_coef = entropy_coef
        self.max_grad_norm = max_grad_norm
        self.device = torch.device(device)

        self.policy = PPOActorCriticNetwork(state_dim, action_dim, hidden_dim).to(self.device)
        self.optimizer = optim.Adam(self.policy.parameters(), lr=lr)

    def train(
        self,
        num_iterations: int = 20,
        episodes_per_iteration: int = 5,
        ppo_epochs: int = 4,
        batch_size: int = 64,
    ) -> Dict[str, Any]:
        """Train PPO policy across multiple rollout iterations."""
        training_history: List[Dict[str, float]] = []

        for iteration in range(1, num_iterations + 1):
            states, actions, log_probs, rewards, dones, values = self._collect_rollouts(episodes_per_iteration)

            # Compute Generalized Advantage Estimation (GAE)
            advantages, returns = self._compute_gae(rewards, values, dones)

            # Convert to tensors
            b_states = torch.as_tensor(np.array(states), dtype=torch.float32, device=self.device)
            b_actions = torch.as_tensor(np.array(actions), dtype=torch.float32, device=self.device)
            b_log_probs = torch.as_tensor(np.array(log_probs), dtype=torch.float32, device=self.device)
            b_advantages = torch.as_tensor(np.array(advantages), dtype=torch.float32, device=self.device)
            b_returns = torch.as_tensor(np.array(returns), dtype=torch.float32, device=self.device)

            # Normalize advantages
            b_advantages = (b_advantages - b_advantages.mean()) / (b_advantages.std() + 1e-8)

            dataset_size = len(b_states)
            indices = np.arange(dataset_size)

            epoch_policy_loss = 0.0
            epoch_value_loss = 0.0
            epoch_entropy = 0.0

            for _ in range(ppo_epochs):
                np.random.shuffle(indices)
                for start in range(0, dataset_size, batch_size):
                    end = start + batch_size
                    mb_idx = indices[start:end]

                    mb_states = b_states[mb_idx]
                    mb_actions = b_actions[mb_idx]
                    mb_old_log_probs = b_log_probs[mb_idx]
                    mb_advantages = b_advantages[mb_idx]
                    mb_returns = b_returns[mb_idx]

                    new_values, new_log_probs, entropy = self.policy.evaluate_actions(mb_states, mb_actions)

                    # PPO Clipped Surrogate Loss
                    ratios = torch.exp(new_log_probs - mb_old_log_probs)
                    surr1 = ratios * mb_advantages
                    surr2 = torch.clamp(ratios, 1.0 - self.clip_epsilon, 1.0 + self.clip_epsilon) * mb_advantages
                    policy_loss = -torch.min(surr1, surr2).mean()

                    # Value function MSE loss
                    value_loss = nn.functional.mse_loss(new_values, mb_returns)

                    # Total Loss
                    loss = policy_loss + self.value_coef * value_loss - self.entropy_coef * entropy.mean()

                    self.optimizer.zero_grad()
                    loss.backward()
                    nn.utils.clip_grad_norm_(self.policy.parameters(), self.max_grad_norm)
                    self.optimizer.step()

                    epoch_policy_loss += float(policy_loss.item())
                    epoch_value_loss += float(value_loss.item())
                    epoch_entropy += float(entropy.mean().item())

            mean_reward = float(np.mean(rewards))
            stats = {
                "iteration": iteration,
                "mean_reward": round(mean_reward, 4),
                "policy_loss": round(epoch_policy_loss / max(1, ppo_epochs * (dataset_size // batch_size + 1)), 4),
                "value_loss": round(epoch_value_loss / max(1, ppo_epochs * (dataset_size // batch_size + 1)), 4),
                "entropy": round(epoch_entropy / max(1, ppo_epochs * (dataset_size // batch_size + 1)), 4),
            }
            training_history.append(stats)
            if iteration % 5 == 0 or iteration == num_iterations:
                logger.info("PPO Training Iteration %d/%d | Mean Reward: %.4f | Policy Loss: %.4f", iteration, num_iterations, stats["mean_reward"], stats["policy_loss"])

        return {
            "status": "completed",
            "iterations_trained": num_iterations,
            "final_mean_reward": training_history[-1]["mean_reward"] if training_history else 0.0,
            "history": training_history,
        }

    def _collect_rollouts(self, num_episodes: int) -> Tuple[List, List, List, List, List, List]:
        """Collect transition trajectories from environment."""
        states, actions, log_probs, rewards, dones, values = [], [], [], [], [], []

        for _ in range(num_episodes):
            obs, _ = self.env.reset()
            terminated = False

            while not terminated:
                state_t = torch.as_tensor(obs, dtype=torch.float32, device=self.device)
                with torch.no_grad():
                    action_t, log_prob_t, value_t = self.policy.get_action(state_t, deterministic=False)

                action = action_t.cpu().numpy()
                next_obs, reward, terminated, truncated, _ = self.env.step(action)

                states.append(obs)
                actions.append(action)
                log_probs.append(float(log_prob_t.cpu().item()))
                rewards.append(reward)
                dones.append(terminated or truncated)
                values.append(float(value_t.cpu().item()))

                obs = next_obs
                if terminated or truncated:
                    break

        return states, actions, log_probs, rewards, dones, values

    def _compute_gae(
        self,
        rewards: List[float],
        values: List[float],
        dones: List[bool],
    ) -> Tuple[List[float], List[float]]:
        """Compute Generalized Advantage Estimation (GAE) and target returns."""
        advantages = []
        gae = 0.0
        n_steps = len(rewards)

        for t in reversed(range(n_steps)):
            next_value = values[t + 1] if t + 1 < n_steps and not dones[t] else 0.0
            delta = rewards[t] + self.gamma * next_value * (1.0 - float(dones[t])) - values[t]
            gae = delta + self.gamma * self.gae_lambda * (1.0 - float(dones[t])) * gae
            advantages.insert(0, gae)

        returns = [adv + val for adv, val in zip(advantages, values)]
        return advantages, returns

    def save_checkpoint(self, checkpoint_path: str | Path) -> None:
        """Save PyTorch weights and training metadata."""
        path = Path(checkpoint_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        torch.save(
            {
                "state_dict": self.policy.state_dict(),
                "optimizer_state": self.optimizer.state_dict(),
                "state_dim": self.state_dim,
                "action_dim": self.action_dim,
                "version": "1.0.0",
            },
            str(path),
        )

        metadata_path = path.parent / "ppo_metadata.json"
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "model_type": "ProximalPolicyOptimization_ActorCritic",
                    "version": "1.0.0",
                    "state_dim": self.state_dim,
                    "action_dim": self.action_dim,
                    "checkpoint_file": path.name,
                    "hyperparameters": {
                        "gamma": self.gamma,
                        "gae_lambda": self.gae_lambda,
                        "clip_epsilon": self.clip_epsilon,
                        "value_coef": self.value_coef,
                        "entropy_coef": self.entropy_coef,
                    },
                },
                f,
                indent=2,
            )
        logger.info("Saved PPO checkpoint to %s and metadata to %s", path, metadata_path)

    def load_checkpoint(self, checkpoint_path: str | Path) -> None:
        """Load PyTorch weights from checkpoint file."""
        checkpoint = torch.load(str(checkpoint_path), map_location=self.device)
        self.policy.load_state_dict(checkpoint["state_dict"])
        logger.info("Loaded PPO policy checkpoint from %s", checkpoint_path)
