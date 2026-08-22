"""Typed Pydantic schemas for ADPilot Agent Contracts and Responsibility System."""

from __future__ import annotations

from typing import List
from pydantic import BaseModel, Field


class AgentIdentity(BaseModel):
    """Immutable identity specification for an ADPilot agent."""

    agent_id: str = Field(..., description="Unique machine-readable agent identifier (e.g. 'strategy_agent')")
    name: str = Field(..., description="Human-readable agent display name")
    version: str = Field(default="1.0.0", description="Semantic version of the agent contract")
    role: str = Field(..., description="Primary architectural role in the Master Pipeline")
    stage_order: int = Field(..., description="Order position in the frozen Master Pipeline sequence")


class AgentActionBoundary(BaseModel):
    """Explicit behavioral boundaries defining what an agent may and may NOT do."""

    allowed_actions: List[str] = Field(..., min_length=1, description="Explicit list of permitted actions")
    forbidden_actions: List[str] = Field(..., min_length=1, description="Explicit list of strictly prohibited actions")


class QualityCriteria(BaseModel):
    """Quality standards, evidence requirements, failure modes, and corrective actions."""

    success_criteria: List[str] = Field(..., min_length=1, description="Validation rules that must evaluate to True")
    failure_conditions: List[str] = Field(..., min_length=1, description="Conditions that trigger failure or retry")
    confidence_threshold: float = Field(default=0.70, ge=0.0, le=1.0, description="Minimum confidence required")
    evidence_requirements: List[str] = Field(..., min_length=1, description="Required audit traces and rationale")
    corrective_actions: List[str] = Field(..., min_length=1, description="Automated actions taken upon failure")


class AgentContract(BaseModel):
    """Complete executable contract defining an ADPilot Agent's runtime responsibility.

    Runtime authority must be represented in executable typed configuration/code,
    NEVER in Markdown files.
    """

    identity: AgentIdentity
    responsibilities: List[str] = Field(..., min_length=1, description="Detailed list of specific agent responsibilities")
    input_schema_name: str = Field(..., description="Canonical name of the Pydantic Input Schema model")
    output_schema_name: str = Field(..., description="Canonical name of the Pydantic Output Schema model")
    tools: List[str] = Field(default_factory=list, description="List of tools available to this agent")
    models: List[str] = Field(default_factory=list, description="Models utilized by this agent")
    boundaries: AgentActionBoundary
    dependencies: List[str] = Field(default_factory=list, description="Prerequisite agent IDs or context fields required")
    quality: QualityCriteria
