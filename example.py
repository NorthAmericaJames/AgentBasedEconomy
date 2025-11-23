#!/usr/bin/env python3
"""
Example: Quick Start with the Evolutionary AI Economic Ecosystem
==================================================================

This script demonstrates the basic usage of the simulation system.
"""

from simulation.engine import SimulationEngine
from dashboard.metrics import Metrics
from infra.config import Config

def main():
    print("=" * 60)
    print("EVOLUTIONARY AI ECONOMIC ECOSYSTEM - QUICK START EXAMPLE")
    print("=" * 60)
    
    # Create a custom configuration
    print("\n1. Setting up configuration...")
    config = Config({
        'initial_population': 15,
        'simulation_steps': 50,
        'starting_wealth': 120.0,
        'tithe_rate': 0.12,
        'reproduction_cost': 40.0,
        'mutation_rate': 0.15,
        'random_seed': 123  # For reproducibility
    })
    print(f"   Initial population: {config.get('initial_population')}")
    print(f"   Simulation steps: {config.get('simulation_steps')}")
    print(f"   Starting wealth: {config.get('starting_wealth')}")
    
    # Create simulation engine
    print("\n2. Initializing simulation engine...")
    engine = SimulationEngine(config.to_dict())
    
    # Initialize population
    print(f"\n3. Creating {config.get('initial_population')} agents...")
    engine.initialize_population(config.get('initial_population'))
    
    # Create metrics
    metrics = Metrics(engine)
    
    # Show initial state
    print("\n4. Initial state:")
    initial_stats = metrics.get_population_stats()
    print(f"   Population: {initial_stats['total']}")
    print(f"   Average age: {initial_stats['avg_age']:.1f}")
    
    # Run simulation
    print(f"\n5. Running simulation for {config.get('simulation_steps')} steps...")
    engine.run(config.get('simulation_steps'))
    
    # Show final results
    print("\n6. Final results:")
    metrics.display_dashboard()
    
    # Export results
    print("\n7. Exporting results...")
    engine.export_results('example_transactions.csv', 'example_stats.json')
    metrics.export_to_csv('example_metrics.csv')
    print("   Files created:")
    print("   - example_transactions.csv")
    print("   - example_stats.json")
    print("   - example_metrics.csv")
    
    # Show some interesting insights
    print("\n8. Key insights:")
    wealth_dist = metrics.get_wealth_distribution()
    gen_analysis = metrics.get_generational_analysis()
    
    print(f"   Total wealth in system: {wealth_dist['total']:.2f}")
    print(f"   Wealth inequality (Gini): {wealth_dist['gini_coefficient']:.3f}")
    print(f"   Number of generations: {len(gen_analysis)}")
    print(f"   Total births: {engine.reproduction_system.total_births}")
    
    if len(gen_analysis) > 1:
        print("\n   Generational comparison:")
        for gen in sorted(gen_analysis.keys())[:3]:  # Show first 3 generations
            stats = gen_analysis[gen]
            print(f"     Gen {gen}: {stats['count']} agents, "
                  f"avg wealth={stats['avg_wealth']:.2f}")
    
    print("\n" + "=" * 60)
    print("EXAMPLE COMPLETE!")
    print("=" * 60)

if __name__ == '__main__':
    main()
