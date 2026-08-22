"""Verification script for Phase 2 — Unified Campaign Context Builder."""

import json
from adpilot.core.context_builder import CampaignContextBuilder
from adpilot.schemas.agent_schemas import (
    CampaignGoal,
    CampaignInput,
    MarketingChannel,
    ToneOfVoice,
)
from adpilot.schemas.campaign_context import (
    CampaignContext,
    Currency,
    ProductType,
)


def main() -> None:
    print("=" * 70)
    print("ADPilot Phase 2 — Unified Campaign Context Builder Verification")
    print("=" * 70)

    # 1. SaaS Product Context Construction
    saas_ctx = (
        CampaignContextBuilder.create("camp-saas-001")
        .with_business(
            name="SaaSFlow Analytics",
            industry="Data Analytics",
            website_url="https://saasflow.io",
            tagline="Real-time Revenue Intelligence",
        )
        .with_product(
            name="SaaSFlow Pro",
            product_type=ProductType.saas,
            description="Autonomous subscription churn prediction and MRR analytics platform.",
            unique_selling_points=["AI churn prediction", "Automated billing recovery", "Instant Stripe sync"],
            pricing_model="subscription",
            price_tier="Growth",
            features=["Churn forecasting", "Cohort analytics", "Slack alerts"],
        )
        .with_goals([CampaignGoal.sales_conversion, CampaignGoal.lead_generation])
        .with_audience(
            summary="SaaS Founders, Head of Growth, and Revenue Operations Leads",
            pain_points=["High customer churn", "Inaccurate MRR reporting"],
        )
        .with_geography(target_countries=["US", "GB", "CA"], languages=["en"])
        .with_budget(total_budget=15000.0, currency=Currency.USD, daily_budget_cap=500.0)
        .with_channels([MarketingChannel.linkedin, MarketingChannel.twitter, MarketingChannel.email])
        .with_timeline(duration_days=30)
        .with_kpis(target_cpa=150.0, target_roas=4.5, primary_kpi="ROAS")
        .with_constraints(max_cpa=200.0, prohibited_keywords=["guaranteed 10x growth"])
        .with_brand(
            tone_of_voice=ToneOfVoice.authoritative,
            brand_colors=["#1E293B", "#3B82F6"],
        )
        .with_competitors(["ProfitWell", "Baremetrics", "ChartMogul"])
        .build()
    )
    print(f"[PASS] 1. SaaS Context: id={saas_ctx.campaign_id}, type={saas_ctx.product.product_type.value}, budget=${saas_ctx.budget.total_budget:,.2f}")

    # 2. Physical Product Context Construction
    phys_ctx = (
        CampaignContextBuilder.create("camp-phys-002")
        .with_business(name="Nordic Goods", industry="Apparel & Lifestyle")
        .with_product(
            name="Merino Wool Performance Hoodie",
            product_type=ProductType.physical,
            description="Ultra-fine 100% sustainable Merino wool hoodie with thermal regulation.",
            unique_selling_points=["Odor resistant", "Machine washable", "Zero scratch"],
            price_tier="Premium",
        )
        .with_goals([CampaignGoal.sales_conversion])
        .with_audience(summary="Outdoor enthusiasts, remote workers, and minimalist travelers")
        .with_budget(total_budget=8000.0, currency=Currency.EUR)
        .with_channels([MarketingChannel.instagram, MarketingChannel.tiktok, MarketingChannel.facebook])
        .with_timeline(duration_days=21)
        .with_brand(tone_of_voice=ToneOfVoice.friendly, brand_colors=["#2D3748", "#E2E8F0"])
        .build()
    )
    print(f"[PASS] 2. Physical Product Context: id={phys_ctx.campaign_id}, type={phys_ctx.product.product_type.value}, budget=€{phys_ctx.budget.total_budget:,.2f}")

    # 3. Real Estate Product Context Construction
    re_ctx = (
        CampaignContextBuilder.create("camp-re-003")
        .with_business(name="Vanguard Developments", industry="Real Estate")
        .with_product(
            name="The Azure Sky Penthouse Collection",
            product_type=ProductType.real_estate,
            description="Exclusive luxury waterfront residences with private helicopter pad.",
            price_tier="Ultra-Luxury",
        )
        .with_goals([CampaignGoal.lead_generation])
        .with_audience(summary="High-net-worth investors and luxury real estate buyers")
        .with_budget(total_budget=40000.0, currency=Currency.USD)
        .with_channels([MarketingChannel.linkedin, MarketingChannel.instagram])
        .with_timeline(duration_days=60)
        .with_brand(tone_of_voice=ToneOfVoice.authoritative, brand_colors=["#000000", "#C5A880"])
        .build()
    )
    print(f"[PASS] 3. Real Estate Context: id={re_ctx.campaign_id}, type={re_ctx.product.product_type.value}, duration={re_ctx.timeline.duration_days} days")

    # 4. Professional Service Context Construction
    srv_ctx = (
        CampaignContextBuilder.create("camp-srv-004")
        .with_business(name="Beacon Growth Partners", industry="Management Advisory")
        .with_product(
            name="Fractional Chief Revenue Officer Advisory",
            product_type=ProductType.service,
            description="B2B go-to-market architecture and enterprise sales team scaling advisory.",
        )
        .with_goals([CampaignGoal.lead_generation])
        .with_audience(summary="Series A and B B2B software founders")
        .with_budget(total_budget=12000.0, currency=Currency.GBP)
        .with_channels([MarketingChannel.linkedin, MarketingChannel.email])
        .with_timeline(duration_days=45)
        .with_brand(tone_of_voice=ToneOfVoice.professional)
        .build()
    )
    print(f"[PASS] 4. Professional Service Context: id={srv_ctx.campaign_id}, type={srv_ctx.product.product_type.value}, currency={srv_ctx.budget.currency.value}")

    # 5. Serialization & Deserialization Roundtrip Check
    raw_json = saas_ctx.to_json(indent=2)
    restored_ctx = CampaignContext.from_json(raw_json)
    assert restored_ctx.campaign_id == saas_ctx.campaign_id
    assert restored_ctx.metadata.fingerprint == saas_ctx.metadata.fingerprint
    assert restored_ctx.budget.total_budget == saas_ctx.budget.total_budget
    print(f"[PASS] 5. Serialization & Deserialization: Fingerprint match ({saas_ctx.metadata.fingerprint[:16]}...)")

    # 6. Pipeline Context Travel & Audit Trail Check
    print(f"       Initial revision: {saas_ctx.metadata.revision}")
    saas_ctx.record_agent_output("strategy_agent", {"pillars": ["Automation", "ROI"]})
    saas_ctx.record_agent_output("content_agent", {"ads_generated": 6})
    saas_ctx.record_agent_output("analytics_agent", {"health_score": 92.4, "passed": True})
    assert saas_ctx.metadata.revision == 4
    assert len(saas_ctx.metadata.change_log) == 3
    print(f"[PASS] 6. Pipeline Context Travel: 3 stages recorded, Final revision={saas_ctx.metadata.revision}")

    # 7. Backward Compatibility Adapter (.brief property)
    brief_adapter = saas_ctx.brief
    assert isinstance(brief_adapter, CampaignInput)
    assert brief_adapter.business_name == "SaaSFlow Analytics"
    assert brief_adapter.budget_usd == 15000.0
    assert brief_adapter.campaign_duration_days == 30
    print(f"[PASS] 7. Backward Compatibility Bridge: brief.business_name='{brief_adapter.business_name}', budget_usd={brief_adapter.budget_usd}")

    print("=" * 70)
    print("ALL PHASE 2 CAMPAIGN CONTEXT VERIFICATIONS PASSED SUCCESSFULLY!")
    print("=" * 70)


if __name__ == "__main__":
    main()
