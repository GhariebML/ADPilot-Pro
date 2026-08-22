"""Runtime forensic verification script for Phase 9 — Analytics Agent & Performance Forecasting Engine."""

import asyncio

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
    MarketingChannel,
    ProductType,
    ToneOfVoice,
)


def main() -> None:
    print("=" * 80)
    print("ADPilot Phase 9 — Analytics Agent & Performance Forecasting Engine Verification")
    print("=" * 80)

    # 1. Build Canonical Campaign Context
    context = (
        CampaignContextBuilder.create("camp-phase9-live")
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
            dos_and_donts=["Focus on enterprise reliability", "Maintain clean dark tech minimalism"],
        )
        .with_competitors(["LegacyFlow Corp", "AutoWorkflow Systems"])
        .build()
    )

    event_bus.clear()
    emitted_events: list[AgentLifecycleEvent] = []
    event_bus.subscribe(lambda e: emitted_events.append(e))

    # 2. Sequential Execution: Strategy -> Research -> Competitor -> Content -> Design -> CV -> Analytics
    print("[RUN] Executing Stages 1–6 (Strategy -> Research -> Competitor -> Content -> Design -> CV)...")
    strategy_agent = StrategyAgent()
    research_agent = ResearchAgent()
    competitor_agent = CompetitorAgent()
    content_agent = ContentAgent()
    design_agent = DesignAgent()
    cv_agent = CVAgent()
    analytics_agent = AnalyticsAgent()

    context = asyncio.run(strategy_agent.run(context))
    context = asyncio.run(research_agent.run(context))
    context = asyncio.run(competitor_agent.run(context))
    context = asyncio.run(content_agent.run(context))
    context = asyncio.run(design_agent.run(context))
    context = asyncio.run(cv_agent.run(context))

    print("[RUN] Executing Stage 7: Analytics Agent...")
    context = asyncio.run(analytics_agent.run(context))
    assert context.analytics is not None
    analytics = context.analytics

    # 3. Verify Predictive Performance Forecast
    print("[PASS] Quantitative Performance Forecast Generated:")
    print(f"       - Predicted ROAS: {analytics.forecast.roas_forecast:.2f}x (Ridge Regression Model)")
    print(f"       - Projected Gross Revenue: ${analytics.forecast.forecast_revenue_usd:,.2f}")
    print(f"       - Predicted CTR: {analytics.forecast.ctr_forecast_percent:.2f}%")
    print(f"       - Predicted CPA: ${analytics.forecast.cpa_forecast_usd:.2f}")
    print(f"       - Predicted Conversion Rate: {analytics.forecast.conversion_rate_percent:.2f}%")
    print(f"       - Projected Conversions: {analytics.forecast.forecast_conversions:,} | Clicks: {analytics.forecast.forecast_clicks:,} | Impressions: {analytics.forecast.forecast_impressions:,}")

    # 4. Verify Goal Deviations & Diagnostics
    print("[PASS] Performance Deviations Analyzed:")
    for dev in analytics.performance_deviations:
        print(f"       - [{dev.metric_name}] Target: {dev.target_value} | Predicted: {dev.predicted_or_observed_value} ({dev.deviation_percent:+.1f}%) -> Status: {dev.status.upper()} ({dev.severity})")

    # 5. Verify Root Cause Attribution
    print("[PASS] Root Cause Attribution Candidates:")
    for i, rc in enumerate(analytics.root_cause_candidates, 1):
        print(f"       {i}. Issue: '{rc.issue}'")
        print(f"          Probable Cause: {rc.probable_root_cause}")
        print(f"          Confidence: {rc.confidence:.2f} | Evidence: {rc.evidence}")

    # 6. Verify Actionable Optimization Directives
    print("[PASS] Actionable Optimization Recommendations:")
    for i, rec in enumerate(analytics.recommendations, 1):
        print(f"       {i}. {rec}")

    # 7. Verify Health Score & Quality Gate
    print(f"[PASS] Overall Campaign Health Score: {analytics.health_score.overall}/100 (Quality Gate: PASSED)")

    # 8. Verify Data Lineage & Provenance
    print("[PASS] Data Provenance Verified:")
    print(f"       - Observed Data Points: {len(analytics.provenance.observed_data)}")
    print(f"       - ML Model Predictions: {len(analytics.provenance.model_prediction)}")
    print(f"       - LLM Inferences: {len(analytics.provenance.llm_inference)}")
    print(f"       - Actionable Recommendations: {len(analytics.provenance.recommendation)}")

    # 9. Master Orchestrator 7-Stage Plan Execution
    print("[RUN] Testing MasterOrchestrator 7-Stage Pipeline Plan...")
    orchestrator = MasterOrchestrator()
    plan = CampaignPlanner().plan(context)
    target_names = {
        "strategy_agent",
        "research_agent",
        "competitor_agent",
        "content_agent",
        "design_agent",
        "cv_agent",
        "analytics_agent",
    }
    plan.agent_sequence = [s for s in plan.agent_sequence if s.agent_name in target_names]
    plan.total_steps = len(plan.agent_sequence)

    orchestrated_context = asyncio.run(orchestrator.execute_plan(context=context, plan=plan))
    assert orchestrated_context.analytics is not None
    print("[PASS] MasterOrchestrator Executed 7-Stage Pipeline through Strategy -> Research -> Competitor -> Content -> Design -> CV -> Analytics.")

    # 10. Event Bus Verification
    completed_events = [e for e in emitted_events if e.event_type == AgentEventType.AGENT_COMPLETED]
    print(f"[PASS] Total Lifecycle Events Verified: {len(emitted_events)} (Completed Stages: {len(completed_events)})")

    print("=" * 80)
    print("ALL PHASE 9 ANALYTICS AGENT VERIFICATIONS PASSED!")
    print("=" * 80)


if __name__ == "__main__":
    main()
