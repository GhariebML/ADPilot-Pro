"""Phase 14 — Monitoring Agent and Closed-Loop Feedback Test Suite.

Verifies:
1. Metric Normalization & Telemetry Ingestion (CTR, CPA, ROAS, CPC, Conversion Rate).
2. Mandatory MonitoringEvent Fields (campaign_id, timestamp, metric, value, expected_value, deviation, severity).
3. CTR Drop Anomaly Detection & Content Agent Attribution.
4. CPA Spike Anomaly Detection & Optimizer Attribution.
5. ROAS Drop Anomaly Detection & Strategy Attribution.
6. Composite Campaign Health Scoring (0-100 index).
7. Structured Prescriptive Alert Routing.
8. Performance Snapshot Time-Series Tracking.
9. MonitoringAgent Standalone Lifecycle Events & Contract Compliance.
10. Full Closed-Loop Feedback Controller Pipeline Execution.
11. Master Orchestrator Stage 12 Integration.
"""

from __future__ import annotations

import pytest

from adpilot.agents.monitoring_agent import MonitoringAgent
from adpilot.hitl.schemas import HITLGateOutput, HumanDecisionType
from adpilot.monitoring.anomaly import AnomalyDetector
from adpilot.monitoring.closed_loop import ClosedLoopFeedbackController
from adpilot.monitoring.health import HealthEvaluator
from adpilot.monitoring.schemas import (
    AlertSeverity,
    AnomalyType,
    PerformanceSnapshot,
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


@pytest.fixture
def base_monitored_context() -> CampaignContext:
    """Fixture providing a published and approved CampaignContext ready for monitoring."""
    ctx = CampaignContext(
        campaign_id="camp-mon-p14",
        metadata=ContextMetadata(created_by="test_monitoring_phase14"),
        business=BusinessInfo(
            name="QuantumSec",
            industry="Cybersecurity",
            description="Autonomous cloud security posture management",
        ),
        product=ProductSpec(
            name="CloudArmor",
            product_type="saas",
            description="Real-time automated CSPM and threat detection",
            unique_selling_points=["Sub-second detection", "Zero-day protection"],
        ),
        goals=[CampaignGoal.lead_generation, CampaignGoal.brand_awareness],
        channels=[MarketingChannel.linkedin, MarketingChannel.facebook, MarketingChannel.email],
        budget=BudgetSpec(total_budget=30000.0, currency="USD", daily_budget_cap=1000.0),
        timeline=TimelineSpec(duration_days=30),
        geography=Geography(target_countries=["US", "CA", "UK"]),
        kpis=KPITargets(target_cpa=40.0, target_roas=3.5, target_ctr=2.5),
        constraints=CampaignConstraints(max_cpa=60.0, min_roas=2.5, prohibited_keywords=["free", "hack"]),
        brand=BrandGuidelines(tone_of_voice=ToneOfVoice.professional, brand_colors=["#0F172A", "#38BDF8"]),
        approvals=ApprovalRequirements(human_approval_required=True, min_health_score=70.0),
        variables={},
    )

    strategy_out = StrategyAgentOutput(
        positioning_statement="Next-gen autonomous CSPM protecting enterprise cloud.",
        usp="Instant cloud security remediation.",
        elevator_pitch="Secure enterprise infrastructure automatically.",
        tone_of_voice=ToneOfVoice.professional,
        brand_voice_guidelines="Authoritative and clear",
        primary_channels=[MarketingChannel.linkedin, MarketingChannel.facebook, MarketingChannel.email],
        messaging_pillars=[MessagingPillar(title="Security", description="Zero breach record")],
        funnel_strategy=[
            FunnelStageStrategy(stage=FunnelStage.awareness, budget_allocation_percent=50.0, key_messages=["Intro"]),
            FunnelStageStrategy(stage=FunnelStage.conversion, budget_allocation_percent=50.0, key_messages=["Demo"]),
        ],
        target_persona_summary="CISO & DevSecOps",
        key_differentiators=["Autonomous repair"],
        risks_and_considerations=["Compliance complexity"],
        confidence=0.95,
    )

    content_out = ContentAgentOutput(
        headlines=["Eliminate Cloud Vulnerabilities", "Autonomous CSPM Platform"],
        primary_copy=["Protect AWS & GCP workloads with automated compliance."],
        descriptions=["Enterprise threat protection."],
        ctas=["Book Security Demo", "Start Trial"],
        keywords=["cloud security", "cspm"],
        content_calendar_note="Weekly deployment cadence",
    )

    design_out = DesignAgentOutput(
        generated_prompts=["Modern cybersecurity SOC dashboard"],
        color_palette=["#0F172A", "#38BDF8"],
        visual_style="Cyber Modern",
        typography_recommendations=["Inter"],
        aspect_ratios=["1:1", "16:9"],
        brand_alignment_score=0.94,
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
        predicted_reward=4.5,
        confidence=0.91,
    )

    publishing_pkg = PublishingPackage(
        headlines=["Eliminate Cloud Vulnerabilities"],
        ctas=["Book Security Demo"],
        targeting_criteria=["Role: CISO", "Industry: Tech"],
        budget_allocation={"linkedin": 15000.0, "facebook": 9000.0, "email": 6000.0},
        utm_parameters=UTMParameters(utm_source="adpilot", utm_medium="cpc", utm_campaign="camp-mon-p14"),
        campaign_metadata={"environment": "production"},
        is_dry_run=True,
        execution_mode="dry_run",
        published_channels=["linkedin", "facebook", "email"],
    )

    hitl_out = HITLGateOutput(
        stage="publishing",
        decision=HumanDecisionType.FINAL_APPROVAL,
        approved_by="ciso_ops",
        approved_at="2026-08-22T14:00:00Z",
        reason="Campaign verified and approved for monitoring.",
        is_approved=True,
        audit_id="audit-mon-gate-1",
    )

    ctx.strategy = strategy_out
    ctx.content = content_out
    ctx.design = design_out
    ctx.optimization = opt_out
    ctx.publishing = publishing_pkg
    ctx.record_agent_output("strategy_agent", strategy_out)
    ctx.record_agent_output("content_agent", content_out)
    ctx.record_agent_output("design_agent", design_out)
    ctx.record_agent_output("optimization_agent", opt_out)
    ctx.record_agent_output("publishing_agent", publishing_pkg)
    ctx.record_agent_output("hitl_gate", hitl_out)

    return ctx


# ---------------------------------------------------------------------------
# Scenario 1: Metric Normalization & Telemetry Ingestion
# ---------------------------------------------------------------------------
def test_scenario_1_metric_normalization_and_ingestion():
    raw_points = [
        RawTelemetryPoint(
            campaign_id="camp-test-1",
            channel="linkedin",
            impressions=10000,
            clicks=300,
            spend=600.0,
            conversions=15,
            revenue=2400.0,
        ),
        RawTelemetryPoint(
            campaign_id="camp-test-1",
            channel="facebook",
            impressions=20000,
            clicks=400,
            spend=400.0,
            conversions=10,
            revenue=1600.0,
        ),
    ]

    snapshot: PerformanceSnapshot = TelemetryIngestionEngine.normalize_telemetry_points(
        campaign_id="camp-test-1",
        points=raw_points,
    )

    assert snapshot.campaign_id == "camp-test-1"
    assert snapshot.impressions == 30000
    assert snapshot.clicks == 700
    assert snapshot.spend == 1000.0
    assert snapshot.conversions == 25
    assert snapshot.revenue == 4000.0

    # Normalized Rates
    assert snapshot.ctr == round(700 / 30000, 4)
    assert snapshot.cpc == round(1000.0 / 700, 2)
    assert snapshot.cpa == round(1000.0 / 25, 2)
    assert snapshot.roas == 4.0  # 4000 / 1000
    assert snapshot.conversion_rate == round(25 / 700, 4)

    # Per-channel breakdowns
    assert "linkedin" in snapshot.channel_breakdown
    assert "facebook" in snapshot.channel_breakdown
    assert snapshot.channel_breakdown["linkedin"]["roas"] == 4.0


# ---------------------------------------------------------------------------
# Scenario 2: Mandatory MonitoringEvent Schema Requirements
# ---------------------------------------------------------------------------
def test_scenario_2_monitoring_event_schema_contract(base_monitored_context):
    raw_points = TelemetryIngestionEngine.generate_simulated_stream_points(base_monitored_context)
    snapshot = TelemetryIngestionEngine.normalize_telemetry_points(base_monitored_context.campaign_id, raw_points)

    events = AnomalyDetector.detect_anomalies(base_monitored_context, snapshot)

    assert len(events) >= 3  # CTR, CPA, ROAS evaluated
    for ev in events:
        assert bool(ev.campaign_id)
        assert bool(ev.timestamp)
        assert bool(ev.metric)
        assert isinstance(ev.value, (int, float))
        assert isinstance(ev.expected_value, (int, float))
        assert isinstance(ev.deviation, (int, float))
        assert isinstance(ev.severity, AlertSeverity)


# ---------------------------------------------------------------------------
# Scenario 3: CTR Drop Anomaly Detection & Content Agent Attribution
# ---------------------------------------------------------------------------
def test_scenario_3_ctr_drop_anomaly_detection(base_monitored_context):
    # Inject poor CTR points (0.5% CTR vs 2.5% target)
    bad_ctr_points = [
        RawTelemetryPoint(
            campaign_id=base_monitored_context.campaign_id,
            channel="linkedin",
            impressions=20000,
            clicks=100,  # 0.5% CTR
            spend=500.0,
            conversions=10,
            revenue=1500.0,
        )
    ]
    snapshot = TelemetryIngestionEngine.normalize_telemetry_points(base_monitored_context.campaign_id, bad_ctr_points)
    events = AnomalyDetector.detect_anomalies(base_monitored_context, snapshot)

    ctr_events = [e for e in events if e.metric == "ctr" and e.severity in [AlertSeverity.WARNING, AlertSeverity.CRITICAL]]
    assert len(ctr_events) == 1
    assert ctr_events[0].anomaly_type == AnomalyType.CTR_DROP
    assert ctr_events[0].target_agent == "content_agent"
    assert ctr_events[0].deviation < -0.40


# ---------------------------------------------------------------------------
# Scenario 4: CPA Spike Anomaly Detection & Optimizer Attribution
# ---------------------------------------------------------------------------
def test_scenario_4_cpa_spike_anomaly_detection(base_monitored_context):
    # Inject high CPA ($90.0 vs $40 target and $60 max constraint)
    high_cpa_points = [
        RawTelemetryPoint(
            campaign_id=base_monitored_context.campaign_id,
            channel="linkedin",
            impressions=10000,
            clicks=400,
            spend=900.0,
            conversions=10,  # CPA = $90
            revenue=1200.0,
        )
    ]
    snapshot = TelemetryIngestionEngine.normalize_telemetry_points(base_monitored_context.campaign_id, high_cpa_points)
    events = AnomalyDetector.detect_anomalies(base_monitored_context, snapshot)

    cpa_events = [e for e in events if e.metric == "cpa" and e.severity == AlertSeverity.CRITICAL]
    assert len(cpa_events) == 1
    assert cpa_events[0].anomaly_type == AnomalyType.CPA_SPIKE
    assert cpa_events[0].target_agent == "optimization_agent"
    assert cpa_events[0].value == 90.0


# ---------------------------------------------------------------------------
# Scenario 5: ROAS Drop Anomaly Detection & Strategy Attribution
# ---------------------------------------------------------------------------
def test_scenario_5_roas_drop_anomaly_detection(base_monitored_context):
    # Inject low ROAS (1.0x vs 3.5x target and 2.5x min constraint)
    low_roas_points = [
        RawTelemetryPoint(
            campaign_id=base_monitored_context.campaign_id,
            channel="linkedin",
            impressions=10000,
            clicks=400,
            spend=1000.0,
            conversions=20,
            revenue=1000.0,  # ROAS = 1.0x
        )
    ]
    snapshot = TelemetryIngestionEngine.normalize_telemetry_points(base_monitored_context.campaign_id, low_roas_points)
    events = AnomalyDetector.detect_anomalies(base_monitored_context, snapshot)

    roas_events = [e for e in events if e.metric == "roas" and e.severity == AlertSeverity.CRITICAL]
    assert len(roas_events) == 1
    assert roas_events[0].anomaly_type == AnomalyType.ROAS_DROP
    assert roas_events[0].target_agent == "strategy_agent"


# ---------------------------------------------------------------------------
# Scenario 6: Composite Campaign Health Scoring
# ---------------------------------------------------------------------------
def test_scenario_6_campaign_health_scoring(base_monitored_context):
    # 1. Nominal telemetry -> Health score 100
    nominal_points = [
        RawTelemetryPoint(
            campaign_id=base_monitored_context.campaign_id,
            channel="linkedin",
            impressions=10000,
            clicks=350,  # 3.5% CTR
            spend=500.0,
            conversions=20,  # $25 CPA
            revenue=2000.0,  # 4.0x ROAS
        )
    ]
    snap_nom = TelemetryIngestionEngine.normalize_telemetry_points(base_monitored_context.campaign_id, nominal_points)
    events_nom = AnomalyDetector.detect_anomalies(base_monitored_context, snap_nom)
    score_nom, status_nom, _, _ = HealthEvaluator.evaluate_campaign_health(events_nom)
    assert score_nom == 100.0
    assert status_nom == "nominal"

    # 2. Degraded telemetry with multiple critical anomalies -> Health score reduced
    degraded_points = [
        RawTelemetryPoint(
            campaign_id=base_monitored_context.campaign_id,
            channel="linkedin",
            impressions=10000,
            clicks=80,  # Low CTR (-25 penalty)
            spend=1000.0,
            conversions=5,  # High CPA $200 (-25 penalty)
            revenue=800.0,  # Low ROAS 0.8x (-25 penalty)
        )
    ]
    snap_deg = TelemetryIngestionEngine.normalize_telemetry_points(base_monitored_context.campaign_id, degraded_points)
    events_deg = AnomalyDetector.detect_anomalies(base_monitored_context, snap_deg)
    score_deg, status_deg, alerts_deg, _ = HealthEvaluator.evaluate_campaign_health(events_deg)
    assert score_deg <= 50.0
    assert status_deg in ["degraded", "critical"]
    assert len(alerts_deg) >= 2


# ---------------------------------------------------------------------------
# Scenario 7: Structured Prescriptive Alert Routing
# ---------------------------------------------------------------------------
def test_scenario_7_prescriptive_alert_routing(base_monitored_context):
    degraded_points = [
        RawTelemetryPoint(
            campaign_id=base_monitored_context.campaign_id,
            channel="linkedin",
            impressions=10000,
            clicks=70,  # Low CTR
            spend=1000.0,
            conversions=5,  # High CPA
            revenue=900.0,
        )
    ]
    snap = TelemetryIngestionEngine.normalize_telemetry_points(base_monitored_context.campaign_id, degraded_points)
    events = AnomalyDetector.detect_anomalies(base_monitored_context, snap)
    _, _, alerts, agent_feedback = HealthEvaluator.evaluate_campaign_health(events)

    assert "content_agent" in agent_feedback
    assert "optimization_agent" in agent_feedback
    assert len(alerts) >= 2


# ---------------------------------------------------------------------------
# Scenario 8: MonitoringAgent Standalone Lifecycle Events & Contract Compliance
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_scenario_8_monitoring_agent_standalone_lifecycle(base_monitored_context):
    agent = MonitoringAgent()
    assert agent.name == "monitoring_agent"

    ctx = await agent.run(base_monitored_context)

    assert ctx.monitoring is not None
    assert ctx.monitoring.telemetry_stream_active is True
    assert "monitoring_agent" in ctx.agent_outputs
    assert agent.last_report is not None
    assert agent.last_report.campaign_id == base_monitored_context.campaign_id


# ---------------------------------------------------------------------------
# Scenario 9: Full Closed-Loop Feedback Controller Pipeline Execution
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_scenario_9_full_closed_loop_feedback_cycle(base_monitored_context):
    controller = ClosedLoopFeedbackController()

    # Ingest degraded telemetry to force closed loop correction and re-approval
    degraded_points = [
        RawTelemetryPoint(
            campaign_id=base_monitored_context.campaign_id,
            channel="linkedin",
            impressions=10000,
            clicks=60,  # Poor CTR
            spend=1200.0,
            conversions=8,  # High CPA $150
            revenue=1000.0,  # Poor ROAS
        )
    ]

    updated_ctx, result = await controller.execute_feedback_cycle(
        context=base_monitored_context,
        telemetry_feed=degraded_points,
        force_dry_run=True,
        auto_approve_hitl=True,
    )

    assert result.campaign_id == base_monitored_context.campaign_id
    assert result.analytics_run is True
    assert result.optimization_run is True
    assert result.human_approved is True
    assert result.republished is True
    assert updated_ctx.publishing is not None


# ---------------------------------------------------------------------------
# Scenario 10: Master Orchestrator Stage 12 Integration
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_scenario_10_master_orchestrator_stage_12_integration(base_monitored_context):
    orchestrator = MasterOrchestrator()
    plan = orchestrator.planner.plan(base_monitored_context)

    final_ctx = await orchestrator.execute_plan(base_monitored_context, plan)

    assert final_ctx.execution_plan.status == WorkflowState.SUCCESS
    assert final_ctx.monitoring is not None
    assert "monitoring_agent" in final_ctx.agent_outputs
    assert final_ctx.monitoring.telemetry_stream_active is True
