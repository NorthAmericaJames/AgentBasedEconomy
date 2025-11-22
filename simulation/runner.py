"""
Simulation Runner
=================

This module defines a basic simulation loop that runs multiple
generations of agents through a simple environment.  It uses the
EvolutionManager to handle selection, reproduction, and culling.  This
runner is intended as a starting point for more complex simulations.
"""

from evo_ai.evolution.manager import EvolutionManager
from evo_ai.simulation.environment import create_simple_tasks, run_tasks


def run_simulation(manager: EvolutionManager, generations: int, tasks_per_gen: int, survivors: int, offspring_count: int) -> None:
    """Run a multi‑generation simulation.

    Args:
        manager: The EvolutionManager controlling the population.
        generations: Number of generations to simulate.
        tasks_per_gen: Number of tasks each agent attempts per generation.
        survivors: Number of agents that survive each generation.
        offspring_count: Number of offspring to produce per generation.
    """
    for gen in range(generations):
        tasks = create_simple_tasks(tasks_per_gen)
        # Each agent performs tasks
        for agent in manager.population:
            run_tasks(agent, tasks)
        # Evolution step
        manager.run_generation(
            tasks=[],  # no additional tasks in this call
            survivors=survivors,
            offspring_count=offspring_count,
        )
