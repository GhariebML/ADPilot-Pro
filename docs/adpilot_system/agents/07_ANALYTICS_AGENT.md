# Analytics Agent

## 1. Purpose
The **Analytics Agent** evaluates generated campaign packages, predicts critical financial metrics (blended Return on Ad Spend [ROAS], Customer Acquisition Cost [CAC], Click-Through Rate [CTR], Conversion Rate [CVR]), and scores overall campaign quality.

## 2. Business Responsibility
Acts as the financial and statistical safety check of the pipeline, ensuring that expected marketing returns justify media spend allocations before budget is committed.

## 3. Technical Responsibility
Ingests complete campaign assets, extracts numerical and TF-IDF feature vectors, executes multi-target Scikit-Learn Ridge regression inference, and outputs `AnalyticsAgentOutput`.

## 4. Source Code
- `src/adpilot/agents/analytics_agent.py`
- Model Artifact: `research/models/analytics/revenue_forecaster.pkl`
- Scaler Artifact: `research/models/analytics/feature_scaler.pkl`

## 5. Input
- **Schema:** `ContentAgentOutput` + `DesignAgentOutput` + `CampaignContext`
  - Total Allocated Budget ($)
  - Number of ad variants
  - Headline sentiment and length
  - Channel selection distribution

## 6. Processing Flow
1. Extract 12-dimensional continuous feature vector from context and content copy.
2. Normalize features using pre-trained `StandardScaler`.
3. Execute multi-target Ridge regression predicting:
   $$\hat{\mathbf{y}} = \mathbf{X} \mathbf{W}^T + \mathbf{b} \quad \text{where } \mathbf{y} = [\text{ROAS}, \text{CAC}, \text{CVR}]$$
4. Compute composite Campaign Health Score ($0 - 100$).
5. Emit `AnalyticsAgentOutput`.

## 7. Models Used
- **Classical ML Model:** Scikit-Learn Multi-Target Ridge Regressor ($R^2 = 0.894$).
- **Inference Latency:** `2.1ms`.

## 8. Tools Used
- Model Loader Service (`src/adpilot/services/model_loader.py`)

## 9. Output
- **Schema:** `AnalyticsAgentOutput`
  - `predicted_roas: float` (e.g., 4.12x)
  - `predicted_cac: float` (e.g., $38.40)
  - `predicted_cvr: float` (e.g., 3.8%)
  - `health_score: float` (0 - 100)
  - `channel_roas_breakdown: Dict[str, float]`
  - `optimization_hints: List[str]`

## 10. Downstream Consumers
- `OptimizationAgent` (uses predicted returns to guide PPO budget shifts)
- `CorrectionEngine` (triggers remediation if health score $< 70$)
- `ExecutiveDashboard` (renders financial projection charts)

## 11. Error Handling
- Safe fallback heuristics if model weights cannot be loaded from disk.

## 12. Validation
- Range validation: $\text{ROAS} \in [0.5, 20.0]$, $\text{HealthScore} \in [0.0, 100.0]$.

## 13. Corrective Actions
- Flags campaigns with $\text{ROAS} < 2.0\text{x}$ to trigger automatic copywriting revisions.

## 14. Human-in-the-Loop
- Displays projected metrics on the Executive Dashboard for growth team sign-off.

## 15. Example Execution
```json
{
  "predicted_roas": 4.12,
  "predicted_cac": 38.40,
  "predicted_cvr": 0.038,
  "health_score": 94.5,
  "channel_roas_breakdown": {
    "LINKEDIN": 4.82,
    "META": 3.95,
    "GOOGLE_SEARCH": 3.65
  },
  "optimization_hints": ["Rebalance +12% budget into LinkedIn to capture high-margin B2B ROAS."]
}
```

## 16. Implementation Status
[IMPLEMENTED]
