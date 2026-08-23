# Appendix D — Database & Vector Storage Schema

## 1. Relational Database Schema (SQLAlchemy ORM)

```
┌────────────────────────────────┐       ┌────────────────────────────────┐
│          organizations         │       │             users              │
├────────────────────────────────┤       ├────────────────────────────────┤
│ id           VARCHAR(36) [PK]  │<──────│ id           VARCHAR(36) [PK]  │
│ name         VARCHAR(255)      │ 1   N │ email        VARCHAR(255)      │
│ slug         VARCHAR(255)      │       │ hashed_pwd   VARCHAR(255)      │
│ plan         VARCHAR(50)       │       │ role         VARCHAR(50)       │
│ created_at   DATETIME          │       │ org_id       VARCHAR(36) [FK]  │
└────────────────────────────────┘       └────────────────────────────────┘
                │ 1
                │
                │ N
┌────────────────────────────────┐       ┌────────────────────────────────┐
│           campaigns            │       │          audit_logs            │
├────────────────────────────────┤       ├────────────────────────────────┤
│ id           VARCHAR(36) [PK]  │       │ id           VARCHAR(36) [PK]  │
│ name         VARCHAR(255)      │       │ event_type   VARCHAR(100)      │
│ status       VARCHAR(50)       │       │ agent_id     VARCHAR(100)      │
│ budget       FLOAT             │       │ user_id      VARCHAR(36)       │
│ org_id       VARCHAR(36) [FK]  │       │ payload_json TEXT              │
│ created_at   DATETIME          │       │ timestamp    DATETIME          │
└────────────────────────────────┘       └────────────────────────────────┘
```

## 2. Vector Collection Schema (Qdrant)
* **Collection Name:** `adpilot_knowledge`
* **Vector Dimension:** 384 (FastEmbed `BAAI/bge-small-en-v1.5`)
* **Distance Metric:** Cosine Distance
* **Payload Structure:** `{"document_id": str, "title": str, "chunk_index": int, "content": str, "category": str}`
