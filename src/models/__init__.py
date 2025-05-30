"""
Economic Models Package

This package contains various economic models for simulation.
"""

from .interest_rate import InterestRateModel, InterestRateShock
from .inflation_shock import InflationShockModel, InflationShock, simulate_inflation_shock
from .bank_panic import BankPanicModel, BankPanicShock, simulate_bank_panic
from .military_spending_shock import MilitarySpendingShockModel, MilitarySpendingShock, simulate_military_spending_shock
from .global_conflict import GlobalConflictModel, GlobalConflictShock, simulate_global_conflict
from .earth_rotation_shock import EarthRotationShockModel, EarthRotationShock, simulate_earth_rotation_shock
from .btc_price_projection import BTCPriceProjectionModel, BTCProjectionScenario, simulate_btc_price_projection
from .cosmic_consciousness_timing import (
    CosmicConsciousnessTimingModel, 
    CosmicTimingScenario, 
    simulate_cosmic_consciousness_timing,
    KARDASHEV_SCALE,
    estimate_kardashev_progress,
    get_kardashev_expansion_multiplier,
    get_kardashev_survival_bonus,
    get_kardashev_level_name
)
from .ai_unemployment_shock import AIUnemploymentShockModel, AIUnemploymentShock, simulate_ai_unemployment_shock
from .plastic_spread_simulation import PlasticSpreadSimulationModel, PlasticSpreadShock, simulate_plastic_spread
from .geopolitical_land_analyst import (
    GeopoliticalLandAnalyst, 
    RegionProfile, 
    GeopoliticalShock, 
    simulate_land_price_trends,
    RegionType,
    ClimatePressure
)

__all__ = [
    'InterestRateModel', 
    'InterestRateShock',
    'InflationShockModel',
    'InflationShock',
    'simulate_inflation_shock',
    'BankPanicModel',
    'BankPanicShock',
    'simulate_bank_panic',
    'MilitarySpendingShockModel',
    'MilitarySpendingShock',
    'simulate_military_spending_shock',
    'GlobalConflictModel',
    'GlobalConflictShock',
    'simulate_global_conflict',
    'EarthRotationShockModel',
    'EarthRotationShock',
    'simulate_earth_rotation_shock',
    'BTCPriceProjectionModel',
    'BTCProjectionScenario',
    'simulate_btc_price_projection',
    'CosmicConsciousnessTimingModel',
    'CosmicTimingScenario',
    'simulate_cosmic_consciousness_timing',
    'KARDASHEV_SCALE',
    'estimate_kardashev_progress',
    'get_kardashev_expansion_multiplier',
    'get_kardashev_survival_bonus',
    'get_kardashev_level_name',
    'AIUnemploymentShockModel',
    'AIUnemploymentShock',
    'simulate_ai_unemployment_shock',
    'PlasticSpreadSimulationModel',
    'PlasticSpreadShock',
    'simulate_plastic_spread',
    'GeopoliticalLandAnalyst',
    'RegionProfile',
    'GeopoliticalShock',
    'simulate_land_price_trends',
    'RegionType',
    'ClimatePressure'
] 