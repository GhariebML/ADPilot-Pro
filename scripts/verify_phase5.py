"""Verification script for Phase 5 — Agent Contract & Responsibility System."""

import asyncio
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


def main() -> None:
    print("=" * 80)
    print("ADPilot Phase 5 — Agent Contract & Responsibility System Verification")
    print("=" * 80)

    required_agents = [
        ("1. Strategy", StrategyAgent),
        ("2. Research", ResearchAgent),
        ("3. Competitor", CompetitorAgent),
        ("4. Content", ContentAgent),
        ("5. Design", DesignAgent),
        ("6. CV", CVAgent),
        ("7. Analytics", AnalyticsAgent),
        ("8. Optimizer", OptimizationAgent),
        ("9. Correction", CorrectionAgent),
        ("10. Publishing", PublishingAgent),
        ("11. Monitoring", MonitoringAgent),
    ]

    # Verification 1 & 2: Verify all 11 Agents have valid typed contracts & expose required methods
    for name, agent_cls in required_agents:
        agent = agent_cls()
        contract = agent.get_contract()
        assert contract is not None, f"Contract missing for {name}"
        assert isinstance(contract, AgentContract)

        in_schema = agent.get_input_schema()
        out_schema = agent.get_output_schema()
        assert issubclass(in_schema, BaseModel), f"Invalid input schema for {name}"
        assert issubclass(out_schema, BaseModel), f"Invalid output schema for {name}"

        responsibilities = agent.get_responsibilities()
        assert isinstance(responsibilities, list) and len(responsibilities) > 0, f"Invalid responsibilities for {name}"

        # Action Boundaries & Quality Criteria checks
        assert len(contract.boundaries.allowed_actions) > 0
        assert len(contract.boundaries.forbidden_actions) > 0
        assert len(contract.quality.success_criteria) > 0
        assert len(contract.quality.failure_conditions) > 0
        assert 0.0 <= contract.quality.confidence_threshold <= 1.0

        print(f"[PASS] Contract Verified: {name} (ID: {contract.identity.agent_id}, Version: {contract.identity.version})")
        print(f"       - Input: {in_schema.__name__}, Output: {out_schema.__name__}")
        print(f"       - Responsibilities: {len(responsibilities)}, Allowed: {len(contract.boundaries.allowed_actions)}, Forbidden: {len(contract.boundaries.forbidden_actions)}")
        print(f"       - Confidence Threshold: {contract.quality.confidence_threshold:.2f}")

    # Verification 3: Structured Event Emission
    event_bus.clear()
    emitted = []
    event_bus.subscribe(lambda e: emitted.append(e))

    context = (
        CampaignContextBuilder.create("camp-phase5-verify")
        .with_business(name="ScaleFlow AI", industry="B2B SaaS")
        .with_product(name="ScaleFlow Orchestrator", product_type=ProductType.saas, description="Enterprise AI workflow automation")
        .with_audience(summary="Engineering VP and Chief Architects")
        .with_budget(total_budget=25000.0)
        .with_timeline(duration_days=30)
        .build()
    )

    # Run CVAgent
    cv_agent = CVAgent()
    asyncio.run(cv_agent.run(context))
    assert context.cv_agent is not None

    # Run CorrectionAgent
    corr_agent = CorrectionAgent()
    asyncio.run(corr_agent.run(context))
    assert context.correction_agent is not None

    # Run MonitoringAgent
    mon_agent = MonitoringAgent()
    asyncio.run(mon_agent.run(context))
    assert context.monitoring_agent is not None

    assert len(emitted) == 6  # 3 started + 3 completed events
    started_events = [e for e in emitted if e.event_type == AgentEventType.AGENT_STARTED]
    completed_events = [e for e in emitted if e.event_type == AgentEventType.AGENT_COMPLETED]

    assert len(started_events) == 3
    assert len(completed_events) == 3

    for ce in completed_events:
        assert ce.campaign_id == "camp-phase5-verify"
        assert ce.status == "completed"
        assert ce.latency >= 0.0
        assert ce.confidence is not None
        assert ce.timestamp is not None
        print(f"[PASS] Event Verified: {ce.event_type.value} | agent={ce.agent_id}, status={ce.status}, latency={ce.latency:.4f}s, confidence={ce.confidence:.2f}")

    print("=" * 80)
    print("ALL PHASE 5 AGENT CONTRACT & RESPONSIBILITY VERIFICATIONS PASSED!")
    print("=" * 80)


if __name__ == "__main__":
    main()
