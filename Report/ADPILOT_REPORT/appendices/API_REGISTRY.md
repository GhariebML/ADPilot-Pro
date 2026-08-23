# Appendix C — REST API Registry

Comprehensive specification of active FastAPI routes in ADPilot Pro.

| Method | Endpoint Path | Tag | Request Body | Response Schema | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `GET` | `/healthz` | System | None | `{"status": "healthy"}` | Liveness & database connection probe |
| `POST` | `/api/v1/simulations` | Simulation | `SimulationCreateReq` | `{"simulation_id": str}` | Initializes new campaign simulation |
| `POST` | `/api/v1/simulations/{id}/run` | Simulation | None | `{"status": "started"}` | Triggers async background 15-agent simulation run |
| `GET` | `/api/v1/simulations/{id}` | Simulation | None | `CampaignSimulation` | Retrieves real-time simulation execution telemetry |
| `POST` | `/api/v1/simulations/{id}/approve` | Simulation | None | `{"status": "approved"}` | Approves HITL gate and records final metrics |
| `POST` | `/api/v1/simulations/{id}/human-review` | Simulation | `HITLReq` | `{"status": "decision_recorded"}` | Submits human review decision & feedback |
| `POST` | `/api/creative/generate` | Creative | `dict` (Product, Goal, Style) | `{"status": "success", "creative_assets": []}` | Generates 4-format visual creatives via Gemini |
| `POST` | `/api/campaigns/run` | Pipeline | `CampaignInput` | `OrchestratorOutput` | Runs complete production DAG workflow |
| `POST` | `/api/analytics/evaluate` | Analytics | `AnalyticsAgentInput` | `AnalyticsAgentOutput` | Standalone analytics quality gate evaluation |
