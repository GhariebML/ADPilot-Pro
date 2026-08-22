# Knowledge Representation & Taxonomy

**Status:** [IMPLEMENTED]  
**Architecture:** Relational Commercial Taxonomies & Vector Knowledge Networks  

---

## 1. Overview
ADPilot Pro represents domain knowledge through a hybrid structure combining **hierarchical relational commercial taxonomies** (Pydantic v2 enums and DAG dependencies) with **high-dimensional vector semantic clusters** (FastEmbed BGE in Qdrant).

---

## 2. Structured Taxonomy Entities

```mermaid
classDiagram
    class MarketingVertical {
        <<enumeration>>
        B2B_SAAS
        PHYSICAL_PRODUCT
        REAL_ESTATE
        PROFESSIONAL_SERVICE
    }

    class MarketingChannel {
        <<enumeration>>
        META_ADS
        GOOGLE_SEARCH
        GOOGLE_DISPLAY
        LINKEDIN_SPONSORED
        EMAIL_AUTOMATION
    }

    class FunnelTier {
        <<enumeration>>
        TOFU_AWARENESS
        MOFU_CONSIDERATION
        BOFU_CONVERSION
        RETENTION_NURTURE
    }

    class CampaignGoal {
        <<enumeration>>
        LEAD_GENERATION
        DIRECT_PURCHASE
        BRAND_AWARENESS
        PRODUCT_LAUNCH
    }

    MarketingVertical --> MarketingChannel : Recommends
    CampaignGoal --> FunnelTier : Maps To
    MarketingChannel --> FunnelTier : Executes In
```

---

## 3. Dedicated Knowledge Graph Engine Status
- **Current Implementation:** [IMPLEMENTED via Hybrid Vector/Relational Structure] — Ingests and links documents with explicit category headers, platform mappings, and entity metadata in SQLite and Qdrant.
- **Neo4j / Dedicated Graph DB:** [NOT REQUIRED / ARCHITECTURALLY SATISFIED BY RELATIONAL + VECTOR HYBRID].
