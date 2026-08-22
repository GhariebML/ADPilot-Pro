"""Runtime verification script for Phase 6 — Strategy, Research, and Competitor Agents."""

import asyncio

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


def main() -> None:
    print("=" * 80)
    print("ADPilot Phase 6 — Strategy, Research, and Competitor Agents Verification")
    print("=" * 80)

    # 1. Build Canonical Campaign Context
    context = (
        CampaignContextBuilder.create("camp-phase6-live")
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
        .with_budget(total_budget=75000.0, currency="USD")
        .with_channels([MarketingChannel.linkedin, MarketingChannel.facebook, MarketingChannel.email])
        .with_timeline(duration_days=90)
        .with_goals([CampaignGoal.lead_generation, CampaignGoal.brand_awareness])
        .with_brand(tone_of_voice=ToneOfVoice.authoritative)
        .with_competitors(["LegacyFlow Corp", "AutoWorkflow Systems", "ManualOps Inc"])
        .build()
    )

    event_bus.clear()
    emitted_events: list[AgentLifecycleEvent] = []
    event_bus.subscribe(lambda e: emitted_events.append(e))

    # 2. Stage 1: Strategy Agent Verification
    strategy_agent = StrategyAgent()
    context = asyncio.run(strategy_agent.run(context))
    assert context.strategy is not None
    strategy = context.strategy

    total_budget_pct = sum(f.budget_allocation_percent for f in strategy.funnel_strategy)
    assert round(total_budget_pct) == 100, f"Budget sum was {total_budget_pct}"
    assert len(strategy.messaging_pillars) >= 2
    assert strategy.provenance is not None
    assert len(strategy.provenance.observed_data) > 0
    assert len(strategy.provenance.llm_inference) > 0
    assert len(strategy.evidence) > 0

    print("[PASS] StrategyAgent Executed:")
    print(f"       - Positioning: '{strategy.positioning_statement[:65]}...'")
    print(f"       - USP: '{strategy.usp[:65]}...'")
    print(f"       - Funnel Budget Allocations (Sum = {total_budget_pct:.0f}%): " + ", ".join(f"{f.stage.value}: {f.budget_allocation_percent:.0f}%" for f in strategy.funnel_strategy))
    print(f"       - Confidence: {strategy.confidence:.2f}, Evidence Items: {len(strategy.evidence)}")

    # 3. Stage 2: Research Agent Verification
    research_agent = ResearchAgent()
    context = asyncio.run(research_agent.run(context))
    assert context.research is not None
    research = context.research

    assert len(research.audience_personas) >= 1
    assert len(research.trending_topics) >= 1
    assert len(research.recommended_keywords) >= 1
    assert research.provenance is not None
    assert len(research.evidence) > 0

    print("[PASS] ResearchAgent Executed:")
    print(f"       - Primary Persona: '{research.audience_personas[0].name}' ({research.audience_personas[0].demographics})")
    print(f"       - Trending Topics: {', '.join(t.topic for t in research.trending_topics[:2])}")
    print(f"       - Keywords: {', '.join(research.recommended_keywords[:3])}")
    print(f"       - Market Size Est: ${research.market_size_estimate:,.2f}")
    print(f"       - Confidence: {research.confidence:.2f}, Evidence Items: {len(research.evidence)}")

    # 4. Stage 3: Competitor Agent Verification
    competitor_agent = CompetitorAgent()
    context = asyncio.run(competitor_agent.run(context))
    assert context.competitors is not None
    competitors = context.competitors

    assert len(competitors.competitors) >= 1
    assert len(competitors.differentiators) >= 1
    assert competitors.provenance is not None
    assert len(competitors.evidence) > 0

    print("[PASS] CompetitorAgent Executed:")
    print(f"       - Competitors Benchmarked: {len(competitors.competitors)} ({', '.join(c.name for c in competitors.competitors[:2])})")
    print(f"       - Differentiators: {', '.join(competitors.differentiators[:2])}")
    print(f"       - Pricing Summary: '{competitors.pricing_comparison_summary[:65]}...'")
    print(f"       - Confidence: {competitors.confidence:.2f}, Evidence Items: {len(competitors.evidence)}")

    # 5. Master Orchestrator Verification
    orchestrator = MasterOrchestrator()
    plan = CampaignPlanner().plan(context)
    target_names = {"strategy_agent", "research_agent", "competitor_agent"}
    plan.agent_sequence = [s for s in plan.agent_sequence if s.agent_name in target_names]
    plan.total_steps = len(plan.agent_sequence)

    orchestrated_context = asyncio.run(orchestrator.execute_plan(context=context, plan=plan))
    assert orchestrated_context.strategy is not None
    assert orchestrated_context.research is not None
    assert orchestrated_context.competitors is not None

    print("[PASS] MasterOrchestrator Plan Execution Verified through Strategy -> Research -> Competitor.")

    # 6. Event Bus Verification
    assert len(emitted_events) >= 6
    completed_events = [e for e in emitted_events if e.event_type == AgentEventType.AGENT_COMPLETED]
    for ce in completed_events[-3:]:
        print(f"[PASS] Event Verified: {ce.event_type.value} | agent={ce.agent_id}, status={ce.status}, latency={ce.latency:.4f}s, confidence={ce.confidence}")

    print("=" * 80)
    print("ALL PHASE 6 STRATEGY, RESEARCH, AND COMPETITOR VERIFICATIONS PASSED!")
    print("=" * 80)


if __name__ == "__main__":
    main()
