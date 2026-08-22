"""Publishing Audit Logger."""

from __future__ import annotations

import logging
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from ..hitl.audit import HITLAuditStore, audit_store
from ..hitl.schemas import ApprovalStage, HITLAuditRecord, HumanDecisionType
from .schemas import PublishingReceipt, PublishingReport

logger = logging.getLogger(__name__)


class PublishingAuditLogger:
    """Records full operational audit lineage for every campaign dispatch."""

    def __init__(self, hitl_audit_store: Optional[HITLAuditStore] = None) -> None:
        self.store = hitl_audit_store or audit_store

    def log_dispatch(
        self,
        receipt: PublishingReceipt,
        user: str = "publishing_agent",
        db_session: Optional[AsyncSession] = None,
    ) -> None:
        """Records an individual channel publishing receipt."""
        audit_record = HITLAuditRecord(
            user=user,
            campaign_id=receipt.campaign_id,
            stage=ApprovalStage.PUBLISHING,
            agent="publishing_agent",
            decision=HumanDecisionType.APPROVE if receipt.status.value in ["published", "dry_run_published"] else HumanDecisionType.REJECT,
            previous_output={},
            modified_output={
                "channel": receipt.channel.value,
                "provider": receipt.provider.value,
                "platform_post_id": receipt.platform_post_id,
                "status": receipt.status.value,
                "is_dry_run": receipt.is_dry_run,
                "attempts": receipt.attempts,
                "idempotency_key": receipt.idempotency_key,
            },
            reason=f"Publishing dispatch to {receipt.channel.value} ({'SAFE DRY-RUN' if receipt.is_dry_run else 'LIVE'}): status={receipt.status.value}",
            metadata=receipt.metadata,
        )
        self.store.record_decision(audit_record)

    def log_report(
        self,
        report: PublishingReport,
        user: str = "publishing_agent",
    ) -> None:
        """Records summary publishing report."""
        logger.info(
            "PublishingAuditLogger | Campaign %s published (%d/%d channels successful, Mode: %s)",
            report.campaign_id,
            report.successful_dispatches,
            report.total_channels,
            report.execution_mode.value,
        )
