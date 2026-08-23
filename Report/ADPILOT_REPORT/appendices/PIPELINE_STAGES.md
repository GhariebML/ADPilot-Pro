# Appendix E — 18-Stage Execution Lifecycle Reference

Complete execution stages executed by ADPilot Pro:

| Stage # | Stage Name | Category | Primary Executing Agent | Ingress Payload | Egress Payload |
|---|---|---|---|---|---|
| **01** | `INGESTION` | Input | Campaign Manager | Client Brief JSON | `CampaignContext` |
| **02** | `TAXONOMY` | Classification | Product Classifier | Business Info | Vertical Classification |
| **03** | `AUDIENCE_MODELING` | Audience | Audience Agent | Product Spec | Demographics & Personas |
| **04** | `COMPETITOR_INTEL` | Research | Competitor Agent | Audience Profile | Market Positioning Matrix |
| **05** | `STRATEGY_SYNTHESIS` | Strategy | Strategy Agent | Competitor Data | Channel Allocation Plan |
| **06** | `SECTOR_RESEARCH` | Knowledge | Research Agent | Strategy Output | Keyword & RAG Vectors |
| **07** | `COPYWRITING` | Creative | Content Agent | Strategic Angle | Multi-Channel Ad Copies |
| **08** | `COPY_EVALUATION` | Quality Gate | Content Evaluator | Ad Copies | Readability Score |
| **09** | `VISUAL_COMPOSITION` | Creative | Design Agent | Copy & Brand Tone | Multi-Format Image Briefs |
| **10** | `IMAGE_SYNTHESIS` | Generation | Gemini Nano Banana | Design Briefs | Native 4-Format Visuals |
| **11** | `CREATIVE_PACKAGING` | Assembly | Creative Agent | Images + Copy | Assembled Asset Bundle |
| **12** | `CV_AESTHETIC_AUDIT` | Vision Gate | CV Agent | Creative Assets | CLIP Score & WCAG AAA |
| **13** | `KPI_FORECASTING` | Analytics | Analytics Agent | Strategy + Creatives | Predicted CTR / ROAS |
| **14** | `HEURISTIC_TUNING` | Optimization | Optimization Agent | Analytics Data | Tuning Recommendations |
| **15** | `PPO_REALLOCATION` | Reinforcement | RL / PPO Optimizer | Performance State | Budget Shift Delta $\Delta b$ |
| **16** | `CORRECTION_ROUTING` | Governance | Correction Agent | Optimization Deltas | Feedback Loops |
| **17** | `HITL_GOVERNANCE` | Governance | Human Review Gate | Risk Index | Cryptographic Approval |
| **18** | `DISPATCH_MONITOR` | Deployment | Publishing Agent | Approved Assets | Live Telemetry Stream |
