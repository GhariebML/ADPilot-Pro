"""Telemetry ingestion and metric normalization engine."""

from __future__ import annotations

import logging
from typing import Dict, List

from ..schemas.agent_schemas import CampaignContext
from .schemas import PerformanceSnapshot, RawTelemetryPoint

logger = logging.getLogger(__name__)


class TelemetryIngestionEngine:
    """Ingests raw telemetry feeds and normalizes performance metrics across channels."""

    @staticmethod
    def normalize_telemetry_points(
        campaign_id: str,
        points: List[RawTelemetryPoint],
    ) -> PerformanceSnapshot:
        """Aggregates and normalizes a collection of raw telemetry points into a PerformanceSnapshot."""
        total_impressions = sum(p.impressions for p in points)
        total_clicks = sum(p.clicks for p in points)
        total_spend = sum(p.spend for p in points)
        total_conversions = sum(p.conversions for p in points)
        total_revenue = sum(p.revenue for p in points)

        # Standard Metric Normalization
        ctr = total_clicks / total_impressions if total_impressions > 0 else 0.0
        cpc = total_spend / total_clicks if total_clicks > 0 else 0.0
        cpa = total_spend / total_conversions if total_conversions > 0 else total_spend
        roas = total_revenue / total_spend if total_spend > 0 else 0.0
        conversion_rate = total_conversions / total_clicks if total_clicks > 0 else 0.0

        # Channel Breakdown
        channel_breakdown: Dict[str, Dict[str, float]] = {}
        for p in points:
            if p.channel not in channel_breakdown:
                channel_breakdown[p.channel] = {
                    "impressions": 0.0,
                    "clicks": 0.0,
                    "spend": 0.0,
                    "conversions": 0.0,
                    "revenue": 0.0,
                }
            channel_breakdown[p.channel]["impressions"] += float(p.impressions)
            channel_breakdown[p.channel]["clicks"] += float(p.clicks)
            channel_breakdown[p.channel]["spend"] += float(p.spend)
            channel_breakdown[p.channel]["conversions"] += float(p.conversions)
            channel_breakdown[p.channel]["revenue"] += float(p.revenue)

        # Calculate per-channel rates
        for ch, data in channel_breakdown.items():
            imps = data["impressions"]
            clks = data["clicks"]
            sp = data["spend"]
            conv = data["conversions"]
            rev = data["revenue"]
            data["ctr"] = clks / imps if imps > 0 else 0.0
            data["cpc"] = sp / clks if clks > 0 else 0.0
            data["cpa"] = sp / conv if conv > 0 else sp
            data["roas"] = rev / sp if sp > 0 else 0.0
            data["conversion_rate"] = conv / clks if clks > 0 else 0.0

        return PerformanceSnapshot(
            campaign_id=campaign_id,
            impressions=total_impressions,
            clicks=total_clicks,
            spend=round(total_spend, 2),
            conversions=total_conversions,
            revenue=round(total_revenue, 2),
            ctr=round(ctr, 4),
            cpc=round(cpc, 2),
            cpa=round(cpa, 2),
            roas=round(roas, 2),
            conversion_rate=round(conversion_rate, 4),
            channel_breakdown=channel_breakdown,
        )

    @classmethod
    def generate_simulated_stream_points(
        cls,
        context: CampaignContext,
        performance_multiplier: float = 1.0,
        inject_ctr_drop: bool = False,
        inject_cpa_spike: bool = False,
    ) -> List[RawTelemetryPoint]:
        """Generates deterministic simulated raw telemetry points matching campaign channels."""
        channels = [ch.value for ch in context.channels] if hasattr(context, "channels") and context.channels else ["linkedin"]
        points = []

        total_budget = getattr(context.budget, "total_budget", 5000.0) if hasattr(context, "budget") else 5000.0
        daily_spend = min(total_budget * 0.05, 500.0)

        for ch in channels:
            ch_spend = daily_spend / len(channels)
            base_impressions = int(ch_spend * 40 * performance_multiplier)
            base_clicks = int(base_impressions * (0.008 if inject_ctr_drop else 0.035) * performance_multiplier)
            base_conversions = max(0, int(base_clicks * (0.01 if inject_cpa_spike else 0.08) * performance_multiplier))
            base_revenue = round(base_conversions * (30.0 if inject_cpa_spike else 120.0), 2)

            point = RawTelemetryPoint(
                campaign_id=context.campaign_id,
                channel=ch,
                impressions=max(100, base_impressions),
                clicks=max(1, base_clicks),
                spend=round(ch_spend, 2),
                conversions=base_conversions,
                revenue=base_revenue,
            )
            points.append(point)

        return points
