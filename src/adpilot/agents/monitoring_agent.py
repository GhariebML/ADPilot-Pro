"""Phase 14 — Enterprise Monitoring Agent."""

from __future__ import annotations

import logging
import time
from typing import List, Optional

from ..core.agent_events import AgentEventType, AgentLifecycleEvent, event_bus
from ..core.base_agent import BaseAgent
from ..core.contract_registry import MONITORING_AGENT_CONTRACT
from ..monitoring.anomaly import AnomalyDetector
from ..monitoring.audit import MonitoringAuditLogger
from ..monitoring.health import HealthEvaluator
from ..monitoring.schemas import (
    AlertSeverity,
    MonitoringReport,
    PerformanceSnapshot,
    RawTelemetryPoint,
)
from ..monitoring.telemetry import TelemetryIngestionEngine
from ..schemas.agent_schemas import (
    AnomalyEvent,
    CampaignContext,
    MonitoringInput,
    MonitoringOutput,
)

logger = logging.getLogger(__name__)


class MonitoringAgent(BaseAgent[MonitoringInput, MonitoringOutput]):
    """Monitoring Agent responsible for real-time telemetry streaming, anomaly detection, and closed-loop feedback."""

    name = "monitoring_agent"
    input_model = MonitoringInput
    output_model = MonitoringOutput
    contract = MONITORING_AGENT_CONTRACT

    def __init__(
        self,
        telemetry_engine: Optional[TelemetryIngestionEngine] = None,
        anomaly_detector: Optional[AnomalyDetector] = None,
        health_evaluator: Optional[HealthEvaluator] = None,
        audit_logger: Optional[MonitoringAuditLogger] = None,
    ) -> None:
        super().__init__()
        self.telemetry_engine = telemetry_engine or TelemetryIngestionEngine()
        self.anomaly_detector = anomaly_detector or AnomalyDetector()
        self.health_evaluator = health_evaluator or HealthEvaluator()
        self.audit_logger = audit_logger or MonitoringAuditLogger()
        self.last_report: Optional[MonitoringReport] = None

    async def run(
        self,
        context: CampaignContext,
        raw_telemetry: Optional[List[RawTelemetryPoint]] = None,
    ) -> CampaignContext:
        """Runs telemetry normalization, anomaly detection, health scoring, and closed-loop feedback generation."""
        campaign_id = context.campaign_id
        start_time = time.time()

        event_bus.emit(
            AgentLifecycleEvent(
                event_type=AgentEventType.AGENT_STARTED,
                agent_id=self.name,
                campaign_id=campaign_id,
                status="started",
            )
        )

        logger.info("MonitoringAgent | Commencing telemetry evaluation for campaign %s", campaign_id)

        try:
            # 1. Telemetry Ingestion & Normalization
            if raw_telemetry is None or len(raw_telemetry) == 0:
                raw_points = self.telemetry_engine.generate_simulated_stream_points(context)
            else:
                raw_points = raw_telemetry

            snapshot: PerformanceSnapshot = self.telemetry_engine.normalize_telemetry_points(
                campaign_id=campaign_id,
                points=raw_points,
            )

            # 2. Statistical Anomaly & Goal Deviation Detection
            monitoring_events = self.anomaly_detector.detect_anomalies(context, snapshot)

            # 3. Campaign Health Scoring & Prescriptive Alert Routing
            health_score, stream_status, alerts, agent_feedback = self.health_evaluator.evaluate_campaign_health(
                monitoring_events
            )

            # 4. Assemble Goal Deviations & Observed KPIs
            goal_deviations = {
                ev.metric: ev.deviation for ev in monitoring_events if ev.severity != AlertSeverity.INFO
            }
            observed_kpis = {
                "ctr": snapshot.ctr,
                "cpa": snapshot.cpa,
                "roas": snapshot.roas,
                "cpc": snapshot.cpc,
                "conversion_rate": snapshot.conversion_rate,
            }

            # 5. Build Comprehensive Monitoring Report
            report = MonitoringReport(
                campaign_id=campaign_id,
                health_score=health_score,
                stream_status=stream_status,
                snapshots=[snapshot],
                events=monitoring_events,
                alerts=alerts,
                goal_deviations=goal_deviations,
                agent_feedback=agent_feedback,
                observed_kpis=observed_kpis,
                summary=f"Monitoring: Health {health_score:.1f}/100 ({stream_status}), {len(alerts)} alerts generated.",
            )
            self.last_report = report

            # 6. Record Audit Journal
            self.audit_logger.log_monitoring_report(report)

            # 7. Construct Canonical MonitoringOutput for CampaignContext
            canonical_anomalies = [
                AnomalyEvent(
                    metric=ev.metric,
                    observed_value=ev.value,
                    expected_range=f"{ev.expected_value:.2f}",
                    severity=ev.severity.value,
                    description=ev.description,
                )
                for ev in monitoring_events
                if ev.severity in [AlertSeverity.WARNING, AlertSeverity.CRITICAL, AlertSeverity.FATAL]
            ]

            output = MonitoringOutput(
                telemetry_stream_active=True,
                live_impressions=snapshot.impressions,
                live_clicks=snapshot.clicks,
                live_spend_usd=snapshot.spend,
                live_conversions=snapshot.conversions,
                detected_anomalies=canonical_anomalies,
                stream_status=stream_status,
                feedback_payload={
                    "campaign_id": campaign_id,
                    "health_score": health_score,
                    "stream_status": stream_status,
                    "alerts": alerts,
                    "agent_feedback": agent_feedback,
                    "goal_deviations": goal_deviations,
                    "observed_kpis": observed_kpis,
                    "events": [ev.model_dump() for ev in monitoring_events],
                    "snapshot": snapshot.model_dump(),
                },
            )

            context.monitoring = output
            context.record_agent_output("monitoring_agent", output)

            latency = time.time() - start_time
            event_bus.emit(
                AgentLifecycleEvent(
                    event_type=AgentEventType.AGENT_COMPLETED,
                    agent_id=self.name,
                    campaign_id=campaign_id,
                    status="completed",
                    latency=latency,
                    metadata={"health_score": health_score, "stream_status": stream_status, "alerts_count": len(alerts)},
                )
            )

            logger.info(
                "MonitoringAgent | Completed monitoring for %s (Health: %.1f/100, Status: %s)",
                campaign_id,
                health_score,
                stream_status,
            )
            return context

        except Exception as exc:
            latency = time.time() - start_time
            event_bus.emit(
                AgentLifecycleEvent(
                    event_type=AgentEventType.AGENT_FAILED,
                    agent_id=self.name,
                    campaign_id=campaign_id,
                    status="failed",
                    error_message=str(exc),
                    latency=latency,
                )
            )
            logger.error("MonitoringAgent | Failed during evaluation of campaign %s: %s", campaign_id, exc)
            raise
