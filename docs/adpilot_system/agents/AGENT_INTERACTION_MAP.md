# Agent Interaction Map

**Status:** [IMPLEMENTED]  
**Communication Protocol:** Strictly Typed Pydantic v2 In-Memory Contracts  

---

## 1. Master Agent Communication Sequence

```mermaid
graph TD
    BriefIn[User Campaign Brief] --> CB[Context Builder]
    CB -->|CampaignContext| PC[Product Classifier]
    PC -->|ProductClassification| Planner[Planner Agent]
    Planner -->|ExecutionPlan| SA[Strategy Agent]
    
    SA -->|StrategyAgentOutput| RA[Research Agent]
    SA -->|StrategyAgentOutput| CA[Competitor Agent]
    
    RA -->|ResearchAgentOutput| Content[Content Agent]
    CA -->|CompetitorOutput| Content
    
    Content -->|ContentAgentOutput| DA[Design Agent]
    DA -->|DesignAgentOutput| CV[CV Agent]
    
    Content -->|Ad Copy & Sentiment| AA[Analytics Agent]
    CV -->|Aesthetic & Contrast Scores| AA
    
    AA -->|Predicted ROAS & CAC| Opt[RL Policy Optimizer PPO]
    Opt -->|Recommended Allocations| CE[Correction Engine]
    
    CE -->|Cleaned Contracts| HITL{HITL Review Gate}
    HITL -->|Signed Decision| Pub[Publishing Agent]
    
    Pub -->|Live Campaign IDs| Mon[Monitoring Agent]
    Mon -->|Live Deviations & Signals| FB[Feedback Engine]
    FB -->|Experience Tuples| Opt
    FB -->|Campaign Artefacts| RAG[(Global RAG & Memory)]

    classDef agent fill:#0B0F19,stroke:#06B6D4,stroke-width:2px,color:#F8FAFC;
    classDef gate fill:#0B0F19,stroke:#F43F5E,stroke-width:2px,color:#F8FAFC;
    classDef model fill:#0B0F19,stroke:#8B5CF6,stroke-width:2px,color:#F8FAFC;
    
    class CB,PC,Planner,SA,RA,CA,Content,DA,CE,Pub,Mon,FB agent;
    class HITL gate;
    class CV,AA,Opt,RAG model;
```

---

## 2. Interaction Contract Matrix

| Source Agent | Produced Contract | Target Consumer(s) | Transport Mechanism |
|---|---|---|---|
| **Context Builder** | `CampaignContext` | Product Classifier, Planner, Strategy | In-Memory Reference |
| **Product Classifier** | `ProductClassification` | Planner Agent, Strategy Agent | In-Memory Reference |
| **Planner Agent** | `ExecutionPlan` | Master Orchestrator, Strategy Agent | In-Memory Reference |
| **Strategy Agent** | `StrategyAgentOutput` | Research Agent, Competitor Agent, Content Agent | In-Memory Reference |
| **Research Agent** | `ResearchAgentOutput` | Competitor Agent, Audience Agent, Content Agent | In-Memory Reference |
| **Competitor Agent** | `CompetitorOutput` | Content Agent, Strategy Agent | In-Memory Reference |
| **Content Agent** | `ContentAgentOutput` | Design Agent, Analytics Agent, Publishing Agent | In-Memory Reference |
| **Design Agent** | `DesignAgentOutput` | CV Agent, Publishing Agent, Creative Studio | In-Memory Reference |
| **CV Agent** | `CVScoreOutput` | Analytics Agent, Correction Engine | In-Memory Reference |
| **Analytics Agent** | `AnalyticsAgentOutput` | RL Optimizer, Executive Dashboard | In-Memory Reference |
| **RL Optimizer** | `OptimizationOutput` | Correction Engine, HITL Gate, Publishing Agent | In-Memory Reference |
| **Correction Engine** | `CorrectionOutput` | HITL Gate, Master Orchestrator | In-Memory Reference |
| **HITL Gate** | `HITLDecisionRecord` | Publishing Agent, Audit Ledger | HMAC-SHA256 Signed Event |
| **Publishing Agent** | `PublishingResult` | Monitoring Agent, Executive Dashboard | Async REST HTTP |
| **Monitoring Agent** | `MonitoringEvent` | Feedback Engine, Live Activity Feed | Event Bus Stream |
| **Feedback Engine** | `PolicyBufferUpdate` | RL Policy Optimizer (PPO Buffer) | PyTorch Tensor Queue |
