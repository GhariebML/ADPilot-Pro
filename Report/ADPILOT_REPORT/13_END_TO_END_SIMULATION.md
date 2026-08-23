# 13 — End-to-End Campaign Simulation

## 1. Simulation Architecture & 5-Phase DAG
The End-to-End Campaign Simulation (`/simulation`) provides a deterministic, zero-risk environment for demonstrating, validating, and stress-testing the complete 18-agent pipeline. The simulation executes asynchronously via `SimulationRunner` in `src/adpilot/orchestrator/simulation_runner.py`.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       15-AGENT SIMULATION PIPELINE DAG                      │
│                                                                             │
│  [PHASE 1: INGESTION]                                                       │
│  Campaign Manager ──> Product Classifier ──> Audience Agent ──> Competitor │
│                                                                             │
│  [PHASE 2: STRATEGY]                                                        │
│  Strategy Agent ──> Research Agent (RAG Context)                            │
│                                                                             │
│  [PHASE 3: CREATIVE FACTORY]                                                │
│  Content Agent ──> Design Agent (Gemini) ──> Creative Agent ──> CV Agent    │
│                                                                             │
│  [PHASE 4: OPTIMIZATION & RL]                                               │
│  Analytics Agent (Forecasting) ──> RL / PPO Optimizer (Reallocation)        │
│                                                                             │
│  [PHASE 5: DEPLOYMENT & GOVERNANCE]                                         │
│  Correction Agent ──> HITL Review Gate ──> Publishing Agent ──> Monitoring │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Live Execution Telemetry & Performance Deltas
During simulation execution, every agent records:
* Execution latency in seconds
* Model identity (e.g., `gpt-4o`, `claude-3-5-sonnet`, `gemini-3.1-flash-image`)
* Input context payloads and structured output traces
* Optimization impact: Ingests baseline metrics and calculates simulated post-optimization metrics upon human approval:
  * **ROAS:** $3.21\text{x} \longrightarrow 3.68\text{x} \; (+14.6\%)$
  * **CAC:** $\$47.80 \longrightarrow \$41.20 \; (-13.8\%)$
  * **Conversion Rate:** $3.4\% \longrightarrow 4.2\% \; (+23.5\%)$
