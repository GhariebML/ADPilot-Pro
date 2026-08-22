# Monitoring Agent

## 1. Purpose
The **Monitoring Agent** ingests real-time advertising telemetry (impressions, clicks, conversions, spend), detects statistical anomalies (e.g., ad fatigue, sudden CAC spikes, budget drain), and emits closed-loop feedback events.

## 2. Business Responsibility
Protects company capital from rapid budget bleed, ad fatigue decay, and broken landing pages by continuously auditing live campaign performance against forecasted baselines.

## 3. Technical Responsibility
Polls live ad metrics, normalizes time-series signals, computes rolling statistical Z-scores against forecasted baselines, flags anomalies, and triggers closed-loop feedback events.

## 4. Source Code
- `src/adpilot/monitoring/telemetry.py`
- Anomaly Detector: `src/adpilot/monitoring/anomaly.py`
- Closed-Loop Router: `src/adpilot/monitoring/closed_loop.py`

## 5. Input
- Live metric stream (Hourly Spend, Impressions, Clicks, Leads)
- Forecasted Baselines from `AnalyticsAgentOutput`

## 6. Processing Flow
1. Ingest metric batch for active campaigns.
2. Normalize metrics:
   $$\text{CTR}_t = \frac{\text{Clicks}_t}{\text{Impressions}_t}, \quad \text{CAC}_t = \frac{\text{Spend}_t}{\text{Conversions}_t}$$
3. Compute anomaly Z-score against expected baseline $\mu$ and standard deviation $\sigma$:
   $$Z = \frac{x_t - \mu}{\sigma}$$
4. If $|Z| > 2.5$, trigger `AnomalyEvent` with severity (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`).
5. Route event to `ClosedLoopFeedbackEngine`.

## 7. Models Used
- Statistical Anomaly Detection (Rolling Z-Score & Moving Average).

## 8. Tools Used
- Telemetry Ingestion Service (`src/adpilot/monitoring/telemetry.py`)

## 9. Output
- **Schema:** `MonitoringEvent`
  - `campaign_id: str`
  - `timestamp: str`
  - `metric: str` (e.g., "CAC", "CTR", "ROAS")
  - `observed_value: float`
  - `expected_value: float`
  - `deviation_pct: float`
  - `severity: str` (`INFO`, `WARNING`, `CRITICAL`)
  - `recommended_action: str`

## 10. Downstream Consumers
- `FeedbackEngine` (updates RL replay buffer with real rewards)
- `CorrectionEngine` (pauses ads or triggers copy revisions)
- `ExecutiveDashboard` (displays real-time health alerts)

## 11. Error Handling
- Handles missing or delayed platform telemetry by imputing short-term rolling averages.

## 12. Validation
- Verifies that metric values are non-negative and timestamps are strictly monotonic.

## 13. Corrective Actions
- Automatically issues pause recommendations if spend exceeds $150\%$ of target without conversions.

## 14. Human-in-the-Loop
- Critical anomalies generate immediate alerts in the Live Activity Feed.

## 15. Example Execution
```json
{
  "campaign_id": "cmp-01",
  "timestamp": "2026-08-22T19:00:00Z",
  "metric": "CAC",
  "observed_value": 68.50,
  "expected_value": 38.40,
  "deviation_pct": 78.4,
  "severity": "WARNING",
  "recommended_action": "Shift spend from Meta to LinkedIn where CAC is stable at $42.10."
}
```

## 16. Implementation Status
[IMPLEMENTED]
