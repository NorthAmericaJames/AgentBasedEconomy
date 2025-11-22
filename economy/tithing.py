"""
Tithing Logic
=============

This module exposes helper functions for calculating tithing contributions
and applying social reputational effects.  While the main logic resides in
the EconomicEngine, external modules may call these functions to guide
decisions or for standalone simulations of the tithing mechanism【151713287013870†screenshot】.
"""

from __future__ import annotations

from typing import Tuple

from evo_ai.agents.agent import EvolutionaryAgent


def calculate_tithe(earnings_cc: float, reputation: float) -> float:
    """Return a suggested tithing rate based on earnings and reputation.

    This basic implementation mirrors the progressive structure described in
    Section 5.2 of the research paper【151713287013870†screenshot】: higher earners pay a larger
    fraction.  Reputation effects can increase or decrease the suggested
    rate.
    """
    base_rate = 0.10
    if earnings_cc > 1000:
        earnings_multiplier = 1.5
    elif earnings_cc > 100:
        earnings_multiplier = 1.0
    else:
        earnings_multiplier = 0.5
    suggested = base_rate * earnings_multiplier
    # Reputation bonus
    bonus = reputation * 0.05
    return min(1.0, suggested + bonus)


def apply_tithe(agent: EvolutionaryAgent, suggested_rate: float) -> float:
    """Ask an agent how much to tithe and return the amount.

    The agent decides how much to contribute.  This function records the
    tithe in the agent's history and returns the tithe fraction.
    """
    actual_rate = agent.decide_tithe(suggested_rate)
    agent.tithe_history.append(actual_rate)
    return actual_rate
