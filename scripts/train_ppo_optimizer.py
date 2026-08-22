"""Training and comparative evaluation script for PPO Optimizer, Bandit, and Rule-Based baselines."""

import json
from pathlib import Path
import time

import numpy as np
import torch

from adpilot.rl.baselines import (
    ContextualBanditPolicy,
    RandomPolicy,
    RuleBasedPolicy,
    evaluate_policy,
)
from adpilot.rl.environment import CampaignOptimizationEnv
from adpilot.rl.trainer import PPOTrainer


def main() -> None:
    print("=" * 80)
    print("ADPilot Phase 10: Training Reinforcement Learning Optimizer (PPO) & Benchmarking")
    print("=" * 80)

    # 1. Initialize Environment and Trainer
    env = CampaignOptimizationEnv(total_budget=80000.0, duration_days=90, target_roas=3.50, target_cpa=45.0, seed=42)
    trainer = PPOTrainer(env=env, state_dim=10, action_dim=5, hidden_dim=64, lr=3e-4)

    # 2. Train PPO Agent
    print("[TRAIN] Starting PPO Actor-Critic Training over simulated campaign environment...")
    start_t = time.perf_counter()
    train_results = trainer.train(num_iterations=25, episodes_per_iteration=5, ppo_epochs=4, batch_size=64)
    train_duration = time.perf_counter() - start_t
    print(f"[TRAIN] Completed {train_results['iterations_trained']} iterations in {train_duration:.2f}s | Final Mean Reward: {train_results['final_mean_reward']:.4f}")

    # 3. Checkpoint Model
    checkpoint_dir = Path("research/models/optimizer")
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_path = checkpoint_dir / "ppo_policy.pt"
    trainer.save_checkpoint(checkpoint_path)
    print(f"[SAVED] Saved trained PPO policy checkpoint to {checkpoint_path}")

    # 4. Comparative Evaluation across Policies
    print("\n" + "=" * 80)
    print("BENCHMARK COMPARATIVE EVALUATION (50 Independent Episodes per Policy)")
    print("=" * 80)

    eval_env = CampaignOptimizationEnv(total_budget=80000.0, duration_days=90, target_roas=3.50, target_cpa=45.0, seed=100)

    random_policy = RandomPolicy(action_dim=5, seed=101)
    rule_policy = RuleBasedPolicy()
    bandit_policy = ContextualBanditPolicy(n_arms=4, seed=102)

    # Pre-train bandit on 30 sample episodes
    for ep in range(30):
        obs, _ = eval_env.reset(seed=200 + ep)
        for _ in range(90):
            action = bandit_policy.select_action(obs)
            obs, r, term, trunc, _ = eval_env.step(action)
            bandit_policy.update(arm=0, reward=r)
            if term or trunc:
                break

    metrics_random = evaluate_policy(random_policy, eval_env, num_episodes=50, seed=300)
    metrics_rule = evaluate_policy(rule_policy, eval_env, num_episodes=50, seed=300)
    metrics_bandit = evaluate_policy(bandit_policy, eval_env, num_episodes=50, seed=300)
    metrics_ppo = evaluate_policy(trainer.policy, eval_env, num_episodes=50, seed=300)

    print(f"{'Policy':<20} | {'Cum. Reward':<14} | {'Final ROAS':<12} | {'Final CPA ($)':<14} | {'Conversions':<12} | {'Gross Revenue ($)':<18}")
    print("-" * 105)
    print(f"{'Random':<20} | {metrics_random['mean_cumulative_reward']:>12.2f}  | {metrics_random['mean_final_roas']:>10.2f}x | ${metrics_random['mean_final_cpa']:>12.2f} | {metrics_random['mean_conversions']:>10.0f}   | ${metrics_random['mean_revenue']:>16,.2f}")
    print(f"{'Rule-Based':<20} | {metrics_rule['mean_cumulative_reward']:>12.2f}  | {metrics_rule['mean_final_roas']:>10.2f}x | ${metrics_rule['mean_final_cpa']:>12.2f} | {metrics_rule['mean_conversions']:>10.0f}   | ${metrics_rule['mean_revenue']:>16,.2f}")
    print(f"{'Contextual Bandit':<20} | {metrics_bandit['mean_cumulative_reward']:>12.2f}  | {metrics_bandit['mean_final_roas']:>10.2f}x | ${metrics_bandit['mean_final_cpa']:>12.2f} | {metrics_bandit['mean_conversions']:>10.0f}   | ${metrics_bandit['mean_revenue']:>16,.2f}")
    print(f"{'PPO (Ours)':<20} | {metrics_ppo['mean_cumulative_reward']:>12.2f}  | {metrics_ppo['mean_final_roas']:>10.2f}x | ${metrics_ppo['mean_final_cpa']:>12.2f} | {metrics_ppo['mean_conversions']:>10.0f}   | ${metrics_ppo['mean_revenue']:>16,.2f}")
    print("=" * 105)

    benchmark_path = checkpoint_dir / "benchmark_results.json"
    with open(benchmark_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "random": metrics_random,
                "rule_based": metrics_rule,
                "contextual_bandit": metrics_bandit,
                "ppo": metrics_ppo,
            },
            f,
            indent=2,
        )
    print(f"[SAVED] Saved benchmark results to {benchmark_path}")


if __name__ == "__main__":
    main()
