"""
Evolution Module
================

This module handles reproduction, mutation, and selection mechanisms for agents.
"""

from .manager import EvolutionManager
from .reproduction import ReproductionSystem
from .mutation import mutate_dna

__all__ = ['EvolutionManager', 'ReproductionSystem', 'mutate_dna']
