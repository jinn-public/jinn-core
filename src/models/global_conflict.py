"""
Global Conflict Model

Economic model for simulating the comprehensive effects of large-scale global conflicts
on GDP, trade, public debt, inflation, human capital, infrastructure, and social stability.
"""

import numpy as np
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class GlobalConflictShock:
    """Configuration for a global conflict scenario."""
    military_spending_jump: float  # Annual military spending increase as % of GDP (e.g., 0.05 for 5%)
    global_trade_disruption: float  # Fraction of trade disrupted (e.g., 0.4 for 40%)
    conflict_duration_years: int   # Duration of conflict in years
    inflation_surge_rate: float    # Initial inflation spike rate (e.g., 0.1 for 10%)
    human_capital_loss: float      # Annual workforce reduction rate (e.g., 0.05 for 5%)
    infrastructure_destruction: float  # Annual infrastructure destruction rate (e.g., 0.1 for 10%)
    start_period: int = 0          # When the conflict begins


def simulate_global_conflict(initial_gdp: float, military_spending_jump: float,
                           global_trade_disruption: float, conflict_duration_years: int,
                           inflation_surge_rate: float, human_capital_loss: float,
                           infrastructure_destruction: float) -> Dict[str, Any]:
    """
    Simple, interpretable function to simulate the effect of global conflict.
    
    Args:
        initial_gdp: Initial global GDP (USD)
        military_spending_jump: Annual military spending increase as % of GDP
        global_trade_disruption: Fraction of global trade disrupted (0-1)
        conflict_duration_years: Duration of conflict in years
        inflation_surge_rate: Initial inflation spike rate
        human_capital_loss: Annual workforce reduction rate
        infrastructure_destruction: Annual infrastructure destruction rate
        
    Returns:
        Dict containing:
        - total_military_spending: Cumulative military spending increase
        - gdp_impact: Total GDP impact (negative)
        - trade_loss: Total trade volume lost
        - inflation_peak: Peak inflation rate
        - workforce_reduction: Total workforce lost
        - infrastructure_loss: Total infrastructure destroyed
        - debt_increase: Public debt increase as % of GDP
        - social_stability_index: Social stability score (0-1, lower is worse)
    """
    # Calculate cumulative military spending
    annual_military_cost = initial_gdp * military_spending_jump
    total_military_spending = annual_military_cost * conflict_duration_years
    
    # GDP impact calculation (compound negative effects)
    # Trade disruption impact: -0.5% GDP per 1% trade lost
    trade_gdp_impact = -global_trade_disruption * 0.5
    
    # Human capital impact: -1.2% GDP per 1% workforce lost (compound over years)
    workforce_gdp_impact = -(1 - (1 - human_capital_loss) ** conflict_duration_years) * 1.2
    
    # Infrastructure impact: -0.8% GDP per 1% infrastructure lost (compound over years)
    infrastructure_gdp_impact = -(1 - (1 - infrastructure_destruction) ** conflict_duration_years) * 0.8
    
    # Military spending drag: -0.3% GDP per 1% of GDP spent on military
    military_gdp_drag = -military_spending_jump * 0.3 * conflict_duration_years
    
    # Total GDP impact
    gdp_impact = trade_gdp_impact + workforce_gdp_impact + infrastructure_gdp_impact + military_gdp_drag
    
    # Trade loss calculation
    baseline_trade = initial_gdp * 0.3  # Assume trade is 30% of GDP
    trade_loss = baseline_trade * global_trade_disruption * conflict_duration_years
    
    # Inflation calculation (peaks early, then moderates)
    inflation_peak = inflation_surge_rate * (1 + global_trade_disruption * 0.5)
    
    # Workforce and infrastructure cumulative losses
    workforce_reduction = 1 - (1 - human_capital_loss) ** conflict_duration_years
    infrastructure_loss = 1 - (1 - infrastructure_destruction) ** conflict_duration_years
    
    # Debt increase (military spending + economic support)
    debt_increase = (military_spending_jump * conflict_duration_years + abs(gdp_impact) * 0.3) * 100
    
    # Social stability index (decreases with conflict intensity and duration)
    conflict_intensity = (military_spending_jump + global_trade_disruption + 
                         human_capital_loss + infrastructure_destruction) / 4
    social_stability_index = max(0.1, 1 - (conflict_intensity * conflict_duration_years * 0.4))
    
    return {
        'total_military_spending': total_military_spending,
        'gdp_impact': gdp_impact * 100,  # Convert to percentage
        'trade_loss': trade_loss,
        'inflation_peak': inflation_peak * 100,  # Convert to percentage
        'workforce_reduction': workforce_reduction * 100,  # Convert to percentage
        'infrastructure_loss': infrastructure_loss * 100,  # Convert to percentage
        'debt_increase': debt_increase,
        'social_stability_index': social_stability_index
    }


class GlobalConflictModel:
    """
    Global Conflict Model
    
    Simulates the comprehensive economic effects of large-scale global conflicts including:
    - Military spending escalation
    - Global trade disruption
    - Human capital destruction
    - Infrastructure damage
    - Inflation and supply chain disruption
    - Public debt dynamics
    - Social stability deterioration
    """
    
    def __init__(self, parameters: Dict[str, Any]):
        """
        Initialize the Global Conflict Model.
        
        Args:
            parameters: Model calibration parameters
        """
        self.parameters = self._validate_parameters(parameters)
        logger.info("Global Conflict Model initialized")
    
    def _validate_parameters(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and set default parameters."""
        defaults = {
            # Economic baseline parameters
            'initial_gdp': 100000000000000.0,     # $100 trillion global GDP
            'baseline_gdp_growth': 0.03,          # 3% baseline global GDP growth
            'baseline_inflation': 0.02,           # 2% baseline inflation
            'baseline_military_spending': 0.02,   # 2% of GDP baseline military spending
            'baseline_trade_ratio': 0.3,          # Trade is 30% of GDP
            'baseline_debt_ratio': 0.7,           # 70% global debt-to-GDP ratio
            
            # Conflict impact parameters
            'trade_gdp_multiplier': 0.5,          # GDP impact per unit of trade disruption
            'human_capital_gdp_multiplier': 1.2,  # GDP impact per unit of workforce loss
            'infrastructure_gdp_multiplier': 0.8, # GDP impact per unit of infrastructure loss
            'military_gdp_drag': 0.3,             # GDP drag per unit of military spending
            
            # Dynamic parameters
            'inflation_trade_sensitivity': 0.5,   # Inflation response to trade disruption
            'social_stability_threshold': 0.3,    # Threshold for social unrest
            'reconstruction_rate': 0.1,           # Annual reconstruction rate post-conflict
            'trade_recovery_rate': 0.2,           # Annual trade recovery rate
            'workforce_recovery_rate': 0.05,      # Annual workforce recovery rate
            
            # Feedback effects
            'debt_growth_drag': 0.01,             # GDP drag per 10pp debt increase
            'social_unrest_gdp_impact': 0.02,     # GDP impact of social instability
            'refugee_cost_ratio': 0.01,           # Refugee costs as % of GDP per % population displaced
            
            # Model parameters
            'periods': 20,                        # Number of simulation periods (years)
            'conflict_escalation_rate': 1.1,     # Annual escalation factor
        }
        
        # Merge with provided parameters
        for key, default_value in defaults.items():
            if key not in params:
                params[key] = default_value
        
        return params
    
    def simulate(self, simulation_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the global conflict simulation.
        
        Args:
            simulation_config: Simulation configuration including conflict details
            
        Returns:
            Dictionary containing simulation results
        """
        periods = self.parameters['periods']
        
        # Parse conflict configuration
        conflict_config = simulation_config.get('conflict', {})
        conflict = GlobalConflictShock(
            military_spending_jump=conflict_config.get('military_spending_jump', 0.05),
            global_trade_disruption=conflict_config.get('global_trade_disruption', 0.4),
            conflict_duration_years=conflict_config.get('conflict_duration_years', 5),
            inflation_surge_rate=conflict_config.get('inflation_surge_rate', 0.1),
            human_capital_loss=conflict_config.get('human_capital_loss', 0.05),
            infrastructure_destruction=conflict_config.get('infrastructure_destruction', 0.1),
            start_period=conflict_config.get('start_period', 0)
        )
        
        logger.info(f"Simulating global conflict: {conflict.military_spending_jump*100:.1f}% GDP military increase, "
                   f"{conflict.global_trade_disruption*100:.1f}% trade disruption, "
                   f"{conflict.conflict_duration_years} years duration")
        
        # Initialize time series
        results = {
            'periods': list(range(periods)),
            'conflict_active': np.zeros(periods, dtype=bool),
            'military_spending_percent': np.full(periods, self.parameters['baseline_military_spending']),
            'gdp': np.full(periods, self.parameters['initial_gdp']),
            'gdp_growth': np.full(periods, self.parameters['baseline_gdp_growth']),
            'trade_volume': np.full(periods, self.parameters['initial_gdp'] * self.parameters['baseline_trade_ratio']),
            'inflation_rate': np.full(periods, self.parameters['baseline_inflation']),
            'workforce_level': np.ones(periods),  # Normalized to 1.0
            'infrastructure_level': np.ones(periods),  # Normalized to 1.0
            'debt_ratio': np.full(periods, self.parameters['baseline_debt_ratio']),
            'social_stability_index': np.ones(periods),  # 1.0 = stable
            'refugee_population': np.zeros(periods),
            'reconstruction_spending': np.zeros(periods),
        }
        
        # Apply conflict effects
        for t in range(periods):
            # Determine if conflict is active
            conflict_active = (conflict.start_period <= t < 
                             conflict.start_period + conflict.conflict_duration_years)
            results['conflict_active'][t] = conflict_active
            
            if conflict_active:
                # Apply conflict effects
                self._apply_conflict_effects(results, t, conflict)
            else:
                # Apply post-conflict recovery
                self._apply_recovery_effects(results, t, conflict)
            
            # Update economic indicators
            self._update_economic_indicators(results, t)
            
            # Calculate social stability
            self._update_social_stability(results, t)
        
        # Convert numpy arrays to lists for JSON serialization
        for key, value in results.items():
            if isinstance(value, np.ndarray):
                if value.dtype == bool:
                    results[key] = value.astype(int).tolist()
                else:
                    results[key] = value.tolist()
        
        # Add summary statistics
        results['summary'] = self._calculate_summary(results, conflict)
        
        logger.info("Global conflict simulation completed")
        return results
    
    def _apply_conflict_effects(self, results: Dict[str, Any], period: int, conflict: GlobalConflictShock):
        """Apply the effects of active conflict."""
        conflict_year = period - conflict.start_period
        escalation_factor = self.parameters['conflict_escalation_rate'] ** conflict_year
        
        if period == 0:
            return
        
        # Military spending increase
        base_military = self.parameters['baseline_military_spending']
        military_increase = conflict.military_spending_jump * escalation_factor
        results['military_spending_percent'][period] = base_military + military_increase
        
        # Trade disruption
        baseline_trade = self.parameters['initial_gdp'] * self.parameters['baseline_trade_ratio']
        trade_disruption = conflict.global_trade_disruption * escalation_factor
        results['trade_volume'][period] = baseline_trade * (1 - min(trade_disruption, 0.9))
        
        # Human capital destruction
        prev_workforce = results['workforce_level'][period - 1]
        workforce_loss = conflict.human_capital_loss * escalation_factor
        results['workforce_level'][period] = prev_workforce * (1 - min(workforce_loss, 0.2))
        
        # Infrastructure destruction
        prev_infrastructure = results['infrastructure_level'][period - 1]
        infrastructure_loss = conflict.infrastructure_destruction * escalation_factor
        results['infrastructure_level'][period] = prev_infrastructure * (1 - min(infrastructure_loss, 0.3))
        
        # Inflation surge
        baseline_inflation = self.parameters['baseline_inflation']
        trade_inflation_impact = trade_disruption * self.parameters['inflation_trade_sensitivity']
        supply_chain_impact = (workforce_loss + infrastructure_loss) * 0.3
        results['inflation_rate'][period] = baseline_inflation + conflict.inflation_surge_rate + trade_inflation_impact + supply_chain_impact
        
        # Refugee population (cumulative)
        new_refugees = (workforce_loss + infrastructure_loss) * 0.1  # 10% become refugees
        if period > 0:
            results['refugee_population'][period] = results['refugee_population'][period - 1] + new_refugees
        else:
            results['refugee_population'][period] = new_refugees
    
    def _apply_recovery_effects(self, results: Dict[str, Any], period: int, conflict: GlobalConflictShock):
        """Apply post-conflict recovery effects."""
        if period == 0:
            return
        
        # Check if we're in post-conflict period
        post_conflict_period = period - (conflict.start_period + conflict.conflict_duration_years)
        if post_conflict_period < 0:
            return
        
        # Military spending normalization
        base_military = self.parameters['baseline_military_spending']
        current_military = results['military_spending_percent'][period - 1]
        military_reduction = (current_military - base_military) * 0.1  # 10% annual reduction
        results['military_spending_percent'][period] = max(base_military, current_military - military_reduction)
        
        # Trade recovery
        baseline_trade = self.parameters['initial_gdp'] * self.parameters['baseline_trade_ratio']
        current_trade = results['trade_volume'][period - 1]
        trade_recovery = (baseline_trade - current_trade) * self.parameters['trade_recovery_rate']
        results['trade_volume'][period] = min(baseline_trade, current_trade + trade_recovery)
        
        # Workforce recovery
        current_workforce = results['workforce_level'][period - 1]
        workforce_recovery = (1.0 - current_workforce) * self.parameters['workforce_recovery_rate']
        results['workforce_level'][period] = min(1.0, current_workforce + workforce_recovery)
        
        # Infrastructure reconstruction
        current_infrastructure = results['infrastructure_level'][period - 1]
        reconstruction_rate = self.parameters['reconstruction_rate']
        infrastructure_recovery = (1.0 - current_infrastructure) * reconstruction_rate
        results['infrastructure_level'][period] = min(1.0, current_infrastructure + infrastructure_recovery)
        
        # Reconstruction spending
        reconstruction_need = 1.0 - current_infrastructure
        results['reconstruction_spending'][period] = reconstruction_need * self.parameters['initial_gdp'] * 0.05
        
        # Inflation normalization
        baseline_inflation = self.parameters['baseline_inflation']
        current_inflation = results['inflation_rate'][period - 1]
        inflation_reduction = (current_inflation - baseline_inflation) * 0.2  # 20% annual reduction
        results['inflation_rate'][period] = max(baseline_inflation, current_inflation - inflation_reduction)
    
    def _update_economic_indicators(self, results: Dict[str, Any], period: int):
        """Update GDP, growth, and debt based on conflict effects."""
        if period == 0:
            results['gdp'][period] = self.parameters['initial_gdp']
            results['gdp_growth'][period] = self.parameters['baseline_gdp_growth']
            results['debt_ratio'][period] = self.parameters['baseline_debt_ratio']
            return
        
        # Calculate GDP impact
        baseline_growth = self.parameters['baseline_gdp_growth']
        
        # Trade impact
        baseline_trade = self.parameters['initial_gdp'] * self.parameters['baseline_trade_ratio']
        trade_loss = (baseline_trade - results['trade_volume'][period]) / self.parameters['initial_gdp']
        trade_impact = -trade_loss * self.parameters['trade_gdp_multiplier']
        
        # Human capital impact
        workforce_loss = 1.0 - results['workforce_level'][period]
        human_capital_impact = -workforce_loss * self.parameters['human_capital_gdp_multiplier']
        
        # Infrastructure impact
        infrastructure_loss = 1.0 - results['infrastructure_level'][period]
        infrastructure_impact = -infrastructure_loss * self.parameters['infrastructure_gdp_multiplier']
        
        # Military spending drag
        excess_military = results['military_spending_percent'][period] - self.parameters['baseline_military_spending']
        military_impact = -excess_military * self.parameters['military_gdp_drag']
        
        # Social stability impact
        stability_loss = 1.0 - results['social_stability_index'][period - 1] if period > 0 else 0
        social_impact = -stability_loss * self.parameters['social_unrest_gdp_impact']
        
        # Debt drag
        excess_debt = results['debt_ratio'][period - 1] - self.parameters['baseline_debt_ratio']
        debt_drag = -max(0, excess_debt) * self.parameters['debt_growth_drag']
        
        # Total growth
        total_growth = (baseline_growth + trade_impact + human_capital_impact + 
                       infrastructure_impact + military_impact + social_impact + debt_drag)
        results['gdp_growth'][period] = max(-0.2, total_growth)  # Floor at -20%
        
        # Update GDP
        results['gdp'][period] = results['gdp'][period - 1] * (1 + results['gdp_growth'][period])
        
        # Update debt ratio
        military_spending = results['military_spending_percent'][period] * results['gdp'][period]
        reconstruction_spending = results['reconstruction_spending'][period]
        refugee_costs = results['refugee_population'][period] * self.parameters['initial_gdp'] * self.parameters['refugee_cost_ratio']
        
        total_spending = military_spending + reconstruction_spending + refugee_costs
        baseline_spending = self.parameters['baseline_military_spending'] * results['gdp'][period]
        excess_spending = total_spending - baseline_spending
        
        # Debt increases with excess spending, decreases with GDP growth
        debt_change = excess_spending / results['gdp'][period] - results['gdp_growth'][period] * 0.5
        results['debt_ratio'][period] = max(0, results['debt_ratio'][period - 1] + debt_change)
    
    def _update_social_stability(self, results: Dict[str, Any], period: int):
        """Update social stability index based on conflict effects."""
        if period == 0:
            results['social_stability_index'][period] = 1.0
            return
        
        # Base stability
        base_stability = 1.0
        
        # Economic stress factors
        gdp_decline = max(0, -results['gdp_growth'][period])
        inflation_stress = max(0, results['inflation_rate'][period] - self.parameters['baseline_inflation'])
        unemployment_stress = 1.0 - results['workforce_level'][period]
        
        # Conflict stress
        conflict_stress = 0
        if results['conflict_active'][period]:
            military_burden = results['military_spending_percent'][period] - self.parameters['baseline_military_spending']
            refugee_burden = results['refugee_population'][period]
            conflict_stress = (military_burden + refugee_burden) * 0.5
        
        # Total stress
        total_stress = gdp_decline + inflation_stress + unemployment_stress + conflict_stress
        
        # Stability decay
        stability_decay = min(0.3, total_stress * 0.2)  # Max 30% annual decline
        
        # Recovery factor (gradual improvement when stress is low)
        if total_stress < 0.1 and period > 0:
            recovery_factor = (1.0 - results['social_stability_index'][period - 1]) * 0.1
        else:
            recovery_factor = 0
        
        new_stability = results['social_stability_index'][period - 1] - stability_decay + recovery_factor
        results['social_stability_index'][period] = max(0.1, min(1.0, new_stability))
    
    def _calculate_summary(self, results: Dict[str, Any], conflict: GlobalConflictShock) -> Dict[str, Any]:
        """Calculate summary statistics for the simulation."""
        gdp_values = np.array(results['gdp'])
        growth_values = np.array(results['gdp_growth'])
        trade_values = np.array(results['trade_volume'])
        inflation_values = np.array(results['inflation_rate'])
        debt_values = np.array(results['debt_ratio'])
        stability_values = np.array(results['social_stability_index'])
        workforce_values = np.array(results['workforce_level'])
        infrastructure_values = np.array(results['infrastructure_level'])
        
        # Use simple function for final assessment
        final_assessment = simulate_global_conflict(
            initial_gdp=self.parameters['initial_gdp'],
            military_spending_jump=conflict.military_spending_jump,
            global_trade_disruption=conflict.global_trade_disruption,
            conflict_duration_years=conflict.conflict_duration_years,
            inflation_surge_rate=conflict.inflation_surge_rate,
            human_capital_loss=conflict.human_capital_loss,
            infrastructure_destruction=conflict.infrastructure_destruction
        )
        
        return {
            'total_gdp_loss': float((gdp_values[0] - np.min(gdp_values)) / gdp_values[0] * 100),
            'peak_gdp_decline': float(np.min(growth_values) * 100),
            'final_gdp_level': float(gdp_values[-1] / gdp_values[0] * 100),
            'peak_inflation': float(np.max(inflation_values) * 100),
            'max_debt_ratio': float(np.max(debt_values) * 100),
            'min_social_stability': float(np.min(stability_values)),
            'total_workforce_loss': float((1.0 - np.min(workforce_values)) * 100),
            'total_infrastructure_loss': float((1.0 - np.min(infrastructure_values)) * 100),
            'trade_volume_loss': float((trade_values[0] - np.min(trade_values)) / trade_values[0] * 100),
            'conflict_severity': 'Catastrophic' if final_assessment['gdp_impact'] < -20 else 'Severe' if final_assessment['gdp_impact'] < -10 else 'Moderate',
            'recovery_years': int(np.argmax(gdp_values[conflict.start_period + conflict.conflict_duration_years:] >= gdp_values[0] * 0.95)) if len(gdp_values) > conflict.start_period + conflict.conflict_duration_years else periods,
            'peak_refugee_population': float(np.max(results['refugee_population']) * 100),
            'total_reconstruction_cost': float(np.sum(results['reconstruction_spending']) / 1e12),  # In trillions
            'final_assessment': final_assessment
        } 