"""
Currency Definitions
====================

Agents transact using two forms of currency:

* **Compute Credits (CC)** – Units of computational power used to pay for
  resource usage and reproduction costs.  CCs are minted by the economic
  engine when tasks are completed and can be spent to execute tasks【151713287013870†screenshot】.
* **Value Tokens (VT)** – Externally facing tokens representing value to
  clients.  VT payments are converted to CC at the exchange rate.  The
  separation of VT and CC mirrors real‑world fiat vs. internal energy
  economy【151713287013870†screenshot】.

This module simply defines constants and helper functions for dealing with
currency conversions.  Exchange rates may be dynamic in future versions.
"""

EXCHANGE_RATE = 1.0  # 1 VT == 1 CC by default


def vt_to_cc(value_tokens: float) -> float:
    """Convert value tokens to compute credits."""
    return value_tokens * EXCHANGE_RATE


def cc_to_vt(compute_credits: float) -> float:
    """Convert compute credits to value tokens."""
    return compute_credits / EXCHANGE_RATE
