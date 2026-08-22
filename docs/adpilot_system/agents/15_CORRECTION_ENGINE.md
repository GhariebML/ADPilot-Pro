# Correction Engine

## 1. Purpose
The **Correction Engine** audits pipeline execution states, detects constraint violations (e.g., budget overflows, negative allocations, brand safety infractions, low copy quality scores), and autonomously executes deterministic remediation actions.

## 2. Business Responsibility
Acts as the autonomous reliability buffer, resolving errors and edge cases internally without requiring human intervention or crashing pipeline execution.

## 3. Technical Responsibility
Inspects agent outputs against a rule matrix and constraint guards (`src/adpilot/correction/constraint_guard.py`), classifies violations via `ProblemClassifier`, routes targeted re-prompting commands via `AgentRouter`, and emits `CorrectionOutput`.

## 4. Source Code
- `src/adpilot/correction/engine.py`
- Problem Classifier: `src/adpilot/correction/problem_classifier.py`
- Constraint Guard: `src/adpilot/correction/constraint_guard.py`
- Agent Router: `src/adpilot/correction/agent_router.py`

## 5. Input
- Pipeline intermediate contracts (`ContentAgentOutput`, `OptimizationOutput`, `CVScoreOutput`)
- Hard constraints (Max Budget, Min Channel Spend, Character Caps)

## 6. Processing Flow
1. Intercept agent output before passing downstream.
2. Evaluate against active constraint guards:
   - Budget Guard: $\sum \text{Allocations} \le \text{MaxBudget}$ and $a_k \ge \$100.00$.
   - Copy Guard: $\text{Length} \le \text{PlatformLimit}$ and $\text{ProfanityCheck} \equiv \text{Clean}$.
   - Vision Guard: $\text{ContrastRatio} \ge 7.0:1$.
3. If violation found, classify root cause (`BUDGET_OVERFLOW`, `COPY_OVERFLOW`, `LOW_AESTHETIC`).
4. Execute auto-remediation rule or trigger targeted re-prompting.
5. Emit `CorrectionOutput`.

## 7. Models Used
- Deterministic Rule Engine + Zero-Shot Problem Classifier.

## 8. Tools Used
- Constraint Guard Validator (`src/adpilot/correction/constraint_guard.py`)

## 9. Output
- **Schema:** `CorrectionOutput`
  - `violations_detected: List[str]`
  - `remediations_applied: List[str]`
  - `is_clean: bool`
  - `retry_count: int`

## 10. Downstream Consumers
- `HITLGate` (receives clean, validated campaign package)
- `MasterOrchestrator` (receives pass/fail execution flag)

## 11. Error Handling
- Hard limit of 3 retries per stage; if unresolved, escalates to human review.

## 12. Validation
- Guarantees zero downstream schema invalidity.

## 13. Corrective Actions
- Clamps budget numbers, trims overflow copy strings, adjusts color contrast.

## 14. Human-in-the-Loop
- Escalates unresolved violations to the HITL Review Gate.

## 15. Example Execution
```json
{
  "violations_detected": ["Google Search Headline exceeded 30 character limit (34 chars)"],
  "remediations_applied": ["Truncated headline to 'Autonomous AI Marketing OS' (26 chars)"],
  "is_clean": true,
  "retry_count": 1
}
```

## 16. Implementation Status
[IMPLEMENTED]
