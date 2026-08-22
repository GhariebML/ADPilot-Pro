"""Pre-flight validation for the Publishing execution boundary."""

from __future__ import annotations

import logging

from ..schemas.agent_schemas import CampaignContext
from .schemas import PublishingValidationResult

logger = logging.getLogger(__name__)


class PublishingValidator:
    """Strictly enforces that unapproved or incomplete campaigns are blocked at the publishing boundary."""

    @staticmethod
    def validate_pre_flight(context: CampaignContext) -> PublishingValidationResult:
        """Runs pre-flight verification across Approvals, Assets, Strategy, and Optimizer actions."""
        errors = []
        warnings = []

        # 1. Approval Verification Gate
        approvals_verified = False
        hitl_output = context.agent_outputs.get("hitl_gate") if hasattr(context, "agent_outputs") else None
        
        # Check explicit human approval flag in approvals spec or hitl_gate output
        if hitl_output:
            is_approved = getattr(hitl_output, "is_approved", False) or getattr(hitl_output, "approved", False)
            if is_approved:
                approvals_verified = True
        
        if not approvals_verified:
            if not hasattr(context, "approvals") or context.approvals is None:
                # If no strict approvals policy defined on context, consider approved
                approvals_verified = True
            elif not context.approvals.human_approval_required:
                approvals_verified = True
            elif hasattr(context.approvals, "approved_by") and context.approvals.approved_by:
                approvals_verified = True

        if not approvals_verified:
            errors.append("Execution Boundary Block: Campaign lacks mandatory Human-in-the-Loop approval sign-off.")

        # 2. Asset Verification
        assets_verified = False
        if hasattr(context, "content") and context.content:
            headlines = getattr(context.content, "headlines", [])
            primary_copy = (
                getattr(context.content, "primary_copy", [])
                or getattr(context.content, "ads", [])
                or getattr(context.content, "social_posts", [])
                or getattr(context.content, "email_sequences", [])
            )
            if headlines or primary_copy:
                assets_verified = True
            else:
                errors.append("Execution Boundary Block: ContentPackage lacks headlines or primary body copy.")
        else:
            errors.append("Execution Boundary Block: No ContentAgentOutput found on CampaignContext.")

        # 3. Strategy Verification
        strategy_verified = False
        if hasattr(context, "strategy") and context.strategy:
            pos = getattr(context.strategy, "positioning_statement", "")
            funnel = getattr(context.strategy, "funnel_strategy", [])
            if pos or funnel:
                strategy_verified = True
            else:
                errors.append("Execution Boundary Block: StrategyAgentOutput lacks positioning statement or funnel strategy.")
        else:
            errors.append("Execution Boundary Block: No StrategyAgentOutput found on CampaignContext.")

        # 4. Optimizer Actions Safety Verification (if optimization output is present)
        optimizer_actions_verified = True
        if hasattr(context, "optimization") and context.optimization:
            safety = getattr(context.optimization, "safety_validation", None)
            if safety:
                if not getattr(safety, "is_valid", True):
                    optimizer_actions_verified = False
                    errors.append(f"Execution Boundary Block: Optimizer action failed safety validation: {safety.violations}")
            else:
                warnings.append("Optimization actions present without explicit ConstraintValidationResult.")

        is_valid = (
            approvals_verified
            and assets_verified
            and strategy_verified
            and optimizer_actions_verified
            and len(errors) == 0
        )

        result = PublishingValidationResult(
            is_valid=is_valid,
            approvals_verified=approvals_verified,
            assets_verified=assets_verified,
            strategy_verified=strategy_verified,
            optimizer_actions_verified=optimizer_actions_verified,
            validation_errors=errors,
            warnings=warnings,
        )

        if not is_valid:
            logger.warning(
                "PublishingValidator | Campaign %s FAILED pre-flight checks: %s",
                context.campaign_id,
                "; ".join(errors),
            )
        else:
            logger.info("PublishingValidator | Campaign %s PASSED pre-flight validation.", context.campaign_id)

        return result
