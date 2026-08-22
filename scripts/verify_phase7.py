"""Runtime verification script for Phase 7 — Content Agent and Content Evaluation System."""

import asyncio

from adpilot.agents import (
    CompetitorAgent,
    ContentAgent,
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
    MarketingChannel,
    ProductType,
    ToneOfVoice,
)


def main() -> None:
    print("=" * 80)
    print("ADPilot Phase 7 — Content Agent & Content Evaluation System Verification")
    print("=" * 80)

    # 1. Build Canonical Campaign Context
    context = (
        CampaignContextBuilder.create("camp-phase7-live")
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
            dos_and_donts=["Focus on enterprise reliability", "Highlight workflow speed"],
        )
        .with_competitors(["LegacyFlow Corp", "AutoWorkflow Systems"])
        .build()
    )

    event_bus.clear()
    emitted_events: list[AgentLifecycleEvent] = []
    event_bus.subscribe(lambda e: emitted_events.append(e))

    # 2. Sequential Execution: Strategy -> Research -> Competitor -> Content
    print("[RUN] Executing upstream Stage 1–3 agents...")
    strategy_agent = StrategyAgent()
    research_agent = ResearchAgent()
    competitor_agent = CompetitorAgent()
    content_agent = ContentAgent()

    context = asyncio.run(strategy_agent.run(context))
    context = asyncio.run(research_agent.run(context))
    context = asyncio.run(competitor_agent.run(context))

    print("[RUN] Executing Stage 4: Content Agent...")
    context = asyncio.run(content_agent.run(context))
    assert context.content is not None
    content = context.content

    # 3. Content Package Outputs Verification
    assert len(content.headlines) >= 2
    assert len(content.primary_copy) >= 1
    assert len(content.descriptions) >= 1
    assert len(content.ctas) >= 1
    assert content.seo_metadata is not None
    assert len(content.keywords) >= 1
    assert len(content.content_variations) >= 2

    print("[PASS] Content Package Generated Successfully:")
    print(f"       - Primary Headline: '{content.headlines[0]}'")
    print(f"       - Primary Copy Sample: '{content.primary_copy[0][:80]}...'")
    print(f"       - SEO Title: '{content.seo_metadata.title}'")
    print(f"       - SEO Meta Description: '{content.seo_metadata.meta_description[:75]}...'")
    print(f"       - Target Keywords ({len(content.keywords)}): {', '.join(content.keywords[:3])}...")
    print(f"       - Multi-Channel Variations: {len(content.content_variations)} (Channels: {', '.join(v.channel.value for v in content.content_variations)})")
    print(f"       - Confidence: {content.confidence:.2f}")

    # 4. Evaluation Engine Verification
    eval_report = content.evaluation
    assert eval_report is not None
    assert eval_report.passed_quality_gate is True

    print("[PASS] Content Evaluation Report Generated:")
    print(f"       - Content Quality Score: {eval_report.content_quality_score:.1f}/100")
    print(f"       - Strategic Relevance Score: {eval_report.relevance_score:.1f}/100")
    print(f"       - Keyword Coverage: {eval_report.keyword_coverage_score:.1f}% ({len(eval_report.covered_keywords)} covered, {len(eval_report.missing_keywords)} missing)")
    print(f"       - Brand Compliance Score: {eval_report.brand_compliance_score:.1f}/100")
    print(f"       - Hallucination Risk Score: {eval_report.hallucination_risk_score:.1f}/100 (Unsupported Claims: {len(eval_report.detected_unsupported_claims)})")
    if eval_report.ml_quality_prediction is not None:
        print(f"       - ML Model Prediction (Ridge Regression): {eval_report.ml_quality_prediction:.4f}")
    print(f"       - Quality Gate Status: {'PASSED' if eval_report.passed_quality_gate else 'FAILED'}")

    # 5. Data Provenance Verification
    prov = content.provenance
    assert prov is not None
    assert len(prov.observed_data) > 0
    assert len(prov.model_prediction) > 0
    assert len(prov.llm_inference) > 0
    assert len(prov.recommendation) > 0

    print("[PASS] Data Provenance Segregation Verified:")
    print(f"       - Observed Data items: {len(prov.observed_data)}")
    print(f"       - Model Prediction items: {len(prov.model_prediction)}")
    print(f"       - LLM Inference items: {len(prov.llm_inference)}")
    print(f"       - Recommendation items: {len(prov.recommendation)}")

    # 6. Master Orchestrator Verification
    print("[RUN] Testing MasterOrchestrator 4-Stage Execution Plan...")
    orchestrator = MasterOrchestrator()
    plan = CampaignPlanner().plan(context)
    target_names = {"strategy_agent", "research_agent", "competitor_agent", "content_agent"}
    plan.agent_sequence = [s for s in plan.agent_sequence if s.agent_name in target_names]
    plan.total_steps = len(plan.agent_sequence)

    orchestrated_context = asyncio.run(orchestrator.execute_plan(context=context, plan=plan))
    assert orchestrated_context.content is not None

    print("[PASS] MasterOrchestrator Plan Execution Verified through Strategy -> Research -> Competitor -> Content.")

    # 7. Event Bus Verification
    assert len(emitted_events) >= 8
    content_events = [e for e in emitted_events if e.agent_id == "content_agent"]
    completed_event = [e for e in content_events if e.event_type == AgentEventType.AGENT_COMPLETED][-1]
    print(f"[PASS] Event Verified: {completed_event.event_type.value} | agent={completed_event.agent_id}, status={completed_event.status}, latency={completed_event.latency:.4f}s, confidence={completed_event.confidence}")

    print("=" * 80)
    print("ALL PHASE 7 CONTENT AGENT AND EVALUATOR VERIFICATIONS PASSED!")
    print("=" * 80)


if __name__ == "__main__":
    main()
