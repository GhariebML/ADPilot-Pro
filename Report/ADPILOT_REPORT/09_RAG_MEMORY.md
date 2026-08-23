# 09 — RAG & Multi-Tier Memory Architecture

## 1. Semantic Knowledge Retrieval Engine
ADPilot Pro integrates a multi-tier Retrieval-Augmented Generation (RAG) system governed by `RAGService` in `src/adpilot/services/rag_service.py`. The engine grounds agent reasoning in verified marketing playbooks, brand voice guidelines, historical campaign telemetry, and regulatory compliance documents.

```
Document Ingestion (.md, .pdf, .json)
         │
         ▼
Recursive Character Chunking (500 tokens, 10% overlap)
         │
         ▼
Dense Embedding Generation (FastEmbed: `bge-small-en-v1.5`, 384 dimensions)
         │
         ▼
Vector Ingestion into Qdrant Collection (`adpilot_knowledge`)
         │
         ▼
┌──────────────────────────────────────────────────────────────────┐
│                   HYBRID RETRIEVAL PIPELINE                      │
│                                                                  │
│  Agent Context Query ──> [Dense Vector Similarity (Cosine)]       │
│                                  +                               │
│                         [Sparse BM25 Keyword Filter]             │
│                                  │                               │
│                                  ▼                               │
│                       Reciprocal Rank Fusion                     │
│                                  │                               │
│                                  ▼                               │
│                     Top-K Grounded Context (k=5)                 │
└──────────────────────────────────┬───────────────────────────────┘
                                   │
                                   ▼
                   Injected into Agent System Prompt
```

---

## 2. Multi-Tier Memory Hierarchy
ADPilot manages memory across three discrete lifecycles:

| Memory Tier | Storage Medium | Lifecycle Scope | Target Data | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Working Memory** | Python Process State (`CampaignContext`) | Single DAG Pipeline Run | Active agent outputs, intermediate JSON tokens | `[IMPLEMENTED]` |
| **Episodic Memory** | SQLite / PostgreSQL ORM Tables | Cross-Campaign (Per Organization) | Final campaign metrics, HITL feedback records | `[IMPLEMENTED]` |
| **Semantic Memory** | Qdrant Vector Store (384-dim dense) | Persistent System-Wide | Knowledge base documents, brand tone vectors | `[IMPLEMENTED]` |
