"""Comprehensive test suite for the Canonical CampaignContext and CampaignContextBuilder."""

import pytest
from pydantic import ValidationError

from adpilot.core.context_builder import CampaignContextBuilder
from adpilot.schemas.agent_schemas import (
    CampaignGoal,
    CampaignInput,
    MarketingChannel,
    ToneOfVoice,
)
from adpilot.schemas.campaign_context import (
    BudgetSpec,
    CampaignContext,
    Currency,
    ProductType,
)


def test_saas_campaign_context_creation():
    """Verify construction of a valid SaaS campaign context."""
    context = (
        CampaignContextBuilder.create("camp-saas-101")
        .with_business(
            name="CloudMetrics AI",
            industry="B2B SaaS",
            website_url="https://cloudmetrics.ai",
            tagline="Intelligent Cloud Telemetry",
        )
        .with_product(
            name="CloudMetrics Enterprise",
            product_type=ProductType.saas,
            description="Autonomous Kubernetes telemetry, anomaly detection, and cloud cost management platform.",
            unique_selling_points=["Zero-config eBPF agent", "Real-time cost anomaly alerts", "Sub-second querying"],
            pricing_model="subscription",
            price_tier="Enterprise",
            features=["eBPF tracing", "Slack alerts", "Cost allocation breakdown"],
        )
        .with_goals([CampaignGoal.sales_conversion, CampaignGoal.lead_generation])
        .with_audience(
            summary="VP of Engineering, DevOps Directors, and Site Reliability Engineers",
            psychographics=["Values reliability", "Cost-conscious cloud architecture", "Seeks automation"],
            pain_points=["Unexpected AWS bills", "Alert fatigue", "Blind spots in microservices"],
        )
        .with_geography(target_countries=["US", "GB", "DE"], languages=["en", "de"])
        .with_budget(total_budget=25000.0, currency=Currency.USD, daily_budget_cap=1000.0)
        .with_channels([MarketingChannel.linkedin, MarketingChannel.twitter, MarketingChannel.email])
        .with_timeline(duration_days=30)
        .with_kpis(target_cpa=120.0, target_roas=4.0, target_ctr=2.5, primary_kpi="CPA")
        .with_constraints(max_cpa=180.0, prohibited_keywords=["cheap", "free tier forever"])
        .with_brand(
            tone_of_voice=ToneOfVoice.authoritative,
            brand_colors=["#0F172A", "#38BDF8"],
            font_family="Inter",
        )
        .with_competitors(["Datadog", "Dynatrace", "New Relic"])
        .build()
    )

    assert context.campaign_id == "camp-saas-101"
    assert context.business.name == "CloudMetrics AI"
    assert context.product.product_type == ProductType.saas
    assert context.budget.total_budget == 25000.0
    assert context.budget.currency == Currency.USD
    assert context.timeline.duration_days == 30
    assert context.metadata.fingerprint is not None
    assert len(context.metadata.fingerprint) == 64  # SHA256 hex digest

    # Verify backward compatibility adapter property
    brief = context.brief
    assert isinstance(brief, CampaignInput)
    assert brief.business_name == "CloudMetrics AI"
    assert brief.budget_usd == 25000.0
    assert brief.campaign_duration_days == 30


def test_physical_product_campaign_context():
    """Verify construction of a physical e-commerce product campaign context."""
    context = (
        CampaignContextBuilder.create("camp-phys-202")
        .with_business(name="Aura Audio", industry="Consumer Electronics")
        .with_product(
            name="Aura Pro Wireless Earbuds",
            product_type=ProductType.physical,
            description="Active noise-cancelling titanium acoustic wireless earbuds with 40-hour battery life.",
            unique_selling_points=["Spatial audio", "Custom EQ", "Waterproof IPX8"],
            price_tier="Premium",
        )
        .with_goals([CampaignGoal.sales_conversion])
        .with_audience(summary="Audiophiles, commuters, and fitness enthusiasts aged 20-45")
        .with_budget(total_budget=10000.0, currency=Currency.EUR)
        .with_channels([MarketingChannel.instagram, MarketingChannel.tiktok, MarketingChannel.facebook])
        .with_timeline(duration_days=14)
        .with_brand(tone_of_voice=ToneOfVoice.witty, brand_colors=["#111827", "#F59E0B"])
        .build()
    )

    assert context.product.product_type == ProductType.physical
    assert context.budget.currency == Currency.EUR
    assert context.timeline.duration_days == 14


def test_real_estate_campaign_context():
    """Verify construction of a real estate property development campaign."""
    context = (
        CampaignContextBuilder.create("camp-re-303")
        .with_business(name="Skyline Luxury Properties", industry="Real Estate")
        .with_product(
            name="The Grand Horizon Penthouse Collection",
            product_type=ProductType.real_estate,
            description="Ultra-luxury 3-bedroom and 4-bedroom beachfront residential apartments in Miami.",
            price_tier="Ultra-Luxury",
        )
        .with_goals([CampaignGoal.lead_generation])
        .with_audience(summary="High-net-worth individuals and international real estate investors")
        .with_geography(target_countries=["US", "CA", "AE"])
        .with_budget(total_budget=50000.0, currency=Currency.USD)
        .with_channels([MarketingChannel.instagram, MarketingChannel.linkedin])
        .with_timeline(duration_days=60)
        .with_brand(tone_of_voice=ToneOfVoice.authoritative, brand_colors=["#000000", "#D4AF37"])
        .build()
    )

    assert context.product.product_type == ProductType.real_estate
    assert context.budget.total_budget == 50000.0
    assert context.timeline.duration_days == 60


def test_service_campaign_context():
    """Verify construction of a professional service campaign context."""
    context = (
        CampaignContextBuilder.create("camp-srv-404")
        .with_business(name="Apex Growth Partners", industry="Management Consulting")
        .with_product(
            name="Enterprise Fractional CMO Advisory",
            product_type=ProductType.service,
            description="Executive strategic marketing consulting and revenue operations advisory for Series B+ startups.",
        )
        .with_goals([CampaignGoal.lead_generation])
        .with_audience(summary="Series B founders and growth-stage CEOs")
        .with_budget(total_budget=15000.0, currency=Currency.USD)
        .with_channels([MarketingChannel.linkedin, MarketingChannel.email])
        .with_timeline(duration_days=45)
        .with_brand(tone_of_voice=ToneOfVoice.professional)
        .build()
    )

    assert context.product.product_type == ProductType.service
    assert context.budget.total_budget == 15000.0


def test_factory_from_brief_normalization():
    """Verify factory construction from legacy CampaignInput and dictionary briefs."""
    legacy_input = CampaignInput(
        business_name="Nordic Coffee Co",
        product_description="Specialty organic single-origin roasted coffee beans delivered weekly",
        target_market="Coffee connoisseurs and remote workers",
        budget_usd=3500.0,
        goals=[CampaignGoal.sales_conversion],
        channels=[MarketingChannel.instagram, MarketingChannel.email],
        tone_of_voice=ToneOfVoice.friendly,
        brand_colors=["#78350F", "#FBBF24"],
        competitors=["Blue Bottle", "Stumptown"],
        campaign_duration_days=14,
    )

    context = CampaignContextBuilder.from_brief(legacy_input, campaign_id="camp-legacy-505")
    assert context.campaign_id == "camp-legacy-505"
    assert context.business.name == "Nordic Coffee Co"
    assert context.budget.total_budget == 3500.0
    assert context.product.product_type == ProductType.physical  # Inferred from coffee/beans
    assert context.timeline.duration_days == 14


def test_validation_errors_missing_required_fields():
    """Verify validation errors when required fields are missing."""
    builder = CampaignContextBuilder.create()
    with pytest.raises(ValueError, match="Business information is required"):
        builder.build()

    builder.with_business(name="Acme Corp")
    with pytest.raises(ValueError, match="Product specifications are required"):
        builder.build()

    builder.with_product(name="Acme Widget", description="A widget for everything")
    with pytest.raises(ValueError, match="Target audience is required"):
        builder.build()

    builder.with_audience(summary="Target consumers")
    with pytest.raises(ValueError, match="Budget specification is required"):
        builder.build()


def test_validation_errors_budget_rules():
    """Verify budget validation rules (positive, daily cap constraint)."""
    # Daily budget cap > Total budget
    with pytest.raises(ValidationError):
        BudgetSpec(total_budget=500.0, daily_budget_cap=1000.0)

    # Negative total budget
    with pytest.raises(ValidationError):
        BudgetSpec(total_budget=-500.0)


def test_validation_errors_timeline_rules():
    """Verify timeline validation rules (duration between 7 and 365 days)."""
    builder = (
        CampaignContextBuilder.create()
        .with_business(name="Test Co")
        .with_product(name="Test Item", description="Test item description")
        .with_audience(summary="Test audience")
        .with_budget(total_budget=1000.0)
    )

    with pytest.raises(ValidationError):
        builder.with_timeline(duration_days=3)  # < 7 days


def test_validation_errors_invalid_hex_colors():
    """Verify invalid hex colors fail validation."""
    builder = (
        CampaignContextBuilder.create()
        .with_business(name="Test Co")
        .with_product(name="Test Item", description="Test item description")
        .with_audience(summary="Test audience")
        .with_budget(total_budget=1000.0)
        .with_timeline(duration_days=14)
    )

    with pytest.raises(ValueError, match="Invalid hex color code"):
        builder.with_brand(brand_colors=["not-a-hex-color"])


def test_serialization_and_deserialization_roundtrip():
    """Verify complete JSON serialization and deserialization roundtrip."""
    context = (
        CampaignContextBuilder.create("camp-json-606")
        .with_business(name="DataSync Pro", industry="Cloud SaaS")
        .with_product(name="DataSync ETL", product_type=ProductType.saas, description="Real-time multi-cloud data pipeline ETL.")
        .with_goals([CampaignGoal.lead_generation])
        .with_audience(summary="Data Engineers and Cloud Architects")
        .with_budget(total_budget=12000.0, currency=Currency.USD)
        .with_channels([MarketingChannel.linkedin, MarketingChannel.twitter])
        .with_timeline(duration_days=30)
        .build()
    )

    json_str = context.to_json()
    assert isinstance(json_str, str)

    restored = CampaignContext.from_json(json_str)
    assert restored.campaign_id == context.campaign_id
    assert restored.business.name == context.business.name
    assert restored.budget.total_budget == context.budget.total_budget
    assert restored.metadata.fingerprint == context.metadata.fingerprint


def test_agent_output_recording_and_audit_lineage():
    """Verify recording agent outputs updates revision and audit change log."""
    context = (
        CampaignContextBuilder.create("camp-audit-707")
        .with_business(name="Nova Dynamics")
        .with_product(name="Nova Core", description="Robotics automation engine")
        .with_audience(summary="Manufacturing Plant Directors")
        .with_budget(total_budget=20000.0)
        .with_timeline(duration_days=30)
        .build()
    )

    assert context.metadata.revision == 1
    assert len(context.metadata.change_log) == 0

    # Record agent output
    context.record_agent_output("strategy_agent", {"pillars": ["Scale", "Safety"]})
    assert context.metadata.revision == 2
    assert len(context.metadata.change_log) == 1
    assert context.metadata.change_log[0]["agent"] == "strategy_agent"

    context.record_agent_output("content_agent", {"ads_count": 5})
    assert context.metadata.revision == 3
    assert len(context.metadata.change_log) == 2


def test_pipeline_context_travel_without_information_loss():
    """Verify that CampaignContext travels through multiple pipeline stages preserving canonical data."""
    initial_context = (
        CampaignContextBuilder.create("camp-travel-808")
        .with_business(
            name="Quantum Payments",
            industry="Fintech",
            website_url="https://quantumpay.io",
            tagline="Sub-millisecond Global Settlements",
        )
        .with_product(
            name="Quantum Rail",
            product_type=ProductType.saas,
            description="Cross-border instant B2B settlement infrastructure with zero FX slippage.",
            unique_selling_points=["Sub-second settlement", "Zero FX markup", "Direct central bank integration"],
            pricing_model="subscription",
            features=["ISO 20022 ready", "Real-time AML screening"],
        )
        .with_goals([CampaignGoal.lead_generation, CampaignGoal.brand_awareness])
        .with_audience(
            summary="Chief Financial Officers and Treasury Heads at Tier-1 Financial Institutions",
            pain_points=["High correspondent banking fees", "T+2 settlement delays"],
        )
        .with_geography(target_countries=["US", "GB", "SG", "CH"], languages=["en"])
        .with_budget(total_budget=75000.0, currency=Currency.USD, daily_budget_cap=2500.0)
        .with_channels([MarketingChannel.linkedin, MarketingChannel.email])
        .with_timeline(duration_days=60)
        .with_kpis(target_cpa=250.0, target_roas=5.0, primary_kpi="ROAS")
        .with_constraints(max_cpa=350.0, prohibited_keywords=["guaranteed profits", "risk-free"])
        .with_brand(
            tone_of_voice=ToneOfVoice.authoritative,
            brand_colors=["#0A192F", "#64FFDA"],
        )
        .with_competitors(["Stripe Treasury", "Wise Business", "Ripple Payments"])
        .build()
    )

    orig_fingerprint = initial_context.metadata.fingerprint

    # Stage 1: Strategy Agent Execution
    strategy_mock = {
        "messaging_pillars": [{"title": "Instant Liquidity", "description": "Free up working capital"}],
        "target_channels": ["linkedin", "email"],
    }
    initial_context.record_agent_output("strategy_agent", strategy_mock)

    # Stage 2: Content Agent Execution
    content_mock = {
        "headlines": ["Settle Global Payments in 200ms", "Eliminate T+2 FX Slippage"],
        "ad_copies": ["Quantum Rail replaces legacy correspondent banking."],
    }
    initial_context.record_agent_output("content_agent", content_mock)

    # Stage 3: Analytics Quality Gate
    analytics_mock = {
        "health_score": {"overall": 88.5, "clarity": 90.0, "compliance": 95.0},
        "passed": True,
    }
    initial_context.record_agent_output("analytics_agent", analytics_mock)

    # Verification: Canonical business, product, budget, and constraints are 100% intact
    assert initial_context.campaign_id == "camp-travel-808"
    assert initial_context.business.name == "Quantum Payments"
    assert initial_context.business.website_url == "https://quantumpay.io"
    assert initial_context.product.name == "Quantum Rail"
    assert initial_context.product.product_type == ProductType.saas
    assert initial_context.budget.total_budget == 75000.0
    assert initial_context.budget.daily_budget_cap == 2500.0
    assert initial_context.timeline.duration_days == 60
    assert initial_context.constraints.prohibited_keywords == ["guaranteed profits", "risk-free"]
    assert initial_context.metadata.fingerprint == orig_fingerprint
    assert initial_context.metadata.revision == 4
    assert len(initial_context.metadata.change_log) == 3

    # Verification: Agent outputs are cleanly accumulated
    assert initial_context.strategy == strategy_mock
    assert initial_context.content == content_mock
    assert initial_context.analytics == analytics_mock


def test_multi_currency_support():
    """Verify ISO 4217 multi-currency support across all valid currencies."""
    for curr in [Currency.USD, Currency.EUR, Currency.GBP, Currency.CAD, Currency.AUD, Currency.JPY, Currency.CHF]:
        ctx = (
            CampaignContextBuilder.create()
            .with_business(name="Global Brand")
            .with_product(name="Global Item", description="Worldwide available product")
            .with_audience(summary="Global buyers")
            .with_budget(total_budget=100000.0, currency=curr)
            .with_timeline(duration_days=30)
            .build()
        )
        assert ctx.budget.currency == curr

