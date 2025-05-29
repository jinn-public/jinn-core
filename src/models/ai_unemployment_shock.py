"""
AI Unemployment Shock Model

Economic model for simulating the effects of AI-driven unemployment on the economy,
including UBI implementation, productivity growth, and fiscal sustainability.
"""

import numpy as np
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class AIUnemploymentShock:
    """Configuration for an AI unemployment shock."""
    ai_displacement_rate: float      # Annual unemployment increase rate (%)
    max_unemployment: float          # Maximum unemployment rate to reach (%)
    duration: int                    # Number of years to simulate
    start_year: int = 0             # When AI displacement begins


def simulate_ai_unemployment_shock(
    current_employment_rate: float,
    ai_displacement_rate: float,
    current_gdp: float,
    current_year: int,
    max_displacement: float = 30.0,
    ubi_threshold: float = 12.0
) -> Dict[str, float]:
    """
    Simple, interpretable function to simulate the effect of AI unemployment shock.
    
    Args:
        current_employment_rate: Current employment rate (%)
        ai_displacement_rate: Annual AI displacement rate (%)
        current_gdp: Current GDP (in USD)
        current_year: Current simulation year
        max_displacement: Maximum total displacement (%)
        ubi_threshold: Unemployment threshold for UBI activation (%)
        
    Returns:
        Dict containing:
        - new_unemployment_rate: Updated unemployment rate
        - new_employment_rate: Updated employment rate
        - productivity_boost: AI-driven productivity increase
        - ubi_activated: Whether UBI is triggered
        - ubi_cost: Annual UBI cost if activated
    """
    initial_unemployment = 6.0  # Starting from 94% employment = 6% unemployment
    
    # Calculate cumulative displacement (capped at max_displacement)
    total_displacement = min(ai_displacement_rate * current_year, max_displacement)
    new_unemployment_rate = min(initial_unemployment + total_displacement, initial_unemployment + max_displacement)
    new_employment_rate = 100 - new_unemployment_rate
    
    # AI productivity boost: baseline 2% + AI boost up to 4% more
    ai_productivity_factor = min(total_displacement / max_displacement, 1.0)
    productivity_boost = 2.0 + (4.0 * ai_productivity_factor)  # 2-6% range
    
    # UBI activation
    ubi_activated = new_unemployment_rate >= ubi_threshold
    ubi_cost = 0.0
    
    if ubi_activated:
        # UBI coverage scales with unemployment severity
        unemployment_severity = (new_unemployment_rate - ubi_threshold) / (50.0 - ubi_threshold)
        coverage_rate = 0.5 + (0.5 * unemployment_severity)  # 50-100% coverage
        ubi_cost = current_gdp * 0.001 * 15 * coverage_rate  # $15k per person, scaled by coverage
    
    return {
        'new_unemployment_rate': new_unemployment_rate,
        'new_employment_rate': new_employment_rate,
        'productivity_boost': productivity_boost,
        'ubi_activated': ubi_activated,
        'ubi_cost': ubi_cost,
        'ubi_coverage_rate': coverage_rate if ubi_activated else 0.0
    }


class AIUnemploymentShockModel:
    """
    AI Unemployment Shock Model
    
    Simulates the macroeconomic effects of AI-driven unemployment including:
    - Employment/unemployment rate dynamics
    - GDP growth with productivity vs. employment trade-offs
    - UBI implementation and fiscal impacts
    - Government budget sustainability
    - Scenario comparison (with/without UBI)
    """
    
    def __init__(self, parameters: Dict[str, Any]):
        """
        Initialize the AI Unemployment Shock Model.
        
        Args:
            parameters: Model calibration parameters
        """
        self.parameters = self._validate_parameters(parameters)
        logger.info("AI Unemployment Shock Model initialized")
    
    def _validate_parameters(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and set default parameters."""
        defaults = {
            # Initial conditions
            'initial_employment_rate': 94.0,       # 94% initial employment
            'initial_gdp': 25_000_000_000_000.0,   # $25 trillion initial GDP
            'baseline_productivity_growth': 2.0,    # 2% baseline productivity growth
            
            # AI displacement parameters
            'ai_displacement_rate': 1.0,           # 1% unemployment increase per year
            'max_unemployment_rate': 30.0,         # Max 30% unemployment over 30 years
            'ai_productivity_boost_min': 2.0,      # Minimum AI productivity boost
            'ai_productivity_boost_max': 6.0,      # Maximum AI productivity boost
            
            # UBI parameters
            'ubi_threshold': 12.0,                 # UBI activated at 12% unemployment
            'ubi_amount_per_person': 15000.0,      # $15,000 per person per year
            'ubi_coverage_min': 0.5,               # 50% minimum coverage
            'ubi_coverage_max': 1.0,               # 100% maximum coverage
            
            # Economic parameters
            'gdp_employment_elasticity': 0.6,      # GDP sensitivity to employment
            'government_spending_limit': 0.30,     # 30% of GDP max government spending
            'tax_adjustment_sensitivity': 1.5,     # Tax adjustment aggressiveness
            
            # Simulation parameters
            'periods': 30,                         # 30 years
            'population': 330_000_000,             # US population approximation
        }
        
        # Merge with provided parameters
        for key, default_value in defaults.items():
            if key not in params:
                params[key] = default_value
        
        return params
    
    def simulate(self, simulation_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the AI unemployment shock simulation.
        
        Args:
            simulation_config: Simulation configuration including shock details
            
        Returns:
            Dictionary containing simulation results
        """
        periods = self.parameters['periods']
        
        # Parse shock configuration
        shock_config = simulation_config.get('shock', {})
        shock = AIUnemploymentShock(
            ai_displacement_rate=shock_config.get('ai_displacement_rate', self.parameters['ai_displacement_rate']),
            max_unemployment=shock_config.get('max_unemployment', self.parameters['max_unemployment_rate']),
            duration=periods,
            start_year=shock_config.get('start_year', 0)
        )
        
        # Check if we should compare scenarios
        compare_scenarios = simulation_config.get('compare_scenarios', True)
        
        logger.info(f"Simulating AI unemployment shock: {shock.ai_displacement_rate}% displacement/year "
                   f"for {shock.duration} years, max {shock.max_unemployment}% unemployment")
        
        if compare_scenarios:
            # Run both scenarios
            scenario_with_ubi = self._run_single_scenario(shock, ubi_enabled=True)
            scenario_without_ubi = self._run_single_scenario(shock, ubi_enabled=False)
            
            results = {
                'scenario_with_ubi': scenario_with_ubi,
                'scenario_without_ubi': scenario_without_ubi,
                'comparison': self._compare_scenarios(scenario_with_ubi, scenario_without_ubi)
            }
        else:
            # Run single scenario
            ubi_enabled = simulation_config.get('ubi_enabled', True)
            results = self._run_single_scenario(shock, ubi_enabled)
        
        logger.info("AI unemployment shock simulation completed")
        return results
    
    def _run_single_scenario(self, shock: AIUnemploymentShock, ubi_enabled: bool) -> Dict[str, Any]:
        """Run a single scenario simulation."""
        periods = self.parameters['periods']
        
        # Initialize time series
        results = {
            'periods': list(range(periods)),
            'employment_rate': np.full(periods, self.parameters['initial_employment_rate']),
            'unemployment_rate': np.full(periods, 100 - self.parameters['initial_employment_rate']),
            'gdp': np.full(periods, self.parameters['initial_gdp']),
            'productivity_growth': np.full(periods, self.parameters['baseline_productivity_growth']),
            'ubi_activated': np.zeros(periods, dtype=bool),
            'ubi_cost': np.zeros(periods),
            'ubi_coverage_rate': np.zeros(periods),
            'government_spending': np.zeros(periods),
            'tax_rate': np.full(periods, 0.25),  # Start with 25% tax rate
            'budget_balance': np.zeros(periods),
            'ubi_enabled': ubi_enabled
        }
        
        # Run simulation year by year
        for t in range(periods):
            if t == 0:
                # Initialize first year
                continue
            
            # Calculate AI displacement effects
            simple_result = simulate_ai_unemployment_shock(
                current_employment_rate=results['employment_rate'][t-1],
                ai_displacement_rate=shock.ai_displacement_rate,
                current_gdp=results['gdp'][t-1],
                current_year=t,
                max_displacement=shock.max_unemployment,
                ubi_threshold=self.parameters['ubi_threshold']
            )
            
            # Update employment/unemployment
            results['unemployment_rate'][t] = simple_result['new_unemployment_rate']
            results['employment_rate'][t] = simple_result['new_employment_rate']
            results['productivity_growth'][t] = simple_result['productivity_boost']
            
            # Update GDP based on employment and productivity trade-offs
            employment_effect = self._calculate_employment_effect(
                results['employment_rate'][t],
                results['employment_rate'][t-1]
            )
            productivity_effect = results['productivity_growth'][t] / 100.0
            gdp_growth = employment_effect + productivity_effect
            results['gdp'][t] = results['gdp'][t-1] * (1 + gdp_growth)
            
            # UBI logic (only if enabled for this scenario)
            if ubi_enabled and simple_result['ubi_activated']:
                results['ubi_activated'][t] = True
                results['ubi_cost'][t] = simple_result['ubi_cost']
                results['ubi_coverage_rate'][t] = simple_result['ubi_coverage_rate']
            
            # Government fiscal dynamics
            self._update_fiscal_position(results, t)
        
        # Convert numpy arrays to lists for JSON serialization
        for key, value in results.items():
            if isinstance(value, np.ndarray):
                results[key] = value.tolist()
        
        # Add summary statistics
        results['summary'] = self._calculate_summary(results)
        
        return results
    
    def _calculate_employment_effect(self, current_employment: float, previous_employment: float) -> float:
        """Calculate GDP effect from employment changes."""
        employment_change = (current_employment - previous_employment) / previous_employment
        return employment_change * self.parameters['gdp_employment_elasticity']
    
    def _update_fiscal_position(self, results: Dict[str, Any], t: int):
        """Update government fiscal position including UBI costs and tax adjustments."""
        current_gdp = results['gdp'][t]
        ubi_cost = results['ubi_cost'][t]
        
        # Base government spending (excluding UBI)
        base_spending = current_gdp * 0.20  # 20% of GDP baseline
        total_spending = base_spending + ubi_cost
        results['government_spending'][t] = total_spending
        
        # Calculate required tax rate
        target_tax_rate = total_spending / current_gdp
        max_tax_rate = 0.50  # Cap at 50%
        
        # Gradual tax adjustment
        if t > 0:
            previous_tax_rate = results['tax_rate'][t-1]
            tax_adjustment = (target_tax_rate - previous_tax_rate) * self.parameters['tax_adjustment_sensitivity']
            new_tax_rate = previous_tax_rate + tax_adjustment
        else:
            new_tax_rate = target_tax_rate
        
        results['tax_rate'][t] = min(new_tax_rate, max_tax_rate)
        
        # Calculate budget balance
        tax_revenue = current_gdp * results['tax_rate'][t]
        results['budget_balance'][t] = tax_revenue - total_spending
    
    def _calculate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate summary statistics for the simulation."""
        unemployment_values = np.array(results['unemployment_rate'])
        gdp_values = np.array(results['gdp'])
        ubi_costs = np.array(results['ubi_cost'])
        budget_balances = np.array(results['budget_balance'])
        
        # Find UBI trigger point
        ubi_trigger_year = None
        if any(results['ubi_activated']):
            ubi_trigger_year = next(i for i, activated in enumerate(results['ubi_activated']) if activated)
        
        return {
            'final_unemployment_rate': float(unemployment_values[-1]),
            'peak_unemployment_rate': float(np.max(unemployment_values)),
            'final_gdp': float(gdp_values[-1]),
            'total_gdp_growth': float((gdp_values[-1] - gdp_values[0]) / gdp_values[0] * 100),
            'avg_annual_gdp_growth': float(np.mean(np.diff(gdp_values) / gdp_values[:-1] * 100)),
            'ubi_trigger_year': ubi_trigger_year,
            'total_ubi_cost': float(np.sum(ubi_costs)),
            'avg_annual_ubi_cost': float(np.mean(ubi_costs[ubi_costs > 0]) if np.any(ubi_costs > 0) else 0),
            'final_budget_balance': float(budget_balances[-1]),
            'total_budget_deficit': float(np.sum(budget_balances[budget_balances < 0])),
            'years_in_deficit': int(np.sum(budget_balances < 0)),
            'final_tax_rate': float(results['tax_rate'][-1]),
            'ubi_years_active': int(np.sum(results['ubi_activated'])),
            'productivity_vs_employment_tradeoff': float(
                (results['productivity_growth'][-1] - results['productivity_growth'][0]) / 
                (results['employment_rate'][0] - results['employment_rate'][-1])
            ) if results['employment_rate'][0] != results['employment_rate'][-1] else 0.0
        }
    
    def _compare_scenarios(self, with_ubi: Dict[str, Any], without_ubi: Dict[str, Any]) -> Dict[str, Any]:
        """Compare scenarios with and without UBI."""
        return {
            'gdp_difference': {
                'final': float(with_ubi['summary']['final_gdp'] - without_ubi['summary']['final_gdp']),
                'total_growth_difference': float(
                    with_ubi['summary']['total_gdp_growth'] - without_ubi['summary']['total_gdp_growth']
                )
            },
            'unemployment_difference': {
                'final': float(
                    with_ubi['summary']['final_unemployment_rate'] - without_ubi['summary']['final_unemployment_rate']
                ),
                'peak': float(
                    with_ubi['summary']['peak_unemployment_rate'] - without_ubi['summary']['peak_unemployment_rate']
                )
            },
            'fiscal_impact': {
                'ubi_cost': float(with_ubi['summary']['total_ubi_cost']),
                'budget_balance_difference': float(
                    with_ubi['summary']['final_budget_balance'] - without_ubi['summary']['final_budget_balance']
                ),
                'tax_rate_difference': float(
                    with_ubi['summary']['final_tax_rate'] - without_ubi['summary']['final_tax_rate']
                )
            },
            'key_insights': [
                f"UBI triggered in year {with_ubi['summary']['ubi_trigger_year']}" if with_ubi['summary']['ubi_trigger_year'] else "UBI never triggered",
                f"Total UBI cost: ${with_ubi['summary']['total_ubi_cost']/1e12:.1f} trillion over 30 years",
                f"GDP impact: {'Positive' if with_ubi['summary']['final_gdp'] > without_ubi['summary']['final_gdp'] else 'Negative'} ${abs(with_ubi['summary']['final_gdp'] - without_ubi['summary']['final_gdp'])/1e12:.1f}T difference",
                f"Final tax rates: {with_ubi['summary']['final_tax_rate']:.1%} (with UBI) vs {without_ubi['summary']['final_tax_rate']:.1%} (without)"
            ]
        } 