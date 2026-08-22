# Publishing Agent

## 1. Purpose
The **Publishing Agent** formats, validates, and dispatches approved campaign creative assets, copy, targeting parameters, and budget allocations to live external ad platforms (Meta Ads, Google Ads, LinkedIn, Email).

## 2. Business Responsibility
Acts as the final execution gateway, turning conceptual marketing strategies into active, revenue-generating digital campaigns without manual copy-pasting or human error.

## 3. Technical Responsibility
Ingests `ContentAgentOutput`, `DesignAgentOutput`, `OptimizationOutput`, and `HITLDecisionRecord`, verifies cryptographic signatures, calls platform API adapters with idempotency keys, and records live campaign identifiers.

## 4. Source Code
- `src/adpilot/publishing/engine.py`
- Adapters: `src/adpilot/publishing/adapters/*.py` (Meta, Google, LinkedIn, Email, Mock)
- Idempotency Manager: `src/adpilot/publishing/idempotency.py`

## 5. Input
- Approved `CampaignContext`
- Finalized Ad Creatives & Visual Assets
- Dollar Budget Allocations
- Verified `HITLDecisionRecord` (HMAC-SHA256 signature)

## 6. Processing Flow
1. Verify cryptographic approval signature from HITL gate.
2. Check idempotency store to prevent duplicate media spend.
3. Validate API payloads against network-specific constraints (e.g., Meta Graph API payload schemas).
4. Dispatch async HTTP requests to ad platform adapters.
5. Ingest external campaign IDs and emit `PublishingResult`.

## 7. Models Used
- Adapter Protocol Engine / Deterministic Validator.

## 8. Tools Used
- Platform REST Adapters (`src/adpilot/publishing/adapters/`)
- Idempotency Store (`src/adpilot/publishing/idempotency.py`)

## 9. Output
- **Schema:** `PublishingResult`
  - `status: str` (`SUCCESS`, `PARTIAL_SUCCESS`, `MOCK_DISPATCH`)
  - `published_campaigns: List[Dict[str, Any]]` (Platform, ExternalCampaignId, SpendCap)
  - `dispatch_timestamp: str`
  - `audit_hash: str`

## 10. Downstream Consumers
- `MonitoringAgent` (begins telemetry collection on published campaign IDs)
- `ExecutiveDashboard` (marks campaigns as active in portfolio)

## 11. Error Handling
- Network retries with exponential backoff; automatic rollback if one channel fails in a multi-channel batch.

## 12. Validation
- Strict validation that no unapproved budget changes or unverified copy variants can reach publishing adapters.

## 13. Corrective Actions
- Falls back to Sandbox/Mock mode in development or if API credentials are missing.

## 14. Human-in-the-Loop
- Requires explicit `Director` authorization before live ad account credit cards are charged.

## 15. Example Execution
```json
{
  "status": "SUCCESS",
  "published_campaigns": [
    { "platform": "LINKEDIN", "external_id": "li_cmp_984128", "budget": 5700.00 },
    { "platform": "META", "external_id": "fb_act_410294", "budget": 2800.00 },
    { "platform": "GOOGLE", "external_id": "goog_ad_883109", "budget": 1500.00 }
  ],
  "dispatch_timestamp": "2026-08-22T18:39:22Z",
  "audit_hash": "SHA256-d7a8f9b2"
}
```

## 16. Implementation Status
[IMPLEMENTED]
