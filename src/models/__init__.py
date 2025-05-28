"""
Economic Models Package

This package contains various economic models for simulation.
"""

from .interest_rate import InterestRateModel, InterestRateShock
from .inflation_shock import InflationShockModel, InflationShock, simulate_inflation_shock

__all__ = [
    'InterestRateModel', 
    'InterestRateShock',
    'InflationShockModel',
    'InflationShock',
    'simulate_inflation_shock'
] 