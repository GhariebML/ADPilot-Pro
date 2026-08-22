"""Problem Classifier: Identifies, categorizes, and prioritizes defects across 7 distinct trigger sources."""

from __future__ import annotations

import logging
import uuid
from typing import Any, Dict, List, Optional

from ..schemas.agent_schemas import CampaignContext
from .schemas import (
    CorrectionTriggerSource,
    IdentifiedProblem,
    ProblemCategory,
    ProblemSeverity,
)

logger = logging.getLogger(__name__)


class ProblemClassifier:
    """Diagnoses root causes and maps defects to categorized IdentifiedProblem instances."""

    def diagnose_all(
        self,
        context: CampaignContext,
        trigger_source: Optional[CorrectionTriggerSource] = None,
        human_feedback: Optional[str] = None,
        explicit_deviations: Optional[List[Dict[str, Any]]] = None,
        explicit_cv_issues: Optional[List[str]] = None,
        explicit_validation_failures: Optional[List[str]] = None,
    ) -> List[IdentifiedProblem]:
        """Exhaustively inspects campaign context and inputs to extract all diagnosed problems."""
        problems: List[IdentifiedProblem] = []

        # 1. Human Rejection & Directives
        if human_feedback or trigger_source == CorrectionTriggerSource.HUMAN_REJECTION:
            feedback_text = human_feedback or "Campaign rejected during human review."
            category, agent, severity = self._classify_human_feedback(feedback_text)
            problems.append(
                IdentifiedProblem(
                    problem_id=f"prob-{uuid.uuid4().hex[:8]}",
                    source=CorrectionTriggerSource.HUMAN_REJECTION,
                    category=category,
                    description=f"Human reviewer critique: {feedback_text}",
                    responsible_agent=agent,
                    severity=severity,
                    context_keys_involved=["approvals", "brief"],
                )
            )

        # 2. Computer Vision (CV) Issues & Visual Aesthetics
        problems.extend(self._diagnose_cv_issues(context, explicit_cv_issues))

        # 3. Analytics Quality Gate, Health Score & Forecasting Bottlenecks
        problems.extend(self._diagnose_analytics_issues(context))

        # 4. Performance Deviations (Observed Metrics & Benchmarks)
        problems.extend(self._diagnose_performance_deviations(context, explicit_deviations))

        # 5. Reinforcement Learning (RL) Optimization Violations
        problems.extend(self._diagnose_rl_issues(context))

        # 6. Strategy & Audience Alignment
        problems.extend(self._diagnose_strategy_issues(context))

        # 7. Validation & Schema Failures
        if explicit_validation_failures:
            for failure in explicit_validation_failures:
                problems.append(
                    IdentifiedProblem(
                        problem_id=f"prob-{uuid.uuid4().hex[:8]}",
                        source=CorrectionTriggerSource.VALIDATION_FAILURE,
                        category=ProblemCategory.SCHEMA_VALIDATION_ERROR,
                        description=f"Validation failure detected: {failure}",
                        responsible_agent="strategy_agent" if "strategy" in failure.lower() else "content_agent",
                        severity=ProblemSeverity.HIGH,
                    )
                )

        # Sort problems by severity: CRITICAL -> HIGH -> MEDIUM -> LOW
        severity_order = {
            ProblemSeverity.CRITICAL: 0,
            ProblemSeverity.HIGH: 1,
            ProblemSeverity.MEDIUM: 2,
            ProblemSeverity.LOW: 3,
        }
        problems.sort(key=lambda p: severity_order.get(p.severity, 4))
        return problems

    def _diagnose_cv_issues(
        self,
        context: CampaignContext,
        explicit_cv_issues: Optional[List[str]] = None,
    ) -> List[IdentifiedProblem]:
        problems: List[IdentifiedProblem] = []

        # Check explicit CV issues passed in input
        if explicit_cv_issues:
            for issue in explicit_cv_issues:
                cat = ProblemCategory.BRAND_SAFETY_VIOLATION if "safety" in issue.lower() else ProblemCategory.POOR_CREATIVE_QUALITY
                problems.append(
                    IdentifiedProblem(
                        problem_id=f"prob-{uuid.uuid4().hex[:8]}",
                        source=CorrectionTriggerSource.CV_ISSUE,
                        category=cat,
                        description=f"CV defect flagged: {issue}",
                        responsible_agent="design_agent",
                        severity=ProblemSeverity.HIGH if cat == ProblemCategory.BRAND_SAFETY_VIOLATION else ProblemSeverity.MEDIUM,
                        context_keys_involved=["design", "cv"],
                    )
                )

        # Inspect context.cv or context.cv_agent
        cv_out = getattr(context, "cv", None) or getattr(context, "cv_agent", None)
        if cv_out:
            # Aesthetic score check (< 6.0 is deficient)
            score = getattr(cv_out, "overall_score", None) or getattr(cv_out, "aesthetic_score", None)
            if score is not None and float(score) < 6.0:
                problems.append(
                    IdentifiedProblem(
                        problem_id=f"prob-{uuid.uuid4().hex[:8]}",
                        source=CorrectionTriggerSource.CV_ISSUE,
                        category=ProblemCategory.POOR_CREATIVE_QUALITY,
                        description=f"Creative aesthetic score ({float(score):.1f}/10.0) is below acceptable quality gate threshold (6.0/10.0).",
                        responsible_agent="design_agent",
                        severity=ProblemSeverity.HIGH,
                        metric_impacted="aesthetic_score",
                        current_value=float(score),
                        target_value=6.5,
                        context_keys_involved=["design", "cv"],
                    )
                )

            # Detected brand safety or quality issues in cv_out
            detected_issues = getattr(cv_out, "detected_issues", []) or []
            for issue in detected_issues:
                desc = issue.description if hasattr(issue, "description") else str(issue)
                is_safety = any(w in desc.lower() for w in ["safety", "prohibited", "trademark", "unauthorized", "violation", "superlative"])
                problems.append(
                    IdentifiedProblem(
                        problem_id=f"prob-{uuid.uuid4().hex[:8]}",
                        source=CorrectionTriggerSource.CV_ISSUE,
                        category=ProblemCategory.BRAND_SAFETY_VIOLATION if is_safety else ProblemCategory.POOR_CREATIVE_QUALITY,
                        description=f"CV diagnostic: {desc}",
                        responsible_agent="design_agent",
                        severity=ProblemSeverity.CRITICAL if is_safety else ProblemSeverity.MEDIUM,
                        context_keys_involved=["design", "brand"],
                    )
                )

            # Check explicit brand_safe boolean flag
            if hasattr(cv_out, "brand_safe") and not cv_out.brand_safe:
                problems.append(
                    IdentifiedProblem(
                        problem_id=f"prob-{uuid.uuid4().hex[:8]}",
                        source=CorrectionTriggerSource.CV_ISSUE,
                        category=ProblemCategory.BRAND_SAFETY_VIOLATION,
                        description="CV inspection flagged brand safety policy non-compliance.",
                        responsible_agent="design_agent",
                        severity=ProblemSeverity.CRITICAL,
                        context_keys_involved=["design", "brand"],
                    )
                )

        return problems

    def _diagnose_analytics_issues(self, context: CampaignContext) -> List[IdentifiedProblem]:
        problems: List[IdentifiedProblem] = []
        analytics = getattr(context, "analytics", None)
        if not analytics:
            return problems

        # 1. Overall Health Score Quality Gate (threshold >= 70.0)
        health_score = None
        if hasattr(analytics, "health_score") and analytics.health_score:
            health_score = float(getattr(analytics.health_score, "overall", 100.0))

        if health_score is not None and health_score < 70.0:
            problems.append(
                IdentifiedProblem(
                    problem_id=f"prob-{uuid.uuid4().hex[:8]}",
                    source=CorrectionTriggerSource.ANALYTICS_ISSUE,
                    category=ProblemCategory.HEALTH_SCORE_GATE_FAILURE,
                    description=f"Campaign overall health score ({health_score:.1f}/100) failed the minimum quality gate threshold (70.0/100).",
                    responsible_agent="content_agent",  # Content is primary re-entry for copy/messaging quality
                    severity=ProblemSeverity.HIGH,
                    metric_impacted="health_score",
                    current_value=health_score,
                    target_value=75.0,
                    context_keys_involved=["analytics", "content"],
                )
            )

        # 2. Performance Deviations in Analytics Output
        deviations = getattr(analytics, "performance_deviations", []) or []
        for dev in deviations:
            metric = getattr(dev, "metric", "unknown")
            curr = getattr(dev, "current_value", None)
            tgt = getattr(dev, "target_value", None)
            desc = getattr(dev, "description", f"Metric '{metric}' deviating from goal.")
            
            cat, agent = self._map_metric_to_category_and_agent(metric)
            problems.append(
                IdentifiedProblem(
                    problem_id=f"prob-{uuid.uuid4().hex[:8]}",
                    source=CorrectionTriggerSource.PERFORMANCE_DEVIATION,
                    category=cat,
                    description=desc,
                    responsible_agent=agent,
                    severity=ProblemSeverity.HIGH if "cpa" in metric.lower() or "roas" in metric.lower() else ProblemSeverity.MEDIUM,
                    metric_impacted=metric,
                    current_value=float(curr) if curr is not None else None,
                    target_value=float(tgt) if tgt is not None else None,
                    context_keys_involved=["analytics", agent.replace("_agent", "")],
                )
            )

        # 3. Forecast Deviations (e.g. ROAS < target)
        forecast = getattr(analytics, "forecast", None)
        if forecast:
            exp_roas = getattr(forecast, "expected_roas", None)
            target_roas = float(context.kpis.target_roas) if hasattr(context, "kpis") and context.kpis and context.kpis.target_roas else 3.0
            if exp_roas is not None and float(exp_roas) < target_roas * 0.80:
                problems.append(
                    IdentifiedProblem(
                        problem_id=f"prob-{uuid.uuid4().hex[:8]}",
                        source=CorrectionTriggerSource.ANALYTICS_ISSUE,
                        category=ProblemCategory.LOW_ROAS,
                        description=f"Forecasted ROAS ({float(exp_roas):.2f}x) is substantially below target ROAS ({target_roas:.2f}x).",
                        responsible_agent="optimization_agent",
                        severity=ProblemSeverity.HIGH,
                        metric_impacted="roas",
                        current_value=float(exp_roas),
                        target_value=target_roas,
                        context_keys_involved=["analytics", "optimization"],
                    )
                )

        return problems

    def _diagnose_performance_deviations(
        self,
        context: CampaignContext,
        explicit_deviations: Optional[List[Dict[str, Any]]] = None,
    ) -> List[IdentifiedProblem]:
        problems: List[IdentifiedProblem] = []
        if not explicit_deviations:
            return problems

        for dev in explicit_deviations:
            metric = str(dev.get("metric", "ctr")).lower()
            curr = dev.get("current_value")
            tgt = dev.get("target_value")
            desc = dev.get("description", f"Performance deviation on {metric}.")

            cat, agent = self._map_metric_to_category_and_agent(metric)
            problems.append(
                IdentifiedProblem(
                    problem_id=f"prob-{uuid.uuid4().hex[:8]}",
                    source=CorrectionTriggerSource.PERFORMANCE_DEVIATION,
                    category=cat,
                    description=desc,
                    responsible_agent=agent,
                    severity=ProblemSeverity.HIGH,
                    metric_impacted=metric,
                    current_value=float(curr) if curr is not None else None,
                    target_value=float(tgt) if tgt is not None else None,
                )
            )

        return problems

    def _diagnose_rl_issues(self, context: CampaignContext) -> List[IdentifiedProblem]:
        problems: List[IdentifiedProblem] = []
        opt = getattr(context, "optimization", None)
        if not opt:
            return problems

        # Check safety validation in optimization output
        safety = getattr(opt, "safety_validation", None)
        if safety:
            violations = getattr(safety, "violations", []) or []
            if violations:
                problems.append(
                    IdentifiedProblem(
                        problem_id=f"prob-{uuid.uuid4().hex[:8]}",
                        source=CorrectionTriggerSource.RL_ISSUE,
                        category=ProblemCategory.INVALID_RL_ACTION,
                        description=f"RL Action constraint breaches: {'; '.join(violations)}",
                        responsible_agent="optimization_agent",
                        severity=ProblemSeverity.HIGH,
                        context_keys_involved=["optimization"],
                    )
                )

        return problems

    def _diagnose_strategy_issues(self, context: CampaignContext) -> List[IdentifiedProblem]:
        problems: List[IdentifiedProblem] = []
        strat = getattr(context, "strategy", None)
        if not strat:
            return problems

        # Check funnel budget split sum == 100
        funnel = getattr(strat, "funnel_strategy", []) or []
        if funnel:
            total_pct = sum(getattr(f, "budget_allocation_percent", 0.0) for f in funnel)
            if round(total_pct) != 100:
                problems.append(
                    IdentifiedProblem(
                        problem_id=f"prob-{uuid.uuid4().hex[:8]}",
                        source=CorrectionTriggerSource.STRATEGY_MISMATCH,
                        category=ProblemCategory.BUDGET_OVERRUN,
                        description=f"Strategy funnel budget allocations sum to {total_pct:.1f}%, must equal 100%.",
                        responsible_agent="strategy_agent",
                        severity=ProblemSeverity.HIGH,
                        context_keys_involved=["strategy", "budget"],
                    )
                )

        return problems

    def _classify_human_feedback(self, feedback: str) -> tuple[ProblemCategory, str, ProblemSeverity]:
        """Maps free-text human feedback to the most appropriate agent and category."""
        lowered = feedback.lower()
        if any(w in lowered for w in ["headline", "copy", "text", "tone", "cta", "hook", "word", "language", "click", "ctr"]):
            return ProblemCategory.LOW_CTR, "content_agent", ProblemSeverity.HIGH
        elif any(w in lowered for w in ["image", "visual", "color", "palette", "font", "aesthetic", "graphic", "logo", "photo", "layout"]):
            return ProblemCategory.POOR_CREATIVE_QUALITY, "design_agent", ProblemSeverity.HIGH
        elif any(w in lowered for w in ["audience", "persona", "positioning", "usp", "market", "competitor", "value prop", "targeting"]):
            return ProblemCategory.AUDIENCE_MISMATCH, "strategy_agent", ProblemSeverity.HIGH
        elif any(w in lowered for w in ["budget", "bid", "cpa", "cac", "roas", "channel allocation", "spend", "cost"]):
            return ProblemCategory.HIGH_CAC, "optimization_agent", ProblemSeverity.HIGH
        elif any(w in lowered for w in ["forecast", "predict", "analytics", "health score", "kpi"]):
            return ProblemCategory.POOR_FORECAST, "analytics_agent", ProblemSeverity.MEDIUM
        else:
            return ProblemCategory.HUMAN_CRITIQUE, "content_agent", ProblemSeverity.MEDIUM

    def _map_metric_to_category_and_agent(self, metric: str) -> tuple[ProblemCategory, str]:
        m = metric.lower()
        if "ctr" in m or "click" in m:
            return ProblemCategory.LOW_CTR, "content_agent"
        elif "cpa" in m or "cac" in m or "cost_per_acquisition" in m:
            return ProblemCategory.HIGH_CAC, "optimization_agent"
        elif "roas" in m or "roi" in m or "revenue" in m:
            return ProblemCategory.LOW_ROAS, "optimization_agent"
        elif "aesthetic" in m or "visual" in m or "quality" in m:
            return ProblemCategory.POOR_CREATIVE_QUALITY, "design_agent"
        elif "safety" in m or "brand" in m:
            return ProblemCategory.BRAND_SAFETY_VIOLATION, "design_agent"
        elif "persona" in m or "audience" in m:
            return ProblemCategory.AUDIENCE_MISMATCH, "strategy_agent"
        else:
            return ProblemCategory.OTHER, "content_agent"
