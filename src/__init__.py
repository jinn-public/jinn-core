"""
Jinn-Core Economic Simulation Engine

A flexible framework for running economic models and analyzing policy scenarios.
"""

from .engine import SimulationEngine
from .models import (
    InterestRateModel, 
    InterestRateShock,
    InflationShockModel,
    InflationShock,
    simulate_inflation_shock,
    BankPanicModel,
    BankPanicShock,
    simulate_bank_panic
)

__version__ = "0.1.0"
__author__ = "Economic Research Team"
__email__ = "research@jinncore.org"

__all__ = [
    "SimulationEngine",
    "InterestRateModel", 
    "InterestRateShock",
    "InflationShockModel",
    "InflationShock",
    "simulate_inflation_shock",
    "BankPanicModel",
    "BankPanicShock",
    "simulate_bank_panic"
] 