"""
Reproduction System
===================

This module handles agent reproduction, including DNA inheritance,
mutation, and parent-child relationships.
"""

from __future__ import annotations
from typing import Optional, Dict, Any, List
import random
import copy


class ReproductionSystem:
    """
    Manages reproduction and genetic inheritance for agents.
    """
    
    def __init__(self, mutation_rate: float = 0.1, reproduction_cost: float = 50.0):
        """
        Initialize reproduction system.
        
        Args:
            mutation_rate: Base probability of mutation (0.0 to 1.0)
            reproduction_cost: Cost in wealth to create offspring
        """
        self.mutation_rate = mutation_rate
        self.reproduction_cost = reproduction_cost
        self.total_births = 0
    
    def create_offspring(
        self,
        parent,  # BaseAgent
        parent_generation: int = 0
    ):
        """
        Create an offspring from a single parent (asexual reproduction).
        
        Args:
            parent: Parent agent
            parent_generation: Generation of the parent
            
        Returns:
            New agent (child)
        """
        # Import here to avoid circular dependency
        from agents.base_agent import BaseAgent
        
        # Inherit DNA with mutations
        child_dna = self._inherit_dna(parent.dna, None)
        
        # Create child with inherited DNA
        child = BaseAgent(
            dna=child_dna,
            parent_id=parent.id,
            starting_wealth=0.0  # Children start with no wealth
        )
        
        # Set generation
        child.generation = parent_generation + 1
        
        # Parent pays reproduction cost
        if parent.wealth >= self.reproduction_cost:
            parent.wealth -= self.reproduction_cost
        else:
            # If can't afford full cost, pay what they can
            parent.wealth = 0.0
        
        # Add to parent's children list
        parent.children.append(child.id)
        
        # Track births
        self.total_births += 1
        
        return child
    
    def create_offspring_sexual(
        self,
        parent1,  # BaseAgent
        parent2,  # BaseAgent
        parent_generation: int = 0
    ):
        """
        Create an offspring from two parents (sexual reproduction).
        
        Args:
            parent1: First parent
            parent2: Second parent
            parent_generation: Generation of parents (should be same)
            
        Returns:
            New agent (child)
        """
        # Import here to avoid circular dependency
        from agents.base_agent import BaseAgent
        
        # Crossover and mutate DNA
        child_dna = self._inherit_dna(parent1.dna, parent2.dna)
        
        # Create child
        child = BaseAgent(
            dna=child_dna,
            parent_id=parent1.id,  # Primary parent
            starting_wealth=0.0
        )
        
        # Set generation
        child.generation = max(parent1.generation, parent2.generation) + 1
        
        # Both parents share reproduction cost
        cost_per_parent = self.reproduction_cost / 2.0
        
        if parent1.wealth >= cost_per_parent:
            parent1.wealth -= cost_per_parent
        else:
            parent1.wealth = 0.0
        
        if parent2.wealth >= cost_per_parent:
            parent2.wealth -= cost_per_parent
        else:
            parent2.wealth = 0.0
        
        # Add to both parents' children lists
        parent1.children.append(child.id)
        parent2.children.append(child.id)
        
        # Track births
        self.total_births += 1
        
        return child
    
    def _inherit_dna(
        self,
        dna1: Dict[str, Any],
        dna2: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Inherit DNA from parent(s) with mutation.
        
        Args:
            dna1: First parent's DNA
            dna2: Second parent's DNA (None for asexual)
            
        Returns:
            Child's DNA
        """
        child_dna = {}
        
        if dna2 is None:
            # Asexual: clone parent DNA
            child_dna = copy.deepcopy(dna1)
        else:
            # Sexual: crossover from both parents
            for key in dna1.keys():
                if key in dna2:
                    # Randomly select from either parent
                    child_dna[key] = random.choice([dna1[key], dna2[key]])
                else:
                    child_dna[key] = dna1[key]
            
            # Add any unique traits from parent2
            for key in dna2.keys():
                if key not in child_dna:
                    child_dna[key] = dna2[key]
        
        # Apply mutations
        child_dna = self._mutate_dna(child_dna)
        
        return child_dna
    
    def _mutate_dna(self, dna: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply random mutations to DNA.
        
        Args:
            dna: DNA to mutate
            
        Returns:
            Mutated DNA
        """
        mutated = copy.deepcopy(dna)
        
        for key, value in mutated.items():
            if random.random() < self.mutation_rate:
                if isinstance(value, float):
                    # Gaussian mutation for float values
                    noise = random.gauss(0, 0.1)
                    mutated[key] = max(0.0, min(1.0, value + noise))  # Keep in [0, 1]
                elif isinstance(value, int):
                    # Small random change for integers
                    mutated[key] = max(0, value + random.randint(-1, 1))
        
        return mutated
    
    def should_cull(self, agent, min_fitness: float = 0.0) -> bool:
        """
        Determine if an agent should be removed from the population.
        
        Args:
            agent: Agent to evaluate
            min_fitness: Minimum fitness threshold
            
        Returns:
            True if agent should be culled
        """
        # Check if agent is alive
        if not agent.is_alive():
            return True
        
        # Check fitness threshold
        if agent.get_fitness() < min_fitness:
            return True
        
        return False
    
    def select_parents(
        self,
        population: List,  # List[BaseAgent]
        count: int,
        selection_method: str = 'fitness'
    ) -> List:
        """
        Select parents for reproduction.
        
        Args:
            population: List of agents
            count: Number of parents to select
            selection_method: 'fitness', 'random', or 'tournament'
            
        Returns:
            List of selected parents
        """
        if not population:
            return []
        
        count = min(count, len(population))
        
        if selection_method == 'fitness':
            # Select top performers by fitness
            sorted_pop = sorted(population, key=lambda a: a.get_fitness(), reverse=True)
            return sorted_pop[:count]
        
        elif selection_method == 'random':
            # Random selection
            return random.sample(population, count)
        
        elif selection_method == 'tournament':
            # Tournament selection
            parents = []
            for _ in range(count):
                # Run a tournament of 3 agents
                tournament = random.sample(population, min(3, len(population)))
                winner = max(tournament, key=lambda a: a.get_fitness())
                parents.append(winner)
            return parents
        
        return []
    
    def get_lineage(self, agent, agent_dict: Dict[str, Any]) -> List[str]:
        """
        Get the lineage of an agent (list of ancestor IDs).
        
        Args:
            agent: Agent to trace
            agent_dict: Dictionary mapping agent IDs to agents
            
        Returns:
            List of ancestor IDs from oldest to newest
        """
        lineage = []
        current = agent
        
        while current.parent_id is not None:
            lineage.append(current.parent_id)
            if current.parent_id in agent_dict:
                current = agent_dict[current.parent_id]
            else:
                break  # Parent no longer exists
        
        return list(reversed(lineage))
