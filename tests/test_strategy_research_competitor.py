"""Tests for Phase 6 — Strategy, Research, and Competitor Agents."""

import pytest

from adpilot.agents import (
    CompetitorAgent,
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
    ProductType,
    ToneOfVoice,
)


@pytest.fixture
def base_campaign_context():
    """Create a canonical CampaignContext for Phase 6 testing."""
    return (
        CampaignContextBuilder.create("camp-phase6-test")
        .with_business(name="ScaleFlow AI", industry="B2B SaaS")
        .with_product(
            name="ScaleFlow Orchestrator",
            product_type=ProductType.saas,
            description="Enterprise autonomous AI workflow platform",
        )
        .with_audience(
            summary="Chief Technology Officers, VP Engineering, and DevOps Directors",
        )
        .with_geography(
            target_countries=["US", "CA", "EU"],
        )
        .with_budget(total_budget=50000.0, currency="USD")
        .with_channels([MarketingChannel.linkedin, MarketingChannel.facebook])
        .with_timeline(duration_days=60)
        .with_goals([CampaignGoal.lead_generation, CampaignGoal.brand_awareness])
        .with_brand(tone_of_voice=ToneOfVoice.authoritative)
        .with_competitors(["LegacyFlow Corp", "AutoWorkflow Systems"])
        .build()
    )


@pytest.mark.asyncio
async def test_strategy_agent_standalone(base_campaign_context):
    """Test StrategyAgent standalone execution, budget sum validation, evidence, confidence, and provenance."""
    event_bus.clear()
    emitted_events: list[AgentLifecycleEvent] = []
    event_bus.subscribe(lambda e: emitted_events.append(e))

    agent = StrategyAgent()
    context = await agent.run(base_campaign_context)

    assert context.strategy is not None
    strategy = context.strategy

    # 1. Output structure & fields
    assert strategy.positioning_statement is not None and len(strategy.positioning_statement) > 0
    assert strategy.usp is not None and len(strategy.usp) > 0
    assert strategy.elevator_pitch is not None and len(strategy.elevator_pitch) > 0
    assert len(strategy.messaging_pillars) >= 2
    assert len(strategy.primary_channels) >= 1

    # 2. Strict 100% Funnel budget allocation sum
    total_budget_pct = sum(f.budget_allocation_percent for f in strategy.funnel_strategy)
    assert round(total_budget_pct) == 100

    # 3. Quality & Governance
    assert 0.0 <= strategy.confidence <= 1.0
    assert len(strategy.evidence) > 0
    assert len(strategy.corrective_actions) > 0

    # 4. Data Provenance
    assert strategy.provenance is not None
    assert isinstance(strategy.provenance, DataProvenance)
    assert len(strategy.provenance.observed_data) > 0
    assert len(strategy.provenance.llm_inference) > 0
    assert len(strategy.provenance.recommendation) > 0

    # 5. Lifecycle Events
    assert len(emitted_events) == 2
    assert emitted_events[0].event_type == AgentEventType.AGENT_STARTED
    assert emitted_events[1].event_type == AgentEventType.AGENT_COMPLETED


@pytest.mark.asyncio
async def test_research_agent_standalone(base_campaign_context):
    """Test ResearchAgent standalone execution, personas, trends, benchmarks, and keywords."""
    event_bus.clear()
    emitted_events: list[AgentLifecycleEvent] = []
    event_bus.subscribe(lambda e: emitted_events.append(e))

    agent = ResearchAgent()
    context = await agent.run(base_campaign_context)

    assert context.research is not None
    research = context.research

    # 1. Personas, Trends, Benchmarks
    assert len(research.audience_personas) >= 1
    assert len(research.trending_topics) >= 1
    assert len(research.channel_benchmarks) >= 1
    assert len(research.recommended_keywords) >= 1
    assert research.market_size_estimate > 0

    # 2. Quality & Governance
    assert 0.0 <= research.confidence <= 1.0
    assert len(research.evidence) > 0
    assert len(research.corrective_actions) > 0

    # 3. Data Provenance
    assert research.provenance is not None
    assert isinstance(research.provenance, DataProvenance)
    assert len(research.provenance.observed_data) > 0
    assert len(research.provenance.llm_inference) > 0

    # 4. Lifecycle Events
    assert len(emitted_events) == 2
    assert emitted_events[0].event_type == AgentEventType.AGENT_STARTED
    assert emitted_events[1].event_type == AgentEventType.AGENT_COMPLETED


@pytest.mark.asyncio
async def test_competitor_agent_standalone(base_campaign_context):
    """Test CompetitorAgent standalone execution, rival profiling, pricing comparison, and differentiators."""
    event_bus.clear()
    emitted_events: list[AgentLifecycleEvent] = []
    event_bus.subscribe(lambda e: emitted_events.append(e))

    agent = CompetitorAgent()
    context = await agent.run(base_campaign_context)

    assert context.competitors is not None
    competitors = context.competitors

    # 1. Competitors, Opportunities, Threats, Pricing
    assert len(competitors.competitors) >= 1
    assert len(competitors.opportunities) >= 1
    assert len(competitors.threats) >= 1
    assert len(competitors.differentiators) >= 1
    assert competitors.pricing_comparison_summary != ""

    # 2. Quality & Governance
    assert 0.0 <= competitors.confidence <= 1.0
    assert len(competitors.evidence) > 0
    assert len(competitors.corrective_actions) > 0

    # 3. Data Provenance
    assert competitors.provenance is not None
    assert isinstance(competitors.provenance, DataProvenance)
    assert len(competitors.provenance.observed_data) > 0
    assert len(competitors.provenance.recommendation) > 0

    # 4. Lifecycle Events
    assert len(emitted_events) == 2
    assert emitted_events[0].event_type == AgentEventType.AGENT_STARTED
    assert emitted_events[1].event_type == AgentEventType.AGENT_COMPLETED


@pytest.mark.asyncio
async def test_end_to_end_strategy_research_competitor_chain(base_campaign_context):
    """Test sequential execution of Strategy -> Research -> Competitor pipeline chain."""
    event_bus.clear()
    emitted_events: list[AgentLifecycleEvent] = []
    event_bus.subscribe(lambda e: emitted_events.append(e))

    strategy_agent = StrategyAgent()
    research_agent = ResearchAgent()
    competitor_agent = CompetitorAgent()

    # Step 1: Strategy
    context = await strategy_agent.run(base_campaign_context)
    assert context.strategy is not None

    # Step 2: Research consumes Strategy
    context = await research_agent.run(context)
    assert context.research is not None

    # Step 3: Competitor consumes Strategy & Research
    context = await competitor_agent.run(context)
    assert context.competitors is not None
    assert context.competitor_research is not None

    # Verify All 3 Agent Outputs Preserved on context
    assert context.strategy.positioning_statement != ""
    assert len(context.research.audience_personas) > 0
    assert len(context.competitors.competitors) > 0

    # Verify event counts (3 started + 3 completed = 6)
    assert len(emitted_events) == 6
    completed = [e for e in emitted_events if e.event_type == AgentEventType.AGENT_COMPLETED]
    assert len(completed) == 3
    assert [e.agent_id for e in completed] == ["strategy_agent", "research_agent", "competitor_agent"]


@pytest.mark.asyncio
async def test_orchestrator_integration_with_phase6_agents(base_campaign_context):
    """Test MasterOrchestrator dispatching through the Phase 6 agent sequence."""
    orchestrator = MasterOrchestrator()
    plan = CampaignPlanner().plan(base_campaign_context)

    # Filter to only the first 3 steps (strategy, research, competitor)
    target_names = {"strategy_agent", "research_agent", "competitor_agent"}
    plan.agent_sequence = [s for s in plan.agent_sequence if s.agent_name in target_names]
    plan.total_steps = len(plan.agent_sequence)

    result_context = await orchestrator.execute_plan(context=base_campaign_context, plan=plan)

    assert result_context.strategy is not None
    assert result_context.research is not None
    assert result_context.competitors is not None
