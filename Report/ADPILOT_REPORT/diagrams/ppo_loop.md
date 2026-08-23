# PPO Reinforcement Learning Optimization Loop

```mermaid
graph TD
    classDef state fill:#0f172a,stroke:#38bdf8,stroke-width:2px,color:#fff;
    classDef ppo fill:#1e1b4b,stroke:#8b5cf6,stroke-width:2px,color:#fff;
    classDef env fill:#064e3b,stroke:#10b981,stroke-width:2px,color:#fff;
    classDef reward fill:#451a03,stroke:#f59e0b,stroke-width:2px,color:#fff;

    S[Campaign State s_t: CTR, CPA, ROAS, Spend]:::state --> PPO[PPO Actor-Critic Policy Net]:::ppo
    PPO --> A[Action a_t: Channel Budget Shifts]:::ppo
    A --> ENV[Campaign Ad Environment / Simulator]:::env
    ENV --> R[Multi-Objective Return r_t]:::reward
    ENV --> S_NEXT[Next State s_{t+1}]:::state
    R --> UPDATE[Clipped Surrogate Objective Policy Update]:::ppo
    UPDATE --> PPO
```
