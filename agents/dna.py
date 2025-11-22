"""
Agent DNA Schema
=================

This module defines the `AgentDNA` class, which encapsulates the genetic
configuration for an evolutionary agent.  The DNA structure determines the
agent's role (e.g., trader, analyst, optimizer), its neural architecture,
memory capacities, learning rates, and mutation parameters.  It serves as
the blueprint passed from parent agents to their offspring during
reproduction【151713287013870†screenshot】.  Mutations and crossover on this DNA allow
for diversity and adaptation over generations【151713287013870†screenshot】.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List
import random
import copy


@dataclass
class AgentDNA:
    """Representation of an agent's genetic information.

    Attributes:
        role: High‑level role that determines the agent's specialization (e.g.
            ``"trader"``, ``"analyst"``, ``"optimizer"``).  Roles influence
            task allocation in the marketplace【151713287013870†screenshot】.
        skill_genes: A dictionary or structured representation of skills and
            competencies.  Each gene controls some ability or feature that
            affects the agent's performance.
        architecture_genes: Configuration of the agent's neural network
            architecture (layer sizes, activations, etc.).  Mutation on
            architecture_genes allows for neuroevolution【151713287013870†screenshot】.
        memory_size: Capacity of the agent's episodic memory.  Larger
            memories enable longer context windows but require more compute.
        context_size: Size of the working memory context window for inference.
        mutation_rate: Base mutation rate applied during reproduction【151713287013870†screenshot】.
        learning_rate: Learning rate for neural updates【151713287013870†screenshot】.
    """

    role: str
    skill_genes: Dict[str, Any]
    architecture_genes: Dict[str, Any]
    memory_size: int = 512
    context_size: int = 512
    mutation_rate: float = 0.05
    learning_rate: float = 0.001

    def mutate(self, rate: float | None = None) -> "AgentDNA":
        """Return a mutated copy of this DNA.

        The mutation operator randomly perturbs genes with probability equal
        to ``rate``.  For numerical parameters, small Gaussian noise is
        applied; for categorical parameters, random selection from an
        allowed set is performed.  This simple implementation is intended
        as a starting point and should be extended by downstream agents.
        """
        mutation_rate = rate if rate is not None else self.mutation_rate
        mutated = copy.deepcopy(self)
        # Mutate numeric genes
        for key, value in mutated.skill_genes.items():
            if isinstance(value, (int, float)) and random.random() < mutation_rate:
                noise = random.gauss(0, 0.1 * abs(value) + 1e-6)
                mutated.skill_genes[key] = value + noise
        # Mutate architecture genes (e.g., layer sizes)
        for key, value in mutated.architecture_genes.items():
            if isinstance(value, int) and random.random() < mutation_rate:
                mutated.architecture_genes[key] = max(1, value + random.randint(-1, 1))
        # Adjust mutation_rate slightly
        if random.random() < mutation_rate:
            mutated.mutation_rate = max(0.001, min(0.5, mutated.mutation_rate + random.uniform(-0.01, 0.01)))
        return mutated

    def crossover(self, other: "AgentDNA") -> "AgentDNA":
        """Perform crossover between this DNA and another to produce child DNA.

        Genes are selected at random from either parent.  This operation is
        symmetric and does not mutate genes.  Mutation should be applied
        separately after crossover【151713287013870†screenshot】.
        """
        child_genes = {}
        for key in self.skill_genes:
            child_genes[key] = self.skill_genes[key] if random.random() < 0.5 else other.skill_genes.get(key, self.skill_genes[key])
        child_arch = {}
        for key in self.architecture_genes:
            child_arch[key] = self.architecture_genes[key] if random.random() < 0.5 else other.architecture_genes.get(key, self.architecture_genes[key])
        return AgentDNA(
            role=self.role if random.random() < 0.5 else other.role,
            skill_genes=child_genes,
            architecture_genes=child_arch,
            memory_size=self.memory_size if random.random() < 0.5 else other.memory_size,
            context_size=self.context_size if random.random() < 0.5 else other.context_size,
            mutation_rate=self.mutation_rate if random.random() < 0.5 else other.mutation_rate,
            learning_rate=self.learning_rate if random.random() < 0.5 else other.learning_rate,
        )

    def copy(self) -> "AgentDNA":
        """Return a deep copy of this DNA."""
        return copy.deepcopy(self)
