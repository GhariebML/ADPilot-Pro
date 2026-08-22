# Content Agent

## 1. Purpose
The **Content Agent** generates high-converting, platform-tailored copywriting across multiple marketing formats: paid ads (Google Search, Meta, LinkedIn), nurture email sequences, and social media feed posts.

## 2. Business Responsibility
Produces authentic, persuasive, and brand-aligned marketing copy that engages buyers, communicates core value propositions, and drives conversion actions.

## 3. Technical Responsibility
Ingests positioning, persona insights, and competitor differentiators, enforces character count limits per ad network, applies brand voice rules, and formats output into `ContentAgentOutput`.

## 4. Source Code
- `src/adpilot/agents/content_agent.py`
- System Prompt: `src/adpilot/prompts/content_system_prompt.md`
- Quality Scorer: `src/adpilot/agents/content_evaluator.py`

## 5. Input
- **Schema:** `StrategyAgentOutput` + `ResearchAgentOutput` + `CompetitorOutput`
- Optimization Hints (if called via self-correcting feedback loop)

## 6. Processing Flow
1. Load brand tone safeguards and banned word lists from Brand Memory Tier.
2. Formulate platform-specific copy variants (Short-form, Long-form, PAS, AIDA).
3. Call Claude 3.5 Sonnet (or GPT-4o) with structured Pydantic schema enforcement.
4. Execute `ContentEvaluator` quality scoring:
   - If Health Score $< 70$, extract feedback hints and retry (up to 3 times).
   - If Health Score $\ge 70$, finalize `ContentAgentOutput`.

## 7. Models Used
- **Foundation LLM:** Anthropic Claude 3.5 Sonnet / OpenAI GPT-4o Router.
- **Scoring Model:** Custom Scikit-Learn Brand Voice Classifier (`research/models/content/brand_voice_classifier.pkl`).

## 8. Tools Used
- Brand Memory Service (`src/adpilot/memory/brand.py`)
- Content Quality Evaluator (`src/adpilot/agents/content_evaluator.py`)

## 9. Output
- **Schema:** `ContentAgentOutput`
  - `ads: List[AdContent]` (Platform, Headline, Body, CTA, Estimated CTR)
  - `email_sequences: List[EmailSequence]` (Subject, Preview, Body, Stage)
  - `social_posts: List[SocialPost]` (Platform, Content, Hashtags, Format)
  - `summary: str`

## 10. Downstream Consumers
- `DesignAgent` & `CreativeAgent` (extracts visual prompts for each ad copy)
- `AnalyticsAgent` (scores projected financial conversion rates)
- `PublishingAgent` (populates ad creative payloads)

## 11. Error Handling
- Character overflow truncation matching ad network constraints (e.g., Google Headlines $\le 30$ chars).
- Automatic hint extraction and regeneration loop on low quality score.

## 12. Validation
- Enforces non-empty headlines, non-empty CTAs, and exact platform enum validity.

## 13. Corrective Actions
- If feedback loops flag repetitive phrasing, temperature is bumped dynamically (+0.1) to increase diversity.

## 14. Human-in-the-Loop
- Copy can be edited, approved, or revised directly in the Result Display view.

## 15. Example Execution
```json
{
  "ads": [
    {
      "platform": "LINKEDIN",
      "headline": "Stop Manually Tuning Ad Budgets",
      "body": "ADPilot Pro uses continuous PPO reinforcement learning to rebalance ad spend in real time. Boost blended ROAS by +28%.",
      "cta": "Request Enterprise Access",
      "performance": "High (Est. CTR 2.4%)"
    }
  ],
  "social_posts": [
    {
      "platform": "TWITTER",
      "content": "Why are growth teams still spending 15 hrs/week in ad spreadsheets? Autonomous agentic marketing is here.",
      "hashtags": ["#AI", "#MarTech", "#GrowthHacking"]
    }
  ]
}
```

## 16. Implementation Status
[IMPLEMENTED]
