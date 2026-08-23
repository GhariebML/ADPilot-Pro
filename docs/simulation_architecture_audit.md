# Simulation Architecture Audit

## 1. Existing Agents
The system currently implements:
- ProductClassifierAgent
- StrategyAgent
- ResearchAgent
- CompetitorAgent
- ContentAgent
- DesignAgent (integrated with Gemini)
- CVAgent
- AnalyticsAgent
- OptimizationAgent
- PublishingAgent
- MonitoringAgent

## 2. Existing Agent Execution Interfaces
All agents inherit from BaseAgent[InputT, OutputT]. They expose un(context: CampaignContext, ...) and return the updated CampaignContext.

## 3. Existing Pipeline / Orchestration
MasterPipelineRunner in src/adpilot/orchestrator/pipeline_runner.py executes an 18-stage DAG sequentially, passing CampaignContext forward.

## 4. Existing ML Models
- FastText / Heuristic Taxonomy Classifier (Product Classification)
- ML Ridge Copy Quality Scorer (Content)
- ML Aesthetic Scorer / CLIP-ViT (Design/CV)
- Sklearn Ridge Forecaster + StandardScaler (Analytics)

## 5. Existing RL/PPO Implementation
OptimizationAgent is invoked at Stage 12, running a PPO optimization for budget and channel reallocation.

## 6. Existing Campaign Input Schema
CampaignInput, CampaignContext (v2.0) with constraints, budget, brand guidelines, tone of voice.

## 7. Existing Analytics
AnalyticsAgent predicts CPA, ROAS, and evaluates a composite health score.

## 8. Existing Design Generation
DesignAgent generates a creative specification and invokes GeminiImageGenerationProvider (recently integrated).

## 9. Existing Constraints
CampaignConstraints handles min/max budget allocations, max CPA, min ROAS. Used by the CorrectionEngine.

## 10. Existing HITL
HITLReviewManager intercepts the context at Stage 14, awaiting human approval before publishing.

## 11. Existing Artifact Storage
MemoryManager and ArtifactRegistry handle storage of assets.

## 12. Existing APIs
POST /api/campaigns/run executes the pipeline. 

## 13. Existing Frontend Components
Interactive DAGs, Creative Studio, Agent Observatory exist, but no unified /simulation stepper page.

## 14. Components that can be directly reused
The entire suite of Agents, the underlying ML models, Gemini Provider, and the execution schemas can be directly reused.

## 15. Components requiring simulation adapters
- The MasterPipelineRunner normally publishes and runs fully automated. A SimulationPipelineRunner or a wrapper is needed to execute step-by-step and capture AgentExecutionTrace / SimulationEvent without triggering actual publishing.
- The OptimizationAgent (PPO) might need a simulation harness to visually expose state -> action -> reward since it currently executes silently.

## 16. Missing Components
- Unified Simulation Domain Models (CampaignSimulation, SimulationEvent, AgentExecutionTrace).
- Database models or in-memory persistence for Simulation data.
- API endpoints (/api/v1/simulations/*).
- /simulation frontend dashboard matching the complex enterprise layout requested (Timeline, Agent Inspector, RL Panel).
