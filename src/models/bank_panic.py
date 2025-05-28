"""
Bank Panic Model

Economic model for simulating banking panic scenarios, including:
- Customer deposit withdrawals
- Bank liquidity management
- Central bank intervention
- Systemic risk assessment
"""

import numpy as np
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class BankPanicShock:
    """Configuration for a bank panic scenario."""
    withdrawal_rate: float  # Daily withdrawal rate as percentage of deposits (e.g., 0.15 for 15%)
    panic_duration: int     # Number of periods the panic persists
    start_period: int = 0   # When the panic begins
    contagion_factor: float = 0.1  # How panic spreads to other banks (0-1)


def simulate_bank_panic(total_deposits: float, liquid_reserves: float, 
                       withdrawal_rate: float, central_bank_support: float = 0.0) -> Dict[str, Any]:
    """
    Simple, interpretable function to simulate the effect of a bank panic.
    
    Args:
        total_deposits: Total bank deposits (USD)
        liquid_reserves: Available liquid reserves (USD)
        withdrawal_rate: Daily withdrawal rate as percentage (e.g., 15.0 for 15%)
        central_bank_support: Central bank emergency funding (USD)
        
    Returns:
        Dict containing:
        - daily_withdrawals: Amount withdrawn per day
        - remaining_liquidity: Liquidity after withdrawals
        - survival_days: How many days bank can survive
        - bank_survives: Boolean indicating if bank survives the panic
        - liquidity_ratio: Final liquidity as percentage of deposits
    """
    # Calculate daily withdrawal amount
    daily_withdrawals = total_deposits * (withdrawal_rate / 100.0)
    
    # Total available liquidity including central bank support
    total_liquidity = liquid_reserves + central_bank_support
    
    # Calculate how many days the bank can survive
    if daily_withdrawals > 0:
        survival_days = int(total_liquidity / daily_withdrawals)
    else:
        survival_days = float('inf')
    
    # Remaining liquidity after one day of withdrawals
    remaining_liquidity = max(0, total_liquidity - daily_withdrawals)
    
    # Bank survives if it can handle at least 7 days of panic (typical panic duration)
    bank_survives = survival_days >= 7
    
    # Calculate final liquidity ratio
    liquidity_ratio = (remaining_liquidity / total_deposits) * 100.0 if total_deposits > 0 else 0.0
    
    return {
        'daily_withdrawals': daily_withdrawals,
        'remaining_liquidity': remaining_liquidity,
        'survival_days': survival_days if survival_days != float('inf') else 999,
        'bank_survives': bank_survives,
        'liquidity_ratio': liquidity_ratio
    }


class BankPanicModel:
    """
    Bank Panic Model
    
    Simulates banking panic scenarios including:
    - Customer deposit withdrawals
    - Bank liquidity depletion
    - Central bank emergency support
    - Systemic contagion effects
    - Economic impact assessment
    """
    
    def __init__(self, parameters: Dict[str, Any]):
        """
        Initialize the Bank Panic Model.
        
        Args:
            parameters: Model calibration parameters
        """
        self.parameters = self._validate_parameters(parameters)
        logger.info("Bank Panic Model initialized")
    
    def _validate_parameters(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and set default parameters."""
        defaults = {
            # Bank balance sheet parameters
            'total_deposits': 100000000000.0,      # $100 billion in deposits
            'liquid_reserves': 15000000000.0,      # $15 billion liquid reserves (15% ratio)
            'loan_portfolio': 80000000000.0,       # $80 billion in loans (illiquid)
            'capital_buffer': 8000000000.0,        # $8 billion capital buffer
            
            # Panic dynamics
            'base_withdrawal_rate': 0.02,          # 2% normal daily withdrawal rate
            'panic_multiplier': 7.5,               # Panic increases withdrawals by 7.5x
            'contagion_threshold': 0.3,            # 30% liquidity ratio triggers contagion
            'recovery_rate': 0.8,                  # 80% of panic subsides each period after peak
            
            # Central bank parameters
            'cb_intervention_threshold': 0.2,      # CB intervenes when liquidity < 20%
            'cb_max_support': 50000000000.0,       # $50 billion max CB support
            'cb_response_delay': 1,                # 1 period delay for CB response
            
            # Economic impact parameters
            'credit_contraction_rate': 0.05,       # 5% credit reduction per period during panic
            'gdp_impact_multiplier': 0.02,         # 2% GDP impact per $1T credit reduction
            
            # Model parameters
            'periods': 30,                         # Number of simulation periods (days)
            'num_banks': 10,                       # Number of banks in the system
        }
        
        # Merge with provided parameters
        for key, default_value in defaults.items():
            if key not in params:
                params[key] = default_value
        
        return params
    
    def simulate(self, simulation_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the bank panic simulation.
        
        Args:
            simulation_config: Simulation configuration including panic details
            
        Returns:
            Dictionary containing simulation results
        """
        periods = self.parameters['periods']
        
        # Parse panic configuration
        panic_config = simulation_config.get('panic', {})
        panic = BankPanicShock(
            withdrawal_rate=panic_config.get('withdrawal_rate', 15.0),  # 15% daily withdrawals
            panic_duration=panic_config.get('panic_duration', 7),
            start_period=panic_config.get('start_period', 0),
            contagion_factor=panic_config.get('contagion_factor', 0.1)
        )
        
        logger.info(f"Simulating bank panic with {panic.withdrawal_rate:.1f}% daily withdrawals "
                   f"for {panic.panic_duration} periods starting at period {panic.start_period}")
        
        # Initialize time series
        results = {
            'periods': list(range(periods)),
            'withdrawal_rate': np.full(periods, self.parameters['base_withdrawal_rate']),
            'daily_withdrawals': np.zeros(periods),
            'remaining_deposits': np.full(periods, self.parameters['total_deposits']),
            'liquid_reserves': np.full(periods, self.parameters['liquid_reserves']),
            'liquidity_ratio': np.zeros(periods),
            'central_bank_support': np.zeros(periods),
            'banks_failed': np.zeros(periods),
            'credit_available': np.full(periods, self.parameters['loan_portfolio']),
            'gdp_impact': np.zeros(periods),
            'panic_intensity': np.zeros(periods),
        }
        
        # Track bank survival
        bank_survival_status = np.ones(self.parameters['num_banks'])  # 1 = alive, 0 = failed
        
        # Apply bank panic
        for t in range(periods):
            # Determine panic intensity
            panic_intensity = self._calculate_panic_intensity(t, panic)
            results['panic_intensity'][t] = panic_intensity
            
            # Calculate withdrawal rate
            current_withdrawal_rate = self.parameters['base_withdrawal_rate']
            if panic_intensity > 0:
                current_withdrawal_rate *= (1 + panic_intensity * self.parameters['panic_multiplier'])
            
            results['withdrawal_rate'][t] = current_withdrawal_rate
            
            # Calculate withdrawals and update bank state
            self._update_bank_state(results, t, current_withdrawal_rate)
            
            # Check for central bank intervention
            self._check_central_bank_intervention(results, t)
            
            # Update bank failures and contagion
            bank_survival_status = self._update_bank_failures(results, t, bank_survival_status, panic.contagion_factor)
            
            # Calculate economic impacts
            self._calculate_economic_impacts(results, t)
        
        # Convert numpy arrays to lists for JSON serialization
        for key, value in results.items():
            if isinstance(value, np.ndarray):
                results[key] = value.tolist()
        
        # Add summary statistics
        results['summary'] = self._calculate_summary(results, bank_survival_status)
        
        logger.info("Bank panic simulation completed")
        return results
    
    def _calculate_panic_intensity(self, period: int, panic: BankPanicShock) -> float:
        """Calculate the intensity of the panic at a given period."""
        if period < panic.start_period:
            return 0.0
        
        panic_period = period - panic.start_period
        
        if panic_period < panic.panic_duration:
            # Peak panic intensity during the panic duration
            return 1.0
        else:
            # Exponential decay after panic peak
            decay_period = panic_period - panic.panic_duration
            return max(0.0, self.parameters['recovery_rate'] ** decay_period)
    
    def _update_bank_state(self, results: Dict[str, Any], period: int, withdrawal_rate: float):
        """Update bank deposits, reserves, and liquidity."""
        if period == 0:
            # Initialize first period
            results['liquidity_ratio'][period] = (results['liquid_reserves'][period] / 
                                                 results['remaining_deposits'][period]) * 100
            return
        
        # Calculate withdrawals
        prev_deposits = results['remaining_deposits'][period - 1]
        daily_withdrawals = prev_deposits * withdrawal_rate
        results['daily_withdrawals'][period] = daily_withdrawals
        
        # Update deposits
        new_deposits = max(0, prev_deposits - daily_withdrawals)
        results['remaining_deposits'][period] = new_deposits
        
        # Update liquid reserves (reduced by withdrawals)
        prev_reserves = results['liquid_reserves'][period - 1]
        cb_support = results['central_bank_support'][period - 1]  # Previous period's support
        available_liquidity = prev_reserves + cb_support
        
        new_reserves = max(0, available_liquidity - daily_withdrawals)
        results['liquid_reserves'][period] = new_reserves
        
        # Calculate liquidity ratio
        if new_deposits > 0:
            results['liquidity_ratio'][period] = (new_reserves / new_deposits) * 100
        else:
            results['liquidity_ratio'][period] = 0
    
    def _check_central_bank_intervention(self, results: Dict[str, Any], period: int):
        """Check if central bank should intervene and provide support."""
        liquidity_ratio = results['liquidity_ratio'][period]
        
        # Central bank intervenes if liquidity falls below threshold
        if liquidity_ratio < self.parameters['cb_intervention_threshold'] * 100:
            # Calculate needed support (with delay)
            if period >= self.parameters['cb_response_delay']:
                support_needed = results['daily_withdrawals'][period] * 7  # 7 days of coverage
                support_provided = min(support_needed, self.parameters['cb_max_support'])
                results['central_bank_support'][period] = support_provided
                logger.info(f"Central bank intervention at period {period}: ${support_provided/1e9:.1f}B")
    
    def _update_bank_failures(self, results: Dict[str, Any], period: int, 
                            bank_survival: np.ndarray, contagion_factor: float) -> np.ndarray:
        """Update bank failure status and calculate contagion effects."""
        liquidity_ratio = results['liquidity_ratio'][period]
        
        # Banks fail if liquidity ratio drops below 5%
        if liquidity_ratio < 5.0:
            # Calculate number of banks that fail due to liquidity crisis
            failure_probability = max(0, (5.0 - liquidity_ratio) / 5.0)
            new_failures = int(failure_probability * np.sum(bank_survival))
            
            # Apply contagion effect
            if new_failures > 0:
                contagion_failures = int(new_failures * contagion_factor * self.parameters['num_banks'])
                total_failures = min(new_failures + contagion_failures, int(np.sum(bank_survival)))
                
                # Update bank survival status
                alive_banks = np.where(bank_survival == 1)[0]
                if len(alive_banks) >= total_failures:
                    failed_indices = np.random.choice(alive_banks, total_failures, replace=False)
                    bank_survival[failed_indices] = 0
        
        # Record total failed banks
        results['banks_failed'][period] = self.parameters['num_banks'] - np.sum(bank_survival)
        
        return bank_survival
    
    def _calculate_economic_impacts(self, results: Dict[str, Any], period: int):
        """Calculate broader economic impacts of the banking crisis."""
        failed_banks = results['banks_failed'][period]
        total_banks = self.parameters['num_banks']
        
        # Credit contraction based on bank failures and liquidity stress
        if period == 0:
            results['credit_available'][period] = self.parameters['loan_portfolio']
        else:
            # Credit contracts based on failed banks and liquidity stress
            failure_rate = failed_banks / total_banks
            liquidity_stress = max(0, (20 - results['liquidity_ratio'][period]) / 20)  # Stress when < 20%
            
            credit_reduction_rate = (failure_rate * 0.5) + (liquidity_stress * self.parameters['credit_contraction_rate'])
            credit_reduction = results['credit_available'][period - 1] * credit_reduction_rate
            
            results['credit_available'][period] = max(0, results['credit_available'][period - 1] - credit_reduction)
        
        # GDP impact based on credit contraction
        baseline_credit = self.parameters['loan_portfolio']
        credit_loss = baseline_credit - results['credit_available'][period]
        results['gdp_impact'][period] = -(credit_loss / 1e12) * self.parameters['gdp_impact_multiplier']  # Convert to trillions
    
    def _calculate_summary(self, results: Dict[str, Any], bank_survival: np.ndarray) -> Dict[str, Any]:
        """Calculate summary statistics for the simulation."""
        withdrawal_values = np.array(results['daily_withdrawals'])
        liquidity_values = np.array(results['liquidity_ratio'])
        cb_support_values = np.array(results['central_bank_support'])
        failed_banks_values = np.array(results['banks_failed'])
        gdp_impact_values = np.array(results['gdp_impact'])
        
        # Use simple function for final assessment
        final_assessment = simulate_bank_panic(
            total_deposits=self.parameters['total_deposits'],
            liquid_reserves=results['liquid_reserves'][-1],
            withdrawal_rate=results['withdrawal_rate'][-1] * 100,  # Convert to percentage
            central_bank_support=np.sum(cb_support_values)
        )
        
        return {
            'max_daily_withdrawals': float(np.max(withdrawal_values)),
            'total_withdrawals': float(np.sum(withdrawal_values)),
            'min_liquidity_ratio': float(np.min(liquidity_values)),
            'total_cb_support': float(np.sum(cb_support_values)),
            'max_banks_failed': int(np.max(failed_banks_values)),
            'final_banks_surviving': int(np.sum(bank_survival)),
            'total_gdp_impact': float(np.sum(gdp_impact_values)),
            'peak_gdp_impact': float(np.min(gdp_impact_values)),  # Most negative impact
            'crisis_severity': 'High' if np.max(failed_banks_values) > 3 else 'Medium' if np.max(failed_banks_values) > 1 else 'Low',
            'final_assessment': final_assessment
        } 