# Campaign Optimization Loop

**Status:** [IMPLEMENTED]  
**Components:** `OptimizationAgent`, `AnalyticsAgent`, `ClosedLoopFeedbackEngine`  

---

## 1. Closed-Loop Optimization Architecture

```mermaid
graph LR
    LiveCampaign[Active Ad Networks] -->|Hourly Spend, Impressions, Conversions| Monitoring[Monitoring Agent]
    Monitoring -->|Z-Score Deviation Event| Feedback[Feedback Engine]
    Feedback -->|Construct Experience Tuple (s, a, r, s')| Buffer[(PyTorch Replay Buffer)]
    Buffer -->|PPO Mini-Batch Update| Policy[PPO Policy Network ppo_policy.pt]
    Policy -->|New Budget Allocations a_t+1| Optimizer[Optimization Agent]
    Optimizer -->|Targeted Capital Shift| Publishing[Publishing Agent Updates Live Spend]
```

---

## 2. Real-Time Intervention Triggers
1. **CAC Escalation:** If live $\text{CAC} > 1.4 \times \text{ForecastedCAC}$, spend on that channel is throttled by $15\%$.
2. **ROAS Outperformance:** If a channel demonstrates $\text{ROAS} > 4.5\text{x}$, PPO reallocates surplus capital up to the Dirichlet safety limit.
3. **Ad Fatigue Decay:** If CTR drops $> 35\%$ over 72 hours, auto-triggers copy variant rotation.
