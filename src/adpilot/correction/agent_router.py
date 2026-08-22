"""Agent Router & Task Synthesizer: Maps diagnosed defects into targeted, non-destructive corrective tasks."""

from __future__ import annotations

import logging
import uuid
from typing import List

from ..schemas.agent_schemas import CampaignContext
from .schemas import (
    CorrectiveTask,
    IdentifiedProblem,
    ProblemCategory,
    ProblemSeverity,
)

logger = logging.getLogger(__name__)


class AgentRouter:
    """Generates structured, constraint-preserving corrective tasks for designated target agents."""

    def generate_tasks(
        self,
        problems: List[IdentifiedProblem],
        context: CampaignContext,
    ) -> List[CorrectiveTask]:
        """Synthesizes prioritized corrective tasks from diagnosed problems."""
        tasks: List[CorrectiveTask] = []

        # Deduplicate problems by responsible agent and category
        seen_keys = set()
        deduped_problems: List[IdentifiedProblem] = []
        for p in problems:
            key = (p.responsible_agent, p.category)
            if key not in seen_keys:
                seen_keys.add(key)
                deduped_problems.append(p)

        for problem in deduped_problems:
            task = self._synthesize_task_for_problem(problem, context)
            if task:
                tasks.append(task)

        # Sort tasks by priority (1 = highest)
        tasks.sort(key=lambda t: t.priority)
        return tasks

    def _synthesize_task_for_problem(
        self,
        problem: IdentifiedProblem,
        context: CampaignContext,
    ) -> CorrectiveTask:
        agent = problem.responsible_agent
        cat = problem.category
        task_id = f"task-{uuid.uuid4().hex[:8]}"

        # Base invariant constraints applicable to all tasks
        constraints = [
            f"Preserve overall budget cap of ${float(context.budget.total_budget):,.2f}" if hasattr(context, "budget") and context.budget else "Preserve total campaign budget cap",
            f"Adhere to brand tone '{getattr(context.brand, 'tone_of_voice', 'professional')}'",
            "Do not alter registered business identity or core product specification",
        ]

        if cat == ProblemCategory.BRAND_SAFETY_VIOLATION or problem.severity == ProblemSeverity.CRITICAL:
            directive = "Eliminate all potentially prohibited, hyperbolic, or non-compliant claims and visual elements."
            prompt_injection = (
                f"CORRECTION DIRECTIVE (CRITICAL SAFETY: {problem.description}):\n"
                "- Remove all unverified guarantees, superlatives, or non-compliant medical/financial claims.\n"
                "- Ensure visual imagery contains zero sensitive, trademarked, or unsafe artifacts.\n"
                "- Ensure full compliance with advertising platform policies."
            )
            expected_outcome = "Zero detected brand safety or policy violations."
            priority = 1

        elif cat == ProblemCategory.LOW_CTR or agent == "content_agent":
            directive = "Revise ad headlines and primary copy to improve click-through intent, clarity, and value proposition hooks."
            prompt_injection = (
                f"CORRECTION DIRECTIVE (Issue: {problem.description}):\n"
                "- Generate high-converting, benefit-driven headlines with strong emotional resonance.\n"
                "- Replace passive verbs with direct, action-oriented CTAs.\n"
                "- Emphasize unique differentiators and address core persona pain points immediately in the hook.\n"
                "- Strictly adhere to character limits per channel."
            )
            expected_outcome = "Improved copy variations yielding predicted CTR >= 2.50%."
            priority = 1

        elif cat in [ProblemCategory.POOR_CREATIVE_QUALITY, ProblemCategory.COLOR_PALETTE_MISMATCH] or agent == "design_agent":
            colors_str = ", ".join(context.brand.brand_colors) if hasattr(context, "brand") and context.brand and context.brand.brand_colors else "#2D6A4F, #B7E4C7"
            directive = "Regenerate visual creative briefs with higher aesthetic standards, negative prompts, and strict palette fidelity."
            prompt_injection = (
                f"CORRECTION DIRECTIVE (Issue: {problem.description}):\n"
                f"- Enforce strict brand hex palette colors: [{colors_str}].\n"
                "- Add comprehensive negative prompts: 'lowres, blurry, distorted text, visual artifacts, oversaturated'.\n"
                "- Use clean, professional composition with clear focal points suitable for high-converting ads.\n"
                "- Specify standard high-resolution dimensions (1200x628 landscape, 1080x1080 square)."
            )
            expected_outcome = "Creative assets scoring aesthetic evaluation >= 6.5/10.0 and passing OCR text checks."
            priority = 1

        elif cat in [ProblemCategory.AUDIENCE_MISMATCH, ProblemCategory.WEAK_POSITIONING] or agent == "strategy_agent":
            directive = "Re-align strategic positioning and messaging pillars to match target buyer personas."
            prompt_injection = (
                f"CORRECTION DIRECTIVE (Issue: {problem.description}):\n"
                "- Refine unique selling proposition (USP) to directly solve target market core friction points.\n"
                "- Ensure funnel budget strategy allocations across Awareness, Consideration, and Conversion sum to exactly 100%.\n"
                "- Clarify target persona demographics and primary communication channels."
            )
            expected_outcome = "Strategy output with positioning aligned to market demographics and 100% budget sum."
            priority = 2

        elif cat in [ProblemCategory.HIGH_CAC, ProblemCategory.LOW_ROAS, ProblemCategory.INVALID_RL_ACTION] or agent == "optimization_agent":
            directive = "Adjust channel budget distributions and bid multipliers to reduce CPA and maximize ROAS within safety boundaries."
            prompt_injection = (
                f"CORRECTION DIRECTIVE (Issue: {problem.description}):\n"
                "- Rebalance budget away from high-CPA channels towards proven higher-converting channels.\n"
                "- Enforce channel allocation bounding between 5.0% and 80.0% per channel (sum = 100.0%).\n"
                "- Clamp bid multiplier adjustments within safe limits [0.80x, 1.20x] to cool down acquisition costs.\n"
                "- Trigger creative refresh if fatigue index > 0.40."
            )
            expected_outcome = "Projected CPA <= target CPA and action proposal strictly passing Constraint Validator."
            priority = 2

        elif cat in [ProblemCategory.POOR_FORECAST, ProblemCategory.HEALTH_SCORE_GATE_FAILURE] or agent == "analytics_agent":
            directive = "Re-evaluate campaign health score breakdown and update performance forecasting models."
            prompt_injection = (
                f"CORRECTION DIRECTIVE (Issue: {problem.description}):\n"
                "- Re-calculate multi-dimensional health scores across awareness, consideration, and conversion stages.\n"
                "- Generate specific root cause candidates and prioritized improvement recommendations.\n"
                "- Provide verified statistical confidence intervals for predicted CTR, CPA, and ROAS."
            )
            expected_outcome = "Analytics report with clear root-cause attribution and overall health score >= 70.0."
            priority = 2

        else:
            directive = f"Execute remediation for diagnosed defect: {problem.description}"
            prompt_injection = f"CORRECTION DIRECTIVE: Please remediate the following defect while strictly preserving campaign constraints:\n{problem.description}"
            expected_outcome = "Resolved defect verified by quality gate."
            priority = 3

        return CorrectiveTask(
            task_id=task_id,
            target_agent=agent,
            action_directive=directive,
            prompt_injection=prompt_injection,
            constraints_enforced=constraints,
            priority=priority,
            expected_outcome=expected_outcome,
        )
