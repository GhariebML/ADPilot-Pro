import numpy as np
import pytest
from adpilot.rl.contextual_bandits import ContextualLinUCB, ThompsonSamplingBandit


def test_linucb_initialization_and_selection():
    n_arms = 4
    dim = 6
    bandit = ContextualLinUCB(n_arms=n_arms, feature_dim=dim, alpha=1.2)

    context = np.random.randn(dim)
    arm = bandit.select_arm(context)
    assert 0 <= arm < n_arms

    # Update with reward
    bandit.update(arm=arm, context=context, reward=1.5)
    assert bandit.A[arm].shape == (dim, dim)
    assert bandit.b[arm].shape == (dim, 1)


def test_linucb_convergence_to_optimal_arm():
    np.random.seed(42)
    n_arms = 3
    dim = 4
    bandit = ContextualLinUCB(n_arms=n_arms, feature_dim=dim, alpha=0.5)

    # True parameter weights for each arm
    true_thetas = [
        np.array([1.0, 0.0, 0.0, 0.0]),
        np.array([0.0, 2.5, 0.0, 0.0]),  # Superior for feature 1
        np.array([0.0, 0.0, 0.5, 0.0]),
    ]

    context = np.array([0.1, 1.0, 0.1, 0.0])  # Feature 1 is high, arm 1 should dominate

    for _ in range(50):
        arm = bandit.select_arm(context)
        reward = float(np.dot(context, true_thetas[arm])) + np.random.normal(0, 0.1)
        bandit.update(arm, context, reward)

    # After 50 rounds, arm 1 should be selected
    best_arm = bandit.select_arm(context)
    assert best_arm == 1


def test_thompson_sampling_bandit_selection_and_update():
    np.random.seed(42)
    n_arms = 5
    dim = 8
    bandit = ThompsonSamplingBandit(n_arms=n_arms, feature_dim=dim, v_sq=0.2)

    context = np.random.randn(dim)
    selected_arm = bandit.select_arm(context)
    assert 0 <= selected_arm < n_arms

    bandit.update(arm=selected_arm, context=context, reward=2.0)
    assert bandit.B[selected_arm].shape == (dim, dim)
    assert bandit.f[selected_arm].shape == (dim, 1)
