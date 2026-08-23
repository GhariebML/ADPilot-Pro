# 17 — Security, Compliance & Governance

## 1. Enterprise Security Architecture
ADPilot Pro incorporates defense-in-depth security principles across all layers:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          DEFENSE-IN-DEPTH SECURITY                          │
│                                                                             │
│  [INGRESS] ──> CORS Whitelist ──> JWT Auth Token ──> RBAC Gate              │
│                                                          │                  │
│  [RUNTIME] ──> Pydantic Schema Validation <──────────────┘                  │
│                    │                                                        │
│                    ▼                                                        │
│  [PROMPT]  ──> Prompt Injection Sanitization & Guardrails                   │
│                    │                                                        │
│                    ▼                                                        │
│  [GOVERN]  ──> Hard Boundary Constraints (Budget Caps, Blacklists)          │
│                    │                                                        │
│                    ▼                                                        │
│  [AUDIT]   ──> Cryptographic Audit Log Event Ledger                         │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Governance Controls
1. **Zero Hardcoded Secrets:** All API keys (`GEMINI_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`) are managed exclusively via environment variables and loaded through `.env`.
2. **Role-Based Access Control (RBAC):** `ADMIN` (full pipeline config & policy modification), `OPERATOR` (campaign trigger & HITL approvals), `VIEWER` (read-only telemetry).
3. **Audit Ledger:** Every agent action, LLM invocation token count, and human approval decision is immutably logged with UTC timestamps in `AuditLog`.
