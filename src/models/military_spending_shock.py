"""
Military Spending Shock Model

Economic model for simulating the effects of military spending changes
on macroeconomic indicators including social budgets, public debt, and GDP growth.
"""

import numpy as np
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class MilitarySpendingShock:
    """Configuration for a military spending shock."""
    spending_increase: float  # Increase in military spending as % of GDP (e.g., 0.02 for 2%)
    duration: int            # Number of periods the increase persists
    start_period: int = 0    # When the spending increase begins
    fiscal_policy: str = "neutral"  # "neutral", "stimulus", or "austerity"


def simulate_military_spending_shock(initial_gdp: float, military_spending_percent: float,
                                   military_spending_increase: float, debt_ratio: float,
                                   fiscal_policy: str = "neutral") -> Dict[str, Any]:
    """
    Simple, interpretable function to simulate the effect of military spending changes.
    
    Args:
        initial_gdp: Initial GDP (USD)
        military_spending_percent: Current military spending as % of GDP (e.g., 0.03 for 3%)
        military_spending_increase: Increase in military spending as % of GDP (e.g., 0.02 for 2%)
        debt_ratio: Initial public debt as % of GDP (e.g., 0.6 for 60%)
        fiscal_policy: Fiscal policy stance ("neutral", "stimulus", "austerity")
        
    Returns:
        Dict containing:
        - new_military_spending_percent: Updated military spending as % of GDP
        - military_spending_amount: Absolute military spending amount (USD)
        - social_budget_impact: Change in social spending (% of GDP)
        - new_debt_ratio: Updated debt-to-GDP ratio
        - gdp_growth_impact: Impact on GDP growth rate (percentage points)
        - fiscal_multiplier: Applied fiscal multiplier based on policy
    """
    # Calculate new military spending
    new_military_spending_percent = military_spending_percent + military_spending_increase
    military_spending_amount = initial_gdp * new_military_spending_percent
    
    # Social budget impact (crowding out effect)
    # Military spending typically crowds out social spending at 60% rate
    social_budget_impact = -military_spending_increase * 0.6
    
    # Debt impact - military spending increases debt unless offset by other measures
    debt_increase = military_spending_increase
    if fiscal_policy == "austerity":
        # Austerity reduces debt impact by cutting other spending
        debt_increase *= 0.4
    elif fiscal_policy == "stimulus":
        # Stimulus increases debt impact with additional spending
        debt_increase *= 1.3
    
    new_debt_ratio = debt_ratio + debt_increase
    
    # GDP growth impact based on fiscal multiplier
    fiscal_multipliers = {
        "neutral": 0.8,    # Military spending has lower multiplier than social spending
        "stimulus": 1.2,   # Combined with other stimulus measures
        "austerity": 0.5   # Reduced effectiveness due to offsetting cuts
    }
    
    fiscal_multiplier = fiscal_multipliers.get(fiscal_policy, 0.8)
    
    # GDP growth impact (percentage points)
    # Military spending has positive but limited GDP impact
    gdp_growth_impact = military_spending_increase * fiscal_multiplier
    
    return {
        'new_military_spending_percent': new_military_spending_percent * 100,  # Convert to percentage
        'military_spending_amount': military_spending_amount,
        'social_budget_impact': social_budget_impact * 100,  # Convert to percentage
        'new_debt_ratio': new_debt_ratio * 100,  # Convert to percentage
        'gdp_growth_impact': gdp_growth_impact * 100,  # Convert to percentage points
        'fiscal_multiplier': fiscal_multiplier
    }


class MilitarySpendingShockModel:
    """
    Military Spending Shock Model
    
    Simulates the macroeconomic effects of military spending changes including:
    - GDP growth impacts
    - Social budget crowding out
    - Public debt dynamics
    - Fiscal policy interactions
    - Economic multiplier effects
    """
    
    def __init__(self, parameters: Dict[str, Any]):
        """
        Initialize the Military Spending Shock Model.
        
        Args:
            parameters: Model calibration parameters
        """
        self.parameters = self._validate_parameters(parameters)
        logger.info("Military Spending Shock Model initialized")
    
    def _validate_parameters(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and set default parameters."""
        defaults = {
            # Economic baseline parameters
            'initial_gdp': 25000000000000.0,       # $25 trillion initial GDP
            'baseline_gdp_growth': 0.02,           # 2% baseline GDP growth rate
            'military_spending_percent': 0.03,     # 3% of GDP baseline military spending
            'social_spending_percent': 0.15,       # 15% of GDP baseline social spending
            'debt_ratio': 0.6,                     # 60% debt-to-GDP ratio
            
            # Policy parameters
            'fiscal_policy': 'neutral',            # Default fiscal policy stance
            'crowding_out_rate': 0.6,             # Rate at which military spending crowds out social
            'debt_sustainability_threshold': 0.9,  # 90% debt-to-GDP warning threshold
            
            # Economic multipliers
            'military_multiplier_neutral': 0.8,    # Military spending multiplier (neutral policy)
            'military_multiplier_stimulus': 1.2,   # Military spending multiplier (stimulus policy)
            'military_multiplier_austerity': 0.5,  # Military spending multiplier (austerity policy)
            'social_multiplier': 1.4,             # Social spending multiplier (higher than military)
            
            # Dynamic parameters
            'multiplier_decay': 0.9,               # How quickly multiplier effects fade
            'debt_feedback_threshold': 0.8,       # Debt level where growth starts to suffer
            'debt_drag_coefficient': 0.02,        # GDP drag per percentage point of excess debt
            
            # Model parameters
            'periods': 20,                         # Number of simulation periods
            'shock_persistence': 0.95,            # How persistent spending changes are
        }
        
        # Merge with provided parameters
        for key, default_value in defaults.items():
            if key not in params:
                params[key] = default_value
        
        return params
    
    def simulate(self, simulation_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the military spending shock simulation.
        
        Args:
            simulation_config: Simulation configuration including shock details
            
        Returns:
            Dictionary containing simulation results
        """
        periods = self.parameters['periods']
        
        # Parse shock configuration
        shock_config = simulation_config.get('shock', {})
        shock = MilitarySpendingShock(
            spending_increase=shock_config.get('spending_increase', 0.02),  # 2% of GDP increase
            duration=shock_config.get('duration', 10),
            start_period=shock_config.get('start_period', 0),
            fiscal_policy=shock_config.get('fiscal_policy', self.parameters['fiscal_policy'])
        )
        
        logger.info(f"Simulating military spending increase of {shock.spending_increase*100:.1f}% of GDP "
                   f"for {shock.duration} periods starting at period {shock.start_period} "
                   f"under {shock.fiscal_policy} fiscal policy")
        
        # Initialize time series
        results = {
            'periods': list(range(periods)),
            'military_spending_shock': np.zeros(periods),
            'military_spending_percent': np.full(periods, self.parameters['military_spending_percent']),
            'social_spending_percent': np.full(periods, self.parameters['social_spending_percent']),
            'gdp': np.full(periods, self.parameters['initial_gdp']),
            'gdp_growth': np.full(periods, self.parameters['baseline_gdp_growth']),
            'debt_ratio': np.full(periods, self.parameters['debt_ratio']),
            'fiscal_balance': np.zeros(periods),
            'economic_multiplier': np.ones(periods),
            'debt_sustainability_risk': np.zeros(periods),
        }
        
        # Apply military spending shock
        for t in range(periods):
            # Determine shock magnitude
            shock_magnitude = self._calculate_shock_magnitude(t, shock)
            results['military_spending_shock'][t] = shock_magnitude
            
            # Update military spending
            if t == 0:
                results['military_spending_percent'][t] = self.parameters['military_spending_percent']
            else:
                # Apply shock with persistence
                base_spending = self.parameters['military_spending_percent']
                results['military_spending_percent'][t] = base_spending + shock_magnitude
            
            # Calculate economic impacts
            self._update_economic_indicators(results, t, shock_magnitude, shock.fiscal_policy)
            
            # Update GDP and growth
            self._update_gdp_dynamics(results, t)
            
            # Calculate fiscal balance and debt dynamics
            self._update_fiscal_dynamics(results, t)
            
            # Assess debt sustainability
            self._assess_debt_sustainability(results, t)
        
        # Convert numpy arrays to lists for JSON serialization
        for key, value in results.items():
            if isinstance(value, np.ndarray):
                results[key] = value.tolist()
        
        # Add summary statistics
        results['summary'] = self._calculate_summary(results, shock)
        
        logger.info("Military spending shock simulation completed")
        return results
    
    def _calculate_shock_magnitude(self, period: int, shock: MilitarySpendingShock) -> float:
        """Calculate the magnitude of the military spending shock at a given period."""
        if period < shock.start_period:
            return 0.0
        
        shock_period = period - shock.start_period
        
        if shock_period < shock.duration:
            # Full shock during the shock duration
            return shock.spending_increase
        else:
            # Gradual decay after shock period
            decay_period = shock_period - shock.duration
            persistence = self.parameters['shock_persistence']
            return shock.spending_increase * (persistence ** decay_period)
    
    def _update_economic_indicators(self, results: Dict[str, Any], period: int, 
                                  shock_magnitude: float, fiscal_policy: str):
        """Update economic indicators based on military spending shock."""
        if period == 0:
            results['economic_multiplier'][period] = 1.0
            return
        
        # Calculate fiscal multiplier based on policy
        if fiscal_policy == "stimulus":
            multiplier = self.parameters['military_multiplier_stimulus']
        elif fiscal_policy == "austerity":
            multiplier = self.parameters['military_multiplier_austerity']
        else:
            multiplier = self.parameters['military_multiplier_neutral']
        
        # Apply multiplier decay
        decay = self.parameters['multiplier_decay']
        results['economic_multiplier'][period] = multiplier * (decay ** period)
        
        # Social spending crowding out
        if shock_magnitude > 0:
            crowding_out = shock_magnitude * self.parameters['crowding_out_rate']
            if fiscal_policy == "austerity":
                # More severe crowding out under austerity
                crowding_out *= 1.5
            elif fiscal_policy == "stimulus":
                # Less crowding out under stimulus (deficit financing)
                crowding_out *= 0.3
            
            baseline_social = self.parameters['social_spending_percent']
            results['social_spending_percent'][period] = max(0, baseline_social - crowding_out)
    
    def _update_gdp_dynamics(self, results: Dict[str, Any], period: int):
        """Update GDP and growth based on spending changes and debt dynamics."""
        if period == 0:
            results['gdp'][period] = self.parameters['initial_gdp']
            results['gdp_growth'][period] = self.parameters['baseline_gdp_growth']
            return
        
        # Base GDP growth
        baseline_growth = self.parameters['baseline_gdp_growth']
        
        # Military spending impact
        military_shock = results['military_spending_shock'][period]
        multiplier = results['economic_multiplier'][period]
        military_impact = military_shock * multiplier
        
        # Social spending impact (negative due to crowding out)
        social_baseline = self.parameters['social_spending_percent']
        social_current = results['social_spending_percent'][period]
        social_change = social_current - social_baseline
        social_impact = social_change * self.parameters['social_multiplier']
        
        # Debt drag effect
        debt_ratio = results['debt_ratio'][period - 1]
        debt_threshold = self.parameters['debt_feedback_threshold']
        if debt_ratio > debt_threshold:
            excess_debt = debt_ratio - debt_threshold
            debt_drag = excess_debt * self.parameters['debt_drag_coefficient']
        else:
            debt_drag = 0
        
        # Total growth impact
        total_growth = baseline_growth + military_impact + social_impact - debt_drag
        results['gdp_growth'][period] = max(-0.1, total_growth)  # Floor at -10% growth
        
        # Update GDP level
        growth_rate = results['gdp_growth'][period]
        results['gdp'][period] = results['gdp'][period - 1] * (1 + growth_rate)
    
    def _update_fiscal_dynamics(self, results: Dict[str, Any], period: int):
        """Update fiscal balance and debt dynamics."""
        if period == 0:
            results['fiscal_balance'][period] = 0
            results['debt_ratio'][period] = self.parameters['debt_ratio']
            return
        
        # Calculate fiscal balance as % of GDP
        military_spending = results['military_spending_percent'][period]
        social_spending = results['social_spending_percent'][period]
        baseline_military = self.parameters['military_spending_percent']
        baseline_social = self.parameters['social_spending_percent']
        
        # Fiscal balance change (negative = deficit increase)
        spending_change = (military_spending - baseline_military) + (social_spending - baseline_social)
        results['fiscal_balance'][period] = -spending_change  # Negative for deficit
        
        # Update debt ratio
        prev_debt_ratio = results['debt_ratio'][period - 1]
        gdp_growth = results['gdp_growth'][period]
        fiscal_balance = results['fiscal_balance'][period]
        
        # Debt dynamics: debt/GDP = (debt + deficit) / (GDP * (1 + growth))
        # Simplified: new_ratio = old_ratio * (1 + deficit_rate) / (1 + growth_rate)
        deficit_impact = -fiscal_balance  # Convert to positive for deficit
        new_debt_ratio = (prev_debt_ratio + deficit_impact) / (1 + gdp_growth)
        results['debt_ratio'][period] = max(0, new_debt_ratio)
    
    def _assess_debt_sustainability(self, results: Dict[str, Any], period: int):
        """Assess debt sustainability risk."""
        debt_ratio = results['debt_ratio'][period]
        threshold = self.parameters['debt_sustainability_threshold']
        
        if debt_ratio > threshold:
            # Risk increases exponentially beyond threshold
            excess_debt = debt_ratio - threshold
            risk_score = min(1.0, excess_debt / 0.3)  # Max risk at 120% debt/GDP
        else:
            risk_score = 0.0
        
        results['debt_sustainability_risk'][period] = risk_score
    
    def _calculate_summary(self, results: Dict[str, Any], shock: MilitarySpendingShock) -> Dict[str, Any]:
        """Calculate summary statistics for the simulation."""
        military_values = np.array(results['military_spending_percent'])
        social_values = np.array(results['social_spending_percent'])
        gdp_values = np.array(results['gdp'])
        growth_values = np.array(results['gdp_growth'])
        debt_values = np.array(results['debt_ratio'])
        risk_values = np.array(results['debt_sustainability_risk'])
        
        # Use simple function for final assessment
        final_assessment = simulate_military_spending_shock(
            initial_gdp=self.parameters['initial_gdp'],
            military_spending_percent=self.parameters['military_spending_percent'],
            military_spending_increase=shock.spending_increase,
            debt_ratio=self.parameters['debt_ratio'],
            fiscal_policy=shock.fiscal_policy
        )
        
        return {
            'peak_military_spending': float(np.max(military_values)),
            'min_social_spending': float(np.min(social_values)),
            'avg_gdp_growth': float(np.mean(growth_values)),
            'min_gdp_growth': float(np.min(growth_values)),
            'max_gdp_growth': float(np.max(growth_values)),
            'final_debt_ratio': float(debt_values[-1]),
            'max_debt_ratio': float(np.max(debt_values)),
            'peak_debt_risk': float(np.max(risk_values)),
            'total_gdp_change': float((gdp_values[-1] - gdp_values[0]) / gdp_values[0] * 100),
            'social_spending_reduction': float((self.parameters['social_spending_percent'] - np.min(social_values)) * 100),
            'debt_increase': float((debt_values[-1] - debt_values[0]) * 100),
            'fiscal_policy_effectiveness': 'High' if final_assessment['gdp_growth_impact'] > 1.5 else 'Medium' if final_assessment['gdp_growth_impact'] > 0.8 else 'Low',
            'sustainability_warning': debt_values[-1] > self.parameters['debt_sustainability_threshold'],
            'final_assessment': final_assessment
        } 