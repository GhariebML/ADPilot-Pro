# 15 — Data & Storage Architecture

## 1. Heterogeneous Data Storage Model
ADPilot Pro segregates data across distinct storage engines according to access patterns, persistence guarantees, and query complexity.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ENTERPRISE DATA ARCHITECTURE                        │
│                                                                             │
│  ┌───────────────────────────┐ ┌────────────────────────┐ ┌───────────────┐ │
│  │   Relational Store        │ │   Vector Storage       │ │ File & Media  │ │
│  │   (PostgreSQL / SQLite)   │ │   (Qdrant Vector DB)   │ │ Asset Store   │ │
│  └─────────────┬─────────────┘ └───────────┬────────────┘ └───────┬───────┘ │
│                │                           │                      │         │
│  · User & Organization Auth    · 384-dim BGE Embeddings     · Generated PNG │
│  · Campaign Configurations     · Marketing Playbooks        · Visual SVGs   │
│  · Immutable Audit Logs        · Brand Voice Semantic Space · Model Weights │
│  · Pipeline Execution Records  · Historical Telemetry       │ (.pkl / .onnx)│
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Database Schema Entities
* **`User` Table:** Authentication credentials, roles (`ADMIN`, `OPERATOR`, `VIEWER`), and organization bindings.
* **`Organization` Table:** Multi-tenant workspace partitions and billing limits.
* **`Campaign` Table:** Active campaign parameters, budget constraints, target KPIs, and current DAG state.
* **`AuditLog` Table:** Cryptographically verifiable event ledger logging agent decisions, model invocations, and human approvals.
