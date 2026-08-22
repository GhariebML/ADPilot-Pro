import pytest
from pydantic import BaseModel

from adpilot.agents import (
    AnalyticsAgent,
    AudienceAgent,
    CompetitorAgent,
    ContentAgent,
    CorrectionAgent,
    CVAgent,
    DesignAgent,
    MonitoringAgent,
    OptimizationAgent,
    PublishingAgent,
    ResearchAgent,
    StrategyAgent,
)
from adpilot.core.agent_contract import AgentContract
from adpilot.core.agent_events import (
    AgentEventType,
    AgentLifecycleEvent,
    event_bus,
)
from adpilot.core.context_builder import CampaignContextBuilder
from adpilot.core.contract_registry import get_agent_contract
from adpilot.schemas.agent_schemas import ProductType


REQUIRED_AGENT_CLASSES = [
    StrategyAgent,
    ResearchAgent,
    AudienceAgent,
    CompetitorAgent,
    ContentAgent,
    DesignAgent,
    CVAgent,
    AnalyticsAgent,
    OptimizationAgent,
    CorrectionAgent,
    PublishingAgent,
    MonitoringAgent,
]


def test_all_11_required_agents_have_valid_typed_contracts():
    """Verify all 11 required pipeline agents have explicit typed contracts."""
    required_ids = [
        "strategy_agent",
        "research_agent",
        "competitor_agent",
        "content_agent",
        "design_agent",
        "cv_agent",
        "analytics_agent",
        "optimization_agent",
        "correction_agent",
        "publishing_agent",
        "monitoring_agent",
    ]

    for agent_id in required_ids:
        contract = get_agent_contract(agent_id)
        assert contract is not None, f"Missing contract for {agent_id}"
        assert isinstance(contract, AgentContract)
        assert contract.identity.agent_id == agent_id
        assert len(contract.responsibilities) > 0
        assert len(contract.boundaries.allowed_actions) > 0
        assert len(contract.boundaries.forbidden_actions) > 0
        assert len(contract.quality.success_criteria) > 0
        assert len(contract.quality.failure_conditions) > 0
        assert 0.0 <= contract.quality.confidence_threshold <= 1.0
        assert len(contract.quality.evidence_requirements) > 0
        assert len(contract.quality.corrective_actions) > 0


def test_agent_classes_expose_required_contract_methods():
    """Verify every agent class implements get_input_schema, get_output_schema, get_responsibilities, get_contract."""
    for agent_cls in REQUIRED_AGENT_CLASSES:
        agent = agent_cls()

        # 1. get_input_schema()
        input_schema = agent.get_input_schema()
        assert issubclass(input_schema, BaseModel), f"{agent_cls.name} input schema is not a Pydantic model"

        # 2. get_output_schema()
        output_schema = agent.get_output_schema()
        assert issubclass(output_schema, BaseModel), f"{agent_cls.name} output schema is not a Pydantic model"

        # 3. get_responsibilities()
        responsibilities = agent.get_responsibilities()
        assert isinstance(responsibilities, list), f"{agent_cls.name} responsibilities is not a list"
        assert len(responsibilities) > 0, f"{agent_cls.name} has empty responsibilities"

        # 4. get_contract()
        contract = agent.get_contract()
        assert contract is not None, f"{agent_cls.name} get_contract() returned None"
        assert isinstance(contract, AgentContract)


def test_forbidden_action_boundaries_enforced():
    """Verify that forbidden action boundaries are defined for critical safety."""
    strategy_contract = get_agent_contract("strategy_agent")
    assert any("Modify overall campaign dollar budget" in f for f in strategy_contract.boundaries.forbidden_actions)

    content_contract = get_agent_contract("content_agent")
    assert any("Publish content to live networks directly" in f for f in content_contract.boundaries.forbidden_actions)

    publishing_contract = get_agent_contract("publishing_agent")
    assert any("Publish unapproved campaigns when human sign-off is required" in f for f in publishing_contract.boundaries.forbidden_actions)


def test_agent_event_emission_lifecycle():
    """Verify structured event emission (agent_started, agent_completed, agent_failed)."""
    event_bus.clear()
    emitted_events = []

    def event_listener(event: AgentLifecycleEvent):
        emitted_events.append(event)

    event_bus.subscribe(event_listener)

    strategy_agent = StrategyAgent()
    strategy_agent.emit_event(
        event_type=AgentEventType.AGENT_STARTED,
        campaign_id="camp-test-evt-001",
        status="started",
        input_reference="brief_summary",
        model="gpt-4o",
    )
    strategy_agent.emit_event(
        event_type=AgentEventType.AGENT_COMPLETED,
        campaign_id="camp-test-evt-001",
        status="completed",
        output_reference="strategy_payload",
        model="gpt-4o",
        latency=0.342,
        confidence=0.91,
    )
    strategy_agent.emit_event(
        event_type=AgentEventType.AGENT_FAILED,
        campaign_id="camp-test-evt-001",
        status="failed",
        error_message="Simulated connection timeout",
        model="gpt-4o",
        latency=0.120,
    )

    assert len(emitted_events) == 3
    assert emitted_events[0].event_type == AgentEventType.AGENT_STARTED
    assert emitted_events[0].campaign_id == "camp-test-evt-001"
    assert emitted_events[0].agent_id == "strategy_agent"

    assert emitted_events[1].event_type == AgentEventType.AGENT_COMPLETED
    assert emitted_events[1].latency == 0.342
    assert emitted_events[1].confidence == 0.91

    assert emitted_events[2].event_type == AgentEventType.AGENT_FAILED
    assert emitted_events[2].error_message == "Simulated connection timeout"

    event_bus.unsubscribe(event_listener)


@pytest.mark.asyncio
async def test_cv_agent_execution_and_events():
    """Verify CVAgent execution emits started and completed lifecycle events."""
    event_bus.clear()
    emitted = []
    event_bus.subscribe(lambda e: emitted.append(e))

    context = (
        CampaignContextBuilder.create("camp-cv-test")
        .with_business(name="Visual Brand", industry="E-commerce")
        .with_product(name="Product X", product_type=ProductType.physical, description="Goods")
        .with_audience(summary="Visual Shoppers")
        .with_budget(total_budget=5000.0)
        .with_timeline(duration_days=30)
        .build()
    )

    agent = CVAgent()
    result_context = await agent.run(context)

    assert result_context.cv_agent is not None
    assert result_context.cv_agent.aesthetic_score >= 6.5
    assert len(emitted) == 2
    assert emitted[0].event_type == AgentEventType.AGENT_STARTED
    assert emitted[1].event_type == AgentEventType.AGENT_COMPLETED


@pytest.mark.asyncio
async def test_correction_agent_execution_and_events():
    """Verify CorrectionAgent quality gate evaluation and event emission."""
    event_bus.clear()
    emitted = []
    event_bus.subscribe(lambda e: emitted.append(e))

    context = (
        CampaignContextBuilder.create("camp-corr-test")
        .with_business(name="Corr Co", industry="SaaS")
        .with_product(name="Software", product_type=ProductType.saas, description="SaaS platform")
        .with_audience(summary="B2B Tech Leaders")
        .with_budget(total_budget=5000.0)
        .with_timeline(duration_days=30)
        .build()
    )

    agent = CorrectionAgent()
    result_context = await agent.run(context)

    assert result_context.correction_agent is not None
    assert result_context.correction_agent.quality_gate_passed is True
    assert len(emitted) == 2
    assert emitted[0].event_type == AgentEventType.AGENT_STARTED
    assert emitted[1].event_type == AgentEventType.AGENT_COMPLETED


@pytest.mark.asyncio
async def test_monitoring_agent_execution_and_events():
    """Verify MonitoringAgent stream telemetry initialization and event emission."""
    event_bus.clear()
    emitted = []
    event_bus.subscribe(lambda e: emitted.append(e))

    context = (
        CampaignContextBuilder.create("camp-mon-test")
        .with_business(name="Stream Co", industry="FinTech")
        .with_product(name="FinTech API", product_type=ProductType.saas, description="Payments")
        .with_audience(summary="Finance Directors")
        .with_budget(total_budget=5000.0)
        .with_timeline(duration_days=30)
        .build()
    )

    agent = MonitoringAgent()
    result_context = await agent.run(context)

    assert result_context.monitoring_agent is not None
    assert result_context.monitoring_agent.telemetry_stream_active is True
    assert len(emitted) == 2
    assert emitted[0].event_type == AgentEventType.AGENT_STARTED
    assert emitted[1].event_type == AgentEventType.AGENT_COMPLETED
