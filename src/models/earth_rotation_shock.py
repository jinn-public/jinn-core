"""
Earth Rotation Shock Model

Economic model for simulating the consequences of changes in Earth's rotation speed
on GDP, agriculture, infrastructure, climate, and human adaptation.
"""

import numpy as np
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class EarthRotationShock:
    """Configuration for an Earth rotation speed change scenario."""
    rotation_change_percent: float  # Percentage change in rotation speed (e.g., 10 for 10% faster)
    adaptation_cost_factor: float   # Cost multiplier for adaptation (e.g., 1.5)
    climate_volatility_multiplier: float  # Climate instability multiplier (e.g., 1.2)
    agriculture_loss_rate: float    # Agricultural productivity loss rate (e.g., 0.7)
    infrastructure_disruption_index: float  # Infrastructure stress index (e.g., 0.5)
    start_period: int = 0           # When the rotation change begins


def simulate_earth_rotation_shock(rotation_change_percent: float, initial_gdp: float,
                                gdp_day_night_dependency: float, infrastructure_adaptability: float,
                                agricultural_sensitivity: float, climate_volatility_multiplier: float) -> Dict[str, Any]:
    """
    Simple, interpretable function to simulate the effect of Earth rotation speed change.
    
    Args:
        rotation_change_percent: Percentage change in rotation speed (positive = faster)
        initial_gdp: Initial global GDP (USD)
        gdp_day_night_dependency: How much GDP depends on day/night cycles (0-1)
        infrastructure_adaptability: How well infrastructure can adapt (0-1)
        agricultural_sensitivity: Agricultural sensitivity to day length changes (0-1)
        climate_volatility_multiplier: Climate instability multiplier
        
    Returns:
        Dict containing:
        - new_day_length_hours: New day length in hours
        - initial_gdp_loss: Immediate GDP impact (%)
        - long_term_gdp_loss: Long-term GDP impact (%)
        - adaptation_time_years: Time to adapt (years)
        - sea_level_shift_meters: Estimated sea level shift at equator (meters)
        - climate_volatility_index: Climate instability index
        - labor_productivity_change: Labor productivity change (%)
        - circadian_stress_index: Human circadian disruption index (0-1)
        - sea_wave_intensity_change: Change in ocean wave intensity (%)
        - population_drop_percent: Estimated population decline (%)
    """
    # Calculate new day length
    # If rotation increases by X%, day length decreases by X/(1+X/100)%
    rotation_factor = 1 + (rotation_change_percent / 100)
    new_day_length_hours = 24 / rotation_factor
    day_length_change_percent = (new_day_length_hours - 24) / 24 * 100
    
    # Immediate GDP impact from disruption
    # Based on day/night dependency, infrastructure adaptability, and agricultural sensitivity
    disruption_factor = abs(day_length_change_percent) / 100
    
    # Infrastructure disruption (immediate)
    infrastructure_impact = disruption_factor * (1 - infrastructure_adaptability) * 0.15  # Up to 15% GDP
    
    # Agricultural disruption (immediate and severe)
    agricultural_impact = disruption_factor * agricultural_sensitivity * 0.25  # Up to 25% of ag GDP (5% total)
    
    # Circadian and productivity disruption
    circadian_disruption = min(1.0, disruption_factor * 2)  # Severe for large changes
    productivity_impact = circadian_disruption * gdp_day_night_dependency * 0.1  # Up to 10% GDP
    
    # Time system misalignment costs
    time_system_costs = disruption_factor * 0.05  # 5% GDP for complete overhaul
    
    initial_gdp_loss = (infrastructure_impact + agricultural_impact + 
                       productivity_impact + time_system_costs) * 100
    
    # Long-term adaptation effects
    # Some recovery over time, but permanent changes remain
    adaptation_efficiency = (infrastructure_adaptability + (1 - agricultural_sensitivity)) / 2
    long_term_recovery_factor = 0.6 + (adaptation_efficiency * 0.3)  # 60-90% recovery
    long_term_gdp_loss = initial_gdp_loss * (1 - long_term_recovery_factor)
    
    # Adaptation time (years)
    # Faster changes and lower adaptability = longer adaptation
    base_adaptation_time = 10  # Base 10 years for major global adaptation
    adaptation_time_years = base_adaptation_time * disruption_factor * (2 - adaptation_efficiency)
    
    # Physical effects
    # Sea level shift due to centrifugal force changes
    # Simplified: roughly proportional to rotation change squared
    sea_level_shift_meters = (rotation_change_percent / 100) ** 2 * 50  # Up to 50m for 100% change
    
    # Climate volatility from Coriolis effect changes
    coriolis_change_factor = rotation_change_percent / 100
    climate_volatility_index = 1 + (coriolis_change_factor * climate_volatility_multiplier)
    
    # Labor productivity change (negative due to circadian disruption)
    labor_productivity_change = -circadian_disruption * 20  # Up to -20%
    
    # Sea wave intensity (affected by rotation speed)
    # Ocean currents and wave patterns change with rotation
    sea_wave_intensity_change = rotation_change_percent * 1.5  # 1.5x multiplier
    
    # Population impact (extreme scenarios)
    # Based on climate volatility, agricultural loss, and adaptation challenges
    climate_stress = (climate_volatility_index - 1) * 100
    agricultural_stress = agricultural_impact * 100
    adaptation_stress = (1 - adaptation_efficiency) * disruption_factor * 100
    
    total_stress = climate_stress + agricultural_stress + adaptation_stress
    population_drop_percent = min(50, total_stress * 0.1)  # Cap at 50% for extreme scenarios
    
    return {
        'new_day_length_hours': new_day_length_hours,
        'initial_gdp_loss': initial_gdp_loss,
        'long_term_gdp_loss': long_term_gdp_loss,
        'adaptation_time_years': adaptation_time_years,
        'sea_level_shift_meters': sea_level_shift_meters,
        'climate_volatility_index': climate_volatility_index,
        'labor_productivity_change': labor_productivity_change,
        'circadian_stress_index': circadian_disruption,
        'sea_wave_intensity_change': sea_wave_intensity_change,
        'population_drop_percent': population_drop_percent
    }


class EarthRotationShockModel:
    """
    Earth Rotation Shock Model
    
    Simulates the comprehensive effects of changes in Earth's rotation speed including:
    - Day length changes and circadian disruption
    - Agricultural productivity impacts
    - Infrastructure adaptation costs
    - Climate system instability
    - Sea level and ocean current changes
    - Human population and productivity effects
    - Economic adaptation dynamics
    """
    
    def __init__(self, parameters: Dict[str, Any]):
        """
        Initialize the Earth Rotation Shock Model.
        
        Args:
            parameters: Model calibration parameters
        """
        self.parameters = self._validate_parameters(parameters)
        logger.info("Earth Rotation Shock Model initialized")
    
    def _validate_parameters(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and set default parameters."""
        defaults = {
            # Physical parameters
            'rotation_change_percent': 10.0,      # 10% increase in rotation speed
            'baseline_day_length': 24.0,          # 24 hours baseline
            'initial_gdp': 100000000000000.0,     # $100 trillion global GDP
            
            # Economic baseline parameters
            'baseline_gdp_growth': 0.03,          # 3% baseline GDP growth
            'gdp_day_night_dependency': 0.3,      # 30% of GDP depends on day/night cycles
            'infrastructure_adaptability': 0.5,   # 50% infrastructure adaptability
            'agricultural_sensitivity': 0.7,      # 70% agricultural sensitivity
            'climate_volatility_multiplier': 1.2, # 20% increase in climate volatility
            
            # Adaptation parameters
            'adaptation_cost_factor': 1.5,        # 1.5x cost multiplier for adaptation
            'infrastructure_disruption_index': 0.5, # 50% infrastructure disruption
            'base_adaptation_time': 10,           # 10 years base adaptation time
            'adaptation_efficiency_improvement': 0.05, # 5% annual improvement in adaptation
            
            # Impact multipliers
            'circadian_disruption_multiplier': 2.0,   # Circadian effects multiplier
            'agricultural_impact_multiplier': 0.25,   # Agricultural GDP impact multiplier
            'infrastructure_impact_multiplier': 0.15, # Infrastructure GDP impact multiplier
            'productivity_impact_multiplier': 0.1,    # Productivity GDP impact multiplier
            
            # Physical effects
            'sea_level_sensitivity': 50.0,        # Meters per 100% rotation change
            'coriolis_climate_sensitivity': 1.0,  # Climate sensitivity to Coriolis changes
            'ocean_current_sensitivity': 1.5,     # Ocean current sensitivity multiplier
            
            # Recovery parameters
            'recovery_rate': 0.1,                 # 10% annual recovery rate
            'minimum_recovery_factor': 0.6,       # 60% minimum recovery
            'maximum_recovery_factor': 0.9,       # 90% maximum recovery
            
            # Model parameters
            'periods': 50,                        # 50-year simulation
            'shock_persistence': 0.95,           # How persistent the shock effects are
        }
        
        # Merge with provided parameters
        for key, default_value in defaults.items():
            if key not in params:
                params[key] = default_value
        
        return params
    
    def simulate(self, simulation_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the Earth rotation shock simulation.
        
        Args:
            simulation_config: Simulation configuration including shock details
            
        Returns:
            Dictionary containing simulation results
        """
        periods = self.parameters['periods']
        
        # Parse shock configuration
        shock_config = simulation_config.get('shock', {})
        shock = EarthRotationShock(
            rotation_change_percent=shock_config.get('rotation_change_percent', self.parameters['rotation_change_percent']),
            adaptation_cost_factor=shock_config.get('adaptation_cost_factor', self.parameters['adaptation_cost_factor']),
            climate_volatility_multiplier=shock_config.get('climate_volatility_multiplier', self.parameters['climate_volatility_multiplier']),
            agriculture_loss_rate=shock_config.get('agriculture_loss_rate', self.parameters['agricultural_sensitivity']),
            infrastructure_disruption_index=shock_config.get('infrastructure_disruption_index', self.parameters['infrastructure_disruption_index']),
            start_period=shock_config.get('start_period', 0)
        )
        
        logger.info(f"Simulating Earth rotation shock: {shock.rotation_change_percent:.1f}% rotation speed change")
        
        # Calculate new day length
        rotation_factor = 1 + (shock.rotation_change_percent / 100)
        new_day_length = self.parameters['baseline_day_length'] / rotation_factor
        
        # Initialize time series
        results = {
            'periods': list(range(periods)),
            'rotation_active': np.zeros(periods, dtype=bool),
            'day_length_hours': np.full(periods, self.parameters['baseline_day_length']),
            'gdp': np.full(periods, self.parameters['initial_gdp']),
            'gdp_growth': np.full(periods, self.parameters['baseline_gdp_growth']),
            'agricultural_productivity': np.ones(periods),  # Normalized to 1.0
            'infrastructure_adaptation': np.ones(periods),  # Normalized to 1.0
            'climate_volatility_index': np.ones(periods),   # 1.0 = baseline
            'circadian_stress_index': np.zeros(periods),    # 0 = no stress
            'labor_productivity': np.ones(periods),         # Normalized to 1.0
            'sea_level_shift': np.zeros(periods),           # Meters
            'adaptation_progress': np.zeros(periods),       # 0-1 scale
            'population_level': np.ones(periods),           # Normalized to 1.0
            'sea_wave_intensity': np.ones(periods),         # Normalized to 1.0
        }
        
        # Apply rotation shock effects
        for t in range(periods):
            # Determine if shock is active
            shock_active = t >= shock.start_period
            results['rotation_active'][t] = shock_active
            
            if shock_active:
                # Apply rotation shock effects
                self._apply_rotation_effects(results, t, shock, new_day_length)
            
            # Update economic indicators
            self._update_economic_indicators(results, t, shock)
            
            # Update adaptation progress
            self._update_adaptation_progress(results, t, shock)
        
        # Convert numpy arrays to lists for JSON serialization
        for key, value in results.items():
            if isinstance(value, np.ndarray):
                if value.dtype == bool:
                    results[key] = value.astype(int).tolist()
                else:
                    results[key] = value.tolist()
        
        # Add summary statistics
        results['summary'] = self._calculate_summary(results, shock, new_day_length)
        
        logger.info("Earth rotation shock simulation completed")
        return results
    
    def _apply_rotation_effects(self, results: Dict[str, Any], period: int, 
                              shock: EarthRotationShock, new_day_length: float):
        """Apply the effects of Earth rotation speed change."""
        if period == 0:
            return
        
        # Day length change
        results['day_length_hours'][period] = new_day_length
        
        # Calculate disruption magnitude
        day_length_change = abs(new_day_length - self.parameters['baseline_day_length'])
        disruption_magnitude = day_length_change / self.parameters['baseline_day_length']
        
        # Agricultural productivity impact
        ag_sensitivity = shock.agriculture_loss_rate
        ag_impact = disruption_magnitude * ag_sensitivity
        results['agricultural_productivity'][period] = max(0.1, 1 - ag_impact)
        
        # Infrastructure adaptation (gradual improvement)
        if period > 0:
            prev_adaptation = results['infrastructure_adaptation'][period - 1]
            adaptation_rate = self.parameters['adaptation_efficiency_improvement']
            disruption_factor = shock.infrastructure_disruption_index * disruption_magnitude
            
            # Infrastructure degrades initially, then adapts
            if period <= 5:  # First 5 years: degradation
                results['infrastructure_adaptation'][period] = max(0.2, prev_adaptation - disruption_factor * 0.1)
            else:  # After 5 years: gradual adaptation
                target_adaptation = 1 - (disruption_factor * 0.5)  # Never fully recovers for large shocks
                recovery = (target_adaptation - prev_adaptation) * adaptation_rate
                results['infrastructure_adaptation'][period] = min(1.0, prev_adaptation + recovery)
        else:
            results['infrastructure_adaptation'][period] = 1.0
        
        # Climate volatility
        coriolis_change = shock.rotation_change_percent / 100
        climate_multiplier = shock.climate_volatility_multiplier
        results['climate_volatility_index'][period] = 1 + (coriolis_change * climate_multiplier)
        
        # Circadian stress (peaks early, then gradual adaptation)
        max_circadian_stress = min(1.0, disruption_magnitude * self.parameters['circadian_disruption_multiplier'])
        adaptation_factor = results['adaptation_progress'][period - 1] if period > 0 else 0
        results['circadian_stress_index'][period] = max_circadian_stress * (1 - adaptation_factor * 0.7)
        
        # Labor productivity (affected by circadian stress)
        circadian_impact = results['circadian_stress_index'][period]
        results['labor_productivity'][period] = 1 - (circadian_impact * 0.2)  # Up to 20% reduction
        
        # Sea level shift (immediate physical effect)
        rotation_change_factor = (shock.rotation_change_percent / 100) ** 2
        results['sea_level_shift'][period] = rotation_change_factor * self.parameters['sea_level_sensitivity']
        
        # Sea wave intensity
        wave_change = shock.rotation_change_percent * self.parameters['ocean_current_sensitivity'] / 100
        results['sea_wave_intensity'][period] = 1 + wave_change
        
        # Population impact (gradual, based on multiple stressors)
        climate_stress = results['climate_volatility_index'][period] - 1
        agricultural_stress = 1 - results['agricultural_productivity'][period]
        total_stress = (climate_stress + agricultural_stress) / 2
        
        if period > 0:
            prev_population = results['population_level'][period - 1]
            population_decline_rate = total_stress * 0.02  # Up to 2% annual decline
            results['population_level'][period] = max(0.5, prev_population * (1 - population_decline_rate))
        else:
            results['population_level'][period] = 1.0
    
    def _update_economic_indicators(self, results: Dict[str, Any], period: int, shock: EarthRotationShock):
        """Update GDP and economic growth based on rotation effects."""
        if period == 0:
            results['gdp'][period] = self.parameters['initial_gdp']
            results['gdp_growth'][period] = self.parameters['baseline_gdp_growth']
            return
        
        baseline_growth = self.parameters['baseline_gdp_growth']
        
        # Agricultural impact (5% of GDP)
        ag_productivity = results['agricultural_productivity'][period]
        ag_impact = (ag_productivity - 1) * 0.05  # 5% of GDP is agriculture
        
        # Infrastructure impact
        infrastructure_level = results['infrastructure_adaptation'][period]
        infrastructure_impact = (infrastructure_level - 1) * 0.2  # 20% of GDP affected
        
        # Labor productivity impact
        labor_productivity = results['labor_productivity'][period]
        labor_impact = (labor_productivity - 1) * 0.6  # 60% of GDP is labor-dependent
        
        # Climate volatility impact
        climate_volatility = results['climate_volatility_index'][period]
        climate_impact = -(climate_volatility - 1) * 0.1  # 10% GDP impact from climate
        
        # Population impact
        population_level = results['population_level'][period]
        population_impact = (population_level - 1) * 0.3  # 30% GDP scales with population
        
        # Total growth impact
        total_impact = ag_impact + infrastructure_impact + labor_impact + climate_impact + population_impact
        results['gdp_growth'][period] = max(-0.3, baseline_growth + total_impact)  # Floor at -30%
        
        # Update GDP level
        results['gdp'][period] = results['gdp'][period - 1] * (1 + results['gdp_growth'][period])
    
    def _update_adaptation_progress(self, results: Dict[str, Any], period: int, shock: EarthRotationShock):
        """Update human and societal adaptation progress."""
        if period == 0:
            results['adaptation_progress'][period] = 0.0
            return
        
        # Adaptation progress (S-curve: slow start, rapid middle, slow end)
        base_adaptation_time = self.parameters['base_adaptation_time']
        disruption_magnitude = abs(shock.rotation_change_percent) / 100
        
        # Adaptation time scales with disruption magnitude
        total_adaptation_time = base_adaptation_time * (1 + disruption_magnitude)
        
        # S-curve adaptation function
        if period < total_adaptation_time:
            # Logistic function for S-curve
            x = (period / total_adaptation_time) * 10 - 5  # Scale to -5 to +5
            adaptation_level = 1 / (1 + np.exp(-x))
        else:
            adaptation_level = 1.0
        
        results['adaptation_progress'][period] = adaptation_level
    
    def _calculate_summary(self, results: Dict[str, Any], shock: EarthRotationShock, 
                         new_day_length: float) -> Dict[str, Any]:
        """Calculate summary statistics for the simulation."""
        gdp_values = np.array(results['gdp'])
        growth_values = np.array(results['gdp_growth'])
        ag_values = np.array(results['agricultural_productivity'])
        infrastructure_values = np.array(results['infrastructure_adaptation'])
        population_values = np.array(results['population_level'])
        
        # Use simple function for final assessment
        final_assessment = simulate_earth_rotation_shock(
            rotation_change_percent=shock.rotation_change_percent,
            initial_gdp=self.parameters['initial_gdp'],
            gdp_day_night_dependency=self.parameters['gdp_day_night_dependency'],
            infrastructure_adaptability=self.parameters['infrastructure_adaptability'],
            agricultural_sensitivity=self.parameters['agricultural_sensitivity'],
            climate_volatility_multiplier=self.parameters['climate_volatility_multiplier']
        )
        
        return {
            'new_day_length_hours': float(new_day_length),
            'day_length_change_percent': float((new_day_length - 24) / 24 * 100),
            'peak_gdp_decline': float(np.min(growth_values) * 100),
            'total_gdp_loss': float((gdp_values[0] - np.min(gdp_values)) / gdp_values[0] * 100),
            'final_gdp_level': float(gdp_values[-1] / gdp_values[0] * 100),
            'min_agricultural_productivity': float(np.min(ag_values) * 100),
            'final_agricultural_productivity': float(ag_values[-1] * 100),
            'min_infrastructure_adaptation': float(np.min(infrastructure_values) * 100),
            'final_infrastructure_adaptation': float(infrastructure_values[-1] * 100),
            'total_population_decline': float((1 - np.min(population_values)) * 100),
            'final_population_level': float(population_values[-1] * 100),
            'adaptation_completion_year': int(np.argmax(np.array(results['adaptation_progress']) >= 0.95)),
            'max_sea_level_shift': float(np.max(results['sea_level_shift'])),
            'max_climate_volatility': float(np.max(results['climate_volatility_index'])),
            'max_circadian_stress': float(np.max(results['circadian_stress_index'])),
            'severity_assessment': 'Catastrophic' if final_assessment['initial_gdp_loss'] > 30 else 'Severe' if final_assessment['initial_gdp_loss'] > 15 else 'Moderate',
            'final_assessment': final_assessment
        } 