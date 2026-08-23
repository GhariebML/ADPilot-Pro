# 08 — Reinforcement Learning & PPO Architecture

## 1. Problem Formulation: The Marketing Allocation MDP
Campaign budget optimization across multi-channel advertising platforms is formulated as a continuous Markov Decision Process (MDP):

$$\mathcal{M} = \langle \mathcal{S}, \mathcal{A}, \mathcal{P}, \mathcal{R}, \gamma \rangle$$

Where:
* **State $\mathcal{S}$:** Continuous vector representing current campaign telemetry:
  $$s_t = [\text{CTR}_t, \text{CPA}_t, \text{ROAS}_t, \text{SpendRate}_t, \text{ChannelShare}_{1..K}, \text{DayIndex}_t]$$
* **Action $\mathcal{A}$:** Continuous budget reallocation delta vector across marketing channels:
  $$a_t = [\Delta b_{\text{Meta}}, \Delta b_{\text{Google}}, \Delta b_{\text{LinkedIn}}], \quad \sum_{k=1}^K b_k = 1.0$$
* **Reward $\mathcal{R}$:** Multi-objective return function balancing revenue maximization with acquisition cost penalties:
  $$r(s_t, a_t) = w_1 \cdot \frac{\text{ROAS}_t}{\text{TargetROAS}} - w_2 \cdot \max\left(0, \frac{\text{CPA}_t - \text{TargetCPA}}{\text{TargetCPA}}\right) - w_3 \cdot \|a_t\|^2$$

---

## 2. Proximal Policy Optimization (PPO) Mechanics
ADPilot employs Proximal Policy Optimization with a clipped surrogate objective to guarantee stable policy gradient updates without catastrophic performance collapse:

$$L^{\text{CLIP}}(\theta) = \hat{\mathbb{E}}_t \left[ \min\left( r_t(\theta)\hat{A}_t, \; \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon)\hat{A}_t \right) \right]$$

Where:
* $r_t(\theta) = \frac{\pi_\theta(a_t | s_t)}{\pi_{\theta_{\text{old}}}(a_t | s_t)}$ is the probability ratio between the current and old policy.
* $\hat{A}_t$ is the Generalized Advantage Estimator (GAE).
* $\epsilon = 0.2$ is the clipping parameter enforcing trust-region boundaries.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                             PPO LEARNING LOOP                               │
│                                                                             │
│     ┌─────────────────────────────────────────────────────────┐             │
│     │               Campaign State Telemetry s_t               │             │
│     └────────────────────────────┬────────────────────────────┘             │
│                                  │                                          │
│                                  ▼                                          │
│     ┌─────────────────────────────────────────────────────────┐             │
│     │            PPO Actor-Critic Policy Network              │             │
│     └────────────────────────────┬────────────────────────────┘             │
│                                  │                                          │
│                                  ▼ Reallocation Action a_t                  │
│     ┌─────────────────────────────────────────────────────────┐             │
│     │     Safety & Constraint Gate (Variance Delta < tau)     │             │
│     └─────────────┬─────────────────────────────┬─────────────┘             │
│                   │ Passed                      │ Variance Exceeded         │
│                   ▼                             ▼                           │
│     ┌───────────────────────────┐ ┌───────────────────────────┐             │
│     │ Execute Budget Shift      │ │ Trigger HITL Review Gate  │             │
│     └─────────────┬─────────────┘ └─────────────┬─────────────┘             │
│                   │                             │ (Approved)                │
│                   └──────────────┬──────────────┘                           │
│                                  ▼                                          │
│     ┌─────────────────────────────────────────────────────────┐             │
│     │     Campaign Environment / Simulation Response          │             │
│     └────────────────────────────┬────────────────────────────┘             │
│                                  │                                          │
│                                  ▼ Ingest Return r_t & Next State s_{t+1}   │
│     ┌─────────────────────────────────────────────────────────┐             │
│     │           Surrogate Policy Gradient Update              │             │
│     └─────────────────────────────────────────────────────────┘             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Implementation Reality
* **Rule Engine Layer (`src/adpilot/services/ai_optimizer.py`):** `[IMPLEMENTED]` Deterministic production optimization rules evaluating CTR, CPA, and ROAS thresholds.
* **RL Policy Environment (`research/notebooks/`):** `[PARTIALLY IMPLEMENTED]` Synthetic gym environment for offline PPO training and policy weight verification.
