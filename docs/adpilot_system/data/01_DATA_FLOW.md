# Data Flow Architecture

**Status:** [IMPLEMENTED]  

---

## 1. End-to-End Data Flow Diagram

```mermaid
graph TD
    Client[Browser Client / REST API] -->|JSON Brief: POST /api/campaigns| FastAPI[FastAPI Ingestion]
    FastAPI -->|Write Task Status: in_progress| SQLite[(SQLite: campaign_tasks)]
    
    FastAPI -->|Initialize PipelineRunner| Orch[Master Orchestrator]
    Orch <-->|Read / Write Stage Contracts| MemoryCache[(Working Memory: In-Memory LRU)]
    
    Orch -->|Semantic Query| Qdrant[(Qdrant Vector Store: bge-small)]
    Qdrant -->|Ranked Chunks| Orch
    
    Orch -->|Inference Calls| PyTorch[PyTorch PPO & Scikit-Learn Models]
    PyTorch -->|ROAS, CAC, Dirichlet Split| Orch
    
    Orch -->|Quarantine High-Risk Actions| HITLStore[(SQLite: hitl_decision_records)]
    
    Orch -->|Store Final Campaign Package| SQLite
    Orch -->|Publishing Adapters| ExternalAPIs[Meta / Google / LinkedIn APIs]
    
    ExternalAPIs -->|Live Telemetry| Monitoring[Monitoring Agent]
    Monitoring -->|Experience Replay Tuples| RLBuffer[(PyTorch Rollout Buffer)]
```

---

## 2. Data Flow Lifecycle

1. **Ingestion:** Raw input is validated and written as an active task in `adpilot.db`.
2. **Context Expansion:** RAG fetches relevant vectors from Qdrant; Brand memory loads style tokens from SQLite.
3. **Execution Pipeline:** Agent outputs pass through memory cache via typed Pydantic instances.
4. **Governance Locking:** If budget changes $> 10\%$, execution halts and writes a pending record to `hitl_decision_records`.
5. **Persistence & Export:** Completed campaigns are written to `campaign_tasks` and bundled into `data/outputs/` asset ZIP files.
