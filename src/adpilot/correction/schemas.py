"""Phase 11 — Correction Engine Typed Schemas."""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from ..schemas.agent_schemas import CampaignContext, DataProvenance


class CorrectionTriggerSource(str, Enum):
    """Originating trigger source for a corrective intervention."""
    AGENT_FEEDBACK = "agent_feedback"
    PERFORMANCE_DEVIATION = "performance_deviation"
    VALIDATION_FAILURE = "validation_failure"
    CV_ISSUE = "cv_issue"
    ANALYTICS_ISSUE = "analytics_issue"
    RL_ISSUE = "rl_issue"
    HUMAN_REJECTION = "human_rejection"
    STRATEGY_MISMATCH = "strategy_mismatch"


class ProblemSeverity(str, Enum):
    """Severity tier for prioritized remediation triage."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ProblemCategory(str, Enum):
    """Categorical classification of detected campaign defects."""
    LOW_CTR = "low_ctr"
    HIGH_CAC = "high_cac"
    LOW_ROAS = "low_roas"
    POOR_CREATIVE_QUALITY = "poor_creative_quality"
    BRAND_SAFETY_VIOLATION = "brand_safety_violation"
    COLOR_PALETTE_MISMATCH = "color_palette_mismatch"
    AUDIENCE_MISMATCH = "audience_mismatch"
    WEAK_POSITIONING = "weak_positioning"
    POOR_FORECAST = "poor_forecast"
    HEALTH_SCORE_GATE_FAILURE = "health_score_gate_failure"
    INVALID_RL_ACTION = "invalid_rl_action"
    BUDGET_OVERRUN = "budget_overrun"
    HUMAN_CRITIQUE = "human_critique"
    SCHEMA_VALIDATION_ERROR = "schema_validation_error"
    OTHER = "other"


class IdentifiedProblem(BaseModel):
    """Structured diagnostic representation of a campaign bottleneck or violation."""
    problem_id: str = Field(..., description="Unique identifier for the problem")
    source: CorrectionTriggerSource = Field(..., description="Trigger source that surfaced this defect")
    category: ProblemCategory = Field(..., description="Categorized problem taxonomy")
    description: str = Field(..., description="Detailed diagnostic description of what went wrong")
    responsible_agent: str = Field(..., description="Target agent responsible for correcting this issue")
    severity: ProblemSeverity = Field(default=ProblemSeverity.MEDIUM, description="Remediation priority severity")
    metric_impacted: Optional[str] = Field(default=None, description="Impacted KPI or diagnostic metric name")
    current_value: Optional[float] = Field(default=None, description="Observed or calculated deficient value")
    target_value: Optional[float] = Field(default=None, description="Required target or benchmark threshold")
    context_keys_involved: List[str] = Field(default_factory=list, description="Keys in CampaignContext relevant to this problem")


class CorrectiveTask(BaseModel):
    """Actionable directive instructing a specific upstream agent to remediate a defect."""
    task_id: str = Field(..., description="Unique task identifier")
    target_agent: str = Field(..., description="Agent name to re-invoke, e.g., 'content_agent', 'design_agent'")
    action_directive: str = Field(..., description="Concise, prescriptive instruction on what must be revised")
    prompt_injection: str = Field(..., description="Targeted prompt guidance or retry instructions")
    constraints_enforced: List[str] = Field(default_factory=list, description="Explicit boundaries that must not be violated")
    context_adjustments: Dict[str, Any] = Field(default_factory=dict, description="Safe context annotations or flags")
    priority: int = Field(default=1, ge=1, le=5, description="Execution priority (1 is highest)")
    expected_outcome: str = Field(..., description="Measurable validation condition required to resolve problem")


class CorrectionEvaluation(BaseModel):
    """Post-execution verification record validating if a corrective task succeeded."""
    problem_id: str
    task_id: str
    target_agent: str
    is_resolved: bool = Field(..., description="Whether the corrective re-execution satisfied resolution criteria")
    before_metric: Optional[float] = None
    after_metric: Optional[float] = None
    verification_notes: str = Field(default="", description="Auditable reasoning on resolution outcome")


class CorrectionEngineInput(BaseModel):
    """Input payload to the Correction Engine."""
    campaign_context: CampaignContext
    trigger_source: Optional[CorrectionTriggerSource] = None
    human_feedback: Optional[str] = None
    deviations: List[Dict[str, Any]] = Field(default_factory=list)
    cv_issues: List[str] = Field(default_factory=list)
    validation_failures: List[str] = Field(default_factory=list)
    current_attempt: int = Field(default=1, ge=1)
    max_attempts: int = Field(default=3, ge=1)


class CorrectionEngineOutput(BaseModel):
    """Canonical output produced by the Correction Engine."""
    identified_problems: List[IdentifiedProblem] = Field(default_factory=list, description="All diagnosed campaign problems")
    responsible_agents: List[str] = Field(default_factory=list, description="Unique list of agents targeted for remediation")
    corrective_tasks: List[CorrectiveTask] = Field(default_factory=list, description="Generated prescriptive remediation tasks")
    routed_corrections: List[str] = Field(default_factory=list, description="Execution log of dispatched corrective tasks")
    preserves_constraints: bool = Field(default=True, description="Strict guarantee that core CampaignContext invariants were preserved")
    quality_gate_passed: bool = Field(default=False, description="Whether all defects are resolved and quality gate passes")
    evaluations: List[CorrectionEvaluation] = Field(default_factory=list, description="Evaluations of re-executed tasks")
    iteration_count: int = Field(default=1, description="Current correction loop iteration number")
    circuit_breaker_triggered: bool = Field(default=False, description="True if max attempts reached without complete resolution")
    confidence: float = Field(default=0.90, ge=0.0, le=1.0, description="Overall confidence in correction synthesis")
    evidence: List[str] = Field(default_factory=list, description="Evidentiary support for diagnosis and routing")
    provenance: Optional[DataProvenance] = Field(default=None, description="Data lineage classification")

    # Backwards-compatible fields for legacy schemas
    requires_correction: bool = Field(default=True)
    target_agent_to_reinvoke: Optional[str] = None
    correction_prompt_directives: List[str] = Field(default_factory=list)
    weakness_summary: str = Field(default="")
    correction_iteration: int = Field(default=1)
