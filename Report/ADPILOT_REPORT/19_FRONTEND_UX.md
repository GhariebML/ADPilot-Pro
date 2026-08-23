# 19 — Frontend Architecture & User Experience

## 1. Enterprise UX Design System
The ADPilot frontend is designed around a high-contrast dark enterprise aesthetic inspired by modern mission-control consoles (Deep Obsidian `#07090e`, Titanium Slate `#0f172a`, Electric Cyan `#00f0ff`, Emerald `#10b981`, Magenta `#ec4899`).

---

## 2. Comprehensive Module Directory

| # | View Module | React Component Path | Core User Purpose | Backend Integration Endpoint |
|---|---|---|---|---|
| **1** | **Executive Dashboard** | `frontend/src/components/ExecutiveDashboardView.tsx` | Macro KPI metrics, active spend, live ROAS charts, active agent status | `GET /api/v1/analytics/overview` |
| **2** | **Campaign Ingestion Brief** | `frontend/src/components/CampaignBriefForm.tsx` | Structured brief creator with USP and budget inputs | `POST /api/v1/campaigns` |
| **3** | **End-to-End Simulation** | `frontend/src/components/simulation/CampaignSimulationView.tsx` | 5-phase DAG execution sandbox with live telemetry inspector and HITL gate | `POST /api/v1/simulations` |
| **4** | **Interactive Pipeline DAG** | `frontend/src/components/InteractivePipelineDAG.tsx` | Visual DAG graph editor showing live inter-agent data streams | WebSocket / Event Bus |
| **5** | **AI Agent Observatory** | `frontend/src/components/AgentObservatory.tsx` | Real-time agent thought traces, cognitive logs, and tool calls | `GET /api/v1/agents/telemetry` |
| **6** | **Nano Banana Creative Studio**| `frontend/src/components/CreativeStudioView.tsx` | Multi-format image generation studio (16:9, 1:1, 4:5, 9:16) with palette extractor | `POST /api/creative/generate` |
| **7** | **RL Policy Optimizer** | `frontend/src/components/OptimizerDashboard.tsx` | PPO reward curves, multi-armed bandit state, channel reallocation heatmaps | `GET /api/v1/optimizer/state` |
| **8** | **RAG & Memory Base** | `frontend/src/components/KnowledgeBaseView.tsx` | Vector document manager, chunk inspector, and 3D embedding visualizer | `POST /api/v1/knowledge/query` |
| **9** | **HITL Approval Center** | `frontend/src/components/HITLApprovalCenter.tsx` | Action review queue, variance delta inspector, and cryptographic sign-off | `POST /api/v1/approvals/action` |
| **10**| **Model Registry** | `frontend/src/components/ModelRegistryView.tsx` | Active checkpoints, ONNX inference engines, and latency benchmarks | `GET /api/v1/models/registry` |
| **11**| **Platform Diagnostics** | `frontend/src/components/SystemHealthView.tsx` | Server health probes, memory utilization, API latencies, and worker queues | `GET /healthz` |
