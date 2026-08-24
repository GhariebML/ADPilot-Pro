"""Pydantic v2 schema definitions for the AdPilot multi‑agent system.

Only the data contracts are defined – no business logic.  These schemas are the
single source of truth for all agents and will be used for validation and
auto‑generation of JSON examples.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional
import uuid

from pydantic import BaseModel, Field, model_validator, field_validator

from .campaign_context import (
    ApprovalRequirements,
    BrandGuidelines,
    BudgetSpec,
    BusinessInfo,
    CampaignConstraints,
    CampaignContext,
    CampaignGoal,
    CompetitorInfo,
    ContextMetadata,
    Currency,
    ExecutionMode,
    Geography,
    MarketingChannel,
    ProductClassificationOutput,
    ProductClassifierInput,
    ProductSpec,
    ProductType,
    TargetAudience,
    TimelineSpec,
    ToneOfVoice,
)
from .execution_plan import (
    ExecutionPlan,
    PlannedStep,
    WorkflowState,
)

__all__ = [
    "ApprovalRequirements",
    "BrandGuidelines",
    "BudgetSpec",
    "BusinessInfo",
    "CampaignConstraints",
    "CampaignContext",
    "CampaignGoal",
    "CompetitorInfo",
    "ContextMetadata",
    "Currency",
    "DataProvenance",
    "ExecutionMode",
    "ExecutionPlan",
    "Geography",
    "MarketingChannel",
    "PlannedStep",
    "ProductClassificationOutput",
    "ProductClassifierInput",
    "ProductSpec",
    "ProductType",
    "TargetAudience",
    "TimelineSpec",
    "ToneOfVoice",
    "WorkflowState",
]

# ---------------------------------------------------------------------------
# Enums – all inherit from ``str`` for JSON friendliness.
# ---------------------------------------------------------------------------


class FunnelStage(str, Enum):
    awareness = "awareness"
    consideration = "consideration"
    conversion = "conversion"
    loyalty = "loyalty"


class ContentType(str, Enum):
    ad_copy = "ad_copy"
    email = "email"
    social_post = "social_post"
    blog = "blog"
    landing_page = "landing_page"


class AdFormat(str, Enum):
    image = "image"
    video = "video"
    carousel = "carousel"
    story = "story"
    text = "text"


class ImageStyle(str, Enum):
    photorealistic = "photorealistic"
    illustration = "illustration"
    flat = "flat"
    retro = "retro"
    minimal = "minimal"


class MetricType(str, Enum):
    ctr = "ctr"
    cpc = "cpc"
    cpa = "cpa"
    impressions = "impressions"
    conversions = "conversions"
    open_rate = "open_rate"
    engagement_rate = "engagement_rate"
    conversion_rate = "conversion_rate"
    roas = "roas"
    roi = "roi"


class AgentRunStatus(str, Enum):
    pending = "pending"
    running = "running"
    success = "success"
    failed = "failed"
    skipped = "skipped"


class SuggestionPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


# ---------------------------------------------------------------------------
# Primitive type helpers (aliases) – real validation done in model validators.
# ---------------------------------------------------------------------------

PercentFloat = float  # 0‑100 inclusive percentage
PositiveFloat = float  # >0
ScoreInt = int  # arbitrary score integer

# ---------------------------------------------------------------------------
# Core input model
# ---------------------------------------------------------------------------


class CampaignInput(BaseModel):
    business_name: str
    product_description: str
    target_market: str
    budget_usd: PositiveFloat = Field(..., gt=0, description="Budget in USD, must be > 0")
    goals: List[CampaignGoal]
    channels: List[MarketingChannel]
    tone_of_voice: ToneOfVoice
    brand_colors: Optional[List[str]] = None
    competitors: List[str]
    website_url: Optional[str] = None
    existing_tagline: Optional[str] = None
    campaign_duration_days: int = Field(..., ge=7, le=365)

    @field_validator("brand_colors", mode="before")
    @classmethod
    def validate_brand_colors(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        if v is None:
            return v
        for color in v:
            if not isinstance(color, str) or not color.startswith("#") or len(color) not in (4, 7):
                raise ValueError(f"Invalid hex color: {color}")
        return v


# ---------------------------------------------------------------------------
# Data Provenance & Evidence Schemas
# ---------------------------------------------------------------------------


class DataProvenance(BaseModel):
    """Explicitly partitions and classifies data sources for full auditability."""

    observed_data: List[str] = Field(
        default_factory=list,
        description="Factual input directly provided in the campaign brief / business profile",
    )
    model_prediction: List[str] = Field(
        default_factory=list,
        description="Quantitative predictions or classifications from specialized ML models",
    )
    llm_inference: List[str] = Field(
        default_factory=list,
        description="Synthesized strategic deductions generated through LLM reasoning",
    )
    recommendation: List[str] = Field(
        default_factory=list,
        description="Actionable guidance and execution recommendations",
    )


# ---------------------------------------------------------------------------
# Strategy schemas
# ---------------------------------------------------------------------------


class MessagingPillar(BaseModel):
    title: str
    description: str


class ChannelPriority(BaseModel):
    channel: MarketingChannel
    priority: int = Field(..., ge=1, le=5)


class FunnelStageStrategy(BaseModel):
    stage: FunnelStage
    budget_allocation_percent: PercentFloat = Field(..., ge=0, le=100)
    key_messages: List[str]


class StrategyAgentInput(BaseModel):
    campaign: CampaignInput


class StrategyAgentOutput(BaseModel):
    positioning_statement: str
    usp: str
    elevator_pitch: str
    tone_of_voice: ToneOfVoice
    brand_voice_guidelines: str
    primary_channels: List[MarketingChannel]
    messaging_pillars: List[MessagingPillar]
    funnel_strategy: List[FunnelStageStrategy]
    target_persona_summary: str
    key_differentiators: List[str]
    risks_and_considerations: List[str]
    confidence: float = Field(default=0.85, ge=0.0, le=1.0, description="Overall confidence score (0.0 - 1.0)")
    evidence: List[str] = Field(default_factory=list, description="Evidentiary support and rationale")
    corrective_actions: List[str] = Field(default_factory=list, description="Fallback or mitigation actions")
    provenance: Optional[DataProvenance] = Field(default=None, description="Detailed data lineage categorization")

    @model_validator(mode="after")
    def check_budget_sum(self) -> "StrategyAgentOutput":
        total = sum(f.budget_allocation_percent for f in self.funnel_strategy)
        if round(total) != 100:
            raise ValueError("funnel_strategy budget allocations must sum to exactly 100%")
        return self


# ---------------------------------------------------------------------------
# Research schemas
# ---------------------------------------------------------------------------


class AudiencePersona(BaseModel):
    name: str
    description: str
    demographics: str
    interests: List[str]


class CompetitorAnalysis(BaseModel):
    name: str
    strengths: List[str]
    weaknesses: List[str]
    positioning: str


class TrendingTopic(BaseModel):
    topic: str
    relevance_score: PercentFloat = Field(..., ge=0, le=100)


class ChannelBenchmark(BaseModel):
    channel: MarketingChannel
    cpc: PositiveFloat
    ctr: PercentFloat = Field(..., ge=0, le=100)


class ResearchAgentInput(BaseModel):
    campaign: CampaignInput


class ResearchAgentOutput(BaseModel):
    audience_personas: List[AudiencePersona]
    competitor_analyses: List[CompetitorAnalysis]
    trending_topics: List[TrendingTopic]
    channel_benchmarks: List[ChannelBenchmark]
    audience_language: str
    key_insights: List[str]
    market_size_estimate: PositiveFloat
    search_queries_used: List[str]
    recommended_keywords: List[str] = Field(default_factory=list, description="Target search and thematic keywords")
    confidence: float = Field(default=0.80, ge=0.0, le=1.0, description="Overall confidence score (0.0 - 1.0)")
    evidence: List[str] = Field(default_factory=list, description="Market evidence and retrieved citations")
    corrective_actions: List[str] = Field(default_factory=list, description="Recommended remediation actions")
    provenance: Optional[DataProvenance] = Field(default=None, description="Detailed data lineage categorization")


# ---------------------------------------------------------------------------
# Content schemas
# ---------------------------------------------------------------------------


class AdCopy(BaseModel):
    headline: str
    body: str
    call_to_action: str
    funnel_stage: FunnelStage
    format: AdFormat
    hashtags: List[str]


class EmailInSequence(BaseModel):
    subject: str
    body: str
    day_offset: int


class EmailSequence(BaseModel):
    sequence_name: str
    emails: List[EmailInSequence]


class SocialPost(BaseModel):
    platform: MarketingChannel
    content: str
    hashtags: List[str]
    visual_url: Optional[str] = None


class BlogOutline(BaseModel):
    title: str
    sections: List[str]


class CTAVariant(BaseModel):
    text: str
    style: Optional[str] = None


class SEOMetadata(BaseModel):
    """SEO and metadata optimization package."""

    title: str = Field(..., description="SEO page title (recommended <= 60 chars)")
    meta_description: str = Field(..., description="SEO meta description (recommended <= 160 chars)")
    target_keywords: List[str] = Field(default_factory=list, description="Target search query keywords")
    canonical_url_slug: Optional[str] = Field(default=None, description="Suggested canonical URL slug")
    robots_directive: str = Field(default="index, follow", description="Robots meta tag instruction")


class ContentVariation(BaseModel):
    """Multi-channel, funnel-stage, and persona tailored content variation."""

    channel: MarketingChannel = Field(..., description="Target distribution channel")
    funnel_stage: FunnelStage = Field(..., description="Awareness, consideration, or conversion")
    target_persona: Optional[str] = Field(default=None, description="Target audience persona name")
    headline: str = Field(..., description="Tailored headline for this variation")
    body: str = Field(..., description="Tailored body copy for this variation")
    cta: str = Field(..., description="Call to action text")
    format: AdFormat = Field(default=AdFormat.text, description="Creative content format")


class ContentEvaluationMetric(BaseModel):
    """Individual quality or guardrail check result."""

    name: str = Field(..., description="Metric name (e.g. content_quality, relevance, keyword_coverage)")
    score: float = Field(..., ge=0.0, le=100.0, description="Evaluated score (0.0 - 100.0)")
    passed: bool = Field(..., description="Whether metric met acceptable threshold")
    details: str = Field(default="", description="Detailed evaluation findings or rationale")


class ContentEvaluationReport(BaseModel):
    """Comprehensive content evaluation report covering quality, relevance, keywords, brand, and claims."""

    content_quality_score: float = Field(..., ge=0.0, le=100.0, description="Overall copy quality score (0-100)")
    relevance_score: float = Field(..., ge=0.0, le=100.0, description="Strategic objective and audience relevance score (0-100)")
    keyword_coverage_score: float = Field(..., ge=0.0, le=100.0, description="Percentage of target keywords covered (0-100)")
    brand_compliance_score: float = Field(..., ge=0.0, le=100.0, description="Brand voice and rules compliance score (0-100)")
    hallucination_risk_score: float = Field(..., ge=0.0, le=100.0, description="Unsupported claim risk score (0=none, 100=extreme)")
    ml_quality_prediction: Optional[float] = Field(default=None, description="ML model regression quality prediction")
    covered_keywords: List[str] = Field(default_factory=list, description="Keywords confirmed present in copy")
    missing_keywords: List[str] = Field(default_factory=list, description="Target keywords not detected in copy")
    detected_unsupported_claims: List[str] = Field(default_factory=list, description="Flagged unsupported or hyperbolic claims")
    passed_quality_gate: bool = Field(default=True, description="Whether content passed all guardrail checks")
    metrics: List[ContentEvaluationMetric] = Field(default_factory=list, description="Detailed metrics breakdown")


class ContentAgentInput(BaseModel):
    strategy: Optional[StrategyAgentOutput] = None
    research: Optional[ResearchAgentOutput] = None
    competitors: Optional[Any] = None
    brand_guidelines: Optional[str] = None
    keywords: Optional[List[str]] = None
    campaign: Optional[CampaignInput] = None


class GoogleAd(BaseModel):
    headline_1: str
    headline_2: str
    headline_3: str
    description_1: str
    description_2: str
    path_1: str
    path_2: str
    call_to_action: str


class LandingPageCopy(BaseModel):
    hero_headline: str
    hero_subheadline: str
    features: List[str]
    benefit_statement: str
    call_to_action: str
    footer_text: str


class ContentAgentOutput(BaseModel):
    # Core Package Fields
    headlines: List[str] = Field(default_factory=list, description="High-converting headline variants")
    primary_copy: List[str] = Field(default_factory=list, description="Primary body copy narrative blocks")
    descriptions: List[str] = Field(default_factory=list, description="Short and medium promotional descriptions")
    ctas: List[str] = Field(default_factory=list, description="Call to action variants")
    seo_metadata: Optional[SEOMetadata] = Field(default=None, description="SEO and metadata optimization package")
    keywords: List[str] = Field(default_factory=list, description="Target and covered keywords")
    content_variations: List[ContentVariation] = Field(default_factory=list, description="Channel, funnel, and persona variations")

    # Backwards-compatible legacy fields
    ads: List[AdCopy] = Field(default_factory=list)
    email_sequences: List[EmailSequence] = Field(default_factory=list)
    social_posts: List[SocialPost] = Field(default_factory=list)
    blog_outlines: List[BlogOutline] = Field(default_factory=list)
    cta_variants: List[CTAVariant] = Field(default_factory=list)
    content_calendar_note: str = Field(..., description="Editorial calendar distribution note")
    google_ads: Optional[List[GoogleAd]] = None
    landing_page_copy: Optional[LandingPageCopy] = None

    # Quality, Evaluation & Provenance
    evaluation: Optional[ContentEvaluationReport] = Field(default=None, description="Automated evaluation report")
    confidence: float = Field(default=0.85, ge=0.0, le=1.0, description="Overall confidence score (0.0 - 1.0)")
    evidence: List[str] = Field(default_factory=list, description="Strategic evidence and data grounding rationale")
    corrective_actions: List[str] = Field(default_factory=list, description="Remediation steps if quality gates trigger")
    provenance: Optional[DataProvenance] = Field(default=None, description="Detailed data lineage categorization")

    @field_validator("ads")
    @classmethod
    def ensure_funnel_coverage(cls, ads: List[AdCopy]) -> List[AdCopy]:
        stages = {ad.funnel_stage for ad in ads}
        if len(stages) < 2:
            # In Phase 1 we only enforce a warning via comment – real rule later.
            pass
        return ads

    @field_validator("social_posts")
    @classmethod
    def lowercase_hashtags(cls, posts: List[SocialPost]) -> List[SocialPost]:
        for p in posts:
            p.hashtags = [h.lower() for h in p.hashtags]
        return posts


# ---------------------------------------------------------------------------
# Analytics schemas
# ---------------------------------------------------------------------------


class PerformanceForecast(BaseModel):
    """Holistic predictive performance model across key marketing metrics."""

    roas_forecast: float = Field(..., ge=0.0, description="Predicted Return on Ad Spend multiplier (e.g. 4.25)")
    ctr_forecast_percent: float = Field(..., ge=0.0, le=100.0, description="Predicted Click-Through Rate (%)")
    cpa_forecast_usd: float = Field(..., ge=0.0, description="Predicted Cost Per Acquisition in USD")
    cpc_forecast_usd: float = Field(default=2.50, ge=0.0, description="Predicted Cost Per Click in USD")
    conversion_rate_percent: float = Field(..., ge=0.0, le=100.0, description="Predicted conversion rate (%)")
    forecast_revenue_usd: float = Field(..., ge=0.0, description="Forecast gross revenue generated from campaign")
    forecast_conversions: int = Field(default=100, ge=0, description="Total projected conversions")
    forecast_impressions: int = Field(default=50000, ge=0, description="Total projected impressions")
    forecast_clicks: int = Field(default=1500, ge=0, description="Total projected clicks")


class PerformanceDeviation(BaseModel):
    """Identified divergence between target KPIs and predicted or observed performance."""

    metric_name: str = Field(..., description="Targeted KPI metric (e.g. ROAS, CTR, CPA)")
    target_value: float = Field(..., description="Goal benchmark target")
    predicted_or_observed_value: float = Field(..., description="Estimated or observed actual value")
    deviation_percent: float = Field(..., description="Percentage variance (+ for overperforming, - for underperforming)")
    status: str = Field(default="on_track", description="'on_track', 'underperforming', 'overperforming'")
    severity: str = Field(default="low", description="'low', 'medium', 'high', 'critical'")
    description: str = Field(..., description="Diagnostic summary of variance")


class RootCauseCandidate(BaseModel):
    """Root cause attribution for underperforming metrics or funnel friction."""

    issue: str = Field(..., description="Observed symptom or bottleneck")
    probable_root_cause: str = Field(..., description="Identified root cause rationale")
    affected_channel_or_stage: str = Field(..., description="Impacted channel or funnel stage")
    confidence: float = Field(default=0.85, ge=0.0, le=1.0, description="Confidence in attribution")
    evidence: str = Field(..., description="Supporting data evidence or benchmark citation")


class CampaignHealthScore(BaseModel):
    overall: PercentFloat = Field(..., ge=0, le=100)
    stage_scores: dict[FunnelStage, PercentFloat]


class MetricPrediction(BaseModel):
    metric: MetricType
    predicted_value: PositiveFloat
    confidence: PercentFloat = Field(..., ge=0, le=100)
    basis: str


class ContentScorecard(BaseModel):
    content_type: ContentType
    score: ScoreInt
    comments: Optional[str] = None


class ImprovementSuggestion(BaseModel):
    suggestion: str
    priority: SuggestionPriority
    impact_estimate_percent: PercentFloat = Field(..., ge=0, le=100)


class AnalyticsAgentInput(BaseModel):
    campaign: CampaignInput
    strategy: Optional[StrategyAgentOutput] = None
    research: Optional[ResearchAgentOutput] = None
    content: Optional[ContentAgentOutput] = None
    design: Optional[DesignAgentOutput] = None
    cv: Optional[CVAgentOutput] = None
    performance_data: Optional[Dict[str, Any]] = None
    observed_metrics: Optional[Dict[str, float]] = None


class KPITargetsDetailed(BaseModel):
    ctr_target: PercentFloat
    cpc_target: PositiveFloat
    cpa_target: PositiveFloat
    roas_target: PositiveFloat
    conversion_goals: List[str]
    kpi_recommendations: List[str]


class AnalyticsAgentOutput(BaseModel):
    # Core Phase 9 Performance Forecasting & Diagnostics
    forecast: Optional[PerformanceForecast] = Field(default=None, description="Detailed quantitative forecasts")
    performance_deviations: List[PerformanceDeviation] = Field(default_factory=list, description="Deviations from declared campaign goals")
    root_cause_candidates: List[RootCauseCandidate] = Field(default_factory=list, description="Attributed root causes for bottlenecks")
    recommendations: List[str] = Field(default_factory=list, description="Actionable optimization instructions")

    # Backwards-compatible legacy fields
    health_score: CampaignHealthScore
    predicted_metrics: List[MetricPrediction]
    content_scorecards: List[ContentScorecard] = Field(default_factory=list)
    improvement_suggestions: List[ImprovementSuggestion] = Field(default_factory=list)
    ab_test_recommendations: List[str] = Field(default_factory=list)
    budget_reallocation_advice: str = Field(default="Maintain balanced allocation across top-performing channels.")
    executive_summary: str = Field(default="Campaign demonstrates strong projected viability.")
    next_review_checkpoint: str = Field(default="Review live metrics 72 hours post-launch.")
    kpi_targets: Optional[KPITargetsDetailed] = None

    # Quality, Provenance & Governance
    confidence: float = Field(default=0.88, ge=0.0, le=1.0, description="Overall confidence score (0.0 - 1.0)")
    evidence: List[str] = Field(default_factory=list, description="Evidentiary basis for forecasts")
    corrective_actions: List[str] = Field(default_factory=list, description="Prescriptive directives for Correction Engine")
    provenance: Optional[DataProvenance] = Field(default=None, description="Data lineage categorization")

    @field_validator("health_score")
    @classmethod
    def health_range(cls, hs: CampaignHealthScore) -> CampaignHealthScore:
        if not (0 <= hs.overall <= 100):
            raise ValueError("Health score must be between 0 and 100")
        return hs


# ---------------------------------------------------------------------------
# Design schemas
# ---------------------------------------------------------------------------


class ImageDimensions(BaseModel):
    width: int = Field(..., gt=0)
    height: int = Field(..., gt=0)


class DesignBrief(BaseModel):
    dalle_prompt: str
    negative_prompt: str
    concept: str
    rationale: str
    image_dimensions: ImageDimensions
    style: ImageStyle
    format: str  # e.g., png, jpg, webp

    @field_validator("format")
    @classmethod
    def validate_format(cls, v: str) -> str:
        val = v.strip().lower()
        if val in {"png", "jpg", "jpeg", "webp"}:
            return "png" if val == "jpeg" else val
        return "png"


class GeneratedVisual(BaseModel):
    image_url: str
    brief: DesignBrief
    generation_error: Optional[str] = None


class CreativeAsset(BaseModel):
    """Structured creative asset specification produced by DesignAgent."""

    asset_id: str = Field(default_factory=lambda: f"asset-{uuid.uuid4().hex[:8]}")
    headline: Optional[str] = Field(default=None, description="Headline text placed on asset")
    cta: Optional[str] = Field(default=None, description="Call to action text placed on asset")
    image_url: Optional[str] = Field(default=None, description="Generated asset URL if engine is active")
    placeholder_url: str = Field(default="https://placehold.co/1200x628.png", description="Deterministic preview URL")
    dimensions: ImageDimensions = Field(default_factory=lambda: ImageDimensions(width=1200, height=628))
    aspect_ratio: str = Field(default="16:9", description="Aspect ratio (e.g. 1:1, 16:9, 9:16, 4:5)")
    format: str = Field(default="png", description="Format (png, jpg, webp)")
    channel: MarketingChannel = Field(default=MarketingChannel.linkedin, description="Target marketing channel")
    funnel_stage: FunnelStage = Field(default=FunnelStage.awareness, description="Funnel stage")
    generation_prompt: str = Field(default="Modern digital advertising campaign creative", description="Diffusion generation prompt")
    negative_prompt: str = Field(default="blurry, low resolution, distorted text, bad anatomy, watermark", description="Negative prompt")
    color_palette: List[str] = Field(default_factory=list, description="Primary brand color hexes used in asset")
    generation_status: str = Field(default="placeholder", description="Status: 'generated', 'unconfigured', 'failed', 'placeholder'")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Custom asset lineage and HITL metadata")


class CreativeMetadata(BaseModel):
    """Layout, typography, and visual styling metadata."""

    layout_type: str = Field(default="split_hero", description="Visual layout archetype (e.g. split_hero, centered, card_grid)")
    typography_style: str = Field(default="modern_sans_serif", description="Typography styling rule")
    primary_color_hex: str = Field(default="#1E3A8A", description="Primary brand color")
    secondary_color_hex: str = Field(default="#3B82F6", description="Secondary accent color")
    contrast_ratio: float = Field(default=4.5, ge=1.0, le=21.0, description="Calculated visual contrast ratio")
    visual_complexity: str = Field(default="clean_minimal", description="Complexity tier")


class DesignAgentInput(BaseModel):
    content: Optional[ContentAgentOutput] = None
    strategy: Optional[StrategyAgentOutput] = None
    campaign_id: Optional[str] = None
    task_id: Optional[str] = None
    revision_feedback: Optional[List[str]] = None


class DesignAgentOutput(BaseModel):
    # Core Phase 8 Outputs
    creative_assets: List[CreativeAsset] = Field(default_factory=list, description="Structured creative assets")
    creative_metadata: Optional[CreativeMetadata] = Field(default=None, description="Visual composition metadata")
    generation_prompts: List[str] = Field(default_factory=list, description="All formatted text-to-image prompts")
    variants: List[CreativeAsset] = Field(default_factory=list, description="Multi-aspect-ratio and channel variations")

    # Backwards-compatible legacy fields
    design_briefs: List[DesignBrief] = Field(default_factory=list)
    generated_visuals: List[GeneratedVisual] = Field(default_factory=list)
    brand_style_guide_snippet: str = Field(default="Use clean typography, high contrast, and approved brand hex palette.")
    generation_errors: List[str] = Field(default_factory=list)

    # Quality, Provenance & Governance
    confidence: float = Field(default=0.85, ge=0.0, le=1.0, description="Overall confidence score (0.0 - 1.0)")
    evidence: List[str] = Field(default_factory=list, description="Design rationale grounded in strategy and brand")
    corrective_actions: List[str] = Field(default_factory=list, description="Mitigation steps if visual issues arise")
    provenance: Optional[DataProvenance] = Field(default=None, description="Data lineage categorization")


# ---------------------------------------------------------------------------
# Campaign manager schemas
# ---------------------------------------------------------------------------


class ChannelBudgetAllocation(BaseModel):
    channel: MarketingChannel
    allocation_percent: PercentFloat = Field(..., ge=0, le=100)


class WeeklyScheduleItem(BaseModel):
    week_number: int = Field(..., ge=1)
    activities: List[str]


class AdSet(BaseModel):
    ads: List[AdCopy]
    budget_allocation: List[ChannelBudgetAllocation]


class ABTestPlan(BaseModel):
    test_name: str
    variant_a: str
    variant_b: str
    metric: MetricType
    duration_days: int


class KPITargets(BaseModel):
    metric: MetricType
    target_value: PositiveFloat


class CampaignManagerInput(BaseModel):
    campaign: CampaignInput
    strategy: StrategyAgentOutput
    research: ResearchAgentOutput
    content: ContentAgentOutput
    analytics: AnalyticsAgentOutput
    design: DesignAgentOutput


class CampaignManagerOutput(BaseModel):
    channel_budget_allocations: List[ChannelBudgetAllocation]
    weekly_schedule: List[WeeklyScheduleItem]
    ad_sets: List[AdSet]
    ab_test_plans: List[ABTestPlan]
    kpi_targets: List[KPITargets]


# ---------------------------------------------------------------------------
# Orchestrator schemas
# ---------------------------------------------------------------------------


class AgentRunRecord(BaseModel):
    agent_name: str
    status: AgentRunStatus
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    error_message: Optional[str] = None
    output_snapshot: Optional[dict] = None


class OrchestratorInput(BaseModel):
    campaign: CampaignInput


class OrchestratorOutput(BaseModel):
    campaign_input: CampaignInput
    strategy: StrategyAgentOutput
    research: ResearchAgentOutput
    content: ContentAgentOutput
    analytics: AnalyticsAgentOutput
    design: DesignAgentOutput
    campaign_manager: Optional[CampaignManagerOutput] = None
    agent_run_records: List[AgentRunRecord]
    final_campaign_summary: str
    errors: List[str] = []

    model_config = {
        "json_schema_extra": {
            "example": {
                "campaign_input": {
                    "business_name": "Nourish Egypt",
                    "product_description": "Healthy meal‑kit delivery",
                    "target_market": "Urban professionals 25‑40",
                    "budget_usd": 5000,
                    "goals": ["lead_generation", "brand_awareness"],
                    "channels": ["instagram", "facebook", "email"],
                    "tone_of_voice": "friendly",
                    "brand_colors": ["#2D6A4F", "#B7E4C7"],
                    "competitors": ["Eat Clean Egypt", "The Food Lab"],
                    "campaign_duration_days": 30,
                }
            }
        }
    }


# ---------------------------------------------------------------------------
# Phase 1 New Agent Schemas
# ---------------------------------------------------------------------------


class Persona(BaseModel):
    name: str
    demographics: str
    psychographics: str
    pain_points: List[str]
    goals: List[str]
    objections: List[str]
    buying_triggers: List[str]


class AudienceOutput(BaseModel):
    primary_persona: Persona
    secondary_personas: List[Persona]
    pain_points: List[str]
    motivations: List[str]
    objections: List[str]


class AudienceAgentInput(BaseModel):
    campaign: CampaignInput


class Competitor(BaseModel):
    name: str
    strengths: List[str]
    weaknesses: List[str]
    opportunities: List[str]
    threats: List[str]
    messaging_analysis: str
    pricing_comparison: str
    market_gaps: List[str]


class CompetitorLandscape(BaseModel):
    competitors: List[Competitor]
    opportunities: List[str]
    threats: List[str]
    pricing_comparison_summary: str = Field(default="", description="High-level synthesis of pricing models across rivals")
    positioning_map: Dict[str, str] = Field(default_factory=dict, description="Map of competitor name to market positioning angle")
    differentiators: List[str] = Field(default_factory=list, description="Client competitive advantages and counter-angles")
    confidence: float = Field(default=0.80, ge=0.0, le=1.0, description="Overall confidence score (0.0 - 1.0)")
    evidence: List[str] = Field(default_factory=list, description="Evidentiary basis for competitive assessments")
    corrective_actions: List[str] = Field(default_factory=list, description="Recommended remediation actions if data is thin")
    provenance: Optional[DataProvenance] = Field(default=None, description="Detailed data lineage categorization")


class CompetitorAgentInput(BaseModel):
    campaign: CampaignInput


class CreativeOutput(BaseModel):
    creative_brief: str
    design_direction: str
    color_palette: List[str]
    image_prompts: List[str]
    video_prompts: List[str]
    thumbnail_prompts: List[str]


class CreativeAgentInput(BaseModel):
    campaign: CampaignInput
    strategy: StrategyAgentOutput


class RLPolicyType(str, Enum):
    ppo = "ppo"
    bandit = "bandit"
    rule_based = "rule_based"
    random = "random"


class RLActionProposal(BaseModel):
    channel_allocations: Dict[str, float] = Field(..., description="Proposed channel budget weights summing to 1.0")
    bid_multiplier: float = Field(default=1.0, ge=0.5, le=2.0, description="Recommended bid scale factor")
    target_cpa_ceiling: float = Field(default=45.0, ge=0.0, description="Maximum allowable CPA bid threshold in USD")
    creative_refresh_recommended: bool = Field(default=False, description="Flag indicating creative rotation is triggered")
    suggested_frequency_cap: float = Field(default=3.0, ge=1.0, description="Weekly impression cap per user")


class ConstraintValidationResult(BaseModel):
    is_valid: bool = Field(..., description="Whether action proposal strictly complies with all bounds")
    violations: List[str] = Field(default_factory=list, description="Constraint bounds or business rules breached")
    modifications_applied: List[str] = Field(default_factory=list, description="Clamping and projections applied for safety")
    clamped_allocations: Dict[str, float] = Field(default_factory=dict, description="Final safe channel allocations")
    approved_by_safety_gate: bool = Field(default=True, description="Safety validator authorization status")
    requires_human_approval: bool = Field(default=False, description="Flag if action shift requires explicit human signoff")


class OptimizationAction(BaseModel):
    condition: str
    metric: str
    current_value: float
    target_value: float
    recommendation: str
    priority: SuggestionPriority
    action_steps: List[str]


class OptimizationOutput(BaseModel):
    optimization_actions: List[OptimizationAction] = Field(default_factory=list, description="Structured optimization directives")
    budget_reallocation_plan: str = Field(default="", description="Executive budget reallocation summary")
    performance_forecast: str = Field(default="", description="Forecasted performance narrative")
    policy_type: RLPolicyType = Field(default=RLPolicyType.ppo, description="RL policy used: 'ppo', 'bandit', or 'rule_based'")
    rl_state_vector: List[float] = Field(default_factory=list, description="10-dimensional normalized state vector")
    action_proposal: Optional[RLActionProposal] = Field(default=None, description="Proposed action parameters from RL policy")
    safety_validation: Optional[ConstraintValidationResult] = Field(default=None, description="Safety and bounds check result")
    predicted_reward: float = Field(default=0.0, description="Estimated policy reward score")
    confidence: float = Field(default=0.88, ge=0.0, le=1.0, description="Overall confidence level")
    evidence: List[str] = Field(default_factory=list, description="Empirical basis for optimization actions")
    corrective_actions: List[str] = Field(default_factory=list, description="Downstream fallback or guardrail directives")
    provenance: Optional[DataProvenance] = Field(default=None, description="Data provenance breakdown")


class OptimizationAgentInput(BaseModel):
    campaign: CampaignInput = Field(..., description="Campaign brief input")
    analytics: Optional[AnalyticsAgentOutput] = Field(default=None, description="Upstream analytics forecast & diagnostics")
    strategy: Optional[StrategyAgentOutput] = Field(default=None, description="Upstream strategy allocation and objectives")


class UTMParameters(BaseModel):
    utm_source: str
    utm_medium: str
    utm_campaign: str
    utm_term: Optional[str] = None
    utm_content: Optional[str] = None


class PublishingPackage(BaseModel):
    headlines: List[str]
    ctas: List[str]
    targeting_criteria: List[str]
    budget_allocation: dict[str, float]
    utm_parameters: UTMParameters
    campaign_metadata: dict[str, str]
    
    # Phase 13 Enterprise Dispatch Fields
    receipts: List[Dict[str, Any]] = Field(default_factory=list, description="Provider dispatch receipts")
    is_dry_run: bool = Field(default=True, description="Whether execution was safe dry-run")
    execution_mode: str = Field(default="dry_run", description="Execution mode: 'dry_run' or 'live'")
    published_channels: List[str] = Field(default_factory=list, description="Target channels published")
    validation_summary: Optional[Dict[str, Any]] = Field(default=None, description="Pre-flight validation summary")


class PublishingAgentInput(BaseModel):
    campaign: CampaignInput
    content: ContentAgentOutput
    strategy: StrategyAgentOutput


# ---------------------------------------------------------------------------
# Computer Vision (CV) Agent Schemas
# ---------------------------------------------------------------------------


class OCRResult(BaseModel):
    """OCR inspection findings on visual text."""

    extracted_text: List[str] = Field(default_factory=list, description="Text tokens detected in visual")
    detected_headline: Optional[str] = Field(default=None, description="Primary headline identified in image")
    detected_cta: Optional[str] = Field(default=None, description="Call to action identified in image")
    text_density_percent: float = Field(default=15.0, ge=0.0, le=100.0, description="Overlay text surface area percentage")
    readability_score: float = Field(default=85.0, ge=0.0, le=100.0, description="Readability index (0-100)")
    legibility_passed: bool = Field(default=True, description="Whether text meets minimum contrast and legibility")


class ObjectDetectionResult(BaseModel):
    """Object, logo, and face detection outcomes."""

    detected_objects: List[str] = Field(default_factory=list, description="Identified visual objects")
    logo_detected: bool = Field(default=True, description="Whether brand logo presence is verified")
    face_detected: bool = Field(default=False, description="Whether human faces are present")
    product_prominence_score: float = Field(default=88.0, ge=0.0, le=100.0, description="Centrality score of offering (0-100)")


class CVAgentInput(BaseModel):
    campaign: Optional[CampaignInput] = None
    design: Optional[DesignAgentOutput] = None
    image_url: Optional[str] = None


class CVAgentOutput(BaseModel):
    # Core Phase 8 Outputs
    creative_score: float = Field(default=85.0, ge=0.0, le=100.0, description="Composite creative quality score (0-100)")
    aesthetic_score: float = Field(default=8.5, ge=0.0, le=10.0, description="Visual aesthetic quality score out of 10")
    detected_issues: List[str] = Field(default_factory=list, description="Identified aesthetic or composition flaws")
    brand_violations: List[str] = Field(default_factory=list, description="Flagged brand style or color deviations")
    ocr_results: Optional[OCRResult] = Field(default=None, description="Detailed OCR text inspection findings")
    object_detection: Optional[ObjectDetectionResult] = Field(default=None, description="Object and logo detection findings")
    visual_issues: List[str] = Field(default_factory=list, description="Image quality or resolution issues")
    improvement_suggestions: List[str] = Field(default_factory=list, description="Prescriptive visual design revisions")
    confidence: float = Field(default=0.90, ge=0.0, le=1.0, description="Evaluation confidence score (0.0 - 1.0)")
    brand_safe: bool = Field(default=True, description="Whether image adheres to safety and brand policies")
    passed_quality_gate: bool = Field(default=True, description="Whether creative satisfies minimum quality threshold (>= 70)")

    # Backwards-compatible legacy fields
    ocr_detected_text: List[str] = Field(default_factory=list, description="Text extracted from image via OCR")
    ocr_passed: bool = Field(default=True, description="Whether text meets readability and copy criteria")
    color_dominance: List[str] = Field(default_factory=list, description="Dominant color hexes detected")
    recommendations: List[str] = Field(default_factory=list, description="Visual improvement suggestions")

    # Provenance & Governance
    evidence: List[str] = Field(default_factory=list, description="Computer vision model detections and citations")
    corrective_actions: List[str] = Field(default_factory=list, description="Directives for Design Agent revision loop")
    provenance: Optional[DataProvenance] = Field(default=None, description="Data lineage categorization")


# ---------------------------------------------------------------------------
# Correction Engine Agent Schemas
# ---------------------------------------------------------------------------


class CorrectionInput(BaseModel):
    campaign: CampaignInput
    analytics: AnalyticsAgentOutput
    current_attempt: int = Field(default=1, ge=1)
    max_attempts: int = Field(default=3, ge=1)


class CorrectionOutput(BaseModel):
    # Core Quality Gate & Status
    quality_gate_passed: bool = Field(..., description="Whether campaign passed minimum health threshold (>= 70)")
    requires_correction: bool = Field(..., description="Whether upstream agents must be re-run")
    target_agent_to_reinvoke: Optional[str] = Field(default=None, description="e.g. 'content_agent' or 'design_agent'")
    correction_prompt_directives: List[str] = Field(default_factory=list, description="Targeted guidance instructions")
    weakness_summary: str = Field(default="", description="Summary of identified weak metrics")
    correction_iteration: int = Field(default=1)

    # Phase 11 Closed-Loop Diagnostic & Task Extensions
    identified_problems: List[Dict[str, Any]] = Field(default_factory=list, description="Structured diagnostics of identified defects")
    responsible_agents: List[str] = Field(default_factory=list, description="List of responsible agents targeted for remediation")
    corrective_tasks: List[Dict[str, Any]] = Field(default_factory=list, description="Detailed corrective task directives")
    routed_corrections: List[str] = Field(default_factory=list, description="Execution dispatch history log")
    preserves_constraints: bool = Field(default=True, description="Strict guarantee that core CampaignContext invariants were preserved")
    evaluations: List[Dict[str, Any]] = Field(default_factory=list, description="Evaluations of re-executed tasks")
    circuit_breaker_triggered: bool = Field(default=False, description="Whether maximum retry attempts threshold was reached")
    confidence: float = Field(default=0.90, ge=0.0, le=1.0, description="Overall diagnostic confidence score")
    evidence: List[str] = Field(default_factory=list, description="Evidentiary support for diagnosis and routing")
    provenance: Optional[DataProvenance] = Field(default=None, description="Data lineage categorization")


# ---------------------------------------------------------------------------
# Monitoring Agent Schemas
# ---------------------------------------------------------------------------


class MonitoringInput(BaseModel):
    campaign: CampaignInput
    publishing: Optional[PublishingPackage] = None


class AnomalyEvent(BaseModel):
    metric: str
    observed_value: float
    expected_range: str
    severity: str  # 'low', 'medium', 'high', 'critical'
    description: str


class MonitoringOutput(BaseModel):
    telemetry_stream_active: bool = Field(default=True)
    live_impressions: int = Field(default=0, ge=0)
    live_clicks: int = Field(default=0, ge=0)
    live_spend_usd: float = Field(default=0.0, ge=0.0)
    live_conversions: int = Field(default=0, ge=0)
    detected_anomalies: List[AnomalyEvent] = Field(default_factory=list)
    stream_status: str = Field(default="nominal")
    feedback_payload: Dict[str, Any] = Field(default_factory=dict)
