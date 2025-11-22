"""
Evolution Manager
=================

The `EvolutionManager` is responsible for orchestrating selection,
mutation, and reproduction across the population of agents.  It implements
the evolutionary algorithms described in the research paper, such as
selecting top performers, applying mutations to DNA, and culling poor
performers【151713287013870†screenshot】.

This skeleton provides basic hooks for these operations.  Future
enhancements should incorporate more sophisticated selection strategies
(e.g., tournament selection, novelty search) and handle concurrency when
running large populations on distributed compute platforms like Ray
【151713287013870†screenshot】.
"""

from __future__ import annotations

from typing import List, Callable, Optional

from evo_ai.agents.agent import EvolutionaryAgent
from evo_ai.agents.dna import AgentDNA


class EvolutionManager:
    """Manage the evolutionary cycle for a population of agents."""

    def __init__(self, population: Optional[List[EvolutionaryAgent]] = None) -> None:
        self.population: List[EvolutionaryAgent] = population or []

    def select(self, k: int) -> List[EvolutionaryAgent]:
        """Select the top ``k`` agents based on fitness.

        This simplistic implementation sorts by fitness and returns the top
        performers.  More nuanced criteria (diversity, reputation) should
        be added to avoid premature convergence【151713287013870†screenshot】.
        """
        sorted_agents = sorted(self.population, key=lambda a: a.fitness, reverse=True)
        return sorted_agents[:k]

    def reproduce(self, parents: List[EvolutionaryAgent], offspring_count: int) -> List[EvolutionaryAgent]:
        """Create offspring from a list of parents.

        Offspring are produced by randomly pairing parents and applying
        reproduction.  If only one parent is provided, reproduction is
        asexual.
        """
        children: List[EvolutionaryAgent] = []
        import random
        for _ in range(offspring_count):
            if len(parents) >= 2:
                mother, father = random.sample(parents, 2)
                child = mother.reproduce(partner=father)
            else:
                child = parents[0].reproduce()
            children.append(child)
        return children

    def cull(self, survivors: int) -> None:
        """Remove the lowest‑performing agents so that only ``survivors`` remain."""
        if survivors < len(self.population):
            sorted_agents = sorted(self.population, key=lambda a: a.fitness, reverse=True)
            self.population = sorted_agents[:survivors]

    def run_generation(self, tasks: List[Callable[[EvolutionaryAgent], None]], survivors: int, offspring_count: int) -> None:
        """Run one evolutionary generation.

        Each agent executes tasks, receives rewards, and accumulates fitness.
        The manager then selects top performers, reproduces to create
        offspring, and culls the population to maintain a constant size.
        """
        # Execute tasks for each agent
        for agent in self.population:
            for task in tasks:
                task(agent)
        # Selection and reproduction
        parents = self.select(survivors)
        children = self.reproduce(parents, offspring_count)
        # Cull and add offspring
        self.cull(survivors)
        self.population.extend(children)
