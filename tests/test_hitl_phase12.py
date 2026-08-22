"""Phase 12 — Comprehensive Test Suite for Human-in-the-Loop (HITL) Governance.

Covers:
1. Review Action & Risk Assessment
2. Strategy Approval Path
3. Content Approval & Edit Path (Copy modifications audited & applied)
4. Creative / Design Approval Path
5. Budget / Optimizer Override Path (Audited override flag, previous vs modified)
6. Publishing / Final Approval Gate
7. Rejection Path (Execution halted, auditable rejection reason)
8. Request Revision Path (Closed-loop correction with prompt directives)
9. Anti-Silent Override Protection (Validation errors on missing user or reason)
10. Complete Audit History & Record Invariance
11. Master Orchestrator Stage 10 Integration
12. Master Orchestrator Pause and Resumption via Human Sign-Off
"""

from __future__ import annotations

import pytest

from adpilot.core.exceptions import ValidationError
from adpilot.hitl.audit import HITLAuditStore
from adpilot.hitl.manager import HITLReviewManager
from adpilot.hitl.schemas import (
    ApprovalStage,
    HITLDecisionSubmission,
    HumanDecisionType,
    RiskLevel,
)
from adpilot.orchestrator.master_orchestrator import MasterOrchestrator
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
def hitl_campaign_context() -> CampaignContext:
    """Fixture providing an enriched CampaignContext across all pipeline outputs."""
    strategy_out = StrategyAgentOutput(
        positioning_statement="Apex Data Cloud: Streaming analytics for real-time scale.",
        usp="Sub-millisecond latency distributed engine.",
        elevator_pitch="Query petabytes of live data in milliseconds.",
        tone_of_voice=ToneOfVoice.professional,
        brand_voice_guidelines="Clear, authoritative, technical",
        primary_channels=[MarketingChannel.linkedin, MarketingChannel.facebook, MarketingChannel.email],
        messaging_pillars=[
            MessagingPillar(title="Speed", description="Sub-millisecond latency query responses"),
            MessagingPillar(title="Scale", description="Elastic cloud streaming cluster"),
        ],
        funnel_strategy=[
            FunnelStageStrategy(
                stage=FunnelStage.awareness,
                budget_allocation_percent=40.0,
                key_messages=["Stop waiting for slow batch queries"],
            ),
            FunnelStageStrategy(
                stage=FunnelStage.consideration,
                budget_allocation_percent=35.0,
                key_messages=["Benchmark comparison vs traditional data warehouses"],
            ),
            FunnelStageStrategy(
                stage=FunnelStage.conversion,
                budget_allocation_percent=25.0,
                key_messages=["Start 14-day free trial on enterprise cluster"],
            ),
        ],
        target_persona_summary="Data Engineers and VP Engineering",
        key_differentiators=["Distributed query federation", "Real-time indexing"],
        risks_and_considerations=["High technical barrier to entry"],
        confidence=0.92,
    )

    content_out = ContentAgentOutput(
        headlines=["Stream Data at Millisecond Speeds", "The Modern Enterprise Query Engine"],
        primary_copy=["Tired of slow batch processing? Apex Cloud delivers instant streaming metrics."],
        descriptions=["Discover the distributed real-time platform engineered for enterprise workloads."],
        ctas=["Start Free Trial", "Book Architecture Call"],
        keywords=["real-time analytics", "streaming database"],
        content_calendar_note="Multi-channel Q3 launch schedule",
    )

    design_out = DesignAgentOutput(
        generated_prompts=["Sleek dark mode data dashboard glowing blue telemetry nodes"],
        color_palette=["#1E3A8A", "#3B82F6", "#93C5FD"],
        visual_style="Minimalist Enterprise Cyberpunk",
        typography_recommendations=["Inter", "JetBrains Mono"],
        aspect_ratios=["1:1", "16:9"],
        brand_alignment_score=0.95,
    )

    opt_out = OptimizationOutput(
        policy_type=RLPolicyType.ppo,
        action_proposal=RLActionProposal(
            channel_allocations={
                MarketingChannel.linkedin.value: 0.55,
                MarketingChannel.facebook.value: 0.25,
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
                MarketingChannel.linkedin.value: 0.55,
                MarketingChannel.facebook.value: 0.25,
                MarketingChannel.email.value: 0.20,
            },
            approved_by_safety_gate=True,
        ),
        predicted_reward=4.2,
        confidence=0.92,
    )

    ctx = CampaignContext(
        campaign_id="camp-hitl-test",
        metadata=ContextMetadata(created_by="hitl_test_suite"),
        business=BusinessInfo(
            name="Apex Data Cloud",
            industry="Cloud Infrastructure",
            description="Ultra low-latency distributed streaming database.",
        ),
        product=ProductSpec(
            name="Apex Engine",
            product_type="saas",
            description="Enterprise streaming analytics engine",
            unique_selling_points=["Sub-millisecond latency", "Distributed query federation"],
        ),
        goals=[CampaignGoal.lead_generation, CampaignGoal.brand_awareness],
        channels=[MarketingChannel.linkedin, MarketingChannel.facebook, MarketingChannel.email],
        budget=BudgetSpec(total_budget=30000.0, currency="USD", daily_budget_cap=1000.0),
        timeline=TimelineSpec(duration_days=30),
        geography=Geography(target_countries=["US", "CA", "UK"]),
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

    return ctx


# ---------------------------------------------------------------------------
# Scenario 1: Review Action & Risk Assessment
# ---------------------------------------------------------------------------
def test_scenario_1_review_request_and_risk_assessment(hitl_campaign_context):
    manager = HITLReviewManager()
    request = manager.create_review_request(hitl_campaign_context, ApprovalStage.STRATEGY)

    assert request.campaign_id == "camp-hitl-test"
    assert request.stage == ApprovalStage.STRATEGY
    assert request.agent_name == "strategy_agent"
    assert request.risk_level == RiskLevel.HIGH
    assert "positioning_statement" in request.agent_recommendation
    assert request.status == "pending"


# ---------------------------------------------------------------------------
# Scenario 2: Strategy Approval Path
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_scenario_2_strategy_approval_path(hitl_campaign_context):
    audit_store = HITLAuditStore()
    manager = HITLReviewManager(audit_store_instance=audit_store)

    sub = HITLDecisionSubmission(
        user="sarah_cmo",
        decision=HumanDecisionType.APPROVE,
        reason="Targeting and messaging pillars align directly with Q3 enterprise strategy.",
    )

    updated_ctx, gate_out = await manager.process_decision(
        context=hitl_campaign_context,
        stage=ApprovalStage.STRATEGY,
        submission=sub,
    )

    assert gate_out.is_approved is True
    assert gate_out.decision == HumanDecisionType.APPROVE
    assert gate_out.approved_by == "sarah_cmo"

    # Verify audit trail
    audits = audit_store.get_campaign_audits("camp-hitl-test")
    assert len(audits) == 1
    assert audits[0].user == "sarah_cmo"
    assert audits[0].stage == ApprovalStage.STRATEGY
    assert audits[0].decision == HumanDecisionType.APPROVE
    assert audits[0].is_override is False


# ---------------------------------------------------------------------------
# Scenario 3: Content Approval & Edit Path
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_scenario_3_content_approval_and_edit_path(hitl_campaign_context):
    audit_store = HITLAuditStore()
    manager = HITLReviewManager(audit_store_instance=audit_store)

    edited_headlines = ["Stop Query Lag with Apex Real-Time Engine", "Distributed Streaming for High-Scale Data"]
    sub = HITLDecisionSubmission(
        user="marcus_copy_lead",
        decision=HumanDecisionType.EDIT,
        reason="Refined headline hooks for stronger B2B conversion appeal.",
        modified_output={"headlines": edited_headlines},
    )

    updated_ctx, gate_out = await manager.process_decision(
        context=hitl_campaign_context,
        stage=ApprovalStage.CONTENT,
        submission=sub,
    )

    assert gate_out.is_approved is True
    assert gate_out.decision == HumanDecisionType.EDIT
    assert updated_ctx.content.headlines == edited_headlines

    # Verify non-silent audit
    audits = audit_store.get_campaign_audits("camp-hitl-test")
    assert len(audits) == 1
    assert audits[0].modified_output == {"headlines": edited_headlines}
    assert audits[0].previous_output["headlines"] != edited_headlines


# ---------------------------------------------------------------------------
# Scenario 4: Creative / Design Approval Path
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_scenario_4_creative_design_approval_path(hitl_campaign_context):
    audit_store = HITLAuditStore()
    manager = HITLReviewManager(audit_store_instance=audit_store)

    sub = HITLDecisionSubmission(
        user="elena_creative_dir",
        decision=HumanDecisionType.APPROVE,
        reason="Visual style and glowing node aesthetic matches our cyber-enterprise branding guidelines.",
    )

    _, gate_out = await manager.process_decision(
        context=hitl_campaign_context,
        stage=ApprovalStage.CREATIVE,
        submission=sub,
    )

    assert gate_out.is_approved is True
    assert gate_out.stage == ApprovalStage.CREATIVE
    assert gate_out.approved_by == "elena_creative_dir"


# ---------------------------------------------------------------------------
# Scenario 5: Budget / Optimizer Override Path
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_scenario_5_budget_optimizer_override_path(hitl_campaign_context):
    audit_store = HITLAuditStore()
    manager = HITLReviewManager(audit_store_instance=audit_store)

    custom_channel_weights = {
        MarketingChannel.linkedin.value: 0.70,
        MarketingChannel.facebook.value: 0.15,
        MarketingChannel.email.value: 0.15,
    }
    proposal_dict = {
        "channel_allocations": custom_channel_weights,
        "bid_multiplier": 1.10,
        "suggested_frequency_cap": 3.0,
    }
    sub = HITLDecisionSubmission(
        user="david_head_growth",
        decision=HumanDecisionType.OVERRIDE,
        reason="Executive mandate to prioritize LinkedIn enterprise lead acquisition over Facebook display.",
        modified_output={"action_proposal": proposal_dict},
    )

    updated_ctx, gate_out = await manager.process_decision(
        context=hitl_campaign_context,
        stage=ApprovalStage.BUDGET_OPTIMIZER,
        submission=sub,
    )

    assert gate_out.is_approved is True
    assert gate_out.decision == HumanDecisionType.OVERRIDE
    assert updated_ctx.optimization.action_proposal.channel_allocations == custom_channel_weights
    assert updated_ctx.optimization.action_proposal.bid_multiplier == 1.10

    # Verify audit record reflects explicit override
    audits = audit_store.get_campaign_audits("camp-hitl-test")
    assert len(audits) == 1
    assert audits[0].is_override is True
    assert audits[0].user == "david_head_growth"


# ---------------------------------------------------------------------------
# Scenario 6: Publishing / Final Approval Gate
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_scenario_6_publishing_final_approval_gate(hitl_campaign_context):
    audit_store = HITLAuditStore()
    manager = HITLReviewManager(audit_store_instance=audit_store)

    sub = HITLDecisionSubmission(
        user="compliance_officer_alex",
        decision=HumanDecisionType.FINAL_APPROVAL,
        reason="All legal, GDPR, brand safety, and budget constraints formally validated for go-live.",
    )

    _, gate_out = await manager.process_decision(
        context=hitl_campaign_context,
        stage=ApprovalStage.PUBLISHING,
        submission=sub,
    )

    assert gate_out.is_approved is True
    assert gate_out.decision == HumanDecisionType.FINAL_APPROVAL
    assert gate_out.approved_by == "compliance_officer_alex"


# ---------------------------------------------------------------------------
# Scenario 7: Rejection Path
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_scenario_7_rejection_path_halts_execution(hitl_campaign_context):
    audit_store = HITLAuditStore()
    manager = HITLReviewManager(audit_store_instance=audit_store)

    sub = HITLDecisionSubmission(
        user="vp_marketing_karen",
        decision=HumanDecisionType.REJECT,
        reason="Targeting channels and value proposition are misaligned with our Q3 enterprise focus.",
    )

    _, gate_out = await manager.process_decision(
        context=hitl_campaign_context,
        stage=ApprovalStage.STRATEGY,
        submission=sub,
    )

    assert gate_out.is_approved is False
    assert gate_out.decision == HumanDecisionType.REJECT
    assert gate_out.requires_revision is False

    audits = audit_store.get_campaign_audits("camp-hitl-test")
    assert len(audits) == 1
    assert audits[0].decision == HumanDecisionType.REJECT
    assert "misaligned" in audits[0].reason


# ---------------------------------------------------------------------------
# Scenario 8: Request Revision with Closed-Loop Correction
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_scenario_8_request_revision_triggers_correction_engine(hitl_campaign_context):
    audit_store = HITLAuditStore()
    manager = HITLReviewManager(audit_store_instance=audit_store)

    directives = [
        "Focus headlines on sub-second query performance for 100TB datasets",
        "Add explicit 'Book Live Demo' CTA",
    ]
    sub = HITLDecisionSubmission(
        user="copywriter_lead",
        decision=HumanDecisionType.REQUEST_REVISION,
        reason="Initial copy was too generic; needs sharper technical specificity.",
        revision_directives=directives,
    )

    updated_ctx, gate_out = await manager.process_decision(
        context=hitl_campaign_context,
        stage=ApprovalStage.CONTENT,
        submission=sub,
    )

    assert gate_out.requires_revision is True
    assert gate_out.is_approved is False
    assert gate_out.revision_directives == directives
    assert updated_ctx.content is not None


# ---------------------------------------------------------------------------
# Scenario 9: Anti-Silent Override Protection
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_scenario_9_anti_silent_override_protection(hitl_campaign_context):
    from pydantic import ValidationError as PydanticValidationError
    manager = HITLReviewManager()

    # 1. Missing user identifier
    with pytest.raises((ValidationError, PydanticValidationError)):
        await manager.process_decision(
            context=hitl_campaign_context,
            stage=ApprovalStage.CONTENT,
            submission=HITLDecisionSubmission(
                user=" ",
                decision=HumanDecisionType.APPROVE,
                reason="Looks good",
            ),
        )

    # 2. Insufficient reason
    with pytest.raises((ValidationError, PydanticValidationError)):
        await manager.process_decision(
            context=hitl_campaign_context,
            stage=ApprovalStage.CONTENT,
            submission=HITLDecisionSubmission(
                user="alice",
                decision=HumanDecisionType.APPROVE,
                reason="ok",
            ),
        )

    # 3. Edit / Override without modified payload
    with pytest.raises((ValidationError, PydanticValidationError)):
        await manager.process_decision(
            context=hitl_campaign_context,
            stage=ApprovalStage.CONTENT,
            submission=HITLDecisionSubmission(
                user="alice",
                decision=HumanDecisionType.EDIT,
                reason="Changed copy",
                modified_output=None,
            ),
        )


# ---------------------------------------------------------------------------
# Scenario 10: Complete Audit History & Storage Verification
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_scenario_10_complete_audit_history_verification(hitl_campaign_context):
    audit_store = HITLAuditStore()
    manager = HITLReviewManager(audit_store_instance=audit_store)

    stages_decisions = [
        (ApprovalStage.STRATEGY, HumanDecisionType.APPROVE, "Strategy sign-off", None),
        (ApprovalStage.CONTENT, HumanDecisionType.EDIT, "Copy tweak", {"headlines": ["Custom Headline"]}),
        (ApprovalStage.CREATIVE, HumanDecisionType.APPROVE, "Design sign-off", None),
        (ApprovalStage.BUDGET_OPTIMIZER, HumanDecisionType.OVERRIDE, "Budget shift", {"bid_multiplier": 1.2}),
        (ApprovalStage.PUBLISHING, HumanDecisionType.FINAL_APPROVAL, "Final deployment approved", None),
    ]

    current_ctx = hitl_campaign_context
    for stage, dec, rsn, mod in stages_decisions:
        current_ctx, _ = await manager.process_decision(
            context=current_ctx,
            stage=stage,
            submission=HITLDecisionSubmission(
                user="auditor_jane",
                decision=dec,
                reason=rsn,
                modified_output=mod,
            ),
        )

    audits = audit_store.get_campaign_audits("camp-hitl-test")
    assert len(audits) == 5

    # Check each mandatory audited attribute
    for audit in audits:
        assert audit.user == "auditor_jane"
        assert audit.campaign_id == "camp-hitl-test"
        assert audit.timestamp is not None
        assert audit.agent is not None
        assert audit.decision is not None
        assert audit.reason is not None
        assert audit.previous_output is not None


# ---------------------------------------------------------------------------
# Scenario 11: Master Orchestrator Stage 10 Integration
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_scenario_11_master_orchestrator_stage_10_integration(hitl_campaign_context):
    orchestrator = MasterOrchestrator()
    plan = orchestrator.planner.plan(hitl_campaign_context)

    # Mock custom runners for publishing and monitoring
    async def mock_pass(ctx):
        return ctx

    orchestrator.register_runner("publishing_agent", mock_pass)
    orchestrator.register_runner("monitoring_agent", mock_pass)

    result_ctx = await orchestrator.execute_plan(hitl_campaign_context, plan)
    assert result_ctx is not None
    assert "hitl_gate" in result_ctx.agent_outputs
    gate_record = result_ctx.agent_outputs["hitl_gate"]
    assert gate_record.is_approved is True
    assert gate_record.decision == HumanDecisionType.FINAL_APPROVAL


# ---------------------------------------------------------------------------
# Scenario 12: Master Orchestrator Pause and Resumption via Human Sign-Off
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_scenario_12_orchestrator_pause_and_resumption(hitl_campaign_context):
    orchestrator = MasterOrchestrator()
    plan = orchestrator.planner.plan(hitl_campaign_context)

    # Run with auto_approve_hitl = False to trigger pause at Stage 10
    paused_ctx = await orchestrator.execute_plan(hitl_campaign_context, plan, auto_approve_hitl=False)
    assert paused_ctx.execution_plan.status == WorkflowState.WAITING_FOR_APPROVAL

    # Submit human approval
    sub = HITLDecisionSubmission(
        user="release_manager_bob",
        decision=HumanDecisionType.FINAL_APPROVAL,
        reason="Manual sign-off after executive team review.",
    )
    resumed_ctx, gate_out = await orchestrator.submit_hitl_decision(
        context=paused_ctx,
        stage=ApprovalStage.PUBLISHING,
        submission=sub,
    )
    assert gate_out.is_approved is True

    # Mark stage 10 approved and resume execution
    async def mock_pass(ctx):
        return ctx

    orchestrator.register_runner("publishing_agent", mock_pass)
    orchestrator.register_runner("monitoring_agent", mock_pass)

    final_ctx = await orchestrator.execute_plan(resumed_ctx, resumed_ctx.execution_plan, auto_approve_hitl=True)
    assert final_ctx.execution_plan.status == WorkflowState.SUCCESS
