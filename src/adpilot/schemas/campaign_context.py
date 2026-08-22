"""Canonical CampaignContext and rich domain schemas for the ADPilot multi-agent system.

The ``CampaignContext`` is the immutable, canonical source of truth for an entire campaign.
It encompasses business details, product specifications, budget, audience, geography, timeline,
KPIs, constraints, brand rules, approval requirements, and accumulates all downstream agent outputs.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


# ---------------------------------------------------------------------------
class MarketingChannel(str, Enum):
    facebook = "facebook"
    instagram = "instagram"
    twitter = "twitter"
    linkedin = "linkedin"
    email = "email"
    tiktok = "tiktok"
    youtube = "youtube"
    snapchat = "snapchat"


class CampaignGoal(str, Enum):
    lead_generation = "lead_generation"
    brand_awareness = "brand_awareness"
    sales_conversion = "sales_conversion"
    engagement = "engagement"
    website_traffic = "website_traffic"


class ToneOfVoice(str, Enum):
    friendly = "friendly"
    professional = "professional"
    witty = "witty"
    compassionate = "compassionate"
    authoritative = "authoritative"


class ProductType(str, Enum):
    """Categorization of the product or service being marketed."""

    saas = "saas"
    physical = "physical"
    real_estate = "real_estate"
    service = "service"
    marketplace = "marketplace"
    education = "education"
    other = "other"


class ExecutionMode(str, Enum):
    """Recommended campaign execution mode based on product and commercial dynamics."""

    direct_response = "direct_response"
    lead_nurture = "lead_nurture"
    brand_launch = "brand_launch"
    enterprise_sales_cycle = "enterprise_sales_cycle"
    marketplace_liquidity = "marketplace_liquidity"
    enrollment_funnel = "enrollment_funnel"


class Currency(str, Enum):
    """Supported ISO 4217 currency codes."""

    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    CAD = "CAD"
    AUD = "AUD"
    JPY = "JPY"
    INR = "INR"
    SGD = "SGD"
    CHF = "CHF"


# ---------------------------------------------------------------------------
# Core Domain Sub-Models
# ---------------------------------------------------------------------------


class BusinessInfo(BaseModel):
    """Information regarding the business entity running the campaign."""

    name: str = Field(..., min_length=2, description="Legal or commercial business name")
    industry: str = Field(default="Technology", description="Industry vertical (e.g. Fintech, E-commerce)")
    website_url: Optional[str] = Field(default=None, description="Primary business website URL")
    description: Optional[str] = Field(default=None, description="Overview of the business and value proposition")
    company_size: Optional[str] = Field(default=None, description="Company size category (e.g. Startup, Enterprise)")
    tagline: Optional[str] = Field(default=None, description="Current brand tagline or slogan")


class ProductSpec(BaseModel):
    """Detailed specifications of the product or service."""

    name: str = Field(..., min_length=1, description="Product or offering name")
    product_type: ProductType = Field(default=ProductType.other, description="Product category")
    description: str = Field(..., min_length=5, description="Comprehensive description of product features and benefits")
    unique_selling_points: List[str] = Field(default_factory=list, description="Key differentiators against competitors")
    price_tier: Optional[str] = Field(default=None, description="Pricing tier (e.g. Budget, Mid-market, Luxury, Enterprise)")
    pricing_model: Optional[str] = Field(default=None, description="Model (e.g. subscription, one-time, commission)")
    features: List[str] = Field(default_factory=list, description="List of notable product features")


class TargetAudience(BaseModel):
    """Target market and ideal customer profile."""

    summary: str = Field(..., min_length=3, description="High-level audience summary description")
    demographics: Dict[str, Any] = Field(default_factory=dict, description="Age, gender, income, education data")
    psychographics: List[str] = Field(default_factory=list, description="Interests, values, attitudes, lifestyle")
    pain_points: List[str] = Field(default_factory=list, description="Core challenges faced by the audience")
    personas: List[str] = Field(default_factory=list, description="Key customer persona names or archetypes")


class Geography(BaseModel):
    """Geographic and linguistic targeting configuration."""

    target_countries: List[str] = Field(default_factory=lambda: ["US"], min_length=1, description="ISO country codes or names")
    regions_or_cities: List[str] = Field(default_factory=list, description="Specific target states, provinces, or metropolitan areas")
    languages: List[str] = Field(default_factory=lambda: ["en"], min_length=1, description="Primary campaign languages")


class BudgetSpec(BaseModel):
    """Financial parameters and spend allocations."""

    total_budget: float = Field(..., gt=0, description="Total campaign budget")
    currency: Currency = Field(default=Currency.USD, description="Currency denomination")
    daily_budget_cap: Optional[float] = Field(default=None, gt=0, description="Optional maximum daily spend")
    min_spend_per_channel: Optional[float] = Field(default=None, ge=0, description="Minimum spend threshold per channel")
    max_spend_per_channel: Optional[float] = Field(default=None, gt=0, description="Maximum spend ceiling per channel")

    @model_validator(mode="after")
    def validate_budget_rules(self) -> BudgetSpec:
        if self.daily_budget_cap and self.daily_budget_cap > self.total_budget:
            raise ValueError(f"daily_budget_cap ({self.daily_budget_cap}) cannot exceed total_budget ({self.total_budget})")
        if (
            self.min_spend_per_channel
            and self.max_spend_per_channel
            and self.min_spend_per_channel > self.max_spend_per_channel
        ):
            raise ValueError(
                f"min_spend_per_channel ({self.min_spend_per_channel}) cannot exceed max_spend_per_channel ({self.max_spend_per_channel})"
            )
        return self


class TimelineSpec(BaseModel):
    """Campaign schedule, duration, and key milestones."""

    duration_days: int = Field(..., ge=7, le=365, description="Campaign duration in days (7 to 365)")
    start_date: Optional[str] = Field(default=None, description="ISO 8601 campaign launch date")
    end_date: Optional[str] = Field(default=None, description="ISO 8601 campaign completion date")
    milestones: List[str] = Field(default_factory=list, description="Target timeline review dates or milestone events")


class KPITargets(BaseModel):
    """Key performance indicator targets and objectives."""

    target_cpa: Optional[float] = Field(default=None, gt=0, description="Target cost per acquisition")
    target_roas: Optional[float] = Field(default=None, gt=0, description="Target return on ad spend (e.g. 3.5 for 350%)")
    target_ctr: Optional[float] = Field(default=None, ge=0, le=100, description="Target click-through rate percentage")
    target_conversions: Optional[int] = Field(default=None, gt=0, description="Target total conversion volume")
    primary_kpi: str = Field(default="ROAS", description="Primary optimization metric (e.g. ROAS, CPA, CTR, Conversions)")


class CampaignConstraints(BaseModel):
    """Operational constraints, brand safety, and regulatory compliance rules."""

    max_cpa: Optional[float] = Field(default=None, gt=0, description="Hard maximum CPA ceiling")
    min_roas: Optional[float] = Field(default=None, gt=0, description="Hard minimum ROAS floor")
    prohibited_keywords: List[str] = Field(default_factory=list, description="Keywords forbidden in ad copy")
    mandatory_disclaimers: List[str] = Field(default_factory=list, description="Required legal or regulatory disclaimers")
    brand_safety_level: str = Field(default="standard", description="Safety tier (e.g. standard, strict)")
    regulatory_requirements: List[str] = Field(default_factory=list, description="Compliance rules (e.g. GDPR, FTC, FINRA)")


class BrandGuidelines(BaseModel):
    """Visual and tonal identity guidelines."""

    tone_of_voice: ToneOfVoice = Field(default=ToneOfVoice.professional, description="Brand voice and personality")
    brand_colors: List[str] = Field(default_factory=list, description="Hex color palette (e.g. ['#1E3A8A', '#3B82F6'])")
    font_family: Optional[str] = Field(default=None, description="Primary brand typography family")
    dos_and_donts: List[str] = Field(default_factory=list, description="Brand messaging guidelines")
    logo_url: Optional[str] = Field(default=None, description="Vector or high-res brand logo asset URL")

    @field_validator("brand_colors", mode="before")
    @classmethod
    def validate_hex_colors(cls, v: Optional[List[str]]) -> List[str]:
        if not v:
            return []
        cleaned = []
        for color in v:
            if not isinstance(color, str):
                continue
            c = color.strip()
            if not c.startswith("#") or len(c) not in (4, 7):
                raise ValueError(f"Invalid hex color code: '{color}'. Expected format #RGB or #RRGGBB.")
            cleaned.append(c)
        return cleaned


class CompetitorInfo(BaseModel):
    """Identified competitors and benchmark targets."""

    names: List[str] = Field(default_factory=list, description="List of competitor brand names")
    details: List[Dict[str, Any]] = Field(default_factory=list, description="Optional detailed competitor profiles")


class ApprovalRequirements(BaseModel):
    """Human-in-the-Loop governance and approval rules."""

    human_approval_required: bool = Field(default=True, description="Whether human review is required before publishing")
    min_health_score: float = Field(default=70.0, ge=0, le=100, description="Minimum analytics quality gate score")
    required_roles: List[str] = Field(default_factory=lambda: ["marketer", "admin"], description="Roles authorized to approve")


class ContextMetadata(BaseModel):
    """Auditability, versioning, and lineage tracking metadata."""

    schema_version: str = Field(default="2.0.0", description="Schema specification version")
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    created_by: str = Field(default="system", description="User ID or service that initialized this context")
    revision: int = Field(default=1, ge=1, description="Monotonically increasing context revision counter")
    fingerprint: Optional[str] = Field(default=None, description="Deterministic SHA256 checksum of campaign brief")
    change_log: List[Dict[str, Any]] = Field(default_factory=list, description="Chronological record of context mutations")


class ProductClassifierInput(BaseModel):
    """Input payload for the Product Classifier Agent."""

    business_name: str
    product_name: str
    product_description: str
    target_market: Optional[str] = None
    website_url: Optional[str] = None
    pricing_model: Optional[str] = None
    unique_selling_points: List[str] = Field(default_factory=list)


class ProductClassificationOutput(BaseModel):
    """Structured output generated by the Product Classifier Agent."""

    product_type: ProductType = Field(..., description="Determined primary operating mode/category")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Classification confidence score (0.0 to 1.0)")
    reason: str = Field(..., min_length=10, description="Detailed rationale explaining the classification decision")
    business_characteristics: List[str] = Field(
        default_factory=list, description="Key commercial, sales cycle, and customer dynamics"
    )
    recommended_execution_mode: ExecutionMode = Field(
        default=ExecutionMode.direct_response, description="Recommended marketing operating mode"
    )
    relevant_constraints: List[str] = Field(
        default_factory=list, description="Domain-specific constraints (compliance, pricing clarity, disclaimers)"
    )
    required_agents: List[str] = Field(
        default_factory=lambda: ["strategy_agent", "research_agent", "content_agent", "analytics_agent"],
        description="Agents mandatory for this product type",
    )
    optional_agents: List[str] = Field(
        default_factory=lambda: ["design_agent", "optimization_agent", "publishing_agent"],
        description="Agents optional or secondary for this product type",
    )
    needs_clarification: bool = Field(
        default=False, description="Flagged True if confidence is below threshold or ambiguity is detected"
    )
    clarification_prompt: Optional[str] = Field(
        default=None, description="Actionable question to ask human reviewer if classification is ambiguous"
    )
    operating_mode_summary: str = Field(
        default="", description="Executive summary of the product operating mode for the Planner"
    )


# ---------------------------------------------------------------------------
# Canonical CampaignContext
# ---------------------------------------------------------------------------


class CampaignContext(BaseModel):
    """Canonical Campaign Context – The single source of truth for the ADPilot pipeline.

    Maintains immutable campaign identity, domain specifications, governance rules, and accumulates
    downstream agent execution artifacts.
    """

    # 1. Identity & Audit Lineage
    campaign_id: str = Field(..., min_length=4, description="Unique, immutable campaign identifier")
    metadata: ContextMetadata = Field(default_factory=ContextMetadata)

    # 2. Canonical Business Truth
    business: BusinessInfo
    product: ProductSpec
    goals: List[CampaignGoal] = Field(..., min_length=1, description="Primary campaign marketing goals")
    marketing_objective: Optional[str] = Field(default=None, description="Detailed strategic marketing objective")
    audience: Optional[Any] = None
    geography: Geography = Field(default_factory=Geography)
    budget: BudgetSpec
    channels: List[MarketingChannel] = Field(..., min_length=1, description="Target marketing distribution channels")
    timeline: TimelineSpec
    kpis: KPITargets = Field(default_factory=KPITargets)
    constraints: CampaignConstraints = Field(default_factory=CampaignConstraints)
    brand: BrandGuidelines = Field(default_factory=BrandGuidelines)
    competitors: Optional[Any] = None
    variables: Dict[str, Any] = Field(default_factory=dict, description="Custom parameters and template variables")
    approvals: ApprovalRequirements = Field(default_factory=ApprovalRequirements)

    @model_validator(mode="before")
    @classmethod
    def _normalize_legacy_inputs(cls, data: Any) -> Any:
        if isinstance(data, dict):
            # Check if brief is provided (legacy input style)
            if "brief" in data and data["brief"] is not None:
                brief = data.pop("brief")
                brief_dict = (
                    brief.model_dump()
                    if hasattr(brief, "model_dump")
                    else (brief if isinstance(brief, dict) else brief.__dict__)
                )

                if "business" not in data:
                    data["business"] = {
                        "name": brief_dict.get("business_name") or brief_dict.get("businessName") or "Client Business",
                        "industry": brief_dict.get("industry", "Technology"),
                        "website_url": brief_dict.get("website_url") or brief_dict.get("websiteUrl"),
                        "tagline": brief_dict.get("existing_tagline") or brief_dict.get("tagline"),
                    }
                if "product" not in data:
                    desc = (
                        brief_dict.get("product_description")
                        or brief_dict.get("productDescription")
                        or "Enterprise offering"
                    )
                    data["product"] = {
                        "name": (
                            brief_dict.get("product_name")
                            or brief_dict.get("productName")
                            or data["business"]["name"]
                        ),
                        "description": desc,
                        "product_type": brief_dict.get("product_type") or brief_dict.get("productType") or "other",
                    }
                if "goals" not in data:
                    data["goals"] = brief_dict.get("goals") or ["brand_awareness"]
                if "audience" not in data or isinstance(data.get("audience"), dict):
                    aud = data.get("audience") or {}
                    data["audience"] = TargetAudience(
                        summary=aud.get("summary")
                        or brief_dict.get("target_market")
                        or brief_dict.get("targetAudience")
                        or "Target Market",
                        demographics=aud.get("demographics", {}),
                        psychographics=aud.get("psychographics", []),
                        pain_points=aud.get("pain_points", []),
                        personas=aud.get("personas", []),
                    )
                if "budget" not in data or isinstance(data.get("budget"), dict):
                    bgt = data.get("budget") or {}
                    data["budget"] = BudgetSpec(
                        total_budget=float(bgt.get("total_budget") or brief_dict.get("budget_usd") or brief_dict.get("budget") or 5000.0),
                        currency=bgt.get("currency") or brief_dict.get("currency") or Currency.USD,
                        daily_budget_cap=bgt.get("daily_budget_cap") or brief_dict.get("daily_budget_cap"),
                    )
                if "channels" not in data:
                    data["channels"] = brief_dict.get("channels") or ["linkedin", "instagram", "email"]
                if "timeline" not in data or isinstance(data.get("timeline"), dict):
                    tl = data.get("timeline") or {}
                    duration = tl.get("duration_days") or brief_dict.get("campaign_duration_days") or brief_dict.get("duration") or 30
                    if isinstance(duration, str):
                        duration = 30
                    data["timeline"] = TimelineSpec(
                        duration_days=max(7, min(365, int(duration))),
                    )
                if "brand" not in data or isinstance(data.get("brand"), dict):
                    br = data.get("brand") or {}
                    data["brand"] = BrandGuidelines(
                        tone_of_voice=br.get("tone_of_voice") or brief_dict.get("tone_of_voice") or brief_dict.get("tone") or "professional",
                        brand_colors=br.get("brand_colors") or brief_dict.get("brand_colors") or brief_dict.get("brandColors") or [],
                    )
                if "competitors" not in data or isinstance(data.get("competitors"), (dict, list)):
                    cmp = data.get("competitors") or []
                    comp_names = cmp.get("names", []) if isinstance(cmp, dict) else (cmp if isinstance(cmp, list) else brief_dict.get("competitors", []))
                    data["competitors"] = CompetitorInfo(
                        names=comp_names,
                    )
        return data

    # 3. Downstream Agent Execution Accumulator
    classification: Optional[ProductClassificationOutput] = None
    execution_plan: Optional[Any] = None
    strategy: Optional[Any] = None
    research: Optional[Any] = None
    audience_research: Optional[Any] = None
    competitor_research: Optional[Any] = None
    content: Optional[Any] = None
    creative: Optional[Any] = None
    design: Optional[Any] = None
    cv_agent: Optional[Any] = None
    cv: Optional[Any] = None
    analytics: Optional[Any] = None
    optimization: Optional[Any] = None
    correction_agent: Optional[Any] = None
    correction: Optional[Any] = None
    publishing: Optional[Any] = None
    monitoring_agent: Optional[Any] = None
    monitoring: Optional[Any] = None
    campaign_manager: Optional[Any] = None
    agent_outputs: Dict[str, Any] = Field(default_factory=dict, description="Registry of all recorded agent outputs")
    creative_revision_notes: List[str] = Field(default_factory=list, description="Directives from CV or human review for design revision")

    # 4. Backward Compatibility Adapter
    @property
    def brief(self):
        """Adapter property returning a backward-compatible ``CampaignInput`` model."""
        from .agent_schemas import CampaignInput

        # Safe extraction of target_market
        if hasattr(self.audience, "summary"):
            target_market = self.audience.summary
        elif isinstance(self.audience, dict):
            target_market = self.audience.get("summary", "Target Market")
        elif self.audience is not None and hasattr(self.audience, "primary_persona"):
            target_market = getattr(self.audience.primary_persona, "name", "Target Market")
        else:
            target_market = str(self.audience) if self.audience else "Target Market"

        # Safe extraction of competitors
        if hasattr(self.competitors, "names"):
            competitor_names = self.competitors.names
        elif isinstance(self.competitors, dict):
            competitor_names = self.competitors.get("names", [])
        elif hasattr(self.competitors, "competitors"):
            competitor_names = [c.name for c in self.competitors.competitors if hasattr(c, "name")]
        elif isinstance(self.competitors, list):
            competitor_names = [c if isinstance(c, str) else getattr(c, "name", str(c)) for c in self.competitors]
        else:
            competitor_names = []

        return CampaignInput(
            business_name=self.business.name if self.business else "Client Business",
            product_description=f"{self.product.name}: {self.product.description}" if self.product else "Offering",
            target_market=target_market,
            budget_usd=self.budget.total_budget if self.budget else 5000.0,
            goals=self.goals,
            channels=self.channels,
            tone_of_voice=self.brand.tone_of_voice if self.brand else "professional",
            brand_colors=self.brand.brand_colors if self.brand else [],
            competitors=competitor_names,
            website_url=self.business.website_url if self.business else None,
            existing_tagline=self.business.tagline if self.business else None,
            campaign_duration_days=self.timeline.duration_days if self.timeline else 30,
        )

    # 5. Core Methods
    def record_agent_output(self, agent_name: str, output: Any) -> None:
        """Accumulate an agent's output and update audit revision."""
        self.agent_outputs[agent_name] = output
        if agent_name in ("product_classifier_agent", "product_classifier", "classifier"):
            self.classification = output
        elif agent_name in ("planner", "planner_agent", "campaign_planner", "execution_plan"):
            self.execution_plan = output
        elif agent_name in ("cv_agent", "cv"):
            self.cv = output
            self.cv_agent = output
        elif hasattr(self, agent_name):
            setattr(self, agent_name, output)
        elif agent_name == "strategy_agent":
            self.strategy = output
        elif agent_name == "research_agent":
            self.research = output
        elif agent_name == "content_agent":
            self.content = output
        elif agent_name == "design_agent":
            self.design = output
        elif agent_name == "analytics_agent":
            self.analytics = output
        elif agent_name == "campaign_manager_agent":
            self.campaign_manager = output

        # Update metadata audit trail
        self.metadata.revision += 1
        self.metadata.updated_at = datetime.now(timezone.utc).isoformat()
        self.metadata.change_log.append({
            "revision": self.metadata.revision,
            "agent": agent_name,
            "timestamp": self.metadata.updated_at,
            "action": f"Recorded output for {agent_name}",
        })

    def compute_fingerprint(self) -> str:
        """Compute deterministic SHA256 checksum of canonical business inputs."""
        canonical_dict = {
            "business": self.business.model_dump(),
            "product": self.product.model_dump(),
            "goals": [g.value for g in self.goals],
            "channels": [c.value for c in self.channels],
            "budget": self.budget.model_dump(),
            "timeline": self.timeline.model_dump(),
        }
        raw_bytes = json.dumps(canonical_dict, sort_keys=True).encode("utf-8")
        digest = hashlib.sha256(raw_bytes).hexdigest()
        self.metadata.fingerprint = digest
        return digest

    def to_dict(self) -> Dict[str, Any]:
        """Serialize context to a Python dictionary."""
        return self.model_dump(mode="json")

    def to_json(self, indent: Optional[int] = None) -> str:
        """Serialize context to JSON string."""
        return self.model_dump_json(indent=indent)

    @classmethod
    def from_json(cls, json_str: str) -> CampaignContext:
        """Deserialize JSON string into a CampaignContext instance."""
        return cls.model_validate_json(json_str)
