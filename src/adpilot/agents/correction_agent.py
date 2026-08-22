"""Correction Engine Agent (Phase 11).

Diagnoses campaign defects, identifies responsible agents, synthesizes constraint-preserving
corrective tasks, orchestrates re-execution, and validates problem resolution.
"""

from __future__ import annotations

import logging
import time
from typing import Any, Dict, List, Optional

from ..core.agent_events import AgentEventType
from ..core.base_agent import BaseAgent
from ..core.contract_registry import CORRECTION_AGENT_CONTRACT
from ..correction.engine import CorrectionEngine
from ..correction.schemas import CorrectionTriggerSource
from ..schemas.agent_schemas import (
    CampaignContext,
    CorrectionInput,
    CorrectionOutput,
)

logger = logging.getLogger(__name__)


class CorrectionAgent(BaseAgent[CorrectionInput, CorrectionOutput]):
    """Correction Engine Agent responsible for multi-source defect triage and closed-loop remediation."""

    name = "correction_agent"
    input_model = CorrectionInput
    output_model = CorrectionOutput
    contract = CORRECTION_AGENT_CONTRACT

    def __init__(self, engine: Optional[CorrectionEngine] = None) -> None:
        super().__init__()
        self.engine = engine or CorrectionEngine()

    async def run(
        self,
        context: CampaignContext,
        trigger_source: Optional[CorrectionTriggerSource] = None,
        human_feedback: Optional[str] = None,
        explicit_deviations: Optional[List[Dict[str, Any]]] = None,
        explicit_cv_issues: Optional[List[str]] = None,
        explicit_validation_failures: Optional[List[str]] = None,
        current_attempt: int = 1,
    ) -> CampaignContext:
        """Evaluate campaign health, diagnose defects, and coordinate closed-loop remediation."""
        campaign_id = context.campaign_id
        start_time = time.perf_counter()

        self.emit_event(
            event_type=AgentEventType.AGENT_STARTED,
            campaign_id=campaign_id,
            status="started",
            input_reference="multi_source_diagnostics",
        )

        try:
            # Delegate to enterprise CorrectionEngine
            updated_context, engine_output = await self.engine.execute_correction_loop(
                context=context,
                trigger_source=trigger_source,
                human_feedback=human_feedback,
                explicit_deviations=explicit_deviations,
                explicit_cv_issues=explicit_cv_issues,
                explicit_validation_failures=explicit_validation_failures,
                current_attempt=current_attempt,
            )

            # Convert to schema-compatible CorrectionOutput
            output = CorrectionOutput(
                quality_gate_passed=engine_output.quality_gate_passed,
                requires_correction=engine_output.requires_correction,
                target_agent_to_reinvoke=engine_output.target_agent_to_reinvoke,
                correction_prompt_directives=engine_output.correction_prompt_directives,
                weakness_summary=engine_output.weakness_summary,
                correction_iteration=engine_output.iteration_count,
                identified_problems=[p.model_dump() for p in engine_output.identified_problems],
                responsible_agents=engine_output.responsible_agents,
                corrective_tasks=[t.model_dump() for t in engine_output.corrective_tasks],
                routed_corrections=engine_output.routed_corrections,
                preserves_constraints=engine_output.preserves_constraints,
                evaluations=[e.model_dump() for e in engine_output.evaluations],
                circuit_breaker_triggered=engine_output.circuit_breaker_triggered,
                confidence=engine_output.confidence,
                evidence=engine_output.evidence,
                provenance=engine_output.provenance,
            )

            updated_context.record_agent_output("correction_agent", output)
            latency = time.perf_counter() - start_time

            self.emit_event(
                event_type=AgentEventType.AGENT_COMPLETED,
                campaign_id=campaign_id,
                status="completed",
                output_reference=f"gate_passed={engine_output.quality_gate_passed}, problems={len(engine_output.identified_problems)}",
                confidence=engine_output.confidence,
                latency=latency,
                metadata={
                    "problems_count": len(engine_output.identified_problems),
                    "responsible_agents": engine_output.responsible_agents,
                    "circuit_breaker": engine_output.circuit_breaker_triggered,
                },
            )
            return updated_context

        except Exception as exc:
            latency = time.perf_counter() - start_time
            self.emit_event(
                event_type=AgentEventType.AGENT_FAILED,
                campaign_id=campaign_id,
                status="failed",
                error_message=str(exc),
                latency=latency,
            )
            raise
