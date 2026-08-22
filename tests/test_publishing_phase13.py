"""Phase 13 — Comprehensive Test Suite for Publishing Agent Execution Boundary.

Covers:
1. Pre-Flight Gate: Rejection of Unapproved Campaign
2. Pre-Flight Gate: Missing Content Assets Blocked
3. Pre-Flight Gate: Missing Strategy Blocked
4. Pre-Flight Gate: Invalid Optimizer Actions Blocked
5. Safe Dry-Run Mode Multi-Channel Dispatch (Meta, Google, LinkedIn, Email)
6. Idempotency Key Generation & Duplicate Publish Prevention
7. Transient Error Automatic Retries with Exponential Backoff
8. Partial Channel Failure Isolation & Exhausted Attempts
9. Non-Silent Operational Audit Logging
10. PublishingAgent Standalone Contract & Lifecycle Event Bus
11. Master Orchestrator Stage 11 Integration
"""

from __future__ import annotations

import pytest

from adpilot.agents.publishing_agent import PublishingAgent
from adpilot.core.agent_events import AgentEventType, event_bus
from adpilot.hitl.audit import HITLAuditStore
from adpilot.hitl.schemas import HITLGateOutput, HumanDecisionType
from adpilot.orchestrator.master_orchestrator import MasterOrchestrator
from adpilot.publishing.adapters import (
    BasePublishingAdapter,
    MockDryRunAdapter,
)
from adpilot.publishing.audit import PublishingAuditLogger
from adpilot.publishing.engine import PublishingEngine
from adpilot.publishing.idempotency import IdempotencyStore
from adpilot.publishing.schemas import (
    ExecutionMode,
    ProviderType,
    PublishingPayload,
    PublishingStatus,
)
from adpilot.publishing.validator import PublishingValidator
from adpilot.schemas.agent_schemas import (
    ApprovalRequirements,
    BrandGuidelines,
    BudgetSpec,
    BusinessInfo,
    CampaignConstraints,
    CampaignContext,
    CampaignGoal,
    ConstraintValidationResult,
    ContentAgentOutput,
    ContextMetadata,
    DesignAgentOutput,
    FunnelStage,
    FunnelStageStrategy,
    Geography,
    MarketingChannel,
    MessagingPillar,
    OptimizationOutput,
    ProductSpec,
    RLActionProposal,
    RLPolicyType,
    StrategyAgentOutput,
    TimelineSpec,
    ToneOfVoice,
)
from adpilot.schemas.campaign_context import KPITargets
from adpilot.schemas.execution_plan import WorkflowState


@pytest.fixture
def base_approved_campaign_context() -> CampaignContext:
    """Fixture providing a fully approved and enriched CampaignContext."""
    strategy_out = StrategyAgentOutput(
        positioning_statement="Apex Cloud: Real-time distributed data infrastructure.",
        usp="Sub-millisecond query execution at petabyte scale.",
        elevator_pitch="Query enterprise live streams instantly.",
        tone_of_voice=ToneOfVoice.professional,
        brand_voice_guidelines="Authoritative, clear, engineering-led",
        primary_channels=[MarketingChannel.linkedin, MarketingChannel.facebook, MarketingChannel.email],
        messaging_pillars=[
            MessagingPillar(title="Velocity", description="Zero latency stream processing"),
            MessagingPillar(title="Reliability", description="High availability enterprise SLA"),
        ],
        funnel_strategy=[
            FunnelStageStrategy(
                stage=FunnelStage.awareness,
                budget_allocation_percent=40.0,
                key_messages=["Stop waiting for slow queries"],
            ),
            FunnelStageStrategy(
                stage=FunnelStage.consideration,
                budget_allocation_percent=35.0,
                key_messages=["Live query benchmark vs Snowflake"],
            ),
            FunnelStageStrategy(
                stage=FunnelStage.conversion,
                budget_allocation_percent=25.0,
                key_messages=["Start 14-day dedicated cluster trial"],
            ),
        ],
        target_persona_summary="VP Engineering and Lead Data Architects",
        key_differentiators=["Federated live indexing", "Sub-millisecond latency"],
        risks_and_considerations=["Requires distributed deployment"],
        confidence=0.94,
    )

    content_out = ContentAgentOutput(
        headlines=["Stream Data at Millisecond Speeds", "Modern Enterprise Query Engine"],
        primary_copy=["Stop batch lag. Apex delivers instant distributed stream analytics for enterprise."],
        descriptions=["High performance real-time query engine."],
        ctas=["Start Free Trial", "Book Demo"],
        keywords=["streaming analytics", "real-time database"],
        content_calendar_note="Multi-channel launch plan",
    )

    design_out = DesignAgentOutput(
        generated_prompts=["Sleek data visualization glowing telemetry nodes in dark mode"],
        color_palette=["#1E3A8A", "#3B82F6", "#93C5FD"],
        visual_style="Minimalist Enterprise",
        typography_recommendations=["Inter"],
        aspect_ratios=["1:1", "16:9"],
        brand_alignment_score=0.96,
    )

    opt_out = OptimizationOutput(
        policy_type=RLPolicyType.ppo,
        action_proposal=RLActionProposal(
            channel_allocations={
                MarketingChannel.linkedin.value: 0.50,
                MarketingChannel.facebook.value: 0.30,
                MarketingChannel.email.value: 0.20,
            },
            bid_multiplier=1.05,
            suggested_frequency_cap=3.0,
        ),
        safety_validation=ConstraintValidationResult(
            is_valid=True,
            violations=[],
            modifications_applied=[],
            clamped_allocations={
                MarketingChannel.linkedin.value: 0.50,
                MarketingChannel.facebook.value: 0.30,
                MarketingChannel.email.value: 0.20,
            },
            approved_by_safety_gate=True,
        ),
        predicted_reward=4.5,
        confidence=0.92,
    )

    ctx = CampaignContext(
        campaign_id="camp-pub-p13",
        metadata=ContextMetadata(created_by="publishing_test_suite"),
        business=BusinessInfo(
            name="Apex Data Cloud",
            industry="Cloud Infrastructure",
            description="Ultra low-latency streaming analytics platform",
        ),
        product=ProductSpec(
            name="Apex Engine",
            product_type="saas",
            description="Enterprise streaming analytics engine",
            unique_selling_points=["Sub-millisecond latency", "Distributed query federation"],
        ),
        goals=[CampaignGoal.lead_generation, CampaignGoal.brand_awareness],
        channels=[MarketingChannel.linkedin, MarketingChannel.facebook, MarketingChannel.email],
        budget=BudgetSpec(total_budget=20000.0, currency="USD", daily_budget_cap=800.0),
        timeline=TimelineSpec(duration_days=30),
        geography=Geography(target_countries=["US", "CA", "DE"]),
        kpis=KPITargets(target_cpa=50.0, target_roas=4.0, target_ctr=3.0),
        constraints=CampaignConstraints(
            max_cpa=70.0,
            min_roas=3.0,
            prohibited_keywords=["free hack", "unlimited money"],
        ),
        brand=BrandGuidelines(
            tone_of_voice=ToneOfVoice.professional,
            brand_colors=["#1E3A8A", "#3B82F6", "#93C5FD"],
        ),
        approvals=ApprovalRequirements(human_approval_required=True, min_health_score=70.0),
        variables={},
    )

    ctx.strategy = strategy_out
    ctx.content = content_out
    ctx.design = design_out
    ctx.optimization = opt_out
    ctx.record_agent_output("strategy_agent", strategy_out)
    ctx.record_agent_output("content_agent", content_out)
    ctx.record_agent_output("design_agent", design_out)
    ctx.record_agent_output("optimization_agent", opt_out)

    # Attach Human Approval Sign-Off in Stage 10 Gate Output
    hitl_gate_out = HITLGateOutput(
        stage="publishing",
        decision=HumanDecisionType.FINAL_APPROVAL,
        approved_by="alex_vp_growth",
        approved_at="2026-08-22T12:00:00Z",
        reason="Campaign verified and signed off for multi-channel live release.",
        is_approved=True,
        audit_id="audit-pub-signoff-123",
    )
    ctx.record_agent_output("hitl_gate", hitl_gate_out)

    return ctx


# ---------------------------------------------------------------------------
# Scenario 1: Pre-Flight Gate — Rejection of Unapproved Campaign
# ---------------------------------------------------------------------------
def test_scenario_1_unapproved_campaign_blocked(base_approved_campaign_context):
    unapproved_ctx = base_approved_campaign_context.model_copy(deep=True)
    # Remove HITL gate signoff
    unapproved_ctx.agent_outputs.pop("hitl_gate", None)

    validator = PublishingValidator()
    result = validator.validate_pre_flight(unapproved_ctx)

    assert result.is_valid is False
    assert result.approvals_verified is False
    assert any("approval" in err.lower() for err in result.validation_errors)


# ---------------------------------------------------------------------------
# Scenario 2: Pre-Flight Gate — Missing Content Assets Blocked
# ---------------------------------------------------------------------------
def test_scenario_2_missing_content_assets_blocked(base_approved_campaign_context):
    ctx_no_content = base_approved_campaign_context.model_copy(deep=True)
    ctx_no_content.content = None
    ctx_no_content.agent_outputs.pop("content_agent", None)

    validator = PublishingValidator()
    result = validator.validate_pre_flight(ctx_no_content)

    assert result.is_valid is False
    assert result.assets_verified is False
    assert any("content" in err.lower() for err in result.validation_errors)


# ---------------------------------------------------------------------------
# Scenario 3: Pre-Flight Gate — Missing Strategy Blocked
# ---------------------------------------------------------------------------
def test_scenario_3_missing_strategy_blocked(base_approved_campaign_context):
    ctx_no_strategy = base_approved_campaign_context.model_copy(deep=True)
    ctx_no_strategy.strategy = None
    ctx_no_strategy.agent_outputs.pop("strategy_agent", None)

    validator = PublishingValidator()
    result = validator.validate_pre_flight(ctx_no_strategy)

    assert result.is_valid is False
    assert result.strategy_verified is False
    assert any("strategy" in err.lower() for err in result.validation_errors)


# ---------------------------------------------------------------------------
# Scenario 4: Pre-Flight Gate — Invalid Optimizer Actions Blocked
# ---------------------------------------------------------------------------
def test_scenario_4_invalid_optimizer_actions_blocked(base_approved_campaign_context):
    ctx_invalid_opt = base_approved_campaign_context.model_copy(deep=True)
    ctx_invalid_opt.optimization.safety_validation = ConstraintValidationResult(
        is_valid=False,
        violations=["Channel allocation sum breached: 1.40 > 1.00"],
        modifications_applied=[],
        clamped_allocations={},
        approved_by_safety_gate=False,
    )

    validator = PublishingValidator()
    result = validator.validate_pre_flight(ctx_invalid_opt)

    assert result.is_valid is False
    assert result.optimizer_actions_verified is False
    assert any("optimizer action failed" in err.lower() for err in result.validation_errors)


# ---------------------------------------------------------------------------
# Scenario 5: Safe Dry-Run Mode Multi-Channel Dispatch
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_scenario_5_safe_dry_run_multi_channel_dispatch(base_approved_campaign_context):
    engine = PublishingEngine()
    
    # Execute publishing in safe dry-run mode
    updated_ctx, report = await engine.execute_publishing(
        context=base_approved_campaign_context,
        force_dry_run=True,
    )

    assert report.execution_mode == ExecutionMode.DRY_RUN
    assert report.successful_dispatches == 3
    assert report.failed_dispatches == 0
    assert len(report.receipts) == 3

    for receipt in report.receipts:
        assert receipt.is_dry_run is True
        assert receipt.status == PublishingStatus.DRY_RUN_PUBLISHED
        assert receipt.platform_post_id is not None
        assert "dry-run" in receipt.metadata.get("dry_run_reason", "").lower() or receipt.metadata.get("simulated") or receipt.is_dry_run is True


# ---------------------------------------------------------------------------
# Scenario 6: Idempotency Key Generation & Duplicate Publish Prevention
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_scenario_6_idempotency_duplicate_prevention(base_approved_campaign_context):
    idemp_store = IdempotencyStore()
    engine = PublishingEngine(idemp_store=idemp_store)

    # First dispatch -> successful dry-run publish
    _, report1 = await engine.execute_publishing(base_approved_campaign_context, force_dry_run=True)
    assert report1.successful_dispatches == 3
    for r in report1.receipts:
        assert r.status == PublishingStatus.DRY_RUN_PUBLISHED

    # Second immediate dispatch with identical parameters -> duplicate ignored
    _, report2 = await engine.execute_publishing(base_approved_campaign_context, force_dry_run=True)
    assert report2.successful_dispatches == 3
    for r in report2.receipts:
        assert r.status == PublishingStatus.DUPLICATE_IGNORED
        assert r.metadata.get("duplicate_ignored") is True


# ---------------------------------------------------------------------------
# Scenario 7: Transient Error Automatic Retries with Exponential Backoff
# ---------------------------------------------------------------------------
class FlakyAdapter(BasePublishingAdapter):
    """Adapter that fails twice before succeeding on attempt 3."""
    provider_type = ProviderType.MOCK_DRY_RUN

    def __init__(self):
        self.call_count = 0

    def is_configured(self) -> bool:
        return True

    async def publish(self, payload: PublishingPayload, dry_run: bool = False):
        self.call_count += 1
        if self.call_count < 3:
            raise ConnectionResetError(f"Temporary socket error on attempt {self.call_count}")
        return self._create_dry_run_receipt(payload, simulated_id_prefix="flaky_recovered")


@pytest.mark.asyncio
async def test_scenario_7_transient_error_retries_with_backoff(base_approved_campaign_context):
    flaky_adapter = FlakyAdapter()
    engine = PublishingEngine(max_retries=3)

    custom_adapters = {MarketingChannel.linkedin: flaky_adapter}
    ctx = base_approved_campaign_context.model_copy(deep=True)
    ctx.channels = [MarketingChannel.linkedin]

    _, report = await engine.execute_publishing(ctx, custom_adapters=custom_adapters)

    assert report.successful_dispatches == 1
    assert report.receipts[0].attempts == 3
    assert flaky_adapter.call_count == 3
    assert report.receipts[0].status == PublishingStatus.DRY_RUN_PUBLISHED


# ---------------------------------------------------------------------------
# Scenario 8: Partial Channel Failure Isolation & Exhausted Attempts
# ---------------------------------------------------------------------------
class PermanentFailingAdapter(BasePublishingAdapter):
    provider_type = ProviderType.META

    def is_configured(self) -> bool:
        return True

    async def publish(self, payload: PublishingPayload, dry_run: bool = False):
        raise PermissionError("Ad account suspended by policy review.")


@pytest.mark.asyncio
async def test_scenario_8_partial_channel_failure_isolation(base_approved_campaign_context):
    failing_adapter = PermanentFailingAdapter()
    working_adapter = MockDryRunAdapter()

    custom_adapters = {
        MarketingChannel.facebook: failing_adapter,
        MarketingChannel.linkedin: working_adapter,
    }
    ctx = base_approved_campaign_context.model_copy(deep=True)
    ctx.channels = [MarketingChannel.facebook, MarketingChannel.linkedin]

    engine = PublishingEngine(max_retries=2)
    _, report = await engine.execute_publishing(ctx, custom_adapters=custom_adapters)

    assert report.total_channels == 2
    assert report.successful_dispatches == 1
    assert report.failed_dispatches == 1

    fb_receipt = next(r for r in report.receipts if r.channel == MarketingChannel.facebook)
    li_receipt = next(r for r in report.receipts if r.channel == MarketingChannel.linkedin)

    assert fb_receipt.status == PublishingStatus.FAILED
    assert "suspended" in fb_receipt.error_message.lower()
    assert li_receipt.status == PublishingStatus.DRY_RUN_PUBLISHED


# ---------------------------------------------------------------------------
# Scenario 9: Non-Silent Operational Audit Logging
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_scenario_9_non_silent_audit_logging(base_approved_campaign_context):
    audit_store = HITLAuditStore()
    audit_logger = PublishingAuditLogger(hitl_audit_store=audit_store)
    engine = PublishingEngine(audit_logger=audit_logger)

    _, report = await engine.execute_publishing(base_approved_campaign_context, force_dry_run=True)

    audits = audit_store.get_campaign_audits("camp-pub-p13")
    assert len(audits) >= 3  # One audit per dispatched channel

    for audit in audits:
        assert audit.agent == "publishing_agent"
        assert audit.stage.value == "publishing"
        assert "SAFE DRY-RUN" in audit.reason
        assert audit.modified_output["channel"] in ["linkedin", "facebook", "email"]
        assert audit.modified_output["status"] == "dry_run_published"


# ---------------------------------------------------------------------------
# Scenario 10: PublishingAgent Standalone Contract & Lifecycle Events
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_scenario_10_publishing_agent_standalone(base_approved_campaign_context):
    agent = PublishingAgent()
    assert agent.name == "publishing_agent"

    events_captured = []
    event_bus.subscribe(lambda ev: events_captured.append(ev.event_type.value))

    result_ctx = await agent.run(base_approved_campaign_context, force_dry_run=True)

    assert result_ctx.publishing is not None
    assert len(result_ctx.publishing.published_channels) == 3
    assert result_ctx.publishing.is_dry_run is True
    assert "publishing_agent" in result_ctx.agent_outputs

    assert AgentEventType.AGENT_STARTED.value in events_captured
    assert AgentEventType.AGENT_COMPLETED.value in events_captured


# ---------------------------------------------------------------------------
# Scenario 11: Master Orchestrator Stage 11 Integration
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_scenario_11_master_orchestrator_stage_11_integration(base_approved_campaign_context):
    orchestrator = MasterOrchestrator()
    plan = orchestrator.planner.plan(base_approved_campaign_context)

    # Verify publishing_agent is scheduled at Stage 11
    pub_steps = [s for s in plan.agent_sequence if s.agent_name == "publishing_agent"]
    assert len(pub_steps) == 1
    assert pub_steps[0].stage_order == 11

    # Mock monitoring agent to pass through
    async def mock_monitoring(ctx):
        return ctx

    orchestrator.register_runner("monitoring_agent", mock_monitoring)

    # Execute full orchestrator run through publishing
    result_context = await orchestrator.execute_plan(base_approved_campaign_context, plan)
    assert result_context is not None
    assert "publishing_agent" in result_context.agent_outputs
    assert result_context.publishing is not None
    assert result_context.execution_plan.status == WorkflowState.SUCCESS
