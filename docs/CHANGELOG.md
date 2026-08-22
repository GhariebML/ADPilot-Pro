# Changelog

All notable changes to ADPilot Pro are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.0] — 2026-08-22

### 🚀 Major Release — Enterprise Autonomous Marketing OS

Complete ground-up redesign of the ADPilot platform into a production-grade autonomous marketing operating system.

### Added

#### 18-Stage Master Pipeline
- Immutable, sequentially deterministic pipeline with typed Pydantic v2 contracts at every stage.
- Stages: Brief Ingestion → Context Builder → Product Classifier → Planner → Strategy → Research → Competitor → Content → Design → CV Quality Gate → Analytics → RL Optimizer → Correction Engine → HITL Gate → Publishing → Monitoring → Feedback Loop → RAG & Memory.

#### 16 Specialized AI Agents
- Strategy, Research, Audience, Competitor, Content, Design, Analytics, Optimizer, Publishing, Monitoring, Product Classifier, Planner, Creative, CV, Correction Engine, and Campaign Manager agents.
- Each agent communicates via immutable Pydantic v2 schema contracts.
- Multi-provider LLM routing: OpenAI GPT-4o and Anthropic Claude 3.5 Sonnet.

#### Deep Reinforcement Learning Optimizer
- Custom PyTorch PPO (Proximal Policy Optimization) Actor-Critic neural network.
- 12-dimensional state vector → Dirichlet concentration parameters → normalized budget allocation.
- Clipped objective with entropy bonus and value function loss.
- Saved policy checkpoint: `research/models/optimizer/ppo_policy.pt`.

#### Hybrid RAG Engine
- Dual-stream retrieval: Dense embeddings (BAAI/bge-small-en-v1.5 via FastEmbed, 384-dim) + Sparse BM25 Okapi.
- Reciprocal Rank Fusion (RRF) with k=60 for result merging.
- Qdrant vector database integration.

#### CLIP-ViT Computer Vision Quality Gate
- Zero-shot CLIP-ViT B/32 aesthetic scoring via ONNX runtime.
- WCAG AAA contrast ratio validation (≥ 7.0:1).
- Brand palette alignment via color histogram analysis.

#### Cryptographic Human-in-the-Loop (HITL) Governance
- RBAC with 3 enterprise roles: Campaign Director, Compliance Auditor, Growth Lead.
- HMAC-SHA256 signed audit receipts for every approval/rejection.
- Automatic quarantine of high-risk actions (budget shifts > $1,000, live publishing).

#### 4-Tier Memory Architecture
- Tier 1: Working Memory (in-memory LRU, 0.2ms latency).
- Tier 2: Brand Voice Memory (SQLite structured store, 1.1ms).
- Tier 3: Customer Memory (Qdrant vector store, 4.2ms).
- Tier 4: Execution Feedback (PyTorch trajectory buffer, 15.8ms).

#### Custom ML Models
- Revenue Forecaster: Scikit-Learn Ridge regressor (`revenue_forecaster.pkl`).
- Brand Voice Classifier: Scikit-Learn Logistic Regression with TF-IDF (`brand_voice_classifier.pkl`).
- Creative Quality Regressor: CLIP-ViT embedding + linear head (`creative_quality_regressor.pkl`).

#### React 18 AI OS Dashboard
- 12 integrated operational modules: Executive Dashboard, Interactive Pipeline DAG, Agent Observatory, Agent Detail Drawer, Raw I/O Telemetry, HITL Governance Center, RL Optimizer, Model Registry & Arena, RAG & Memory, Creative Studio, Campaign Timeline, Platform Diagnostics.
- 29 modular TypeScript/React components.
- Zustand state management, TailwindCSS v3, Lucide icons.
- Vite dev server with API proxy to FastAPI backend.

#### FastAPI Backend
- 14+ REST API endpoints with OpenAPI/Swagger documentation.
- Async pipeline runner with campaign lifecycle management.
- Health check, model registry, RAG query, and memory inspection endpoints.

#### Comprehensive Test Suite
- 217 backend tests (pytest) — 100% pass rate.
- 52 frontend tests (Vitest) — 100% pass rate.
- 269 total automated tests.
- Ruff and ESLint with zero errors/warnings.

#### 56-File Documentation Package (`docs/adpilot_system/`)
- System Foundations (3 files): Overview, Architecture, Pipeline.
- Agent Documentation (17 files): 16 agent specs + interaction map.
- AI Models (6 files): LLM layer, ML models, RL optimizer, CV, custom models, registry.
- Intelligence & Memory (5 files): RAG, Memory, Knowledge Graph, Reasoning, Evaluation.
- Data Architecture (5 files): Data flow, Database, Vector DB, Features, Data models.
- Infrastructure (6 files): Backend, Frontend, API, Workers, Configuration, Deployment.
- Campaign Execution (4 files): Input, Execution, Optimization, HITL.
- Evaluation & QA (4 files): Model evaluation, Testing, RL evaluation, Performance.
- Presentations (4 files): Executive summary, Technical summary, Business value, Demo script.

#### CI/CD & Repository Infrastructure
- GitHub Actions CI pipeline with 3 jobs (Backend, Frontend, Docker).
- 8 issue templates (bug report, feature request, agent task, schema change, docs).
- PR template, CODEOWNERS, CODE_OF_CONDUCT.
- Professional README with 6 generated high-resolution diagrams.

---

## [1.0.0] — 2026-05-19

### Added

- LangChain structured-output support through the shared `BaseAgent` pattern.
- Implemented Research, Content, Analytics, Design, and Campaign Manager agents.
- Multi-provider LLM support for OpenAI, OpenRouter, and Hugging Face Inference Providers.
- Phase 1 runner scripts for individual agents and the full pipeline.
- Dashboard-compatible FastAPI endpoints for campaign submission, task polling, and local result display.
- Tests for provider selection, missing provider keys, structured-output patterns, and agent behavior.
- Professional project documentation in `docs/`.

### Changed

- Updated configuration to use `pydantic-settings` and `.env` loading.
- Updated `.env.example` for OpenAI, OpenRouter, Hugging Face, temperature, and environment settings.
- Updated README for GitHub-ready setup, usage, provider configuration, and contribution guidance.
- Improved `.gitignore` coverage for local files, caches, logs, environments, and build output.

### Fixed

- Fixed direct script execution from the repository root.
- Fixed the local dashboard workflow by aligning frontend API calls with backend routes.
- Prevented local dashboard previews from hanging on real LLM calls by using demo output unless explicitly enabled.

### Security

- Confirmed no real `.env` file is committed.
- Kept secrets out of tracked files.
- Added safer ignore rules for local environment files, logs, caches, and build outputs.

### Documentation

- Added `PROJECT_OVERVIEW.md`, `UPDATE_REPORT.md`, `SETUP_GUIDE.md`, `GITHUB_WORKFLOW.md`, and `CHANGELOG.md`.
- Documented local setup, provider selection, test commands, GitHub workflow, and security notes.
