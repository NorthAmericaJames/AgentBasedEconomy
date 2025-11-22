"""
Metrics and Dashboard
=====================

This module provides metrics collection and text-based dashboard visualization
for the simulation.
"""

from __future__ import annotations
from typing import List, Dict, Any, Optional
import json
import csv
from datetime import datetime


class Metrics:
    """
    Collects and displays metrics about the simulation.
    """
    
    def __init__(self, simulation_engine=None):
        """
        Initialize metrics collector.
        
        Args:
            simulation_engine: Reference to the simulation engine
        """
        self.engine = simulation_engine
    
    def get_population_stats(self) -> Dict[str, Any]:
        """
        Get current population statistics.
        
        Returns:
            Dictionary of population metrics
        """
        if not self.engine or not self.engine.agents:
            return {
                'total': 0,
                'by_generation': {},
                'avg_age': 0,
                'max_age': 0,
                'min_age': 0
            }
        
        agents = self.engine.agents
        ages = [a.age for a in agents]
        
        # Generation distribution
        gen_dist = {}
        for agent in agents:
            gen = agent.generation
            gen_dist[gen] = gen_dist.get(gen, 0) + 1
        
        return {
            'total': len(agents),
            'by_generation': gen_dist,
            'avg_age': sum(ages) / len(ages) if ages else 0,
            'max_age': max(ages) if ages else 0,
            'min_age': min(ages) if ages else 0
        }
    
    def get_wealth_distribution(self) -> Dict[str, Any]:
        """
        Get wealth distribution statistics.
        
        Returns:
            Dictionary of wealth metrics
        """
        if not self.engine or not self.engine.agents:
            return {
                'total': 0,
                'average': 0,
                'median': 0,
                'max': 0,
                'min': 0,
                'gini_coefficient': 0
            }
        
        wealths = sorted([a.wealth for a in self.engine.agents])
        n = len(wealths)
        total = sum(wealths)
        
        # Median
        median = wealths[n // 2] if n > 0 else 0
        
        # Gini coefficient (measure of inequality)
        if total == 0:
            gini = 0
        else:
            cumsum = 0
            gini_sum = 0
            for i, w in enumerate(wealths):
                cumsum += w
                gini_sum += (2 * (i + 1) - n - 1) * w
            gini = gini_sum / (n * total) if n > 0 and total > 0 else 0
        
        return {
            'total': total,
            'average': total / n if n > 0 else 0,
            'median': median,
            'max': max(wealths) if wealths else 0,
            'min': min(wealths) if wealths else 0,
            'gini_coefficient': gini
        }
    
    def get_generational_analysis(self) -> Dict[str, Any]:
        """
        Get analysis of different generations.
        
        Returns:
            Dictionary with per-generation statistics
        """
        if not self.engine or not self.engine.agents:
            return {}
        
        gen_stats = {}
        
        for agent in self.engine.agents:
            gen = agent.generation
            if gen not in gen_stats:
                gen_stats[gen] = {
                    'count': 0,
                    'total_wealth': 0,
                    'total_fitness': 0,
                    'avg_age': 0,
                    'ages': []
                }
            
            gen_stats[gen]['count'] += 1
            gen_stats[gen]['total_wealth'] += agent.wealth
            gen_stats[gen]['total_fitness'] += agent.get_fitness()
            gen_stats[gen]['ages'].append(agent.age)
        
        # Calculate averages
        for gen, stats in gen_stats.items():
            count = stats['count']
            stats['avg_wealth'] = stats['total_wealth'] / count if count > 0 else 0
            stats['avg_fitness'] = stats['total_fitness'] / count if count > 0 else 0
            stats['avg_age'] = sum(stats['ages']) / count if stats['ages'] else 0
            del stats['ages']  # Remove raw data
        
        return gen_stats
    
    def get_economic_health(self) -> Dict[str, Any]:
        """
        Get economic health indicators.
        
        Returns:
            Dictionary of economic health metrics
        """
        if not self.engine:
            return {
                'transaction_volume': 0,
                'active_agents': 0,
                'reproduction_rate': 0,
                'death_rate': 0
            }
        
        # Transaction volume
        txn_stats = self.engine.ledger.get_statistics()
        
        # Recent activity (last 10 steps if available)
        recent_steps = 10
        recent_births = 0
        recent_deaths = 0
        
        if len(self.engine.stats_history) > recent_steps:
            recent_history = self.engine.stats_history[-recent_steps:]
            start_pop = recent_history[0]['population']
            end_pop = recent_history[-1]['population']
            start_births = recent_history[0].get('total_births', 0)
            end_births = recent_history[-1].get('total_births', 0)
            
            recent_births = end_births - start_births
            recent_deaths = start_pop + recent_births - end_pop
        
        return {
            'transaction_volume': txn_stats['total_volume'],
            'total_transactions': txn_stats['total_transactions'],
            'active_agents': len(self.engine.agents),
            'recent_births': recent_births,
            'recent_deaths': recent_deaths,
            'reproduction_rate': recent_births / recent_steps if recent_steps > 0 else 0,
            'death_rate': recent_deaths / recent_steps if recent_steps > 0 else 0
        }
    
    def export_to_csv(self, filename: str) -> None:
        """
        Export metrics to CSV file.
        
        Args:
            filename: Output CSV file path
        """
        if not self.engine or not self.engine.stats_history:
            return
        
        with open(filename, 'w', newline='') as f:
            if not self.engine.stats_history:
                return
            
            # Use first entry to get fieldnames
            fieldnames = ['step', 'population', 'avg_wealth', 'total_wealth', 
                         'avg_age', 'avg_fitness', 'max_generation', 'total_births']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for stats in self.engine.stats_history:
                row = {
                    'step': stats.get('step', 0),
                    'population': stats.get('population', 0),
                    'avg_wealth': stats.get('avg_wealth', 0),
                    'total_wealth': stats.get('total_wealth', 0),
                    'avg_age': stats.get('avg_age', 0),
                    'avg_fitness': stats.get('avg_fitness', 0),
                    'max_generation': stats.get('max_generation', 0),
                    'total_births': stats.get('total_births', 0)
                }
                writer.writerow(row)
    
    def export_to_json(self, filename: str) -> None:
        """
        Export metrics to JSON file.
        
        Args:
            filename: Output JSON file path
        """
        if not self.engine:
            return
        
        data = {
            'population_stats': self.get_population_stats(),
            'wealth_distribution': self.get_wealth_distribution(),
            'generational_analysis': self.get_generational_analysis(),
            'economic_health': self.get_economic_health(),
            'history': self.engine.stats_history
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def display_dashboard(self) -> None:
        """Display a text-based dashboard."""
        print("\n" + "="*60)
        print("EVOLUTIONARY AI ECONOMIC ECOSYSTEM - DASHBOARD")
        print("="*60)
        
        if not self.engine:
            print("No simulation engine connected.")
            return
        
        # Current step
        print(f"\nCurrent Step: {self.engine.current_step}")
        
        # Population stats
        print("\n--- POPULATION STATISTICS ---")
        pop_stats = self.get_population_stats()
        print(f"Total Population: {pop_stats['total']}")
        print(f"Average Age: {pop_stats['avg_age']:.2f}")
        print(f"Max Age: {pop_stats['max_age']}")
        print(f"Generation Distribution:")
        for gen, count in sorted(pop_stats['by_generation'].items()):
            print(f"  Generation {gen}: {count} agents")
        
        # Wealth distribution
        print("\n--- WEALTH DISTRIBUTION ---")
        wealth_stats = self.get_wealth_distribution()
        print(f"Total Wealth: {wealth_stats['total']:.2f}")
        print(f"Average Wealth: {wealth_stats['average']:.2f}")
        print(f"Median Wealth: {wealth_stats['median']:.2f}")
        print(f"Wealth Range: {wealth_stats['min']:.2f} - {wealth_stats['max']:.2f}")
        print(f"Gini Coefficient: {wealth_stats['gini_coefficient']:.3f} (0=equal, 1=unequal)")
        
        # Economic health
        print("\n--- ECONOMIC HEALTH ---")
        econ_health = self.get_economic_health()
        print(f"Total Transaction Volume: {econ_health['transaction_volume']:.2f}")
        print(f"Total Transactions: {econ_health['total_transactions']}")
        print(f"Recent Births (last 10 steps): {econ_health['recent_births']}")
        print(f"Recent Deaths (last 10 steps): {econ_health['recent_deaths']}")
        print(f"Reproduction Rate: {econ_health['reproduction_rate']:.2f} per step")
        print(f"Death Rate: {econ_health['death_rate']:.2f} per step")
        
        # Generational analysis
        print("\n--- GENERATIONAL ANALYSIS ---")
        gen_analysis = self.get_generational_analysis()
        for gen in sorted(gen_analysis.keys()):
            stats = gen_analysis[gen]
            print(f"Generation {gen}: {stats['count']} agents, "
                  f"Avg Wealth={stats['avg_wealth']:.2f}, "
                  f"Avg Fitness={stats['avg_fitness']:.2f}")
        
        print("\n" + "="*60 + "\n")
