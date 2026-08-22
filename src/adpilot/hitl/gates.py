"""Stage-specific approval gates and risk assessment."""

from __future__ import annotations

from typing import Any, Dict, Tuple

from ..schemas.agent_schemas import CampaignContext
from .schemas import ApprovalStage, RiskLevel


class HITLGates:
    """Evaluates agent recommendations and prepares stage-specific review packages."""

    @staticmethod
    def extract_stage_recommendation(
        context: CampaignContext,
        stage: ApprovalStage,
    ) -> Tuple[str, Dict[str, Any], RiskLevel, str]:
        """Extracts the agent name, output dictionary, risk tier, and summary for a given approval stage."""
        if stage == ApprovalStage.STRATEGY:
            agent_name = "strategy_agent"
            output = getattr(context, "strategy", None)
            risk = RiskLevel.HIGH
            summary = "Strategy & Channel Allocation Approval"
            payload = output.model_dump() if output and hasattr(output, "model_dump") else (output or {})

        elif stage == ApprovalStage.CONTENT:
            agent_name = "content_agent"
            output = getattr(context, "content", None)
            risk = RiskLevel.MEDIUM
            summary = "Ad Copy, Headlines & Messaging Approval"
            payload = output.model_dump() if output and hasattr(output, "model_dump") else (output or {})

        elif stage == ApprovalStage.CREATIVE:
            agent_name = "design_agent"
            output = getattr(context, "design", None) or getattr(context, "creative", None)
            risk = RiskLevel.MEDIUM
            summary = "Visual Assets, Color Palettes & Diffusion Briefs Approval"
            payload = output.model_dump() if output and hasattr(output, "model_dump") else (output or {})

        elif stage == ApprovalStage.BUDGET_OPTIMIZER:
            agent_name = "optimization_agent"
            output = getattr(context, "optimization", None)
            risk = RiskLevel.CRITICAL
            summary = "RL Budget Allocation & Bid Multiplier Optimization Approval"
            payload = output.model_dump() if output and hasattr(output, "model_dump") else (output or {})

        elif stage == ApprovalStage.PUBLISHING:
            agent_name = "publishing_agent"
            output = getattr(context, "publishing", None)
            risk = RiskLevel.CRITICAL
            summary = "Live Ad Network Deployment & Publication Approval"
            payload = output.model_dump() if output and hasattr(output, "model_dump") else (output or {})

        else:
            agent_name = "unknown_agent"
            payload = {}
            risk = RiskLevel.MEDIUM
            summary = f"Review for {stage.value}"

        return agent_name, payload, risk, summary

    @staticmethod
    def apply_modification_to_context(
        context: CampaignContext,
        stage: ApprovalStage,
        modified_output: Dict[str, Any],
    ) -> CampaignContext:
        """Applies an approved human edit or override directly to the canonical CampaignContext."""
        if stage == ApprovalStage.STRATEGY and hasattr(context, "strategy") and context.strategy:
            for k, v in modified_output.items():
                if hasattr(context.strategy, k):
                    setattr(context.strategy, k, v)
            context.record_agent_output("strategy_agent", context.strategy)

        elif stage == ApprovalStage.CONTENT and hasattr(context, "content") and context.content:
            for k, v in modified_output.items():
                if hasattr(context.content, k):
                    setattr(context.content, k, v)
            context.record_agent_output("content_agent", context.content)

        elif stage == ApprovalStage.CREATIVE and hasattr(context, "design") and context.design:
            for k, v in modified_output.items():
                if hasattr(context.design, k):
                    setattr(context.design, k, v)
            context.record_agent_output("design_agent", context.design)

        elif stage == ApprovalStage.BUDGET_OPTIMIZER and hasattr(context, "optimization") and context.optimization:
            from ..schemas.agent_schemas import RLActionProposal
            for k, v in modified_output.items():
                if k == "action_proposal" and isinstance(v, dict):
                    context.optimization.action_proposal = RLActionProposal(**v)
                elif hasattr(context.optimization, k):
                    setattr(context.optimization, k, v)
            context.record_agent_output("optimization_agent", context.optimization)

        elif stage == ApprovalStage.PUBLISHING and hasattr(context, "publishing") and context.publishing:
            for k, v in modified_output.items():
                if hasattr(context.publishing, k):
                    setattr(context.publishing, k, v)
            context.record_agent_output("publishing_agent", context.publishing)

        return context
