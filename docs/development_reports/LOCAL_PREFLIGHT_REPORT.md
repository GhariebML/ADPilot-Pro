# ADPilot Pro — Local Pre-Flight Inspection Report

**Inspection Date:** August 22, 2026  
**Environment:** Windows (PowerShell)  
**System Runtimes:** Python 3.14.3 | Node.js v24.18.0 | npm 11.16.0  
**Inspection Target:** Local execution & verification of the frozen Master Pipeline  

---

## 1. System Dependency Classification Matrix

Every system component and service has been classified according to readiness:

| Dependency / Service | Classification | Status & Path / Port | Details & Fallbacks |
| :--- | :---: | :---: | :--- |
| **Python Runtime** | `READY` | Python 3.14.3 | Supported runtime ($\ge 3.12$ required). |
| **Node.js / npm Runtime** | `READY` | Node v24.18.0 / npm 11.16.0 | Modern JS runtime ready for Vite frontend build. |
| **Backend Framework (FastAPI)** | `READY` | `src/adpilot/api/main.py` | FastAPI 0.136.1 + Uvicorn 0.47.0. |
| **Frontend Framework (React)** | `READY` | `frontend/` | React 18 + Vite 7 + Tailwind CSS + Zustand. |
| **Frontend Node Modules** | `MISSING` | `frontend/node_modules` | Requires initial `npm install` in `frontend/`. |
| **Database (SQLite Async)** | `READY` | `adpilot.db` (Local SQLite) | `sqlite+aiosqlite:///./adpilot.db` active by default. |
| **Database (PostgreSQL)** | `OPTIONAL` | `postgresql://localhost:5432` | Optional production DB; SQLite is used locally. |
| **Vector DB (Local Qdrant)** | `READY` | `./storage/qdrant_rag` | Embedded local vector database with `:memory:` fallback. |
| **Vector DB (Qdrant Cloud)** | `OPTIONAL` | `QDRANT_URL` / `QDRANT_API_KEY` | Optional cloud cluster for high-scale RAG. |
| **Redis Cache / Message Bus** | `OPTIONAL` | `redis://localhost:6379/0` | Optional for direct pipeline; required for `arq` background workers. |
| **MongoDB Document Store** | `OPTIONAL` | `mongodb://localhost:27017` | Optional document store; in-memory fallback active. |
| **Background Task Worker (arq)** | `READY` | `src/adpilot/worker.py` | ARQ worker queue (`arq src.adpilot.worker.WorkerSettings`). |
| **RL Policy Checkpoint** | `READY` | `research/models/optimizer/ppo_policy.pt` | PyTorch PPO Actor-Critic continuous neural checkpoint. |
| **Analytics Forecaster Models** | `READY` | `research/models/analytics/*.pkl` | Sklearn Ridge regression, Scalers, ROAS forecasters. |
| **Content ML Quality Models** | `READY` | `research/models/content/*.pkl` | ML Ridge Copy quality scoring model & text predictors. |
| **CV Compliance Models** | `READY` | `research/models/cv/*.pkl` | Zero-shot CLIP-ViT and quality regression models. |
| **FastEmbed BGE Embeddings** | `READY` | `BAAI/bge-small-en-v1.5` | FastEmbed local ONNX model caching automatically. |
| **OpenRouter API Key** | `REQUIRES_API_KEY` | `OPENROUTER_API_KEY` | Optional for live cloud LLM calls; offline fallbacks ready. |
| **OpenAI API Key** | `REQUIRES_API_KEY` | `OPENAI_API_KEY` | Optional for direct OpenAI gpt-4o calls. |
| **Anthropic API Key** | `REQUIRES_API_KEY` | `ANTHROPIC_API_KEY` | Optional for Claude 3.5 Sonnet router calls. |
| **Docker Engine & Compose** | `OPTIONAL` | `docker-compose.yml` | Full containerized stack (API, worker, Redis). |
| **Seed / Demo Datasets** | `READY` | `data/samples/*.json` | Complete sample brief and output fixtures ready. |

---

## 2. Readiness Evaluation Summary

1. **Local Direct Execution:**
   - **Status:** **100% READY**
   - The entire 18-stage Master Pipeline, all 14 agents, multi-tier memory, and hybrid RAG can execute directly on Windows without external cloud infrastructure.
2. **REST API & Web Service:**
   - **Status:** **100% READY**
   - FastAPI server starts on port `8000` via Uvicorn with SQLite persistence.
3. **Web Dashboard UI:**
   - **Status:** **READY** (Requires `npm install` in `frontend/` directory).
   - Vite dev server runs on port `3000` and automatically proxies requests to FastAPI on port `8000`.
4. **Background Asynchronous Worker:**
   - **Status:** **OPTIONAL / REQUIRES_EXTERNAL_SERVICE**
   - If asynchronous background task queuing is required, Redis (`localhost:6379`) must be started before launching `arq src.adpilot.worker.WorkerSettings`.
