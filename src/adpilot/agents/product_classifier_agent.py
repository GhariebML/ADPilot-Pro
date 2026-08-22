"""Product Classifier Agent.

Determines the commercial operating mode, business characteristics, execution mode,
and required agent capabilities before planner orchestrates downstream execution.
"""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import List

from langchain_core.prompts import ChatPromptTemplate

from ..core.base_agent import BaseAgent
from ..schemas.campaign_context import (
    CampaignContext,
    ExecutionMode,
    ProductClassificationOutput,
    ProductClassifierInput,
    ProductType,
)

logger = logging.getLogger(__name__)


def _matches_keywords(text: str, keywords: List[str]) -> bool:
    """Check if any keyword or phrase appears as whole words in text."""
    for kw in keywords:
        pattern = r"\b" + re.escape(kw.lower()) + r"\b"
        if re.search(pattern, text):
            return True
    return False


class ProductClassifierAgent(BaseAgent[ProductClassifierInput, ProductClassificationOutput]):
    """Analyzes product/business context to determine operating mode and execution requirements."""

    name = "product_classifier_agent"
    input_model = ProductClassifierInput
    output_model = ProductClassificationOutput

    CONFIDENCE_THRESHOLD: float = 0.70

    system_prompt = (
        "You are AdPilot's Principal Product Classifier & Commercial Operating Mode Architect. "
        "Your objective is to analyze the product and business specifications and accurately classify "
        "the product category, commercial dynamics, sales cycle, recommended execution mode, domain constraints, "
        "and required agent capabilities. Output must strictly match the ProductClassificationOutput JSON schema."
    )

    @classmethod
    def load_system_prompt(cls) -> str:
        prompt_path = Path(__file__).resolve().parent.parent / "prompts" / "product_classifier_system_prompt.md"
        if prompt_path.is_file():
            try:
                return prompt_path.read_text(encoding="utf-8").strip()
            except Exception as e:
                logger.warning(f"Could not read prompt from {prompt_path}: {e}")
        return cls.system_prompt

    def build_prompt(self) -> ChatPromptTemplate:
        system_text = self.load_system_prompt()
        return ChatPromptTemplate.from_messages([
            ("system", system_text),
            (
                "human",
                (
                    "Please classify the following business and product specifications:\n\n"
                    "```json\n{product_input_json}\n```\n\n"
                    "Provide a thorough structured classification with confidence score, "
                    "operating characteristics, recommended execution mode, constraints, "
                    "and required downstream agent capabilities."
                ),
            ),
        ])

    @classmethod
    def rule_based_classify(cls, input_data: ProductClassifierInput) -> ProductClassificationOutput:
        """Deterministic heuristic classifier for offline environments and fast fallback."""
        text = f"{input_data.business_name} {input_data.product_name} {input_data.product_description} {' '.join(input_data.unique_selling_points)}".lower()
        pricing = (input_data.pricing_model or "").lower()

        # Check for ambiguity / sparse input
        if len(input_data.product_description.strip()) < 15 or text.strip() in ("test", "unknown", "product", "n/a"):
            return ProductClassificationOutput(
                product_type=ProductType.other,
                confidence=0.45,
                reason="Insufficient product details and ambiguous description provided.",
                business_characteristics=["Undefined commercial model", "Sparse input specification"],
                recommended_execution_mode=ExecutionMode.brand_launch,
                relevant_constraints=["Requires immediate brief clarification from customer"],
                required_agents=["strategy_agent", "research_agent", "content_agent", "analytics_agent"],
                optional_agents=["design_agent"],
                needs_clarification=True,
                clarification_prompt="Could you clarify the core offering, target market, and pricing structure of your product?",
                operating_mode_summary="Ambiguous product operating mode requiring human clarification.",
            )

        # 1. Education / Training heuristics
        if _matches_keywords(text, ["course", "bootcamp", "academy", "training", "masterclass", "curriculum", "learn", "student", "edtech", "cohort"]):
            return ProductClassificationOutput(
                product_type=ProductType.education,
                confidence=0.92,
                reason="Offering revolves around instructional training, educational courses, or cohort learning.",
                business_characteristics=[
                    "Cohort enrollment deadlines creating natural urgency",
                    "Transformational outcome and student success story marketing",
                    "Lead capture via free webinars, syllabi downloads, and preview lessons",
                ],
                recommended_execution_mode=ExecutionMode.enrollment_funnel,
                relevant_constraints=[
                    "Earnings and career outcome disclaimers",
                    "Accreditation transparency and refund policy clarity",
                ],
                required_agents=["strategy_agent", "research_agent", "content_agent", "analytics_agent"],
                optional_agents=["design_agent", "optimization_agent"],
                needs_clarification=False,
                operating_mode_summary="Education & Cohort Training operating mode.",
            )

        # 2. Real Estate heuristics
        if _matches_keywords(text, ["real estate", "property", "apartment", "condo", "villa", "penthouse", "realty", "residential", "housing", "waterfront"]):
            return ProductClassificationOutput(
                product_type=ProductType.real_estate,
                confidence=0.96,
                reason="Product offers residential or commercial property development and real estate investment.",
                business_characteristics=[
                    "High-ticket transactional value with prolonged decision cycles",
                    "Heavy reliance on visual aesthetics, floor plans, and location prestige",
                    "High-touch sales consultation and private VIP viewing appointments",
                ],
                recommended_execution_mode=ExecutionMode.lead_nurture,
                relevant_constraints=[
                    "Fair Housing Act & local real estate advertising regulations",
                    "Accurate pricing disclosures and architectural rendering disclaimers",
                    "Strict geographic targeting parameters",
                ],
                required_agents=["strategy_agent", "research_agent", "design_agent", "content_agent", "analytics_agent"],
                optional_agents=["publishing_agent"],
                needs_clarification=False,
                operating_mode_summary="High-value Real Estate & Property Development operating mode.",
            )

        # 3. Marketplace heuristics
        if _matches_keywords(text, ["marketplace", "two-sided", "buyers and sellers", "peer-to-peer", "platform network", "brokerage platform"]):
            return ProductClassificationOutput(
                product_type=ProductType.marketplace,
                confidence=0.91,
                reason="Two-sided marketplace connecting supply and demand sides.",
                business_characteristics=[
                    "Network effect dynamics requiring balanced buyer and seller growth",
                    "Transaction fee or take-rate monetization",
                    "Dual-sided messaging (merchant onboarding vs consumer acquisition)",
                ],
                recommended_execution_mode=ExecutionMode.marketplace_liquidity,
                relevant_constraints=[
                    "Transaction security guarantees and user verification rules",
                    "Regional supply density matching",
                ],
                required_agents=["strategy_agent", "research_agent", "content_agent", "analytics_agent"],
                optional_agents=["design_agent", "optimization_agent", "publishing_agent"],
                needs_clarification=False,
                operating_mode_summary="Two-sided Marketplace liquidity operating mode.",
            )

        # 4. Professional Service heuristics
        if _matches_keywords(text, ["consulting", "agency", "advisory", "coaching", "legal", "accounting", "service", "services", "cmo", "fractional", "audit"]):
            return ProductClassificationOutput(
                product_type=ProductType.service,
                confidence=0.90,
                reason="B2B professional services and expert consultative advisory.",
                business_characteristics=[
                    "Expertise and trust-based authority marketing",
                    "Consultative discovery call and tailored scope of work proposals",
                    "Case studies and proprietary framework demonstrations",
                ],
                recommended_execution_mode=ExecutionMode.lead_nurture,
                relevant_constraints=[
                    "Professional liability and disclaimer standards",
                    "Clear scope boundaries and executive persona targeting",
                ],
                required_agents=["strategy_agent", "research_agent", "content_agent", "analytics_agent"],
                optional_agents=["optimization_agent"],
                needs_clarification=False,
                operating_mode_summary="Professional Services & Advisory operating mode.",
            )

        # 5. Physical Product heuristics
        if _matches_keywords(text, ["hoodie", "earbuds", "coffee", "shoe", "bottle", "clothing", "apparel", "hardware", "device", "goods", "merchandise"]):
            return ProductClassificationOutput(
                product_type=ProductType.physical,
                confidence=0.93,
                reason="Tangible consumer or industrial physical product.",
                business_characteristics=[
                    "Direct-to-consumer e-commerce checkout or retail distribution",
                    "Visual-first marketing emphasizing product unboxing, craftsmanship, and lifestyle fit",
                    "Impulse purchase considerations and seasonal discount promotions",
                ],
                recommended_execution_mode=ExecutionMode.direct_response,
                relevant_constraints=[
                    "Shipping and return policy disclosures",
                    "Accurate physical specifications and dimensions",
                    "Product safety and materials compliance",
                ],
                required_agents=["strategy_agent", "research_agent", "content_agent", "design_agent", "analytics_agent"],
                optional_agents=["optimization_agent", "publishing_agent"],
                needs_clarification=False,
                operating_mode_summary="Direct-to-Consumer Physical Product operating mode.",
            )

        # 6. SaaS heuristics
        if _matches_keywords(text, ["saas", "software", "cloud", "api", "platform", "telemetry", "devops", "kubernetes", "crm", "analytics"]) or "subscription" in pricing:
            return ProductClassificationOutput(
                product_type=ProductType.saas,
                confidence=0.94,
                reason="Product features software subscription, cloud/API delivery, and recurring MRR model.",
                business_characteristics=[
                    "Recurring subscription monetization (MRR/ARR)",
                    "Free trial or self-serve demo onboarding funnel",
                    "High customer lifetime value with emphasis on retention and churn prevention",
                ],
                recommended_execution_mode=ExecutionMode.enterprise_sales_cycle if "enterprise" in text else ExecutionMode.lead_nurture,
                relevant_constraints=[
                    "SOC2 / GDPR compliance considerations",
                    "Clear trial terms and transparent tier pricing",
                    "Integration ecosystem highlighting",
                ],
                required_agents=["strategy_agent", "research_agent", "content_agent", "analytics_agent"],
                optional_agents=["design_agent", "optimization_agent", "publishing_agent"],
                needs_clarification=False,
                operating_mode_summary="B2B SaaS / Software platform operating mode.",
            )

        # Fallback for generic
        return ProductClassificationOutput(
            product_type=ProductType.other,
            confidence=0.72,
            reason="General business commercial offering.",
            business_characteristics=["Standard commercial marketing cycle"],
            recommended_execution_mode=ExecutionMode.brand_launch,
            relevant_constraints=["Standard advertising policies"],
            required_agents=["strategy_agent", "research_agent", "content_agent", "analytics_agent"],
            optional_agents=["design_agent"],
            needs_clarification=False,
            operating_mode_summary="Standard commercial marketing operating mode.",
        )

    async def run(self, context: CampaignContext) -> CampaignContext:
        """Classify product/business operating mode and update CampaignContext."""
        logger.info("ProductClassifierAgent | running classification for campaign: %s", context.campaign_id)

        # 1. Build typed input model from canonical context
        biz_name = context.business.name if context.business else "Client"
        prod_name = context.product.name if context.product else biz_name
        prod_desc = context.product.description if context.product else ""
        usps = context.product.unique_selling_points if context.product else []
        pricing_model = context.product.pricing_model if context.product else None
        target_market = context.audience.summary if hasattr(context.audience, "summary") else str(context.audience)
        website_url = context.business.website_url if context.business else None

        agent_input = ProductClassifierInput(
            business_name=biz_name,
            product_name=prod_name,
            product_description=prod_desc,
            target_market=target_market,
            website_url=website_url,
            pricing_model=pricing_model,
            unique_selling_points=usps,
        )

        validated_input = self.validate_input(agent_input)

        # 2. Execute LLM with heuristic fallback
        try:
            prompt = self.build_prompt()
            input_json_str = json.dumps(validated_input.model_dump(mode="json"), indent=2)
            classification_output = await self.call_llm(
                prompt=prompt,
                product_input_json=input_json_str,
                campaign_id=context.campaign_id,
            )
        except Exception as exc:
            logger.warning(
                "ProductClassifierAgent | LLM call failed or provider unavailable (%s). Using rule-based classifier.",
                exc,
            )
            classification_output = self.rule_based_classify(validated_input)

        # 3. Validate confidence threshold
        if classification_output.confidence < self.CONFIDENCE_THRESHOLD:
            logger.warning(
                "ProductClassifierAgent | Low classification confidence (%.2f < %.2f). Marking for Human-in-the-Loop review.",
                classification_output.confidence,
                self.CONFIDENCE_THRESHOLD,
            )
            classification_output.needs_clarification = True
            if not classification_output.clarification_prompt:
                classification_output.clarification_prompt = (
                    f"The product '{prod_name}' has ambiguous commercial characteristics. "
                    "Please confirm whether this is SaaS, a Physical Product, Real Estate, or a Service."
                )
            context.approvals.human_approval_required = True

        # 4. Attach classification to context without mutating original user inputs
        context.classification = classification_output
        context.record_agent_output("product_classifier_agent", classification_output)

        logger.info(
            "ProductClassifierAgent | Completed classification: product_type=%s, mode=%s, confidence=%.2f, needs_clarification=%s",
            classification_output.product_type.value,
            classification_output.recommended_execution_mode.value,
            classification_output.confidence,
            classification_output.needs_clarification,
        )

        return context
