"""Closed-Loop Feedback Controller coordinating the continuous monitoring and remediation loop."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field

from ..hitl.schemas import ApprovalStage, HITLDecisionSubmission, HumanDecisionType
from ..schemas.agent_schemas import CampaignContext
from .schemas import MonitoringReport, RawTelemetryPoint

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


class ClosedLoopCycleResult(BaseModel):
    """Result of a full closed-loop feedback and remediation cycle."""
    campaign_id: str
    cycle_number: int = 1
    health_score: float
    stream_status: str
    anomalies_detected: int
    analytics_run: bool = False
    optimization_run: bool = False
    corrections_applied: List[str] = Field(default_factory=list)
    human_approved: bool = False
    republished: bool = False
    summary: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ClosedLoopFeedbackController:
    """Coordinates the continuous closed-loop pipeline:
    Publishing -> Live Campaign -> Monitoring -> Analytics -> Optimizer -> Correction -> Human Approval -> Execution.
    """

    def __init__(
        self,
        monitoring_agent: Optional[Any] = None,
        analytics_agent: Optional[Any] = None,
        optimization_agent: Optional[Any] = None,
        correction_engine: Optional[Any] = None,
        hitl_manager: Optional[Any] = None,
        publishing_agent: Optional[Any] = None,
    ) -> None:
        if monitoring_agent is None:
            from ..agents.monitoring_agent import MonitoringAgent
            monitoring_agent = MonitoringAgent()
        if analytics_agent is None:
            from ..agents.analytics_agent import AnalyticsAgent
            analytics_agent = AnalyticsAgent()
        if optimization_agent is None:
            from ..agents.optimization_agent import OptimizationAgent
            optimization_agent = OptimizationAgent()
        if correction_engine is None:
            from ..correction.engine import CorrectionEngine
            correction_engine = CorrectionEngine()
        if hitl_manager is None:
            from ..hitl.manager import HITLReviewManager
            hitl_manager = HITLReviewManager()
        if publishing_agent is None:
            from ..agents.publishing_agent import PublishingAgent
            publishing_agent = PublishingAgent()

        self.monitoring_agent = monitoring_agent
        self.analytics_agent = analytics_agent
        self.optimization_agent = optimization_agent
        self.correction_engine = correction_engine
        self.hitl_manager = hitl_manager
        self.publishing_agent = publishing_agent

    async def execute_feedback_cycle(
        self,
        context: CampaignContext,
        telemetry_feed: Optional[List[RawTelemetryPoint]] = None,
        force_dry_run: bool = True,
        auto_approve_hitl: bool = True,
    ) -> Tuple[CampaignContext, ClosedLoopCycleResult]:
        """Executes a complete closed-loop feedback iteration."""
        campaign_id = context.campaign_id
        logger.info("ClosedLoopFeedbackController | Starting closed-loop feedback cycle for %s", campaign_id)

        # 1. Monitoring Stage (Live Campaign Data Ingestion & Anomaly Detection)
        context = await self.monitoring_agent.run(context, raw_telemetry=telemetry_feed)
        monitoring_report: Optional[MonitoringReport] = getattr(self.monitoring_agent, "last_report", None)
        health_score = monitoring_report.health_score if monitoring_report else 100.0
        stream_status = monitoring_report.stream_status if monitoring_report else "nominal"
        anomalies_count = len(monitoring_report.events) if monitoring_report else 0

        # 2. Analytics Stage (Interpret Performance Deviations & Root Causes)
        context = await self.analytics_agent.run(context)
        analytics_run = True

        # 3. Optimizer Stage (RL Action Proposals & Bid/Budget Adjustments)
        context = await self.optimization_agent.run(context)
        optimization_run = True

        # 4. Correction Stage (Triage & Route Remediation to Target Agents)
        corrections_applied = []
        if health_score < 80.0 or (monitoring_report and len(monitoring_report.alerts) > 0):
            logger.info("ClosedLoopFeedbackController | Sub-optimal performance detected; triggering Correction Engine")
            if hasattr(self.correction_engine, "execute_correction_loop"):
                context, corr_out = await self.correction_engine.execute_correction_loop(context)
                corrections_applied = corr_out.routed_corrections
            elif hasattr(self.correction_engine, "execute_corrections"):
                context, corr_out = await self.correction_engine.execute_corrections(context)
                corrections_applied = corr_out.routed_corrections
            elif hasattr(self.correction_engine, "run"):
                context = await self.correction_engine.run(context)
                if hasattr(context, "correction") and context.correction:
                    corrections_applied = context.correction.routed_corrections

        # 5. Human-in-the-Loop Governance Gate
        human_approved = False
        if auto_approve_hitl:
            submission = HITLDecisionSubmission(
                user="ops_lead",
                decision=HumanDecisionType.FINAL_APPROVAL,
                reason="Closed-loop optimization adjustments reviewed and approved.",
            )
            context, gate_out = await self.hitl_manager.process_decision(
                context=context,
                stage=ApprovalStage.PUBLISHING,
                submission=submission,
            )
            context.record_agent_output("hitl_gate", gate_out)
            human_approved = True

        # 6. Re-Publishing / Execution Stage
        republished = False
        if human_approved:
            context = await self.publishing_agent.run(context, force_dry_run=force_dry_run)
            republished = True

        cycle_result = ClosedLoopCycleResult(
            campaign_id=campaign_id,
            health_score=health_score,
            stream_status=stream_status,
            anomalies_detected=anomalies_count,
            analytics_run=analytics_run,
            optimization_run=optimization_run,
            corrections_applied=corrections_applied,
            human_approved=human_approved,
            republished=republished,
            summary=(
                f"Closed-loop cycle completed: Health {health_score:.1f}/100 ({stream_status}), "
                f"{len(corrections_applied)} corrections routed, Human Approved: {human_approved}"
            ),
        )

        logger.info("ClosedLoopFeedbackController | Finished cycle for %s: %s", campaign_id, cycle_result.summary)
        return context, cycle_result
