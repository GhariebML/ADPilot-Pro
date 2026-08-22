"""Phase 14 — Standalone Verification Script: Monitoring Agent & Closed-Loop Feedback.

Verifies:
1. Telemetry Ingestion & Metric Normalization (CTR, CPA, ROAS, CPC, Conversion Rate).
2. Mandatory MonitoringEvent contract fields.
3. Multi-KPI Anomaly Detection & Agent Feedback Attribution.
4. Composite Campaign Health Scoring (0-100 index).
5. ClosedLoopFeedbackController full loop execution:
   Publishing -> Live Campaign -> Monitoring -> Analytics -> Optimizer -> Correction -> Human Approval -> Execution.
6. Non-silent monitoring audit log persistence.
7. Master Orchestrator Stage 12 pipeline completion.
"""

from __future__ import annotations

import asyncio
import sys

from adpilot.agents.monitoring_agent import MonitoringAgent
from adpilot.hitl.audit import HITLAuditStore
from adpilot.hitl.schemas import HITLGateOutput, HumanDecisionType
from adpilot.monitoring.anomaly import AnomalyDetector
from adpilot.monitoring.audit import MonitoringAuditLogger
from adpilot.monitoring.closed_loop import ClosedLoopFeedbackController
from adpilot.monitoring.health import HealthEvaluator
from adpilot.monitoring.schemas import (
    AnomalyType,
    RawTelemetryPoint,
)
from adpilot.monitoring.telemetry import TelemetryIngestionEngine
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
    PublishingPackage,
    RLActionProposal,
    RLPolicyType,
    StrategyAgentOutput,
    TimelineSpec,
    ToneOfVoice,
    UTMParameters,
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
        positioning_statement="Apex Stream: Real-time event broker.",
        usp="Ultra-low latency streaming.",
        elevator_pitch="Stream events with zero drop rate.",
        tone_of_voice=ToneOfVoice.professional,
        brand_voice_guidelines="Clear and technical",
        primary_channels=[MarketingChannel.linkedin, MarketingChannel.facebook, MarketingChannel.email],
        messaging_pillars=[MessagingPillar(title="Speed", description="Sub-ms latency")],
        funnel_strategy=[
            FunnelStageStrategy(stage=FunnelStage.awareness, budget_allocation_percent=50.0, key_messages=["Intro"]),
            FunnelStageStrategy(stage=FunnelStage.conversion, budget_allocation_percent=50.0, key_messages=["Trial"]),
        ],
        target_persona_summary="Cloud Architects",
        key_differentiators=["Instant replication"],
        risks_and_considerations=["Integration overhead"],
        confidence=0.95,
    )

    content_out = ContentAgentOutput(
        headlines=["Next-Gen Real-Time Event Broker", "Stream Millions of Events/Sec"],
        primary_copy=["Stop batch lag with Apex streaming engine."],
        descriptions=["Real-time data infrastructure."],
        ctas=["Start Free Trial", "Book Demo"],
        keywords=["event streaming", "real-time broker"],
        content_calendar_note="Multi-channel release schedule",
    )

    design_out = DesignAgentOutput(
        generated_prompts=["Modern stream architecture diagram"],
        color_palette=["#1E3A8A", "#3B82F6"],
        visual_style="Minimalist Cloud",
        typography_recommendations=["Inter"],
        aspect_ratios=["1:1", "16:9"],
        brand_alignment_score=0.95,
    )

    opt_out = OptimizationOutput(
        policy_type=RLPolicyType.ppo,
        action_proposal=RLActionProposal(
            channel_allocations={
                MarketingChannel.linkedin.value: 0.50,
                MarketingChannel.facebook.value: 0.30,
                MarketingChannel.email.value: 0.20,
            },
            bid_multiplier=1.0,
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
        predicted_reward=4.2,
        confidence=0.92,
    )

    pub_pkg = PublishingPackage(
        headlines=["Next-Gen Real-Time Event Broker"],
        ctas=["Start Free Trial"],
        targeting_criteria=["Role: Cloud Architect"],
        budget_allocation={"linkedin": 10000.0, "facebook": 6000.0, "email": 4000.0},
        utm_parameters=UTMParameters(utm_source="adpilot", utm_medium="cpc", utm_campaign="camp-verify-p14"),
        campaign_metadata={"environment": "production"},
        is_dry_run=True,
        execution_mode="dry_run",
        published_channels=["linkedin", "facebook", "email"],
    )

    ctx = CampaignContext(
        campaign_id="camp-verify-p14",
        metadata=ContextMetadata(created_by="verify_phase14"),
        business=BusinessInfo(name="Apex Stream Inc", industry="Cloud Infrastructure", description="Real-time message broker"),
        product=ProductSpec(name="Apex Engine", product_type="saas", description="Event streaming engine", unique_selling_points=["Zero latency"]),
        goals=[CampaignGoal.lead_generation, CampaignGoal.brand_awareness],
        channels=[MarketingChannel.linkedin, MarketingChannel.facebook, MarketingChannel.email],
        budget=BudgetSpec(total_budget=20000.0, currency="USD", daily_budget_cap=800.0),
        timeline=TimelineSpec(duration_days=30),
        geography=Geography(target_countries=["US", "UK"]),
        kpis=KPITargets(target_cpa=45.0, target_roas=3.5, target_ctr=2.5),
        constraints=CampaignConstraints(max_cpa=65.0, min_roas=2.5, prohibited_keywords=["hack", "free"]),
        brand=BrandGuidelines(tone_of_voice=ToneOfVoice.professional, brand_colors=["#1E3A8A", "#3B82F6"]),
        approvals=ApprovalRequirements(human_approval_required=True, min_health_score=70.0),
        variables={},
    )

    ctx.strategy = strategy_out
    ctx.content = content_out
    ctx.design = design_out
    ctx.optimization = opt_out
    ctx.publishing = pub_pkg
    ctx.record_agent_output("strategy_agent", strategy_out)
    ctx.record_agent_output("content_agent", content_out)
    ctx.record_agent_output("design_agent", design_out)
    ctx.record_agent_output("optimization_agent", opt_out)
    ctx.record_agent_output("publishing_agent", pub_pkg)

    hitl_gate_out = HITLGateOutput(
        stage="publishing",
        decision=HumanDecisionType.FINAL_APPROVAL,
        approved_by="vp_eng",
        approved_at="2026-08-22T14:00:00Z",
        reason="Campaign verified and signed off for live monitoring.",
        is_approved=True,
        audit_id="audit-verify-p14-signoff",
    )
    ctx.record_agent_output("hitl_gate", hitl_gate_out)
    return ctx


def verify_telemetry_and_normalization():
    section("1. Telemetry Ingestion & Metric Normalization")
    points = [
        RawTelemetryPoint(
            campaign_id="camp-v14",
            channel="linkedin",
            impressions=10000,
            clicks=300,
            spend=600.0,
            conversions=15,
            revenue=2400.0,
        ),
        RawTelemetryPoint(
            campaign_id="camp-v14",
            channel="facebook",
            impressions=20000,
            clicks=500,
            spend=400.0,
            conversions=10,
            revenue=1600.0,
        ),
    ]

    snapshot = TelemetryIngestionEngine.normalize_telemetry_points("camp-v14", points)
    check("impressions aggregated correctly", snapshot.impressions == 30000)
    check("clicks aggregated correctly", snapshot.clicks == 800)
    check("spend aggregated correctly", snapshot.spend == 1000.0)
    check("conversions aggregated correctly", snapshot.conversions == 25)
    check("revenue aggregated correctly", snapshot.revenue == 4000.0)
    check("normalized CTR is 2.67%", snapshot.ctr == round(800 / 30000, 4))
    check("normalized CPC is $1.25", snapshot.cpc == 1.25)
    check("normalized CPA is $40.00", snapshot.cpa == 40.0)
    check("normalized ROAS is 4.0x", snapshot.roas == 4.0)


def verify_anomaly_detection_and_health():
    section("2. Anomaly Detection & Health Scoring")
    context = create_sample_context()

    # Degraded metrics: Low CTR (0.5%), High CPA ($90), Low ROAS (1.0x)
    bad_points = [
        RawTelemetryPoint(
            campaign_id=context.campaign_id,
            channel="linkedin",
            impressions=20000,
            clicks=100,  # 0.5% CTR
            spend=900.0,
            conversions=10,  # $90 CPA
            revenue=900.0,  # 1.0x ROAS
        )
    ]
    snapshot = TelemetryIngestionEngine.normalize_telemetry_points(context.campaign_id, bad_points)
    events = AnomalyDetector.detect_anomalies(context, snapshot)

    check("mandatory fields present on all events", all(bool(e.campaign_id and e.timestamp and e.metric and e.severity) for e in events))
    check("CTR drop anomaly detected", any(e.anomaly_type == AnomalyType.CTR_DROP for e in events))
    check("CPA spike anomaly detected", any(e.anomaly_type == AnomalyType.CPA_SPIKE for e in events))
    check("ROAS drop anomaly detected", any(e.anomaly_type == AnomalyType.ROAS_DROP for e in events))

    score, status, alerts, feedback = HealthEvaluator.evaluate_campaign_health(events)
    check("health score heavily penalized", score <= 50.0)
    check("stream status is degraded/critical", status in ["degraded", "critical"])
    check("alerts generated for anomalies", len(alerts) >= 3)
    check("feedback routed to content_agent", "content_agent" in feedback)
    check("feedback routed to optimization_agent", "optimization_agent" in feedback)


async def verify_monitoring_agent_standalone():
    section("3. MonitoringAgent Standalone Lifecycle")
    context = create_sample_context()
    audit_store = HITLAuditStore()
    audit_logger = MonitoringAuditLogger(hitl_audit_store=audit_store)
    agent = MonitoringAgent(audit_logger=audit_logger)

    ctx = await agent.run(context)
    check("context.monitoring populated", ctx.monitoring is not None)
    check("telemetry stream active", ctx.monitoring.telemetry_stream_active is True)
    check("agent_outputs recorded", "monitoring_agent" in ctx.agent_outputs)
    check("audit store recorded evaluation", len(audit_store.get_campaign_audits(context.campaign_id)) >= 1)


async def verify_closed_loop_feedback_and_orchestrator():
    section("4. Closed-Loop Feedback & Master Orchestrator Pipeline")
    context = create_sample_context()
    controller = ClosedLoopFeedbackController()

    degraded_points = [
        RawTelemetryPoint(
            campaign_id=context.campaign_id,
            channel="linkedin",
            impressions=10000,
            clicks=60,
            spend=1200.0,
            conversions=8,
            revenue=1000.0,
        )
    ]

    updated_ctx, result = await controller.execute_feedback_cycle(
        context=context,
        telemetry_feed=degraded_points,
        force_dry_run=True,
        auto_approve_hitl=True,
    )

    check("closed-loop feedback cycle ran analytics", result.analytics_run is True)
    check("closed-loop feedback cycle ran optimizer", result.optimization_run is True)
    check("closed-loop feedback cycle human approved", result.human_approved is True)
    check("closed-loop feedback cycle re-published", result.republished is True)

    # Master Orchestrator Stage 12 integration
    orchestrator = MasterOrchestrator()
    plan = orchestrator.planner.plan(context)
    full_ctx = await orchestrator.execute_plan(context, plan)

    check("orchestrator completed successfully", full_ctx.execution_plan.status == WorkflowState.SUCCESS)
    check("orchestrator monitoring output present", full_ctx.monitoring is not None)


def main():
    print("\n" + "#" * 72)
    print("  PHASE 14 -- MONITORING AGENT & CLOSED-LOOP FEEDBACK VERIFICATION")
    print("#" * 72)

    verify_telemetry_and_normalization()
    verify_anomaly_detection_and_health()
    asyncio.run(verify_monitoring_agent_standalone())
    asyncio.run(verify_closed_loop_feedback_and_orchestrator())

    print(f"\n{'=' * 72}")
    print(f"  ALL {passed_checks}/{total_checks} PHASE 14 CHECKS PASSED")
    print(f"{'=' * 72}\n")


if __name__ == "__main__":
    main()
