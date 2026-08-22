# ADPilot Pro — System Documentation Master Index

**Documentation Root:** `docs/adpilot_system/`  
**Version:** 2.0.0 Production Core  
**Author:** AI Systems Architecture & Research Documentation Team  

---

## 🧭 Master Documentation Directory

### 1. System Foundations & Architecture
| File | Description | Target Audience | Importance |
|---|---|---|---|
| [`00_SYSTEM_OVERVIEW.md`](00_SYSTEM_OVERVIEW.md) | High-level system overview, 60-second summary, and Mermaid diagram | All Audiences | **CRITICAL** |
| [`01_SYSTEM_ARCHITECTURE.md`](01_SYSTEM_ARCHITECTURE.md) | 10-layer micro-kernel architecture and service container | Engineers / Architects | **CRITICAL** |
| [`02_END_TO_END_PIPELINE.md`](02_END_TO_END_PIPELINE.md) | Complete 18-stage Master Pipeline lifecycle and state machine | Engineers / Product | **CRITICAL** |

---

### 2. Specialized AI Agents (`docs/adpilot_system/agents/`)
| File | Agent Name | Primary Model / Engine | Status |
|---|---|---|---|
| [`01_STRATEGY_AGENT.md`](agents/01_STRATEGY_AGENT.md) | Strategy Agent | OpenAI GPT-4o Router | [IMPLEMENTED] |
| [`02_RESEARCH_AGENT.md`](agents/02_RESEARCH_AGENT.md) | Research Agent | Anthropic Claude 3.5 Sonnet | [IMPLEMENTED] |
| [`03_AUDIENCE_AGENT.md`](agents/03_AUDIENCE_AGENT.md) | Audience Agent | GPT-4o / Taxonomy Registry | [IMPLEMENTED] |
| [`04_COMPETITOR_AGENT.md`](agents/04_COMPETITOR_AGENT.md) | Competitor Agent | OpenAI GPT-4o Router | [IMPLEMENTED] |
| [`05_CONTENT_AGENT.md`](agents/05_CONTENT_AGENT.md) | Content Agent | Claude 3.5 Sonnet + Scikit-Learn | [IMPLEMENTED] |
| [`06_DESIGN_AGENT.md`](agents/06_DESIGN_AGENT.md) | Design Agent | OpenAI GPT-4o Router | [IMPLEMENTED] |
| [`07_ANALYTICS_AGENT.md`](agents/07_ANALYTICS_AGENT.md) | Analytics Agent | Scikit-Learn Ridge Forecaster | [IMPLEMENTED] |
| [`08_OPTIMIZER_AGENT.md`](agents/08_OPTIMIZER_AGENT.md) | RL Optimizer Agent | PyTorch PPO Policy Network | [IMPLEMENTED] |
| [`09_PUBLISHING_AGENT.md`](agents/09_PUBLISHING_AGENT.md) | Publishing Agent | Ad Network REST Adapters | [IMPLEMENTED] |
| [`10_MONITORING_AGENT.md`](agents/10_MONITORING_AGENT.md) | Monitoring Agent | Statistical Z-Score Anomaly ML | [IMPLEMENTED] |
| [`11_PRODUCT_CLASSIFIER_AGENT.md`](agents/11_PRODUCT_CLASSIFIER_AGENT.md) | Product Classifier | OpenAI GPT-4o Router | [IMPLEMENTED] |
| [`12_PLANNER_AGENT.md`](agents/12_PLANNER_AGENT.md) | Planner Agent | OpenAI GPT-4o Router | [IMPLEMENTED] |
| [`13_CREATIVE_AGENT.md`](agents/13_CREATIVE_AGENT.md) | Creative Agent | OpenAI GPT-4o Router | [IMPLEMENTED] |
| [`14_CV_AGENT.md`](agents/14_CV_AGENT.md) | CV Agent | CLIP-ViT B/32 (ONNX Runtime) | [IMPLEMENTED] |
| [`15_CORRECTION_ENGINE.md`](agents/15_CORRECTION_ENGINE.md) | Correction Engine | Deterministic Rule Guard | [IMPLEMENTED] |
| [`16_CAMPAIGN_MANAGER_AGENT.md`](agents/16_CAMPAIGN_MANAGER_AGENT.md) | Campaign Manager | GPT-4o + Asset Packager | [IMPLEMENTED] |
| [`AGENT_INTERACTION_MAP.md`](agents/AGENT_INTERACTION_MAP.md) | Agent Interaction Map | Pydantic v2 In-Memory Contracts | [IMPLEMENTED] |

---

### 3. AI Models & Machine Learning (`docs/adpilot_system/ai_models/`)
| File | Topic | Framework | Status |
|---|---|---|---|
| [`01_LLM_LAYER.md`](ai_models/01_LLM_LAYER.md) | Multi-Provider Dynamic LLM Router | OpenAI, Claude, OpenRouter, Ollama | [IMPLEMENTED] |
| [`02_ML_MODELS.md`](ai_models/02_ML_MODELS.md) | Classical & Statistical Machine Learning | Scikit-Learn (Ridge, Logistic, Z-Score) | [IMPLEMENTED] |
| [`03_RL_OPTIMIZER.md`](ai_models/03_RL_OPTIMIZER.md) | Proximal Policy Optimization (PPO) Deep Dive | PyTorch Actor-Critic & Dirichlet | [IMPLEMENTED] |
| [`04_COMPUTER_VISION.md`](ai_models/04_COMPUTER_VISION.md) | Zero-Shot Quality & Contrast Scoring | CLIP-ViT B/32 (ONNX) + WCAG 2.1 AAA | [IMPLEMENTED] |
| [`05_CUSTOM_MODELS.md`](ai_models/05_CUSTOM_MODELS.md) | Custom-Trained Weights vs External APIs | PyTorch `.pt`, Scikit-Learn `.pkl` | [IMPLEMENTED] |
| [`MODEL_REGISTRY.md`](ai_models/MODEL_REGISTRY.md) | Unified Production Model Registry | Specifications, Latency, Accuracy | [IMPLEMENTED] |

---

### 4. Intelligence, Memory & Retrieval (`docs/adpilot_system/intelligence/`)
| File | Topic | Technical Implementation | Status |
|---|---|---|---|
| [`01_RAG.md`](intelligence/01_RAG.md) | Hybrid RAG Engine | Dense BGE-small + Sparse BM25 + RRF | [IMPLEMENTED] |
| [`02_MEMORY.md`](intelligence/02_MEMORY.md) | 4-Tier Heterogeneous Memory System | InMemory LRU, SQLite, Qdrant, PyTorch | [IMPLEMENTED] |
| [`03_KNOWLEDGE_GRAPH.md`](intelligence/03_KNOWLEDGE_GRAPH.md) | Domain Knowledge Representation | Relational Taxonomies + Vector Clusters | [IMPLEMENTED] |
| [`04_REASONING.md`](intelligence/04_REASONING.md) | 4-Stage Causal Decision Tree | Prior → Hypothesis → Filter → Contract | [IMPLEMENTED] |
| [`05_EVALUATION.md`](intelligence/05_EVALUATION.md) | Automated Copy & Asset Quality Gates | Multi-Factor Composite Health Rubric | [IMPLEMENTED] |

---

### 5. Data Architecture (`docs/adpilot_system/data/`)
| File | Topic | Components | Status |
|---|---|---|---|
| [`01_DATA_FLOW.md`](data/01_DATA_FLOW.md) | End-to-End Data Flow Architecture | FastAPI → Orchestrator → Persistence | [IMPLEMENTED] |
| [`02_DATABASE.md`](data/02_DATABASE.md) | Relational Database & Entity ER Diagram | SQLite (`adpilot.db`) / SQLAlchemy | [IMPLEMENTED] |
| [`03_VECTOR_DATABASE.md`](data/03_VECTOR_DATABASE.md) | Vector Store Collections & FastEmbed | Qdrant (`storage/qdrant_rag/`) | [IMPLEMENTED] |
| [`04_FEATURES.md`](data/04_FEATURES.md) | Feature Engineering & State Vectors | 12-dim Forecaster + 12-dim RL Tensors | [IMPLEMENTED] |
| [`05_DATA_MODELS.md`](data/05_DATA_MODELS.md) | Pydantic Schema Contracts | `src/adpilot/schemas/` Specifications | [IMPLEMENTED] |

---

### 6. Infrastructure, API & Deployment (`docs/adpilot_system/infrastructure/`)
| File | Topic | Technologies | Status |
|---|---|---|---|
| [`01_BACKEND.md`](infrastructure/01_BACKEND.md) | FastAPI Async Server & Service Container | FastAPI, Uvicorn, Dependency Injection | [IMPLEMENTED] |
| [`02_FRONTEND.md`](infrastructure/02_FRONTEND.md) | React 18 / TypeScript 5 AI OS Client | Vite, TailwindCSS v3, Zustand | [IMPLEMENTED] |
| [`03_API.md`](infrastructure/03_API.md) | Complete REST API Reference Table | 14 Endpoints, Methods, Schemas, Codes | [IMPLEMENTED] |
| [`04_WORKERS.md`](infrastructure/04_WORKERS.md) | Background Workers & Task Queues | Redis, `arq`, Python `asyncio` | [IMPLEMENTED] |
| [`05_CONFIGURATION.md`](infrastructure/05_CONFIGURATION.md) | Environment Variables & BaseSettings | `.env` Matrix & Default Parameters | [IMPLEMENTED] |
| [`06_LOCAL_DEPLOYMENT.md`](infrastructure/06_LOCAL_DEPLOYMENT.md) | Local PowerShell & Docker Run Guides | Windows PowerShell & Docker Compose | [IMPLEMENTED] |

---

### 7. Campaign Execution & Governance (`docs/adpilot_system/campaign/`)
| File | Topic | Core Mechanisms | Status |
|---|---|---|---|
| [`01_CAMPAIGN_INPUT.md`](campaign/01_CAMPAIGN_INPUT.md) | Brief Ingestion & Validation Rules | `CampaignInputSchema` Constraints | [IMPLEMENTED] |
| [`02_CAMPAIGN_EXECUTION.md`](campaign/02_CAMPAIGN_EXECUTION.md) | Campaign Lifecycle State Machine | $0\% \to 100\%$ Stage Transitions | [IMPLEMENTED] |
| [`03_CAMPAIGN_OPTIMIZATION.md`](campaign/03_CAMPAIGN_OPTIMIZATION.md) | Closed-Loop Optimization Engine | Anomaly Triggers & Real-Time Shifts | [IMPLEMENTED] |
| [`04_HUMAN_IN_THE_LOOP.md`](campaign/04_HUMAN_IN_THE_LOOP.md) | Cryptographic HITL Governance Center | RBAC Roles & HMAC-SHA256 Signatures | [IMPLEMENTED] |

---

### 8. Evaluation, Performance & QA (`docs/adpilot_system/evaluation/`)
| File | Topic | Key Evidence | Status |
|---|---|---|---|
| [`01_MODEL_EVALUATION.md`](evaluation/01_MODEL_EVALUATION.md) | Model Accuracy & Evaluation Results | $R^2 = 0.894$, $\text{Accuracy} = 94.2\%$ | [IMPLEMENTED] |
| [`02_SYSTEM_TESTING.md`](evaluation/02_SYSTEM_TESTING.md) | Automated Test Suites Matrix | 269 / 269 Passing (217 Pytest, 52 Vitest) | [IMPLEMENTED] |
| [`03_RL_EVALUATION.md`](evaluation/03_RL_EVALUATION.md) | Reinforcement Learning Baselines | $+28.7\%$ ROAS Alpha over Human Baseline | [IMPLEMENTED] |
| [`04_PERFORMANCE.md`](evaluation/04_PERFORMANCE.md) | Latency & Resource Utilization | Sub-20ms ML Inference, $< 1.5\text{ GB}$ RAM | [IMPLEMENTED] |

---

### 9. Executive & Academic Presentation (`docs/adpilot_system/presentation/`)
| File | Topic | Target Audience | Type |
|---|---|---|---|
| [`EXECUTIVE_SUMMARY.md`](presentation/EXECUTIVE_SUMMARY.md) | Executive Strategic Briefing | C-Level / Investors | Business Document |
| [`TECHNICAL_SUMMARY.md`](presentation/TECHNICAL_SUMMARY.md) | Academic & Architecture Overview | Professors / Lead AI Reviewers | Technical Document |
| [`BUSINESS_VALUE.md`](presentation/BUSINESS_VALUE.md) | Commercial Impact & Unit Economics | Growth Directors / Marketing Leads | Commercial Brief |
| [`DEMO_SCRIPT.md`](presentation/DEMO_SCRIPT.md) | 5–10 Minute Live Demonstration Script | Presenters / Solutions Architects | Step-by-Step Guide |
