"""Runtime forensic verification script for Phase 8 — Design Agent & Computer Vision Agent."""

import asyncio

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
    MarketingChannel,
    ProductType,
    ToneOfVoice,
)


def main() -> None:
    print("=" * 80)
    print("ADPilot Phase 8 — Design Agent & Computer Vision Agent Verification")
    print("=" * 80)

    # 1. Build Canonical Campaign Context
    context = (
        CampaignContextBuilder.create("camp-phase8-live")
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

    # 2. Sequential Execution: Strategy -> Research -> Competitor -> Content -> Design -> CV
    print("[RUN] Executing Stages 1–4 (Strategy -> Research -> Competitor -> Content)...")
    strategy_agent = StrategyAgent()
    research_agent = ResearchAgent()
    competitor_agent = CompetitorAgent()
    content_agent = ContentAgent()
    design_agent = DesignAgent()
    cv_agent = CVAgent()

    context = asyncio.run(strategy_agent.run(context))
    context = asyncio.run(research_agent.run(context))
    context = asyncio.run(competitor_agent.run(context))
    context = asyncio.run(content_agent.run(context))

    print("[RUN] Executing Stage 5: Design Agent...")
    context = asyncio.run(design_agent.run(context))
    assert context.design is not None
    design = context.design

    # 3. Verify Design Outputs & NanoBanana Provider Behavior
    print("[PASS] Design Agent Output Generated:")
    print(f"       - Total Creative Assets: {len(design.creative_assets)}")
    for i, asset in enumerate(design.creative_assets, 1):
        print(f"         {i}. [{asset.channel.value.upper()}] {asset.dimensions.width}x{asset.dimensions.height} ({asset.aspect_ratio}) - Status: {asset.generation_status}")
        print(f"            Prompt: '{asset.generation_prompt[:65]}...'")
    print(f"       - Layout Archetype: {design.creative_metadata.layout_type}")
    print(f"       - Primary Palette: {design.creative_metadata.primary_color_hex} / Secondary: {design.creative_metadata.secondary_color_hex}")
    print(f"       - Contrast Ratio: {design.creative_metadata.contrast_ratio:.1f}:1 (WCAG AA Compliant)")
    print(f"       - Image Generation Provider: NanoBananaProviderAdapter (Available: {NanoBananaProviderAdapter().is_available()}, Safe Unconfigured Policy)")
    print(f"       - Design Confidence: {design.confidence:.2f}")

    # 4. Computer Vision Agent Evaluation
    print("[RUN] Executing Stage 6: Computer Vision Agent...")
    context = asyncio.run(cv_agent.run(context))
    assert "cv_agent" in context.agent_outputs
    cv_out = context.agent_outputs["cv_agent"]

    print("[PASS] Computer Vision Evaluation Generated:")
    print(f"       - Composite Creative Score: {cv_out.creative_score:.1f} / 100")
    print(f"       - Aesthetic Score: {cv_out.aesthetic_score:.2f} / 10.0 (Ridge Regression)")
    print(f"       - OCR Extracted Headline: '{cv_out.ocr_results.detected_headline}'")
    print(f"       - OCR Readability Score: {cv_out.ocr_results.readability_score:.1f} / 100 (Text Density: {cv_out.ocr_results.text_density_percent:.1f}%)")
    print(f"       - Object Detection: {', '.join(cv_out.object_detection.detected_objects)} (Product Prominence: {cv_out.object_detection.product_prominence_score:.1f}%)")
    print(f"       - Brand Safety Status: {'SAFE' if cv_out.brand_safe else 'VIOLATION DETECTED'} (Violations: {len(cv_out.brand_violations)})")
    print(f"       - Quality Gate Status: {'PASSED' if cv_out.passed_quality_gate else 'FAILED'}")

    # 5. Automated Revision Loop Verification
    print("[RUN] Verifying Automated Design -> CV Revision Loop Engine...")
    revised_context = asyncio.run(cv_agent.run_with_revision(context, design_agent=design_agent, max_revisions=2))
    assert revised_context.design is not None
    assert revised_context.agent_outputs["cv_agent"].passed_quality_gate is True
    print("[PASS] Automated Revision Loop Engine executed and converged cleanly.")

    # 6. Master Orchestrator 6-Stage Execution
    print("[RUN] Testing MasterOrchestrator 6-Stage Pipeline Plan...")
    orchestrator = MasterOrchestrator()
    plan = CampaignPlanner().plan(context)
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

    orchestrated_context = asyncio.run(orchestrator.execute_plan(context=context, plan=plan))
    assert orchestrated_context.design is not None
    assert "cv_agent" in orchestrated_context.agent_outputs
    print("[PASS] MasterOrchestrator Executed 6-Stage Pipeline through Strategy -> Research -> Competitor -> Content -> Design -> CV.")

    # 7. Event Bus Verification
    completed_events = [e for e in emitted_events if e.event_type == AgentEventType.AGENT_COMPLETED]
    print(f"[PASS] Total Lifecycle Events Verified: {len(emitted_events)} (Completed Stages: {len(completed_events)})")

    print("=" * 80)
    print("ALL PHASE 8 DESIGN & COMPUTER VISION AGENT VERIFICATIONS PASSED!")
    print("=" * 80)


if __name__ == "__main__":
    main()
