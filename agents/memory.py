"""
Memory Systems for Evolutionary Agents
======================================

Agents employ several memory subsystems to store experiences, conceptual
knowledge, and working context.  These memory mechanisms are inspired by
cognitive neuroscience and are critical for enabling agents to learn from
their history, reason about abstract relationships, and maintain context
during task execution【151713287013870†screenshot】.

This module provides simple placeholder implementations of these memory
systems.  Downstream contributors should extend these classes to
incorporate more sophisticated storage and retrieval strategies, such as
vector databases, knowledge graphs, or episodic replay buffers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


class EpisodicMemory:
    """A cyclic buffer for storing recent experiences (task, action, outcome)."""

    def __init__(self, capacity: int = 512) -> None:
        self.capacity = capacity
        self.buffer: List[Tuple[Any, Any, Any]] = []

    def store(self, task: Any, action: Any, outcome: Any) -> None:
        """Store an episode consisting of the task, the action taken, and the outcome."""
        if len(self.buffer) >= self.capacity:
            self.buffer.pop(0)
        self.buffer.append((task, action, outcome))

    def update_value(self, task_id: str, reward: float) -> None:
        """Update the stored outcome value for a given task ID.

        In a more sophisticated implementation, this would find episodes
        matching the task ID and adjust their stored reward estimates.
        """
        pass

    def retrieve(self, query: Any) -> List[Tuple[Any, Any, Any]]:
        """Retrieve episodes relevant to a query.

        This placeholder returns all episodes.  Actual retrieval should
        perform similarity search based on query features.
        """
        return self.buffer.copy()


class SemanticKnowledgeGraph:
    """A lightweight container for structured knowledge about the world.

    This placeholder uses a dictionary of subject→predicate→object triples.
    """

    def __init__(self) -> None:
        self.graph: Dict[str, Dict[str, Any]] = {}

    def add_fact(self, subject: str, predicate: str, obj: Any) -> None:
        self.graph.setdefault(subject, {})[predicate] = obj

    def query(self, subject: str, predicate: Optional[str] = None) -> Any:
        if predicate is None:
            return self.graph.get(subject, {})
        return self.graph.get(subject, {}).get(predicate)

    def compress(self, ratio: float = 0.1) -> Dict[str, Dict[str, Any]]:
        """Return a partial copy of the knowledge graph for inheritance.

        To simulate partial knowledge transfer during reproduction, this
        method returns a subset of the stored facts controlled by
        ``ratio``【151713287013870†screenshot】.
        """
        limited = {}
        for i, (subj, preds) in enumerate(self.graph.items()):
            if i / len(self.graph) < ratio:
                limited[subj] = preds.copy()
        return limited

    def load(self, compressed_kg: Dict[str, Dict[str, Any]]) -> None:
        """Merge compressed knowledge into the existing graph."""
        for subj, preds in compressed_kg.items():
            self.graph.setdefault(subj, {}).update(preds)


class WorkingMemory:
    """A finite context window for task execution.

    Working memory holds the current context for an agent's inference.  It
    maintains a sliding window of tokens or data points that the agent
    processes during a task【151713287013870†screenshot】.
    """

    def __init__(self, context_window: int = 512) -> None:
        self.context_window = context_window
        self.contents: List[Any] = []

    def push(self, item: Any) -> None:
        if len(self.contents) >= self.context_window:
            self.contents.pop(0)
        self.contents.append(item)

    def reset(self) -> None:
        self.contents.clear()

    def get_contents(self) -> List[Any]:
        return self.contents.copy()
