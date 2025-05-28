"""
Interest Rate Shock Model

Economic model for simulating the effects of interest rate changes
on various economic indicators.
"""

import numpy as np
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class InterestRateShock:
    """Configuration for an interest rate shock."""
    magnitude: float  # Percentage point change (e.g., 0.5 for 50 basis points)
    duration: int     # Number of periods the shock persists
    start_period: int = 0  # When the shock begins


class InterestRateModel:
    """
    Interest Rate Shock Model
    
    Simulates the macroeconomic effects of interest rate changes including:
    - GDP growth impact
    - Inflation effects
    - Investment changes
    - Consumption patterns
    """
    
    def __init__(self, parameters: Dict[str, Any]):
        """
        Initialize the Interest Rate Model.
        
        Args:
            parameters: Model calibration parameters
        """
        self.parameters = self._validate_parameters(parameters)
        logger.info("Interest Rate Model initialized")
    
    def _validate_parameters(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and set default parameters."""
        defaults = {
            # Sensitivity parameters
            'gdp_sensitivity': -0.3,      # GDP response to 1pp rate increase
            'inflation_sensitivity': -0.2, # Inflation response to 1pp rate increase
            'investment_sensitivity': -0.8, # Investment response to 1pp rate increase
            'consumption_sensitivity': -0.15, # Consumption response to 1pp rate increase
            
            # Baseline values
            'baseline_gdp_growth': 0.02,    # 2% quarterly growth
            'baseline_inflation': 0.005,    # 0.5% quarterly inflation
            'baseline_investment': 1000.0,  # Baseline investment level
            'baseline_consumption': 5000.0, # Baseline consumption level
            
            # Model parameters
            'periods': 20,                  # Number of simulation periods
            'persistence': 0.8,            # Shock persistence factor
        }
        
        # Merge with provided parameters
        for key, default_value in defaults.items():
            if key not in params:
                params[key] = default_value
        
        return params
    
    def simulate(self, simulation_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the interest rate shock simulation.
        
        Args:
            simulation_config: Simulation configuration including shocks
            
        Returns:
            Dictionary containing simulation results
        """
        periods = self.parameters['periods']
        
        # Parse shock configuration
        shock_config = simulation_config.get('shock', {})
        shock = InterestRateShock(
            magnitude=shock_config.get('magnitude', 0.0),
            duration=shock_config.get('duration', 5),
            start_period=shock_config.get('start_period', 0)
        )
        
        logger.info(f"Simulating {shock.magnitude*100:.1f} basis point shock "
                   f"for {shock.duration} periods starting at period {shock.start_period}")
        
        # Initialize time series
        results = {
            'periods': list(range(periods)),
            'interest_rate_shock': np.zeros(periods),
            'gdp_growth': np.full(periods, self.parameters['baseline_gdp_growth']),
            'inflation': np.full(periods, self.parameters['baseline_inflation']),
            'investment': np.full(periods, self.parameters['baseline_investment']),
            'consumption': np.full(periods, self.parameters['baseline_consumption']),
        }
        
        # Apply interest rate shock
        for t in range(periods):
            if shock.start_period <= t < shock.start_period + shock.duration:
                # Apply shock with persistence decay
                shock_period = t - shock.start_period
                persistence_factor = self.parameters['persistence'] ** shock_period
                current_shock = shock.magnitude * persistence_factor
                results['interest_rate_shock'][t] = current_shock
                
                # Calculate economic impacts
                self._apply_shock_effects(results, t, current_shock)
        
        # Convert numpy arrays to lists for JSON serialization
        for key, value in results.items():
            if isinstance(value, np.ndarray):
                results[key] = value.tolist()
        
        # Add summary statistics
        results['summary'] = self._calculate_summary(results)
        
        logger.info("Interest rate shock simulation completed")
        return results
    
    def _apply_shock_effects(self, results: Dict[str, Any], period: int, shock: float):
        """Apply the economic effects of the interest rate shock."""
        # GDP growth impact
        gdp_impact = shock * self.parameters['gdp_sensitivity']
        results['gdp_growth'][period] += gdp_impact
        
        # Inflation impact
        inflation_impact = shock * self.parameters['inflation_sensitivity']
        results['inflation'][period] += inflation_impact
        
        # Investment impact (percentage change from baseline)
        investment_impact = shock * self.parameters['investment_sensitivity']
        investment_multiplier = 1 + (investment_impact / 100)
        results['investment'][period] *= investment_multiplier
        
        # Consumption impact (percentage change from baseline)
        consumption_impact = shock * self.parameters['consumption_sensitivity']
        consumption_multiplier = 1 + (consumption_impact / 100)
        results['consumption'][period] *= consumption_multiplier
    
    def _calculate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate summary statistics for the simulation."""
        gdp_values = np.array(results['gdp_growth'])
        inflation_values = np.array(results['inflation'])
        investment_values = np.array(results['investment'])
        consumption_values = np.array(results['consumption'])
        
        return {
            'avg_gdp_growth': float(np.mean(gdp_values)),
            'min_gdp_growth': float(np.min(gdp_values)),
            'max_gdp_growth': float(np.max(gdp_values)),
            'avg_inflation': float(np.mean(inflation_values)),
            'min_inflation': float(np.min(inflation_values)),
            'max_inflation': float(np.max(inflation_values)),
            'total_investment_change': float(np.sum(investment_values) - 
                                           len(investment_values) * self.parameters['baseline_investment']),
            'total_consumption_change': float(np.sum(consumption_values) - 
                                            len(consumption_values) * self.parameters['baseline_consumption']),
        } 