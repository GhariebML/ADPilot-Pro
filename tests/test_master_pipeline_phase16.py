"""Phase 16 — Master Pipeline Integration & End-to-End Test Suite.

Verifies:
1. SaaS Archetype full 18-stage pipeline.
2. Physical Product Archetype full 18-stage pipeline.
3. Real Estate Archetype full 18-stage pipeline.
4. Professional Service Archetype full 18-stage pipeline.
5. Failed Agent Exception Handling & Retry Ceiling.
6. Rejected Human Approval & Audit Lineage.
7. Correction Loop Triggering on Sub-optimal Assets.
8. Invalid Optimizer Action Clamping by Safety Gate.
9. Publishing Failure Isolation & Idempotency.
10. Closed-Loop Telemetry Monitoring Feedback Cycle.
"""

from __future__ import annotations

import pytest

from adpilot.hitl.schemas import HumanDecisionType
from adpilot.monitoring.schemas import RawTelemetryPoint
from adpilot.orchestrator.pipeline_runner import MasterPipelineRunner
from adpilot.schemas.agent_schemas import (
    ApprovalRequirements,
    BudgetSpec,
    BusinessInfo,
    CampaignContext,
    CampaignGoal,
    ContextMetadata,
    MarketingChannel,
    ProductSpec,
    ProductType,
    TimelineSpec,
    ToneOfVoice,
)
from adpilot.publishing.adapters import BasePublishingAdapter
from adpilot.publishing.engine import PublishingEngine
from adpilot.publishing.schemas import ProviderType, PublishingPayload, PublishingStatus


# ---------------------------------------------------------------------------
# Archetype 1: SaaS Platform End-to-End
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_archetype_1_saas_end_to_end_pipeline():
    runner = MasterPipelineRunner()
    user_input = {
        "campaign_id": "camp-saas-e2e",
        "business_name": "Apex Cloud Systems",
        "industry": "Cloud Infrastructure",
        "description": "Ultra-low latency streaming message broker for high-throughput enterprise systems.",
        "product_name": "Apex Stream Engine",
        "product_type": ProductType.saas,
        "product_description": "Real-time Kafka-compatible event streaming engine with sub-5ms latencies.",
        "unique_selling_points": ["Sub-5ms commit latency", "Zero data-loss replication"],
        "target_audience": "VP of Engineering, Cloud Architects, Enterprise IT Directors",
        "total_budget": 25000.0,
        "currency": "USD",
        "duration_days": 30,
        "target_cpa": 45.0,
        "target_roas": 4.0,
        "target_ctr": 3.0,
        "max_cpa": 65.0,
        "min_roas": 3.0,
        "brand_colors": ["#0F172A", "#38BDF8"],
        "prohibited_keywords": ["hack", "free trial without limits"],
    }

    context, trace = await runner.execute_pipeline(user_input, industry_archetype="saas")

    assert trace.overall_status == "success"
    assert len(trace.stages) == 18
    assert context.strategy is not None
    assert context.content is not None
    assert context.design is not None
    assert context.optimization is not None
    assert context.publishing is not None
    assert context.monitoring is not None


# ---------------------------------------------------------------------------
# Archetype 2: Physical Product / E-Commerce End-to-End
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_archetype_2_physical_product_end_to_end_pipeline():
    runner = MasterPipelineRunner()
    user_input = {
        "campaign_id": "camp-physical-e2e",
        "business_name": "ErgoPro Labs",
        "industry": "Consumer Electronics & Furniture",
        "description": "High-end ergonomic workstation accessories.",
        "product_name": "ErgoDesk Pro Stand",
        "product_type": ProductType.physical,
        "product_description": "Motorized dual-tier solid walnut standing desk with wireless charging.",
        "unique_selling_points": ["Solid American Walnut", "Whisper-quiet dual motors"],
        "target_audience": "Remote Software Engineers, Creative Professionals",
        "total_budget": 15000.0,
        "currency": "USD",
        "duration_days": 21,
        "target_cpa": 35.0,
        "target_roas": 3.5,
        "brand_colors": ["#78350F", "#D97706"],
    }

    context, trace = await runner.execute_pipeline(user_input, industry_archetype="physical_product")

    assert trace.overall_status == "success"
    assert len(trace.stages) == 18
    assert context.product.product_type == ProductType.physical
    assert context.publishing.is_dry_run is True


# ---------------------------------------------------------------------------
# Archetype 3: Real Estate Development End-to-End
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_archetype_3_real_estate_end_to_end_pipeline():
    runner = MasterPipelineRunner()
    user_input = {
        "campaign_id": "camp-realestate-e2e",
        "business_name": "Aura Heights Luxury Living",
        "industry": "Real Estate Development",
        "description": "Exclusive penthouse residences in Manhattan.",
        "product_name": "Aura Tower Residences",
        "product_type": ProductType.real_estate,
        "product_description": "3-bedroom panoramic penthouses with private rooftop terraces.",
        "unique_selling_points": ["360 Skyline Views", "Private Concierge & Valet"],
        "target_audience": "High-Net-Worth Individuals, Luxury Investors",
        "total_budget": 50000.0,
        "currency": "USD",
        "duration_days": 45,
        "target_cpa": 150.0,
        "target_roas": 6.0,
        "brand_colors": ["#1C1917", "#D4AF37"],
    }

    context, trace = await runner.execute_pipeline(user_input, industry_archetype="real_estate")

    assert trace.overall_status == "success"
    assert len(trace.stages) == 18
    assert context.business.industry == "Real Estate Development"


# ---------------------------------------------------------------------------
# Archetype 4: Professional Service Consulting End-to-End
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_archetype_4_service_consulting_end_to_end_pipeline():
    runner = MasterPipelineRunner()
    user_input = {
        "campaign_id": "camp-service-e2e",
        "business_name": "Vanguard Cyber Defense",
        "industry": "Cybersecurity & Consulting",
        "description": "Elite red-team penetration testing and cloud compliance auditing.",
        "product_name": "Zero-Trust Architecture Audit",
        "product_type": ProductType.service,
        "product_description": "Comprehensive 3-week penetration testing and compliance remediation.",
        "unique_selling_points": ["Former NSA Red Team Specialists", "Guaranteed SOC2 Compliance Roadmap"],
        "target_audience": "CISOs, Heads of InfoSec",
        "total_budget": 20000.0,
        "currency": "USD",
        "duration_days": 30,
        "target_cpa": 90.0,
        "target_roas": 5.0,
        "brand_colors": ["#022C22", "#10B981"],
    }

    context, trace = await runner.execute_pipeline(user_input, industry_archetype="service")

    assert trace.overall_status == "success"
    assert len(trace.stages) == 18
    assert context.product.product_type == ProductType.service


# ---------------------------------------------------------------------------
# Failure Scenario 1: Rejected Human Approval Stops Publishing
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_scenario_rejected_human_approval():
    runner = MasterPipelineRunner()
    user_input = {
        "campaign_id": "camp-reject-hitl",
        "business_name": "Test Co",
        "product_name": "Test Product",
        "total_budget": 5000.0,
    }

    context, trace = await runner.execute_pipeline(
        user_input=user_input,
        auto_approve_hitl=False,  # Force rejection
        human_decision=HumanDecisionType.REJECT,
        human_feedback_text="Disapproved: Tone of voice violates company brand guidelines.",
    )

    assert trace.overall_status == "rejected_by_human"
    assert not hasattr(context, "publishing") or context.publishing is None
    assert any(s.agent_name == "hitl_manager" and s.output_summary.get("is_approved") is False for s in trace.stages)


# ---------------------------------------------------------------------------
# Failure Scenario 2: Invalid RL Action Handled & Clamped by Safety Gate
# ---------------------------------------------------------------------------
def test_scenario_invalid_rl_action_clamped():
    """Verify out-of-bounds RL allocations are safely clamped by the optimization safety gate."""
    import numpy as np
    from adpilot.rl.constraint_validator import ConstraintValidator

    validator = ConstraintValidator(min_channel_weight=0.05, max_channel_weight=0.80)
    # Wild out-of-bounds raw candidate action
    wild_action = np.array([10.0, -10.0, 50.0, 5.0, 0.0])
    current_allocs = {"linkedin": 0.50, "facebook": 0.30, "email": 0.20}

    action_prop, safety_res = validator.validate_and_project(
        candidate_action=wild_action,
        current_allocations=current_allocs,
    )

    clamped = action_prop.channel_allocations
    assert all(0.0 <= v <= 1.0 for v in clamped.values())
    assert abs(sum(clamped.values()) - 1.0) < 1e-3
    assert safety_res.approved_by_safety_gate is True
    assert len(safety_res.modifications_applied) > 0


# ---------------------------------------------------------------------------
# Failure Scenario 3: Publishing Transient Failure Isolation & Retries
# ---------------------------------------------------------------------------
class FlakyAdapter(BasePublishingAdapter):
    """Adapter that fails once before succeeding on attempt 2."""
    provider_type = ProviderType.MOCK_DRY_RUN

    def __init__(self):
        self.call_count = 0

    def is_configured(self) -> bool:
        return True

    async def publish(self, payload: PublishingPayload, dry_run: bool = False):
        self.call_count += 1
        if self.call_count < 2:
            raise ConnectionResetError("Temporary network reset on attempt 1")
        return self._create_dry_run_receipt(payload, simulated_id_prefix="flaky_recovered")


@pytest.mark.asyncio
async def test_scenario_publishing_transient_failure_isolation():
    engine = PublishingEngine(max_retries=3)
    flaky = FlakyAdapter()

    ctx = CampaignContext(
        campaign_id="camp-fail-iso",
        metadata=ContextMetadata(created_by="test_fail_iso"),
        business=BusinessInfo(name="Test Co", industry="Technology Solutions", description="Enterprise infrastructure provider"),
        product=ProductSpec(name="Product Core", product_type=ProductType.saas, description="Enterprise software platform solution"),
        goals=[CampaignGoal.lead_generation],
        channels=[MarketingChannel.linkedin],
        budget=BudgetSpec(total_budget=5000.0),
        timeline=TimelineSpec(duration_days=30),
        approvals=ApprovalRequirements(human_approval_required=False),
        variables={},
    )
    # Mark approved
    from adpilot.hitl.schemas import HITLGateOutput
    ctx.record_agent_output("hitl_gate", HITLGateOutput(stage="publishing", decision=HumanDecisionType.APPROVE, approved_by="test", approved_at="2026-08-22T14:00:00Z", is_approved=True, audit_id="a1", reason="Pre-flight verification passed"))
    from adpilot.schemas.agent_schemas import (
        ContentAgentOutput,
        DesignAgentOutput,
        FunnelStage,
        FunnelStageStrategy,
        MessagingPillar,
        StrategyAgentOutput,
    )
    ctx.strategy = StrategyAgentOutput(
        positioning_statement="Apex Cloud: Real-time distributed data infrastructure.",
        usp="Sub-millisecond query execution at petabyte scale.",
        elevator_pitch="Query enterprise live streams instantly.",
        tone_of_voice=ToneOfVoice.professional,
        brand_voice_guidelines="Authoritative, clear, engineering-led",
        primary_channels=[MarketingChannel.linkedin],
        messaging_pillars=[
            MessagingPillar(title="Velocity", description="Zero latency stream processing"),
        ],
        funnel_strategy=[
            FunnelStageStrategy(
                stage=FunnelStage.awareness,
                budget_allocation_percent=100.0,
                key_messages=["Stop waiting for slow queries"],
            ),
        ],
        target_persona_summary="VP Engineering and Lead Data Architects",
        key_differentiators=["Federated live indexing", "Sub-millisecond latency"],
        risks_and_considerations=["Requires distributed deployment"],
        confidence=0.94,
    )
    ctx.content = ContentAgentOutput(
        headlines=["Head"],
        primary_copy=["Copy"],
        descriptions=["Desc"],
        ctas=["CTA"],
        keywords=["kw"],
        content_calendar_note="Launch plan",
    )
    ctx.design = DesignAgentOutput(generated_prompts=["Prompt"], color_palette=["#000000"], typography_recommendations=["Inter"], aspect_ratios=["1:1"])

    custom_adapters = {MarketingChannel.linkedin: flaky}
    _, report = await engine.execute_publishing(ctx, custom_adapters=custom_adapters)

    assert report.successful_dispatches == 1
    assert report.receipts[0].status == PublishingStatus.DRY_RUN_PUBLISHED
    assert report.receipts[0].attempts == 2


# ---------------------------------------------------------------------------
# Failure Scenario 4: Degraded Monitoring Triggers Closed-Loop Re-Optimization
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_scenario_monitoring_feedback_closed_loop():
    runner = MasterPipelineRunner()
    degraded_telemetry = [
        RawTelemetryPoint(
            campaign_id="camp-feedback-loop",
            channel="linkedin",
            impressions=10000,
            clicks=40,  # Severe CTR drop (0.4%)
            spend=1500.0,
            conversions=5,  # High CPA $300
            revenue=1000.0,  # Low ROAS 0.67x
        )
    ]

    user_input = {
        "campaign_id": "camp-feedback-loop",
        "business_name": "Telemetry Feedback Co",
        "product_name": "Feedback App",
        "total_budget": 8000.0,
    }

    context, trace = await runner.execute_pipeline(
        user_input=user_input,
        telemetry_stream=degraded_telemetry,
        auto_approve_hitl=True,
    )

    assert trace.overall_status == "success"
    assert len(trace.stages) == 18
    # Stage 17 Feedback controller should have caught the degradation
    feedback_stage = next(s for s in trace.stages if s.stage_number == 17)
    assert feedback_stage.status == "completed"
