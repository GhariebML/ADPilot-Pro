"""Executable Agent Contract Registry for all 11 Master Pipeline Agents.

Runtime authority must be represented in executable typed configuration/code,
NEVER in Markdown files.
"""

from __future__ import annotations

from typing import Dict, List, Optional
from .agent_contract import (
    AgentActionBoundary,
    AgentContract,
    AgentIdentity,
    QualityCriteria,
)

# ---------------------------------------------------------------------------
# 1. Strategy Agent Contract
# ---------------------------------------------------------------------------
STRATEGY_AGENT_CONTRACT = AgentContract(
    identity=AgentIdentity(
        agent_id="strategy_agent",
        name="Strategy Agent",
        version="1.0.0",
        role="Synthesizes core marketing positioning, value proposition, messaging pillars, and funnel budget allocation.",
        stage_order=1,
    ),
    responsibilities=[
        "Synthesize unique value proposition (USP) and elevator pitch from campaign brief",
        "Define target market positioning and brand voice guidelines",
        "Formulate multi-stage funnel strategy with budget allocation percentages summing to 100%",
        "Identify strategic risks, dependencies, and differentiators",
    ],
    input_schema_name="StrategyAgentInput",
    output_schema_name="StrategyAgentOutput",
    tools=["campaign_profiler", "market_intelligence", "funnel_allocator"],
    models=["gpt-4o", "claude-3-5-sonnet"],
    boundaries=AgentActionBoundary(
        allowed_actions=[
            "Formulate strategic positioning statements",
            "Allocate percentage budget across awareness, consideration, and conversion stages",
            "Define tone of voice and brand messaging pillars",
        ],
        forbidden_actions=[
            "Modify overall campaign dollar budget",
            "Directly dispatch ads to ad networks",
            "Generate image or visual assets",
            "Override original business identity information",
        ],
    ),
    dependencies=["context_builder", "product_classifier"],
    quality=QualityCriteria(
        success_criteria=[
            "Funnel budget allocations sum exactly to 100%",
            "Positioning statement is non-empty and contains key differentiator",
            "At least one primary channel is specified",
        ],
        failure_conditions=[
            "Funnel budget percentages do not equal 100%",
            "Empty positioning statement or USP",
            "Invalid tone of voice enumeration",
        ],
        confidence_threshold=0.75,
        evidence_requirements=["Detailed rationale for funnel stage budget split and target persona summary"],
        corrective_actions=["Re-prompt model with budget normalization constraint", "Fallback to default 50/30/20 funnel split"],
    ),
)

# ---------------------------------------------------------------------------
# 2. Research & Audience Agent Contract
# ---------------------------------------------------------------------------
RESEARCH_AGENT_CONTRACT = AgentContract(
    identity=AgentIdentity(
        agent_id="research_agent",
        name="Research & Audience Agent",
        version="1.0.0",
        role="Identifies and profiles target buyer personas, psychological triggers, and customer journey pain points.",
        stage_order=2,
    ),
    responsibilities=[
        "Synthesize primary and secondary buyer personas with demographics and psychographics",
        "Extract customer pain points, core motivations, and buying triggers",
        "Map audience persona to preferred communication channels",
        "Generate negative targeting criteria to avoid budget waste",
    ],
    input_schema_name="AudienceInput",
    output_schema_name="AudienceOutput",
    tools=["qdrant_vector_store", "audience_synthesizer", "market_demographics_db"],
    models=["gpt-4o", "fastembed-bge"],
    boundaries=AgentActionBoundary(
        allowed_actions=[
            "Query RAG vector database for audience insights",
            "Synthesize persona demographics and pain points",
            "Recommend audience exclusion criteria",
        ],
        forbidden_actions=[
            "Change strategic messaging pillars",
            "Generate ad copy or landing page content",
            "Mutate user target market specification",
        ],
    ),
    dependencies=["strategy_agent"],
    quality=QualityCriteria(
        success_criteria=[
            "Primary persona has complete name, title, demographics, and pain points",
            "At least 2 buying triggers are articulated",
        ],
        failure_conditions=[
            "Missing primary persona",
            "Zero pain points or buying triggers identified",
        ],
        confidence_threshold=0.70,
        evidence_requirements=["Persona profile backed by industry vertical context"],
        corrective_actions=["Re-query RAG store with broadened search scope", "Apply industry default persona archetype"],
    ),
)

# ---------------------------------------------------------------------------
# 3. Competitor Agent Contract
# ---------------------------------------------------------------------------
COMPETITOR_AGENT_CONTRACT = AgentContract(
    identity=AgentIdentity(
        agent_id="competitor_agent",
        name="Competitor Agent",
        version="1.0.0",
        role="Analyzes competitor landscape, pricing, counter-messaging strategies, and market positioning gaps.",
        stage_order=3,
    ),
    responsibilities=[
        "Benchmark product against direct and indirect competitors",
        "Identify competitor strengths, weaknesses, and market positioning",
        "Formulate counter-positioning angles and competitive moat advantages",
    ],
    input_schema_name="CompetitorInput",
    output_schema_name="CompetitorLandscape",
    tools=["competitive_benchmarking", "market_share_index", "web_search"],
    models=["gpt-4o"],
    boundaries=AgentActionBoundary(
        allowed_actions=[
            "Analyze competitor strengths and weaknesses",
            "Recommend counter-messaging hooks",
        ],
        forbidden_actions=[
            "Make unsubstantiated legal claims regarding competitors",
            "Alter campaign product pricing",
        ],
    ),
    dependencies=["research_agent"],
    quality=QualityCriteria(
        success_criteria=[
            "At least one competitor analyzed or generic competitive baseline established",
            "At least two differentiators articulated",
        ],
        failure_conditions=[
            "Empty competitor landscape output",
        ],
        confidence_threshold=0.70,
        evidence_requirements=["Competitive differentiation analysis matrix"],
        corrective_actions=["Fallback to standard market vertical baseline"],
    ),
)

# ---------------------------------------------------------------------------
# 4. Content Agent Contract
# ---------------------------------------------------------------------------
CONTENT_AGENT_CONTRACT = AgentContract(
    identity=AgentIdentity(
        agent_id="content_agent",
        name="Content Agent",
        version="1.0.0",
        role="Drafts high-converting copy across ads, email sequences, social posts, landing pages, and CTAs.",
        stage_order=4,
    ),
    responsibilities=[
        "Generate multi-variant ad copy covering awareness, consideration, and conversion stages",
        "Draft email nurture sequences and automated onboarding drips",
        "Create social media posts with validated lowercase hashtags",
        "Produce high-impact CTA button and headline variants",
    ],
    input_schema_name="ContentAgentInput",
    output_schema_name="ContentAgentOutput",
    tools=["copywriting_engine", "multichannel_formatter", "hashtag_normalizer"],
    models=["gpt-4o", "claude-3-5-sonnet"],
    boundaries=AgentActionBoundary(
        allowed_actions=[
            "Generate ad headlines, body copy, and CTAs",
            "Draft multi-stage funnel email sequences",
            "Format social posts and blog outlines",
        ],
        forbidden_actions=[
            "Alter strategy positioning or brand guidelines",
            "Publish content to live networks directly",
            "Modify campaign budget allocation",
        ],
    ),
    dependencies=["strategy_agent", "research_agent", "competitor_agent"],
    quality=QualityCriteria(
        success_criteria=[
            "Ads cover at least 2 distinct funnel stages",
            "Social posts contain valid lowercase hashtags",
            "At least 3 distinct CTA variants provided",
        ],
        failure_conditions=[
            "Generated ad copy missing primary headline or CTA",
            "Character limit violations on platform copy",
        ],
        confidence_threshold=0.75,
        evidence_requirements=["Multi-variant copy mapped to strategic messaging pillars"],
        corrective_actions=["Re-generate underperforming funnel stage variants", "Trigger copy length normalizer"],
    ),
)

# ---------------------------------------------------------------------------
# 5. Design Agent Contract
# ---------------------------------------------------------------------------
DESIGN_AGENT_CONTRACT = AgentContract(
    identity=AgentIdentity(
        agent_id="design_agent",
        name="Design Agent",
        version="1.0.0",
        role="Translates copy and brand guidelines into image generation prompts, layout specs, and color palettes.",
        stage_order=5,
    ),
    responsibilities=[
        "Generate detailed image generation prompts with negative prompts for diffusion models",
        "Validate image dimensions and aspect ratios according to channel requirements",
        "Enforce brand color hex palette compliance",
        "Generate visual assets or mock previews",
    ],
    input_schema_name="DesignAgentInput",
    output_schema_name="DesignAgentOutput",
    tools=["diffusion_canvas", "brand_palette_matcher", "aspect_ratio_validator"],
    models=["dall-e-3", "stability-sdxl"],
    boundaries=AgentActionBoundary(
        allowed_actions=[
            "Formulate visual prompts and design briefs",
            "Specify target image dimensions and aspect ratios",
            "Match brand color palette",
        ],
        forbidden_actions=[
            "Violate brand color hex code guidelines",
            "Generate prohibited or unsafe visual content",
            "Alter ad copy text inside content schema",
        ],
    ),
    dependencies=["content_agent"],
    quality=QualityCriteria(
        success_criteria=[
            "Design briefs include explicit dimensions, style, and negative prompts",
            "Brand style guide snippet is populated",
        ],
        failure_conditions=[
            "Invalid image dimensions (<= 0)",
            "Missing negative prompt in design brief",
        ],
        confidence_threshold=0.70,
        evidence_requirements=["Design concept rationale mapped to brand guidelines"],
        corrective_actions=["Apply default brand dimensions (1200x628)", "Apply standard negative prompt filters"],
    ),
)

# ---------------------------------------------------------------------------
# 6. Computer Vision (CV) Agent Contract
# ---------------------------------------------------------------------------
CV_AGENT_CONTRACT = AgentContract(
    identity=AgentIdentity(
        agent_id="cv_agent",
        name="Computer Vision (CV) Agent",
        version="1.0.0",
        role="Evaluates visual aesthetics, performs OCR text inspection on ad creatives, and validates brand safety.",
        stage_order=6,
    ),
    responsibilities=[
        "Score generated visual assets using aesthetic assessment models",
        "Extract and verify embedded text via OCR for legibility and accuracy",
        "Verify visual compliance with platform brand safety standards",
    ],
    input_schema_name="CVAgentInput",
    output_schema_name="CVAgentOutput",
    tools=["clip_aesthetic_scorer", "ocr_text_validator", "brand_safety_filter"],
    models=["clip-vit-base-patch32", "yolov8"],
    boundaries=AgentActionBoundary(
        allowed_actions=[
            "Compute aesthetic scores (1.0 - 10.0)",
            "Extract OCR text and check copy overlap",
            "Flag brand safety visual violations",
        ],
        forbidden_actions=[
            "Alter image generation briefs directly",
            "Bypass safety flags without human override",
        ],
    ),
    dependencies=["design_agent"],
    quality=QualityCriteria(
        success_criteria=[
            "Aesthetic score >= 6.5 / 10.0",
            "OCR text accuracy matches design copy",
            "Zero brand safety policy violations",
        ],
        failure_conditions=[
            "Aesthetic score < 6.0",
            "Severe visual artifacting or safety violation detected",
        ],
        confidence_threshold=0.80,
        evidence_requirements=["Quantitative aesthetic score breakdown and OCR text diff"],
        corrective_actions=["Flag visual for re-generation by Design Agent"],
    ),
)

# ---------------------------------------------------------------------------
# 7. Analytics Agent Contract
# ---------------------------------------------------------------------------
ANALYTICS_AGENT_CONTRACT = AgentContract(
    identity=AgentIdentity(
        agent_id="analytics_agent",
        name="Analytics Agent",
        version="1.0.0",
        role="Evaluates end-to-end campaign viability, calculates health scores, and predicts CTR/CPC/CPA performance.",
        stage_order=7,
    ),
    responsibilities=[
        "Evaluate multi-dimensional campaign health score (0-100) across all funnel stages",
        "Predict key performance metrics (CTR, CPC, CPA, ROAS) with statistical confidence",
        "Generate prioritized, actionable improvement suggestions",
        "Enforce quality gate threshold (score >= 70.0) before downstream publishing",
    ],
    input_schema_name="AnalyticsAgentInput",
    output_schema_name="AnalyticsAgentOutput",
    tools=["health_score_evaluator", "ctr_prediction_model", "cpa_benchmarking_engine"],
    models=["ridge_regression_scorer", "gpt-4o"],
    boundaries=AgentActionBoundary(
        allowed_actions=[
            "Compute health scores and funnel stage scores",
            "Predict CTR/CPC metrics and confidence intervals",
            "Recommend budget reallocations and A/B test experiments",
        ],
        forbidden_actions=[
            "Directly overwrite strategy or content copy",
            "Deploy ad budget to external ad accounts",
        ],
    ),
    dependencies=["content_agent", "design_agent"],
    quality=QualityCriteria(
        success_criteria=[
            "Overall health score is within [0, 100]",
            "All predicted metrics contain confidence percentage and estimation basis",
            "Stage scores provided for awareness and conversion",
        ],
        failure_conditions=[
            "Overall health score outside [0, 100]",
            "Missing basis explanation on predicted metrics",
        ],
        confidence_threshold=0.75,
        evidence_requirements=["Ridge regression feature attribution and historical benchmark comparisons"],
        corrective_actions=["Trigger Correction Engine loop back to Content Agent if overall score < 70.0"],
    ),
)

# ---------------------------------------------------------------------------
# 8. Optimizer Agent Contract
# ---------------------------------------------------------------------------
OPTIMIZATION_AGENT_CONTRACT = AgentContract(
    identity=AgentIdentity(
        agent_id="optimization_agent",
        name="Optimizer Agent (RL / ML)",
        version="1.0.0",
        role="Applies reinforcement learning and optimization policies to optimize budget allocations, bidding, and schedules.",
        stage_order=8,
    ),
    responsibilities=[
        "Generate concrete optimization actions (bid adjustments, audience pruning, budget shifts)",
        "Formulate multi-channel budget reallocation plans to maximize ROAS",
        "Produce forward-looking performance forecast based on suggested adjustments",
    ],
    input_schema_name="OptimizationInput",
    output_schema_name="OptimizationOutput",
    tools=["budget_reallocator", "rl_policy_optimizer", "bid_curve_simulator"],
    models=["ppo_bid_optimizer", "gpt-4o"],
    boundaries=AgentActionBoundary(
        allowed_actions=[
            "Recommend percentage budget shifts between channels and ad sets",
            "Generate prioritized optimization action steps",
        ],
        forbidden_actions=[
            "Exceed overall campaign budget cap",
            "Execute destructive campaign deletion operations",
        ],
    ),
    dependencies=["analytics_agent"],
    quality=QualityCriteria(
        success_criteria=[
            "At least one prioritized optimization action provided",
            "Budget reallocation plan is mathematically bounded",
            "Performance forecast is articulated",
        ],
        failure_conditions=[
            "Empty optimization action list",
            "Budget reallocation exceeding 100% total allocation",
        ],
        confidence_threshold=0.70,
        evidence_requirements=["Expected impact percentage and step-by-step action plan"],
        corrective_actions=["Apply conservative rule-based reallocation (shift 5% to top performing channel)"],
    ),
)

# ---------------------------------------------------------------------------
# 9. Correction Engine Agent Contract
# ---------------------------------------------------------------------------
CORRECTION_AGENT_CONTRACT = AgentContract(
    identity=AgentIdentity(
        agent_id="correction_agent",
        name="Correction Engine Agent",
        version="1.0.0",
        role="Evaluates quality gate scorecards and generates actionable feedback directives to re-align creative copy and strategy.",
        stage_order=9,
    ),
    responsibilities=[
        "Evaluate Analytics Agent quality scorecard against threshold (>= 70.0)",
        "Extract specific weaknesses in headlines, tone, or channel fit",
        "Synthesize concise prompt injection directives for re-running Content or Design agents",
        "Track correction iteration count to prevent infinite loops",
    ],
    input_schema_name="CorrectionInput",
    output_schema_name="CorrectionOutput",
    tools=["feedback_injector", "prompt_refiner", "quality_gate_evaluator"],
    models=["rule_engine", "gpt-4o"],
    boundaries=AgentActionBoundary(
        allowed_actions=[
            "Evaluate health score against quality gate threshold",
            "Generate actionable correction hints for upstream agents",
            "Trigger pipeline re-entry at Content or Design stage",
        ],
        forbidden_actions=[
            "Exceed maximum allowed correction iterations (max 3)",
            "Silently lower quality gate threshold",
        ],
    ),
    dependencies=["analytics_agent", "optimization_agent"],
    quality=QualityCriteria(
        success_criteria=[
            "Quality gate decision is deterministically boolean",
            "Correction directives are actionable and target identified weak sub-scores",
        ],
        failure_conditions=[
            "Correction count exceeding loop ceiling without resolution",
        ],
        confidence_threshold=0.85,
        evidence_requirements=["Score diff breakdown and specific correction guidance text"],
        corrective_actions=["Escalate to Human-in-the-Loop review if max retries exceeded"],
    ),
)

# ---------------------------------------------------------------------------
# 10. Publishing Agent Contract
# ---------------------------------------------------------------------------
PUBLISHING_AGENT_CONTRACT = AgentContract(
    identity=AgentIdentity(
        agent_id="publishing_agent",
        name="Publishing Agent",
        version="1.0.0",
        role="Formats, validates, and dispatches approved campaign payloads to external advertising and messaging channels.",
        stage_order=11,
    ),
    responsibilities=[
        "Transform unified campaign payload into channel-specific API schemas (Meta, LinkedIn, Email, Google)",
        "Attach tracking UTM parameters and conversion webhooks",
        "Execute publishing dispatch or generate staging review URLs",
        "Record external campaign IDs and dispatch audit receipts",
    ],
    input_schema_name="PublishingAgentInput",
    output_schema_name="PublishingAgentOutput",
    tools=["meta_graph_api", "linkedin_v2_client", "mailchimp_api", "utm_builder"],
    models=["utm_builder", "gpt-4o"],
    boundaries=AgentActionBoundary(
        allowed_actions=[
            "Publish approved campaigns to configured advertising channels",
            "Generate platform preview URLs and dispatch receipts",
            "Append UTM tracking parameters",
        ],
        forbidden_actions=[
            "Publish unapproved campaigns when human sign-off is required",
            "Publish to channels not explicitly enabled in the CampaignContext",
            "Mutate ad spend or credit card billing settings",
        ],
    ),
    dependencies=["hitl_gate"],
    quality=QualityCriteria(
        success_criteria=[
            "All active target channels receive dispatch payloads or preview receipts",
            "UTM tracking parameters are valid and attached",
        ],
        failure_conditions=[
            "Channel API returns authentication or schema rejection error",
            "Missing required human approval signature",
        ],
        confidence_threshold=0.90,
        evidence_requirements=["Channel dispatch response receipts with external IDs"],
        corrective_actions=["Mark channel as failed and queue for retry with exponential backoff"],
    ),
)

# ---------------------------------------------------------------------------
# 11. Monitoring Agent Contract
# ---------------------------------------------------------------------------
MONITORING_AGENT_CONTRACT = AgentContract(
    identity=AgentIdentity(
        agent_id="monitoring_agent",
        name="Monitoring Agent",
        version="1.0.0",
        role="Tracks real-time live performance streams, detects KPI anomalies, and feeds telemetry back into the Optimizer.",
        stage_order=12,
    ),
    responsibilities=[
        "Ingest live metric telemetry streams (impressions, clicks, conversions, spend)",
        "Detect statistical performance anomalies (sudden CPC spike, CTR drop)",
        "Trigger webhook alerts on critical deviations",
        "Feed telemetry back into Analytics and Optimizer agents for closed-loop learning",
    ],
    input_schema_name="MonitoringInput",
    output_schema_name="MonitoringOutput",
    tools=["live_metrics_stream", "anomaly_detector", "slack_alert_webhook"],
    models=["time_series_forecaster", "z_score_detector"],
    boundaries=AgentActionBoundary(
        allowed_actions=[
            "Stream live campaign metrics",
            "Flag statistical anomalies and performance alerts",
            "Package telemetry payload for closed-loop feedback",
        ],
        forbidden_actions=[
            "Pause or delete external ad campaigns without authorization",
            "Modify live campaign budgets directly",
        ],
    ),
    dependencies=["publishing_agent"],
    quality=QualityCriteria(
        success_criteria=[
            "Telemetry stream initialized and responsive",
            "Anomaly detection thresholds calibrated to baseline",
        ],
        failure_conditions=[
            "Telemetry stream disconnection lasting > 300s",
        ],
        confidence_threshold=0.85,
        evidence_requirements=["Time-series metric telemetry stream snapshots"],
        corrective_actions=["Reconnect telemetry stream with backoff", "Emit fallback heartbeat status"],
    ),
)


# ---------------------------------------------------------------------------
# Contract Registry Map
# ---------------------------------------------------------------------------

AGENT_CONTRACTS: Dict[str, AgentContract] = {
    "strategy_agent": STRATEGY_AGENT_CONTRACT,
    "research_agent": RESEARCH_AGENT_CONTRACT,
    "audience_agent": RESEARCH_AGENT_CONTRACT,
    "competitor_agent": COMPETITOR_AGENT_CONTRACT,
    "content_agent": CONTENT_AGENT_CONTRACT,
    "design_agent": DESIGN_AGENT_CONTRACT,
    "cv_agent": CV_AGENT_CONTRACT,
    "analytics_agent": ANALYTICS_AGENT_CONTRACT,
    "optimization_agent": OPTIMIZATION_AGENT_CONTRACT,
    "correction_agent": CORRECTION_AGENT_CONTRACT,
    "correction_engine": CORRECTION_AGENT_CONTRACT,
    "publishing_agent": PUBLISHING_AGENT_CONTRACT,
    "monitoring_agent": MONITORING_AGENT_CONTRACT,
}


def get_agent_contract(agent_id: str) -> Optional[AgentContract]:
    """Retrieve the typed executable contract for a given agent identifier."""
    return AGENT_CONTRACTS.get(agent_id)


def list_all_contracts() -> List[AgentContract]:
    """Retrieve all distinct registered agent contracts."""
    seen = set()
    distinct_contracts = []
    for contract in AGENT_CONTRACTS.values():
        if contract.identity.agent_id not in seen:
            seen.add(contract.identity.agent_id)
            distinct_contracts.append(contract)
    return distinct_contracts
