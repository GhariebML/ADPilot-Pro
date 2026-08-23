# 12 — Human-in-the-Loop (HITL) Governance

## 1. Zero-Trust Autonomous Governance
In enterprise advertising systems where monetary budgets and brand reputation are at stake, autonomous agents must operate under bounded authority. ADPilot Pro implements an asynchronous Human-in-the-Loop (HITL) governance framework governed by `HITLApprovalCenter` in the frontend and `/api/v1/simulations/{id}/approve` endpoints on the backend.

```
                  ┌────────────────────────────────────────┐
                  │      AI Recommendation Generated       │
                  │   (e.g., PPO Budget Shift, New Copy)   │
                  └───────────────────┬────────────────────┘
                                      │
                                      ▼
                  ┌────────────────────────────────────────┐
                  │        Risk & Constraint Check         │
                  └───────────────────┬────────────────────┘
                                      │
                         ┌────────────┴────────────┐
                         ▼                         ▼
                  [Risk <= Low]             [Risk > Threshold]
                         │                         │
                         ▼                         ▼
                  Auto-Execute Action       HALT PIPELINE & TRIGGER HITL GATE
                                                   │
                                                   ▼
                                            Human Reviewer
                                            ├── [APPROVE] ──> Dispatch Action
                                            ├── [MODIFY]  ──> Inject Feedback
                                            └── [REJECT]  ──> Revert to Prior
```

---

## 2. HITL Trigger Conditions
A campaign state transitions to `REVIEW_REQUIRED` under 4 explicit conditions:
1. **PPO Budget Variance:** Proposed channel reallocation delta $\Delta b > 15\%$ of total spend.
2. **Quality Gate Marginal Pass:** Creative or copy quality score falls between acceptable and threshold ($7.0 \le \text{Score} < 8.5$).
3. **High-Risk Vertical:** Regulated industry classification (e.g. Healthcare, Financial Services).
4. **New Channel Ingress:** First deployment on an unverified advertising connector.
