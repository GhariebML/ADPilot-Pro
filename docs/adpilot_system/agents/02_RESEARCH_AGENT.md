# Research Agent

## 1. Purpose
The **Research Agent** conducts synthetic market research, derives Ideal Customer Profiles (ICPs), uncovers core customer pain points, and extracts relevant industry macroeconomic trends.

## 2. Business Responsibility
Grounds marketing copy and visual design in authentic audience psychology and market realities, preventing disconnected generic pitches.

## 3. Technical Responsibility
Ingests `CampaignContext` and `StrategyAgentOutput`, performs semantic retrieval over persona memory in Qdrant, prompts the research LLM, and formats structured buyer profiles into `ResearchAgentOutput`.

## 4. Source Code
- `src/adpilot/agents/research_agent.py`
- System Prompt: `src/adpilot/prompts/research_system_prompt.md`

## 5. Input
- **Schema:** `StrategyAgentOutput` + `CampaignContext`
  - Strategic positioning
  - Target vertical
  - Core market themes

## 6. Processing Flow
1. Query Customer Memory Tier in Qdrant for matching historical personas.
2. Formulate prompt injecting industry trends and psychological pain hooks.
3. Call LLM (Claude 3.5 Sonnet / GPT-4o) with strict Pydantic formatting.
4. Synthesize personas, pain points, purchase objections, and market catalysts.

## 7. Models Used
- **Foundation LLM:** Anthropic Claude 3.5 Sonnet / OpenAI GPT-4o Router.

## 8. Tools Used
- Persona Memory Service (`src/adpilot/memory/customer.py`)
- FastEmbed Vector Retriever (`src/adpilot/rag/engine.py`)

## 9. Output
- **Schema:** `ResearchAgentOutput`
  - `primary_persona: Dict[str, Any]` (Demographics, Title, Goals, Frustrations)
  - `secondary_personas: List[Dict[str, Any]]`
  - `key_pain_points: List[str]`
  - `market_trends: List[str]`
  - `buying_triggers: List[str]`

## 10. Downstream Consumers
- `AudienceAgent` & `CompetitorAgent`
- `ContentAgent` (addresses specific pain points in copy)
- `DesignAgent` (reflects persona tone in visual style)

## 11. Error Handling
- Schema validation fallbacks; defaults to baseline demographic distributions if retrieval is empty.

## 12. Validation
- Verifies that at least 3 distinct pain points and 1 primary persona are returned.

## 13. Corrective Actions
- If personas fail downstream relevance tests, triggers targeted re-prompting with narrowed constraints.

## 14. Human-in-the-Loop
- Reviewers can view and adjust persona pain points in the Campaign Control Bar.

## 15. Example Execution
```json
{
  "primary_persona": {
    "title": "VP of Growth & Performance Marketing",
    "company_size": "50-500 employees",
    "core_goal": "Maximize blended ROAS across fragmented paid media channels",
    "biggest_frustration": "Manual weekly budget spreadsheets and human delay"
  },
  "key_pain_points": [
    "Slow campaign iteration cycles taking 2+ weeks per variant",
    "Ad fatigue causing CTR decay without automated alert triggers",
    "Difficulty predicting cross-channel attribution returns"
  ],
  "market_trends": ["Shift towards autonomous agentic media buying", "Zero-party data prioritization"]
}
```

## 16. Implementation Status
[IMPLEMENTED]
