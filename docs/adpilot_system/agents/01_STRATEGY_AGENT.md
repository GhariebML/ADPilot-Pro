# Strategy Agent

## 1. Purpose
The **Strategy Agent** defines the high-level marketing positioning, selects optimal advertising channels, segments the marketing funnel into distinct tiers (TOFU, MOFU, BOFU), and establishes the narrative angle for the campaign.

## 2. Business Responsibility
Prevents generic, unfocused advertising by tailoring messaging frameworks to the target vertical, selecting high-ROI distribution channels, and formulating cohesive value propositions.

## 3. Technical Responsibility
Ingests `CampaignContext` or `ExecutionPlan`, invokes the foundation LLM router with strict Pydantic prompt formatting, validates the response against `StrategyAgentOutput`, and passes structured positioning downstream.

## 4. Source Code
- `src/adpilot/agents/strategy_agent.py`
- System Prompt: `src/adpilot/prompts/strategy_system_prompt.md`

## 5. Input
- **Schema:** `CampaignContext`
  - `product_name: str`
  - `description: str`
  - `goals: List[CampaignGoal]`
  - `budget: float`
  - `target_audience: Optional[str]`

## 6. Processing Flow
1. Receive and validate input `CampaignContext`.
2. Retrieve relevant market playbooks from RAG knowledge store.
3. Build prompt with positioning rules and marketing funnel templates.
4. Execute LLM call via Provider Router (OpenAI GPT-4o / Claude 3.5).
5. Parse and validate JSON against `StrategyAgentOutput`.

## 7. Models Used
- **Foundation LLM:** OpenAI GPT-4o / OpenRouter (Temperature: 0.2).

## 8. Tools Used
- Provider Router (`src/adpilot/services/provider_router.py`)
- RAG Knowledge Service (`src/adpilot/services/rag_service.py`)

## 9. Output
- **Schema:** `StrategyAgentOutput`
  - `positioning_statement: str`
  - `selected_channels: List[MarketingChannel]` (e.g., LinkedIn, Meta, Google)
  - `funnel_strategy: Dict[str, str]` (TOFU / MOFU / BOFU messaging)
  - `key_messaging_pillars: List[str]`

## 10. Downstream Consumers
- `ResearchAgent` (builds ICP profiles matching strategy)
- `CompetitorAgent` (compares positioning against rivals)
- `ContentAgent` (drafts copy aligned with messaging pillars)

## 11. Error Handling
- Automatic retry on JSON formatting errors (max 3 retries).
- Fallback to rule-based positioning template if LLM provider fails.

## 12. Validation
- Pydantic schema validation ensuring non-empty channel lists and valid channel enums.

## 13. Corrective Actions
- If `AnalyticsAgent` flags low strategy-market fit, re-routes with modified constraints.

## 14. Human-in-the-Loop
- Strategy roadmap can be reviewed and edited by Campaign Director before copy generation.

## 15. Example Execution
```json
{
  "positioning_statement": "The only autonomous AI operating system delivering real-time PPO ad budget optimization.",
  "selected_channels": ["LINKEDIN", "META", "GOOGLE_SEARCH"],
  "funnel_strategy": {
    "TOFU": "Awareness of AI marketing automation inefficiency",
    "MOFU": "Technical demonstration of continuous PPO optimization",
    "BOFU": "Enterprise pilot deployment and ROI guarantee"
  },
  "key_messaging_pillars": ["Autonomous Policy Rebalancing", "Zero Hallucination", "Cryptographic Governance"]
}
```

## 16. Implementation Status
[IMPLEMENTED]
