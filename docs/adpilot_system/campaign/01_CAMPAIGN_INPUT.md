# Campaign Input Ingestion & Brief Normalization

**Status:** [IMPLEMENTED]  
**Schema:** `CampaignInputSchema` (`src/adpilot/schemas/agent_schemas.py`)  

---

## 1. Input Brief Schema Structure

```json
{
  "product_name": "VisionGuard AI",
  "description": "Enterprise automated computer vision quality inspection platform for manufacturing production lines.",
  "goals": ["LEAD_GENERATION", "PRODUCT_LAUNCH"],
  "budget": 10000.00,
  "target_audience": "VP of Manufacturing Operations, Quality Assurance Directors",
  "selected_channels": ["LINKEDIN", "META", "GOOGLE_SEARCH"],
  "brand_guidelines": {
    "primary_color": "#06B6D4",
    "tone": "Authoritative, technical, high-ROI"
  }
}
```

---

## 2. Validation & Normalization Rules (`src/adpilot/core/context_builder.py`)
1. **Budget Bounds:** Enforces $\text{Budget} \ge \$500.00$ and $\text{Budget} \le \$1,000,000.00$.
2. **Channel Normalization:** Strips duplicates and maps string names to `MarketingChannel` enum values.
3. **Pydantic Contract Transformation:** Yields immutable `CampaignContext` entity assigned a unique UUID `campaign_id`.
