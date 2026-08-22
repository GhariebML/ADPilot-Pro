"""Comprehensive test suite for Phase 10 — Reinforcement Learning Optimizer Agent, Policies, and Environment."""


import numpy as np
import pytest
import torch

from adpilot.agents import (
    AnalyticsAgent,
    CompetitorAgent,
    ContentAgent,
    CVAgent,
    DesignAgent,
    OptimizationAgent,
    ResearchAgent,
    StrategyAgent,
)
from adpilot.core.agent_events import AgentEventType, event_bus
from adpilot.core.context_builder import CampaignContextBuilder
from adpilot.orchestrator.master_orchestrator import MasterOrchestrator
from adpilot.orchestrator.planner import CampaignPlanner
from adpilot.rl import (
    CampaignOptimizationEnv,
    ConstraintValidator,
    ContextualBanditPolicy,
    PPOActorCriticNetwork,
    PPOTrainer,
    RandomPolicy,
    RuleBasedPolicy,
)
from adpilot.rl.baselines import evaluate_policy
from adpilot.schemas.agent_schemas import (
    CampaignGoal,
    MarketingChannel,
    OptimizationOutput,
    ProductType,
    RLPolicyType,
    ToneOfVoice,
)


@pytest.fixture
def sample_campaign_context():
    """Construct full canonical CampaignContext for Phase 10 testing."""
    return (
        CampaignContextBuilder.create("camp-phase10-test")
        .with_business(name="ScaleFlow AI", industry="Enterprise SaaS")
        .with_product(
            name="ScaleFlow Orchestrator",
            product_type=ProductType.saas,
            description="Autonomous multi-agent orchestration engine",
        )
        .with_audience(summary="CTOs and VP Engineering leaders")
        .with_geography(target_countries=["US", "GB"])
        .with_budget(total_budget=80000.0, currency="USD")
        .with_channels([MarketingChannel.linkedin, MarketingChannel.facebook, MarketingChannel.email])
        .with_timeline(duration_days=90)
        .with_goals([CampaignGoal.lead_generation, CampaignGoal.brand_awareness])
        .with_brand(
            tone_of_voice=ToneOfVoice.authoritative,
            brand_colors=["#1E3A8A", "#3B82F6", "#FFFFFF"],
        )
        .with_competitors(["LegacyFlow Corp"])
        .build()
    )


def test_campaign_optimization_env_step_and_reset():
    """Verify Gymnasium environment dynamics, observation spaces, action spaces, and transitions."""
    env = CampaignOptimizationEnv(total_budget=50000.0, duration_days=30, seed=42)
    obs, info = env.reset(seed=42)

    assert obs.shape == (10,)
    assert obs.dtype == np.float32
    assert info["day"] == 0
    assert len(info["channel_allocations"]) == 3

    # Step with valid action
    action = np.array([0.10, -0.10, 0.00, 0.05, -0.50], dtype=np.float32)
    next_obs, reward, terminated, truncated, step_info = env.step(action)

    assert next_obs.shape == (10,)
    assert isinstance(reward, float)
    assert not terminated
    assert not truncated
    assert step_info["day"] == 1
    assert step_info["daily_spend"] > 0.0
    assert step_info["daily_conversions"] >= 0
    assert np.isclose(sum(step_info["channel_allocations"]), 1.0)


def test_constraint_validator_enforces_safety_and_clamping():
    """Verify ConstraintValidator clamps illegal actions, prevents overruns, and guarantees 100% budget sum."""
    validator = ConstraintValidator(min_channel_weight=0.05, max_channel_weight=0.80)
    current_allocs = {"linkedin": 0.60, "facebook": 0.25, "email": 0.15}

    # Test extreme out-of-bounds candidate action
    extreme_action = np.array([1.0, -1.0, -1.0, 1.0, 1.0], dtype=np.float32)
    proposal, safety_result = validator.validate_and_project(extreme_action, current_allocs)

    assert safety_result.approved_by_safety_gate
    assert np.isclose(sum(proposal.channel_allocations.values()), 1.0, atol=1e-3)
    for ch, w in proposal.channel_allocations.items():
        assert 0.049 <= w <= 0.801
    assert 0.70 <= proposal.bid_multiplier <= 1.40
    assert proposal.creative_refresh_recommended is True
    assert len(safety_result.modifications_applied) > 0


def test_ppo_actor_critic_network_and_trainer(tmp_path):
    """Verify PPO neural network forward pass, GAE computation, training step, and checkpointing."""
    net = PPOActorCriticNetwork(state_dim=10, action_dim=5, hidden_dim=32)
    state = torch.randn(10)
    action, log_prob, value = net.get_action(state, deterministic=True)

    assert action.shape == (5,)
    assert action.min() >= -1.0 and action.max() <= 1.0
    assert log_prob.dim() == 0
    assert value.dim() == 0

    # Test Trainer
    env = CampaignOptimizationEnv(total_budget=20000.0, duration_days=10, seed=1)
    trainer = PPOTrainer(env=env, state_dim=10, action_dim=5, hidden_dim=32, lr=1e-3)
    res = trainer.train(num_iterations=2, episodes_per_iteration=2, ppo_epochs=2, batch_size=16)

    assert res["status"] == "completed"
    assert res["iterations_trained"] == 2

    # Test checkpoint saving and loading
    ckpt_file = tmp_path / "test_ppo.pt"
    trainer.save_checkpoint(ckpt_file)
    assert ckpt_file.exists()

    new_trainer = PPOTrainer(env=env, state_dim=10, action_dim=5, hidden_dim=32)
    new_trainer.load_checkpoint(ckpt_file)
    assert new_trainer.policy is not None


def test_baseline_policies_and_benchmark_evaluation():
    """Verify Random, Rule-Based, and Contextual Bandit policies and comparative evaluator."""
    env = CampaignOptimizationEnv(total_budget=30000.0, duration_days=15, seed=10)

    random_pol = RandomPolicy(action_dim=5, seed=11)
    rule_pol = RuleBasedPolicy()
    bandit_pol = ContextualBanditPolicy(n_arms=4, seed=12)

    eval_random = evaluate_policy(random_pol, env, num_episodes=3, seed=20)
    eval_rule = evaluate_policy(rule_pol, env, num_episodes=3, seed=20)
    eval_bandit = evaluate_policy(bandit_pol, env, num_episodes=3, seed=20)

    assert "mean_cumulative_reward" in eval_random
    assert "mean_final_roas" in eval_rule
    assert "mean_final_cpa" in eval_bandit
    assert eval_random["mean_conversions"] >= 0


@pytest.mark.asyncio
async def test_optimization_agent_standalone_with_full_context(sample_campaign_context):
    """Verify OptimizationAgent standalone execution with real PPO/Bandit inference and safety validation."""
    # Pre-populate upstream context with stages 1-7
    context = sample_campaign_context
    context = await StrategyAgent().run(context)
    context = await ResearchAgent().run(context)
    context = await CompetitorAgent().run(context)
    context = await ContentAgent().run(context)
    context = await DesignAgent().run(context)
    context = await CVAgent().run(context)
    context = await AnalyticsAgent().run(context)

    agent = OptimizationAgent()
    assert agent.name == "optimization_agent"
    assert len(agent.get_responsibilities()) >= 3

    event_bus.clear()
    emitted_events = []
    event_bus.subscribe(lambda e: emitted_events.append(e))

    context = await agent.run(context)
    assert context.optimization is not None
    opt: OptimizationOutput = context.optimization

    # Verify OptimizationOutput fields
    assert opt.policy_type in [RLPolicyType.ppo, RLPolicyType.bandit, RLPolicyType.rule_based]
    assert len(opt.rl_state_vector) == 10
    assert opt.action_proposal is not None
    assert np.isclose(sum(opt.action_proposal.channel_allocations.values()), 1.0, atol=1e-3)
    assert 0.70 <= opt.action_proposal.bid_multiplier <= 1.40
    assert opt.action_proposal.target_cpa_ceiling > 0.0

    # Verify Safety Validation
    assert opt.safety_validation is not None
    assert opt.safety_validation.approved_by_safety_gate is True

    # Verify Structured Optimization Actions
    assert len(opt.optimization_actions) >= 1
    assert len(opt.budget_reallocation_plan) > 0
    assert len(opt.performance_forecast) > 0
    assert opt.confidence >= 0.70

    # Verify Lifecycle Events
    event_types = [e.event_type for e in emitted_events]
    assert AgentEventType.AGENT_STARTED in event_types
    assert AgentEventType.AGENT_COMPLETED in event_types


@pytest.mark.asyncio
async def test_end_to_end_8_stage_pipeline_strategy_to_optimization(sample_campaign_context):
    """Verify uninterrupted execution across 8 stages: Strategy -> Research -> Competitor -> Content -> Design -> CV -> Analytics -> Optimization."""
    context = sample_campaign_context

    context = await StrategyAgent().run(context)
    assert context.strategy is not None

    context = await ResearchAgent().run(context)
    assert context.research is not None

    context = await CompetitorAgent().run(context)
    assert context.competitors is not None

    context = await ContentAgent().run(context)
    assert context.content is not None

    context = await DesignAgent().run(context)
    assert context.design is not None

    context = await CVAgent().run(context)
    assert context.cv is not None

    context = await AnalyticsAgent().run(context)
    assert context.analytics is not None

    context = await OptimizationAgent().run(context)
    assert context.optimization is not None

    # Check that context holds complete data across all 8 stages
    assert context.optimization.action_proposal is not None
    assert context.optimization.safety_validation.approved_by_safety_gate is True


@pytest.mark.asyncio
async def test_master_orchestrator_integration_with_phase10_optimizer(sample_campaign_context):
    """Verify MasterOrchestrator executes 8-stage plan incorporating OptimizationAgent."""
    context = sample_campaign_context
    planner = CampaignPlanner()
    plan = planner.plan(context)

    # Filter to first 8 stages
    target_stages = {
        "strategy_agent",
        "research_agent",
        "competitor_agent",
        "content_agent",
        "design_agent",
        "cv_agent",
        "analytics_agent",
        "optimization_agent",
    }
    plan.agent_sequence = [s for s in plan.agent_sequence if s.agent_name in target_stages]
    plan.total_steps = len(plan.agent_sequence)

    orchestrator = MasterOrchestrator()
    orchestrated_context = await orchestrator.execute_plan(context=context, plan=plan)

    assert orchestrated_context.optimization is not None
    assert orchestrated_context.optimization.action_proposal is not None
