"""Phase 11 — Comprehensive Test Suite for the Correction Engine.

Covers 12 distinct scenarios:
1. Low CTR -> Content Agent
2. Poor Creative Quality (Aesthetic Score < 6.0) -> Design Agent
3. Brand Safety / Policy Violation -> Design Agent
4. Target Audience / Positioning Mismatch -> Strategy Agent
5. High CAC Bottleneck -> Optimization Agent
6. Poor Forecast & Health Score Quality Gate (< 70.0) -> Analytics & Content Agents
7. Invalid RL Action / Safety Bounds Violation -> Optimization Agent
8. Human Rejection Directives -> Target Agent
9. Multiple Concurrent Multi-Agent Failures -> Prioritized Triage
10. Max Retries Exceeded Circuit Breaker -> HITL Escalation
11. Strict Context Invariant Safeguard (ConstraintGuard)
12. Master Orchestrator Stage 9 Integration
"""

from __future__ import annotations

import copy
import pytest

from adpilot.agents.correction_agent import CorrectionAgent
from adpilot.correction.constraint_guard import ConstraintGuard
from adpilot.correction.engine import CorrectionEngine
from adpilot.correction.schemas import (
    CorrectionTriggerSource,
    ProblemCategory,
    ProblemSeverity,
)
from adpilot.orchestrator.master_orchestrator import MasterOrchestrator
from adpilot.schemas.execution_plan import WorkflowState
from adpilot.schemas.campaign_context import KPITargets
from adpilot.schemas.agent_schemas import (
    AnalyticsAgentOutput,
    ApprovalRequirements,
    BrandGuidelines,
    BudgetSpec,
    BusinessInfo,
    CampaignConstraints,
    CampaignContext,
    CampaignGoal,
    CampaignHealthScore,
    ConstraintValidationResult,
    ContextMetadata,
    CVAgentOutput,
    Geography,
    MarketingChannel,
    OptimizationOutput,
    ProductSpec,
    RLActionProposal,
    TimelineSpec,
    ToneOfVoice,
)


@pytest.fixture
def base_campaign_context() -> CampaignContext:
    """Fixture providing a standard typed CampaignContext."""
    return CampaignContext(
        campaign_id="camp-correction-test",
        metadata=ContextMetadata(created_by="test_suite"),
        business=BusinessInfo(
            name="CloudFlow Systems",
            industry="Enterprise Software",
            description="Enterprise workflow and document orchestration platform",
        ),
        product=ProductSpec(
            name="CloudFlow Orchestrator",
            product_type="saas",
            description="AI-native business process engine",
            unique_selling_points=["99.99% uptime", "Zero-code automation"],
        ),
        goals=[CampaignGoal.lead_generation, CampaignGoal.brand_awareness],
        channels=[MarketingChannel.linkedin, MarketingChannel.facebook, MarketingChannel.email],
        budget=BudgetSpec(
            total_budget=15000.0,
            currency="USD",
            daily_budget_cap=500.0,
        ),
        timeline=TimelineSpec(duration_days=30),
        geography=Geography(target_countries=["US", "GB", "DE"]),
        kpis=KPITargets(
            target_cpa=45.0,
            target_roas=3.5,
            target_ctr=2.5,
        ),
        constraints=CampaignConstraints(
            max_cpa=60.0,
            min_roas=2.5,
            prohibited_keywords=["free forever", "unlimited guaranteed"],
        ),
        brand=BrandGuidelines(
            tone_of_voice=ToneOfVoice.professional,
            brand_colors=["#0F2027", "#203A43", "#2C5364"],
        ),
        approvals=ApprovalRequirements(
            human_approval_required=True,
            min_health_score=70.0,
        ),
        variables={},
    )


# ---------------------------------------------------------------------------
# Scenario 1: Low CTR -> Content Agent
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_scenario_1_low_ctr_routes_to_content_agent(base_campaign_context):
    engine = CorrectionEngine()
    
    deviations = [
        {
            "metric": "ctr",
            "current_value": 0.85,
            "target_value": 2.50,
            "description": "Observed CTR (0.85%) is 66% below target benchmark (2.50%).",
        }
    ]

    updated_context, output = await engine.execute_correction_loop(
        context=base_campaign_context,
        trigger_source=CorrectionTriggerSource.PERFORMANCE_DEVIATION,
        explicit_deviations=deviations,
    )

    assert len(output.identified_problems) >= 1
    prob = output.identified_problems[0]
    assert prob.category == ProblemCategory.LOW_CTR
    assert prob.responsible_agent == "content_agent"
    assert "content_agent" in output.responsible_agents
    assert any("headline" in t.prompt_injection.lower() for t in output.corrective_tasks)
    assert output.preserves_constraints is True


# ---------------------------------------------------------------------------
# Scenario 2: Poor Creative Quality (Aesthetic < 6.0) -> Design Agent
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_scenario_2_poor_aesthetic_score_routes_to_design_agent(base_campaign_context):
    engine = CorrectionEngine()
    
    # Attach a deficient CV output
    base_campaign_context.cv = CVAgentOutput(
        aesthetic_score=4.8,  # Below 6.0 threshold
        passed_quality_gate=False,
        detected_issues=["Low visual resolution and lack of clear focal point in hero banner."],
    )

    updated_context, output = await engine.execute_correction_loop(
        context=base_campaign_context,
        trigger_source=CorrectionTriggerSource.CV_ISSUE,
    )

    assert len(output.identified_problems) >= 1
    design_problems = [p for p in output.identified_problems if p.responsible_agent == "design_agent"]
    assert len(design_problems) >= 1
    assert design_problems[0].category == ProblemCategory.POOR_CREATIVE_QUALITY
    assert any("negative prompt" in t.prompt_injection.lower() for t in output.corrective_tasks)


# ---------------------------------------------------------------------------
# Scenario 3: Brand Safety / Prohibited Claim Violation -> Design / Content
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_scenario_3_brand_safety_violation_triggers_critical_directive(base_campaign_context):
    engine = CorrectionEngine()
    
    base_campaign_context.cv = CVAgentOutput(
        aesthetic_score=8.5,
        passed_quality_gate=False,
        detected_issues=["Visual asset contains unauthorized trademark logo and prohibited superlatives."],
        brand_safe=False,
    )

    updated_context, output = await engine.execute_correction_loop(
        context=base_campaign_context,
        trigger_source=CorrectionTriggerSource.CV_ISSUE,
    )

    safety_problems = [p for p in output.identified_problems if p.category == ProblemCategory.BRAND_SAFETY_VIOLATION or p.severity == ProblemSeverity.CRITICAL]
    assert len(safety_problems) >= 1
    assert any("CRITICAL SAFETY" in t.prompt_injection for t in output.corrective_tasks)


# ---------------------------------------------------------------------------
# Scenario 4: Target Audience / Positioning Mismatch -> Strategy Agent
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_scenario_4_audience_mismatch_routes_to_strategy_agent(base_campaign_context):
    engine = CorrectionEngine()

    human_critique = "The target market positioning misses enterprise IT directors and focuses too much on junior devs."

    updated_context, output = await engine.execute_correction_loop(
        context=base_campaign_context,
        trigger_source=CorrectionTriggerSource.HUMAN_REJECTION,
        human_feedback=human_critique,
    )

    strat_problems = [p for p in output.identified_problems if p.responsible_agent == "strategy_agent"]
    assert len(strat_problems) >= 1
    assert strat_problems[0].category == ProblemCategory.AUDIENCE_MISMATCH
    assert any(t.target_agent == "strategy_agent" for t in output.corrective_tasks)


# ---------------------------------------------------------------------------
# Scenario 5: High CAC Bottleneck -> Optimization Agent
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_scenario_5_high_cac_routes_to_optimizer(base_campaign_context):
    engine = CorrectionEngine()

    deviations = [
        {
            "metric": "cpa",
            "current_value": 82.50,
            "target_value": 45.00,
            "description": "Observed customer acquisition cost ($82.50) exceeds maximum ceiling ($60.00).",
        }
    ]

    updated_context, output = await engine.execute_correction_loop(
        context=base_campaign_context,
        trigger_source=CorrectionTriggerSource.PERFORMANCE_DEVIATION,
        explicit_deviations=deviations,
    )

    cac_problems = [p for p in output.identified_problems if p.category == ProblemCategory.HIGH_CAC]
    assert len(cac_problems) >= 1
    assert cac_problems[0].responsible_agent == "optimization_agent"
    assert any("bid multiplier" in t.prompt_injection.lower() for t in output.corrective_tasks)


# ---------------------------------------------------------------------------
# Scenario 6: Health Score Quality Gate Failure (< 70.0) -> Analytics / Content
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_scenario_6_health_score_failure_triggers_remediation(base_campaign_context):
    engine = CorrectionEngine()

    # Attach deficient analytics health score
    base_campaign_context.analytics = AnalyticsAgentOutput(
        health_score=CampaignHealthScore(overall=58.0, stage_scores={"awareness": 50.0, "conversion": 62.0}),
        predicted_metrics=[],
    )

    updated_context, output = await engine.execute_correction_loop(
        context=base_campaign_context,
        trigger_source=CorrectionTriggerSource.ANALYTICS_ISSUE,
    )

    health_problems = [p for p in output.identified_problems if p.category == ProblemCategory.HEALTH_SCORE_GATE_FAILURE]
    assert len(health_problems) >= 1
    assert health_problems[0].current_value == 58.0
    assert health_problems[0].responsible_agent == "content_agent"


# ---------------------------------------------------------------------------
# Scenario 7: Invalid RL Action / Simplex Constraint Breach -> Optimization
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_scenario_7_invalid_rl_action_routes_to_optimizer(base_campaign_context):
    engine = CorrectionEngine()

    base_campaign_context.optimization = OptimizationOutput(
        safety_validation=ConstraintValidationResult(
            is_valid=False,
            violations=["Channel 'facebook' requested shift (45%) exceeds maximum single-cycle limit."],
            modifications_applied=["Clamped weights"],
            approved_by_safety_gate=False,
            requires_human_approval=True,
        ),
        action_proposal=RLActionProposal(
            channel_allocations={"linkedin": 0.5, "facebook": 0.3, "email": 0.2},
            bid_multiplier=1.5,
        ),
        optimization_actions=[],
        budget_reallocation_plan="Shift budget",
        performance_forecast="Increased ROAS",
        confidence=0.85,
    )

    updated_context, output = await engine.execute_correction_loop(
        context=base_campaign_context,
        trigger_source=CorrectionTriggerSource.RL_ISSUE,
    )

    rl_problems = [p for p in output.identified_problems if p.category == ProblemCategory.INVALID_RL_ACTION]
    assert len(rl_problems) >= 1
    assert rl_problems[0].responsible_agent == "optimization_agent"


# ---------------------------------------------------------------------------
# Scenario 8: Human Rejection with Copy Directives
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_scenario_8_human_rejection_directives(base_campaign_context):
    agent = CorrectionAgent()

    feedback = "Headlines are too generic; focus on AI automation and enterprise compliance."

    updated_context = await agent.run(
        context=base_campaign_context,
        trigger_source=CorrectionTriggerSource.HUMAN_REJECTION,
        human_feedback=feedback,
    )

    assert "correction_agent" in updated_context.agent_outputs
    out = updated_context.agent_outputs["correction_agent"]
    assert "content_agent" in out.responsible_agents
    assert any("AI automation" in d or "generic" in d for d in out.correction_prompt_directives)


# ---------------------------------------------------------------------------
# Scenario 9: Multiple Concurrent Multi-Agent Failures (Prioritized Triage)
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_scenario_9_multiple_concurrent_failures_triage(base_campaign_context):
    engine = CorrectionEngine()

    # 1. Deficient CV
    base_campaign_context.cv = CVAgentOutput(
        aesthetic_score=5.2,
        passed_quality_gate=False,
        detected_issues=["Blurry imagery"],
    )

    # 2. Performance Deviations (CTR + CPA)
    deviations = [
        {"metric": "ctr", "current_value": 0.90, "target_value": 2.50, "description": "Low CTR"},
        {"metric": "cpa", "current_value": 75.0, "target_value": 45.0, "description": "High CPA"},
    ]

    updated_context, output = await engine.execute_correction_loop(
        context=base_campaign_context,
        explicit_deviations=deviations,
    )

    assert len(output.identified_problems) >= 3
    agents = output.responsible_agents
    assert "design_agent" in agents
    assert "content_agent" in agents
    assert "optimization_agent" in agents

    # Verify tasks are ordered by priority
    priorities = [t.priority for t in output.corrective_tasks]
    assert priorities == sorted(priorities)


# ---------------------------------------------------------------------------
# Scenario 10: Max Retries Exceeded Circuit Breaker -> HITL Escalation
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_scenario_10_circuit_breaker_escalates_to_hitl(base_campaign_context):
    engine = CorrectionEngine(max_iterations=3)

    deviations = [{"metric": "ctr", "current_value": 0.50, "target_value": 2.50, "description": "Critical low CTR"}]

    updated_context, output = await engine.execute_correction_loop(
        context=base_campaign_context,
        explicit_deviations=deviations,
        current_attempt=3,  # Attempt = Max Iterations
    )

    assert output.circuit_breaker_triggered is True
    assert output.quality_gate_passed is False
    assert "HITL" in " ".join(output.evidence) or "circuit breaker" in " ".join(output.evidence).lower()


# ---------------------------------------------------------------------------
# Scenario 11: Strict Context Invariant Safeguard (ConstraintGuard)
# ---------------------------------------------------------------------------
def test_scenario_11_constraint_guard_detects_and_recovers_invariants(base_campaign_context):
    guard = ConstraintGuard()
    baseline = guard.snapshot_invariants(base_campaign_context)

    # Simulate an agent illegally modifying campaign budget and company name
    tampered_context = copy.deepcopy(base_campaign_context)
    tampered_context.budget.total_budget = 999999.0
    tampered_context.business.name = "Malicious Hijack Corp"

    is_valid, violations = guard.verify_invariants(baseline, tampered_context)
    assert is_valid is False
    assert len(violations) == 2

    # Verify automatic restoration
    restored_context = guard.restore_invariants(tampered_context, baseline)
    assert restored_context.budget.total_budget == 15000.0
    assert restored_context.business.name == "CloudFlow Systems"

    is_valid_now, _ = guard.verify_invariants(baseline, restored_context)
    assert is_valid_now is True


# ---------------------------------------------------------------------------
# Scenario 12: Master Orchestrator Stage 9 Integration
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_scenario_12_master_orchestrator_stage_9_integration(base_campaign_context):
    orchestrator = MasterOrchestrator()
    plan = orchestrator.planner.plan(base_campaign_context)

    # Verify correction_engine is scheduled at Step 9
    correction_steps = [s for s in plan.agent_sequence if s.agent_name in ["correction_engine", "correction_agent"]]
    assert len(correction_steps) == 1
    assert correction_steps[0].stage_order == 9

    async def mock_pass(ctx):
        return ctx

    orchestrator.register_runner("publishing_agent", mock_pass)
    orchestrator.register_runner("monitoring_agent", mock_pass)

    # Execute full orchestrator run
    result_context = await orchestrator.execute_plan(base_campaign_context, plan)
    assert result_context is not None
    assert "correction_agent" in result_context.agent_outputs
    assert result_context.execution_plan.status == WorkflowState.SUCCESS
