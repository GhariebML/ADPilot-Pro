# ADPilot Pro — Master System Revision & Enterprise Hardening Plan
## Comprehensive Technical Refactoring, Bug Remediation, and Architectural Hardening Specification

**Document Version:** 3.0.0-PRO  
**Author:** Principal AI Systems Architect & Lead Software Engineer  
**System:** ADPilot Pro — Enterprise Autonomous AI Campaign Operating System  

---

## Table of Contents

1. [Executive Overview & Audit Synthesis](#1-executive-overview--audit-synthesis)
2. [Target Architecture & Quality Standards](#2-target-architecture--quality-standards)
3. [Phased Revision Roadmap (Phases 1 to 6)](#3-phased-revision-roadmap)
   - [Phase 1: Critical Bug Remediation & Runtime Stability](#phase-1-critical-bug-remediation--runtime-stability)
   - [Phase 2: Backend Architecture & API Decomposition](#phase-2-backend-architecture--api-decomposition)
   - [Phase 3: Agent Fleet, Schema Typing & Contract Registry](#phase-3-agent-fleet-schema-typing--contract-registry)
   - [Phase 4: Intelligence Infrastructure (RAG, ML, CV, RL)](#phase-4-intelligence-infrastructure-rag-ml-cv-rl)
   - [Phase 5: Frontend State Architecture & Responsive UX](#phase-5-frontend-state-architecture--responsive-ux)
   - [Phase 6: Quality Engineering, Testing & DevOps Hardening](#phase-6-quality-engineering-testing--devops-hardening)
4. [Detailed File Modification & Refactoring Matrix](#4-detailed-file-modification--refactoring-matrix)
5. [Verification, Testing & Rollback Strategy](#5-verification-testing--rollback-strategy)

---

## 1. Executive Overview & Audit Synthesis

A rigorous, full-stack audit across **169 Python modules** (952 KB), **66 Frontend components** (562 KB), and **53 Test suites** revealed the following key areas for enhancement:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                             SYSTEM AUDIT SUMMARY                            │
├────────────────────────────────┬────────────────────────────────────────────┤
│ Subsystem                      │ Identified Findings / Revision Focus       │
├────────────────────────────────┼────────────────────────────────────────────┤
│ 1. Runtime Pipeline Execution  │ Fix 'CompetitorInfo' attribute mismatch    │
│ 2. API Gateway Architecture    │ Decompose monolithic api/main.py (1492 L)  │
│ 3. Orchestration Layer         │ Consolidate orchestration/ vs orchestrator/│
│ 4. Provider Layer Resilience   │ Enhance Gemini GenAI quota retry & caching │
│ 5. Agent Contract Registry     │ Complete bidirectional Pydantic v2 parity  │
│ 6. Storage & Cleanliness       │ Remove zero-byte dead files                │
│ 7. DevOps & Quality Config     │ Add ruff.toml, mypy.ini, .dockerignore     │
│ 8. Frontend State Sync         │ Standardize async polling & toast errors   │
└────────────────────────────────┴────────────────────────────────────────────┘
```

---

## 2. Target Architecture & Quality Standards

* **Zero-Downtime Refactoring:** All modifications preserve backward compatibility across all public API endpoints (`/api/v1/*`) and database schemas.
* **100% Type-Safe Contracts:** Absolute enforcement of Pydantic v2 generic models across all 18 agent boundaries.
* **Modular Clean Architecture:** Strict separation of concerns (API Controllers -> Orchestrator -> Agents -> Service Layer -> Storage).
* **Test Certification:** Zero test regressions; 100% passing automated test suite across backend and frontend.

---

## 3. Phased Revision Roadmap

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    6-PHASE SYSTEM REVISION ROADMAP                          │
│                                                                             │
│  [PHASE 1] CRITICAL BUG FIXES & RUNTIME STABILITY                           │
│  • Fix CompetitorInfo attribute access bug in CampaignManagerAgent          │
│  • Implement exponential backoff & disk caching for Gemini image provider   │
│  • Purge dead/empty files (refactor_task_manager.py)                         │
│                                                                             │
│  [PHASE 2] BACKEND MODULARIZATION & ROUTE DECOMPOSITION                     │
│  • Break down api/main.py (1492 L) into modular APIRouter controllers       │
│  • Eliminate duplicate src/adpilot/orchestration/ directory                 │
│                                                                             │
│  [PHASE 3] AGENT CONTRACTS & BASEAGENT RESILIENCE                           │
│  • Harden Pydantic v2 schemas and JSON extraction fallback                  │
│  • Standardize error recovery loop across all 18 agent classes              │
│                                                                             │
│  [PHASE 4] INTELLIGENCE INFRASTRUCTURE HARDENING                            │
│  • Optimize FastEmbed + BM25 hybrid RAG memory retrieval                   │
│  • Verify ONNX/Scikit model inference speed and memory footprint            │
│                                                                             │
│  [PHASE 5] FRONTEND STATE & OBSERVABILITY POLISH                            │
│  • Decouple Zustand store slices, add global toast error interceptors       │
│  • Refine mobile/tablet responsiveness on Interactive DAG & Studio          │
│                                                                             │
│  [PHASE 6] DEVOPS, TESTING & CI/CD HARDENING                                │
│  • Run & certify full Pytest and Vitest test suites                         │
│  • Add ruff.toml, mypy.ini, and optimized multi-stage Docker build          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Detailed File Modification & Refactoring Matrix

| Phase | Target File / Module | Nature of Change | Purpose & Impact |
| :--- | :--- | :--- | :--- |
| **Phase 1** | `src/adpilot/agents/campaign_manager_agent.py` | Bug Fix | Correct `competitors` list property access on `CompetitorAnalysisOutput` |
| **Phase 1** | `src/adpilot/providers/image_provider.py` | Enhancement | Add local file-hash caching & exponential backoff on 429 quota limits |
| **Phase 1** | `src/adpilot/services/refactor_task_manager.py`| Deletion | Remove 0-byte orphan file |
| **Phase 2** | `src/adpilot/api/v1/routes/*.py` | Refactoring | Distribute routes into `campaigns.py`, `agents.py`, `creative.py`, `analytics.py`, `hitl.py`, `models.py` |
| **Phase 2** | `src/adpilot/api/main.py` | Refactoring | Slim down main entry point to middleware, lifespan, and router mounts |
| **Phase 2** | `src/adpilot/orchestration/` | Refactoring | Consolidate legacy files into `src/adpilot/orchestrator/` |
| **Phase 3** | `src/adpilot/core/base_agent.py` | Hardening | Enhance JSON schema repair prompt during LLM parsing failures |
| **Phase 3** | `src/adpilot/core/contract_registry.py` | Hardening | Verify all 18 agent input/output contract mappings |
| **Phase 4** | `src/adpilot/rag/hybrid.py` | Optimization| Ensure reciprocal rank fusion (k=60) cache hits |
| **Phase 5** | `frontend/src/store/useAppStore.ts` | Refinement | Modularize store state and optimize event bus polling |
| **Phase 6** | `ruff.toml` & `mypy.ini` | Configuration| Establish enterprise Python linting & type checking |
| **Phase 6** | `.dockerignore` | Configuration| Optimize Docker build context excluding unnecessary cache |

---

## 5. Verification, Testing & Rollback Strategy

1. **Unit & Contract Verification:** Run `pytest tests/` after each phase to ensure zero regressions.
2. **End-to-End Simulation Check:** Run `simulation_runner.py` verifying seamless 18-stage execution without fallback triggers.
3. **Frontend Integration Check:** Run `npm run test` and verify all 12 dashboard views in the browser.
4. **Git Version Control Checkpoint:** Commit each phase atomically with clear semantic commit messages.

---
*End of Master Revision Plan Document — ADPilot Pro*