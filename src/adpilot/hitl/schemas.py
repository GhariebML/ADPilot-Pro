"""Phase 12 — Human-in-the-Loop (HITL) Typed Schemas."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4
from pydantic import BaseModel, Field, field_validator


class HumanDecisionType(str, Enum):
    """Supported human actions and decision types."""
    REVIEW = "review"
    APPROVE = "approve"
    REJECT = "reject"
    EDIT = "edit"
    REQUEST_REVISION = "request_revision"
    OVERRIDE = "override"
    FINAL_APPROVAL = "final_approval"


class ApprovalStage(str, Enum):
    """Mandatory high-risk approval gates across the campaign lifecycle."""
    STRATEGY = "strategy"
    CONTENT = "content"
    CREATIVE = "creative"
    BUDGET_OPTIMIZER = "budget_optimizer"
    PUBLISHING = "publishing"


class RiskLevel(str, Enum):
    """Execution risk tier assigned to the operation."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class HumanReviewRequest(BaseModel):
    """Payload presented to a human reviewer to solicit a decision."""
    request_id: str = Field(default_factory=lambda: f"rev-{uuid4().hex[:8]}")
    campaign_id: str = Field(..., description="Campaign identifier")
    stage: ApprovalStage = Field(..., description="Target approval gate")
    agent_name: str = Field(..., description="Agent that produced the recommendation")
    agent_recommendation: Dict[str, Any] = Field(..., description="Structured agent proposal")
    risk_level: RiskLevel = Field(default=RiskLevel.HIGH, description="Risk tier of this execution step")
    summary: str = Field(default="", description="Executive summary of proposal")
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    status: str = Field(default="pending", description="Status: 'pending', 'approved', 'rejected', 'modified'")


class HITLAuditRecord(BaseModel):
    """Immutable audit record capturing every human intervention and decision."""
    audit_id: str = Field(default_factory=lambda: f"audit-{uuid4().hex[:12]}")
    user: str = Field(..., min_length=1, description="Identifier / username of human decision maker")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    campaign_id: str = Field(..., description="Associated campaign identifier")
    stage: ApprovalStage = Field(..., description="Approval gate stage")
    agent: str = Field(..., description="Responsible agent identifier")
    decision: HumanDecisionType = Field(..., description="Selected decision type")
    previous_output: Dict[str, Any] = Field(default_factory=dict, description="Original agent recommendation")
    modified_output: Optional[Dict[str, Any]] = Field(default=None, description="Human modified output if edited or overridden")
    reason: str = Field(..., min_length=3, description="Mandatory rationale for the decision")
    revision_directives: List[str] = Field(default_factory=list, description="Directives passed if requesting revision")
    is_override: bool = Field(default=False, description="Flag indicating model override")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional contextual metadata")


class HITLDecisionSubmission(BaseModel):
    """Payload submitted by a human reviewer."""
    user: str = Field(..., min_length=1, description="Username or ID of reviewer")
    decision: HumanDecisionType = Field(..., description="Action taken")
    reason: str = Field(..., min_length=3, description="Mandatory rationale explaining decision")
    modified_output: Optional[Dict[str, Any]] = Field(default=None, description="Modified payload if edited or overridden")
    revision_directives: List[str] = Field(default_factory=list, description="Targeted prompt directives if revision requested")
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("user", "reason")
    @classmethod
    def validate_non_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field must not be empty or whitespace only.")
        return v.strip()


class HITLGateOutput(BaseModel):
    """Structured output returned by Stage 10 HITL Gate."""
    stage: ApprovalStage
    decision: HumanDecisionType
    approved_by: str
    approved_at: str
    reason: str
    is_approved: bool
    audit_id: str
    requires_revision: bool = False
    revision_directives: List[str] = Field(default_factory=list)
    modified_output: Optional[Dict[str, Any]] = None
