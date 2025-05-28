"""
Inflation Shock Model

Economic model for simulating the effects of inflation spikes
on various economic indicators including GDP, investment, and consumption.
"""

import numpy as np
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class InflationShock:
    """Configuration for an inflation shock."""
    spike_magnitude: float  # Percentage point increase in inflation (e.g., 3.0 for 3pp)
    duration: int          # Number of periods the shock persists
    start_period: int = 0  # When the shock begins


def simulate_inflation_shock(current_inflation: float, inflation_spike: float, 
                           gdp: float, investment_level: float) -> Dict[str, float]:
    """
    Simple, interpretable function to simulate the effect of an inflation shock.
    
    Args:
        current_inflation: Current inflation rate (%)
        inflation_spike: Additional inflation spike (%)
        gdp: Current GDP (in USD)
        investment_level: Current investment level (USD)
        
    Returns:
        Dict containing:
        - new_inflation: Combined inflation rate
        - real_gdp_estimate: Adjusted GDP with -4% contraction
        - expected_investment_drop: Percentage drop in investment
        - expected_consumption_change: Fixed -4% consumption change
    """
    # Calculate new combined inflation rate
    new_inflation = current_inflation + inflation_spike
    
    # Apply simplified economic impacts based on historical patterns
    # Real GDP contracts by approximately 4% during high inflation periods
    real_gdp_estimate = gdp * 0.96  # 4% contraction
    
    # Investment typically drops more severely during inflation spikes
    # Using a simple multiplier: 2% investment drop per 1% inflation spike
    investment_drop_percentage = min(inflation_spike * 2.0, 20.0)  # Cap at 20%
    
    # Consumption fixed at -4% as specified
    expected_consumption_change = -4.0
    
    return {
        'new_inflation': new_inflation,
        'real_gdp_estimate': real_gdp_estimate,
        'expected_investment_drop': investment_drop_percentage,
        'expected_consumption_change': expected_consumption_change
    }


class InflationShockModel:
    """
    Inflation Shock Model
    
    Simulates the macroeconomic effects of inflation spikes including:
    - Real GDP contraction
    - Investment decline
    - Consumption reduction
    - Price level adjustments
    """
    
    def __init__(self, parameters: Dict[str, Any]):
        """
        Initialize the Inflation Shock Model.
        
        Args:
            parameters: Model calibration parameters
        """
        self.parameters = self._validate_parameters(parameters)
        logger.info("Inflation Shock Model initialized")
    
    def _validate_parameters(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and set default parameters."""
        defaults = {
            # Economic impact parameters
            'gdp_contraction_rate': -0.04,      # 4% GDP contraction during high inflation
            'investment_sensitivity': -2.0,     # 2% investment drop per 1% inflation
            'consumption_impact': -0.04,        # Fixed 4% consumption reduction
            'max_investment_drop': 0.20,        # Cap investment drop at 20%
            
            # Baseline economic values
            'baseline_inflation': 0.025,        # 2.5% baseline inflation (as decimal)
            'baseline_gdp': 25000000000000.0,   # $25 trillion baseline GDP
            'baseline_investment': 5000000000000.0,  # $5 trillion baseline investment
            'baseline_consumption': 15000000000000.0, # $15 trillion baseline consumption
            
            # Model parameters
            'periods': 20,                      # Number of simulation periods
            'shock_persistence': 0.9,          # How quickly inflation shock decays
        }
        
        # Merge with provided parameters
        for key, default_value in defaults.items():
            if key not in params:
                params[key] = default_value
        
        return params
    
    def simulate(self, simulation_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the inflation shock simulation.
        
        Args:
            simulation_config: Simulation configuration including shock details
            
        Returns:
            Dictionary containing simulation results
        """
        periods = self.parameters['periods']
        
        # Parse shock configuration
        shock_config = simulation_config.get('shock', {})
        shock = InflationShock(
            spike_magnitude=shock_config.get('spike_magnitude', 0.0),
            duration=shock_config.get('duration', 5),
            start_period=shock_config.get('start_period', 0)
        )
        
        logger.info(f"Simulating {shock.spike_magnitude:.1f}pp inflation shock "
                   f"for {shock.duration} periods starting at period {shock.start_period}")
        
        # Initialize time series
        results = {
            'periods': list(range(periods)),
            'inflation_shock': np.zeros(periods),
            'inflation_rate': np.full(periods, self.parameters['baseline_inflation']),
            'real_gdp': np.full(periods, self.parameters['baseline_gdp']),
            'investment': np.full(periods, self.parameters['baseline_investment']),
            'consumption': np.full(periods, self.parameters['baseline_consumption']),
        }
        
        # Apply inflation shock
        for t in range(periods):
            if shock.start_period <= t < shock.start_period + shock.duration:
                # Apply shock with persistence decay
                shock_period = t - shock.start_period
                persistence_factor = self.parameters['shock_persistence'] ** shock_period
                current_shock = shock.spike_magnitude * persistence_factor
                results['inflation_shock'][t] = current_shock
                
                # Update inflation rate (convert percentage to decimal)
                results['inflation_rate'][t] += current_shock / 100.0
                
                # Calculate economic impacts using the simple function
                simple_result = simulate_inflation_shock(
                    current_inflation=self.parameters['baseline_inflation'] * 100,
                    inflation_spike=current_shock,
                    gdp=self.parameters['baseline_gdp'],
                    investment_level=self.parameters['baseline_investment']
                )
                
                # Apply the calculated impacts
                self._apply_shock_effects(results, t, simple_result)
        
        # Convert numpy arrays to lists for JSON serialization
        for key, value in results.items():
            if isinstance(value, np.ndarray):
                results[key] = value.tolist()
        
        # Add summary statistics
        results['summary'] = self._calculate_summary(results)
        
        logger.info("Inflation shock simulation completed")
        return results
    
    def _apply_shock_effects(self, results: Dict[str, Any], period: int, simple_result: Dict[str, float]):
        """Apply the economic effects from the simple simulation function."""
        # Real GDP impact
        gdp_contraction = self.parameters['gdp_contraction_rate']
        results['real_gdp'][period] *= (1 + gdp_contraction)
        
        # Investment impact
        investment_drop = simple_result['expected_investment_drop'] / 100.0
        results['investment'][period] *= (1 - min(investment_drop, self.parameters['max_investment_drop']))
        
        # Consumption impact
        consumption_change = simple_result['expected_consumption_change'] / 100.0
        results['consumption'][period] *= (1 + consumption_change)
    
    def _calculate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate summary statistics for the simulation."""
        inflation_values = np.array(results['inflation_rate'])
        gdp_values = np.array(results['real_gdp'])
        investment_values = np.array(results['investment'])
        consumption_values = np.array(results['consumption'])
        
        return {
            'avg_inflation_rate': float(np.mean(inflation_values)),
            'peak_inflation': float(np.max(inflation_values)),
            'min_inflation': float(np.min(inflation_values)),
            'avg_real_gdp': float(np.mean(gdp_values)),
            'min_real_gdp': float(np.min(gdp_values)),
            'max_real_gdp': float(np.max(gdp_values)),
            'total_gdp_loss': float(self.parameters['baseline_gdp'] * len(gdp_values) - np.sum(gdp_values)),
            'total_investment_loss': float(self.parameters['baseline_investment'] * len(investment_values) - np.sum(investment_values)),
            'total_consumption_loss': float(self.parameters['baseline_consumption'] * len(consumption_values) - np.sum(consumption_values)),
            'gdp_contraction_percent': float((self.parameters['baseline_gdp'] - np.min(gdp_values)) / self.parameters['baseline_gdp'] * 100),
        } 