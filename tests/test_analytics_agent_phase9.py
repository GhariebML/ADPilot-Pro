"""Comprehensive test suite for Phase 9 — Analytics Agent & Performance Forecasting Engine."""

import pytest

from adpilot.agents import (
    AnalyticsAgent,
    CompetitorAgent,
    ContentAgent,
    CVAgent,
    DesignAgent,
    ResearchAgent,
    StrategyAgent,
)
from adpilot.core.agent_events import (
    AgentEventType,
    AgentLifecycleEvent,
    event_bus,
)
from adpilot.core.context_builder import CampaignContextBuilder
from adpilot.orchestrator.master_orchestrator import MasterOrchestrator
from adpilot.orchestrator.planner import CampaignPlanner
from adpilot.schemas.agent_schemas import (
    CampaignGoal,
    DataProvenance,
    MarketingChannel,
    PerformanceDeviation,
    PerformanceForecast,
    ProductType,
    RootCauseCandidate,
    ToneOfVoice,
)
from adpilot.services.model_loader import ModelLoader


@pytest.fixture
def phase9_campaign_context():
    """Create a canonical enterprise CampaignContext for Phase 9 testing."""
    return (
        CampaignContextBuilder.create("camp-phase9-test")
        .with_business(
            name="ScaleFlow AI",
            industry="B2B Enterprise SaaS",
            tagline="Enterprise Multi-Agent Orchestration",
            website_url="https://scaleflow.ai",
        )
        .with_product(
            name="ScaleFlow Orchestrator",
            product_type=ProductType.saas,
            description="Autonomous multi-agent orchestration platform for enterprise revenue and operations.",
        )
        .with_audience(
            summary="Chief Technology Officers, VP Engineering, and Enterprise Architects at Global 2000 companies.",
            demographics={"age_range": "35-55", "seniority": "Executive", "tech_savviness": "High"},
            psychographics=["Values operational efficiency", "Prioritizes system uptime and enterprise security"],
            pain_points=["Manual campaign coordination delays", "Lack of cross-channel visibility"],
        )
        .with_geography(
            target_countries=["US", "GB", "DE"],
            languages=["en"],
        )
        .with_budget(
            total_budget=80000.0,
            currency="USD",
            daily_budget_cap=2700.0,
        )
        .with_channels([
            MarketingChannel.linkedin,
            MarketingChannel.facebook,
            MarketingChannel.email,
        ])
        .with_timeline(
            duration_days=90,
            start_date="2026-09-01T00:00:00Z",
            end_date="2026-11-30T23:59:59Z",
        )
        .with_goals([
            CampaignGoal.lead_generation,
            CampaignGoal.brand_awareness,
        ])
        .with_brand(
            tone_of_voice=ToneOfVoice.authoritative,
            brand_colors=["#1E3A8A", "#3B82F6", "#FFFFFF"],
            dos_and_donts=[
                "Focus on enterprise reliability and ROI",
                "Maintain clean dark tech minimalism",
            ],
        )
        .with_competitors(["LegacyFlow Corp", "AutoWorkflow Systems"])
        .build()
    )


@pytest.mark.asyncio
async def test_analytics_agent_standalone_with_full_context(phase9_campaign_context):
    """Test AnalyticsAgent standalone execution after upstream stages 1 to 6."""
    event_bus.clear()
    emitted_events: list[AgentLifecycleEvent] = []
    event_bus.subscribe(lambda e: emitted_events.append(e))

    # Run stages 1 to 6
    context = await StrategyAgent().run(phase9_campaign_context)
    context = await ResearchAgent().run(context)
    context = await CompetitorAgent().run(context)
    context = await ContentAgent().run(context)
    context = await DesignAgent().run(context)
    context = await CVAgent().run(context)

    # Run Stage 7 Analytics Agent
    analytics_agent = AnalyticsAgent()
    result_context = await analytics_agent.run(context)

    assert result_context.analytics is not None
    analytics = result_context.analytics

    # 1. Verify Performance Forecast Output
    assert isinstance(analytics.forecast, PerformanceForecast)
    assert analytics.forecast.roas_forecast >= 1.0
    assert analytics.forecast.forecast_revenue_usd > 0.0
    assert 0.0 <= analytics.forecast.ctr_forecast_percent <= 100.0
    assert analytics.forecast.cpa_forecast_usd > 0.0
    assert 0.0 <= analytics.forecast.conversion_rate_percent <= 100.0
    assert analytics.forecast.forecast_conversions > 0
    assert analytics.forecast.forecast_clicks > 0
    assert analytics.forecast.forecast_impressions > 0

    # 2. Verify Performance Deviations
    assert len(analytics.performance_deviations) >= 2
    for dev in analytics.performance_deviations:
        assert isinstance(dev, PerformanceDeviation)
        assert dev.metric_name in {"ROAS", "CTR", "CPA"}
        assert dev.status in {"on_track", "underperforming", "overperforming"}
        assert len(dev.description) > 10

    # 3. Verify Root Cause Attribution
    assert len(analytics.root_cause_candidates) >= 1
    for rc in analytics.root_cause_candidates:
        assert isinstance(rc, RootCauseCandidate)
        assert len(rc.issue) > 5
        assert len(rc.probable_root_cause) > 10
        assert 0.0 <= rc.confidence <= 1.0
        assert len(rc.evidence) > 10

    # 4. Verify Actionable Optimization Directives
    assert len(analytics.recommendations) >= 2
    for rec in analytics.recommendations:
        assert isinstance(rec, str) and len(rec) > 15

    # 5. Verify Health Score & Quality Gate
    assert analytics.health_score.overall >= 70.0
    assert AnalyticsAgent.passes_quality_gate(analytics) is True

    # 6. Verify Data Provenance
    assert isinstance(analytics.provenance, DataProvenance)
    assert len(analytics.provenance.observed_data) >= 3
    assert len(analytics.provenance.model_prediction) >= 2
    assert len(analytics.provenance.llm_inference) >= 1
    assert len(analytics.provenance.recommendation) >= 1

    # 7. Verify Lifecycle Events
    analytics_events = [e for e in emitted_events if e.agent_id == "analytics_agent"]
    assert len(analytics_events) == 2
    assert analytics_events[0].event_type == AgentEventType.AGENT_STARTED
    assert analytics_events[1].event_type == AgentEventType.AGENT_COMPLETED


def test_analytics_ml_models_inference_deterministic():
    """Verify authentic ML models in research/models/analytics execute deterministically."""
    loader = ModelLoader()
    roas_model = loader.load_model("research/models/analytics/roas_predictor.pkl")
    rev_model = loader.load_model("research/models/analytics/revenue_forecaster.pkl")
    conv_model = loader.load_model("research/models/analytics/conversion_predictor.pkl")
    scaler = loader.load_model("research/models/analytics/scaler.pkl")

    assert roas_model is not None
    assert rev_model is not None
    assert conv_model is not None
    assert scaler is not None

    # Deterministic test feature vector
    raw_features = [[35.0, 5000.0, 30.0, 3.0, 1.0, 5000.0 / 30.0, 0.85]]
    scaled = scaler.transform(raw_features)

    roas_pred = float(roas_model.predict(scaled)[0])
    rev_pred = float(rev_model.predict(scaled)[0])

    assert 1.0 <= roas_pred <= 10.0
    assert rev_pred > 0.0


@pytest.mark.asyncio
async def test_end_to_end_strategy_research_competitor_content_design_cv_analytics_chain(phase9_campaign_context):
    """Test full sequential 7-stage pipeline execution chain."""
    event_bus.clear()
    emitted_events: list[AgentLifecycleEvent] = []
    event_bus.subscribe(lambda e: emitted_events.append(e))

    # Sequential execution: Stage 1 to 7
    context = await StrategyAgent().run(phase9_campaign_context)
    context = await ResearchAgent().run(context)
    context = await CompetitorAgent().run(context)
    context = await ContentAgent().run(context)
    context = await DesignAgent().run(context)
    context = await CVAgent().run(context)
    context = await AnalyticsAgent().run(context)

    assert context.strategy is not None
    assert context.research is not None
    assert context.competitors is not None
    assert context.content is not None
    assert context.design is not None
    assert "cv_agent" in context.agent_outputs
    assert context.analytics is not None

    # Verify event bus recorded all 7 stages (7 started + 7 completed = 14 events)
    completed_events = [e for e in emitted_events if e.event_type == AgentEventType.AGENT_COMPLETED]
    assert len(completed_events) == 7
    completed_agents = [e.agent_id for e in completed_events]
    assert completed_agents == [
        "strategy_agent",
        "research_agent",
        "competitor_agent",
        "content_agent",
        "design_agent",
        "cv_agent",
        "analytics_agent",
    ]


@pytest.mark.asyncio
async def test_orchestrator_integration_with_phase9_analytics(phase9_campaign_context):
    """Test MasterOrchestrator execution of a 7-stage plan including AnalyticsAgent."""
    planner = CampaignPlanner()
    plan = planner.plan(phase9_campaign_context)

    # Filter plan to stages 1–7
    target_stages = {
        "strategy_agent",
        "research_agent",
        "competitor_agent",
        "content_agent",
        "design_agent",
        "cv_agent",
        "analytics_agent",
    }
    plan.agent_sequence = [s for s in plan.agent_sequence if s.agent_name in target_stages]
    plan.total_steps = len(plan.agent_sequence)

    orchestrator = MasterOrchestrator()
    final_context = await orchestrator.execute_plan(context=phase9_campaign_context, plan=plan)

    assert final_context.strategy is not None
    assert final_context.content is not None
    assert final_context.design is not None
    assert final_context.analytics is not None
    assert final_context.analytics.forecast is not None
    assert final_context.analytics.forecast.roas_forecast >= 1.0
    assert len(final_context.analytics.performance_deviations) >= 1
