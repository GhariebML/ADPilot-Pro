"""Phase 13 — Publishing Agent Typed Schemas."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4
from pydantic import BaseModel, Field

from ..schemas.agent_schemas import MarketingChannel


class PublishingStatus(str, Enum):
    """Lifecycle statuses for campaign dispatch."""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    VALIDATING = "validating"
    PUBLISHING = "publishing"
    PUBLISHED = "published"
    DRY_RUN_PUBLISHED = "dry_run_published"
    FAILED = "failed"
    REJECTED_UNAPPROVED = "rejected_unapproved"
    DUPLICATE_IGNORED = "duplicate_ignored"


class ProviderType(str, Enum):
    """Supported external advertising and distribution providers."""
    META = "meta"
    GOOGLE_ADS = "google_ads"
    LINKEDIN = "linkedin"
    BUFFER = "buffer"
    EMAIL_MAILCHIMP = "email_mailchimp"
    MOCK_DRY_RUN = "mock_dry_run"


class ExecutionMode(str, Enum):
    """Operational mode for the publishing engine."""
    LIVE = "live"
    DRY_RUN = "dry_run"


class PublishingValidationResult(BaseModel):
    """Pre-flight quality and approval validation outcomes."""
    is_valid: bool = Field(..., description="Whether pre-flight verification passed")
    approvals_verified: bool = Field(default=False, description="Whether required HITL approvals exist")
    assets_verified: bool = Field(default=False, description="Whether headlines and body copy are non-empty")
    strategy_verified: bool = Field(default=False, description="Whether strategy & positioning are defined")
    optimizer_actions_verified: bool = Field(default=False, description="Whether RL optimizer actions passed safety checks")
    validation_errors: List[str] = Field(default_factory=list, description="Critical blocking reasons")
    warnings: List[str] = Field(default_factory=list, description="Non-blocking observations")


class PublishingPayload(BaseModel):
    """Channel-specific prepared payload for external adapter dispatch."""
    campaign_id: str = Field(..., description="Target campaign identifier")
    channel: MarketingChannel = Field(..., description="Target distribution channel")
    provider: ProviderType = Field(..., description="Target adapter provider")
    headlines: List[str] = Field(default_factory=list, description="Ad headlines")
    primary_copy: str = Field(..., description="Primary promotional narrative")
    ctas: List[str] = Field(default_factory=list, description="Call to action strings")
    target_audience: Dict[str, Any] = Field(default_factory=dict, description="Targeting parameters")
    budget_allocation: float = Field(default=0.0, description="Allocated spend for this channel")
    bid_multiplier: float = Field(default=1.0, description="Optimizer bid multiplier")
    utm_parameters: Dict[str, str] = Field(default_factory=dict, description="Tracking parameters")
    creative_asset_urls: List[str] = Field(default_factory=list, description="Visual assets")
    scheduled_for: Optional[str] = Field(default=None, description="ISO timestamp for future publication")
    idempotency_key: str = Field(..., description="Unique deterministic hash preventing duplicate publish")


class PublishingReceipt(BaseModel):
    """Immutable dispatch receipt returned by an adapter."""
    receipt_id: str = Field(default_factory=lambda: f"rcpt-{uuid4().hex[:10]}")
    campaign_id: str = Field(..., description="Campaign identifier")
    channel: MarketingChannel = Field(..., description="Target channel")
    provider: ProviderType = Field(..., description="Provider adapter utilized")
    status: PublishingStatus = Field(..., description="Final dispatch status")
    is_dry_run: bool = Field(default=True, description="Flag indicating whether this was a dry-run execution")
    platform_post_id: Optional[str] = Field(default=None, description="External platform object ID")
    published_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    scheduled_for: Optional[str] = Field(default=None, description="Scheduled time if delayed")
    attempts: int = Field(default=1, description="Number of dispatch attempts")
    idempotency_key: str = Field(..., description="Idempotency key associated with this dispatch")
    error_message: Optional[str] = Field(default=None, description="Error explanation if failed")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Provider response metadata")


class PublishingReport(BaseModel):
    """Aggregate report produced by the Publishing Agent."""
    campaign_id: str = Field(..., description="Campaign identifier")
    execution_mode: ExecutionMode = Field(default=ExecutionMode.DRY_RUN, description="Execution mode utilized")
    total_channels: int = Field(default=0, description="Total channels processed")
    successful_dispatches: int = Field(default=0, description="Successful live or dry-run publishes")
    failed_dispatches: int = Field(default=0, description="Failed dispatches")
    receipts: List[PublishingReceipt] = Field(default_factory=list, description="Receipts by channel")
    validation: Optional[PublishingValidationResult] = Field(default=None, description="Pre-flight validation scorecard")
    published_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    summary: str = Field(default="", description="Executive dispatch summary")
