"""Pydantic v2 schemas for ExecutionPlan, WorkflowState, and PlannedStep."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field

from .campaign_context import ExecutionMode, ProductType


class WorkflowState(str, Enum):
    """Explicit lifecycle states for workflow steps and entire execution plans."""

    PENDING = "PENDING"
    PLANNING = "PLANNING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    RETRYING = "RETRYING"
    SKIPPED = "SKIPPED"
    WAITING_FOR_APPROVAL = "WAITING_FOR_APPROVAL"
    TIMED_OUT = "TIMED_OUT"
    CORRECTING = "CORRECTING"


class PlannedStep(BaseModel):
    """A single scheduled step in the Master Pipeline execution sequence."""

    step_id: str = Field(default_factory=lambda: str(uuid4()))
    agent_name: str = Field(..., description="Canonical agent identifier (e.g., 'strategy_agent')")
    stage_order: int = Field(..., description="1-based stage order in the frozen Master Pipeline sequence")
    display_name: str = Field(..., description="Human-readable stage title")
    is_optional: bool = Field(default=False, description="Whether this step can be skipped safely")
    dependencies: List[str] = Field(default_factory=list, description="Step IDs or agent names required prior to execution")
    required_tools: List[str] = Field(default_factory=list, description="Tools required for this agent (e.g. 'qdrant_rag', 'web_search')")
    required_models: List[str] = Field(default_factory=list, description="Models utilized (e.g. 'gpt-4o', 'claude-3-5-sonnet')")
    expected_outputs: List[str] = Field(default_factory=list, description="Attributes produced on CampaignContext")
    timeout_seconds: float = Field(default=30.0, ge=1.0, description="Execution timeout ceiling in seconds")
    max_retries: int = Field(default=3, ge=0, description="Maximum retry attempts on failure")
    validation_point: Optional[str] = Field(default=None, description="Quality gate rule evaluated post-execution")
    approval_point: bool = Field(default=False, description="Whether human approval is required before proceeding")
    
    # Execution Tracking State
    state: WorkflowState = Field(default=WorkflowState.PENDING, description="Current lifecycle state of this step")
    attempts: int = Field(default=0, description="Number of execution attempts made")
    error_message: Optional[str] = Field(default=None, description="Error detail if failed or timed out")
    started_at: Optional[str] = Field(default=None, description="ISO timestamp when execution started")
    finished_at: Optional[str] = Field(default=None, description="ISO timestamp when execution concluded")
    output_snapshot: Optional[Dict[str, Any]] = Field(default=None, description="Summary telemetry of output")


class ExecutionPlan(BaseModel):
    """Structured execution plan produced by the Planner for orchestrating the Master Pipeline."""

    plan_id: str = Field(default_factory=lambda: str(uuid4()))
    campaign_id: str = Field(..., description="Associated campaign identifier")
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    product_type: ProductType = Field(..., description="Classified product type")
    execution_mode: ExecutionMode = Field(..., description="Determined marketing execution mode")
    
    # The Frozen Master Pipeline Sequence
    agent_sequence: List[PlannedStep] = Field(
        ..., min_length=1, description="Ordered steps strictly adhering to the Master Pipeline"
    )
    
    # Governance & Context Summaries
    validation_points: List[str] = Field(default_factory=list, description="Global validation rules")
    approval_points: List[str] = Field(default_factory=list, description="Checkpoints requiring human sign-off")
    rag_context_summary: Optional[str] = Field(default=None, description="Summary of RAG knowledge retrieved")
    memory_context_summary: Optional[str] = Field(default=None, description="Summary of conversational/historical memory")
    
    # Overall Plan State
    status: WorkflowState = Field(default=WorkflowState.PENDING, description="Overall execution status")
    current_step_index: int = Field(default=0, description="Index of the currently active step")
    total_steps: int = Field(default=0, description="Total planned steps count")
    completed_steps: int = Field(default=0, description="Count of successfully executed or skipped steps")
    failed_steps: int = Field(default=0, description="Count of failed steps")

    def model_post_init(self, __context: Any) -> None:
        if self.agent_sequence and self.total_steps == 0:
            self.total_steps = len(self.agent_sequence)
