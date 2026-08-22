"""Actor-Critic Neural Network Architecture for Proximal Policy Optimization (PPO)."""

from __future__ import annotations

from typing import Tuple

import torch
import torch.nn as nn
from torch.distributions import Normal


class PPOActorCriticNetwork(nn.Module):
    """Continuous Actor-Critic Network parameterized with diagonal Gaussian policy."""

    def __init__(
        self,
        state_dim: int = 10,
        action_dim: int = 5,
        hidden_dim: int = 64,
    ) -> None:
        super().__init__()
        self.state_dim = state_dim
        self.action_dim = action_dim

        # Shared feature representation
        self.shared_net = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.Tanh(),
        )

        # Actor head (policy mean)
        self.actor_mean = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.Tanh(),
            nn.Linear(hidden_dim // 2, action_dim),
            nn.Tanh(),  # Bounded in [-1.0, 1.0]
        )
        self.actor_log_std = nn.Parameter(torch.zeros(action_dim))

        # Critic head (state value function)
        self.critic = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.Tanh(),
            nn.Linear(hidden_dim // 2, 1),
        )

    def forward(self, state: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """Forward pass computing action distribution mean and state value."""
        features = self.shared_net(state)
        action_mean = self.actor_mean(features)
        value = self.critic(features)
        return action_mean, value

    def get_action(
        self,
        state: torch.Tensor,
        deterministic: bool = False,
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Sample action, compute log-likelihood and estimated state value."""
        if state.dim() == 1:
            state = state.unsqueeze(0)

        action_mean, value = self.forward(state)
        action_std = torch.exp(self.actor_log_std.clamp(-20, 2))
        dist = Normal(action_mean, action_std)

        if deterministic:
            action = action_mean
        else:
            action = dist.sample()

        action_clipped = torch.clamp(action, -1.0, 1.0)
        log_prob = dist.log_prob(action).sum(dim=-1)

        return action_clipped.squeeze(0), log_prob.squeeze(0), value.squeeze(-1).squeeze(0)

    def evaluate_actions(
        self,
        states: torch.Tensor,
        actions: torch.Tensor,
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Evaluate batch of states and actions for PPO gradient updates."""
        action_mean, values = self.forward(states)
        action_std = torch.exp(self.actor_log_std.clamp(-20, 2))
        dist = Normal(action_mean, action_std)

        log_probs = dist.log_prob(actions).sum(dim=-1)
        entropy = dist.entropy().sum(dim=-1)

        return values.squeeze(-1), log_probs, entropy
