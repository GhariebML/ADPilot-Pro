"""Master Pipeline Orchestrator for Phase 4.

Executes the frozen Master Pipeline according to the ExecutionPlan with explicit state transitions,
traceability, timeouts, retries, optional agent skipping, HITL approval points, and quality gate correction loops.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timezone
from typing import Any, Awaitable, Callable, Dict, List, Optional, Set, Tuple

from ..agents.analytics_agent import AnalyticsAgent
from ..agents.audience_agent import AudienceAgent
from ..agents.campaign_manager_agent import CampaignManagerAgent
from ..agents.competitor_agent import CompetitorAgent
from ..agents.content_agent import ContentAgent
from ..agents.correction_agent import CorrectionAgent
from ..agents.cv_agent import CVAgent
from ..agents.design_agent import DesignAgent
from ..agents.monitoring_agent import MonitoringAgent
from ..agents.optimization_agent import OptimizationAgent
from ..agents.publishing_agent import PublishingAgent
from ..agents.research_agent import ResearchAgent
from ..agents.strategy_agent import StrategyAgent
from ..core.exceptions import AgentExecutionError
from ..hitl.manager import HITLReviewManager
from ..hitl.schemas import (
    ApprovalStage,
    HITLDecisionSubmission,
    HITLGateOutput,
    HumanDecisionType,
)
from ..schemas.agent_schemas import (
    AgentRunRecord,
    AgentRunStatus,
    CampaignContext,
)
from ..schemas.execution_plan import (
    ExecutionPlan,
    WorkflowState,
)
from ..services.memory_service import MemoryService
from .planner import CampaignPlanner

logger = logging.getLogger(__name__)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class MasterOrchestrator:
    """Production Master Pipeline Orchestrator enforcing the frozen Master Pipeline sequence."""

    def __init__(
        self,
        memory_service: Optional[MemoryService] = None,
        planner: Optional[CampaignPlanner] = None,
        hitl_manager: Optional[HITLReviewManager] = None,
        custom_agent_runners: Optional[Dict[str, Callable[[CampaignContext], Awaitable[CampaignContext]]]] = None,
    ) -> None:
        self.memory_service = memory_service or MemoryService()
        self.planner = planner or CampaignPlanner()
        self.hitl_manager = hitl_manager or HITLReviewManager()
        self.agent_run_records: List[AgentRunRecord] = []
        
        # Default agent registry
        self._strategy_agent = StrategyAgent()
        self._research_agent = ResearchAgent()
        self._audience_agent = AudienceAgent()
        self._competitor_agent = CompetitorAgent()
        self._content_agent = ContentAgent()
        self._design_agent = DesignAgent()
        self._cv_agent = CVAgent()
        self._analytics_agent = AnalyticsAgent()
        self._optimization_agent = OptimizationAgent()
        self._correction_agent = CorrectionAgent()
        self._campaign_manager_agent = CampaignManagerAgent()
        self._publishing_agent = PublishingAgent()
        self._monitoring_agent = MonitoringAgent()

        # Custom runner overrides (useful for mocks/tests)
        self.custom_runners: Dict[str, Callable[[CampaignContext], Awaitable[CampaignContext]]] = (
            custom_agent_runners or {}
        )

    def register_runner(
        self, agent_name: str, runner_fn: Callable[[CampaignContext], Awaitable[CampaignContext]]
    ) -> None:
        """Register or override an agent execution function."""
        self.custom_runners[agent_name] = runner_fn

    async def _dispatch_agent(
        self, agent_name: str, context: CampaignContext
    ) -> CampaignContext:
        """Dispatch execution to the matching agent implementation."""
        if agent_name in self.custom_runners:
            return await self.custom_runners[agent_name](context)

        if agent_name == "strategy_agent":
            return await self._strategy_agent.run(context)
        elif agent_name == "research_agent":
            return await self._research_agent.run(context)
        elif agent_name == "audience_agent":
            return await self._audience_agent.run(context)
        elif agent_name == "competitor_agent":
            return await self._competitor_agent.run(context)
        elif agent_name == "content_agent":
            return await self._content_agent.run(context)
        elif agent_name == "design_agent":
            return await self._design_agent.run(context)
        elif agent_name == "cv_agent":
            return await self._cv_agent.run(context)
        elif agent_name == "analytics_agent":
            return await self._analytics_agent.run(context)
        elif agent_name == "optimization_agent":
            return await self._optimization_agent.run(context)
        elif agent_name in ("correction_engine", "correction_agent"):
            return await self._correction_agent.run(context)
        elif agent_name == "hitl_gate":
            # Human-in-the-loop checkpoint execution and audit logging
            sub = HITLDecisionSubmission(
                user="system_orchestrator",
                decision=HumanDecisionType.FINAL_APPROVAL,
                reason="Master pipeline pre-flight quality verification and final sign-off",
            )
            updated_ctx, gate_out = await self.hitl_manager.process_decision(
                context=context,
                stage=ApprovalStage.PUBLISHING,
                submission=sub,
            )
            updated_ctx.record_agent_output("hitl_gate", gate_out)
            return updated_ctx
        elif agent_name == "publishing_agent":
            return await self._publishing_agent.run(context)
        elif agent_name == "monitoring_agent":
            return await self._monitoring_agent.run(context)
        elif agent_name == "campaign_manager_agent":
            return await self._campaign_manager_agent.run(context)
        else:
            logger.warning("MasterOrchestrator | Unknown agent: %s, passing through.", agent_name)
            return context

    async def submit_hitl_decision(
        self,
        context: CampaignContext,
        stage: ApprovalStage,
        submission: HITLDecisionSubmission,
        db_session: Optional[Any] = None,
    ) -> Tuple[CampaignContext, HITLGateOutput]:
        """Processes a human decision and updates CampaignContext with full non-silent audit logging."""
        return await self.hitl_manager.process_decision(
            context=context,
            stage=stage,
            submission=submission,
            db_session=db_session,
        )

    async def execute_plan(
        self,
        context: CampaignContext,
        plan: Optional[ExecutionPlan] = None,
        skipped_agents: Optional[Set[str]] = None,
        auto_approve_hitl: bool = True,
        max_corrections: int = 2,
    ) -> CampaignContext:
        """Execute all steps in the ExecutionPlan with full state tracking and fault tolerance."""
        active_plan = plan or context.execution_plan or self.planner.plan(context)
        context.execution_plan = active_plan
        active_plan.status = WorkflowState.RUNNING
        skipped_set = skipped_agents or set()

        logger.info(
            "MasterOrchestrator | Executing plan %s for campaign %s (%d steps)",
            active_plan.plan_id,
            context.campaign_id,
            len(active_plan.agent_sequence),
        )

        correction_count = 0
        step_idx = 0

        while step_idx < len(active_plan.agent_sequence):
            step = active_plan.agent_sequence[step_idx]
            active_plan.current_step_index = step_idx

            # 1. Check for skipped optional agent
            if step.is_optional and (step.agent_name in skipped_set or step.agent_name == "cv_agent" and "cv_agent" in skipped_set):
                step.state = WorkflowState.SKIPPED
                step.finished_at = _utc_now()
                step.output_snapshot = {"skipped": True, "reason": "Optional agent skipped by policy"}
                active_plan.completed_steps += 1
                logger.info("MasterOrchestrator | Stage %d: %s is SKIPPED.", step.stage_order, step.agent_name)
                step_idx += 1
                continue

            # 2. Check for Human-in-the-Loop approval point
            if step.approval_point and not auto_approve_hitl:
                step.state = WorkflowState.WAITING_FOR_APPROVAL
                active_plan.status = WorkflowState.WAITING_FOR_APPROVAL
                context.execution_plan = active_plan
                logger.warning(
                    "MasterOrchestrator | Pausing execution at Stage %d (%s) for Human-in-the-Loop approval.",
                    step.stage_order,
                    step.agent_name,
                )
                await self.memory_service.save_context(context.campaign_id, context)
                return context

            # 3. Execute Step with Retries and Timeout Protection
            step.started_at = _utc_now()
            step.state = WorkflowState.RUNNING
            step_success = False
            last_error: Optional[Exception] = None

            for attempt in range(1, step.max_retries + 1):
                step.attempts = attempt
                if attempt > 1:
                    step.state = WorkflowState.RETRYING
                    backoff = min(2.0, 0.1 * (2 ** (attempt - 1)))
                    logger.info(
                        "MasterOrchestrator | Retrying %s (attempt %d/%d) after %.2fs backoff",
                        step.agent_name,
                        attempt,
                        step.max_retries,
                        backoff,
                    )
                    await asyncio.sleep(backoff)

                try:
                    logger.info("MasterOrchestrator | Running Stage %d: %s (attempt %d)", step.stage_order, step.agent_name, attempt)
                    # Apply step timeout ceiling
                    context = await asyncio.wait_for(
                        self._dispatch_agent(step.agent_name, context),
                        timeout=step.timeout_seconds,
                    )
                    step_success = True
                    step.state = WorkflowState.SUCCESS
                    step.finished_at = _utc_now()
                    step.error_message = None
                    active_plan.completed_steps += 1
                    
                    # Record run record
                    self._record_run(
                        agent_name=step.agent_name,
                        status=AgentRunStatus.success,
                        started_at=step.started_at,
                        finished_at=step.finished_at,
                        attempts=attempt,
                    )
                    await self.memory_service.save_context(context.campaign_id, context)
                    break

                except asyncio.TimeoutError:
                    last_error = TimeoutError(f"Step {step.agent_name} timed out after {step.timeout_seconds}s")
                    logger.warning("MasterOrchestrator | Stage %d: %s TIMED OUT on attempt %d", step.stage_order, step.agent_name, attempt)
                    if attempt >= step.max_retries:
                        step.state = WorkflowState.TIMED_OUT
                except Exception as exc:
                    last_error = exc
                    logger.warning("MasterOrchestrator | Stage %d: %s FAILED on attempt %d: %s", step.stage_order, step.agent_name, attempt, exc)
                    if attempt >= step.max_retries:
                        step.state = WorkflowState.FAILED

            if not step_success:
                step.finished_at = _utc_now()
                step.error_message = str(last_error)
                active_plan.status = WorkflowState.FAILED
                active_plan.failed_steps += 1
                self._record_run(
                    agent_name=step.agent_name,
                    status=AgentRunStatus.failed,
                    started_at=step.started_at,
                    finished_at=step.finished_at,
                    error_message=str(last_error),
                    attempts=step.attempts,
                )
                await self.memory_service.save_context(context.campaign_id, context)
                raise AgentExecutionError(f"Stage {step.stage_order} ({step.agent_name}) failed: {last_error}") from last_error

            # 4. Check for Design-CV Visual Quality Gate & Revision Loop
            if step.agent_name == "cv_agent" and hasattr(context, "agent_outputs") and "cv_agent" in context.agent_outputs:
                cv_out = context.agent_outputs["cv_agent"]
                cv_passed = getattr(cv_out, "passed_quality_gate", True)
                if not cv_passed and correction_count < max_corrections:
                    correction_count += 1
                    logger.warning(
                        "MasterOrchestrator | CV Creative score %.1f < 70.0. Triggering Design-CV revision loop (%d/%d).",
                        getattr(cv_out, "creative_score", 0.0),
                        correction_count,
                        max_corrections,
                    )
                    active_plan.status = WorkflowState.CORRECTING
                    context.creative_revision_notes = getattr(cv_out, "improvement_suggestions", ["Improve contrast and brand palette adherence."])
                    design_idx = next(
                        (i for i, s in enumerate(active_plan.agent_sequence) if s.agent_name == "design_agent"),
                        None,
                    )
                    if design_idx is not None:
                        step_idx = design_idx
                        continue

            # 5. Check for Analytics Quality Gate & Correction Loop
            if step.agent_name == "analytics_agent" and hasattr(context, "analytics") and context.analytics:
                passes_gate = AnalyticsAgent.passes_quality_gate(context.analytics)
                if not passes_gate and correction_count < max_corrections:
                    correction_count += 1
                    logger.warning(
                        "MasterOrchestrator | Quality gate score %.2f < 70.0. Triggering correction loop (%d/%d).",
                        getattr(context.analytics.health_score, "overall", 0.0),
                        correction_count,
                        max_corrections,
                    )
                    active_plan.status = WorkflowState.CORRECTING
                    # Find content_agent index to loop back
                    content_idx = next(
                        (i for i, s in enumerate(active_plan.agent_sequence) if s.agent_name == "content_agent"),
                        None,
                    )
                    if content_idx is not None:
                        step_idx = content_idx
                        continue

            step_idx += 1

        active_plan.status = WorkflowState.SUCCESS
        context.execution_plan = active_plan
        logger.info(
            "MasterOrchestrator | Successfully completed full pipeline execution for campaign %s (Plan: %s)",
            context.campaign_id,
            active_plan.plan_id,
        )
        return context

    def _record_run(
        self,
        agent_name: str,
        status: AgentRunStatus,
        started_at: str,
        finished_at: str,
        error_message: Optional[str] = None,
        attempts: int = 1,
    ) -> None:
        record = AgentRunRecord(
            agent_name=agent_name,
            status=status,
            started_at=started_at,
            finished_at=finished_at,
            error_message=error_message,
            output_snapshot={"attempts": attempts},
        )
        self.agent_run_records.append(record)
