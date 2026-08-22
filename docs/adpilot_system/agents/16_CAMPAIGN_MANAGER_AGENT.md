# Campaign Manager Agent

## 1. Purpose
The **Campaign Manager Agent** coordinates end-to-end campaign lifecycle packaging, structures A/B test split plans, formulates experimentation hypotheses, and aggregates multi-agent deliverables into launch-ready client packages.

## 2. Business Responsibility
Ensures all multi-agent deliverables (strategy, copy, assets, budgets, schedules) are synthesized into a coherent, executive-ready marketing plan with clear hypothesis testing roadmaps.

## 3. Technical Responsibility
Ingests outputs from all upstream agents, constructs comprehensive A/B experimentation matrices, compiles ZIP asset bundles, and outputs `CampaignManagerOutput`.

## 4. Source Code
- `src/adpilot/agents/campaign_manager_agent.py`
- System Prompt: `src/adpilot/prompts/campaign_manager_system_prompt.md`

## 5. Input
- Comprehensive multi-agent context (Strategy, Research, Content, Design, Analytics, Optimization).

## 6. Processing Flow
1. Ingest all pipeline outputs from execution context.
2. Formulate A/B testing hypotheses (e.g., Pain-point Headline vs Benefit Headline).
3. Structure campaign rollout timeline and budget deployment phases.
4. Package assets into downloadable ZIP structures.
5. Emit `CampaignManagerOutput`.

## 7. Models Used
- Foundation LLM (GPT-4o Router) / Deterministic Packager.

## 8. Tools Used
- Asset Packager Service (`src/adpilot/services/asset_packager.py`)

## 9. Output
- **Schema:** `CampaignManagerOutput`
  - `ab_test_plan: List[Dict[str, Any]]` (Variant A vs B, Hypothesis, Sample Size)
  - `rollout_schedule: Dict[str, str]` (Phase 1, Phase 2, Phase 3)
  - `executive_summary: str`

## 10. Downstream Consumers
- `ResultDisplay` (renders campaign brief and A/B test view)
- `PublishingAgent` (sets initial A/B test traffic split parameters)

## 11. Error Handling
- Safe default 50/50 traffic split if experimental configuration is missing.

## 12. Validation
- Checks that all ad creative variants have matching landing page destinations.

## 13. Corrective Actions
- Re-aligns experimental variables if more than 1 variable is altered in an A/B pair.

## 14. Human-in-the-Loop
- Experimentation parameters can be viewed and edited in the Campaign Brief Review view.

## 15. Example Execution
```json
{
  "ab_test_plan": [
    {
      "test_name": "Headline Hook Experiment",
      "variant_a": "Stop Manually Tuning Ad Budgets (Pain Point)",
      "variant_b": "Boost Blended ROAS by +28% with RL (Benefit)",
      "traffic_split": "50/50",
      "target_sample_size": 2500
    }
  ],
  "rollout_schedule": {
    "Day 1-3": "Initial audience calibration ($1,500 spend)",
    "Day 4-14": "PPO continuous policy rebalancing ($8,500 spend)"
  }
}
```

## 16. Implementation Status
[IMPLEMENTED]
