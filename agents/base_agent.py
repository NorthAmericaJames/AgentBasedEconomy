"""
Base Agent for MVP
==================

This module defines a simplified BaseAgent class for the MVP implementation.
It focuses on core functionality: wealth, lineage, DNA-based traits, and basic decision-making.
"""

from __future__ import annotations
from typing import Optional, Dict, Any
import uuid
import random


class BaseAgent:
    """
    A simplified agent for the MVP implementation.
    
    Attributes:
        id: Unique identifier for the agent
        wealth: Current wealth (compute credits)
        generation: Generation number (0 for initial agents)
        parent_id: ID of parent agent (None for initial agents)
        dna: Dictionary of inheritable traits
        age: Current age in simulation steps
        energy: Vitality/energy level (0-100)
    """
    
    def __init__(
        self,
        dna: Optional[Dict[str, Any]] = None,
        parent_id: Optional[str] = None,
        starting_wealth: float = 100.0
    ):
        """
        Initialize a new agent.
        
        Args:
            dna: Dictionary of genetic traits (risk_tolerance, efficiency, innovation_rate)
            parent_id: ID of parent agent (None for initial generation)
            starting_wealth: Initial wealth in compute credits
        """
        self.id: str = str(uuid.uuid4())
        self.wealth: float = starting_wealth
        self.parent_id: Optional[str] = parent_id
        self.generation: int = 0  # Will be set by parent during reproduction
        self.age: int = 0
        self.energy: float = 100.0
        
        # DNA/genome system
        if dna is None:
            # Default DNA for initial agents
            self.dna = {
                'risk_tolerance': random.uniform(0.3, 0.7),
                'efficiency': random.uniform(0.5, 1.0),
                'innovation_rate': random.uniform(0.1, 0.5)
            }
        else:
            self.dna = dna.copy()
        
        # Track children
        self.children: list[str] = []
        
        # Performance tracking
        self.total_earnings: float = 0.0
        self.total_tithes_paid: float = 0.0
        self.total_tithes_received: float = 0.0
        self.tasks_completed: int = 0
    
    def decide_work(self, available_jobs: list[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Decide whether to work and which job to take.
        
        Args:
            available_jobs: List of job dictionaries with 'id', 'reward', 'difficulty'
            
        Returns:
            Selected job or None if declining to work
        """
        if not available_jobs:
            return None
        
        # Decision based on energy and risk tolerance
        if self.energy < 20:
            return None  # Too tired to work
        
        # Filter jobs by difficulty based on efficiency
        suitable_jobs = [
            job for job in available_jobs 
            if job.get('difficulty', 0.5) <= self.dna['efficiency']
        ]
        
        if not suitable_jobs:
            suitable_jobs = available_jobs  # Take what's available
        
        # Choose job based on risk tolerance
        if self.dna['risk_tolerance'] > 0.6:
            # High risk tolerance: go for highest reward
            return max(suitable_jobs, key=lambda x: x.get('reward', 0))
        else:
            # Low risk tolerance: balance reward and difficulty
            return min(
                suitable_jobs,
                key=lambda x: x.get('difficulty', 0.5) - x.get('reward', 0) * 0.5
            )
    
    def work(self, job: Dict[str, Any]) -> float:
        """
        Perform work and return the earnings.
        
        Args:
            job: Job dictionary with 'reward' and 'difficulty'
            
        Returns:
            Actual earnings (can be modified by efficiency)
        """
        base_reward = job.get('reward', 10.0)
        difficulty = job.get('difficulty', 0.5)
        
        # Earnings modified by efficiency
        efficiency_modifier = self.dna['efficiency'] / difficulty if difficulty > 0 else self.dna['efficiency']
        earnings = base_reward * min(efficiency_modifier, 1.5)  # Cap at 150%
        
        # Energy cost
        energy_cost = difficulty * 10
        self.energy = max(0, self.energy - energy_cost)
        
        # Update stats
        self.wealth += earnings
        self.total_earnings += earnings
        self.tasks_completed += 1
        
        return earnings
    
    def decide_trade(self, other_agent: 'BaseAgent', offer: Dict[str, Any]) -> bool:
        """
        Decide whether to accept a trade offer.
        
        Args:
            other_agent: The agent making the offer
            offer: Dictionary with trade details
            
        Returns:
            True to accept, False to decline
        """
        # Simple trade logic based on risk tolerance
        offered_value = offer.get('value', 0)
        requested_value = offer.get('cost', 0)
        
        if requested_value > self.wealth:
            return False  # Can't afford it
        
        # Accept if value > cost, with risk tolerance affecting threshold
        threshold = 1.0 + (0.5 - self.dna['risk_tolerance'])
        return offered_value / requested_value >= threshold if requested_value > 0 else False
    
    def decide_reproduce(self, reproduction_cost: float) -> bool:
        """
        Decide whether to reproduce.
        
        Args:
            reproduction_cost: Cost of creating offspring
            
        Returns:
            True to reproduce, False otherwise
        """
        # Can't afford it
        if self.wealth < reproduction_cost:
            return False
        
        # Need minimum age
        if self.age < 10:
            return False
        
        # Need sufficient energy
        if self.energy < 50:
            return False
        
        # Decision based on wealth level and innovation rate
        wealth_threshold = reproduction_cost * (2.0 - self.dna['innovation_rate'])
        return self.wealth >= wealth_threshold
    
    def pay_tithe(self, parent_agent: Optional['BaseAgent'], tithe_rate: float, earnings: float) -> float:
        """
        Pay tithe to parent agent.
        
        Args:
            parent_agent: Parent agent to receive tithe
            tithe_rate: Percentage to pay (0.0 to 1.0)
            earnings: Recent earnings to tithe from
            
        Returns:
            Amount paid
        """
        tithe_amount = earnings * tithe_rate
        
        if tithe_amount > self.wealth:
            tithe_amount = self.wealth  # Pay what we can
        
        self.wealth -= tithe_amount
        self.total_tithes_paid += tithe_amount
        
        if parent_agent:
            parent_agent.receive_tithe(tithe_amount)
        
        return tithe_amount
    
    def receive_tithe(self, amount: float) -> None:
        """
        Receive tithe from child agent.
        
        Args:
            amount: Tithe amount to receive
        """
        self.wealth += amount
        self.total_tithes_received += amount
    
    def age_step(self, energy_recovery: float = 5.0) -> None:
        """
        Age the agent by one time step.
        
        Args:
            energy_recovery: Amount of energy recovered per step
        """
        self.age += 1
        self.energy = min(100.0, self.energy + energy_recovery)
    
    def is_alive(self) -> bool:
        """
        Check if agent should remain in simulation.
        
        Returns:
            True if agent is alive, False if should be removed
        """
        # Die if bankrupt or too old without resources
        if self.wealth <= 0 and self.age > 50:
            return False
        
        # Die if energy depleted for too long
        if self.energy <= 0 and self.wealth < 10:
            return False
        
        return True
    
    def get_fitness(self) -> float:
        """
        Calculate agent's fitness score.
        
        Returns:
            Fitness score based on wealth, age, and productivity
        """
        if self.age == 0:
            return self.wealth
        
        # Fitness combines wealth, productivity, and survival
        productivity = self.tasks_completed / self.age if self.age > 0 else 0
        return self.wealth + (productivity * 10) + len(self.children) * 5
