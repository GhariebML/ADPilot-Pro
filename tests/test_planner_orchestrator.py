"""Unit and integration tests for Phase 4 — Planner and Master Orchestrator."""

import asyncio
import pytest
from adpilot.core.context_builder import CampaignContextBuilder
from adpilot.core.exceptions import AgentExecutionError
from adpilot.orchestrator.master_orchestrator import MasterOrchestrator
from adpilot.orchestrator.planner import CampaignPlanner
from adpilot.schemas.agent_schemas import ProductType
from adpilot.schemas.execution_plan import (
    ExecutionPlan,
    WorkflowState,
)


@pytest.fixture
def sample_context():
    return (
        CampaignContextBuilder.create("camp-plan-001")
        .with_business(name="NexSys Cloud", industry="Cloud Infrastructure")
        .with_product(
            name="NexSys Kubernetes Optimizer",
            product_type=ProductType.saas,
            description="Autonomous Kubernetes cluster cost optimization and pod autoscaling engine.",
            unique_selling_points=["40% AWS savings", "Zero downtime migration"],
            pricing_model="subscription",
        )
        .with_audience(summary="Cloud Architects and Platform Engineers")
        .with_budget(total_budget=15000.0)
        .with_timeline(duration_days=30)
        .build()
    )


def test_planner_generates_frozen_master_pipeline(sample_context):
    planner = CampaignPlanner()
    plan = planner.plan(sample_context)

    assert isinstance(plan, ExecutionPlan)
    assert plan.campaign_id == "camp-plan-001"
    assert plan.product_type == ProductType.saas
    assert plan.total_steps == 12

    # Verify Frozen Master Pipeline Order
    expected_order = [
        "strategy_agent",
        "research_agent",
        "competitor_agent",
        "content_agent",
        "design_agent",
        "cv_agent",
        "analytics_agent",
        "optimization_agent",
        "correction_engine",
        "hitl_gate",
        "publishing_agent",
        "monitoring_agent",
    ]
    actual_order = [step.agent_name for step in plan.agent_sequence]
    assert actual_order == expected_order

    # Verify stage numbering is strictly 1 to 12
    for i, step in enumerate(plan.agent_sequence, start=1):
        assert step.stage_order == i
        assert step.state == WorkflowState.PENDING

    # Verify validation and approval points
    assert any("funnel_budget_allocation_sum_100" in vp for vp in plan.validation_points)
    assert any("analytics_health_gate" in vp for vp in plan.validation_points)
    assert any(step.approval_point is True for step in plan.agent_sequence if step.agent_name == "hitl_gate")


@pytest.mark.asyncio
async def test_master_orchestrator_complete_successful_workflow(sample_context):
    orchestrator = MasterOrchestrator()

    # Mock runners for every stage to succeed
    async def mock_runner(ctx):
        return ctx

    for step_name in [
        "strategy_agent", "research_agent", "competitor_agent", "content_agent",
        "design_agent", "cv_agent", "analytics_agent", "optimization_agent",
        "correction_engine", "hitl_gate", "publishing_agent", "monitoring_agent",
    ]:
        orchestrator.register_runner(step_name, mock_runner)

    plan = orchestrator.planner.plan(sample_context)
    result_context = await orchestrator.execute_plan(sample_context, plan=plan)

    assert result_context.execution_plan.status == WorkflowState.SUCCESS
    assert result_context.execution_plan.completed_steps == 12
    assert result_context.execution_plan.failed_steps == 0
    for step in result_context.execution_plan.agent_sequence:
        assert step.state == WorkflowState.SUCCESS
        assert step.finished_at is not None


@pytest.mark.asyncio
async def test_master_orchestrator_unrecoverable_failure(sample_context):
    orchestrator = MasterOrchestrator()

    async def failing_runner(ctx):
        raise RuntimeError("Unrecoverable database connection crash")

    async def mock_runner(ctx):
        return ctx

    orchestrator.register_runner("strategy_agent", mock_runner)
    orchestrator.register_runner("research_agent", failing_runner)

    plan = orchestrator.planner.plan(sample_context)
    # Set max_retries=1 to fail fast
    for s in plan.agent_sequence:
        s.max_retries = 1

    with pytest.raises(AgentExecutionError, match="Stage 2"):
        await orchestrator.execute_plan(sample_context, plan=plan)

    assert plan.status == WorkflowState.FAILED
    assert plan.failed_steps == 1
    assert plan.agent_sequence[1].state == WorkflowState.FAILED
    assert "Unrecoverable database connection crash" in plan.agent_sequence[1].error_message


@pytest.mark.asyncio
async def test_master_orchestrator_retry_with_backoff(sample_context):
    orchestrator = MasterOrchestrator()

    attempts = 0

    async def flaky_strategy_runner(ctx):
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise ConnectionResetError("Transient network drop")
        return ctx

    async def mock_runner(ctx):
        return ctx

    orchestrator.register_runner("strategy_agent", flaky_strategy_runner)
    for step_name in [
        "research_agent", "competitor_agent", "content_agent",
        "design_agent", "cv_agent", "analytics_agent", "optimization_agent",
        "correction_engine", "hitl_gate", "publishing_agent", "monitoring_agent",
    ]:
        orchestrator.register_runner(step_name, mock_runner)

    plan = orchestrator.planner.plan(sample_context)
    result_context = await orchestrator.execute_plan(sample_context, plan=plan)

    assert result_context.execution_plan.status == WorkflowState.SUCCESS
    strategy_step = result_context.execution_plan.agent_sequence[0]
    assert strategy_step.attempts == 2
    assert strategy_step.state == WorkflowState.SUCCESS


@pytest.mark.asyncio
async def test_master_orchestrator_step_timeout_protection(sample_context):
    orchestrator = MasterOrchestrator()

    async def hanging_runner(ctx):
        await asyncio.sleep(5.0)  # Hangs for 5s
        return ctx

    orchestrator.register_runner("strategy_agent", hanging_runner)

    plan = orchestrator.planner.plan(sample_context)
    # Set timeout to 0.05 seconds and 1 retry
    plan.agent_sequence[0].timeout_seconds = 0.05
    plan.agent_sequence[0].max_retries = 1

    with pytest.raises(AgentExecutionError, match="timed out"):
        await orchestrator.execute_plan(sample_context, plan=plan)

    strategy_step = plan.agent_sequence[0]
    assert strategy_step.state == WorkflowState.TIMED_OUT
    assert plan.status == WorkflowState.FAILED


@pytest.mark.asyncio
async def test_master_orchestrator_skipped_optional_agent(sample_context):
    orchestrator = MasterOrchestrator()

    async def mock_runner(ctx):
        return ctx

    for step_name in [
        "strategy_agent", "research_agent", "competitor_agent", "content_agent",
        "design_agent", "cv_agent", "analytics_agent", "optimization_agent",
        "correction_engine", "hitl_gate", "publishing_agent", "monitoring_agent",
    ]:
        orchestrator.register_runner(step_name, mock_runner)

    plan = orchestrator.planner.plan(sample_context)
    
    # Execute with 'cv_agent' marked as skipped
    result_context = await orchestrator.execute_plan(
        sample_context,
        plan=plan,
        skipped_agents={"cv_agent"},
    )

    assert result_context.execution_plan.status == WorkflowState.SUCCESS
    cv_step = next(s for s in result_context.execution_plan.agent_sequence if s.agent_name == "cv_agent")
    assert cv_step.state == WorkflowState.SKIPPED
    assert cv_step.output_snapshot["skipped"] is True


@pytest.mark.asyncio
async def test_master_orchestrator_hitl_approval_pause(sample_context):
    orchestrator = MasterOrchestrator()

    async def mock_runner(ctx):
        return ctx

    for step_name in [
        "strategy_agent", "research_agent", "competitor_agent", "content_agent",
        "design_agent", "cv_agent", "analytics_agent", "optimization_agent",
        "correction_engine", "hitl_gate", "publishing_agent", "monitoring_agent",
    ]:
        orchestrator.register_runner(step_name, mock_runner)

    plan = orchestrator.planner.plan(sample_context)

    # Execute with auto_approve_hitl=False -> should pause at hitl_gate
    result_context = await orchestrator.execute_plan(
        sample_context,
        plan=plan,
        auto_approve_hitl=False,
    )

    assert result_context.execution_plan.status == WorkflowState.WAITING_FOR_APPROVAL
    hitl_step = next(s for s in result_context.execution_plan.agent_sequence if s.agent_name == "hitl_gate")
    assert hitl_step.state == WorkflowState.WAITING_FOR_APPROVAL


@pytest.mark.asyncio
async def test_master_orchestrator_traceability_run_records(sample_context):
    orchestrator = MasterOrchestrator()

    async def mock_runner(ctx):
        return ctx

    for step_name in [
        "strategy_agent", "research_agent", "competitor_agent", "content_agent",
        "design_agent", "cv_agent", "analytics_agent", "optimization_agent",
        "correction_engine", "hitl_gate", "publishing_agent", "monitoring_agent",
    ]:
        orchestrator.register_runner(step_name, mock_runner)

    plan = orchestrator.planner.plan(sample_context)
    await orchestrator.execute_plan(sample_context, plan=plan)

    records = orchestrator.agent_run_records
    assert len(records) == 12
    for r in records:
        assert r.status.value == "success"
        assert r.started_at is not None
        assert r.finished_at is not None
        assert "attempts" in r.output_snapshot


@pytest.mark.asyncio
async def test_master_orchestrator_correction_loop(sample_context):
    from adpilot.schemas.agent_schemas import (
        AnalyticsAgentOutput,
        CampaignHealthScore,
        FunnelStage,
    )

    orchestrator = MasterOrchestrator()
    content_execution_count = 0

    async def counting_content_runner(ctx):
        nonlocal content_execution_count
        content_execution_count += 1
        return ctx

    async def mock_analytics_runner(ctx):
        # On first run, return failing health score 55.0; on second run, return 85.0
        score = 55.0 if content_execution_count == 1 else 85.0
        health_score = CampaignHealthScore(
            overall=score,
            stage_scores={FunnelStage.awareness: score, FunnelStage.conversion: score},
        )
        ctx.analytics = AnalyticsAgentOutput(
            health_score=health_score,
            predicted_metrics=[],
            content_scorecards=[],
            improvement_suggestions=[],
            ab_test_recommendations=[],
            budget_reallocation_advice="Maintain budget",
            executive_summary="Executive summary test",
            next_review_checkpoint="Checkpoint 1",
        )
        return ctx

    async def mock_runner(ctx):
        return ctx

    for step_name in [
        "strategy_agent", "research_agent", "competitor_agent",
        "design_agent", "cv_agent", "optimization_agent",
        "correction_engine", "hitl_gate", "publishing_agent", "monitoring_agent",
    ]:
        orchestrator.register_runner(step_name, mock_runner)

    orchestrator.register_runner("content_agent", counting_content_runner)
    orchestrator.register_runner("analytics_agent", mock_analytics_runner)

    plan = orchestrator.planner.plan(sample_context)
    result_context = await orchestrator.execute_plan(sample_context, plan=plan, max_corrections=2)

    # Content agent should have run twice due to correction loop
    assert content_execution_count == 2
    assert result_context.execution_plan.status == WorkflowState.SUCCESS
