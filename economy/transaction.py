"""
Transaction Logging
===================

This module implements transaction tracking for the economic system.
All economic activity is logged for analysis and auditing.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime
import json
import csv


@dataclass
class Transaction:
    """
    Represents a single economic transaction.
    
    Attributes:
        transaction_id: Unique identifier for the transaction
        timestamp: When the transaction occurred (simulation step)
        transaction_type: Type of transaction (work, trade, tithe, reproduction)
        agent_id: Primary agent involved
        counterparty_id: Other agent involved (if applicable)
        amount: Amount of wealth transferred
        details: Additional transaction details
    """
    transaction_id: str
    timestamp: int
    transaction_type: str
    agent_id: str
    counterparty_id: Optional[str]
    amount: float
    details: Optional[dict] = None
    
    def to_dict(self) -> dict:
        """Convert transaction to dictionary."""
        return {
            'transaction_id': self.transaction_id,
            'timestamp': self.timestamp,
            'transaction_type': self.transaction_type,
            'agent_id': self.agent_id,
            'counterparty_id': self.counterparty_id,
            'amount': self.amount,
            'details': self.details
        }
    
    def to_json(self) -> str:
        """Convert transaction to JSON string."""
        return json.dumps(self.to_dict())


class TransactionLedger:
    """
    Maintains a complete ledger of all transactions in the economy.
    """
    
    def __init__(self):
        """Initialize an empty ledger."""
        self.transactions: List[Transaction] = []
        self._next_id = 1
    
    def log_transaction(
        self,
        timestamp: int,
        transaction_type: str,
        agent_id: str,
        counterparty_id: Optional[str],
        amount: float,
        details: Optional[dict] = None
    ) -> Transaction:
        """
        Log a new transaction.
        
        Args:
            timestamp: Current simulation step
            transaction_type: Type (work, trade, tithe, reproduction)
            agent_id: Primary agent
            counterparty_id: Other agent (optional)
            amount: Wealth amount
            details: Additional details
            
        Returns:
            Created transaction
        """
        transaction = Transaction(
            transaction_id=f"TXN-{self._next_id:08d}",
            timestamp=timestamp,
            transaction_type=transaction_type,
            agent_id=agent_id,
            counterparty_id=counterparty_id,
            amount=amount,
            details=details
        )
        self.transactions.append(transaction)
        self._next_id += 1
        return transaction
    
    def get_transactions_by_agent(self, agent_id: str) -> List[Transaction]:
        """Get all transactions involving a specific agent."""
        return [
            txn for txn in self.transactions
            if txn.agent_id == agent_id or txn.counterparty_id == agent_id
        ]
    
    def get_transactions_by_type(self, transaction_type: str) -> List[Transaction]:
        """Get all transactions of a specific type."""
        return [
            txn for txn in self.transactions
            if txn.transaction_type == transaction_type
        ]
    
    def get_transactions_in_range(self, start: int, end: int) -> List[Transaction]:
        """Get transactions within a time range."""
        return [
            txn for txn in self.transactions
            if start <= txn.timestamp <= end
        ]
    
    def get_total_volume(self) -> float:
        """Calculate total transaction volume."""
        return sum(txn.amount for txn in self.transactions)
    
    def export_to_csv(self, filename: str) -> None:
        """
        Export ledger to CSV file.
        
        Args:
            filename: Path to output CSV file
        """
        with open(filename, 'w', newline='') as f:
            if not self.transactions:
                return
            
            fieldnames = ['transaction_id', 'timestamp', 'transaction_type', 
                         'agent_id', 'counterparty_id', 'amount', 'details']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for txn in self.transactions:
                row = txn.to_dict()
                row['details'] = json.dumps(row['details']) if row['details'] else ''
                writer.writerow(row)
    
    def export_to_json(self, filename: str) -> None:
        """
        Export ledger to JSON file.
        
        Args:
            filename: Path to output JSON file
        """
        with open(filename, 'w') as f:
            data = [txn.to_dict() for txn in self.transactions]
            json.dump(data, f, indent=2)
    
    def get_statistics(self) -> dict:
        """
        Get summary statistics about transactions.
        
        Returns:
            Dictionary of statistics
        """
        if not self.transactions:
            return {
                'total_transactions': 0,
                'total_volume': 0,
                'by_type': {}
            }
        
        by_type = {}
        for txn in self.transactions:
            if txn.transaction_type not in by_type:
                by_type[txn.transaction_type] = {'count': 0, 'volume': 0}
            by_type[txn.transaction_type]['count'] += 1
            by_type[txn.transaction_type]['volume'] += txn.amount
        
        return {
            'total_transactions': len(self.transactions),
            'total_volume': self.get_total_volume(),
            'by_type': by_type
        }
