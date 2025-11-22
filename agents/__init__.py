"""
Agents Module
=============

This module contains agent implementations for the Evolutionary AI Economic Ecosystem.
It includes both the advanced EvolutionaryAgent class and the simplified BaseAgent class for MVP.
"""

from .base_agent import BaseAgent
from .agent import EvolutionaryAgent
from .dna import AgentDNA

__all__ = ['BaseAgent', 'EvolutionaryAgent', 'AgentDNA']
