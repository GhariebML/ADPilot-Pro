"""Gymnasium-compliant Campaign Optimization Simulation Environment for Reinforcement Learning."""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional, Tuple

import gymnasium as gym
from gymnasium import spaces
import numpy as np

logger = logging.getLogger(__name__)


class CampaignOptimizationEnv(gym.Env):
    """Simulates real-world multi-channel advertising auction dynamics, bid curves, and creative fatigue."""

    metadata = {"render_modes": ["human"], "render_fps": 30}

    def __init__(
        self,
        total_budget: float = 80000.0,
        duration_days: int = 90,
        target_roas: float = 3.50,
        target_cpa: float = 45.00,
        target_ctr: float = 3.00,
        num_channels: int = 3,
        seed: Optional[int] = None,
    ) -> None:
        super().__init__()
        self.total_budget = float(total_budget)
        self.duration_days = int(duration_days)
        self.target_roas = float(target_roas)
        self.target_cpa = float(target_cpa)
        self.target_ctr = float(target_ctr)
        self.num_channels = int(num_channels)

        # Base channel characteristics [LinkedIn, Meta, Email/Search]
        # [base_cpc, base_cvr, max_capacity_per_day, elasticity]
        self.channel_profiles = [
            {"name": "linkedin", "base_cpc": 3.80, "base_cvr": 0.055, "elasticity": 0.85, "fatigue_rate": 0.02},
            {"name": "facebook", "base_cpc": 1.90, "base_cvr": 0.032, "elasticity": 0.70, "fatigue_rate": 0.04},
            {"name": "email", "base_cpc": 0.60, "base_cvr": 0.048, "elasticity": 0.90, "fatigue_rate": 0.01},
        ]

        # 10-dimensional state space:
        # 0: spent_ratio, 1: time_ratio, 2: current_roas/target, 3: current_cpa/target, 4: current_ctr/target,
        # 5: ch1_alloc, 6: ch2_alloc, 7: ch3_alloc, 8: creative_fatigue, 9: pacing_error
        self.observation_space = spaces.Box(
            low=np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -2.0], dtype=np.float32),
            high=np.array([2.0, 1.0, 5.0, 5.0, 5.0, 1.0, 1.0, 1.0, 1.0, 2.0], dtype=np.float32),
            dtype=np.float32,
        )

        # 5-dimensional continuous action space in [-1.0, 1.0]:
        # [delta_ch1, delta_ch2, delta_ch3, bid_multiplier_delta, creative_refresh_trigger]
        self.action_space = spaces.Box(
            low=-1.0,
            high=1.0,
            shape=(5,),
            dtype=np.float32,
        )

        self._rng = np.random.default_rng(seed)
        self.reset(seed=seed)

    def reset(
        self,
        *,
        seed: Optional[int] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Reset environment to day 0 with initial strategy baseline allocations."""
        if seed is not None:
            self._rng = np.random.default_rng(seed)

        self.current_day = 0
        self.total_spent = 0.0
        self.cumulative_revenue = 0.0
        self.cumulative_conversions = 0
        self.cumulative_clicks = 0
        self.cumulative_impressions = 0

        # Initial allocation weights: [60% LinkedIn, 25% Meta, 15% Email]
        self.channel_allocations = np.array([0.60, 0.25, 0.15], dtype=np.float32)
        self.bid_multiplier = 1.0
        self.creative_fatigue = 0.10

        self.current_roas = self.target_roas * float(self._rng.uniform(0.95, 1.10))
        self.current_cpa = self.target_cpa * float(self._rng.uniform(0.90, 1.05))
        self.current_ctr = self.target_ctr * float(self._rng.uniform(0.95, 1.10))

        obs = self._get_observation()
        info = {
            "day": self.current_day,
            "total_spent": self.total_spent,
            "cumulative_revenue": self.cumulative_revenue,
            "cumulative_conversions": self.cumulative_conversions,
            "channel_allocations": self.channel_allocations.tolist(),
        }
        return obs, info

    def _get_observation(self) -> np.ndarray:
        """Construct normalized 10-dimensional state vector."""
        spent_ratio = float(self.total_spent / max(1.0, self.total_budget))
        time_ratio = float(self.current_day / max(1, self.duration_days))
        roas_ratio = float(self.current_roas / max(0.1, self.target_roas))
        cpa_ratio = float(self.current_cpa / max(0.1, self.target_cpa))
        ctr_ratio = float(self.current_ctr / max(0.1, self.target_ctr))

        expected_conversions = (self.total_budget / self.target_cpa) * time_ratio
        actual_conversions = float(self.cumulative_conversions)
        pacing_error = float((actual_conversions - expected_conversions) / max(1.0, expected_conversions + 1.0))

        obs = np.array(
            [
                spent_ratio,
                time_ratio,
                np.clip(roas_ratio, 0.0, 5.0),
                np.clip(cpa_ratio, 0.0, 5.0),
                np.clip(ctr_ratio, 0.0, 5.0),
                float(self.channel_allocations[0]),
                float(self.channel_allocations[1]),
                float(self.channel_allocations[2]),
                float(self.creative_fatigue),
                np.clip(pacing_error, -2.0, 2.0),
            ],
            dtype=np.float32,
        )
        return obs

    def step(self, action: np.ndarray) -> Tuple[np.ndarray, float, bool, bool, Dict[str, Any]]:
        """Advance simulation by 1 day applying candidate actions with realistic market responses."""
        self.current_day += 1
        action = np.clip(action, -1.0, 1.0)

        # 1. Apply Channel Allocation Adjustments
        raw_deltas = action[:3] * 0.15  # Max 15% shift per step
        new_alloc = self.channel_allocations + raw_deltas
        new_alloc = np.clip(new_alloc, 0.05, 0.85)  # Enforce minimum channel diversity bounds
        self.channel_allocations = new_alloc / np.sum(new_alloc)  # Re-normalize to 1.0

        # 2. Apply Bid Multiplier (mapping [-1, 1] to [0.80, 1.20])
        bid_delta = float(action[3]) * 0.10
        self.bid_multiplier = float(np.clip(self.bid_multiplier + bid_delta, 0.70, 1.40))

        # 3. Creative Refresh / Fatigue Dynamics
        creative_refresh = bool(action[4] > 0.3)
        if creative_refresh:
            self.creative_fatigue = max(0.05, self.creative_fatigue - 0.35)
        else:
            self.creative_fatigue = min(0.95, self.creative_fatigue + 0.03)

        # 4. Simulate Daily Channel Performance & Auction Dynamics
        daily_target_budget = (self.total_budget / self.duration_days)
        noise = float(self._rng.normal(0.0, 0.05))

        daily_spend = 0.0
        daily_clicks = 0
        daily_impressions = 0
        daily_conversions = 0
        daily_revenue = 0.0

        fatigue_penalty = 1.0 - (0.40 * self.creative_fatigue)

        for i, profile in enumerate(self.channel_profiles):
            alloc_weight = float(self.channel_allocations[i])
            channel_spend = daily_target_budget * alloc_weight

            effective_cpc = profile["base_cpc"] * (self.bid_multiplier ** profile["elasticity"])
            channel_clicks = int(channel_spend / max(0.1, effective_cpc))
            channel_ctr = self.target_ctr * (1.0 + (self.bid_multiplier - 1.0) * 0.2) * fatigue_penalty + noise
            channel_ctr = max(0.5, channel_ctr)
            channel_impressions = int(channel_clicks / (channel_ctr / 100.0))

            effective_cvr = profile["base_cvr"] * fatigue_penalty * (1.0 + noise)
            channel_conversions = int(channel_clicks * effective_cvr)

            # Revenue per conversion (AOV / LTV proxy)
            aov = self.target_cpa * self.target_roas
            channel_revenue = channel_conversions * aov * (1.0 + noise)

            daily_spend += channel_spend
            daily_clicks += channel_clicks
            daily_impressions += channel_impressions
            daily_conversions += channel_conversions
            daily_revenue += channel_revenue

        self.total_spent += daily_spend
        self.cumulative_revenue += daily_revenue
        self.cumulative_conversions += daily_conversions
        self.cumulative_clicks += daily_clicks
        self.cumulative_impressions += daily_impressions

        # Update running metrics
        self.current_roas = daily_revenue / max(1.0, daily_spend)
        self.current_cpa = daily_spend / max(1, daily_conversions)
        self.current_ctr = (daily_clicks / max(1, daily_impressions)) * 100.0

        # 5. Multi-Objective Reward Formulation
        # R = w_roas * (ROAS / Target_ROAS) + w_conv * norm_conv + w_rev * (Rev / Spend) - w_cpa * cpa_penalty - constraint_penalty
        roas_score = float(self.current_roas / max(0.1, self.target_roas))
        rev_score = float(daily_revenue / max(1.0, daily_spend * self.target_roas))
        cpa_penalty = float(max(0.0, (self.current_cpa - self.target_cpa) / max(1.0, self.target_cpa)))
        conv_score = float(daily_conversions / 15.0)

        reward = float(1.2 * roas_score + 0.8 * rev_score + 0.6 * conv_score - 1.0 * cpa_penalty)

        # Terminate when days reached or budget exhausted
        terminated = bool(self.current_day >= self.duration_days or self.total_spent >= self.total_budget * 1.05)
        truncated = False

        obs = self._get_observation()
        info = {
            "day": self.current_day,
            "daily_spend": daily_spend,
            "daily_revenue": daily_revenue,
            "daily_conversions": daily_conversions,
            "cumulative_conversions": self.cumulative_conversions,
            "current_roas": self.current_roas,
            "current_cpa": self.current_cpa,
            "current_ctr": self.current_ctr,
            "cumulative_revenue": self.cumulative_revenue,
            "total_spent": self.total_spent,
            "channel_allocations": self.channel_allocations.tolist(),
            "bid_multiplier": self.bid_multiplier,
            "creative_fatigue": self.creative_fatigue,
        }
        return obs, reward, terminated, truncated, info
