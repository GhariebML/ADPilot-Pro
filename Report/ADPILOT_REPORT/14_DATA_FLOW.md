# 14 — Data Flow & System Communication

## 1. Communication Topologies
ADPilot Pro employs a hybrid communication architecture balancing low-latency synchronous REST calls for user queries with asynchronous event streaming for long-running agent workflows.

```
┌──────────────┐             REST HTTP (JSON)            ┌──────────────┐
│  React UI    │ <=====================================> │  FastAPI     │
│  (Port 3000) │                                         │  (Port 8001) │
└──────────────┘                                         └──────┬───────┘
                                                                │
                                              Background Tasks / Event Bus
                                                                │
                                                                ▼
                                                         ┌──────────────┐
                                                         │ Orchestrator │
                                                         └──────┬───────┘
                                                                │
                                            ┌───────────────────┼───────────────────┐
                                            ▼                   ▼                   ▼
                                     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
                                     │ Strategy    │     │ Content     │     │ Design      │
                                     │ Agent       │     │ Agent       │     │ Agent       │
                                     └─────────────┘     └─────────────┘     └─────────────┘
```

---

## 2. Communication Modes
1. **Synchronous REST (`/api/v1/`):** Immediate response queries for dashboard metrics, health status, and simulation initialization.
2. **Asynchronous Background Execution (`BackgroundTasks`):** Autonomous multi-agent pipeline runs and PPO policy evaluations running decoupled from HTTP request-response cycles.
3. **Polling & Event Loop (1.5s Interval):** Frontend polling loop syncing live DAG execution telemetry and status transitions (`RUNNING` $\to$ `REVIEW_REQUIRED` $\to$ `COMPLETED`).
