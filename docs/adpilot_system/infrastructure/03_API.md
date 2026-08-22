# API Endpoints Specification

**Status:** [IMPLEMENTED]  
**Base URL:** `http://127.0.0.1:8001` (Dev/Prod default)  
**OpenAPI Spec:** `http://127.0.0.1:8001/docs`  

---

## 1. Complete Endpoints Table

| Method | Path | Request Body | Response Body | HTTP Codes | Description |
|---|---|---|---|---|---|
| `GET` | `/healthz` | None | `{status, version}` | `200` | Platform health heartbeat |
| `POST` | `/api/campaigns` | `CampaignBrief` | `{task_id, status}` | `200`, `422` | Initializes campaign generation |
| `GET` | `/api/campaigns/{id}` | None | `CampaignTaskStatus` | `200`, `404` | Retrieves stage progress & deliverables |
| `GET` | `/api/campaigns` | Query params | `List[CampaignTask]` | `200` | Paginated campaign execution history |
| `POST` | `/api/campaigns/{id}/optimize` | `{budget, target_cac}` | `OptimizationOutput` | `200`, `400` | Triggers PPO policy budget rebalancing |
| `POST` | `/api/campaigns/{id}/publish` | `{channels, test_mode}`| `PublishingResult` | `200`, `403` | Dispatches media to ad networks |
| `GET` | `/api/hitl/pending` | None | `List[HITLDecision]` | `200` | Fetches quarantined governance decisions |
| `POST` | `/api/hitl/{id}/approve` | `{role, reviewer}` | `HITLDecisionRecord` | `200`, `404` | Signs decision with HMAC-SHA256 |
| `POST` | `/api/hitl/{id}/reject` | `{role, reason}` | `HITLDecisionRecord` | `200`, `404` | Rejects decision and logs audit receipt |
| `GET` | `/api/models` | None | `List[ModelRegistryItem]` | `200` | Lists production model weights & specs |
| `POST` | `/api/rag/query` | `{query, top_k}` | `List[RetrievedChunk]`| `200` | Hybrid vector + BM25 evidence retrieval |
| `POST` | `/api/rag/index` | `{document, category}` | `{status, chunks}` | `200`, `422` | Ingests and indexes new knowledge |
| `GET` | `/api/memory/{tier}` | Path param | `MemorySnapshot` | `200`, `404` | Inspects state of Memory Tier 1, 2, 3, 4 |
| `GET` | `/api/metrics/executive` | None | `ExecutiveMetrics` | `200` | Returns aggregated spend and ROAS |
