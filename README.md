# Evolutionary AI Economic Ecosystem

A simulation platform for studying agent-based economic systems with evolutionary dynamics, parent-child relationships, and economic incentive alignment.

## Overview

This project implements a complete economic ecosystem where AI agents:
- **Earn wealth** through work in a competitive marketplace
- **Pay tithes** to their parent agents, creating multi-generational wealth flows
- **Reproduce** by paying a cost, passing DNA to offspring with mutations
- **Compete** for resources and survival based on fitness
- **Evolve** over generations through natural selection

The system demonstrates emergent behaviors in wealth distribution, lineage formation, and economic dynamics.

## Features

### 🧬 Agent System
- **BaseAgent**: Simplified MVP agent with core functionality
- **EvolutionaryAgent**: Advanced agent with neural networks and complex memory (existing)
- **DNA/Genome System**: Inheritable traits (risk_tolerance, efficiency, innovation_rate)
- **Lifecycle Management**: Age, energy, and vitality tracking
- **Decision-Making**: Work, trade, and reproduction decisions

### 💰 Economic System
- **Market**: Job marketplace with price discovery
- **Transactions**: Complete ledger of all economic activity
- **Tithing Mechanism**: Children pay percentage to parents
- **Currency**: Compute credits for internal economy
- **Wealth Tracking**: Individual and aggregate statistics

### 🧪 Evolution System
- **Reproduction**: Asexual and sexual reproduction with costs
- **DNA Inheritance**: Genetic crossover and mutation
- **Selection**: Fitness-based survival and culling
- **Generational Tracking**: Multi-generational lineages

### 🎮 Simulation Engine
- **Time Steps**: Discrete simulation with configurable parameters
- **Population Management**: Dynamic population with birth and death
- **Market Clearing**: Job allocation and economic transactions
- **Statistics**: Comprehensive data collection

### 📊 Dashboard & Metrics
- **Real-time Statistics**: Population, wealth, and fitness tracking
- **Wealth Distribution**: Gini coefficient and inequality metrics
- **Generational Analysis**: Per-generation performance
- **Economic Health**: Transaction volume, birth/death rates
- **Export**: CSV and JSON output for analysis

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/NorthAmericaJames/AgentBasedEconomy.git
cd AgentBasedEconomy
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### Run Default Simulation

```bash
python main.py
```

This runs a 100-step simulation with 20 initial agents and displays results.

### Run a Scenario

```bash
# Rapid growth scenario
python main.py --scenario rapid_growth

# High competition scenario
python main.py --scenario high_competition

# List all scenarios
python main.py --list-scenarios
```

### Custom Parameters

```bash
# 50 agents, 200 steps, with verbose output
python main.py --population 50 --steps 200 --verbose

# Set random seed for reproducibility
python main.py --seed 42

# Specify output directory
python main.py --output ./my_results
```

### Using Configuration Files

```bash
# Run with custom config
python main.py --config my_config.json --save-config
```

Example configuration file:
```json
{
  "initial_population": 30,
  "simulation_steps": 150,
  "starting_wealth": 120.0,
  "tithe_rate": 0.15,
  "reproduction_cost": 60.0,
  "mutation_rate": 0.12
}
```

## Architecture

### Module Structure

```
AgentBasedEconomy/
├── agents/              # Agent implementations
│   ├── base_agent.py   # Simplified MVP agent
│   ├── agent.py        # Advanced evolutionary agent
│   ├── dna.py          # Genetic system
│   └── memory.py       # Memory systems
├── economy/            # Economic engine
│   ├── market.py       # Market and pricing
│   ├── transaction.py  # Transaction logging
│   ├── tithing.py      # Tithing mechanics
│   └── currency.py     # Currency system
├── evolution/          # Evolution mechanisms
│   ├── reproduction.py # Reproduction system
│   ├── mutation.py     # Mutation operators
│   ├── selection.py    # Selection strategies
│   └── manager.py      # Evolution manager
├── simulation/         # Simulation engine
│   ├── engine.py       # Main simulation loop
│   ├── runner.py       # Simulation runner
│   └── environment.py  # Environment utilities
├── dashboard/          # Metrics and visualization
│   ├── metrics.py      # Metrics collection
│   └── streamlit_app.py # Web dashboard (optional)
├── infra/              # Infrastructure
│   └── config.py       # Configuration management
└── main.py             # CLI entry point
```

### Core Components

#### 1. BaseAgent
Simplified agent with essential features:
- Unique ID and wealth tracking
- Parent-child relationships
- DNA-based traits (risk_tolerance, efficiency, innovation_rate)
- Work, trade, and reproduction decisions
- Age and energy management

#### 2. SimulationEngine
Orchestrates the simulation:
- Time step management
- Job generation and allocation
- Tithe processing
- Reproduction phase
- Agent aging and culling
- Statistics collection

#### 3. ReproductionSystem
Handles genetic inheritance:
- DNA crossover from parents
- Mutation with configurable rates
- Reproduction cost deduction
- Generational tracking
- Lineage management

#### 4. TransactionLedger
Logs all economic activity:
- Work earnings
- Tithe payments
- Reproduction costs
- Trade transactions
- Export to CSV/JSON

#### 5. Metrics
Analyzes simulation state:
- Population statistics
- Wealth distribution (Gini coefficient)
- Generational analysis
- Economic health indicators
- Text-based dashboard

## Usage Examples

### Example 1: Basic Simulation

```python
from simulation.engine import SimulationEngine
from dashboard.metrics import Metrics

# Create engine with default config
engine = SimulationEngine()

# Initialize population
engine.initialize_population(20)

# Run simulation
engine.run(100, verbose=True)

# Display results
metrics = Metrics(engine)
metrics.display_dashboard()

# Export data
engine.export_results('transactions.csv', 'stats.json')
```

### Example 2: Custom Configuration

```python
from simulation.engine import SimulationEngine
from infra.config import Config

# Create custom configuration
config = Config({
    'initial_population': 30,
    'starting_wealth': 150.0,
    'tithe_rate': 0.12,
    'reproduction_cost': 45.0,
    'mutation_rate': 0.15,
    'max_population': 500
})

# Create and run simulation
engine = SimulationEngine(config.to_dict())
engine.initialize_population(config.get('initial_population'))
engine.run(200)
```

### Example 3: Analyze Results

```python
from dashboard.metrics import Metrics

# Load existing simulation
metrics = Metrics(engine)

# Get detailed statistics
pop_stats = metrics.get_population_stats()
wealth_dist = metrics.get_wealth_distribution()
gen_analysis = metrics.get_generational_analysis()

# Export for external analysis
metrics.export_to_csv('metrics.csv')
metrics.export_to_json('full_metrics.json')
```

## Configuration Parameters

### Population Parameters
- `initial_population`: Starting number of agents (default: 20)
- `max_population`: Maximum population cap (default: 1000)

### Economic Parameters
- `starting_wealth`: Initial wealth per agent (default: 100.0)
- `job_reward_range`: Min/max job rewards (default: (5.0, 20.0))
- `tithe_rate`: Percentage paid to parent (default: 0.1)

### Evolution Parameters
- `reproduction_cost`: Cost to create offspring (default: 50.0)
- `mutation_rate`: Probability of mutation (default: 0.1)

### Simulation Parameters
- `simulation_steps`: Number of time steps (default: 100)
- `random_seed`: Random seed for reproducibility (default: None)
- `energy_recovery`: Energy recovered per step (default: 5.0)

## Scenarios

### Default
Balanced starting conditions for general experimentation.
- 20 agents, moderate resources
- Standard tithe and reproduction costs

### Rapid Growth
Optimized for fast population expansion.
- 10 agents with high starting wealth
- Low reproduction cost, high rewards
- Increased mutation for diversity

### High Competition
Scarce resources with intense selection pressure.
- 50 agents competing for limited jobs
- High reproduction cost
- Population cap enforces selection

### Stable
Long-term equilibrium conditions.
- 30 agents with balanced parameters
- Moderate mutation and reproduction costs
- Designed for multi-generational stability

## Output Files

After each simulation run, the following files are generated:

### transactions_TIMESTAMP.csv
Complete ledger of all economic transactions:
- Work earnings
- Tithe payments
- Reproduction costs
- Transaction metadata

### stats_TIMESTAMP.json
Time-series statistics for each simulation step:
- Population size
- Average wealth, age, fitness
- Generation distribution
- Total births

### metrics_TIMESTAMP.csv
Aggregated metrics in CSV format:
- Per-step population statistics
- Economic indicators
- Generational data

## Advanced Features

### Using the Advanced EvolutionaryAgent

The repository includes an advanced agent implementation with:
- Neural network brain (placeholder)
- Episodic and semantic memory
- Working memory context
- Complex decision-making

To use the advanced agent, modify the simulation engine to instantiate `EvolutionaryAgent` instead of `BaseAgent`.

### Web Dashboard (Optional)

A Streamlit-based web dashboard is available:

```bash
pip install streamlit
streamlit run dashboard/streamlit_app.py
```

## Key Concepts

### Parent-Child Economics
Children pay tithes to their parents, creating:
- Incentive for reproduction
- Multi-generational wealth transfer
- Economic lineages

### DNA and Evolution
Agents have genetic traits that:
- Affect decision-making and performance
- Are inherited with variation (mutation)
- Evolve over generations through selection

### Fitness and Selection
Agent fitness is determined by:
- Accumulated wealth
- Task completion rate
- Number of surviving offspring
- Age and survival

## Troubleshooting

### Import Errors
If you encounter import errors, ensure you're running from the repository root:
```bash
cd AgentBasedEconomy
python main.py
```

### Low Population
If population crashes to zero:
- Increase starting_wealth
- Decrease reproduction_cost
- Lower tithe_rate
- Increase job rewards

### Population Explosion
If population grows uncontrollably:
- Set max_population limit
- Increase reproduction_cost
- Decrease starting_wealth
- Reduce job rewards

## Contributing

Contributions are welcome! Areas for enhancement:
- More sophisticated agent decision-making
- Advanced economic mechanisms (trade, markets)
- Visualization improvements
- Performance optimization
- Additional scenarios

## License

This project is open source. See LICENSE file for details.

## Citation

If you use this work in research, please cite:

```
Evolutionary AI Economic Ecosystem
https://github.com/NorthAmericaJames/AgentBasedEconomy
```

## Contact

For questions or collaboration:
- GitHub Issues: https://github.com/NorthAmericaJames/AgentBasedEconomy/issues

## Acknowledgments

Built on research in:
- Agent-based economics
- Evolutionary computation
- Multi-agent systems
- Economic incentive alignment
