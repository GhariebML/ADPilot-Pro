"""Verification script for Phase 4 — Planner / Orchestrator."""

import asyncio
from adpilot.core.context_builder import CampaignContextBuilder
from adpilot.core.exceptions import AgentExecutionError
from adpilot.orchestrator.master_orchestrator import MasterOrchestrator
from adpilot.orchestrator.planner import CampaignPlanner
from adpilot.schemas.agent_schemas import (
    AnalyticsAgentOutput,
    CampaignHealthScore,
    FunnelStage,
    ProductType,
)
from adpilot.schemas.execution_plan import (
    ExecutionPlan,
    WorkflowState,
)


def main() -> None:
    print("=" * 80)
    print("ADPilot Phase 4 — Planner / Master Orchestrator Verification")
    print("=" * 80)

    # 1. Build Context
    context = (
        CampaignContextBuilder.create("camp-phase4-verify")
        .with_business(name="AuraPay", industry="FinTech SaaS")
        .with_product(
            name="AuraPay Global Billing Engine",
            product_type=ProductType.saas,
            description="Real-time multi-currency recurring billing, tax compliance, and automated invoicing.",
            unique_selling_points=["135+ currencies", "99.999% uptime", "Zero fraud chargebacks"],
            pricing_model="subscription",
        )
        .with_audience(summary="CFOs, VP of Finance, and Head of Payments at scale-ups")
        .with_budget(total_budget=35000.0)
        .with_timeline(duration_days=45)
        .build()
    )

    planner = CampaignPlanner()
    orchestrator = MasterOrchestrator(planner=planner)

    # Verification 1: Frozen Pipeline Plan Generation
    plan = planner.plan(context)
    assert isinstance(plan, ExecutionPlan)
    assert len(plan.agent_sequence) == 12
    expected_order = [
        "strategy_agent", "research_agent", "competitor_agent", "content_agent",
        "design_agent", "cv_agent", "analytics_agent", "optimization_agent",
        "correction_engine", "hitl_gate", "publishing_agent", "monitoring_agent",
    ]
    actual_order = [s.agent_name for s in plan.agent_sequence]
    assert actual_order == expected_order
    print(f"[PASS] 1. Frozen Pipeline Plan Generation: {len(plan.agent_sequence)} steps strictly ordered.")

    # Mock runner helper
    async def mock_pass(ctx):
        return ctx

    for s in expected_order:
        orchestrator.register_runner(s, mock_pass)

    # Verification 2: Full Successful Pipeline Execution
    res_ctx = asyncio.run(orchestrator.execute_plan(context, plan=plan))
    assert res_ctx.execution_plan.status == WorkflowState.SUCCESS
    assert res_ctx.execution_plan.completed_steps == 12
    print(f"[PASS] 2. Full Pipeline Execution: status={res_ctx.execution_plan.status.value}, completed_steps={res_ctx.execution_plan.completed_steps}/12")

    # Verification 3: Fault Handling & Unrecoverable Failure
    fail_orch = MasterOrchestrator()
    fail_orch.register_runner("strategy_agent", mock_pass)
    async def crash_runner(ctx):
        raise ValueError("Critical LLM context overflow error")
    fail_orch.register_runner("research_agent", crash_runner)

    fail_plan = planner.plan(context)
    for s in fail_plan.agent_sequence:
        s.max_retries = 1

    try:
        asyncio.run(fail_orch.execute_plan(context, plan=fail_plan))
        assert False, "Expected AgentExecutionError"
    except AgentExecutionError as e:
        assert fail_plan.status == WorkflowState.FAILED
        assert fail_plan.failed_steps == 1
        print(f"[PASS] 3. Unrecoverable Failure Handling: caught={type(e).__name__}, plan_status={fail_plan.status.value}")

    # Verification 4: Retry with Exponential Backoff
    retry_orch = MasterOrchestrator()
    flaky_attempts = 0
    async def flaky_runner(ctx):
        nonlocal flaky_attempts
        flaky_attempts += 1
        if flaky_attempts == 1:
            raise ConnectionError("Transient timeout")
        return ctx

    retry_orch.register_runner("strategy_agent", flaky_runner)
    for s in expected_order[1:]:
        retry_orch.register_runner(s, mock_pass)

    retry_plan = planner.plan(context)
    retry_res = asyncio.run(retry_orch.execute_plan(context, plan=retry_plan))
    assert retry_res.execution_plan.status == WorkflowState.SUCCESS
    assert retry_res.execution_plan.agent_sequence[0].attempts == 2
    print(f"[PASS] 4. Retry & Backoff Resilience: attempts={retry_res.execution_plan.agent_sequence[0].attempts}, status={retry_res.execution_plan.status.value}")

    # Verification 5: Step Timeout Protection
    timeout_orch = MasterOrchestrator()
    async def slow_runner(ctx):
        await asyncio.sleep(2.0)
        return ctx

    timeout_orch.register_runner("strategy_agent", slow_runner)
    timeout_plan = planner.plan(context)
    timeout_plan.agent_sequence[0].timeout_seconds = 0.05
    timeout_plan.agent_sequence[0].max_retries = 1

    try:
        asyncio.run(timeout_orch.execute_plan(context, plan=timeout_plan))
        assert False, "Expected AgentExecutionError"
    except AgentExecutionError:
        assert timeout_plan.agent_sequence[0].state == WorkflowState.TIMED_OUT
        print(f"[PASS] 5. Timeout Protection: step_state={timeout_plan.agent_sequence[0].state.value}")

    # Verification 6: Skipped Optional Agent
    skip_orch = MasterOrchestrator()
    for s in expected_order:
        skip_orch.register_runner(s, mock_pass)

    skip_plan = planner.plan(context)
    skip_res = asyncio.run(skip_orch.execute_plan(context, plan=skip_plan, skipped_agents={"cv_agent"}))
    cv_s = next(s for s in skip_res.execution_plan.agent_sequence if s.agent_name == "cv_agent")
    assert cv_s.state == WorkflowState.SKIPPED
    assert skip_res.execution_plan.status == WorkflowState.SUCCESS
    print(f"[PASS] 6. Optional Agent Skipping: cv_agent_state={cv_s.state.value}, plan_status={skip_res.execution_plan.status.value}")

    # Verification 7: Human-in-the-Loop (HITL) Pause Gate
    hitl_orch = MasterOrchestrator()
    for s in expected_order:
        hitl_orch.register_runner(s, mock_pass)

    hitl_plan = planner.plan(context)
    hitl_res = asyncio.run(hitl_orch.execute_plan(context, plan=hitl_plan, auto_approve_hitl=False))
    assert hitl_res.execution_plan.status == WorkflowState.WAITING_FOR_APPROVAL
    hitl_s = next(s for s in hitl_res.execution_plan.agent_sequence if s.agent_name == "hitl_gate")
    assert hitl_s.state == WorkflowState.WAITING_FOR_APPROVAL
    print(f"[PASS] 7. Human-in-the-Loop Gate: plan_status={hitl_res.execution_plan.status.value}, hitl_step_state={hitl_s.state.value}")

    # Verification 8: Quality Gate Correction Loop
    corr_orch = MasterOrchestrator()
    content_count = 0
    async def counting_content(ctx):
        nonlocal content_count
        content_count += 1
        return ctx

    async def mock_evaluator(ctx):
        score = 50.0 if content_count == 1 else 90.0
        health = CampaignHealthScore(
            overall=score,
            stage_scores={FunnelStage.awareness: score, FunnelStage.conversion: score},
        )
        ctx.analytics = AnalyticsAgentOutput(
            health_score=health,
            predicted_metrics=[],
            content_scorecards=[],
            improvement_suggestions=[],
            ab_test_recommendations=[],
            budget_reallocation_advice="Optimized",
            executive_summary="Summary",
            next_review_checkpoint="Checkpoint",
        )
        return ctx

    for s in expected_order:
        corr_orch.register_runner(s, mock_pass)
    corr_orch.register_runner("content_agent", counting_content)
    corr_orch.register_runner("analytics_agent", mock_evaluator)

    corr_plan = planner.plan(context)
    corr_res = asyncio.run(corr_orch.execute_plan(context, plan=corr_plan, max_corrections=2))
    assert content_count == 2
    assert corr_res.execution_plan.status == WorkflowState.SUCCESS
    print(f"[PASS] 8. Quality Gate Correction Loop: content_executions={content_count}, plan_status={corr_res.execution_plan.status.value}")

    # Verification 9: Full Traceability Audit Records
    records = orchestrator.agent_run_records
    assert len(records) == 12
    for r in records:
        assert r.status.value == "success"
        assert r.started_at is not None
        assert r.finished_at is not None
    print(f"[PASS] 9. Full Traceability Audit Records: {len(records)} AgentRunRecords verified.")

    print("=" * 80)
    print("ALL PHASE 4 PLANNER & MASTER ORCHESTRATOR VERIFICATIONS PASSED!")
    print("=" * 80)


if __name__ == "__main__":
    main()
