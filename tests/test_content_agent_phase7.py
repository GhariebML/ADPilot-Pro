"""Tests for Phase 7 — Content Agent, Multi-Model ML Inference, and Content Evaluator."""

import pytest

from adpilot.agents import (
    CompetitorAgent,
    ContentAgent,
    ResearchAgent,
    StrategyAgent,
)
from adpilot.agents.content_evaluator import ContentEvaluator
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
    ProductType,
    ToneOfVoice,
)
from adpilot.services.model_loader import ModelLoader


@pytest.fixture
def phase7_campaign_context():
    """Create a canonical CampaignContext for Phase 7 testing."""
    return (
        CampaignContextBuilder.create("camp-phase7-test")
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
        .with_budget(total_budget=60000.0, currency="USD")
        .with_channels([MarketingChannel.linkedin, MarketingChannel.facebook, MarketingChannel.email])
        .with_timeline(duration_days=60)
        .with_goals([CampaignGoal.lead_generation, CampaignGoal.brand_awareness])
        .with_brand(
            tone_of_voice=ToneOfVoice.authoritative,
            dos_and_donts=["Focus on enterprise security", "Never make unsubstantiated claims"],
        )
        .with_competitors(["LegacyFlow Corp", "AutoWorkflow Systems"])
        .build()
    )


@pytest.mark.asyncio
async def test_content_agent_standalone_with_full_context(phase7_campaign_context):
    """Test standalone ContentAgent execution and verify all required Phase 7 outputs."""
    event_bus.clear()
    emitted_events: list[AgentLifecycleEvent] = []
    event_bus.subscribe(lambda e: emitted_events.append(e))

    # Pre-populate upstream context
    strategy_agent = StrategyAgent()
    research_agent = ResearchAgent()
    competitor_agent = CompetitorAgent()
    content_agent = ContentAgent()

    context = await strategy_agent.run(phase7_campaign_context)
    context = await research_agent.run(context)
    context = await competitor_agent.run(context)

    result_context = await content_agent.run(context)
    assert result_context.content is not None
    content = result_context.content

    # 1. Package Outputs
    assert len(content.headlines) >= 2
    assert len(content.primary_copy) >= 1
    assert len(content.descriptions) >= 1
    assert len(content.ctas) >= 1
    assert content.seo_metadata is not None
    assert len(content.seo_metadata.title) > 0
    assert len(content.seo_metadata.meta_description) > 0
    assert len(content.keywords) >= 1
    assert len(content.content_variations) >= 2

    # 2. Backwards-compatible fields
    assert len(content.ads) >= 1
    assert len(content.email_sequences) >= 1
    assert len(content.social_posts) >= 1
    assert len(content.blog_outlines) >= 1
    assert len(content.cta_variants) >= 1
    assert content.content_calendar_note is not None

    # 3. Provenance & Confidence
    assert isinstance(content.provenance, DataProvenance)
    assert len(content.provenance.observed_data) > 0
    assert len(content.provenance.model_prediction) > 0
    assert len(content.provenance.llm_inference) > 0
    assert len(content.provenance.recommendation) > 0
    assert 0.0 <= content.confidence <= 1.0
    assert len(content.evidence) > 0
    assert len(content.corrective_actions) > 0

    # 4. Evaluation Report
    assert content.evaluation is not None
    assert 0.0 <= content.evaluation.content_quality_score <= 100.0
    assert 0.0 <= content.evaluation.relevance_score <= 100.0
    assert 0.0 <= content.evaluation.keyword_coverage_score <= 100.0
    assert 0.0 <= content.evaluation.brand_compliance_score <= 100.0
    assert 0.0 <= content.evaluation.hallucination_risk_score <= 100.0
    assert content.evaluation.passed_quality_gate is True
    assert len(content.evaluation.metrics) == 5

    # 5. Universal BaseAgent Methods
    assert content_agent.get_input_schema() is not None
    assert content_agent.get_output_schema() is not None
    assert len(content_agent.get_responsibilities()) >= 2
    assert content_agent.get_contract() is not None

    # 6. Event Bus Telemetry
    assert len(emitted_events) >= 8
    content_events = [e for e in emitted_events if e.agent_id == "content_agent"]
    assert len(content_events) == 2
    assert content_events[0].event_type == AgentEventType.AGENT_STARTED
    assert content_events[1].event_type == AgentEventType.AGENT_COMPLETED


def test_content_evaluator_quality_and_relevance():
    """Test ContentEvaluator metric computations on high-quality and low-quality copy."""
    evaluator = ContentEvaluator()

    headlines = ["ScaleFlow AI: Enterprise Autonomous Orchestration", "Accelerate Velocity Today"]
    primary_copy = [
        (
            "ScaleFlow AI provides an enterprise-grade multi-agent orchestration platform engineered "
            "for Chief Technology Officers and Engineering Directors. Our platform eliminates friction, "
            "guarantees high availability, and accelerates automated workflow delivery across cloud infrastructure."
        )
    ]
    descriptions = ["Enterprise multi-agent automation platform for modern teams."]
    ctas = ["Request an Enterprise Demo", "Explore the Platform"]
    target_keywords = ["scaleflow ai", "orchestration platform", "enterprise", "workflow"]

    report = evaluator.evaluate(
        headlines=headlines,
        primary_copy=primary_copy,
        descriptions=descriptions,
        ctas=ctas,
        target_keywords=target_keywords,
        product_type=ProductType.saas,
        expected_tone=ToneOfVoice.authoritative,
    )

    assert report.content_quality_score >= 70.0
    assert report.relevance_score >= 70.0
    assert report.keyword_coverage_score >= 75.0
    assert report.brand_compliance_score >= 80.0
    assert report.hallucination_risk_score <= 10.0
    assert report.passed_quality_gate is True
    assert "scaleflow ai" in report.covered_keywords or "workflow" in report.covered_keywords


def test_content_evaluator_detects_prohibited_keywords_and_hallucinations(phase7_campaign_context):
    """Test ContentEvaluator detecting prohibited brand terms and hyperbolic claims."""
    evaluator = ContentEvaluator()

    headlines = ["The Undisputed #1 Solution In Existence"]
    primary_copy = [
        "We guarantee 1000% ROI overnight with zero risk guaranteed! It magically solves all problems."
    ]
    descriptions = ["Get rich quick with guaranteed millions."]
    ctas = ["Buy Now"]

    # Inject prohibited keywords into constraints
    phase7_campaign_context.constraints.prohibited_keywords = ["cheap", "untested", "overnight"]
    primary_copy[0] += " This is not a cheap or untested tool."

    report = evaluator.evaluate(
        headlines=headlines,
        primary_copy=primary_copy,
        descriptions=descriptions,
        ctas=ctas,
        target_keywords=["enterprise software"],
        context=phase7_campaign_context,
        brand_guidelines=phase7_campaign_context.brand,
    )

    # Should flag hallucination and prohibited keywords
    assert report.hallucination_risk_score >= 50.0
    assert len(report.detected_unsupported_claims) >= 2
    assert report.brand_compliance_score < 70.0


def test_content_agent_ml_model_inference():
    """Test that the ML content model and tokenizer execute real inference."""
    loader = ModelLoader()
    model = loader.load_model("research/models/content/content_model.pkl")
    tokenizer = loader.load_model("research/models/content/tokenizer.pkl")

    assert model is not None
    assert tokenizer is not None

    sample_text = "modern luxury apartment in downtown with panoramic skyline views and spacious suite"
    vec = tokenizer.transform([sample_text])
    score = float(model.predict(vec)[0])

    assert isinstance(score, float)
    assert score > 0.0


@pytest.mark.asyncio
async def test_end_to_end_strategy_research_competitor_content_chain(phase7_campaign_context):
    """Test sequential execution of Strategy -> Research -> Competitor -> Content chain."""
    event_bus.clear()
    emitted_events: list[AgentLifecycleEvent] = []
    event_bus.subscribe(lambda e: emitted_events.append(e))

    strategy_agent = StrategyAgent()
    research_agent = ResearchAgent()
    competitor_agent = CompetitorAgent()
    content_agent = ContentAgent()

    # Step 1: Strategy
    context = await strategy_agent.run(phase7_campaign_context)
    assert context.strategy is not None

    # Step 2: Research
    context = await research_agent.run(context)
    assert context.research is not None

    # Step 3: Competitor
    context = await competitor_agent.run(context)
    assert context.competitors is not None

    # Step 4: Content
    context = await content_agent.run(context)
    assert context.content is not None
    assert len(context.content.headlines) >= 2
    assert context.content.evaluation is not None

    # Verify event bus recorded all 4 stages (4 started + 4 completed = 8 events)
    assert len(emitted_events) == 8
    completed = [e for e in emitted_events if e.event_type == AgentEventType.AGENT_COMPLETED]
    assert len(completed) == 4
    assert [e.agent_id for e in completed] == ["strategy_agent", "research_agent", "competitor_agent", "content_agent"]


@pytest.mark.asyncio
async def test_orchestrator_integration_with_content_agent(phase7_campaign_context):
    """Test MasterOrchestrator dispatching through Strategy -> Research -> Competitor -> Content sequence."""
    orchestrator = MasterOrchestrator()
    plan = CampaignPlanner().plan(phase7_campaign_context)

    # Filter to only the first 4 steps
    target_names = {"strategy_agent", "research_agent", "competitor_agent", "content_agent"}
    plan.agent_sequence = [s for s in plan.agent_sequence if s.agent_name in target_names]
    plan.total_steps = len(plan.agent_sequence)

    result_context = await orchestrator.execute_plan(context=phase7_campaign_context, plan=plan)

    assert result_context.strategy is not None
    assert result_context.research is not None
    assert result_context.competitors is not None
    assert result_context.content is not None
    assert len(result_context.content.headlines) >= 2
    assert result_context.content.evaluation.passed_quality_gate is True
