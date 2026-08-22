# Campaign Lifecycle & Execution State Machine

**Status:** [IMPLEMENTED]  
**State Machine:** `src/adpilot/models/campaign_task.py`  

---

## 1. Lifecycle State Machine Diagram

```mermaid
stateDiagram-v2
    [*] --> PENDING : User Brief Ingested
    PENDING --> IN_PROGRESS : Orchestrator Runner Start
    
    state IN_PROGRESS {
        ContextBuilding --> ProductClassification
        ProductClassification --> ExecutionPlanning
        ExecutionPlanning --> StrategyFormulation
        StrategyFormulation --> MarketResearch
        MarketResearch --> CompetitorIntelligence
        CompetitorIntelligence --> ContentCopywriting
        ContentCopywriting --> CreativeStudio
        CreativeStudio --> CVQualityGate
        CVQualityGate --> PredictiveAnalytics
        PredictiveAnalytics --> RLOptimization
        RLOptimization --> ConstraintCorrection
    }

    IN_PROGRESS --> AWAITING_HITL : High-Risk Decision Detected
    AWAITING_HITL --> IN_PROGRESS : Human Signed Approval
    AWAITING_HITL --> REJECTED : Human Rejection
    
    IN_PROGRESS --> PUBLISHING : HITL Cleared
    PUBLISHING --> LIVE_MONITORING : Ad Networks Ingested
    LIVE_MONITORING --> COMPLETED : All Milestones Met
    IN_PROGRESS --> FAILED : Unhandled System Error
```

---

## 2. Execution Telemetry & Stage Checkpoints
- **Progress Counter:** Stages $1 \to 18$ map to $0\% \to 100\%$ linear completion indicators.
- **Trace Persistence:** Intermediate stage JSON artifacts are persisted in SQLite `campaign_tasks` table so failed runs can resume without re-running completed stages.
