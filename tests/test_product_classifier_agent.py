"""Unit and integration tests for Phase 3 Product Classifier Agent."""

import asyncio
import pytest
from adpilot.agents.product_classifier_agent import ProductClassifierAgent
from adpilot.core.context_builder import CampaignContextBuilder
from adpilot.schemas.agent_schemas import (
    ExecutionMode,
    ProductType,
)


@pytest.fixture
def classifier_agent():
    return ProductClassifierAgent()


def test_saas_product_classification_heuristics(classifier_agent):
    context = (
        CampaignContextBuilder.create("camp-saas-001")
        .with_business(name="MetricStream Cloud", industry="Cloud Observability")
        .with_product(
            name="MetricStream Enterprise",
            product_type=ProductType.saas,
            description="Autonomous Kubernetes telemetry, APM metrics, and microservices log analytics platform.",
            unique_selling_points=["Sub-second query speed", "Enterprise SSO", "Slack incident alerts"],
            pricing_model="subscription",
        )
        .with_audience(summary="DevOps and SRE Engineers")
        .with_budget(total_budget=10000.0)
        .with_timeline(duration_days=30)
        .build()
    )

    result_context = asyncio.run(classifier_agent.run(context))
    assert result_context.classification is not None
    classification = result_context.classification

    assert classification.product_type == ProductType.saas
    assert classification.confidence >= 0.70
    assert classification.needs_clarification is False
    assert "subscription" in classification.reason.lower() or "software" in classification.reason.lower()
    assert "strategy_agent" in classification.required_agents


def test_physical_product_classification_heuristics(classifier_agent):
    context = (
        CampaignContextBuilder.create("camp-phys-002")
        .with_business(name="Urban Athletics", industry="Apparel")
        .with_product(
            name="HydroShield Running Hoodie",
            product_type=ProductType.physical,
            description="Water-repellent thermal running hoodie with reflective night-safety strips.",
            unique_selling_points=["Breathable membrane", "Zero bulk", "Machine washable"],
        )
        .with_audience(summary="Marathon runners and outdoor athletes")
        .with_budget(total_budget=5000.0)
        .with_timeline(duration_days=30)
        .build()
    )

    result_context = asyncio.run(classifier_agent.run(context))
    assert result_context.classification is not None
    classification = result_context.classification

    assert classification.product_type == ProductType.physical
    assert classification.confidence >= 0.70
    assert classification.recommended_execution_mode == ExecutionMode.direct_response
    assert "design_agent" in classification.required_agents


def test_real_estate_product_classification_heuristics(classifier_agent):
    context = (
        CampaignContextBuilder.create("camp-re-003")
        .with_business(name="Elysium Properties", industry="Real Estate")
        .with_product(
            name="The Azure Marina Penthouse",
            product_type=ProductType.real_estate,
            description="Luxury residential waterfront penthouse with panoramic sea views and private concierge.",
        )
        .with_audience(summary="High-net-worth real estate buyers")
        .with_budget(total_budget=25000.0)
        .with_timeline(duration_days=30)
        .build()
    )

    result_context = asyncio.run(classifier_agent.run(context))
    classification = result_context.classification

    assert classification.product_type == ProductType.real_estate
    assert classification.confidence >= 0.70
    assert classification.recommended_execution_mode == ExecutionMode.lead_nurture
    assert any("housing" in c.lower() or "disclaimer" in c.lower() for c in classification.relevant_constraints)


def test_service_product_classification_heuristics(classifier_agent):
    context = (
        CampaignContextBuilder.create("camp-srv-004")
        .with_business(name="Apex GTM Advisory", industry="Consulting")
        .with_product(
            name="Fractional Chief Marketing Officer Advisory",
            product_type=ProductType.service,
            description="B2B enterprise go-to-market advisory, brand positioning, and executive consulting.",
        )
        .with_audience(summary="Founders and CEOs of B2B scaleups")
        .with_budget(total_budget=8000.0)
        .with_timeline(duration_days=30)
        .build()
    )

    result_context = asyncio.run(classifier_agent.run(context))
    classification = result_context.classification

    assert classification.product_type == ProductType.service
    assert classification.confidence >= 0.70
    assert classification.recommended_execution_mode == ExecutionMode.lead_nurture


def test_marketplace_product_classification_heuristics(classifier_agent):
    context = (
        CampaignContextBuilder.create("camp-mkt-005")
        .with_business(name="TalentGrid", industry="Freelance Platform")
        .with_product(
            name="TalentGrid Marketplace",
            product_type=ProductType.marketplace,
            description="Two-sided freelance marketplace connecting verified AI developers with enterprise buyers.",
        )
        .with_audience(summary="Freelancers and hiring managers")
        .with_budget(total_budget=15000.0)
        .with_timeline(duration_days=30)
        .build()
    )

    result_context = asyncio.run(classifier_agent.run(context))
    classification = result_context.classification

    assert classification.product_type == ProductType.marketplace
    assert classification.recommended_execution_mode == ExecutionMode.marketplace_liquidity


def test_education_product_classification_heuristics(classifier_agent):
    context = (
        CampaignContextBuilder.create("camp-edu-006")
        .with_business(name="AI Builders Academy", industry="EdTech")
        .with_product(
            name="LLM Systems Engineering Bootcamp",
            product_type=ProductType.education,
            description="10-week intensive cohort bootcamp training software engineers on production LLM architecture.",
        )
        .with_audience(summary="Senior Software Engineers")
        .with_budget(total_budget=12000.0)
        .with_timeline(duration_days=30)
        .build()
    )

    result_context = asyncio.run(classifier_agent.run(context))
    classification = result_context.classification

    assert classification.product_type == ProductType.education
    assert classification.recommended_execution_mode == ExecutionMode.enrollment_funnel


def test_low_confidence_and_ambiguity_triggers_hitl(classifier_agent):
    context = (
        CampaignContextBuilder.create("camp-amb-007")
        .with_business(name="Unknown Corp", industry="General")
        .with_product(
            name="Item X",
            description="Stuff for sale",
        )
        .with_audience(summary="General people")
        .with_budget(total_budget=1000.0)
        .with_timeline(duration_days=30)
        .build()
    )

    result_context = asyncio.run(classifier_agent.run(context))
    classification = result_context.classification

    assert classification.confidence < 0.70
    assert classification.needs_clarification is True
    assert classification.clarification_prompt is not None
    # Verify Human-in-the-Loop was triggered
    assert result_context.approvals.human_approval_required is True


def test_immutability_preserves_original_user_input(classifier_agent):
    original_description = "Specialized AI workflow software for bio-pharmaceutical research."
    context = (
        CampaignContextBuilder.create("camp-immut-008")
        .with_business(name="BioSynth Labs", industry="Life Sciences", website_url="https://biosynth.bio")
        .with_product(
            name="SynthPipeline Pro",
            description=original_description,
            pricing_model="annual license",
        )
        .with_audience(summary="Biotech researchers and lab managers")
        .with_budget(total_budget=50000.0)
        .with_timeline(duration_days=30)
        .build()
    )

    initial_revision = context.metadata.revision
    result_context = asyncio.run(classifier_agent.run(context))

    # Business and Product input must remain strictly identical
    assert result_context.product.description == original_description
    assert result_context.business.name == "BioSynth Labs"
    assert result_context.business.website_url == "https://biosynth.bio"
    # Revision and audit change_log must have incremented
    assert result_context.metadata.revision == initial_revision + 1
    assert any(log["agent"] == "product_classifier_agent" for log in result_context.metadata.change_log)


def test_product_classifier_llm_mock_parsing(monkeypatch, classifier_agent):
    mock_payload = {
        "product_type": "saas",
        "confidence": 0.98,
        "reason": "Clear B2B SaaS platform with cloud delivery and subscription tiers.",
        "business_characteristics": ["High MRR expansion", "Self-service onboarding"],
        "recommended_execution_mode": "enterprise_sales_cycle",
        "relevant_constraints": ["SOC2 compliance messaging"],
        "required_agents": ["strategy_agent", "content_agent", "analytics_agent"],
        "optional_agents": ["design_agent"],
        "needs_clarification": False,
        "clarification_prompt": None,
        "operating_mode_summary": "High-growth B2B SaaS telemetry platform.",
    }

    async def fake_call_llm(self, **kwargs):
        return self.validate_output(mock_payload)

    monkeypatch.setattr(
        "adpilot.agents.product_classifier_agent.ProductClassifierAgent.call_llm",
        fake_call_llm,
    )

    context = (
        CampaignContextBuilder.create("camp-llm-009")
        .with_business(name="DataPulse", industry="Fintech")
        .with_product(name="DataPulse Engine", description="Financial ledger streaming API")
        .with_audience(summary="Fintech developers")
        .with_budget(total_budget=20000.0)
        .with_timeline(duration_days=30)
        .build()
    )

    result_context = asyncio.run(classifier_agent.run(context))
    assert result_context.classification.confidence == 0.98
    assert result_context.classification.product_type == ProductType.saas
    assert result_context.classification.recommended_execution_mode == ExecutionMode.enterprise_sales_cycle
