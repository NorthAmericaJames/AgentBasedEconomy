"""
Mutation Operators
==================

This module defines mutation operators used during reproduction.  It wraps
the mutation logic on `AgentDNA`, exposing utilities for customizing
mutation rates or applying domain‑specific mutations【151713287013870†screenshot】.
"""

from __future__ import annotations

from typing import Optional

from agents.dna import AgentDNA


def mutate_dna(dna: AgentDNA, rate: Optional[float] = None) -> AgentDNA:
    """Return a mutated copy of the given DNA."""
    return dna.mutate(rate)
