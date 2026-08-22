# Phase 11 — Correction Engine & Closed-Loop Governance Report

**Author / Component:** ADPilot Advanced Agentic Orchestration Core  
**Pipeline Stage:** Stage 9 — Correction Engine (`correction_agent` / `correction_engine`)  
**Status:** FULLY IMPLEMENTED, INTEGRATED, AND VERIFIED (166/166 Tests Passing)  
**Date:** 2026-08-22  

---

## Executive Summary

Phase 11 delivers the **Correction Engine** for the ADPilot platform. The Correction Engine operates as the central closed-loop governance, diagnostic, and remediation system. It ingests defect signals across seven trigger sources, determines root-cause attribution, maps failures deterministically to responsible agents, synthesizes constraint-preserving corrective directives, re-executes remediation tasks, verifies invariant safety, and produces structured audit lineage before escalating unresolved defects to Human-in-the-Loop (HITL) review.

---

## Architecture & Responsibilities

```
                                    +-------------------------------------------------------------+
                                    |                Multi-Source Defect Ingestion                |
                                    |  - Agent Quality Gates   - Performance Deviations (CTR/CPA) |
                                    |  - Validation Failures   - Computer Vision (CV) Defects     |
                                    |  - Analytics Bottlenecks - RL Safety Breaches               |
                                    |  - Human-in-the-Loop (HITL) Rejection Critique              |
                                    +------------------------------+------------------------------+
                                                                   |
                                                                   v
                                    +-------------------------------------------------------------+
                                    |                      ProblemClassifier                      |
                                    |  - Root-cause diagnosis and categorization                  |
                                    |  - Severity classification (Critical, High, Medium, Low)   |
                                    |  - Responsible agent attribution & context key tracking     |
                                    +------------------------------+------------------------------+
                                                                   |
                                                                   v
                                    +-------------------------------------------------------------+
                                    |                         AgentRouter                         |
                                    |  - Deterministic routing to responsible upstream agents     |
                                    |  - Prescriptive prompt injection synthesis                  |
                                    |  - Task prioritization and boundary enforcement             |
                                    +------------------------------+------------------------------+
                                                                   |
                                                                   v
                                    +-------------------------------------------------------------+
                                    |                       ConstraintGuard                       |
                                    |  - Baseline context invariant snapshotting                  |
                                    |  - Total budget cap & currency immutability enforcement     |
                                    |  - Business identity & brand color palette preservation     |
                                    |  - Automatic tampering detection & invariant restoration    |
                                    +------------------------------+------------------------------+
                                                                   |
                                                                   v
                                    +-------------------------------------------------------------+
                                    |                CorrectionEngine Orchestrator                |
                                    |  - Re-executes responsible agents with corrective guidance  |
                                    |  - Evaluates resolution criteria and updates CampaignContext|
                                    |  - Circuit-breaker ceiling (max 3 loops) -> HITL Escalation |
                                    |  - Emits lifecycle events (started, completed, failed)      |
                                    +-------------------------------------------------------------+
```

---

## Defect Classification & Agent Routing Matrix

| Problem Category | Trigger Source | Responsible Agent | Corrective Remediation Directive |
|---|---|---|---|
| **Low CTR** | `performance_deviation` / `human_rejection` | `content_agent` | Synthesizes high-converting benefit-driven hooks, dynamic CTAs, and headline clarity revisions. |
| **Poor Creative Quality** | `cv_issue` (Aesthetic < 6.0) | `design_agent` | Injects negative prompts ('lowres, blurry, distorted text') and layout focal point requirements. |
| **Brand Safety Violation** | `cv_issue` / `validation_failure` | `design_agent` / `content_agent` | Enforces critical safety boundaries; removes unverified claims, trademarked imagery, and platform policy risks. |
| **Audience / Persona Mismatch** | `strategy_mismatch` / `human_rejection` | `strategy_agent` | Re-aligns value proposition, target buyer persona messaging pillars, and validates 100% funnel budget allocation sum. |
| **High CAC / Low ROAS** | `performance_deviation` / `analytics_issue` | `optimization_agent` | Rebalances budget from high-CPA channels, clamps bid multipliers within safe intervals [0.80x, 1.20x], and cools acquisition cost. |
| **Health Score Gate Failure** | `analytics_issue` (Health Score < 70.0) | `content_agent` / `analytics_agent` | Re-scores multi-dimensional funnel health and generates copy optimizations to lift conversion probabilities. |
| **Invalid RL Action** | `rl_issue` (Simplex / Box Constraint breach) | `optimization_agent` | Re-executes simplex projection and bounds clamping via `ConstraintValidator`. |
| **Human Rejection Critique** | `human_rejection` | Target Agent | Parses human critique into targeted prompt injections while strictly preserving core campaign parameters. |
| **Concurrent Multi-Agent Failure** | Multi-source | Prioritized Agents | Triages multiple concurrent issues in order of severity (Critical Safety $\to$ High CTR $\to$ Medium Optimization). |
| **Circuit Breaker Ceiling** | Max Retries ($N \ge 3$) | HITL Escalation | Halts automated loops and transitions plan state to `WAITING_FOR_APPROVAL` with diagnostic failure trace. |

---

## Strict Invariant Preservation (`ConstraintGuard`)

Per the core requirement: *"The Correction Engine MUST NOT arbitrarily modify campaign variables. All corrective actions must be aligned with CampaignContext."*

The `ConstraintGuard` implements strict immutability checks across every correction cycle:
1. **Total Budget & Currency**: The total allocated budget and currency cannot be modified by any corrective task.
2. **Business Identity**: Company name, industry vertical, and tagline cannot be altered.
3. **Product Specification**: Product name, SKU type, and core capabilities remain immutable.
4. **Brand Guidelines**: Official hex color palettes and typography rules cannot be overridden.
5. **Tampering Auto-Recovery**: In the event an upstream agent accidentally mutates invariant fields during re-execution, `ConstraintGuard.restore_invariants()` automatically rolls back invariant fields to baseline snapshots.

---

## 12 Verified Correction Scenarios (`tests/test_correction_engine_phase11.py`)

All 12 comprehensive scenario tests execute deterministically and pass:

1. **Scenario 1 — Low CTR**: Performance deviation ($0.85\%$ observed vs. $2.50\%$ target) diagnosed, routed to `content_agent`, generated headline directives, verified constraint preservation.
2. **Scenario 2 — Poor Aesthetic Quality**: Visual aesthetic score ($4.8/10.0$) diagnosed, routed to `design_agent`, negative prompt injected, passed quality checks.
3. **Scenario 3 — Brand Safety & Policy Violation**: Critical policy defect flagged, prioritized as Severity CRITICAL, injected safety constraint directives.
4. **Scenario 4 — Audience Persona Disconnect**: Human reviewer feedback on persona mismatch routed to `strategy_agent`, realigned messaging pillars.
5. **Scenario 5 — High Customer Acquisition Cost (CAC)**: High CPA ($82.50 vs $45.00) routed to `optimization_agent`, cooled bid scale factor and adjusted channel weights.
6. **Scenario 6 — Health Score Quality Gate Failure (< 70.0)**: Analytics overall health score of $58.0/100$ triggered remediation loop on `content_agent`.
7. **Scenario 7 — Invalid RL Action Proposal**: Simplex constraint violation in RL channel allocation routed to `optimization_agent` for projected bounded rebalancing.
8. **Scenario 8 — Human Rejection Directives**: Direct human copy critique integrated into prompt payload and routed to `content_agent`.
9. **Scenario 9 — Multiple Concurrent Multi-Agent Failures**: Simultaneous CV score defect + low CTR + high CPA triaged and dispatched in priority order across `design_agent`, `content_agent`, and `optimization_agent`.
10. **Scenario 10 — Circuit Breaker Ceiling (Max Retries Exceeded)**: When loop attempt reached 3, automated execution halted, `circuit_breaker_triggered = True` was asserted, and execution transitioned to HITL escalation.
11. **Scenario 11 — Strict Invariant Tampering Detection & Recovery**: Illegal mutations to `total_budget` ($999,999) and `business_name` were detected, blocked, and auto-restored by `ConstraintGuard`.
12. **Scenario 12 — Master Orchestrator Stage 9 Integration**: Full Master Pipeline executed through Stage 9 `correction_engine`, asserting status `WorkflowState.SUCCESS` and recorded output in `CampaignContext`.

---

## Test & Verification Results

- **Phase 11 Scenario Test Suite:** `pytest tests/test_correction_engine_phase11.py -v` $\to$ **12/12 PASSED**
- **Phase 11 Standalone Verification:** `python scripts/verify_phase11.py` $\to$ **28/28 CHECKS PASSED**
- **Repository Full Regression Suite:** `pytest tests/ -v` $\to$ **166/166 PASSED (0 failures)**
- **Lint & Static Type Quality:** `ruff check` $\to$ **Clean (0 errors)**
