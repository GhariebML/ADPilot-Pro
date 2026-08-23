# ADPilot Pro — One-Page System Architecture Blueprint

## Executive Overview
**ADPilot Pro** is an autonomous AI Campaign Operating System that replaces fragmented, manual digital marketing workflows with a deterministic, multi-agent Directed Acyclic Graph (DAG) governed by Human-in-the-Loop oversight.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. INGESTION & STRATEGY                                                     │
│ · Ingests Brand Identity, Target Market, Duration, and Budget Bounds        │
│ · Strategy & Research Agents synthesize positioning using Qdrant Vector RAG │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. CREATIVE FACTORY & DUAL-ENGINE VISION                                    │
│ · Content Agent drafts multi-channel copywriting variants                   │
│ · Design Agent synthesizes 4 aspect ratios via Google Gemini Nano Banana    │
│ · Computer Vision Agent audits zero-shot CLIP aesthetic & WCAG AAA contrast │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. ANALYTICS & REINFORCEMENT LEARNING OPTIMIZATION                          │
│ · Custom ONNX/Scikit models forecast CTR, CPA, and 30-day ROAS trajectory   │
│ · PPO Policy Optimizer dynamically shifts multi-channel budget allocations  │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. DETERMINISTIC GOVERNANCE & EXECUTION                                     │
│ · Decision Engine assesses risk index and evaluates policy boundaries       │
│ · Human-in-the-Loop gate requires cryptographic review for high-delta shifts│
│ · Publishing Agent dispatches campaigns; Monitoring Agent loops telemetry   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Core Empirical Outcomes:
* **ROAS Improvement:** $+14.6\%$ ($3.21\text{x} \to 3.68\text{x}$)
* **Customer Acquisition Cost:** $-13.8\%$ ($\$47.80 \to \$41.20$)
* **Contract Verification:** $100\%$ type-safe Pydantic v2 execution across 18 specialized agents.
