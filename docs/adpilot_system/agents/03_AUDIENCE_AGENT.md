# Audience Agent

## 1. Purpose
The **Audience Agent** translates market research into actionable ad platform audience targeting parameters (e.g., job titles, interests, lookalikes, negative targeting, age/geo brackets).

## 2. Business Responsibility
Ensures advertising budget is not wasted on unqualified clicks by defining platform-specific targeting parameters for Meta, LinkedIn, and Google Ads.

## 3. Technical Responsibility
Transforms abstract ICP personas from `ResearchAgentOutput` into concrete, structured targeting matrices conforming to platform ad API constraints.

## 4. Source Code
- `src/adpilot/agents/audience_agent.py`

## 5. Input
- `ResearchAgentOutput` (Personas, pain points, demographics)
- `StrategyAgentOutput` (Target channels)

## 6. Processing Flow
1. Parse ICP title and industry fields.
2. Map to platform-specific taxonomies (e.g., LinkedIn Job Functions, Meta Interest Categories, Google In-Market Audiences).
3. Apply negative audience exclusions to safeguard spend.
4. Output structured targeting configurations.

## 7. Models Used
- Foundation LLM (GPT-4o Router) / Taxonomy Mapping Rules.

## 8. Tools Used
- Audience Taxonomy Registry.

## 9. Output
- Platform-specific targeting configurations:
  - LinkedIn: Job Titles, Industries, Company Size.
  - Meta: Interests, Behaviors, Age/Gender.
  - Google: Search Intent Keywords, Demographic filters.

## 10. Downstream Consumers
- `PublishingAgent` (populates ad campaign creation payloads)
- `CampaignManagerAgent` / `AnalyticsAgent`

## 11. Error Handling
- Invalid platform taxonomy values are automatically stripped or mapped to closest valid parent categories.

## 12. Validation
- Checks that audience size estimates fall within recommended minimum liquidity thresholds ($\ge 50,000$).

## 13. Corrective Actions
- If `AnalyticsAgent` projects high CAC due to overly narrow targeting, expands audience criteria.

## 14. Human-in-the-Loop
- Marketers can refine targeting criteria inside the Audience tab.

## 15. Example Execution
```json
{
  "linkedin_targeting": {
    "job_functions": ["Marketing", "Operations", "Engineering"],
    "seniority": ["Director", "VP", "C-Level"],
    "company_headcount": ["51-200", "201-500", "501-1000"]
  },
  "meta_targeting": {
    "interests": ["Digital Marketing", "Artificial Intelligence", "SaaS Growth"],
    "age_min": 28,
    "age_max": 55
  }
}
```

## 16. Implementation Status
[IMPLEMENTED]
