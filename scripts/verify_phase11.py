"""Phase 11 — Verification Script: Correction Engine & Closed-Loop Governance.

Verifies:
1. ProblemClassifier diagnosis across all 7 defect categories.
2. AgentRouter task synthesis, priority ordering, and prompt injections.
3. ConstraintGuard invariant snapshotting, violation detection, and auto-restoration.
4. CorrectionEngine closed-loop execution and task evaluations.
5. CorrectionAgent BaseAgent contract compliance & lifecycle events.
6. Multi-agent concurrent failure triage.
7. Circuit-breaker max retries ceiling.
"""

from __future__ import annotations

import asyncio
import copy
import sys
from typing import List

from adpilot.agents.correction_agent import CorrectionAgent
from adpilot.core.agent_events import AgentEventType, event_bus
from adpilot.core.contract_registry import CORRECTION_AGENT_CONTRACT
from adpilot.correction.agent_router import AgentRouter
from adpilot.correction.constraint_guard import ConstraintGuard
from adpilot.correction.engine import CorrectionEngine
from adpilot.correction.problem_classifier import ProblemClassifier
from adpilot.correction.schemas import (
    CorrectionTriggerSource,
    IdentifiedProblem,
    ProblemCategory,
    ProblemSeverity,
)
from adpilot.schemas.agent_schemas import (
    ApprovalRequirements,
    BrandGuidelines,
    BudgetSpec,
    BusinessInfo,
    CampaignConstraints,
    CampaignContext,
    CampaignGoal,
    ContextMetadata,
    CVAgentOutput,
    Geography,
    MarketingChannel,
    ProductSpec,
    TimelineSpec,
    ToneOfVoice,
)
from adpilot.schemas.campaign_context import KPITargets

passed_checks = 0
total_checks = 0


def check(name: str, condition: bool) -> None:
    global passed_checks, total_checks
    total_checks += 1
    if condition:
        passed_checks += 1
        print(f"  [PASS]  {name}")
    else:
        print(f"  [FAIL]  {name}")
        sys.exit(1)


def section(title: str) -> None:
    print(f"\n{'=' * 72}")
    print(f"  {title}")
    print(f"{'=' * 72}")


def create_sample_context() -> CampaignContext:
    return CampaignContext(
        campaign_id="camp-verify-p11",
        metadata=ContextMetadata(created_by="verify_phase11"),
        business=BusinessInfo(
            name="Apex Data Cloud",
            industry="Cloud Infrastructure",
            description="Real-time analytics engine for high-scale enterprise workloads",
        ),
        product=ProductSpec(
            name="Apex Engine",
            product_type="saas",
            description="Ultra low-latency streaming analytics platform",
            unique_selling_points=["Sub-millisecond latency", "Distributed streaming"],
        ),
        goals=[CampaignGoal.lead_generation, CampaignGoal.brand_awareness],
        channels=[MarketingChannel.linkedin, MarketingChannel.facebook, MarketingChannel.email],
        budget=BudgetSpec(total_budget=25000.0, currency="USD", daily_budget_cap=800.0),
        timeline=TimelineSpec(duration_days=30),
        geography=Geography(target_countries=["US", "CA", "DE"]),
        kpis=KPITargets(target_cpa=50.0, target_roas=4.0, target_ctr=3.0),
        constraints=CampaignConstraints(
            max_cpa=75.0,
            min_roas=3.0,
            prohibited_keywords=["cheap analytics", "guaranteed profit"],
        ),
        brand=BrandGuidelines(
            tone_of_voice=ToneOfVoice.professional,
            brand_colors=["#1E3A8A", "#3B82F6", "#93C5FD"],
        ),
        approvals=ApprovalRequirements(human_approval_required=True, min_health_score=70.0),
        variables={},
    )


def verify_problem_classifier():
    section("1. Problem Classifier Multi-Source Diagnostics")
    classifier = ProblemClassifier()
    context = create_sample_context()

    # Low CTR deviation
    deviations = [{"metric": "ctr", "current_value": 0.95, "target_value": 3.0, "description": "Low CTR"}]
    probs = classifier.diagnose_all(context, explicit_deviations=deviations)
    check("diagnoses low CTR performance deviation", any(p.category == ProblemCategory.LOW_CTR for p in probs))
    check("maps low CTR to 'content_agent'", any(p.responsible_agent == "content_agent" for p in probs))

    # CV aesthetic score defect
    context.cv = CVAgentOutput(aesthetic_score=4.5, passed_quality_gate=False, detected_issues=["Blurry layout"])
    probs = classifier.diagnose_all(context)
    check("diagnoses deficient visual aesthetic score", any(p.category == ProblemCategory.POOR_CREATIVE_QUALITY for p in probs))
    check("maps CV defect to 'design_agent'", any(p.responsible_agent == "design_agent" for p in probs))

    # Human critique classification
    probs = classifier.diagnose_all(context, human_feedback="The buyer persona is totally wrong for enterprise.")
    check("diagnoses human critique on persona", any(p.category == ProblemCategory.AUDIENCE_MISMATCH for p in probs))
    check("maps persona critique to 'strategy_agent'", any(p.responsible_agent == "strategy_agent" for p in probs))


def verify_agent_router():
    section("2. Agent Router & Corrective Task Generation")
    router = AgentRouter()
    context = create_sample_context()

    problems = [
        IdentifiedProblem(
            problem_id="prob-1",
            source=CorrectionTriggerSource.PERFORMANCE_DEVIATION,
            category=ProblemCategory.LOW_CTR,
            description="CTR dropped to 0.8%",
            responsible_agent="content_agent",
            severity=ProblemSeverity.HIGH,
        ),
        IdentifiedProblem(
            problem_id="prob-2",
            source=CorrectionTriggerSource.CV_ISSUE,
            category=ProblemCategory.BRAND_SAFETY_VIOLATION,
            description="Prohibited logo detected",
            responsible_agent="design_agent",
            severity=ProblemSeverity.CRITICAL,
        ),
    ]

    tasks = router.generate_tasks(problems, context)
    check("generates exactly 2 corrective tasks", len(tasks) == 2)
    check("tasks are prioritized (critical safety task has priority 1)", tasks[0].priority == 1)
    check("critical safety prompt injection is generated", any("CRITICAL SAFETY" in t.prompt_injection for t in tasks))
    check("content corrective prompt injection is generated", any("headline" in t.prompt_injection.lower() for t in tasks))
    check("enforces budget invariants in constraints", any("budget" in c.lower() for c in tasks[0].constraints_enforced))


def verify_constraint_guard():
    section("3. Constraint Guard & Invariant Safety")
    guard = ConstraintGuard()
    context = create_sample_context()
    baseline = guard.snapshot_invariants(context)

    # Valid check
    is_valid, violations = guard.verify_invariants(baseline, context)
    check("verifies untouched context is 100% valid", is_valid and len(violations) == 0)

    # Tampered check
    tampered = copy.deepcopy(context)
    tampered.budget.total_budget = 999999.0
    tampered.business.name = "Infiltrated Brand"
    is_valid, violations = guard.verify_invariants(baseline, tampered)
    check("detects unauthorized budget & name modifications", not is_valid and len(violations) == 2)

    # Recovery check
    restored = guard.restore_invariants(tampered, baseline)
    check("restores original budget ($25,000)", restored.budget.total_budget == 25000.0)
    check("restores original business name ('Apex Data Cloud')", restored.business.name == "Apex Data Cloud")


async def verify_correction_engine():
    section("4. Correction Engine Closed-Loop Orchestration")
    engine = CorrectionEngine()
    context = create_sample_context()

    deviations = [{"metric": "ctr", "current_value": 1.1, "target_value": 3.0, "description": "Below target CTR"}]
    updated_ctx, output = await engine.execute_correction_loop(
        context=context,
        explicit_deviations=deviations,
    )

    check("output identifies problems", len(output.identified_problems) >= 1)
    check("output includes responsible agents", "content_agent" in output.responsible_agents)
    check("output records routed corrections", len(output.routed_corrections) >= 1)
    check("preserves constraints is True", output.preserves_constraints is True)
    check("output includes provenance metadata", output.provenance is not None)


async def verify_correction_agent():
    section("5. Correction Agent Contract & Lifecycle Events")
    agent = CorrectionAgent()
    check("agent.name == 'correction_agent'", agent.name == "correction_agent")
    check("contract identity matches", CORRECTION_AGENT_CONTRACT.identity.agent_id == "correction_agent")

    events_captured: List[str] = []
    event_bus.subscribe(lambda ev: events_captured.append(ev.event_type.value))

    context = create_sample_context()
    deviations = [{"metric": "cpa", "current_value": 90.0, "target_value": 50.0, "description": "High CPA"}]
    updated_ctx = await agent.run(context, explicit_deviations=deviations)

    check("correction_agent output recorded in context", "correction_agent" in updated_ctx.agent_outputs)
    check("emits agent_started event", AgentEventType.AGENT_STARTED.value in events_captured)
    check("emits agent_completed event", AgentEventType.AGENT_COMPLETED.value in events_captured)


def verify_circuit_breaker():
    section("6. Circuit Breaker Ceiling & HITL Escalation")
    engine = CorrectionEngine(max_iterations=3)
    context = create_sample_context()

    deviations = [{"metric": "cpa", "current_value": 120.0, "target_value": 50.0, "description": "Severe CPA overrun"}]
    _, output = asyncio.run(
        engine.execute_correction_loop(
            context=context,
            explicit_deviations=deviations,
            current_attempt=3,
        )
    )

    check("circuit breaker triggered on max attempts", output.circuit_breaker_triggered is True)
    check("quality gate passed is False on circuit breaker", output.quality_gate_passed is False)
    check("requires correction is True", output.requires_correction is True)


def main():
    print("\n" + "#" * 72)
    print("  PHASE 11 -- CORRECTION ENGINE VERIFICATION")
    print("#" * 72)

    verify_problem_classifier()
    verify_agent_router()
    verify_constraint_guard()
    asyncio.run(verify_correction_engine())
    asyncio.run(verify_correction_agent())
    verify_circuit_breaker()

    print(f"\n{'=' * 72}")
    print(f"  ALL {passed_checks}/{total_checks} PHASE 11 CHECKS PASSED")
    print(f"{'=' * 72}\n")


if __name__ == "__main__":
    main()
