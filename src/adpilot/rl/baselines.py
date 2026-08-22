"""Baseline policies for marketing optimization: Random, Rule-Based, and Contextual Bandit."""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

import numpy as np
import torch

from .environment import CampaignOptimizationEnv

logger = logging.getLogger(__name__)


class RandomPolicy:
    """Baseline policy selecting uniform random actions from continuous action space."""

    def __init__(self, action_dim: int = 5, seed: Optional[int] = None) -> None:
        self.action_dim = action_dim
        self.rng = np.random.default_rng(seed)

    def select_action(self, state: np.ndarray, deterministic: bool = False) -> np.ndarray:
        return self.rng.uniform(-1.0, 1.0, size=(self.action_dim,)).astype(np.float32)


class RuleBasedPolicy:
    """Deterministic heuristic control policy balancing ROAS, CPA, and creative fatigue."""

    def select_action(self, state: np.ndarray, deterministic: bool = True) -> np.ndarray:
        # State: [spent_ratio, time_ratio, roas/target, cpa/target, ctr/target, ch1, ch2, ch3, fatigue, pacing]
        roas_ratio = float(state[2])
        cpa_ratio = float(state[3])
        fatigue = float(state[8])

        # Rule 1: High CPA -> Reduce Meta/ch2 allocation, shift to LinkedIn/ch1 and Email/ch3
        if cpa_ratio > 1.15:
            delta_ch1 = 0.40   # Increase LinkedIn (B2B intent)
            delta_ch2 = -0.60  # Decrease Facebook
            delta_ch3 = 0.20   # Increase Email
            bid_delta = -0.30  # Cool down bids
        # Rule 2: High ROAS -> Scale up high performing channels & raise bid
        elif roas_ratio > 1.10:
            delta_ch1 = 0.20
            delta_ch2 = 0.10
            delta_ch3 = -0.30
            bid_delta = 0.25
        else:
            delta_ch1 = 0.0
            delta_ch2 = 0.0
            delta_ch3 = 0.0
            bid_delta = 0.0

        # Rule 3: Creative Fatigue > 0.45 -> Trigger creative refresh
        refresh_trigger = 0.80 if fatigue > 0.45 else -0.80

        action = np.array([delta_ch1, delta_ch2, delta_ch3, bid_delta, refresh_trigger], dtype=np.float32)
        return np.clip(action, -1.0, 1.0)


class ContextualBanditPolicy:
    """Thompson Sampling Multi-Armed Bandit over discrete campaign operational strategies."""

    # 4 distinct candidate strategic postures:
    # 0: High-Intent B2B (Heavy LinkedIn, Low Meta, Refresh off)
    # 1: Scaled Reach (Balanced LinkedIn + Meta, Higher Bid)
    # 2: Cost-Efficiency / Retargeting (Heavy Email + LinkedIn, Low Bid)
    # 3: Creative Reset (Refresh on, Moderate Bid)
    STRATEGY_ARMS = [
        np.array([0.50, -0.60, 0.10, -0.20, -0.50], dtype=np.float32),
        np.array([0.10, 0.40, -0.50, 0.40, -0.50], dtype=np.float32),
        np.array([0.20, -0.40, 0.60, -0.40, -0.50], dtype=np.float32),
        np.array([0.00, 0.00, 0.00, 0.00, 0.90], dtype=np.float32),
    ]

    def __init__(self, n_arms: int = 4, seed: Optional[int] = None) -> None:
        self.n_arms = n_arms
        self.rng = np.random.default_rng(seed)
        # Beta distribution priors for Thompson Sampling
        self.alpha = np.ones(n_arms, dtype=np.float64) * 2.0
        self.beta = np.ones(n_arms, dtype=np.float64) * 2.0

    def select_action(self, state: np.ndarray, deterministic: bool = False) -> np.ndarray:
        if deterministic:
            # Exploit highest expected mean
            arm = int(np.argmax(self.alpha / (self.alpha + self.beta)))
        else:
            # Thompson sampling draw
            samples = self.rng.beta(self.alpha, self.beta)
            arm = int(np.argmax(samples))

        return self.STRATEGY_ARMS[arm].copy()

    def update(self, arm: int, reward: float) -> None:
        """Update Bayesian priors based on observed reward signal (normalized in [0, 1])."""
        normalized_reward = np.clip((reward + 1.0) / 4.0, 0.0, 1.0)
        self.alpha[arm] += normalized_reward
        self.beta[arm] += (1.0 - normalized_reward)


def evaluate_policy(
    policy: Any,
    env: CampaignOptimizationEnv,
    num_episodes: int = 50,
    seed: int = 42,
) -> Dict[str, float]:
    """Run comparative evaluation of a policy over simulated campaign episodes."""
    cumulative_rewards: List[float] = []
    final_roas_list: List[float] = []
    final_cpa_list: List[float] = []
    total_conversions_list: List[int] = []
    total_revenue_list: List[float] = []

    for ep in range(num_episodes):
        obs, _ = env.reset(seed=seed + ep)
        ep_reward = 0.0
        terminated = False

        while not terminated:
            if hasattr(policy, "select_action"):
                action = policy.select_action(obs, deterministic=True)
            elif isinstance(policy, torch.nn.Module):
                with torch.no_grad():
                    state_t = torch.as_tensor(obs, dtype=torch.float32)
                    action_t, _, _ = policy.get_action(state_t, deterministic=True)
                    action = action_t.cpu().numpy()
            else:
                action = np.zeros(5, dtype=np.float32)

            obs, reward, terminated, truncated, info = env.step(action)
            ep_reward += reward
            if terminated or truncated:
                break

        cumulative_rewards.append(ep_reward)
        final_roas_list.append(info.get("current_roas", 0.0))
        final_cpa_list.append(info.get("current_cpa", 0.0))
        total_conversions_list.append(info.get("cumulative_conversions", 0))
        total_revenue_list.append(info.get("cumulative_revenue", 0.0))

    return {
        "mean_cumulative_reward": float(np.mean(cumulative_rewards)),
        "std_cumulative_reward": float(np.std(cumulative_rewards)),
        "mean_final_roas": float(np.mean(final_roas_list)),
        "mean_final_cpa": float(np.mean(final_cpa_list)),
        "mean_conversions": float(np.mean(total_conversions_list)),
        "mean_revenue": float(np.mean(total_revenue_list)),
    }
