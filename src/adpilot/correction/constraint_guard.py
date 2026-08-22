"""Constraint Guard: Enforces CampaignContext and CampaignConstraints immutability during corrections."""

from __future__ import annotations

import copy
import logging
from typing import Any, Dict, List, Tuple

from ..schemas.agent_schemas import CampaignContext

logger = logging.getLogger(__name__)


class ConstraintGuard:
    """Safeguards CampaignContext invariants against unauthorized mutations during correction cycles."""

    @staticmethod
    def snapshot_invariants(context: CampaignContext) -> Dict[str, Any]:
        """Capture deep snapshot of core business identity and constraint fields."""
        return {
            "campaign_id": context.campaign_id,
            "business_name": context.business.name if hasattr(context, "business") and context.business else None,
            "product_name": context.product.name if hasattr(context, "product") and context.product else None,
            "total_budget": float(context.budget.total_budget) if hasattr(context, "budget") and context.budget else None,
            "currency": context.budget.currency if hasattr(context, "budget") and context.budget else None,
            "brand_colors": list(context.brand.brand_colors) if hasattr(context, "brand") and context.brand and context.brand.brand_colors else [],
            "target_countries": list(context.geography.target_countries) if hasattr(context, "geography") and context.geography else [],
            "duration_days": context.timeline.duration_days if hasattr(context, "timeline") and context.timeline else None,
        }

    @staticmethod
    def verify_invariants(
        baseline_snapshot: Dict[str, Any],
        updated_context: CampaignContext,
    ) -> Tuple[bool, List[str]]:
        """Verify that an updated CampaignContext preserved all baseline invariants."""
        violations: List[str] = []

        # 1. Immutable Campaign ID
        if updated_context.campaign_id != baseline_snapshot["campaign_id"]:
            violations.append(
                f"Campaign ID mutated: expected '{baseline_snapshot['campaign_id']}', got '{updated_context.campaign_id}'."
            )

        # 2. Immutable Business Name
        if hasattr(updated_context, "business") and updated_context.business:
            if updated_context.business.name != baseline_snapshot["business_name"]:
                violations.append(
                    f"Business name mutated: expected '{baseline_snapshot['business_name']}', got '{updated_context.business.name}'."
                )

        # 3. Immutable Total Budget & Currency
        if hasattr(updated_context, "budget") and updated_context.budget:
            current_budget = float(updated_context.budget.total_budget)
            if baseline_snapshot["total_budget"] is not None and abs(current_budget - baseline_snapshot["total_budget"]) > 1e-4:
                violations.append(
                    f"Total budget mutated: expected {baseline_snapshot['total_budget']}, got {current_budget}."
                )
            if updated_context.budget.currency != baseline_snapshot["currency"]:
                violations.append(
                    f"Budget currency mutated: expected '{baseline_snapshot['currency']}', got '{updated_context.budget.currency}'."
                )

        # 4. Immutable Brand Colors
        if hasattr(updated_context, "brand") and updated_context.brand and baseline_snapshot["brand_colors"]:
            current_colors = list(updated_context.brand.brand_colors or [])
            if current_colors != baseline_snapshot["brand_colors"]:
                violations.append(
                    f"Brand colors mutated: expected {baseline_snapshot['brand_colors']}, got {current_colors}."
                )

        # 5. Immutable Timeline Duration
        if hasattr(updated_context, "timeline") and updated_context.timeline and baseline_snapshot["duration_days"]:
            if updated_context.timeline.duration_days != baseline_snapshot["duration_days"]:
                violations.append(
                    f"Campaign duration mutated: expected {baseline_snapshot['duration_days']} days, got {updated_context.timeline.duration_days} days."
                )

        is_valid = len(violations) == 0
        if not is_valid:
            logger.error("ConstraintGuard detected invariant violations: %s", violations)
        return is_valid, violations

    @staticmethod
    def restore_invariants(
        target_context: CampaignContext,
        baseline_snapshot: Dict[str, Any],
    ) -> CampaignContext:
        """Restores core invariant fields if an agent inadvertently modified them."""
        context = copy.deepcopy(target_context)
        if hasattr(context, "business") and context.business and baseline_snapshot["business_name"]:
            context.business.name = baseline_snapshot["business_name"]
        if hasattr(context, "budget") and context.budget and baseline_snapshot["total_budget"] is not None:
            context.budget.total_budget = baseline_snapshot["total_budget"]
            context.budget.currency = baseline_snapshot["currency"]
        if hasattr(context, "brand") and context.brand and baseline_snapshot["brand_colors"]:
            context.brand.brand_colors = baseline_snapshot["brand_colors"]
        if hasattr(context, "timeline") and context.timeline and baseline_snapshot["duration_days"]:
            context.timeline.duration_days = baseline_snapshot["duration_days"]
        return context
