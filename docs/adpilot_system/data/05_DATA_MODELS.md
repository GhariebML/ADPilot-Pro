# Data Models & Pydantic Schema Contracts

**Status:** [IMPLEMENTED]  
**Location:** `src/adpilot/schemas/` & `src/adpilot/schemas/agent_schemas.py`  

---

## 1. Single Source of Truth Principle

All agent interactions and API communications strictly adhere to Pydantic v2 data models. No unvalidated dictionaries or loosely typed structures are permitted across agent boundaries.

---

## 2. Core Pydantic Schemas

### 1. `CampaignContext` (`src/adpilot/schemas/campaign_context.py`)
```python
class CampaignContext(BaseModel):
    campaign_id: str
    product_name: str
    description: str
    goals: List[CampaignGoal]
    budget: float = Field(gt=0, description="Total budget in USD")
    target_audience: Optional[str] = None
    selected_channels: List[MarketingChannel] = []
    brand_guidelines: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### 2. `ContentAgentOutput` (`src/adpilot/schemas/agent_schemas.py`)
```python
class AdContent(BaseModel):
    platform: MarketingChannel
    headline: str
    body: str
    cta: str
    performance: Optional[str] = None

class ContentAgentOutput(BaseModel):
    ads: List[AdContent]
    email_sequences: List[EmailSequence] = []
    social_posts: List[SocialPost] = []
    summary: str
```

### 3. `AnalyticsAgentOutput` (`src/adpilot/schemas/agent_schemas.py`)
```python
class AnalyticsAgentOutput(BaseModel):
    predicted_roas: float = Field(ge=0.0)
    predicted_cac: float = Field(ge=0.0)
    predicted_cvr: float = Field(ge=0.0, le=1.0)
    health_score: float = Field(ge=0.0, le=100.0)
    channel_roas_breakdown: Dict[str, float]
    optimization_hints: List[str] = []
```

### 4. `OptimizationOutput` (`src/adpilot/schemas/agent_schemas.py`)
```python
class OptimizationOutput(BaseModel):
    recommended_budget_split: Dict[str, float]
    dollar_allocations: Dict[str, float]
    expected_roas_lift: float
    optimization_rationale: str
    requires_human_approval: bool
```
