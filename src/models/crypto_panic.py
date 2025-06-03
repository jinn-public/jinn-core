"""
Crypto Panic Model

Economic model for simulating crypto market panic scenarios, including:
- Mass liquidation events with different agent types
- Price dynamics across major crypto assets (BTC, ETH, DOGE)
- Exchange liquidity management and potential freezes/collapses
- Meme coin volatility and social media influence
- Contagion effects across the crypto ecosystem
"""

import numpy as np
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class CryptoPanicShock:
    """Configuration for a crypto panic scenario."""
    trigger_type: str           # Type of trigger: 'doge_pump', 'exchange_halt', 'regulatory', 'whale_dump'
    trigger_intensity: float    # Intensity of the trigger event (0.0-1.0)
    panic_duration: int         # Number of periods the panic persists
    start_period: int = 0       # When the panic begins
    contagion_factor: float = 0.15  # How panic spreads across assets and platforms (0-1)


def simulate_crypto_panic(btc_price: float, eth_price: float, doge_price: float,
                         trigger_type: str, panic_intensity: float) -> Dict[str, Any]:
    """
    Simple, interpretable function to simulate the effect of a crypto panic event.
    
    Args:
        btc_price: Current BTC price (USD)
        eth_price: Current ETH price (USD)
        doge_price: Current DOGE price (USD)
        trigger_type: Type of panic trigger
        panic_intensity: Panic intensity factor (0.0-1.0)
        
    Returns:
        Dict containing:
        - btc_price_change: BTC price change (%)
        - eth_price_change: ETH price change (%)
        - doge_price_change: DOGE price change (%)
        - exchange_freeze_risk: Risk of exchange freezes (0-1)
        - liquidation_volume: Total liquidation volume (USD)
    """
    # Base price impacts by trigger type
    trigger_impacts = {
        'doge_pump': {'btc': 0.05, 'eth': 0.03, 'doge': 0.80},       # DOGE pump affects DOGE massively
        'exchange_halt': {'btc': -0.25, 'eth': -0.30, 'doge': -0.35}, # DOGE more volatile in crashes
        'regulatory': {'btc': -0.20, 'eth': -0.18, 'doge': -0.40},    # DOGE more affected by regulation
        'whale_dump': {'btc': -0.12, 'eth': -0.08, 'doge': -0.25}     # DOGE more sensitive to manipulation
    }
    
    base_impact = trigger_impacts.get(trigger_type, trigger_impacts['whale_dump'])
    
    # Scale by panic intensity
    btc_price_change = base_impact['btc'] * panic_intensity * 100
    eth_price_change = base_impact['eth'] * panic_intensity * 100
    doge_price_change = base_impact['doge'] * panic_intensity * 100
    
    # Calculate exchange freeze risk
    exchange_freeze_risk = min(panic_intensity * 0.6, 0.8)
    
    # Estimate liquidation volume
    market_cap_btc = btc_price * 19_500_000        # Approximate BTC supply
    market_cap_eth = eth_price * 120_000_000       # Approximate ETH supply
    market_cap_doge = doge_price * 140_000_000_000 # Approximate DOGE supply (140B)
    total_market_cap = market_cap_btc + market_cap_eth + market_cap_doge
    
    liquidation_volume = total_market_cap * panic_intensity * 0.1  # 10% of market cap at max panic
    
    return {
        'btc_price_change': btc_price_change,
        'eth_price_change': eth_price_change,
        'doge_price_change': doge_price_change,
        'exchange_freeze_risk': exchange_freeze_risk,
        'liquidation_volume': liquidation_volume
    }


class CryptoPanicModel:
    """
    Crypto Panic Model
    
    Simulates crypto market panic scenarios including:
    - Multi-agent behavior (retail, whales, exchanges, meme coin influencers)
    - Asset price dynamics (BTC, ETH, DOGE)
    - Exchange liquidity management and freezes
    - Meme coin social media dynamics and volatility
    - Systemic contagion effects
    - Market recovery dynamics
    """
    
    def __init__(self, parameters: Dict[str, Any]):
        """
        Initialize the Crypto Panic Model.
        
        Args:
            parameters: Model calibration parameters
        """
        self.parameters = self._validate_parameters(parameters)
        logger.info("Crypto Panic Model initialized")
    
    def _validate_parameters(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and set default parameters."""
        defaults = {
            # Initial asset prices and supplies
            'btc_initial_price': 45000.0,          # $45,000 BTC
            'eth_initial_price': 3000.0,           # $3,000 ETH
            'doge_initial_price': 0.15,            # $0.15 DOGE
            'btc_supply': 19_500_000,              # ~19.5M BTC in circulation
            'eth_supply': 120_000_000,             # ~120M ETH in circulation
            'doge_supply': 140_000_000_000,        # ~140B DOGE in circulation
            
            # Agent populations and behaviors
            'num_retail_investors': 1_000_000,     # 1M retail investors
            'num_whales': 100,                     # 100 whale accounts
            'num_exchanges': 20,                   # 20 major exchanges
            'num_influencers': 50,                 # 50 crypto influencers/meme creators
            
            # Retail investor behavior
            'retail_panic_threshold': 0.05,        # 5% price drop triggers retail panic
            'retail_sell_probability': 0.3,        # 30% of retail sells during panic
            'retail_herd_multiplier': 2.0,         # Herd behavior amplification
            'retail_doge_fomo': 0.8,              # DOGE FOMO factor for retail
            
            # Whale behavior
            'whale_manipulation_factor': 0.8,      # Whales can amplify or dampen moves
            'whale_coordination_prob': 0.2,        # 20% chance whales coordinate
            'whale_average_holding': 1000.0,       # 1000 BTC average per whale
            'whale_doge_pump_power': 2.0,         # Whales can pump DOGE more easily
            
            # Exchange parameters
            'exchange_liquidity_ratio': 0.15,      # 15% of holdings in liquid reserves
            'exchange_freeze_threshold': 0.4,      # Freeze when liquidity < 40% of normal
            'exchange_recovery_rate': 0.1,         # 10% recovery rate per period after freeze
            
            # DOGE meme coin parameters
            'doge_social_media_factor': 1.5,       # Social media influence on DOGE
            'doge_celebrity_effect': 0.3,          # Celebrity endorsement impact
            'doge_volatility_multiplier': 3.0,     # DOGE is 3x more volatile
            'doge_pump_probability': 0.1,          # 10% chance of random pump per period
            
            # Market dynamics
            'price_volatility_base': 0.02,         # 2% base daily volatility
            'liquidity_impact_factor': 0.5,        # How liquidity affects price impact
            'recovery_half_life': 7,               # Days for 50% panic recovery
            
            # Contagion parameters
            'btc_to_eth_correlation': 0.7,         # BTC-ETH price correlation
            'btc_to_doge_correlation': 0.4,        # BTC-DOGE correlation (lower)
            'eth_to_doge_correlation': 0.3,        # ETH-DOGE correlation (lower)
            'crypto_to_traditional_spillover': 0.1, # Spillover to traditional markets
            
            # Model parameters
            'periods': 30,                         # Number of simulation periods (days)
            'random_seed': 42,                     # For reproducible results
        }
        
        # Merge with provided parameters
        for key, default_value in defaults.items():
            if key not in params:
                params[key] = default_value
        
        return params
    
    def simulate(self, simulation_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the crypto panic simulation.
        
        Args:
            simulation_config: Simulation configuration including panic details
            
        Returns:
            Dictionary containing simulation results
        """
        periods = self.parameters['periods']
        
        # Set random seed for reproducibility
        np.random.seed(self.parameters['random_seed'])
        
        # Parse panic configuration
        panic_config = simulation_config.get('panic', {})
        panic = CryptoPanicShock(
            trigger_type=panic_config.get('trigger_type', 'whale_dump'),
            trigger_intensity=panic_config.get('trigger_intensity', 0.6),
            panic_duration=panic_config.get('panic_duration', 7),
            start_period=panic_config.get('start_period', 0),
            contagion_factor=panic_config.get('contagion_factor', 0.15)
        )
        
        logger.info(f"Simulating crypto panic: {panic.trigger_type} with intensity {panic.trigger_intensity:.2f} "
                   f"for {panic.panic_duration} periods starting at period {panic.start_period}")
        
        # Initialize time series
        results = {
            'periods': list(range(periods)),
            'btc_price': np.full(periods, self.parameters['btc_initial_price']),
            'eth_price': np.full(periods, self.parameters['eth_initial_price']),
            'doge_price': np.full(periods, self.parameters['doge_initial_price']),
            'btc_volume': np.zeros(periods),
            'eth_volume': np.zeros(periods),
            'doge_volume': np.zeros(periods),
            'panic_intensity': np.zeros(periods),
            'retail_sell_rate': np.zeros(periods),
            'whale_activity': np.zeros(periods),
            'exchange_liquidity': np.full(periods, 1.0),  # Normalized liquidity
            'exchanges_frozen': np.zeros(periods),
            'doge_social_media_index': np.full(periods, 50.0),   # Neutral at 50
        }
        
        # Initialize agent states
        agent_states = self._initialize_agents()
        
        # Run simulation
        for t in range(periods):
            # Calculate current panic intensity
            panic_intensity = self._calculate_panic_intensity(t, panic)
            results['panic_intensity'][t] = panic_intensity
            
            # Update agent behaviors based on panic
            self._update_agent_behaviors(agent_states, t, panic_intensity, results)
            
            # Update asset prices based on agent actions
            self._update_asset_prices(results, t, agent_states, panic_intensity)
            
            # Update exchange states (liquidity and freezes)
            self._update_exchange_states(results, t, agent_states, panic_intensity)
            
            # Calculate fear & greed index
            results['doge_social_media_index'][t] = self._calculate_doge_social_media_index(results, t, panic_intensity)
            
            # Print progress
            if t % 5 == 0 or panic_intensity > 0:
                self._print_daily_update(t, results, panic_intensity)
        
        # Calculate summary statistics
        summary = self._calculate_summary(results, panic)
        results['summary'] = summary
        
        logger.info("Crypto panic simulation completed")
        return results
    
    def _initialize_agents(self) -> Dict[str, Any]:
        """Initialize agent states."""
        return {
            'retail_investors': {
                'count': self.parameters['num_retail_investors'],
                'panic_state': 0.0,  # 0 = calm, 1 = full panic
                'average_holding_btc': 0.1,  # 0.1 BTC average
                'average_holding_eth': 2.0,   # 2 ETH average
            },
            'whales': {
                'count': self.parameters['num_whales'],
                'coordination_level': 0.0,  # 0 = no coordination, 1 = full coordination
                'average_holding_btc': self.parameters['whale_average_holding'],
                'manipulation_intent': 0.0,  # -1 = bearish, +1 = bullish
            },
            'exchanges': {
                'count': self.parameters['num_exchanges'],
                'liquidity_reserves': np.full(self.parameters['num_exchanges'], 1.0),  # Normalized
                'operational_status': np.ones(self.parameters['num_exchanges']),  # 1 = operational, 0 = frozen
                'withdrawal_pressure': np.zeros(self.parameters['num_exchanges']),
            },
            'influencers': {
                'count': self.parameters['num_influencers'],
                'social_media_influence': np.zeros(self.parameters['num_influencers']),
            }
        }
    
    def _calculate_panic_intensity(self, period: int, panic: CryptoPanicShock) -> float:
        """Calculate panic intensity at given period."""
        if period < panic.start_period:
            return 0.0
        elif period < panic.start_period + panic.panic_duration:
            # Peak panic in the middle, tapering off
            relative_period = period - panic.start_period
            peak_period = panic.panic_duration // 2
            if relative_period <= peak_period:
                # Ramp up to peak
                intensity = panic.trigger_intensity * (relative_period / peak_period)
            else:
                # Decay from peak
                decay_factor = (panic.panic_duration - relative_period) / (panic.panic_duration - peak_period)
                intensity = panic.trigger_intensity * decay_factor
            return max(0.0, intensity)
        else:
            # Post-panic recovery with exponential decay
            recovery_period = period - panic.start_period - panic.panic_duration
            decay_rate = 0.2  # 20% decay per period
            residual_panic = panic.trigger_intensity * 0.1 * np.exp(-decay_rate * recovery_period)
            return max(0.0, residual_panic)
    
    def _update_agent_behaviors(self, agent_states: Dict[str, Any], period: int, 
                               panic_intensity: float, results: Dict[str, Any]):
        """Update agent behaviors based on current market conditions."""
        
        # Update retail investor behavior
        retail = agent_states['retail_investors']
        if panic_intensity > self.parameters['retail_panic_threshold']:
            retail['panic_state'] = min(1.0, retail['panic_state'] + panic_intensity * 0.5)
        else:
            retail['panic_state'] = max(0.0, retail['panic_state'] - 0.1)  # Gradual recovery
        
        # Retail sell rate based on panic state and herd behavior
        base_sell_rate = retail['panic_state'] * self.parameters['retail_sell_probability']
        herd_effect = retail['panic_state'] * self.parameters['retail_herd_multiplier']
        results['retail_sell_rate'][period] = min(1.0, base_sell_rate * (1 + herd_effect))
        
        # Update whale behavior
        whales = agent_states['whales']
        # Whales may coordinate during high panic (contrarian or momentum)
        if panic_intensity > 0.3:
            coordination_prob = self.parameters['whale_coordination_prob'] * panic_intensity
            whales['coordination_level'] = min(1.0, whales['coordination_level'] + coordination_prob)
            # Random manipulation intent (-1 to +1)
            whales['manipulation_intent'] = np.random.uniform(-1, 1) * whales['coordination_level']
        else:
            whales['coordination_level'] = max(0.0, whales['coordination_level'] - 0.2)
            whales['manipulation_intent'] *= 0.8  # Decay manipulation intent
        
        results['whale_activity'][period] = abs(whales['manipulation_intent'])
        
        # Update exchange withdrawal pressure
        exchanges = agent_states['exchanges']
        withdrawal_pressure = panic_intensity * (1 + results['retail_sell_rate'][period])
        exchanges['withdrawal_pressure'] = np.full(len(exchanges['withdrawal_pressure']), withdrawal_pressure)
    
    def _update_asset_prices(self, results: Dict[str, Any], period: int, 
                            agent_states: Dict[str, Any], panic_intensity: float):
        """Update asset prices based on agent actions and market dynamics."""
        
        if period == 0:
            # Initialize liquidation volume for period 0
            results['liquidation_volume'] = np.zeros(len(results['periods']))
            return  # Keep initial prices for period 0
        
        # Previous prices
        prev_btc = results['btc_price'][period - 1]
        prev_eth = results['eth_price'][period - 1]
        prev_doge = results['doge_price'][period - 1]
        
        # Base volatility
        btc_volatility = self.parameters['price_volatility_base'] * (1 + panic_intensity * 2)
        eth_volatility = self.parameters['price_volatility_base'] * (1 + panic_intensity * 2.5)
        doge_volatility = self.parameters['price_volatility_base'] * self.parameters['doge_volatility_multiplier'] * (1 + panic_intensity * 3)
        
        # Retail selling pressure
        retail_sell_pressure = results['retail_sell_rate'][period] * 0.1  # Max 10% price impact
        
        # Whale manipulation impact
        whale_impact = agent_states['whales']['manipulation_intent'] * 0.05  # Max 5% price impact
        whale_doge_impact = whale_impact * self.parameters['whale_doge_pump_power']  # Whales can pump DOGE more
        
        # Exchange liquidity impact
        liquidity_factor = results['exchange_liquidity'][period - 1] if period > 0 else 1.0
        liquidity_impact = (1 - liquidity_factor) * 0.2  # Reduced liquidity amplifies moves
        
        # DOGE-specific social media and celebrity effects
        doge_social_media_effect = 0.0
        if np.random.random() < self.parameters['doge_celebrity_effect']:
            doge_social_media_effect = np.random.uniform(-0.15, 0.3)  # Celebrity tweets can pump DOGE
        
        # Random DOGE pump probability
        doge_random_pump = 0.0
        if np.random.random() < self.parameters['doge_pump_probability']:
            doge_random_pump = np.random.uniform(0.1, 0.5)  # Random 10-50% pump
        
        # BTC price calculation
        btc_change = (
            np.random.normal(0, btc_volatility) -  # Random walk
            retail_sell_pressure +                 # Retail selling pressure (negative)
            whale_impact -                         # Whale manipulation
            liquidity_impact                       # Liquidity impact (negative)
        )
        
        # ETH price calculation (correlated with BTC)
        eth_correlation = self.parameters['btc_to_eth_correlation']
        eth_independent = np.random.normal(0, eth_volatility) * (1 - eth_correlation)
        eth_correlated = btc_change * eth_correlation
        eth_change = (
            eth_correlated + eth_independent -
            retail_sell_pressure * 1.2 +          # ETH more sensitive to retail
            whale_impact * 0.8 -                  # Less whale impact on ETH
            liquidity_impact
        )
        
        # DOGE price calculation (less correlated, more volatile)
        doge_btc_correlation = self.parameters['btc_to_doge_correlation']
        doge_eth_correlation = self.parameters['eth_to_doge_correlation']
        doge_independent = np.random.normal(0, doge_volatility) * (1 - doge_btc_correlation - doge_eth_correlation)
        doge_btc_correlated = btc_change * doge_btc_correlation
        doge_eth_correlated = eth_change * doge_eth_correlation
        
        doge_change = (
            doge_btc_correlated + doge_eth_correlated + doge_independent -
            retail_sell_pressure * self.parameters['retail_doge_fomo'] +  # DOGE FOMO effect
            whale_doge_impact +                    # Enhanced whale impact on DOGE
            doge_social_media_effect +             # Celebrity/social media effect
            doge_random_pump -                     # Random pumps
            liquidity_impact * 1.5                 # DOGE more sensitive to liquidity
        )
        
        # Apply changes to prices
        results['btc_price'][period] = max(prev_btc * (1 + btc_change), prev_btc * 0.01)  # Floor at 1% of previous
        results['eth_price'][period] = max(prev_eth * (1 + eth_change), prev_eth * 0.01)
        results['doge_price'][period] = max(prev_doge * (1 + doge_change), prev_doge * 0.001)  # Lower floor for DOGE
        
        # Calculate trading volumes (higher during panic and price moves)
        volume_multiplier = 1 + panic_intensity * 3 + abs(btc_change) * 10
        
        btc_market_cap = results['btc_price'][period] * self.parameters['btc_supply']
        eth_market_cap = results['eth_price'][period] * self.parameters['eth_supply']
        doge_market_cap = results['doge_price'][period] * self.parameters['doge_supply']
        
        results['btc_volume'][period] = btc_market_cap * 0.02 * volume_multiplier  # 2% daily turnover base
        results['eth_volume'][period] = eth_market_cap * 0.03 * volume_multiplier  # 3% daily turnover base
        results['doge_volume'][period] = doge_market_cap * 0.05 * volume_multiplier  # 5% daily turnover base (higher for meme coin)
        
        # Calculate liquidation volume
        total_volume = results['btc_volume'][period] + results['eth_volume'][period] + results['doge_volume'][period]
        liquidation_rate = panic_intensity * 0.1  # Up to 10% of volume in liquidations
        results['liquidation_volume'][period] = total_volume * liquidation_rate
    
    def _update_exchange_states(self, results: Dict[str, Any], period: int,
                               agent_states: Dict[str, Any], panic_intensity: float):
        """Update exchange liquidity and operational status."""
        
        exchanges = agent_states['exchanges']
        
        # Update liquidity based on withdrawal pressure
        for i in range(len(exchanges['liquidity_reserves'])):
            if exchanges['operational_status'][i] > 0:  # Only if operational
                withdrawal_impact = exchanges['withdrawal_pressure'][i] * 0.1
                exchanges['liquidity_reserves'][i] = max(0.0, 
                    exchanges['liquidity_reserves'][i] - withdrawal_impact)
                
                # Recovery if no pressure
                if exchanges['withdrawal_pressure'][i] < 0.1:
                    exchanges['liquidity_reserves'][i] = min(1.0,
                        exchanges['liquidity_reserves'][i] + self.parameters['exchange_recovery_rate'])
        
        # Check for exchange freezes
        freeze_threshold = self.parameters['exchange_freeze_threshold']
        for i in range(len(exchanges['operational_status'])):
            if (exchanges['liquidity_reserves'][i] < freeze_threshold and 
                exchanges['operational_status'][i] > 0):
                exchanges['operational_status'][i] = 0  # Freeze exchange
                logger.info(f"Exchange {i+1} frozen due to liquidity shortage at period {period}")
            elif (exchanges['liquidity_reserves'][i] > 0.8 and 
                  exchanges['operational_status'][i] == 0):
                exchanges['operational_status'][i] = 1  # Unfreeze exchange
                logger.info(f"Exchange {i+1} resumed operations at period {period}")
        
        # Aggregate metrics
        results['exchange_liquidity'][period] = np.mean(exchanges['liquidity_reserves'])
        results['exchanges_frozen'][period] = np.sum(exchanges['operational_status'] == 0)
    
    def _calculate_doge_social_media_index(self, results: Dict[str, Any], period: int, panic_intensity: float) -> float:
        """Calculate a DOGE social media index (0 = extreme fear, 100 = extreme greed)."""
        
        if period == 0:
            return 50.0  # Neutral
        
        # Components of fear/greed
        # 1. Price momentum
        doge_change = (results['doge_price'][period] - results['doge_price'][period-1]) / results['doge_price'][period-1]
        price_momentum_score = 50 + (doge_change * 1000)  # Scale price change
        
        # 2. Panic intensity (inverse)
        panic_score = 50 - (panic_intensity * 40)  # High panic = low score
        
        # 3. Exchange health
        exchange_health = results['exchange_liquidity'][period] * 50
        
        # 4. DOGE social media influence
        social_media_influence = results['doge_social_media_index'][period-1] + (panic_intensity * 0.05)
        
        # Weighted average
        doge_social_media = (
            price_momentum_score * 0.4 +
            panic_score * 0.3 +
            exchange_health * 0.2 +
            social_media_influence * 0.1
        )
        
        return np.clip(doge_social_media, 0, 100)
    
    def _print_daily_update(self, period: int, results: Dict[str, Any], panic_intensity: float):
        """Print daily simulation update."""
        btc_price = results['btc_price'][period]
        eth_price = results['eth_price'][period]
        doge_price = results['doge_price'][period]
        frozen_exchanges = results['exchanges_frozen'][period]
        doge_social_media = results['doge_social_media_index'][period]
        
        print(f"Day {period:2d}: BTC=${btc_price:8,.0f} | ETH=${eth_price:6,.0f} | "
              f"DOGE=${doge_price:.4f} | Frozen Exchanges: {frozen_exchanges:2.0f} | "
              f"DOGE Social Media: {doge_social_media:4.1f} | Panic: {panic_intensity:.3f}")
    
    def _calculate_summary(self, results: Dict[str, Any], panic: CryptoPanicShock) -> Dict[str, Any]:
        """Calculate summary statistics."""
        
        periods = len(results['periods'])
        
        # Price changes
        btc_initial = results['btc_price'][0]
        btc_final = results['btc_price'][-1]
        btc_min = np.min(results['btc_price'])
        btc_max_drawdown = ((btc_initial - btc_min) / btc_initial) * 100
        
        eth_initial = results['eth_price'][0]
        eth_final = results['eth_price'][-1]
        eth_min = np.min(results['eth_price'])
        eth_max_drawdown = ((eth_initial - eth_min) / eth_initial) * 100
        
        doge_initial = results['doge_price'][0]
        doge_final = results['doge_price'][-1]
        doge_min = np.min(results['doge_price'])
        doge_max = np.max(results['doge_price'])
        doge_max_drawdown = ((doge_initial - doge_min) / doge_initial) * 100
        doge_max_pump = ((doge_max - doge_initial) / doge_initial) * 100
        
        # DOGE social media influence
        max_social_media_index = np.max(results['doge_social_media_index'])
        social_media_periods = np.sum(results['doge_social_media_index'] > 50)
        
        # Exchange health
        max_frozen_exchanges = np.max(results['exchanges_frozen'])
        min_liquidity = np.min(results['exchange_liquidity'])
        
        # Market stress
        max_panic = np.max(results['panic_intensity'])
        panic_periods = np.sum(results['panic_intensity'] > 0.1)
        min_doge_social_media = np.min(results['doge_social_media_index'])
        
        # Recovery metrics
        recovery_period = None
        for i in range(periods):
            if results['btc_price'][i] >= btc_initial * 0.95:  # 95% recovery
                recovery_period = i
                break
        
        summary = {
            'trigger_type': panic.trigger_type,
            'max_panic_intensity': max_panic,
            'panic_periods': panic_periods,
            
            'btc_total_return_pct': ((btc_final - btc_initial) / btc_initial) * 100,
            'btc_max_drawdown_pct': btc_max_drawdown,
            'eth_total_return_pct': ((eth_final - eth_initial) / eth_initial) * 100,
            'eth_max_drawdown_pct': eth_max_drawdown,
            'doge_total_return_pct': ((doge_final - doge_initial) / doge_initial) * 100,
            'doge_max_drawdown_pct': doge_max_drawdown,
            'doge_max_pump_pct': doge_max_pump,
            
            'doge_max_social_media_index': max_social_media_index,
            'doge_social_media_periods': social_media_periods,
            'doge_social_media_ratio': social_media_periods / periods,
            
            'max_frozen_exchanges': max_frozen_exchanges,
            'min_exchange_liquidity': min_liquidity,
            'exchange_stress_periods': np.sum(results['exchange_liquidity'] < 0.5),
            
            'min_doge_social_media_index': min_doge_social_media,
            'recovery_period': recovery_period if recovery_period else periods,
            'total_liquidation_volume': np.sum(results['liquidation_volume']),
            
            'market_survived': btc_final > btc_initial * 0.5,  # Market survives if BTC > 50% of initial
            'system_stability': min_liquidity > 0.2 and max_social_media_index < 90,  # Adjusted for DOGE volatility
        }
        
        return summary


# Simple utility function for quick testing
def run_crypto_panic_scenario(trigger_type: str = 'whale_dump', intensity: float = 0.6) -> Dict[str, Any]:
    """
    Quick utility to run a crypto panic scenario.
    
    Args:
        trigger_type: Type of trigger event
        intensity: Panic intensity (0.0-1.0)
        
    Returns:
        Simulation results
    """
    model = CryptoPanicModel({})
    
    simulation_config = {
        'panic': {
            'trigger_type': trigger_type,
            'trigger_intensity': intensity,
            'panic_duration': 7,
            'start_period': 0
        }
    }
    
    return model.simulate(simulation_config) 