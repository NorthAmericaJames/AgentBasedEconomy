"""
Economic Engine and Market Mechanics
====================================

This module implements the central economic engine that manages resource
exchange, task payments, tithing contributions, and reputation updates【151713287013870†screenshot】.
The implementation follows the pseudocode described in the research paper
(Section 6.3), but is simplified for initial scaffolding.  It should be
extended by other agents to include more detailed transaction logic, fraud
detection, and dynamic exchange rate adjustment【151713287013870†screenshot】.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from evo_ai.agents.agent import EvolutionaryAgent, Task, TaskResult


@dataclass
class TransactionRecord:
    agent_id: str
    task_id: str
    gross_earnings: float
    tithe: float
    net_earnings: float
    reputation_change: float


class EconomicEngine:
    """Simplified economic engine for compute credits and value tokens."""

    def __init__(self) -> None:
        self.compute_credit_supply: float = 0.0
        self.value_token_treasury: float = 0.0
        self.tithing_pool: Dict[str, float] = {
            "infrastructure": 0.0,
            "population_support": 0.0,
            "reserve": 0.0,
        }
        self.exchange_rate: float = 1.0
        self.transactions: list[TransactionRecord] = []

    # ------------------------------------------------------------------
    # Payment processing
    # ------------------------------------------------------------------
    def evaluate_quality(self, result: TaskResult, requirements: Dict[str, Any] | None) -> float:
        """Evaluate task result quality with respect to requirements.

        In the simplified model, we return a constant quality score.  Future
        iterations should implement metrics such as accuracy, latency, or
        client satisfaction【151713287013870†screenshot】.
        """
        return 1.0

    def calculate_suggested_tithe(self, earnings_cc: float, reputation: float) -> float:
        """Compute a suggested tithing rate based on earnings and reputation.

        This implementation returns the baseline rate of 10%.  More
        sophisticated logic (e.g., progressive tiers) should be added by
        extending agents or this engine【151713287013870†screenshot】.
        """
        return 0.10

    def update_reputation(self, agent: EvolutionaryAgent, ratio: float) -> None:
        """Update agent reputation based on tithe behavior.

        Agents gain or lose reputation depending on how their actual
        contribution compares to the suggested rate【151713287013870†screenshot】.
        """
        agent.reputation += 0.1 * (ratio - 1.0)
        agent.reputation = max(0.0, min(1.0, agent.reputation))

    def record_transaction(self, **kwargs: Any) -> None:
        """Record a transaction in the ledger."""
        self.transactions.append(TransactionRecord(**kwargs))

    def process_task_completion(
        self,
        agent: EvolutionaryAgent,
        task: Task,
        result: TaskResult,
        client_payment_vt: float,
    ) -> None:
        """Handle payments when an external client pays for a completed task.

        Converts value tokens to compute credits at a fixed exchange rate,
        suggests a tithe, and distributes the tithe across the pools【151713287013870†screenshot】.
        """
        quality = self.evaluate_quality(result, task.requirements)
        earnings_vt = client_payment_vt * quality
        earnings_cc = earnings_vt * self.exchange_rate

        suggested = self.calculate_suggested_tithe(earnings_cc, agent.reputation)
        actual_rate = agent.decide_tithe(suggested)
        tithe_amount = earnings_cc * actual_rate
        net = earnings_cc - tithe_amount

        # Pay agent
        agent.wallet["compute_credits"] += net
        # Collect tithe
        self.tithing_pool["infrastructure"] += tithe_amount * 0.40
        self.tithing_pool["population_support"] += tithe_amount * 0.35
        self.tithing_pool["reserve"] += tithe_amount * 0.25
        agent.tithe_history.append(tithe_amount)
        # Update supply
        self.compute_credit_supply += earnings_cc

        # Update reputation
        if suggested > 0:
            self.update_reputation(agent, actual_rate / suggested)

        # Log transaction
        self.record_transaction(
            agent_id=agent.id,
            task_id=task.id,
            gross_earnings=earnings_cc,
            tithe=tithe_amount,
            net_earnings=net,
            reputation_change=agent.reputation,
        )
