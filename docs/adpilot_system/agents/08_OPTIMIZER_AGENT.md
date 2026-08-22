# Optimization Agent (RL Policy Optimizer)

## 1. Purpose
The **Optimization Agent** autonomously adjusts campaign parameters, rebalances advertising spend across channels, and generates continuous optimization interventions using a trained **Proximal Policy Optimization (PPO)** neural policy network.

## 2. Business Responsibility
Maximizes blended return on ad spend (ROAS) and lowers customer acquisition cost (CAC) by continuously shifting capital towards top-performing channels while enforcing strict budget ceilings.

## 3. Technical Responsibility
Ingests `AnalyticsAgentOutput`, constructs the continuous 12-dimensional state vector $\mathbf{s}_t$, executes PyTorch PPO Actor-Critic policy forward pass, projects actions onto Dirichlet budget constraints, and emits `OptimizationOutput`.

## 4. Source Code
- `src/adpilot/agents/optimization_agent.py`
- RL Policy Architecture: `src/adpilot/rl/models.py`
- Training Pipeline: `src/adpilot/rl/trainer.py`
- Policy Weights: `research/models/optimizer/ppo_policy.pt`

## 5. Input
- **Schema:** `AnalyticsAgentOutput` + `CampaignContext`
  - Current channel spend allocations
  - Channel-specific ROAS, CTR, CVR
  - Total allowable budget ceiling ($)

## 6. Processing Flow
1. Construct 12-dimensional state tensor:
   $$\mathbf{s}_t = [\text{SpendRatio}_k, \text{ROAS}_k, \text{CAC}_k, \text{CTR}_k, \dots]^T$$
2. Forward pass through PyTorch Actor-Critic policy network ($12 \to 64 \to 64 \to K$ dimensions).
3. Apply Dirichlet concentration projection to guarantee:
   $$\sum_{k=1}^K a_{t,k} = 1.0 \quad \text{and} \quad a_{t,k} \ge 0.05 \quad \forall k$$
4. Compute recommended dollar allocations and expected marginal ROAS lift.
5. Emit `OptimizationOutput`.

## 7. Models Used
- **Reinforcement Learning Model:** PyTorch PPO Actor-Critic Policy Network (`research/models/optimizer/ppo_policy.pt`).
- **Mean Reward:** $+0.48$.
- **Inference Latency:** `15.8ms`.

## 8. Tools Used
- Constraint Validator (`src/adpilot/rl/constraint_validator.py`)
- Trajectory Memory Buffer (`src/adpilot/rl/environment.py`)

## 9. Output
- **Schema:** `OptimizationOutput`
  - `recommended_budget_split: Dict[str, float]` (Percentages summing to 1.0)
  - `dollar_allocations: Dict[str, float]` (Exact dollar amounts)
  - `expected_roas_lift: float` (e.g., +0.48x)
  - `optimization_rationale: str`
  - `requires_human_approval: bool` (true if delta $> 10\%$)

## 10. Downstream Consumers
- `CorrectionEngine` (verifies hard budget constraints)
- `HITLGate` (quarantines large budget shifts for human authorization)
- `PublishingAgent` (updates live campaign budgets)

## 11. Error Handling
- Automatic fallback to baseline proportional budget splits if PyTorch inference encounters numerical instability.

## 12. Validation
- Strict assertion checking: $\sum \text{Allocations} \equiv \text{TotalBudget} \pm \$0.01$.

## 13. Corrective Actions
- Clamps single-step budget changes to a maximum $\pm 20\%$ delta to prevent aggressive spending volatility.

## 14. Human-in-the-Loop
- High-risk budget changes trigger a pending decision in the HITL Approval Center.

## 15. Example Execution
```json
{
  "recommended_budget_split": {
    "LINKEDIN": 0.57,
    "META": 0.28,
    "GOOGLE_SEARCH": 0.15
  },
  "dollar_allocations": {
    "LINKEDIN": 5700.00,
    "META": 2800.00,
    "GOOGLE_SEARCH": 1500.00
  },
  "expected_roas_lift": 0.48,
  "optimization_rationale": "PPO policy shifted +12% budget into LinkedIn following strong 4.82x ROAS signal.",
  "requires_human_approval": true
}
```

## 16. Implementation Status
[IMPLEMENTED]
