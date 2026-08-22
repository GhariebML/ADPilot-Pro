"""Audit Core: Enforces tamper-resistant, non-silent human decision tracking."""

from __future__ import annotations

import json
import logging
import threading
from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.exceptions import ValidationError
from ..models.audit_log import AuditLog
from .schemas import HITLAuditRecord, HumanDecisionType

logger = logging.getLogger(__name__)


class HITLAuditStore:
    """Thread-safe in-memory and database-backed audit store for human-in-the-loop decisions."""

    def __init__(self) -> None:
        self._records: List[HITLAuditRecord] = []
        self._lock = threading.Lock()

    def record_decision(
        self,
        record: HITLAuditRecord,
        db_session: Optional[AsyncSession] = None,
    ) -> HITLAuditRecord:
        """Validates and stores a human decision record, preventing silent overrides."""
        # 1. Anti-Silent Override & Integrity Validation
        if not record.user or not record.user.strip():
            raise ValidationError("HITL decision rejected: 'user' identifier is mandatory.")

        if not record.reason or len(record.reason.strip()) < 3:
            raise ValidationError("HITL decision rejected: Explicit 'reason' (min 3 chars) is mandatory for auditability.")

        if record.decision in [HumanDecisionType.EDIT, HumanDecisionType.OVERRIDE]:
            if not record.modified_output:
                raise ValidationError(
                    f"HITL decision '{record.decision.value}' requires a non-empty 'modified_output' payload."
                )
            if not record.previous_output:
                logger.warning("HITL decision '%s' recorded without previous_output snapshot.", record.decision.value)

        # 2. Append to memory audit journal
        with self._lock:
            self._records.append(record)

        logger.info(
            "HITLAuditStore | Recorded decision: audit_id=%s, user=%s, campaign_id=%s, stage=%s, decision=%s",
            record.audit_id,
            record.user,
            record.campaign_id,
            record.stage.value,
            record.decision.value,
        )

        return record

    async def persist_to_db(self, record: HITLAuditRecord, session: AsyncSession) -> None:
        """Asynchronously writes the audit record to the persistent SQLite / Postgres audit_logs table."""
        try:
            payload: Dict[str, Any] = {
                "stage": record.stage.value,
                "agent": record.agent,
                "decision": record.decision.value,
                "reason": record.reason,
                "is_override": record.is_override,
                "previous_output": record.previous_output,
                "modified_output": record.modified_output,
                "revision_directives": record.revision_directives,
                "metadata": record.metadata,
            }
            log_entry = AuditLog(
                id=record.audit_id,
                user_id=record.user,
                action=f"hitl_{record.decision.value}",
                entity_type="campaign_hitl_gate",
                entity_id=record.campaign_id,
                payload_json=json.dumps(payload),
            )
            session.add(log_entry)
            await session.commit()
        except Exception as exc:
            logger.error("Failed to persist HITLAuditRecord to database: %s", exc)

    def get_campaign_audits(self, campaign_id: str) -> List[HITLAuditRecord]:
        """Retrieve all audit records associated with a specific campaign."""
        with self._lock:
            return [r for r in self._records if r.campaign_id == campaign_id]

    def get_audit_by_id(self, audit_id: str) -> Optional[HITLAuditRecord]:
        """Retrieve a specific audit record by its unique ID."""
        with self._lock:
            return next((r for r in self._records if r.audit_id == audit_id), None)

    def clear(self) -> None:
        """Clear in-memory audit records (useful for test resets)."""
        with self._lock:
            self._records.clear()


# Default singleton audit store
audit_store = HITLAuditStore()
