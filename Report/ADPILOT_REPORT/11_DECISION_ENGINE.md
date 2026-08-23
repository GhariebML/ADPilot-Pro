# 11 — The Decision Engine & Policy Synthesis

## 1. Multi-Criteria Decision Synthesis
The ADPilot Decision Engine is the central deterministic arbitration layer that converts heterogeneous outputs from agents, custom ML models, PPO policies, and risk boundaries into an actionable campaign decision.

```
Agent Strategic Briefs
         │
ML Predictive Forecasts (CTR, ROAS)
         │
PPO Policy Reallocations
         │
CV Quality & Safety Audits
         │
         ▼
┌──────────────────────────────────────────────────────────────────┐
│                   DETERMINISTIC DECISION ENGINE                  │
│                                                                  │
│  1. Check Hard Governance Constraints (Budget Caps, Blacklists)  │
│  2. Evaluate Quality Gates (Aesthetic >= 8.5, Contrast >= AAA)  │
│  3. Calculate Risk Index: R = w_1(Var) + w_2(Spend) + w_3(Delta) │
└──────────────────────────────────┬───────────────────────────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    ▼                             ▼
       Risk Score <= Threshold         Risk Score > Threshold
                    │                             │
                    ▼                             ▼
         [APPROVED FOR DISPATCH]       [ROUTE TO HUMAN REVIEW GATE]
```

---

## 2. Decision Logic & Failure Recovery
1. **Rule Evaluation:** If any quality gate fails (e.g. Creative Evaluator score $< 7.0$), the Decision Engine halts deployment and routes targeted corrective feedback back to the originating agent.
2. **Correction Routing:** Strategy and Content agents re-execute with explicit revision directives, iterating up to 3 times before requiring human escalation.
3. **Execution Safety:** No campaign modification exceeding $20\%$ budget variance can execute without explicit cryptographic human approval.
