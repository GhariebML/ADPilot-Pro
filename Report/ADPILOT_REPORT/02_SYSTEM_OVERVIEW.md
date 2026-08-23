# 02 — System Overview

## 1. High-Level Concept: The AI Campaign Operating System
**ADPilot Pro** is structured as an autonomous campaign operating system. Rather than generating isolated text snippets or static ad copy, ADPilot treats a marketing campaign as a formal mathematical contract:

$$\mathcal{C} = \langle \mathcal{B}, \mathcal{T}, \mathcal{A}, \mathcal{K}, \mathcal{G}, \Omega \rangle$$

Where:
* $\mathcal{B}$ = Business & Brand Identity
* $\mathcal{T}$ = Timeline & Duration Parameters
* $\mathcal{A}$ = Audience Demographics & Psychographics
* $\mathcal{K}$ = Knowledge & Retrieved Vector Context
* $\mathcal{G}$ = Goals & Quantitative Target Metrics (ROAS, CAC, CTR)
* $\Omega$ = Governance, Policy Constraints, and Safety Boundaries

---

## 2. End-to-End Campaign Lifecycle Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                             1. INGESTION PHASE                              │
│  Client Brief ──> Campaign Manager ──> Product Classifier ──> Audience Agent │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────▼──────────────────────────────────────┐
│                             2. STRATEGY PHASE                               │
│  Knowledge Retrieval (RAG) ──> Strategy Agent ──> Research & Competitor Intel│
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────▼──────────────────────────────────────┐
│                         3. CREATIVE FACTORY PHASE                           │
│  Content Agent ──> Design Agent (Gemini) ──> Creative Agent ──> CV Gate Audit│
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────▼──────────────────────────────────────┐
│                        4. OPTIMIZATION & RL PHASE                           │
│  Analytics Agent (Forecasting) ──> PPO Policy Optimizer (Budget Allocation)  │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────▼──────────────────────────────────────┐
│                   5. DEPLOYMENT & GOVERNANCE PHASE                          │
│  Correction Engine ──> HITL Review Gate ──> Publishing Agent ──> Monitor Log│
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Core Architectural Subsystems
1. **Presentation Subsystem (Vite + React 18):** Enterprise UI providing interactive DAG visualization, agent observability telemetry, live simulation sandbox, and human approval control center.
2. **API & Orchestration Subsystem (FastAPI):** High-throughput asynchronous routing engine managing background task execution, event streaming, and schema validation.
3. **Agent Intelligence Subsystem:** Fleet of 18 autonomous agents executing specialized cognitive workflows.
4. **Analytics & Machine Learning Subsystem:** ONNX and scikit-learn models delivering aesthetic regression, intent classification, and churn/CLV forecasting.
5. **Memory & Vector Knowledge Subsystem (Qdrant):** Dense hybrid semantic memory preserving historical campaign telemetry and brand tone guidelines.
