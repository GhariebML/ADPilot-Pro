"""Verification script for Phase 3 — Product Classifier Agent."""

import asyncio
from adpilot.agents.product_classifier_agent import ProductClassifierAgent
from adpilot.core.context_builder import CampaignContextBuilder
from adpilot.schemas.agent_schemas import (
    ExecutionMode,
    ProductType,
)


def main() -> None:
    print("=" * 75)
    print("ADPilot Phase 3 — Product Classifier Agent Verification")
    print("=" * 75)

    agent = ProductClassifierAgent()

    # 1. SaaS Classification Check
    saas_ctx = (
        CampaignContextBuilder.create("camp-saas-verify")
        .with_business(name="TracePulse", industry="Cloud Observability")
        .with_product(
            name="TracePulse Enterprise APM",
            description="Distributed tracing, Kubernetes telemetry, and cloud infrastructure monitoring platform.",
            unique_selling_points=["0.5ms tracing latency", "SOC2 Type II compliant", "OpenTelemetry native"],
            pricing_model="subscription",
        )
        .with_audience(summary="DevOps Leads, Platform Architects, and Site Reliability Engineers")
        .with_budget(total_budget=20000.0)
        .with_timeline(duration_days=30)
        .build()
    )
    res_saas = asyncio.run(agent.run(saas_ctx))
    c_saas = res_saas.classification
    assert c_saas.product_type == ProductType.saas
    assert c_saas.confidence >= 0.70
    assert c_saas.needs_clarification is False
    print(f"[PASS] 1. SaaS Operating Mode: type={c_saas.product_type.value}, mode={c_saas.recommended_execution_mode.value}, confidence={c_saas.confidence:.2f}")

    # 2. Physical Product Classification Check
    phys_ctx = (
        CampaignContextBuilder.create("camp-phys-verify")
        .with_business(name="Nordic Apparel", industry="Fashion")
        .with_product(
            name="Merino Tech Running Hoodie",
            description="All-weather thermal running hoodie made of 100% organic Merino wool.",
            unique_selling_points=["Odor resistant", "Machine washable"],
        )
        .with_audience(summary="Athletes and outdoor adventurers")
        .with_budget(total_budget=7500.0)
        .with_timeline(duration_days=21)
        .build()
    )
    res_phys = asyncio.run(agent.run(phys_ctx))
    c_phys = res_phys.classification
    assert c_phys.product_type == ProductType.physical
    assert c_phys.recommended_execution_mode == ExecutionMode.direct_response
    assert "design_agent" in c_phys.required_agents
    print(f"[PASS] 2. Physical Product Mode: type={c_phys.product_type.value}, mode={c_phys.recommended_execution_mode.value}, required_agents={c_phys.required_agents}")

    # 3. Real Estate Classification Check
    re_ctx = (
        CampaignContextBuilder.create("camp-re-verify")
        .with_business(name="Azure Heights Realty", industry="Luxury Real Estate")
        .with_product(
            name="The Azure Marina Penthouse Collection",
            description="Ultra-luxury residential waterfront residences with private helipad and concierge.",
        )
        .with_audience(summary="High-net-worth real estate investors")
        .with_budget(total_budget=45000.0)
        .with_timeline(duration_days=60)
        .build()
    )
    res_re = asyncio.run(agent.run(re_ctx))
    c_re = res_re.classification
    assert c_re.product_type == ProductType.real_estate
    assert c_re.recommended_execution_mode == ExecutionMode.lead_nurture
    print(f"[PASS] 3. Real Estate Mode: type={c_re.product_type.value}, mode={c_re.recommended_execution_mode.value}, constraints={len(c_re.relevant_constraints)}")

    # 4. Professional Service Classification Check
    srv_ctx = (
        CampaignContextBuilder.create("camp-srv-verify")
        .with_business(name="Vanguard Growth Advisory", industry="Advisory")
        .with_product(
            name="Fractional Chief Revenue Officer Advisory",
            description="Strategic B2B go-to-market advisory, sales architecture, and executive coaching.",
        )
        .with_audience(summary="Series A and B B2B founders")
        .with_budget(total_budget=15000.0)
        .with_timeline(duration_days=45)
        .build()
    )
    res_srv = asyncio.run(agent.run(srv_ctx))
    c_srv = res_srv.classification
    assert c_srv.product_type == ProductType.service
    assert c_srv.recommended_execution_mode == ExecutionMode.lead_nurture
    print(f"[PASS] 4. Service Mode: type={c_srv.product_type.value}, mode={c_srv.recommended_execution_mode.value}, characteristics={len(c_srv.business_characteristics)}")

    # 5. Marketplace Classification Check
    mkt_ctx = (
        CampaignContextBuilder.create("camp-mkt-verify")
        .with_business(name="FreelanceAI", industry="Talent Platform")
        .with_product(
            name="FreelanceAI Marketplace",
            description="Two-sided marketplace connecting specialized AI research engineers with enterprise clients.",
        )
        .with_audience(summary="Enterprise buyers and elite AI researchers")
        .with_budget(total_budget=30000.0)
        .with_timeline(duration_days=30)
        .build()
    )
    res_mkt = asyncio.run(agent.run(mkt_ctx))
    c_mkt = res_mkt.classification
    assert c_mkt.product_type == ProductType.marketplace
    assert c_mkt.recommended_execution_mode == ExecutionMode.marketplace_liquidity
    print(f"[PASS] 5. Marketplace Mode: type={c_mkt.product_type.value}, mode={c_mkt.recommended_execution_mode.value}")

    # 6. Education Classification Check
    edu_ctx = (
        CampaignContextBuilder.create("camp-edu-verify")
        .with_business(name="NextGen Academy", industry="EdTech")
        .with_product(
            name="AI Architect Masterclass Bootcamp",
            description="12-week live cohort bootcamp training senior developers in agentic AI architecture.",
        )
        .with_audience(summary="Staff and Senior Software Engineers")
        .with_budget(total_budget=18000.0)
        .with_timeline(duration_days=30)
        .build()
    )
    res_edu = asyncio.run(agent.run(edu_ctx))
    c_edu = res_edu.classification
    assert c_edu.product_type == ProductType.education
    assert c_edu.recommended_execution_mode == ExecutionMode.enrollment_funnel
    print(f"[PASS] 6. Education Mode: type={c_edu.product_type.value}, mode={c_edu.recommended_execution_mode.value}")

    # 7. Low Confidence Ambiguity & HITL Gate Check
    amb_ctx = (
        CampaignContextBuilder.create("camp-amb-verify")
        .with_business(name="Mystery Co", industry="General")
        .with_product(
            name="Generic Offering",
            description="Items",
        )
        .with_audience(summary="Anyone")
        .with_budget(total_budget=1000.0)
        .with_timeline(duration_days=14)
        .build()
    )
    res_amb = asyncio.run(agent.run(amb_ctx))
    c_amb = res_amb.classification
    assert c_amb.confidence < 0.70
    assert c_amb.needs_clarification is True
    assert res_amb.approvals.human_approval_required is True
    print(f"[PASS] 7. Ambiguity & HITL Gate: confidence={c_amb.confidence:.2f}, needs_clarification={c_amb.needs_clarification}, human_approval_required={res_amb.approvals.human_approval_required}")

    # 8. Context Immutability & Audit Lineage Check
    initial_desc = saas_ctx.product.description
    assert res_saas.product.description == initial_desc
    assert res_saas.metadata.revision == 2
    assert res_saas.metadata.change_log[0]["agent"] == "product_classifier_agent"
    print(f"[PASS] 8. Immutability & Audit Lineage: product description unchanged, revision={res_saas.metadata.revision}, log_entry={res_saas.metadata.change_log[0]['agent']}")

    print("=" * 75)
    print("ALL PHASE 3 PRODUCT CLASSIFIER VERIFICATIONS PASSED SUCCESSFULLY!")
    print("=" * 75)


if __name__ == "__main__":
    main()
