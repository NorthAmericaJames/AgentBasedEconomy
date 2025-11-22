"""
Configuration Management
========================

This module provides configuration management for the simulation,
including default parameters and utility functions.
"""

from __future__ import annotations
from typing import Dict, Any, Optional
import json
import logging


class Config:
    """
    Configuration container for simulation parameters.
    """
    
    def __init__(self, config_dict: Optional[Dict[str, Any]] = None):
        """
        Initialize configuration.
        
        Args:
            config_dict: Dictionary of configuration parameters
        """
        # Load defaults
        defaults = get_default_config()
        
        # Override with provided config
        if config_dict:
            defaults.update(config_dict)
        
        # Store configuration
        self._config = defaults
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        self._config[key] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """Return configuration as dictionary."""
        return self._config.copy()
    
    def save_to_file(self, filename: str) -> None:
        """
        Save configuration to JSON file.
        
        Args:
            filename: Path to output file
        """
        with open(filename, 'w') as f:
            json.dump(self._config, f, indent=2)
    
    @classmethod
    def load_from_file(cls, filename: str) -> 'Config':
        """
        Load configuration from JSON file.
        
        Args:
            filename: Path to config file
            
        Returns:
            Config instance
        """
        with open(filename, 'r') as f:
            config_dict = json.load(f)
        return cls(config_dict)


def get_default_config() -> Dict[str, Any]:
    """
    Get default configuration parameters.
    
    Returns:
        Dictionary of default parameters
    """
    return {
        # Population parameters
        'initial_population': 20,
        'max_population': 1000,
        
        # Economic parameters
        'starting_wealth': 100.0,
        'job_reward_range': (5.0, 20.0),
        'tithe_rate': 0.1,  # 10% to parent
        
        # Evolution parameters
        'reproduction_cost': 50.0,
        'mutation_rate': 0.1,
        
        # Agent lifecycle parameters
        'energy_recovery': 5.0,
        'min_reproduction_age': 10,
        'min_reproduction_energy': 50.0,
        
        # Simulation parameters
        'simulation_steps': 100,
        'random_seed': None,  # None for random, or integer for reproducibility
        
        # DNA default ranges
        'dna_defaults': {
            'risk_tolerance': (0.3, 0.7),
            'efficiency': (0.5, 1.0),
            'innovation_rate': (0.1, 0.5)
        },
        
        # Logging
        'log_level': 'INFO',
        'log_file': None,  # None for no file logging
        
        # Output
        'output_dir': './output',
        'save_interval': 10,  # Save stats every N steps
    }


def setup_logging(config: Config) -> None:
    """
    Set up logging based on configuration.
    
    Args:
        config: Configuration object
    """
    log_level = config.get('log_level', 'INFO')
    log_file = config.get('log_file')
    
    # Convert string to logging level
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Configure logging
    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers
    )


def validate_config(config: Config) -> bool:
    """
    Validate configuration parameters.
    
    Args:
        config: Configuration to validate
        
    Returns:
        True if valid, raises ValueError if invalid
    """
    c = config.to_dict()
    
    # Check positive values
    if c.get('initial_population', 0) <= 0:
        raise ValueError("initial_population must be positive")
    
    if c.get('starting_wealth', 0) <= 0:
        raise ValueError("starting_wealth must be positive")
    
    if c.get('reproduction_cost', 0) <= 0:
        raise ValueError("reproduction_cost must be positive")
    
    # Check rates are in [0, 1]
    if not (0 <= c.get('mutation_rate', 0) <= 1):
        raise ValueError("mutation_rate must be between 0 and 1")
    
    if not (0 <= c.get('tithe_rate', 0) <= 1):
        raise ValueError("tithe_rate must be between 0 and 1")
    
    # Check population limits
    if c.get('max_population', 0) < c.get('initial_population', 0):
        raise ValueError("max_population must be >= initial_population")
    
    return True


def create_scenario_config(scenario: str) -> Config:
    """
    Create a pre-configured scenario.
    
    Args:
        scenario: Scenario name ('default', 'rapid_growth', 'high_competition', 'stable')
        
    Returns:
        Config object for the scenario
    """
    if scenario == 'default':
        return Config()
    
    elif scenario == 'rapid_growth':
        return Config({
            'initial_population': 10,
            'starting_wealth': 150.0,
            'reproduction_cost': 30.0,
            'tithe_rate': 0.05,
            'mutation_rate': 0.15,
            'job_reward_range': (10.0, 30.0)
        })
    
    elif scenario == 'high_competition':
        return Config({
            'initial_population': 50,
            'starting_wealth': 80.0,
            'reproduction_cost': 80.0,
            'tithe_rate': 0.15,
            'mutation_rate': 0.05,
            'job_reward_range': (3.0, 15.0),
            'max_population': 100
        })
    
    elif scenario == 'stable':
        return Config({
            'initial_population': 30,
            'starting_wealth': 100.0,
            'reproduction_cost': 50.0,
            'tithe_rate': 0.1,
            'mutation_rate': 0.08,
            'job_reward_range': (8.0, 18.0),
            'energy_recovery': 7.0
        })
    
    else:
        raise ValueError(f"Unknown scenario: {scenario}")


# Utility functions

def ensure_directory(path: str) -> None:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        path: Directory path
    """
    import os
    os.makedirs(path, exist_ok=True)


def get_timestamp() -> str:
    """
    Get current timestamp as string.
    
    Returns:
        Formatted timestamp
    """
    from datetime import datetime
    return datetime.now().strftime("%Y%m%d_%H%M%S")
