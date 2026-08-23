# 03 — System Architecture

## 1. Multi-Tiered Enterprise Architecture
ADPilot Pro is engineered as a decoupled, 6-tier enterprise platform built for high concurrency, deterministic execution, and zero-trust security.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          1. PRESENTATION LAYER                              │
│  React 18 · Vite · Tailwind CSS · Three.js 3D Globe · Lucide Enterprise UI   │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ HTTP / REST & WebSockets (Port 3000 -> 8001)
┌──────────────────────────────────────▼──────────────────────────────────────┐
│                          2. API & GATEWAY LAYER                             │
│  FastAPI Router · Pydantic V2 · JWT Auth · CORS Security · Rate Limiter     │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────▼──────────────────────────────────────┐
│                      3. ORCHESTRATION & DAG ENGINE                          │
│  Simulation Runner · Pipeline Runner · Event Bus · Background Worker Queue  │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────▼──────────────────────────────────────┐
│                     4. MULTI-AGENT INTELLIGENCE FLEET                       │
│  Strategy · Research · Content · Design · CV · Analytics · PPO · HITL Gate  │
└───────────────────┬─────────────────────────────────────┬───────────────────┘
                    │                                     │
┌───────────────────▼───────────────┐     ┌───────────────▼───────────────────┐
│     5. ML, RL & VISION MODELS     │     │      6. DATA & MEMORY LAYER       │
│ · OpenAI / Anthropic / Gemini SDK │     │ · PostgreSQL / SQLite ORM Models  │
│ · Custom ONNX & Scikit Regressors │     │ · Qdrant Vector Store (384-dim)   │
│ · CLIP-ViT Zero-Shot Aesthetic    │     │ · FastEmbed (bge-small-en-v1.5)   │
│ · PPO Reinforcement Policy Engine │     │ · Redis Cache & Episodic Memory   │
└───────────────────────────────────┘     └───────────────────────────────────┘
```

---

## 2. Technical Layer Breakdown

### Layer 1: Presentation Tier
* **Framework:** React 18 with TypeScript and Vite bundler.
* **Component Architecture:** Modular dashboard structure featuring 11 views: `ExecutiveDashboardView`, `CampaignBriefForm`, `CampaignSimulationView`, `InteractivePipelineDAG`, `AgentObservatory`, `CreativeStudioView`, `OptimizerDashboard`, `KnowledgeBaseView`, `HITLApprovalCenter`, `ModelRegistryView`, and `SystemHealthView`.

### Layer 2: API Gateway Tier
* **Framework:** FastAPI with asynchronous ASGI worker (`uvicorn`).
* **Contract Enforcement:** 100% Pydantic v2 data validation on all ingress and egress payloads.
* **Security Middleware:** CORS whitelisting, JWT authentication tokens, role-based authorization gates (`ADMIN`, `OPERATOR`, `VIEWER`), and structured audit logging.

### Layer 3: Orchestration & Execution Engine
* **Execution Pattern:** Directed Acyclic Graph (DAG) pipeline coordinator with conditional branching, error recovery, and human-in-the-loop pause states.
* **Concurrency:** Asynchronous non-blocking background workers (`FastAPI BackgroundTasks` & asyncio event loops).

### Layer 4: Intelligence Tier
* Multi-agent system implementing `BaseAgent` abstract class with strict input validation, LLM invocation, schema translation, error handling, and output contract validation.

### Layer 5: ML / RL / CV Model Tier
* Pre-trained and fine-tuned predictive machine learning models loaded dynamically through `ModelLoader`.
* Google Gemini multi-modal generative image models alongside zero-shot vision quality auditing.

### Layer 6: Storage & Memory Tier
* **Relational DB:** SQLAlchemy ORM models managing Users, Organizations, Campaigns, Creatives, and Audit Logs.
* **Vector DB:** Qdrant instance storing 384-dimensional dense embeddings with cosine similarity distance metrics.
