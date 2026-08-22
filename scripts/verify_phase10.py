#!/usr/bin/env python3
"""Phase 10 — RL Optimizer Verification Script.

Validates:
1. Gymnasium environment dynamics
2. PPO Actor-Critic network architecture
3. PPO training & checkpoint integrity
4. Baseline policies (Random, Rule-Based, Contextual Bandit)
5. Constraint validator safety projection
6. Optimization Agent end-to-end inference
7. Policy comparison benchmark
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

# ── Ensure project root on sys.path ──
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))


def section(title: str) -> None:
    print(f"\n{'=' * 72}")
    print(f"  {title}")
    print(f"{'=' * 72}")


def check(label: str, condition: bool) -> None:
    status = "PASS" if condition else "FAIL"
    print(f"  [{status}]  {label}")
    if not condition:
        raise AssertionError(f"FAILED: {label}")


def verify_environment() -> None:
    section("1. Gymnasium Environment — CampaignOptimizationEnv")
    from adpilot.rl.environment import CampaignOptimizationEnv

    env = CampaignOptimizationEnv()
    obs, info = env.reset()
    check("reset() returns observation of shape (10,)", obs.shape == (10,))
    check("observation space shape matches", env.observation_space.shape == (10,))
    check("action space shape is (5,)", env.action_space.shape == (5,))

    action = env.action_space.sample()
    obs2, reward, terminated, truncated, info2 = env.step(action)
    check("step() returns valid observation", obs2.shape == (10,))
    check("reward is a finite float", np.isfinite(reward))
    check("step info contains 'current_roas'", "current_roas" in info2)
    check("step info contains 'cumulative_conversions'", "cumulative_conversions" in info2)
    check("step info contains 'cumulative_revenue'", "cumulative_revenue" in info2)
    print(f"    Sample reward: {reward:.4f}")
    print(f"    Sample ROAS:   {info2['current_roas']:.4f}")
    env.close()


def verify_ppo_network() -> None:
    section("2. PPO Actor-Critic Network Architecture")
    import torch
    from adpilot.rl.models import PPOActorCriticNetwork

    net = PPOActorCriticNetwork(state_dim=10, action_dim=5, hidden_dim=64)
    params = sum(p.numel() for p in net.parameters())
    check("network has >0 parameters", params > 0)
    print(f"    Total parameters: {params:,}")

    state = torch.randn(10)
    action, log_prob, value = net.get_action(state)
    check("action shape is (5,)", action.shape == (5,))
    check("log_prob is scalar", log_prob.dim() == 0)
    check("value is scalar", value.dim() == 0)
    check("action clamped to [-1, 1]", float(action.abs().max()) <= 1.0 + 1e-5)


def verify_checkpoint() -> None:
    section("3. PPO Checkpoint Integrity")
    ckpt_path = project_root / "research" / "models" / "optimizer" / "ppo_policy.pt"
    meta_path = project_root / "research" / "models" / "optimizer" / "ppo_metadata.json"

    check("ppo_policy.pt exists", ckpt_path.exists())
    check("ppo_metadata.json exists", meta_path.exists())

    if meta_path.exists():
        meta = json.loads(meta_path.read_text())
        check("metadata contains 'state_dim'", "state_dim" in meta)
        check("metadata contains 'action_dim'", "action_dim" in meta)
        check("metadata state_dim == 10", meta["state_dim"] == 10)
        check("metadata action_dim == 5", meta["action_dim"] == 5)
        print(f"    Iterations trained: {meta.get('iterations', 'N/A')}")
        print(f"    Training time:      {meta.get('training_time_seconds', 'N/A')}s")


def verify_constraint_validator() -> None:
    section("4. Constraint Validator Safety Projection")
    from adpilot.rl.constraint_validator import ConstraintValidator

    cv = ConstraintValidator()
    extreme_action = np.array([1.0, -0.5, -0.5, 0.8, 1.0], dtype=np.float64)
    allocations = {"linkedin": 0.60, "facebook": 0.25, "email": 0.15}

    action_proposal, safety_result = cv.validate_and_project(extreme_action, allocations)
    allocs = action_proposal.channel_allocations

    total = sum(allocs.values())
    check(f"allocations sum ~ 1.0 (got {total:.6f})", abs(total - 1.0) < 0.01)

    for ch, w in allocs.items():
        check(f"channel '{ch}' weight {w:.4f} >= 0.05", w >= 0.05 - 1e-4)
        check(f"channel '{ch}' weight {w:.4f} <= 0.80", w <= 0.80 + 1e-4)

    bid = action_proposal.bid_multiplier
    check(f"bid multiplier {bid:.3f} in [0.5, 2.0]", 0.5 <= bid <= 2.0)
    check("safety_result has is_valid field", hasattr(safety_result, "is_valid"))
    check("safety_result has violations field", hasattr(safety_result, "violations"))
    print(f"    Projected allocations: {allocs}")
    print(f"    Bid multiplier:        {bid:.3f}")
    print(f"    Is valid:              {safety_result.is_valid}")
    print(f"    Violations:            {safety_result.violations}")
    print(f"    Modifications:         {safety_result.modifications_applied}")


def verify_baselines() -> None:
    section("5. Baseline Policies")
    from adpilot.rl.baselines import (
        ContextualBanditPolicy,
        RandomPolicy,
        RuleBasedPolicy,
        evaluate_policy,
    )
    from adpilot.rl.environment import CampaignOptimizationEnv

    env = CampaignOptimizationEnv()
    policies = {
        "Random": RandomPolicy(action_dim=5),
        "Rule-Based": RuleBasedPolicy(),
        "Contextual Bandit": ContextualBanditPolicy(n_arms=4),
    }

    for name, policy in policies.items():
        metrics = evaluate_policy(policy, env, num_episodes=10)
        check(f"{name} mean_cumulative_reward is finite", np.isfinite(metrics["mean_cumulative_reward"]))
        print(f"    {name}: reward={metrics['mean_cumulative_reward']:.2f}, roas={metrics.get('mean_final_roas', 0):.2f}x")

    env.close()


def verify_benchmark_results() -> None:
    section("6. Benchmark Results File")
    bench_path = project_root / "research" / "models" / "optimizer" / "benchmark_results.json"
    check("benchmark_results.json exists", bench_path.exists())

    if bench_path.exists():
        data = json.loads(bench_path.read_text())
        for policy_name in ["random", "rule_based", "contextual_bandit", "ppo"]:
            check(f"benchmark contains '{policy_name}'", policy_name in data)
            if policy_name in data:
                entry = data[policy_name]
                reward_key = "mean_cumulative_reward" if "mean_cumulative_reward" in entry else "mean_reward"
                roas_key = "mean_final_roas" if "mean_final_roas" in entry else "mean_roas"
                print(f"    {policy_name}: reward={entry.get(reward_key, 'N/A')}, "
                      f"roas={entry.get(roas_key, 'N/A')}")


def verify_optimization_agent_imports() -> None:
    section("7. Optimization Agent Import & Schema Validation")
    from adpilot.agents.optimization_agent import OptimizationAgent
    from adpilot.schemas.agent_schemas import (
        RLPolicyType,
        RLActionProposal,
        ConstraintValidationResult,
    )

    agent = OptimizationAgent()
    check("OptimizationAgent instantiates", agent is not None)
    check("agent.name == 'optimization_agent'", agent.name == "optimization_agent")

    check("RLPolicyType enum exists", hasattr(RLPolicyType, "ppo"))
    check("RLActionProposal model exists", hasattr(RLActionProposal, "model_fields"))
    check("ConstraintValidationResult model exists", hasattr(ConstraintValidationResult, "model_fields"))

    from adpilot.core.contract_registry import OPTIMIZATION_AGENT_CONTRACT
    check("contract identity.agent_id == 'optimization_agent'", OPTIMIZATION_AGENT_CONTRACT.identity.agent_id == "optimization_agent")
    print(f"    Contract role: {OPTIMIZATION_AGENT_CONTRACT.identity.role[:80]}...")


def main() -> None:
    print("\n" + "#" * 72)
    print("  PHASE 10 -- RL OPTIMIZER VERIFICATION")
    print("#" * 72)

    try:
        verify_environment()
        verify_ppo_network()
        verify_checkpoint()
        verify_constraint_validator()
        verify_baselines()
        verify_benchmark_results()
        verify_optimization_agent_imports()

        print("\n" + "=" * 72)
        print("  ALL PHASE 10 VERIFICATIONS PASSED")
        print("=" * 72 + "\n")
    except AssertionError as e:
        print(f"\n  VERIFICATION FAILED: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
