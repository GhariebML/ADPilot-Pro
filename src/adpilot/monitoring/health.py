"""Health score evaluation, alert generation, and agent feedback router."""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Tuple

from .schemas import AlertSeverity, MonitoringEvent

logger = logging.getLogger(__name__)


class HealthEvaluator:
    """Computes campaign health score (0-100), builds alerts, and routes prescriptive agent feedback."""

    @staticmethod
    def evaluate_campaign_health(
        events: List[MonitoringEvent],
    ) -> Tuple[float, str, List[Dict[str, Any]], Dict[str, List[str]]]:
        """Calculates health score, stream status, structured alerts, and agent feedback dictionary."""
        base_score = 100.0
        alerts: List[Dict[str, Any]] = []
        agent_feedback: Dict[str, List[str]] = {}

        for ev in events:
            if ev.severity == AlertSeverity.CRITICAL or ev.severity == AlertSeverity.FATAL:
                base_score -= 25.0
                alerts.append({
                    "metric": ev.metric,
                    "severity": ev.severity.value,
                    "description": ev.description,
                    "deviation": ev.deviation,
                    "observed": ev.value,
                    "expected": ev.expected_value,
                })
                if ev.target_agent:
                    if ev.target_agent not in agent_feedback:
                        agent_feedback[ev.target_agent] = []
                    agent_feedback[ev.target_agent].append(ev.description)

            elif ev.severity == AlertSeverity.WARNING:
                base_score -= 10.0
                alerts.append({
                    "metric": ev.metric,
                    "severity": ev.severity.value,
                    "description": ev.description,
                    "deviation": ev.deviation,
                    "observed": ev.value,
                    "expected": ev.expected_value,
                })
                if ev.target_agent:
                    if ev.target_agent not in agent_feedback:
                        agent_feedback[ev.target_agent] = []
                    agent_feedback[ev.target_agent].append(ev.description)

        health_score = max(0.0, min(100.0, round(base_score, 1)))

        if health_score >= 80.0:
            stream_status = "nominal"
        elif health_score >= 50.0:
            stream_status = "degraded"
        else:
            stream_status = "critical"

        logger.info(
            "HealthEvaluator | Health Score: %.1f/100, Stream Status: %s (%d alerts generated)",
            health_score,
            stream_status,
            len(alerts),
        )
        return health_score, stream_status, alerts, agent_feedback
