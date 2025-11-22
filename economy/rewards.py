"""
Reward Distribution
===================

This module encapsulates logic for calculating and distributing rewards to
agents based on task outcomes.  It defines abstract interfaces that can be
extended to implement domain‑specific reward functions【151713287013870†screenshot】.
"""

from __future__ import annotations

from typing import Any

from agents.agent import EvolutionaryAgent, Task, TaskResult


def default_reward_function(result: TaskResult, task: Task) -> float:
    """Compute a reward for a task result.

    This default implementation assigns a constant reward.  Downstream
    agents should customize this function to reflect task‑specific
    objectives, such as accuracy or latency【151713287013870†screenshot】.
    """
    return 1.0


def distribute_reward(agent: EvolutionaryAgent, reward: float, task: Task) -> None:
    """Update the agent's state with the specified reward.

    This wrapper forwards to the agent's ``receive_reward`` method.  It
    exists to decouple reward calculation from state updates and to allow
    for logging or side effects.
    """
    agent.receive_reward(reward, task)
