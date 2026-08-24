"""Contextual Multi-Armed Bandits & Bayesian Decision Optimization (LinUCB & Thompson Sampling)."""

from __future__ import annotations

import logging
from typing import Dict, List, Optional, Tuple
import numpy as np

logger = logging.getLogger(__name__)


class ContextualLinUCB:
    """Contextual Upper Confidence Bound (LinUCB) bandit with disjoint linear models for each arm.
    
    Formula:
        A_a = D_a^T D_a + I_d
        b_a = D_a^T r_a
        theta_hat_a = A_a^{-1} b_a
        p_a = x^T theta_hat_a + alpha * sqrt(x^T A_a^{-1} x)
    """

    def __init__(self, n_arms: int, feature_dim: int, alpha: float = 1.0) -> None:
        self.n_arms = n_arms
        self.feature_dim = feature_dim
        self.alpha = float(alpha)

        # A_a = d x d identity matrix for each arm
        self.A: Dict[int, np.ndarray] = {
            a: np.identity(feature_dim, dtype=np.float64) for a in range(n_arms)
        }
        # b_a = d-dimensional zero vector for each arm
        self.b: Dict[int, np.ndarray] = {
            a: np.zeros((feature_dim, 1), dtype=np.float64) for a in range(n_arms)
        }

    def select_arm(self, context: np.ndarray) -> int:
        """Select best arm according to upper confidence bound given context vector."""
        x = context.reshape(-1, 1).astype(np.float64)
        p_values = np.zeros(self.n_arms, dtype=np.float64)

        for a in range(self.n_arms):
            A_inv = np.linalg.pinv(self.A[a])
            theta_hat = A_inv @ self.b[a]
            variance = float((x.T @ A_inv @ x).item())
            expected_payoff = float((x.T @ theta_hat).item())
            ucb_score = expected_payoff + self.alpha * np.sqrt(max(0.0, variance))
            p_values[a] = ucb_score

        return int(np.argmax(p_values))

    def update(self, arm: int, context: np.ndarray, reward: float) -> None:
        """Update arm covariance and reward vector with observed outcome."""
        x = context.reshape(-1, 1).astype(np.float64)
        self.A[arm] += x @ x.T
        self.b[arm] += float(reward) * x


class ThompsonSamplingBandit:
    """Bayesian Linear Regression Contextual Bandit with posterior Gaussian weight sampling."""

    def __init__(self, n_arms: int, feature_dim: int, v_sq: float = 0.25) -> None:
        self.n_arms = n_arms
        self.feature_dim = feature_dim
        self.v_sq = float(v_sq)

        self.B: Dict[int, np.ndarray] = {
            a: np.identity(feature_dim, dtype=np.float64) for a in range(n_arms)
        }
        self.f: Dict[int, np.ndarray] = {
            a: np.zeros((feature_dim, 1), dtype=np.float64) for a in range(n_arms)
        }

    def select_arm(self, context: np.ndarray) -> int:
        """Sample weights from posterior and select arm with highest expected payout."""
        x = context.reshape(-1, 1).astype(np.float64)
        expected_rewards = np.zeros(self.n_arms, dtype=np.float64)

        for a in range(self.n_arms):
            B_inv = np.linalg.pinv(self.B[a])
            mu_hat = (B_inv @ self.f[a]).flatten()
            cov = self.v_sq * B_inv
            # Sample theta from posterior normal
            theta_sample = np.random.multivariate_normal(mu_hat, cov).reshape(-1, 1)
            expected_rewards[a] = float((x.T @ theta_sample).item())

        return int(np.argmax(expected_rewards))

    def update(self, arm: int, context: np.ndarray, reward: float) -> None:
        """Update posterior parameters with observed reward."""
        x = context.reshape(-1, 1).astype(np.float64)
        self.B[arm] += x @ x.T
        self.f[arm] += float(reward) * x
