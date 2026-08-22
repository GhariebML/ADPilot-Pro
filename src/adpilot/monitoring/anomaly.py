"""Anomaly detection and goal deviation evaluation engine."""

from __future__ import annotations

import logging
from typing import List

from ..schemas.agent_schemas import CampaignContext
from .schemas import (
    AlertSeverity,
    AnomalyType,
    MonitoringEvent,
    PerformanceSnapshot,
)

logger = logging.getLogger(__name__)


class AnomalyDetector:
    """Detects statistical anomalies, KPI degradation, and constraint violations from live telemetry."""

    @staticmethod
    def detect_anomalies(
        context: CampaignContext,
        snapshot: PerformanceSnapshot,
    ) -> List[MonitoringEvent]:
        """Evaluates a PerformanceSnapshot against target KPIs and constraints, returning structured MonitoringEvents."""
        events: List[MonitoringEvent] = []
        campaign_id = context.campaign_id

        # 1. Target KPI baselines
        target_ctr = (getattr(context.kpis, "target_ctr", None) or 2.5) if hasattr(context, "kpis") and context.kpis else 2.5
        target_ctr_ratio = (target_ctr / 100.0) if (target_ctr is not None and target_ctr > 0.5) else (target_ctr or 0.025)
        target_cpa = (getattr(context.kpis, "target_cpa", None) or 50.0) if hasattr(context, "kpis") and context.kpis else 50.0
        target_roas = (getattr(context.kpis, "target_roas", None) or 3.0) if hasattr(context, "kpis") and context.kpis else 3.0

        # Constraints
        max_cpa = getattr(context.constraints, "max_cpa", None) if hasattr(context, "constraints") and context.constraints else None
        min_roas = getattr(context.constraints, "min_roas", None) if hasattr(context, "constraints") and context.constraints else None

        # -------------------------------------------------------------------
        # 1. CTR Evaluation (Content & Copy Weakness)
        # -------------------------------------------------------------------
        observed_ctr = snapshot.ctr
        ctr_dev = (observed_ctr - target_ctr_ratio) / target_ctr_ratio if target_ctr_ratio > 0 else 0.0
        
        if ctr_dev < -0.40:
            events.append(
                MonitoringEvent(
                    campaign_id=campaign_id,
                    metric="ctr",
                    value=round(observed_ctr * 100, 2),
                    expected_value=round(target_ctr_ratio * 100, 2),
                    deviation=round(ctr_dev, 4),
                    severity=AlertSeverity.CRITICAL,
                    anomaly_type=AnomalyType.CTR_DROP,
                    description=f"Critical CTR drop: Observed {observed_ctr*100:.2f}% vs target {target_ctr_ratio*100:.2f}% (Deviation: {ctr_dev*100:.1f}%)",
                    target_agent="content_agent",
                )
            )
        elif ctr_dev < -0.20:
            events.append(
                MonitoringEvent(
                    campaign_id=campaign_id,
                    metric="ctr",
                    value=round(observed_ctr * 100, 2),
                    expected_value=round(target_ctr_ratio * 100, 2),
                    deviation=round(ctr_dev, 4),
                    severity=AlertSeverity.WARNING,
                    anomaly_type=AnomalyType.CTR_DROP,
                    description=f"Moderate CTR underperformance: Observed {observed_ctr*100:.2f}% vs target {target_ctr_ratio*100:.2f}%",
                    target_agent="content_agent",
                )
            )
        else:
            events.append(
                MonitoringEvent(
                    campaign_id=campaign_id,
                    metric="ctr",
                    value=round(observed_ctr * 100, 2),
                    expected_value=round(target_ctr_ratio * 100, 2),
                    deviation=round(ctr_dev, 4),
                    severity=AlertSeverity.INFO,
                    description=f"Nominal CTR performance ({observed_ctr*100:.2f}%)",
                )
            )

        # -------------------------------------------------------------------
        # 2. CPA Evaluation (Optimizer / Strategy Bidding & Targeting)
        # -------------------------------------------------------------------
        observed_cpa = snapshot.cpa
        cpa_dev = (observed_cpa - target_cpa) / target_cpa if target_cpa > 0 else 0.0

        if max_cpa is not None and observed_cpa > max_cpa:
            events.append(
                MonitoringEvent(
                    campaign_id=campaign_id,
                    metric="cpa",
                    value=observed_cpa,
                    expected_value=target_cpa,
                    deviation=round(cpa_dev, 4),
                    severity=AlertSeverity.CRITICAL,
                    anomaly_type=AnomalyType.CPA_SPIKE,
                    description=f"Critical CPA spike: Observed ${observed_cpa:.2f} breached max constraint ${max_cpa:.2f} (Target: ${target_cpa:.2f})",
                    target_agent="optimization_agent",
                )
            )
        elif cpa_dev > 0.30:
            events.append(
                MonitoringEvent(
                    campaign_id=campaign_id,
                    metric="cpa",
                    value=observed_cpa,
                    expected_value=target_cpa,
                    deviation=round(cpa_dev, 4),
                    severity=AlertSeverity.WARNING,
                    anomaly_type=AnomalyType.CPA_SPIKE,
                    description=f"Elevated CPA: Observed ${observed_cpa:.2f} vs target ${target_cpa:.2f} (+{cpa_dev*100:.1f}%)",
                    target_agent="optimization_agent",
                )
            )
        else:
            events.append(
                MonitoringEvent(
                    campaign_id=campaign_id,
                    metric="cpa",
                    value=observed_cpa,
                    expected_value=target_cpa,
                    deviation=round(cpa_dev, 4),
                    severity=AlertSeverity.INFO,
                    description=f"Nominal CPA (${observed_cpa:.2f})",
                )
            )

        # -------------------------------------------------------------------
        # 3. ROAS Evaluation (Overall Revenue / Strategy Efficiency)
        # -------------------------------------------------------------------
        observed_roas = snapshot.roas
        roas_dev = (observed_roas - target_roas) / target_roas if target_roas > 0 else 0.0

        if min_roas is not None and observed_roas < min_roas:
            events.append(
                MonitoringEvent(
                    campaign_id=campaign_id,
                    metric="roas",
                    value=observed_roas,
                    expected_value=target_roas,
                    deviation=round(roas_dev, 4),
                    severity=AlertSeverity.CRITICAL,
                    anomaly_type=AnomalyType.ROAS_DROP,
                    description=f"Critical ROAS drop: Observed {observed_roas:.2f}x breached min constraint {min_roas:.2f}x (Target: {target_roas:.2f}x)",
                    target_agent="strategy_agent",
                )
            )
        elif roas_dev < -0.25:
            events.append(
                MonitoringEvent(
                    campaign_id=campaign_id,
                    metric="roas",
                    value=observed_roas,
                    expected_value=target_roas,
                    deviation=round(roas_dev, 4),
                    severity=AlertSeverity.WARNING,
                    anomaly_type=AnomalyType.ROAS_DROP,
                    description=f"Sub-optimal ROAS: Observed {observed_roas:.2f}x vs target {target_roas:.2f}x",
                    target_agent="strategy_agent",
                )
            )
        else:
            events.append(
                MonitoringEvent(
                    campaign_id=campaign_id,
                    metric="roas",
                    value=observed_roas,
                    expected_value=target_roas,
                    deviation=round(roas_dev, 4),
                    severity=AlertSeverity.INFO,
                    description=f"Nominal ROAS ({observed_roas:.2f}x)",
                )
            )

        logger.info(
            "AnomalyDetector | Campaign %s evaluated: %d total events (%d anomalies flagged)",
            campaign_id,
            len(events),
            sum(1 for e in events if e.severity in [AlertSeverity.WARNING, AlertSeverity.CRITICAL]),
        )
        return events
