<p align="center">
  <img src="docs/images/hero_banner.png" alt="ADPilot Pro — Enterprise Autonomous Marketing OS" width="100%" />
</p>

<h1 align="center">ADPilot Pro</h1>

<p align="center">
  <strong>Enterprise-Grade Autonomous Marketing Operating System</strong><br/>
  <em>18-Agent Multi-Model AI Pipeline · Reinforcement Learning Optimizer · Human-in-the-Loop Governance</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-0.110%2B-009688?logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=white" alt="React" />
  <img src="https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/PyTorch-PPO%20RL-EE4C2C?logo=pytorch&logoColor=white" alt="PyTorch" />
  <img src="https://img.shields.io/badge/Pydantic-v2-E92063?logo=pydantic&logoColor=white" alt="Pydantic" />
  <img src="https://img.shields.io/badge/TailwindCSS-v3-38B2AC?logo=tailwindcss&logoColor=white" alt="TailwindCSS" />
  <img src="https://img.shields.io/badge/Scikit--Learn-Ridge%20%7C%20CLIP-F7931E?logo=scikit-learn&logoColor=white" alt="Scikit-Learn" />
  <img src="https://img.shields.io/badge/Qdrant-Vector%20DB-DC382D?logo=qdrant&logoColor=white" alt="Qdrant" />
  <img src="https://img.shields.io/badge/Tests-269%20Passing-brightgreen?logo=pytest&logoColor=white" alt="Tests" />
  <img src="https://img.shields.io/github/license/GhariebML/ADPilot-Pro?color=orange" alt="License" />
</p>

---

## What is ADPilot Pro?

**ADPilot Pro** is an **autonomous AI marketing operating system** that transforms a single campaign brief into a complete, launch-ready multi-channel advertising package — including ad copy, email sequences, social media content, creative design assets, budget allocation, and performance optimization.

It orchestrates **18 specialized AI agents** across an immutable Master Pipeline, combining **Large Language Models** (GPT-4o, Claude 3.5 Sonnet), **Reinforcement Learning** (PPO continuous policy optimization), **Computer Vision** (CLIP-ViT quality scoring), **Classical ML** (Ridge regression forecasting), and **Retrieval-Augmented Generation** (BGE FastEmbed + Qdrant) — all governed by a cryptographic **Human-in-the-Loop (HITL)** approval center.

### Key Capabilities

- 🧠 **18 Autonomous AI Agents** — Each with enforced Pydantic I/O contracts, epistemic confidence scoring, and deterministic downstream routing
- 🔄 **Self-Correcting Quality Gate Loop** — Content ↔ Analytics feedback cycle with 3-retry cap and automated hint extraction
- 📊 **PPO Reinforcement Learning Optimizer** — Continuous budget reallocation across channels using Actor-Critic policy networks
- 🖼️ **CLIP-ViT Visual Quality Scoring** — Automated creative asset safety, contrast ratio, and brand compliance verification
- 🔍 **Production RAG with Hybrid Retrieval** — Semantic (BGE) + Lexical (BM25) retrieval with reranking and provenance tracking
- 🛡️ **HITL Governance Center** — Role-based access control with HMAC-SHA256 signed cryptographic audit trails
- 📈 **Executive Intelligence Dashboard** — Real-time KPI metrics, ROAS trajectory charts, channel attribution matrix, and live autonomous action feeds

---

## 🏗️ Frozen Master Pipeline (18 Stages)

<p align="center">
  <img src="docs/images/pipeline_architecture.png" alt="ADPilot Pro — 18-Stage Master Pipeline Architecture" width="100%" />
</p>

The pipeline is **immutable** — every campaign traverses these stages in exact order:

```
User Input → Campaign Context → Product Classifier → Planner → Strategy → Research →
Competitor → Content → Design → CV → Analytics → RL Optimizer → Correction Engine →
Human Approval → Publishing → Monitoring → Feedback Loop → RAG Memory
```

| # | Stage | Agent | Model | Key Output |
|---|---|---|---|---|
| 1 | Campaign Context | Context Builder | Deterministic Engine | Structured campaign brief |
| 2 | Product Classification | Product Classifier | LLM (GPT-4o) | Product category & vertical |
| 3 | Strategic Planning | Planner Agent | LLM (GPT-4o) | Execution roadmap & milestones |
| 4 | Strategy | Strategy Agent | LLM (GPT-4o) | Positioning, channels, funnel stages |
| 5 | Market Research | Research Agent | LLM (Claude 3.5) | Persona profiles, market trends |
| 6 | Competitor Analysis | Competitor Agent | LLM (GPT-4o) | Competitive matrix, gap analysis |
| 7 | Content Creation | Content Agent | LLM (Claude 3.5) | Ad copy, emails, social posts |
| 8 | Design Direction | Design Agent | LLM (GPT-4o) | Visual concepts, image prompts |
| 9 | Visual Quality | CV Agent | CLIP-ViT (ONNX) | Aesthetic scores, contrast checks |
| 10 | Performance Analytics | Analytics Agent | Ridge Regressor | ROAS, CAC, CVR predictions |
| 11 | Budget Optimization | RL Optimizer | PyTorch PPO | Budget reallocation actions |
| 12 | Error Correction | Correction Engine | Deterministic | Constraint violation remediation |
| 13 | Human Approval | HITL Gate | Human Decision | Approve / Reject / Revise |
| 14 | Publishing | Publishing Agent | Adapter Engine | Multi-channel ad dispatch |
| 15 | Monitoring | Monitoring Agent | Anomaly Detector | Performance alerts & deviations |
| 16 | Feedback Loop | Feedback Engine | Deterministic | Closed-loop signal routing |
| 17 | Knowledge Storage | RAG Engine | FastEmbed BGE | Vector-indexed evidence store |
| 18 | Memory Persistence | Memory Manager | Multi-Tier Store | Campaign, brand & customer memory |

---

## 🖥️ Enterprise Dashboard & AI Operating System UI

<p align="center">
  <img src="docs/images/dashboard_preview.png" alt="ADPilot Pro — Executive Intelligence Dashboard" width="100%" />
</p>

The frontend is a **full AI Operating System dashboard** — not just a marketing dashboard:

| Module | Description |
|---|---|
| **Executive Dashboard** | Hero KPI cards (Managed Spend, ROAS, CAC, Autonomous Decisions), ROAS trajectory chart, channel attribution matrix |
| **Interactive Pipeline DAG** | Responsive 18-node visualization with live status, confidence bars, and click-to-inspect |
| **Agent Observatory** | Deep telemetry for every agent — latency, model, I/O contracts, epistemic confidence |
| **Agent Detail Drawer** | 4-stage Causal Explainability Tree (Prior → Hypothesis → Constraint Filter → Output) |
| **HITL Governance Center** | RBAC role switching (Director/Auditor/Growth Lead), approve/reject with SHA-256 signed audit log |
| **RL Optimizer Dashboard** | PPO training curves, reward trajectories, Dirichlet budget constraint visualization |
| **Model Registry & Benchmark Arena** | Catalog of 5 production models + latency/cost/quality comparison table |
| **RAG & Multi-Tier Memory** | Searchable vector document store + 4-tier memory architecture browser |
| **Creative Studio** | Design asset previews with CLIP-ViT quality scores and brand compliance indicators |
| **Campaign Timeline** | Chronological event log of every pipeline stage execution |
| **System Health** | Real-time platform diagnostics and service heartbeat monitors |
| **Command Palette** | `⌘K` keyboard-driven navigation across all OS modules |

---

## 🤖 AI Agent Fleet

<p align="center">
  <img src="docs/images/agent_fleet.png" alt="ADPilot Pro — 18-Agent Autonomous Fleet" width="100%" />
</p>

| Agent | Responsibility | Model Type | Framework |
|---|---|---|---|
| **Context Builder** | Structures raw user brief into validated campaign context | Deterministic Engine | Pydantic v2 |
| **Product Classifier** | Classifies product vertical (SaaS, Physical, Real Estate, Service) | LLM | GPT-4o |
| **Planner** | Generates execution roadmap with milestones and dependencies | LLM | GPT-4o |
| **Strategy Agent** | Creates positioning, selects channels, defines funnel stages | LLM | GPT-4o |
| **Research Agent** | Conducts audience profiling and market trend analysis | LLM | Claude 3.5 Sonnet |
| **Competitor Agent** | Maps competitive landscape with differentiation opportunities | LLM | GPT-4o |
| **Content Agent** | Drafts multi-format ad copy, emails, and social posts | LLM | Claude 3.5 Sonnet |
| **Design Agent** | Creates visual concepts and text-to-image prompts | LLM | GPT-4o |
| **CV Agent** | Scores visual quality, contrast ratios, brand compliance | Computer Vision | CLIP-ViT (ONNX) |
| **Analytics Agent** | Predicts ROAS, CAC, CVR using historical regression | Classical ML | Scikit-Learn Ridge |
| **RL Optimizer** | Optimizes multi-channel budget allocation via policy gradient | Reinforcement Learning | PyTorch PPO |
| **Correction Engine** | Detects and remediates constraint violations | Deterministic | Rule Engine |
| **HITL Gate** | Routes high-risk decisions to human reviewers | Human Decision | RBAC + SHA-256 |
| **Publishing Agent** | Dispatches ads to Meta, Google, LinkedIn via adapters | Adapter Engine | REST APIs |
| **Monitoring Agent** | Tracks live campaign KPIs and triggers anomaly alerts | Anomaly Detection | Statistical |
| **Feedback Engine** | Routes performance signals back to RL Optimizer | Deterministic | Event Router |
| **RAG Engine** | Indexes and retrieves evidence with semantic + BM25 hybrid search | Vector Embeddings | FastEmbed BGE |
| **Memory Manager** | Persists campaign, brand, customer, and execution memories | Multi-Tier Store | SQLite + Qdrant |

---

## ⚡ Tech Stack

### Backend
| Technology | Purpose |
|---|---|
| **FastAPI** | Async HTTP API with Pydantic v2 request/response validation |
| **Pydantic v2** | Strict typed schemas as single source of truth for all agent contracts |
| **SQLite** | Persistent campaign history and audit log storage |
| **Redis** | Background task queue and high-speed working memory cache |
| **Qdrant** | Production vector database for RAG semantic retrieval |
| **LangChain** | LLM provider abstraction and structured output parsing |

### Frontend
| Technology | Purpose |
|---|---|
| **React 18** | Component-based reactive UI with hooks |
| **TypeScript 5** | Strict type safety across all components and API contracts |
| **Vite** | Sub-second HMR dev server and optimized production bundler |
| **TailwindCSS v3** | Utility-first obsidian dark theme with glassmorphism effects |
| **Zustand** | Lightweight global state management |

### Machine Learning & AI
| Technology | Purpose |
|---|---|
| **PyTorch** | PPO Actor-Critic reinforcement learning policy network |
| **Scikit-Learn** | Ridge regression for multi-target revenue/ROAS forecasting |
| **CLIP-ViT (ONNX)** | Zero-shot visual quality scoring and brand compliance |
| **FastEmbed BGE** | Lightweight 384-dim dense vector embeddings for RAG |
| **OpenAI GPT-4o** | Primary LLM router for strategic planning and analysis |
| **Claude 3.5 Sonnet** | Creative copywriting and audience research LLM |

### DevOps & Quality
| Technology | Purpose |
|---|---|
| **Docker + Compose** | Containerized deployment (FastAPI + Redis + Qdrant) |
| **pytest** | 217 backend unit and integration tests |
| **Vitest** | 52 frontend component and integration tests |
| **ESLint + Ruff** | Zero-warning code quality enforcement |
| **GitHub Actions** | CI/CD pipeline for automated testing |

---

## 🚀 Quick Start

### Prerequisites

- **Python** 3.12+ 
- **Node.js** 20+
- **Redis** (local or remote)

### Backend Setup

```powershell
# 1. Clone the repository
git clone https://github.com/GhariebML/ADPilot-Pro.git
cd ADPilot-Pro

# 2. Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
Copy-Item .env.example .env
# Edit .env with your API keys

# 5. Launch the API server
$env:PYTHONPATH="src"
uvicorn adpilot.api.main:app --host 127.0.0.1 --port 8001
```

### Frontend Setup

```powershell
cd frontend
npm install
npm run dev
```

Open **http://localhost:3000** — click **"1-Click AI Demo"** to see the full pipeline in action.

---

## ⚙️ Environment Variables

| Variable | Description | Example |
|---|---|---|
| `LLM_PROVIDER` | Active LLM backend | `openai`, `openrouter`, `ollama` |
| `OPENAI_API_KEY` | OpenAI API secret key | `sk-...` |
| `OPENAI_MODEL` | Target OpenAI model | `gpt-4o` |
| `ANTHROPIC_API_KEY` | Anthropic Claude API key | `sk-ant-...` |
| `OPENROUTER_API_KEY` | OpenRouter gateway key | `sk-or-...` |
| `REDIS_URL` | Redis connection URL | `redis://localhost:6379/0` |
| `QDRANT_URL` | Qdrant vector DB endpoint | `http://localhost:6333` |
| `TEMPERATURE` | LLM creativity control | `0.2` |
| `ENVIRONMENT` | Runtime environment | `development` / `production` |

---

## 🧪 Testing & Quality

### Backend (217 Tests)
```powershell
$env:PYTHONPATH="src"
pytest tests/ -v
```

### Frontend (52 Tests)
```powershell
cd frontend
npm test -- --run     # Unit tests
npm run lint          # ESLint (0 errors, 0 warnings)
npm run build         # Production build (0 errors)
```

---

## 📂 Project Structure

```
ADPilot-Pro/
├── src/adpilot/                 # Core Python backend
│   ├── agents/                  # 18 specialized AI agents
│   ├── api/                     # FastAPI routes and middleware
│   ├── core/                    # Config, BaseAgent, exceptions, health
│   ├── correction/              # Self-correcting constraint engine
│   ├── hitl/                    # Human-in-the-Loop governance gates
│   ├── memory/                  # Multi-tier memory (campaign, brand, customer)
│   ├── monitoring/              # Live telemetry and anomaly detection
│   ├── orchestrator/            # Master pipeline orchestrator and planner
│   ├── prompts/                 # Agent system prompt templates
│   ├── providers/               # LLM provider adapters (OpenAI, Claude, Ollama)
│   ├── publishing/              # Multi-channel ad dispatch adapters
│   ├── rag/                     # RAG engine (chunker, BM25, hybrid, reranker)
│   ├── rl/                      # PPO reinforcement learning (env, models, trainer)
│   ├── schemas/                 # Pydantic v2 contracts (source of truth)
│   ├── services/                # Business logic and integrations
│   └── utils/                   # Logging and helper utilities
├── frontend/                    # React / TypeScript / Vite Dashboard
│   ├── src/components/          # 29 UI components (DAG, Observatory, HITL, etc.)
│   ├── src/services/            # API client and streaming
│   ├── src/store/               # Zustand global state
│   └── src/__tests__/           # Vitest component tests (52 tests)
├── research/                    # ML model training and evaluation
│   └── models/                  # Trained artifacts (PPO, Ridge, CLIP, BGE)
├── tests/                       # Backend pytest suite (217 tests)
├── docs/                        # Architecture docs and images
├── docker-compose.yml           # Multi-container orchestration
├── pyproject.toml               # Python project configuration
└── requirements.txt             # Production dependencies
```

---

## 🔒 Security

- **Credential Hygiene:** `.env` files are excluded via `.gitignore`. Never commit API keys.
- **HITL Governance:** All high-risk autonomous decisions require signed human approval.
- **Audit Trail:** Every agent execution and human decision is logged with timestamps.
- **Vulnerability Reporting:** See [SECURITY.md](SECURITY.md) for responsible disclosure.

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

<p align="center">
  <strong>Built with ❤️ by <a href="https://github.com/GhariebML">GhariebML</a></strong>
</p>
