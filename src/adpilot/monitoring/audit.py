"""Audit logger for Monitoring Agent events and health snapshots."""

from __future__ import annotations

import logging
from typing import Optional

from ..hitl.audit import HITLAuditStore
from ..hitl.schemas import ApprovalStage, HITLAuditRecord, HumanDecisionType
from .schemas import MonitoringReport

logger = logging.getLogger(__name__)


class MonitoringAuditLogger:
    """Records monitoring summaries and anomaly events to the audit journal."""

    def __init__(self, hitl_audit_store: Optional[HITLAuditStore] = None) -> None:
        self.audit_store = hitl_audit_store or HITLAuditStore()

    def log_monitoring_report(self, report: MonitoringReport) -> None:
        """Persists a structured audit record for the monitoring evaluation."""
        audit_record = HITLAuditRecord(
            user="monitoring_agent",
            campaign_id=report.campaign_id,
            stage=ApprovalStage.PUBLISHING,
            agent="monitoring_agent",
            decision=HumanDecisionType.APPROVE if report.health_score >= 70.0 else HumanDecisionType.REQUEST_REVISION,
            reason=f"Monitoring completed: Health {report.health_score:.1f}/100, Stream: {report.stream_status}, {len(report.alerts)} alerts.",
            previous_output={},
            modified_output={
                "health_score": report.health_score,
                "stream_status": report.stream_status,
                "alerts_count": len(report.alerts),
                "events_count": len(report.events),
                "goal_deviations": report.goal_deviations,
                "observed_kpis": report.observed_kpis,
            },
        )
        self.audit_store.record_decision(audit_record)
        logger.info(
            "MonitoringAuditLogger | Recorded monitoring audit for campaign %s (Health: %.1f/100)",
            report.campaign_id,
            report.health_score,
        )
