"""Planner Service for generating Master Pipeline Execution Plans.

The Planner is responsible for orchestration, DAG planning, and governance, NOT business execution.
It produces an ExecutionPlan that strictly adheres to the frozen Master Pipeline sequence.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional
from uuid import uuid4

from ..schemas.campaign_context import (
    CampaignContext,
    ExecutionMode,
    ProductClassificationOutput,
    ProductType,
)
from ..schemas.execution_plan import (
    ExecutionPlan,
    PlannedStep,
    WorkflowState,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Canonical 12-Step Frozen Master Pipeline Template
# ---------------------------------------------------------------------------

FROZEN_PIPELINE_STEPS = [
    {
        "agent_name": "strategy_agent",
        "stage_order": 1,
        "display_name": "Strategy Agent",
        "is_optional": False,
        "dependencies": ["context_builder", "product_classifier"],
        "required_tools": ["campaign_profiler", "market_intelligence"],
        "required_models": ["gpt-4o", "claude-3-5-sonnet"],
        "expected_outputs": ["positioning_statement", "usp", "messaging_pillars", "funnel_strategy"],
        "timeout_seconds": 30.0,
        "max_retries": 3,
        "validation_point": "funnel_budget_allocation_sum_100",
        "approval_point": False,
    },
    {
        "agent_name": "research_agent",
        "stage_order": 2,
        "display_name": "Research & Audience Agent",
        "is_optional": False,
        "dependencies": ["strategy_agent"],
        "required_tools": ["qdrant_vector_store", "audience_synthesizer"],
        "required_models": ["gpt-4o", "fastembed-bge"],
        "expected_outputs": ["primary_persona", "pain_points", "motivations", "buying_triggers"],
        "timeout_seconds": 30.0,
        "max_retries": 3,
        "validation_point": "primary_persona_validation",
        "approval_point": False,
    },
    {
        "agent_name": "competitor_agent",
        "stage_order": 3,
        "display_name": "Competitor Agent",
        "is_optional": False,
        "dependencies": ["research_agent"],
        "required_tools": ["competitive_benchmarking", "market_share_index"],
        "required_models": ["gpt-4o"],
        "expected_outputs": ["competitor_landscape", "differentiators", "threat_matrix"],
        "timeout_seconds": 30.0,
        "max_retries": 3,
        "validation_point": None,
        "approval_point": False,
    },
    {
        "agent_name": "content_agent",
        "stage_order": 4,
        "display_name": "Content Agent",
        "is_optional": False,
        "dependencies": ["strategy_agent", "research_agent", "competitor_agent"],
        "required_tools": ["copywriting_engine", "multichannel_formatter"],
        "required_models": ["gpt-4o", "claude-3-5-sonnet"],
        "expected_outputs": ["ads", "email_sequences", "social_posts", "cta_variants"],
        "timeout_seconds": 45.0,
        "max_retries": 3,
        "validation_point": "content_length_and_format_check",
        "approval_point": False,
    },
    {
        "agent_name": "design_agent",
        "stage_order": 5,
        "display_name": "Design Agent",
        "is_optional": False,
        "dependencies": ["content_agent"],
        "required_tools": ["diffusion_canvas", "brand_palette_matcher"],
        "required_models": ["dall-e-3", "stability-sdxl"],
        "expected_outputs": ["visual_prompts", "generated_visuals", "color_palette"],
        "timeout_seconds": 45.0,
        "max_retries": 3,
        "validation_point": "brand_color_hex_compliance",
        "approval_point": False,
    },
    {
        "agent_name": "cv_agent",
        "stage_order": 6,
        "display_name": "Computer Vision (CV) Agent",
        "is_optional": True,
        "dependencies": ["design_agent"],
        "required_tools": ["clip_aesthetic_scorer", "ocr_text_validator"],
        "required_models": ["clip-vit-base-patch32", "yolov8"],
        "expected_outputs": ["aesthetic_score", "ocr_validation", "brand_safety_visual"],
        "timeout_seconds": 30.0,
        "max_retries": 2,
        "validation_point": "visual_aesthetic_score >= 6.5",
        "approval_point": False,
    },
    {
        "agent_name": "analytics_agent",
        "stage_order": 7,
        "display_name": "Analytics Agent",
        "is_optional": False,
        "dependencies": ["content_agent", "design_agent"],
        "required_tools": ["health_score_evaluator", "ctr_prediction_model"],
        "required_models": ["ridge_regression_scorer", "gpt-4o"],
        "expected_outputs": ["health_score", "predicted_metrics", "improvement_suggestions"],
        "timeout_seconds": 30.0,
        "max_retries": 3,
        "validation_point": "analytics_health_gate >= 70.0",
        "approval_point": False,
    },
    {
        "agent_name": "optimization_agent",
        "stage_order": 8,
        "display_name": "Optimizer Agent (RL / ML)",
        "is_optional": False,
        "dependencies": ["analytics_agent"],
        "required_tools": ["budget_reallocator", "rl_policy_optimizer"],
        "required_models": ["ppo_bid_optimizer", "gpt-4o"],
        "expected_outputs": ["optimization_actions", "budget_reallocation_plan", "forecast"],
        "timeout_seconds": 30.0,
        "max_retries": 3,
        "validation_point": None,
        "approval_point": False,
    },
    {
        "agent_name": "correction_engine",
        "stage_order": 9,
        "display_name": "Correction Engine",
        "is_optional": False,
        "dependencies": ["analytics_agent", "optimization_agent"],
        "required_tools": ["feedback_injector", "prompt_refiner"],
        "required_models": ["rule_engine"],
        "expected_outputs": ["correction_status", "retry_recommendations"],
        "timeout_seconds": 15.0,
        "max_retries": 1,
        "validation_point": "quality_gate_passed",
        "approval_point": False,
    },
    {
        "agent_name": "hitl_gate",
        "stage_order": 10,
        "display_name": "Human-in-the-Loop (HITL) Gate",
        "is_optional": False,
        "dependencies": ["correction_engine"],
        "required_tools": ["approval_modal", "audit_log_exporter"],
        "required_models": ["auth_rbac"],
        "expected_outputs": ["human_approval_signature", "approval_timestamp"],
        "timeout_seconds": 300.0,
        "max_retries": 1,
        "validation_point": "human_sign_off_received",
        "approval_point": True,
    },
    {
        "agent_name": "publishing_agent",
        "stage_order": 11,
        "display_name": "Publishing Agent",
        "is_optional": False,
        "dependencies": ["hitl_gate"],
        "required_tools": ["meta_graph_api", "linkedin_v2_client", "mailchimp_api"],
        "required_models": ["utm_builder", "gpt-4o"],
        "expected_outputs": ["published_campaign_ids", "live_urls", "dispatch_receipts"],
        "timeout_seconds": 60.0,
        "max_retries": 3,
        "validation_point": "all_target_channels_published",
        "approval_point": False,
    },
    {
        "agent_name": "monitoring_agent",
        "stage_order": 12,
        "display_name": "Monitoring Agent",
        "is_optional": False,
        "dependencies": ["publishing_agent"],
        "required_tools": ["live_metrics_stream", "anomaly_detector", "slack_alert_webhook"],
        "required_models": ["time_series_forecaster"],
        "expected_outputs": ["telemetry_stream", "anomaly_flags", "feedback_loop_payload"],
        "timeout_seconds": 30.0,
        "max_retries": 3,
        "validation_point": "monitoring_stream_active",
        "approval_point": False,
    },
]


class CampaignPlanner:
    """Produces a tailored ExecutionPlan based on CampaignContext, Classification, Memory, and RAG."""

    def __init__(self, default_timeout: float = 30.0, default_retries: int = 3) -> None:
        self.default_timeout = default_timeout
        self.default_retries = default_retries

    def plan(
        self,
        context: CampaignContext,
        classification: Optional[ProductClassificationOutput] = None,
        memory_records: Optional[List[Dict[str, Any]]] = None,
        rag_context: Optional[str] = None,
    ) -> ExecutionPlan:
        """Generate the deterministic ExecutionPlan adhering strictly to the Master Pipeline sequence."""
        logger.info("CampaignPlanner | generating execution plan for campaign: %s", context.campaign_id)

        # Resolve classification
        prod_classification = classification or context.classification
        if not prod_classification:
            # Fallback default if not yet run
            prod_type = context.product.product_type if context.product else ProductType.other
            exec_mode = ExecutionMode.direct_response
            required_agents = ["strategy_agent", "research_agent", "content_agent", "analytics_agent"]
            optional_agents = ["design_agent", "cv_agent", "optimization_agent"]
        else:
            prod_type = prod_classification.product_type
            exec_mode = prod_classification.recommended_execution_mode
            required_agents = prod_classification.required_agents
            optional_agents = prod_classification.optional_agents

        # Summaries
        rag_summary = rag_context or (
            f"Indexed {len(context.channels)} distribution channels and {len(context.goals)} goals."
        )
        mem_summary = f"{len(memory_records)} prior memory records loaded." if memory_records else "Fresh campaign context session."

        # Construct PlannedSteps strictly in frozen Master Pipeline order
        planned_steps: List[PlannedStep] = []
        validation_points_list: List[str] = []
        approval_points_list: List[str] = []

        for template in FROZEN_PIPELINE_STEPS:
            agent_name = template["agent_name"]
            
            # Determine whether this step is optional for this specific product classification
            is_opt = template["is_optional"]
            if agent_name in optional_agents and agent_name not in required_agents:
                is_opt = True

            # If human approval is explicitly required or flagged by HITL
            is_approval = template["approval_point"]
            if agent_name == "hitl_gate" or (
                agent_name == "publishing_agent" and context.approvals.human_approval_required
            ):
                is_approval = True
                approval_points_list.append(f"Require sign-off before {agent_name} execution")

            val_point = template["validation_point"]
            if val_point:
                validation_points_list.append(f"Stage {template['stage_order']} ({agent_name}): {val_point}")

            step = PlannedStep(
                step_id=f"step-{template['stage_order']:02d}-{agent_name}",
                agent_name=agent_name,
                stage_order=template["stage_order"],
                display_name=template["display_name"],
                is_optional=is_opt,
                dependencies=template["dependencies"],
                required_tools=template["required_tools"],
                required_models=template["required_models"],
                expected_outputs=template["expected_outputs"],
                timeout_seconds=template["timeout_seconds"],
                max_retries=template["max_retries"],
                validation_point=val_point,
                approval_point=is_approval,
                state=WorkflowState.PENDING,
            )
            planned_steps.append(step)

        execution_plan = ExecutionPlan(
            plan_id=f"plan-{uuid4().hex[:12]}",
            campaign_id=context.campaign_id,
            product_type=prod_type,
            execution_mode=exec_mode,
            agent_sequence=planned_steps,
            validation_points=validation_points_list,
            approval_points=approval_points_list,
            rag_context_summary=rag_summary,
            memory_context_summary=mem_summary,
            status=WorkflowState.PENDING,
            current_step_index=0,
            total_steps=len(planned_steps),
            completed_steps=0,
            failed_steps=0,
        )

        logger.info(
            "CampaignPlanner | Created ExecutionPlan: id=%s, steps=%d, mode=%s",
            execution_plan.plan_id,
            len(execution_plan.agent_sequence),
            execution_plan.execution_mode.value,
        )

        # Attach to context
        context.execution_plan = execution_plan
        context.record_agent_output("campaign_planner", execution_plan)

        return execution_plan
