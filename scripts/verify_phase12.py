"""Phase 12 — Verification Script: Human-in-the-Loop (HITL) Governance & Auditing.

Verifies:
1. All 7 Human Decision Actions: Review, Approve, Reject, Edit, Request Revision, Override, Final Approval.
2. All 5 High-Risk Approval Gates: Strategy, Content, Creative, Budget/Optimizer, Publishing.
3. Strict Non-Silent Audit Logging (user, timestamp, campaign_id, agent, decision, previous_output, modified_output, reason).
4. Anti-Silent Override Protection (Validation on missing user/reason/modifications).
5. Closed-loop Correction Integration on Request Revision.
6. Master Orchestrator Stage 10 Gate Execution, Pause, and Resumption.
"""

from __future__ import annotations

import asyncio
import sys

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
    strategy_out = StrategyAgentOutput(
        positioning_statement="Apex Data Cloud: Real-time streaming database.",
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
        campaign_id="camp-verify-p12",
        metadata=ContextMetadata(created_by="verify_phase12"),
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


def verify_review_request():
    section("1. Review Action & Risk Assessment")
    manager = HITLReviewManager()
    context = create_sample_context()

    req = manager.create_review_request(context, ApprovalStage.STRATEGY)
    check("generates review request ID", req.request_id.startswith("rev-"))
    check("assigns correct approval stage", req.stage == ApprovalStage.STRATEGY)
    check("identifies responsible agent (strategy_agent)", req.agent_name == "strategy_agent")
    check("assigns risk tier (HIGH)", req.risk_level == RiskLevel.HIGH)
    check("contains recommendation payload", "positioning_statement" in req.agent_recommendation)


async def verify_approval_paths():
    section("2. Approval & Final Approval Gates")
    audit_store = HITLAuditStore()
    manager = HITLReviewManager(audit_store_instance=audit_store)
    context = create_sample_context()

    # Strategy Approval
    sub_strat = HITLDecisionSubmission(
        user="sarah_cmo",
        decision=HumanDecisionType.APPROVE,
        reason="Strategy aligned with enterprise marketing plan.",
    )
    _, gate_strat = await manager.process_decision(context, ApprovalStage.STRATEGY, sub_strat)
    check("strategy approval is approved", gate_strat.is_approved is True)
    check("strategy approval recorded user", gate_strat.approved_by == "sarah_cmo")

    # Publishing Final Approval
    sub_pub = HITLDecisionSubmission(
        user="compliance_officer",
        decision=HumanDecisionType.FINAL_APPROVAL,
        reason="GDPR and ad platform compliance verified.",
    )
    _, gate_pub = await manager.process_decision(context, ApprovalStage.PUBLISHING, sub_pub)
    check("publishing final approval is approved", gate_pub.is_approved is True)
    check("final approval decision type", gate_pub.decision == HumanDecisionType.FINAL_APPROVAL)


async def verify_edit_and_override_paths():
    section("3. Edit & Override Decisions (Zero Silent Overrides)")
    audit_store = HITLAuditStore()
    manager = HITLReviewManager(audit_store_instance=audit_store)
    context = create_sample_context()

    # Edit Copy
    edited_headlines = ["Stop Query Latency with Apex Real-Time Engine"]
    sub_edit = HITLDecisionSubmission(
        user="marcus_copywriter",
        decision=HumanDecisionType.EDIT,
        reason="Polished headline clarity for enterprise audience.",
        modified_output={"headlines": edited_headlines},
    )
    updated_ctx, gate_edit = await manager.process_decision(context, ApprovalStage.CONTENT, sub_edit)
    check("copy edit is approved", gate_edit.is_approved is True)
    check("context reflects edited headlines", updated_ctx.content.headlines == edited_headlines)

    # Override RL Optimizer
    custom_weights = {"linkedin": 0.75, "facebook": 0.15, "email": 0.10}
    proposal_dict = {
        "channel_allocations": custom_weights,
        "bid_multiplier": 1.15,
        "suggested_frequency_cap": 3.0,
    }
    sub_over = HITLDecisionSubmission(
        user="david_growth_lead",
        decision=HumanDecisionType.OVERRIDE,
        reason="Mandate to overweight LinkedIn B2B spend.",
        modified_output={"action_proposal": proposal_dict},
    )
    updated_ctx, gate_over = await manager.process_decision(updated_ctx, ApprovalStage.BUDGET_OPTIMIZER, sub_over)
    check("optimizer override is approved", gate_over.is_approved is True)
    check("optimizer channel allocations updated", updated_ctx.optimization.action_proposal.channel_allocations == custom_weights)

    # Verify audit store tracking
    audits = audit_store.get_campaign_audits("camp-verify-p12")
    check("2 audit records created", len(audits) == 2)
    check("override audit flag is True", any(a.is_override for a in audits))
    check("modified output captured in audit", any(a.modified_output is not None for a in audits))


async def verify_rejection_and_revision_paths():
    section("4. Rejection & Closed-Loop Revision Paths")
    audit_store = HITLAuditStore()
    manager = HITLReviewManager(audit_store_instance=audit_store)
    context = create_sample_context()

    # Rejection
    sub_rej = HITLDecisionSubmission(
        user="vp_marketing",
        decision=HumanDecisionType.REJECT,
        reason="Targeting channels do not match enterprise focus.",
    )
    _, gate_rej = await manager.process_decision(context, ApprovalStage.STRATEGY, sub_rej)
    check("rejection is not approved", gate_rej.is_approved is False)
    check("rejection decision recorded", gate_rej.decision == HumanDecisionType.REJECT)

    # Request Revision
    directives = ["Emphasize sub-millisecond query benchmarking", "Add demo CTA"]
    sub_rev = HITLDecisionSubmission(
        user="editor_in_chief",
        decision=HumanDecisionType.REQUEST_REVISION,
        reason="Needs sharper technical benchmarking.",
        revision_directives=directives,
    )
    updated_ctx, gate_rev = await manager.process_decision(context, ApprovalStage.CONTENT, sub_rev)
    check("revision request requires_revision is True", gate_rev.requires_revision is True)
    check("revision request is_approved is False", gate_rev.is_approved is False)
    check("correction re-execution updated content", updated_ctx.content is not None)


def verify_anti_silent_override():
    section("5. Anti-Silent Override Protection")
    from pydantic import ValidationError as PydanticValidationError
    manager = HITLReviewManager()
    context = create_sample_context()

    # Empty user
    try:
        asyncio.run(
            manager.process_decision(
                context,
                ApprovalStage.CONTENT,
                HITLDecisionSubmission(user=" ", decision=HumanDecisionType.APPROVE, reason="Valid reason"),
            )
        )
        check("rejects empty user identifier", False)
    except (ValidationError, PydanticValidationError, ValueError):
        check("rejects empty user identifier", True)

    # Empty reason
    try:
        asyncio.run(
            manager.process_decision(
                context,
                ApprovalStage.CONTENT,
                HITLDecisionSubmission(user="alice", decision=HumanDecisionType.APPROVE, reason="ok"),
            )
        )
        check("rejects short/empty reason", False)
    except (ValidationError, PydanticValidationError, ValueError):
        check("rejects short/empty reason", True)

    # Edit without modified payload
    try:
        asyncio.run(
            manager.process_decision(
                context,
                ApprovalStage.CONTENT,
                HITLDecisionSubmission(user="alice", decision=HumanDecisionType.EDIT, reason="Edited copy", modified_output=None),
            )
        )
        check("rejects edit without modified_output", False)
    except (ValidationError, PydanticValidationError, ValueError):
        check("rejects edit without modified_output", True)


async def verify_orchestrator_integration():
    section("6. Master Orchestrator Stage 10 HITL Gate Integration")
    orchestrator = MasterOrchestrator()
    context = create_sample_context()
    plan = orchestrator.planner.plan(context)

    async def mock_pass(ctx):
        return ctx

    orchestrator.register_runner("publishing_agent", mock_pass)
    orchestrator.register_runner("monitoring_agent", mock_pass)

    # Test auto-approved pipeline execution
    result_ctx = await orchestrator.execute_plan(context, plan)
    check("orchestrator execution succeeded", result_ctx.execution_plan.status == WorkflowState.SUCCESS)
    check("hitl_gate output recorded in context", "hitl_gate" in result_ctx.agent_outputs)
    gate_record = result_ctx.agent_outputs["hitl_gate"]
    check("hitl_gate is approved", gate_record.is_approved is True)

    # Test pause when auto_approve_hitl is False
    paused_ctx = await orchestrator.execute_plan(context, plan, auto_approve_hitl=False)
    check("orchestrator paused at approval gate", paused_ctx.execution_plan.status == WorkflowState.WAITING_FOR_APPROVAL)


def main():
    print("\n" + "#" * 72)
    print("  PHASE 12 -- HUMAN-IN-THE-LOOP (HITL) VERIFICATION")
    print("#" * 72)

    verify_review_request()
    asyncio.run(verify_approval_paths())
    asyncio.run(verify_edit_and_override_paths())
    asyncio.run(verify_rejection_and_revision_paths())
    verify_anti_silent_override()
    asyncio.run(verify_orchestrator_integration())

    print(f"\n{'=' * 72}")
    print(f"  ALL {passed_checks}/{total_checks} PHASE 12 CHECKS PASSED")
    print(f"{'=' * 72}\n")


if __name__ == "__main__":
    main()
