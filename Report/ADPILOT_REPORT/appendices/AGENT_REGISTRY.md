# Appendix A — Master Agent Registry

Comprehensive technical catalog of all 18 autonomous agents in the ADPilot Pro fleet.

| ID | Agent Name | Python File Path | Class Name | Base Class | Primary Model | Decision Authority | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **AG-01** | **Campaign Manager Agent** | `src/adpilot/agents/campaign_manager_agent.py` | `CampaignManagerAgent` | `BaseAgent` | GPT-4o / Claude 3.5 | Orchestrates DAG execution | `[IMPLEMENTED]` |
| **AG-02** | **Product Classifier Agent** | `src/adpilot/agents/product_classifier_agent.py` | `ProductClassifierAgent` | `BaseAgent` | Scikit / GPT-4o | Sets offering taxonomy | `[IMPLEMENTED]` |
| **AG-03** | **Audience Agent** | `src/adpilot/agents/audience_agent.py` | `AudienceAgent` | `BaseAgent` | GPT-4o | Defines ICP & targeting | `[IMPLEMENTED]` |
| **AG-04** | **Competitor Agent** | `src/adpilot/agents/competitor_agent.py` | `CompetitorAgent` | `BaseAgent` | Claude 3.5 Sonnet | Maps rival landscape | `[IMPLEMENTED]` |
| **AG-05** | **Strategy Agent** | `src/adpilot/agents/strategy_agent.py` | `StrategyAgent` | `BaseAgent` | Claude 3.5 Sonnet | Macro campaign strategy | `[IMPLEMENTED]` |
| **AG-06** | **Research Agent** | `src/adpilot/agents/research_agent.py` | `ResearchAgent` | `BaseAgent` | GPT-4o + FastEmbed | Sector keyword research | `[IMPLEMENTED]` |
| **AG-07** | **Content Agent** | `src/adpilot/agents/content_agent.py` | `ContentAgent` | `BaseAgent` | GPT-4o / Claude 3.5 | Multi-channel copywriter | `[IMPLEMENTED]` |
| **AG-08** | **Content Evaluator** | `src/adpilot/agents/content_evaluator.py` | `ContentEvaluator` | `BaseAgent` | Scikit Classifier | Copy quality gate | `[IMPLEMENTED]` |
| **AG-09** | **Design Agent** | `src/adpilot/agents/design_agent.py` | `DesignAgent` | `BaseAgent` | Gemini Nano Banana | Visual asset composer | `[IMPLEMENTED]` |
| **AG-10** | **Creative Agent** | `src/adpilot/agents/creative_agent.py` | `CreativeAgent` | `BaseAgent` | Custom Assembler | Multi-format packager | `[IMPLEMENTED]` |
| **AG-11** | **Creative Evaluator** | `src/adpilot/agents/creative_evaluator.py` | `CreativeEvaluator` | `BaseAgent` | Rule & Metric Engine | Design compliance gate | `[IMPLEMENTED]` |
| **AG-12** | **CV Agent** | `src/adpilot/agents/cv_agent.py` | `CVAgent` | `BaseAgent` | CLIP-ViT / ONNX | Visual aesthetic grading | `[IMPLEMENTED]` |
| **AG-13** | **Analytics Agent** | `src/adpilot/agents/analytics_agent.py` | `AnalyticsAgent` | `BaseAgent` | Custom ONNX | KPI & ROAS forecasting | `[IMPLEMENTED]` |
| **AG-14** | **Optimization Agent** | `src/adpilot/agents/optimization_agent.py` | `OptimizationAgent` | `BaseAgent` | Rule Engine | Parameter tuning | `[IMPLEMENTED]` |
| **AG-15** | **RL / PPO Optimizer** | `src/adpilot/services/ai_optimizer.py` | `AIOptimizer` | `BaseService` | PPO Policy Net | Channel budget shifts | `[PARTIAL]` |
| **AG-16** | **Correction Agent** | `src/adpilot/agents/correction_agent.py` | `CorrectionAgent` | `BaseAgent` | Rule Engine | Anomaly & rollback loop | `[IMPLEMENTED]` |
| **AG-17** | **Publishing Agent** | `src/adpilot/agents/publishing_agent.py` | `PublishingAgent` | `BaseAgent` | Connector Suite | Ad network dispatcher | `[IMPLEMENTED]` |
| **AG-18** | **Monitoring Agent** | `src/adpilot/agents/monitoring_agent.py` | `MonitoringAgent` | `BaseAgent` | Stats Aggregator | Live telemetry listener | `[IMPLEMENTED]` |
