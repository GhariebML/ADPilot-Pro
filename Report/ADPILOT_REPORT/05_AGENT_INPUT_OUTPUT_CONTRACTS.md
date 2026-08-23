# 05 — Agent Input & Output Contracts

## 1. Contract Governance & Schema Principles
In ADPilot Pro, inter-agent communication is strictly governed by immutable Pydantic v2 schemas defined in `src/adpilot/schemas/agent_schemas.py` and `src/adpilot/schemas/campaign_context.py`. Agents never exchange untyped strings or arbitrary JSON dictionaries.

```
┌───────────────────────────┐
│     Upstream Agent        │
└─────────────┬─────────────┘
              │ Produces Validated Output Schema
              ▼
┌───────────────────────────┐
│   AgentContract Boundary  │ ──> Validates Schema, Constraints & Provenance
└─────────────┬─────────────┘
              │ Translates into Input Schema
              ▼
┌───────────────────────────┐
│    Downstream Agent       │
└───────────────────────────┘
```

---

## 2. Core Agent Contract Specifications

### 2.1 Strategy Agent Contract
* **Input Schema:** `StrategyAgentInput`
  ```python
  class StrategyAgentInput(BaseModel):
      campaign_id: str
      business_info: BusinessInfo
      product_spec: ProductSpec
      audience_profile: Optional[AudienceProfile] = None
      budget: BudgetSpec
      timeline: TimelineSpec
      historical_context: Optional[List[Dict[str, Any]]] = None
  ```
* **Output Schema:** `StrategyAgentOutput`
  ```python
  class StrategyAgentOutput(BaseModel):
      strategy_id: str
      campaign_id: str
      positioning_statement: str
      core_value_propositions: List[str]
      channel_allocation: Dict[MarketingChannel, float]
      target_kpis: Dict[str, float]
      funnel_strategy: Dict[FunnelStage, str]
      provenance: ProvenanceRecord
  ```

### 2.2 Content Agent Contract
* **Input Schema:** `ContentAgentInput`
  ```python
  class ContentAgentInput(BaseModel):
      campaign_id: str
      strategy: StrategyAgentOutput
      brand_voice: ToneOfVoice
      channels: List[MarketingChannel]
      competitors: Optional[Any] = None
  ```
* **Output Schema:** `ContentAgentOutput`
  ```python
  class ContentAgentOutput(BaseModel):
      content_id: str
      campaign_id: str
      ad_copies: List[AdCopyVariant]
      headlines: List[str]
      call_to_actions: List[str]
      channel_specific_copy: Dict[MarketingChannel, List[AdCopyVariant]]
      quality_score: float
  ```

### 2.3 Design Agent Contract
* **Input Schema:** `DesignAgentInput`
  ```python
  class DesignAgentInput(BaseModel):
      campaign_id: str
      content: ContentAgentOutput
      strategy: StrategyAgentOutput
      revision_feedback: Optional[List[str]] = None
  ```
* **Output Schema:** `DesignAgentOutput`
  ```python
  class DesignAgentOutput(BaseModel):
      design_id: str
      campaign_id: str
      creative_assets: List[CreativeAsset]
      design_briefs: List[DesignBrief]
      color_palette: List[str]
      visual_complexity_score: float
  ```
