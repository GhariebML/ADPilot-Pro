# Database Schema & Relational Models

**Status:** [IMPLEMENTED]  
**Database Engine:** SQLite (`data/adpilot.db`) / SQLAlchemy ORM / Pydantic v2  

---

## 1. Relational Entity Relationship (ER) Diagram

```mermaid
erDiagram
    CAMPAIGN_TASK ||--o{ DESIGN_ASSET : contains
    CAMPAIGN_TASK ||--o{ AUDIT_LOG : generates
    CAMPAIGN_TASK ||--o{ HITL_RECORD : requires
    ORGANIZATION ||--o{ USER : employs
    ORGANIZATION ||--o{ CAMPAIGN_TASK : owns

    CAMPAIGN_TASK {
        string task_id PK
        string product_name
        string status
        float budget
        string goals
        string raw_content_json
        string raw_design_json
        string raw_analytics_json
        datetime created_at
        datetime updated_at
    }

    DESIGN_ASSET {
        string asset_id PK
        string task_id FK
        string platform
        string aspect_ratio
        string image_url
        float aesthetic_score
        float contrast_ratio
    }

    AUDIT_LOG {
        string log_id PK
        string task_id FK
        string agent_name
        string action
        string status
        int latency_ms
        datetime timestamp
    }

    HITL_RECORD {
        string decision_id PK
        string task_id FK
        string stage
        string role
        string decision
        string signature_hash
        datetime timestamp
    }
```

---

## 2. Table Specifications (`src/adpilot/models/`)

| Table Name | Model File | Purpose |
|---|---|---|
| `campaign_tasks` | `campaign_task.py` | Stores full campaign brief, execution status, and final JSON deliverables |
| `design_assets` | `design_asset.py` | Stores rendered creatives, aspect ratios, image URLs, and CV quality scores |
| `audit_logs` | `audit_log.py` | Immutable time-series log of all agent runs, latencies, and tool calls |
| `hitl_records` | `hitl/schemas.py` | Cryptographically signed human approval/rejection decisions |
| `organizations` | `organization.py` | Multi-tenant organization boundaries and brand rule settings |
| `users` | `user.py` | User authentication, RBAC roles (`Director`, `Auditor`, `GrowthLead`) |
