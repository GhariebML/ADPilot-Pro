"""Unified Campaign Context Builder service.

Provides factory methods and a fluent builder pattern to construct, validate,
and normalize strongly typed canonical ``CampaignContext`` instances.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Union
from uuid import uuid4

from ..schemas.agent_schemas import (
    CampaignGoal,
    CampaignInput,
    MarketingChannel,
    ToneOfVoice,
)
from ..schemas.campaign_context import (
    ApprovalRequirements,
    BrandGuidelines,
    BudgetSpec,
    BusinessInfo,
    CampaignConstraints,
    CampaignContext,
    CompetitorInfo,
    ContextMetadata,
    Currency,
    Geography,
    KPITargets,
    ProductSpec,
    ProductType,
    TargetAudience,
    TimelineSpec,
)


class CampaignContextBuilder:
    """Fluent and factory builder for constructing canonical ``CampaignContext`` instances."""

    def __init__(self, campaign_id: Optional[str] = None) -> None:
        self._campaign_id = campaign_id or f"camp-{uuid4().hex[:12]}"
        self._business: Optional[BusinessInfo] = None
        self._product: Optional[ProductSpec] = None
        self._goals: List[CampaignGoal] = []
        self._marketing_objective: Optional[str] = None
        self._audience: Optional[TargetAudience] = None
        self._geography: Geography = Geography()
        self._budget: Optional[BudgetSpec] = None
        self._channels: List[MarketingChannel] = []
        self._timeline: Optional[TimelineSpec] = None
        self._kpis: KPITargets = KPITargets()
        self._constraints: CampaignConstraints = CampaignConstraints()
        self._brand: BrandGuidelines = BrandGuidelines()
        self._competitors: CompetitorInfo = CompetitorInfo()
        self._variables: Dict[str, Any] = {}
        self._approvals: ApprovalRequirements = ApprovalRequirements()
        self._created_by: str = "system"

    @classmethod
    def create(cls, campaign_id: Optional[str] = None) -> CampaignContextBuilder:
        """Initialize a new fluent builder instance."""
        return cls(campaign_id=campaign_id)

    def with_business(
        self,
        name: str,
        industry: str = "Technology",
        website_url: Optional[str] = None,
        description: Optional[str] = None,
        company_size: Optional[str] = None,
        tagline: Optional[str] = None,
    ) -> CampaignContextBuilder:
        self._business = BusinessInfo(
            name=name,
            industry=industry,
            website_url=website_url,
            description=description,
            company_size=company_size,
            tagline=tagline,
        )
        return self

    def with_product(
        self,
        name: str,
        product_type: Union[ProductType, str] = ProductType.other,
        description: str = "",
        unique_selling_points: Optional[List[str]] = None,
        price_tier: Optional[str] = None,
        pricing_model: Optional[str] = None,
        features: Optional[List[str]] = None,
    ) -> CampaignContextBuilder:
        ptype = ProductType(product_type) if isinstance(product_type, str) else product_type
        self._product = ProductSpec(
            name=name,
            product_type=ptype,
            description=description,
            unique_selling_points=unique_selling_points or [],
            price_tier=price_tier,
            pricing_model=pricing_model,
            features=features or [],
        )
        return self

    def with_goals(self, goals: List[Union[CampaignGoal, str]], marketing_objective: Optional[str] = None) -> CampaignContextBuilder:
        parsed_goals = []
        for g in goals:
            if isinstance(g, str):
                val = g.strip().lower().replace(" ", "_").replace("-", "_")
                parsed_goals.append(CampaignGoal(val) if val in CampaignGoal._value2member_map_ else CampaignGoal.brand_awareness)
            else:
                parsed_goals.append(g)
        self._goals = parsed_goals or [CampaignGoal.brand_awareness]
        self._marketing_objective = marketing_objective
        return self

    def with_audience(
        self,
        summary: str,
        demographics: Optional[Dict[str, Any]] = None,
        psychographics: Optional[List[str]] = None,
        pain_points: Optional[List[str]] = None,
        personas: Optional[List[str]] = None,
    ) -> CampaignContextBuilder:
        self._audience = TargetAudience(
            summary=summary,
            demographics=demographics or {},
            psychographics=psychographics or [],
            pain_points=pain_points or [],
            personas=personas or [],
        )
        return self

    def with_geography(
        self,
        target_countries: Optional[List[str]] = None,
        regions_or_cities: Optional[List[str]] = None,
        languages: Optional[List[str]] = None,
    ) -> CampaignContextBuilder:
        self._geography = Geography(
            target_countries=target_countries or ["US"],
            regions_or_cities=regions_or_cities or [],
            languages=languages or ["en"],
        )
        return self

    def with_budget(
        self,
        total_budget: float,
        currency: Union[Currency, str] = Currency.USD,
        daily_budget_cap: Optional[float] = None,
        min_spend_per_channel: Optional[float] = None,
        max_spend_per_channel: Optional[float] = None,
    ) -> CampaignContextBuilder:
        curr = Currency(currency) if isinstance(currency, str) else currency
        self._budget = BudgetSpec(
            total_budget=total_budget,
            currency=curr,
            daily_budget_cap=daily_budget_cap,
            min_spend_per_channel=min_spend_per_channel,
            max_spend_per_channel=max_spend_per_channel,
        )
        return self

    def with_channels(self, channels: List[Union[MarketingChannel, str]]) -> CampaignContextBuilder:
        parsed_channels = []
        for ch in channels:
            if isinstance(ch, str):
                val = ch.strip().lower().replace(" ", "_")
                if val in MarketingChannel._value2member_map_:
                    parsed_channels.append(MarketingChannel(val))
            else:
                parsed_channels.append(ch)
        self._channels = parsed_channels or [MarketingChannel.linkedin, MarketingChannel.instagram, MarketingChannel.email]
        return self

    def with_timeline(
        self,
        duration_days: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        milestones: Optional[List[str]] = None,
    ) -> CampaignContextBuilder:
        self._timeline = TimelineSpec(
            duration_days=duration_days,
            start_date=start_date,
            end_date=end_date,
            milestones=milestones or [],
        )
        return self

    def with_kpis(
        self,
        target_cpa: Optional[float] = None,
        target_roas: Optional[float] = None,
        target_ctr: Optional[float] = None,
        target_conversions: Optional[int] = None,
        primary_kpi: str = "ROAS",
    ) -> CampaignContextBuilder:
        self._kpis = KPITargets(
            target_cpa=target_cpa,
            target_roas=target_roas,
            target_ctr=target_ctr,
            target_conversions=target_conversions,
            primary_kpi=primary_kpi,
        )
        return self

    def with_constraints(
        self,
        max_cpa: Optional[float] = None,
        min_roas: Optional[float] = None,
        prohibited_keywords: Optional[List[str]] = None,
        mandatory_disclaimers: Optional[List[str]] = None,
        brand_safety_level: str = "standard",
    ) -> CampaignContextBuilder:
        self._constraints = CampaignConstraints(
            max_cpa=max_cpa,
            min_roas=min_roas,
            prohibited_keywords=prohibited_keywords or [],
            mandatory_disclaimers=mandatory_disclaimers or [],
            brand_safety_level=brand_safety_level,
        )
        return self

    def with_brand(
        self,
        tone_of_voice: Union[ToneOfVoice, str] = ToneOfVoice.professional,
        brand_colors: Optional[List[str]] = None,
        font_family: Optional[str] = None,
        dos_and_donts: Optional[List[str]] = None,
        logo_url: Optional[str] = None,
    ) -> CampaignContextBuilder:
        tone = ToneOfVoice(tone_of_voice) if isinstance(tone_of_voice, str) else tone_of_voice
        self._brand = BrandGuidelines(
            tone_of_voice=tone,
            brand_colors=brand_colors or [],
            font_family=font_family,
            dos_and_donts=dos_and_donts or [],
            logo_url=logo_url,
        )
        return self

    def with_competitors(self, names: List[str], details: Optional[List[Dict[str, Any]]] = None) -> CampaignContextBuilder:
        self._competitors = CompetitorInfo(names=names, details=details or [])
        return self

    def with_variables(self, variables: Dict[str, Any]) -> CampaignContextBuilder:
        self._variables = variables
        return self

    def with_created_by(self, user_id: str) -> CampaignContextBuilder:
        self._created_by = user_id
        return self

    def build(self) -> CampaignContext:
        """Validate all parameters and construct canonical CampaignContext."""
        if not self._business:
            raise ValueError("Business information is required. Call with_business() before build().")
        if not self._product:
            raise ValueError("Product specifications are required. Call with_product() before build().")
        if not self._audience:
            raise ValueError("Target audience is required. Call with_audience() before build().")
        if not self._budget:
            raise ValueError("Budget specification is required. Call with_budget() before build().")
        if not self._timeline:
            raise ValueError("Timeline specification is required. Call with_timeline() before build().")
        if not self._goals:
            self._goals = [CampaignGoal.brand_awareness]
        if not self._channels:
            self._channels = [MarketingChannel.linkedin, MarketingChannel.instagram, MarketingChannel.email]

        metadata = ContextMetadata(created_by=self._created_by)

        context = CampaignContext(
            campaign_id=self._campaign_id,
            metadata=metadata,
            business=self._business,
            product=self._product,
            goals=self._goals,
            marketing_objective=self._marketing_objective,
            audience=self._audience,
            geography=self._geography,
            budget=self._budget,
            channels=self._channels,
            timeline=self._timeline,
            kpis=self._kpis,
            constraints=self._constraints,
            brand=self._brand,
            competitors=self._competitors,
            variables=self._variables,
            approvals=self._approvals,
        )

        context.compute_fingerprint()
        return context

    # -----------------------------------------------------------------------
    # Factory Methods & Normalizers
    # -----------------------------------------------------------------------

    @staticmethod
    def _duration_to_days(duration: Any) -> int:
        if isinstance(duration, int):
            return max(7, min(365, duration))
        if isinstance(duration, str):
            s = duration.strip().lower()
            mapping = {
                "1-week": 7,
                "1 week": 7,
                "2-weeks": 14,
                "2 weeks": 14,
                "1-month": 30,
                "1 month": 30,
                "3-months": 90,
                "3 months": 90,
                "6-months": 180,
                "1-year": 365,
            }
            if s in mapping:
                return mapping[s]
            if s.isdigit():
                return max(7, min(365, int(s)))
        return 30

    @staticmethod
    def _infer_product_type(text: str) -> ProductType:
        t = text.lower()
        if any(w in t for w in ["saas", "software", "api", "cloud", "b2b platform", "app", "subscription", "kubernetes"]):
            return ProductType.saas
        if any(w in t for w in ["real estate", "property", "apartment", "condo", "villa", "realty", "residential", "penthouse"]):
            return ProductType.real_estate
        if any(w in t for w in ["consulting", "agency", "coaching", "service", "maintenance", "legal", "accounting", "advisory"]):
            return ProductType.service
        if any(w in t for w in ["product", "bottle", "watch", "shoe", "clothing", "hardware", "goods", "device", "coffee", "beans", "food", "beverage", "apparel", "wearable"]):
            return ProductType.physical
        return ProductType.other

    @classmethod
    def from_brief(cls, brief: Union[CampaignInput, Dict[str, Any], Any], campaign_id: Optional[str] = None) -> CampaignContext:
        """Construct canonical CampaignContext from legacy CampaignInput, FrontendCampaignBrief, or dict."""
        cid = campaign_id or getattr(brief, "campaign_id", None) or f"camp-{uuid4().hex[:12]}"
        builder = cls.create(campaign_id=cid)

        # Handle Pydantic CampaignInput
        if isinstance(brief, CampaignInput):
            p_type = cls._infer_product_type(brief.product_description)
            builder.with_business(name=brief.business_name, website_url=brief.website_url, tagline=brief.existing_tagline)
            builder.with_product(name=brief.business_name, product_type=p_type, description=brief.product_description)
            builder.with_goals(brief.goals)
            builder.with_audience(summary=brief.target_market)
            builder.with_budget(total_budget=brief.budget_usd, currency=Currency.USD)
            builder.with_channels(brief.channels)
            builder.with_timeline(duration_days=brief.campaign_duration_days)
            builder.with_brand(tone_of_voice=brief.tone_of_voice, brand_colors=brief.brand_colors)
            builder.with_competitors(names=brief.competitors)
            return builder.build()

        # Handle raw dictionary or FrontendCampaignBrief
        data = brief.model_dump() if hasattr(brief, "model_dump") else (brief if isinstance(brief, dict) else brief.__dict__)

        biz_name = data.get("businessName") or data.get("business_name") or "Enterprise Client"
        prod_name = data.get("productName") or data.get("product_name") or biz_name
        prod_desc = data.get("productDescription") or data.get("product_description") or f"High-performance offerings by {biz_name}"
        prod_type_raw = data.get("productType") or data.get("product_type")
        prod_type = ProductType(prod_type_raw) if prod_type_raw in ProductType._value2member_map_ else cls._infer_product_type(prod_desc)

        target_audience = data.get("targetAudience") or data.get("target_market") or "Modern enterprise decision makers"
        budget_val = float(data.get("budget") or data.get("budget_usd") or 5000.0)
        currency_val = data.get("currency", "USD")
        duration_days = cls._duration_to_days(data.get("duration") or data.get("campaign_duration_days", 30))

        builder.with_business(
            name=biz_name,
            industry=data.get("industry", "Technology"),
            website_url=data.get("website_url") or data.get("websiteUrl"),
            tagline=data.get("tagline") or data.get("existing_tagline"),
        )
        builder.with_product(
            name=prod_name,
            product_type=prod_type,
            description=prod_desc,
            unique_selling_points=data.get("unique_selling_points", []),
            price_tier=data.get("price_tier"),
            pricing_model=data.get("pricing_model"),
            features=data.get("features", []),
        )
        builder.with_goals(data.get("goals", [CampaignGoal.brand_awareness]), marketing_objective=data.get("marketing_objective"))
        builder.with_audience(summary=target_audience, personas=data.get("personas", []))
        builder.with_geography(target_countries=data.get("target_countries", ["US"]), languages=data.get("languages", ["en"]))
        builder.with_budget(total_budget=budget_val, currency=currency_val, daily_budget_cap=data.get("daily_budget_cap"))
        builder.with_channels(data.get("channels", [MarketingChannel.linkedin, MarketingChannel.instagram, MarketingChannel.email]))
        builder.with_timeline(duration_days=duration_days)
        builder.with_brand(
            tone_of_voice=data.get("tone") or data.get("tone_of_voice", ToneOfVoice.professional),
            brand_colors=data.get("brandColors") or data.get("brand_colors", []),
        )
        builder.with_competitors(names=data.get("competitors", []))
        builder.with_variables(data.get("variables", {}))

        return builder.build()

    @classmethod
    def from_json(cls, json_str: str) -> CampaignContext:
        """Load CampaignContext directly from JSON."""
        return CampaignContext.from_json(json_str)
