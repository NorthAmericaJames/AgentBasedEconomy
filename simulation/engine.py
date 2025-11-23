"""
Simulation Engine
=================

This module orchestrates the simulation, managing time steps, agent lifecycles,
market operations, and population dynamics.
"""

from __future__ import annotations
from typing import List, Dict, Any, Optional
import random
from agents.base_agent import BaseAgent
from economy.transaction import TransactionLedger
from evolution.reproduction import ReproductionSystem


class SimulationEngine:
    """
    Main simulation engine that orchestrates the economic ecosystem.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the simulation engine.
        
        Args:
            config: Configuration dictionary with simulation parameters
        """
        # Load configuration
        config = config or {}
        self.starting_wealth = config.get('starting_wealth', 100.0)
        self.tithe_rate = config.get('tithe_rate', 0.1)
        self.reproduction_cost = config.get('reproduction_cost', 50.0)
        self.mutation_rate = config.get('mutation_rate', 0.1)
        self.energy_recovery = config.get('energy_recovery', 5.0)
        self.job_reward_range = config.get('job_reward_range', (5.0, 20.0))
        self.max_population = config.get('max_population', 1000)
        
        # Initialize systems
        self.ledger = TransactionLedger()
        self.reproduction_system = ReproductionSystem(
            mutation_rate=self.mutation_rate,
            reproduction_cost=self.reproduction_cost
        )
        
        # Population and tracking
        self.agents: List[BaseAgent] = []
        self.agent_dict: Dict[str, BaseAgent] = {}  # For quick lookup
        self.current_step = 0
        
        # Market state
        self.available_jobs: List[Dict[str, Any]] = []
        
        # Statistics
        self.stats_history: List[Dict[str, Any]] = []
    
    def initialize_population(self, size: int) -> None:
        """
        Create initial population of agents.
        
        Args:
            size: Number of agents to create
        """
        for _ in range(size):
            agent = BaseAgent(starting_wealth=self.starting_wealth)
            agent.generation = 0
            self.agents.append(agent)
            self.agent_dict[agent.id] = agent
    
    def step(self) -> None:
        """
        Execute one simulation time step.
        """
        self.current_step += 1
        
        # 1. Generate jobs for this step
        self._generate_jobs()
        
        # 2. Agents work
        self._agent_work_phase()
        
        # 3. Agents pay tithes
        self._tithe_phase()
        
        # 4. Agents reproduce
        self._reproduction_phase()
        
        # 5. Age agents and check vitality
        self._aging_phase()
        
        # 6. Cull dead/unfit agents
        self._culling_phase()
        
        # 7. Collect statistics
        self._collect_statistics()
    
    def _generate_jobs(self) -> None:
        """Generate available jobs for this time step."""
        # Clear old jobs
        self.available_jobs = []
        
        # Generate jobs based on population size
        num_jobs = max(10, len(self.agents) // 2)
        
        for i in range(num_jobs):
            job = {
                'id': f"job-{self.current_step}-{i}",
                'reward': random.uniform(*self.job_reward_range),
                'difficulty': random.uniform(0.3, 0.9)
            }
            self.available_jobs.append(job)
    
    def _agent_work_phase(self) -> None:
        """Allow agents to select and perform work."""
        # Shuffle agents for fair job access
        working_agents = self.agents.copy()
        random.shuffle(working_agents)
        
        for agent in working_agents:
            # Agent decides whether to work
            job = agent.decide_work(self.available_jobs)
            
            if job:
                # Perform work
                earnings = agent.work(job)
                
                # Log transaction
                self.ledger.log_transaction(
                    timestamp=self.current_step,
                    transaction_type='work',
                    agent_id=agent.id,
                    counterparty_id=None,
                    amount=earnings,
                    details={'job_id': job['id']}
                )
                
                # Remove job from available jobs
                if job in self.available_jobs:
                    self.available_jobs.remove(job)
    
    def _tithe_phase(self) -> None:
        """Process tithe payments from children to parents."""
        for agent in self.agents:
            # Only pay tithe if has parent and earned money
            if agent.parent_id and agent.total_earnings > 0:
                parent = self.agent_dict.get(agent.parent_id)
                
                if parent:
                    # Calculate tithe on recent earnings (since last step)
                    # For simplicity, use a portion of current wealth
                    earnings_to_tithe = agent.wealth * 0.1  # 10% of current wealth
                    tithe_amount = agent.pay_tithe(parent, self.tithe_rate, earnings_to_tithe)
                    
                    if tithe_amount > 0:
                        # Log transaction
                        self.ledger.log_transaction(
                            timestamp=self.current_step,
                            transaction_type='tithe',
                            agent_id=agent.id,
                            counterparty_id=parent.id,
                            amount=tithe_amount,
                            details={'rate': self.tithe_rate}
                        )
    
    def _reproduction_phase(self) -> None:
        """Allow agents to reproduce."""
        # Limit reproductions per step to avoid population explosion
        max_reproductions = max(5, len(self.agents) // 10)
        reproductions = 0
        
        # Shuffle to give everyone a chance
        potential_parents = [a for a in self.agents if a.decide_reproduce(self.reproduction_cost)]
        random.shuffle(potential_parents)
        
        for agent in potential_parents:
            if reproductions >= max_reproductions:
                break
            
            if len(self.agents) >= self.max_population:
                break  # Population cap reached
            
            # Create offspring
            child = self.reproduction_system.create_offspring(
                agent,
                parent_generation=agent.generation
            )
            
            # Add to population
            self.agents.append(child)
            self.agent_dict[child.id] = child
            
            # Log transaction
            self.ledger.log_transaction(
                timestamp=self.current_step,
                transaction_type='reproduction',
                agent_id=agent.id,
                counterparty_id=child.id,
                amount=self.reproduction_cost,
                details={'generation': child.generation}
            )
            
            reproductions += 1
    
    def _aging_phase(self) -> None:
        """Age all agents and recover energy."""
        for agent in self.agents:
            agent.age_step(self.energy_recovery)
    
    def _culling_phase(self) -> None:
        """Remove dead or unfit agents."""
        alive_agents = []
        
        for agent in self.agents:
            if agent.is_alive():
                alive_agents.append(agent)
            else:
                # Remove from lookup dict
                if agent.id in self.agent_dict:
                    del self.agent_dict[agent.id]
        
        self.agents = alive_agents
    
    def _collect_statistics(self) -> None:
        """Collect statistics about current simulation state."""
        if not self.agents:
            stats = {
                'step': self.current_step,
                'population': 0,
                'avg_wealth': 0,
                'total_wealth': 0,
                'avg_age': 0,
                'avg_fitness': 0,
                'generations': {}
            }
        else:
            total_wealth = sum(a.wealth for a in self.agents)
            total_age = sum(a.age for a in self.agents)
            total_fitness = sum(a.get_fitness() for a in self.agents)
            
            # Generation distribution
            gen_dist = {}
            for agent in self.agents:
                gen = agent.generation
                gen_dist[gen] = gen_dist.get(gen, 0) + 1
            
            stats = {
                'step': self.current_step,
                'population': len(self.agents),
                'avg_wealth': total_wealth / len(self.agents),
                'total_wealth': total_wealth,
                'avg_age': total_age / len(self.agents),
                'avg_fitness': total_fitness / len(self.agents),
                'generations': gen_dist,
                'max_generation': max(a.generation for a in self.agents),
                'total_births': self.reproduction_system.total_births
            }
        
        self.stats_history.append(stats)
    
    def run(self, steps: int, verbose: bool = False) -> None:
        """
        Run the simulation for a specified number of steps.
        
        Args:
            steps: Number of time steps to simulate
            verbose: If True, print progress updates
        """
        for i in range(steps):
            self.step()
            
            if verbose and (i + 1) % 10 == 0:
                stats = self.stats_history[-1]
                print(f"Step {self.current_step}: "
                      f"Pop={stats['population']}, "
                      f"AvgWealth={stats['avg_wealth']:.2f}, "
                      f"MaxGen={stats.get('max_generation', 0)}")
    
    def get_current_statistics(self) -> Dict[str, Any]:
        """Get statistics for the current step."""
        if self.stats_history:
            return self.stats_history[-1]
        return {}
    
    def get_agent_by_id(self, agent_id: str) -> Optional[BaseAgent]:
        """Get an agent by ID."""
        return self.agent_dict.get(agent_id)
    
    def export_results(self, transactions_file: str, stats_file: str) -> None:
        """
        Export simulation results.
        
        Args:
            transactions_file: Path for transactions CSV
            stats_file: Path for statistics JSON
        """
        import json
        
        # Export transactions
        self.ledger.export_to_csv(transactions_file)
        
        # Export statistics
        with open(stats_file, 'w') as f:
            json.dump(self.stats_history, f, indent=2)
