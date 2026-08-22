# Product Classifier Agent

## 1. Purpose
The **Product Classifier Agent** analyzes the product name, description, and target objectives to categorize the offering into its specific commercial vertical (`B2B_SAAS`, `PHYSICAL_PRODUCT`, `REAL_ESTATE`, `SERVICE`, `FINTECH`, `ECOMMERCE`) and extract business model attributes.

## 2. Business Responsibility
Prevents mismatched marketing strategies by ensuring that B2B SaaS products receive lead-generation funnel frameworks rather than impulse-buy e-commerce tactics.

## 3. Technical Responsibility
Ingests raw `CampaignContext`, matches against taxonomy embeddings and few-shot classification prompts via GPT-4o, validates against `ProductClassification`, and outputs vertical metadata.

## 4. Source Code
- `src/adpilot/agents/product_classifier_agent.py`
- System Prompt: `src/adpilot/prompts/product_classifier_system_prompt.md`

## 5. Input
- `product_name: str`
- `description: str`
- `target_audience: Optional[str]`
- `goals: List[str]`

## 6. Processing Flow
1. Ingest raw product text from context.
2. Formulate classification prompt injecting commercial vertical definitions and business model criteria.
3. Call GPT-4o with structured Pydantic schema enforcement.
4. Output structured classification metadata and confidence score.

## 7. Models Used
- Foundation LLM: OpenAI GPT-4o Router.

## 8. Tools Used
- Provider Router (`src/adpilot/services/provider_router.py`)

## 9. Output
- **Schema:** `ProductClassification`
  - `vertical: str` (`B2B_SAAS`, `PHYSICAL_PRODUCT`, `REAL_ESTATE`, `SERVICE`)
  - `business_model: str` (`SUBSCRIPTION`, `ONE_TIME_PURCHASE`, `HIGH_TICKET_LEAD_GEN`)
  - `complexity_level: str` (`LOW`, `MEDIUM`, `HIGH`)
  - `confidence_score: float` (0.0 - 1.0)

## 10. Downstream Consumers
- `PlannerAgent` (adjusts pipeline roadmap milestones based on vertical)
- `StrategyAgent` (selects vertical-specific channels)

## 11. Error Handling
- Defaults to `B2B_SAAS` with a `0.50` confidence flag if input text is ambiguous.

## 12. Validation
- Strict enum validation against supported commercial verticals.

## 13. Corrective Actions
- Re-prompts with explicit feature extraction if confidence $< 0.70$.

## 14. Human-in-the-Loop
- User can override detected vertical in the Campaign Brief Form.

## 15. Example Execution
```json
{
  "vertical": "B2B_SAAS",
  "business_model": "SUBSCRIPTION",
  "complexity_level": "HIGH",
  "confidence_score": 0.98
}
```

## 16. Implementation Status
[IMPLEMENTED]
