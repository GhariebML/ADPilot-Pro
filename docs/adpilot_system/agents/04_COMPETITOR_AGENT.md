# Competitor Agent

## 1. Purpose
The **Competitor Agent** identifies primary market competitors, evaluates their messaging and pricing strategies, and constructs a competitive moat matrix with actionable differentiation angles.

## 2. Business Responsibility
Prevents generic "me-too" positioning by finding weaknesses in competitors' value propositions and arming copywriting with compelling competitive wedges.

## 3. Technical Responsibility
Ingests `CampaignContext` and `ResearchAgentOutput`, executes competitive search lookups (via search services / RAG), prompts the LLM for gap analysis, and emits `CompetitorOutput`.

## 4. Source Code
- `src/adpilot/agents/competitor_agent.py`

## 5. Input
- `product_name: str`
- `description: str`
- `target_audience: str`
- `market_trends: List[str]`

## 6. Processing Flow
1. Query search service / competitor memory for rival brands in the same category.
2. Analyze rival feature matrices, typical pricing models, and public customer complaints.
3. Formulate comparative moat matrix highlighting unique brand advantages.
4. Output structured differentiation hooks for copywriters.

## 7. Models Used
- Foundation LLM: OpenAI GPT-4o / OpenRouter.

## 8. Tools Used
- Search Service (`src/adpilot/services/search_service.py`)
- Competitor Memory Store (`src/adpilot/memory/manager.py`)

## 9. Output
- **Schema:** `CompetitorOutput`
  - `top_competitors: List[Dict[str, str]]` (Name, Strengths, Weaknesses)
  - `differentiation_matrix: Dict[str, str]` (Our Moat vs Rival Feature)
  - `competitive_angles: List[str]` (Specific copy hooks)

## 10. Downstream Consumers
- `ContentAgent` (embeds differentiation hooks directly into ad headlines)
- `StrategyAgent` (updates channel positioning)

## 11. Error Handling
- Fallbacks to generic competitive positioning if rival search lookups time out.

## 12. Validation
- Verifies at least 2 distinct competitors and 3 differentiation angles.

## 13. Corrective Actions
- Re-runs analysis if competitor claims are flagged as legally unprovable or overly aggressive.

## 14. Human-in-the-Loop
- Reviewers can view competitor matrix in the Observatory drawer.

## 15. Example Execution
```json
{
  "top_competitors": [
    {
      "name": "Legacy AdPlatform",
      "weakness": "Requires manual rule configuration; no continuous RL policy",
      "strength": "High brand recognition"
    }
  ],
  "differentiation_matrix": {
    "Optimization Speed": "Real-time PPO policy updates vs weekly manual human adjustments",
    "Creative Safety": "Automated CLIP-ViT contrast & aesthetic checks vs manual review"
  },
  "competitive_angles": [
    "Stop wasting 15 hours/week tuning ad budgets in spreadsheets.",
    "The first AI marketing OS with mathematically bound Dirichlet budget constraints."
  ]
}
```

## 16. Implementation Status
[IMPLEMENTED]
