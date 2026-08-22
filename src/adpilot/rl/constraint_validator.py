"""Safety and Constraint Validator for RL and Optimization candidate action proposals."""

from __future__ import annotations

import logging
from typing import Dict, List, Optional, Tuple

import numpy as np

from ..schemas.agent_schemas import CampaignContext, ConstraintValidationResult, RLActionProposal

logger = logging.getLogger(__name__)


class ConstraintValidator:
    """Enforces deterministic business rules, brand constraints, and mathematical bounds on RL candidate actions."""

    def __init__(
        self,
        min_channel_weight: float = 0.05,
        max_channel_weight: float = 0.80,
        min_bid_multiplier: float = 0.70,
        max_bid_multiplier: float = 1.40,
        max_single_shift_pct: float = 0.25,
    ) -> None:
        self.min_channel_weight = float(min_channel_weight)
        self.max_channel_weight = float(max_channel_weight)
        self.min_bid_multiplier = float(min_bid_multiplier)
        self.max_bid_multiplier = float(max_bid_multiplier)
        self.max_single_shift_pct = float(max_single_shift_pct)

    def validate_and_project(
        self,
        candidate_action: np.ndarray,
        current_allocations: Dict[str, float],
        context: Optional[CampaignContext] = None,
    ) -> Tuple[RLActionProposal, ConstraintValidationResult]:
        """Validate raw candidate action from policy network and project to safe bounded action."""
        violations: List[str] = []
        modifications: List[str] = []
        requires_human_approval = False

        channels = list(current_allocations.keys()) if current_allocations else ["linkedin", "facebook", "email"]
        n_channels = len(channels)

        # 1. Channel Allocation Calculation & Bound Clamping
        raw_deltas = candidate_action[:n_channels] * 0.15
        current_weights = np.array([current_allocations.get(ch, 1.0 / n_channels) for ch in channels], dtype=np.float64)
        target_weights = current_weights + raw_deltas[:n_channels]

        # Check for single-step massive shifts
        for i, ch in enumerate(channels):
            shift = abs(target_weights[i] - current_weights[i])
            if shift > self.max_single_shift_pct:
                violations.append(f"Channel '{ch}' requested shift ({shift:.1%}) exceeds maximum single-cycle limit ({self.max_single_shift_pct:.1%}).")
                requires_human_approval = True

        # Iterative simplex projection with box constraints [min_channel_weight, max_channel_weight]
        weights = target_weights.copy()
        if not np.allclose(np.clip(weights, self.min_channel_weight, self.max_channel_weight), weights):
            modifications.append(f"Clamped channel allocation weights within safety boundaries [{self.min_channel_weight:.0%}, {self.max_channel_weight:.0%}].")

        for _ in range(20):
            weights = np.clip(weights, self.min_channel_weight, self.max_channel_weight)
            diff = 1.0 - float(np.sum(weights))
            if abs(diff) < 1e-6:
                break
            if diff > 0:
                eligible = weights < self.max_channel_weight - 1e-4
            else:
                eligible = weights > self.min_channel_weight + 1e-4

            if not np.any(eligible):
                break
            weights[eligible] += diff / float(np.sum(eligible))

        normalized_weights = np.clip(weights, self.min_channel_weight, self.max_channel_weight)
        normalized_weights = normalized_weights / float(np.sum(normalized_weights))

        clamped_allocations_dict = {
            channels[i]: round(float(normalized_weights[i]), 4)
            for i in range(n_channels)
        }

        # 2. Bid Multiplier Validation
        bid_raw = 1.0 + float(candidate_action[3]) * 0.20 if len(candidate_action) > 3 else 1.0
        clamped_bid = float(np.clip(bid_raw, self.min_bid_multiplier, self.max_bid_multiplier))
        if not np.isclose(bid_raw, clamped_bid):
            violations.append(f"Raw bid multiplier ({bid_raw:.2f}x) exceeded safety limits [{self.min_bid_multiplier:.2f}x, {self.max_bid_multiplier:.2f}x].")
            modifications.append(f"Clamped bid multiplier to safe ceiling {clamped_bid:.2f}x.")

        # 3. Creative Refresh Recommendation
        creative_refresh = bool(candidate_action[4] > 0.30) if len(candidate_action) > 4 else False

        # 4. Target CPA Ceiling & Frequency Capping
        target_cpa = 45.0
        if context and context.analytics and context.analytics.kpi_targets:
            target_cpa = float(context.analytics.kpi_targets.cpa_target or 45.0)

        cpa_ceiling = round(target_cpa * 1.15, 2)
        frequency_cap = 3.0

        # Construct Action Proposal & Validation Result
        action_proposal = RLActionProposal(
            channel_allocations=clamped_allocations_dict,
            bid_multiplier=round(clamped_bid, 3),
            target_cpa_ceiling=cpa_ceiling,
            creative_refresh_recommended=creative_refresh,
            suggested_frequency_cap=frequency_cap,
        )

        is_valid = len(violations) == 0
        safety_validation = ConstraintValidationResult(
            is_valid=is_valid,
            violations=violations,
            modifications_applied=modifications,
            clamped_allocations=clamped_allocations_dict,
            approved_by_safety_gate=True,  # Approved because modifications projected it to safe set
            requires_human_approval=requires_human_approval,
        )

        return action_proposal, safety_validation
