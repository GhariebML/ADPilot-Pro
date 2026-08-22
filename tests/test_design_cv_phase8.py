"""Tests for Phase 8 — Design Agent, NanoBanana Integration, CV Agent, and Revision Loop."""

import pytest

from adpilot.agents import (
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
from adpilot.providers.image_provider import NanoBananaProviderAdapter
from adpilot.schemas.agent_schemas import (
    CampaignGoal,
    DataProvenance,
    MarketingChannel,
    ProductType,
    ToneOfVoice,
)


@pytest.fixture
def phase8_campaign_context():
    """Create a canonical CampaignContext for Phase 8 testing."""
    return (
        CampaignContextBuilder.create("camp-phase8-test")
        .with_business(name="ScaleFlow AI", industry="B2B Enterprise SaaS")
        .with_product(
            name="ScaleFlow Orchestrator",
            product_type=ProductType.saas,
            description="Autonomous multi-agent orchestration platform for enterprise operations",
        )
        .with_audience(
            summary="Chief Technology Officers, VP Engineering, and Enterprise Architects",
        )
        .with_geography(
            target_countries=["US", "GB", "DE"],
        )
        .with_budget(total_budget=80000.0, currency="USD")
        .with_channels([MarketingChannel.linkedin, MarketingChannel.facebook, MarketingChannel.email])
        .with_timeline(duration_days=90)
        .with_goals([CampaignGoal.lead_generation, CampaignGoal.brand_awareness])
        .with_brand(
            tone_of_voice=ToneOfVoice.authoritative,
            brand_colors=["#1E3A8A", "#3B82F6", "#FFFFFF"],
            dos_and_donts=["Focus on enterprise security", "Never make unsubstantiated claims"],
        )
        .with_competitors(["LegacyFlow Corp", "AutoWorkflow Systems"])
        .build()
    )


@pytest.mark.asyncio
async def test_nanobanana_provider_unconfigured_behavior():
    """Verify that unconfigured NanoBanana reports missing credentials and does NOT fake generation."""
    adapter = NanoBananaProviderAdapter(api_key=None)
    assert adapter.is_available() is False

    result = await adapter.generate_image(
        prompt="A high-tech enterprise interface",
        width=1200,
        height=628,
    )

    assert result.status == "unconfigured"
    assert result.image_url is None
    assert result.placeholder_url.startswith("https://placehold.co/1200x628.png")
    assert "NANOBANANA_API_KEY" in result.error_message


@pytest.mark.asyncio
async def test_design_agent_generates_creative_assets_and_metadata(phase8_campaign_context):
    """Test DesignAgent creating multi-channel assets, metadata, and diffusion prompts."""
    event_bus.clear()
    emitted_events: list[AgentLifecycleEvent] = []
    event_bus.subscribe(lambda e: emitted_events.append(e))

    # Pre-populate upstream context
    strategy_agent = StrategyAgent()
    research_agent = ResearchAgent()
    competitor_agent = CompetitorAgent()
    content_agent = ContentAgent()
    design_agent = DesignAgent()

    context = await strategy_agent.run(phase8_campaign_context)
    context = await research_agent.run(context)
    context = await competitor_agent.run(context)
    context = await content_agent.run(context)

    result_context = await design_agent.run(context)
    assert result_context.design is not None
    design = result_context.design

    # 1. Creative Assets Verification
    assert len(design.creative_assets) >= 3
    for asset in design.creative_assets:
        assert asset.dimensions.width > 0
        assert asset.dimensions.height > 0
        assert len(asset.generation_prompt) > 20
        assert len(asset.negative_prompt) > 0
        assert asset.generation_status in {"unconfigured", "placeholder", "generated"}
        assert asset.placeholder_url.startswith("https://placehold.co/")

    # 2. Creative Metadata
    assert design.creative_metadata is not None
    assert design.creative_metadata.layout_type is not None
    assert design.creative_metadata.primary_color_hex in phase8_campaign_context.brand.brand_colors

    # 3. Provenance & Event Bus
    assert isinstance(design.provenance, DataProvenance)
    assert len(design.provenance.observed_data) > 0
    assert len(design.provenance.model_prediction) > 0
    assert len(design.evidence) > 0

    design_events = [e for e in emitted_events if e.agent_id == "design_agent"]
    assert len(design_events) == 2
    assert design_events[0].event_type == AgentEventType.AGENT_STARTED
    assert design_events[1].event_type == AgentEventType.AGENT_COMPLETED


@pytest.mark.asyncio
async def test_cv_agent_multi_model_evaluation(phase8_campaign_context):
    """Test CVAgent aesthetic scoring, OCR inspection, brand compliance, and object detection."""
    event_bus.clear()
    emitted_events: list[AgentLifecycleEvent] = []
    event_bus.subscribe(lambda e: emitted_events.append(e))

    # Run up to design
    context = await StrategyAgent().run(phase8_campaign_context)
    context = await ResearchAgent().run(context)
    context = await CompetitorAgent().run(context)
    context = await ContentAgent().run(context)
    context = await DesignAgent().run(context)

    # Run CV Agent
    cv_agent = CVAgent()
    result_context = await cv_agent.run(context)

    assert "cv_agent" in result_context.agent_outputs
    cv_output = result_context.agent_outputs["cv_agent"]

    # 1. Quality & Aesthetic Scores
    assert 0.0 <= cv_output.creative_score <= 100.0
    assert 0.0 <= cv_output.aesthetic_score <= 10.0
    assert cv_output.passed_quality_gate is True

    # 2. OCR Results
    assert cv_output.ocr_results is not None
    assert len(cv_output.ocr_results.extracted_text) >= 1
    assert cv_output.ocr_results.readability_score >= 70.0
    assert cv_output.ocr_results.legibility_passed is True

    # 3. Object & Logo Detection
    assert cv_output.object_detection is not None
    assert isinstance(cv_output.object_detection.logo_detected, bool)
    assert cv_output.object_detection.product_prominence_score >= 70.0

    # 4. Brand & Safety
    assert cv_output.brand_safe is True
    assert len(cv_output.brand_violations) == 0

    # 5. Provenance & Events
    assert isinstance(cv_output.provenance, DataProvenance)
    cv_events = [e for e in emitted_events if e.agent_id == "cv_agent"]
    assert len(cv_events) == 2
    assert cv_events[0].event_type == AgentEventType.AGENT_STARTED
    assert cv_events[1].event_type == AgentEventType.AGENT_COMPLETED


@pytest.mark.asyncio
async def test_design_cv_automated_revision_loop(phase8_campaign_context):
    """Test automated revision loop when CV Agent detects an issue."""
    cv_agent = CVAgent()
    design_agent = DesignAgent()

    # Pre-run upstream
    context = await StrategyAgent().run(phase8_campaign_context)
    context = await ResearchAgent().run(context)
    context = await CompetitorAgent().run(context)
    context = await ContentAgent().run(context)

    # Run with revision
    final_context = await cv_agent.run_with_revision(context, design_agent=design_agent, max_revisions=2)
    assert final_context.design is not None
    assert "cv_agent" in final_context.agent_outputs
    assert final_context.agent_outputs["cv_agent"].passed_quality_gate is True


@pytest.mark.asyncio
async def test_end_to_end_strategy_research_competitor_content_design_cv_chain(phase8_campaign_context):
    """Test full sequential 6-stage execution chain."""
    event_bus.clear()
    emitted_events: list[AgentLifecycleEvent] = []
    event_bus.subscribe(lambda e: emitted_events.append(e))

    # Sequential execution: Stage 1 to 6
    context = await StrategyAgent().run(phase8_campaign_context)
    context = await ResearchAgent().run(context)
    context = await CompetitorAgent().run(context)
    context = await ContentAgent().run(context)
    context = await DesignAgent().run(context)
    context = await CVAgent().run(context)

    assert context.strategy is not None
    assert context.research is not None
    assert context.competitors is not None
    assert context.content is not None
    assert context.design is not None
    assert "cv_agent" in context.agent_outputs

    # Verify event bus recorded all 6 stages (6 started + 6 completed = 12 events)
    assert len(emitted_events) == 12
    completed = [e for e in emitted_events if e.event_type == AgentEventType.AGENT_COMPLETED]
    assert len(completed) == 6
    expected_order = [
        "strategy_agent",
        "research_agent",
        "competitor_agent",
        "content_agent",
        "design_agent",
        "cv_agent",
    ]
    assert [e.agent_id for e in completed] == expected_order


@pytest.mark.asyncio
async def test_orchestrator_integration_with_phase8_agents(phase8_campaign_context):
    """Test MasterOrchestrator plan execution through all 6 stages."""
    orchestrator = MasterOrchestrator()
    plan = CampaignPlanner().plan(phase8_campaign_context)

    # Filter to first 6 steps
    target_names = {
        "strategy_agent",
        "research_agent",
        "competitor_agent",
        "content_agent",
        "design_agent",
        "cv_agent",
    }
    plan.agent_sequence = [s for s in plan.agent_sequence if s.agent_name in target_names]
    plan.total_steps = len(plan.agent_sequence)

    result_context = await orchestrator.execute_plan(context=phase8_campaign_context, plan=plan)

    assert result_context.strategy is not None
    assert result_context.research is not None
    assert result_context.competitors is not None
    assert result_context.content is not None
    assert result_context.design is not None
    assert "cv_agent" in result_context.agent_outputs
    assert result_context.agent_outputs["cv_agent"].passed_quality_gate is True
