#!/usr/bin/env python3
"""
Evolutionary AI Economic Ecosystem - Main Entry Point
======================================================

This is the main command-line interface for running simulations of the
Evolutionary AI Economic Ecosystem.
"""

import argparse
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from simulation.engine import SimulationEngine
from dashboard.metrics import Metrics
from infra.config import Config, get_default_config, create_scenario_config, setup_logging, validate_config, ensure_directory, get_timestamp


def run_simulation_cli(args):
    """Run simulation based on command-line arguments."""
    
    # Load or create configuration
    if args.config:
        print(f"Loading configuration from {args.config}")
        config = Config.load_from_file(args.config)
    elif args.scenario:
        print(f"Using scenario: {args.scenario}")
        config = create_scenario_config(args.scenario)
    else:
        print("Using default configuration")
        config = Config()
    
    # Override with command-line arguments
    if args.population:
        config.set('initial_population', args.population)
    if args.steps:
        config.set('simulation_steps', args.steps)
    if args.seed is not None:
        config.set('random_seed', args.seed)
    
    # Set up output directory
    output_dir = args.output or config.get('output_dir', './output')
    ensure_directory(output_dir)
    config.set('output_dir', output_dir)
    
    # Set up logging
    if args.verbose:
        config.set('log_level', 'DEBUG')
    setup_logging(config)
    
    # Validate configuration
    try:
        validate_config(config)
    except ValueError as e:
        print(f"Configuration error: {e}")
        return 1
    
    # Set random seed if specified
    if config.get('random_seed') is not None:
        import random
        random.seed(config.get('random_seed'))
        print(f"Random seed set to: {config.get('random_seed')}")
    
    # Create simulation engine
    print("\nInitializing simulation engine...")
    engine = SimulationEngine(config.to_dict())
    
    # Initialize population
    initial_pop = config.get('initial_population', 20)
    print(f"Creating initial population of {initial_pop} agents...")
    engine.initialize_population(initial_pop)
    
    # Create metrics dashboard
    metrics = Metrics(engine)
    
    # Show initial state
    if args.verbose or args.dashboard:
        print("\n--- Initial State ---")
        metrics.display_dashboard()
    
    # Run simulation
    steps = config.get('simulation_steps', 100)
    print(f"\nRunning simulation for {steps} steps...")
    print("(This may take a moment...)\n")
    
    engine.run(steps, verbose=args.verbose)
    
    # Show final state
    print("\n--- Simulation Complete ---")
    metrics.display_dashboard()
    
    # Export results
    timestamp = get_timestamp()
    transactions_file = os.path.join(output_dir, f"transactions_{timestamp}.csv")
    stats_file = os.path.join(output_dir, f"stats_{timestamp}.json")
    metrics_file = os.path.join(output_dir, f"metrics_{timestamp}.csv")
    
    print(f"\nExporting results to {output_dir}...")
    engine.export_results(transactions_file, stats_file)
    metrics.export_to_csv(metrics_file)
    
    print(f"  - Transactions: {transactions_file}")
    print(f"  - Statistics: {stats_file}")
    print(f"  - Metrics: {metrics_file}")
    
    # Save final configuration
    if args.save_config:
        config_file = os.path.join(output_dir, f"config_{timestamp}.json")
        config.save_to_file(config_file)
        print(f"  - Configuration: {config_file}")
    
    print("\nSimulation complete!")
    return 0


def show_scenarios():
    """Display available pre-configured scenarios."""
    print("\nAvailable Scenarios:")
    print("=" * 60)
    
    print("\ndefault:")
    print("  Balanced starting conditions")
    print("  - 20 agents, 100 wealth each")
    print("  - 10% tithe rate, 50 cost to reproduce")
    
    print("\nrapid_growth:")
    print("  Optimized for fast population growth")
    print("  - 10 agents, 150 wealth each")
    print("  - 5% tithe rate, 30 cost to reproduce")
    print("  - Higher rewards, more mutation")
    
    print("\nhigh_competition:")
    print("  Scarce resources, intense selection pressure")
    print("  - 50 agents, 80 wealth each")
    print("  - 15% tithe rate, 80 cost to reproduce")
    print("  - Lower rewards, population cap of 100")
    
    print("\nstable:")
    print("  Long-term equilibrium conditions")
    print("  - 30 agents, 100 wealth each")
    print("  - 10% tithe rate, moderate rewards")
    print("  - Balanced parameters for stability")
    
    print("\n" + "=" * 60)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Evolutionary AI Economic Ecosystem Simulation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default settings
  python main.py
  
  # Run a specific scenario
  python main.py --scenario rapid_growth
  
  # Run with custom parameters
  python main.py --population 50 --steps 200 --seed 42
  
  # Load configuration from file
  python main.py --config my_config.json
  
  # Show available scenarios
  python main.py --list-scenarios
        """
    )
    
    parser.add_argument(
        '--config', '-c',
        help='Path to configuration JSON file'
    )
    
    parser.add_argument(
        '--scenario', '-s',
        choices=['default', 'rapid_growth', 'high_competition', 'stable'],
        help='Pre-configured scenario to run'
    )
    
    parser.add_argument(
        '--population', '-p',
        type=int,
        help='Initial population size'
    )
    
    parser.add_argument(
        '--steps', '-n',
        type=int,
        help='Number of simulation steps'
    )
    
    parser.add_argument(
        '--seed',
        type=int,
        help='Random seed for reproducibility'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Output directory for results'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output during simulation'
    )
    
    parser.add_argument(
        '--dashboard', '-d',
        action='store_true',
        help='Show dashboard before and after simulation'
    )
    
    parser.add_argument(
        '--save-config',
        action='store_true',
        help='Save configuration to output directory'
    )
    
    parser.add_argument(
        '--list-scenarios',
        action='store_true',
        help='List available scenarios and exit'
    )
    
    args = parser.parse_args()
    
    # Handle special commands
    if args.list_scenarios:
        show_scenarios()
        return 0
    
    # Run simulation
    return run_simulation_cli(args)


if __name__ == '__main__':
    sys.exit(main())
