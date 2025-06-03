# Crypto Panic Model Documentation

## Overview

The Crypto Panic Model simulates mass panic events in cryptocurrency markets, modeling the behavior of different agent types and their impact on asset prices, exchange liquidity, and stablecoin stability.

## Features

### Agent Types
- **Retail Investors**: Large in number, panic-driven behavior with herd mentality
- **Whales**: Price movers with coordination capabilities and manipulation potential
- **Exchanges**: Manage liquidity reserves and may freeze operations under stress
- **Stablecoin Issuers**: Defend pegs through intervention mechanisms

### Tracked Assets
- **BTC**: Primary crypto asset with base volatility and whale influence
- **ETH**: Correlated with BTC but more sensitive to retail behavior
- **USDT**: Stablecoin with peg dynamics and intervention mechanisms

### Key Metrics
- Asset prices and volumes
- Exchange liquidity and operational status
- Stablecoin peg deviations
- Liquidation volumes
- Fear & Greed Index (0-100 scale)
- Market recovery timing

## Trigger Events

### 1. Whale Dump (`whale_dump`)
- Large holders coordinate selling
- Moderate price impact, limited exchange stress
- Example: Major Bitcoin holder liquidates position

### 2. Exchange Halt (`exchange_halt`)
- Major exchange freezes withdrawals
- High price impact, potential for exchange freezes
- Example: Binance halts withdrawals due to "maintenance"

### 3. USDT Depeg (`usdt_depeg`)
- Tether loses dollar peg
- Moderate price impact, high stablecoin instability
- Example: Tether banking issues cause confidence crisis

### 4. Regulatory Shock (`regulatory`)
- Government announces crypto restrictions
- High initial impact with gradual recovery
- Example: SEC announces major enforcement action

## Example Scenarios

The `examples/` folder contains pre-configured scenarios that demonstrate different starting conditions:

### `scenario_10_crypto_panic.json` - Custom High-Value Market
- **BTC**: $60,000 starting price
- **ETH**: $4,000 starting price  
- **USDT**: $120B supply
- **Trigger**: Exchange halt (70% intensity)
- **Focus**: Testing panic in high-value market conditions

### `scenario_11_crypto_panic_bear_market.json` - Bear Market Conditions
- **BTC**: $25,000 starting price (depressed)
- **ETH**: $1,600 starting price (depressed)
- **Market**: Weakened exchanges, nervous retail investors
- **Trigger**: Regulatory shock (60% intensity)
- **Focus**: Testing resilience during market weakness

### `scenario_12_crypto_panic_bull_market.json` - Bull Market Peak
- **BTC**: $75,000 starting price (peak)
- **ETH**: $5,500 starting price (peak)
- **Market**: Strong infrastructure, confident retail
- **Trigger**: Whale dump (80% intensity)
- **Focus**: Testing what happens when panic hits during euphoria

### `scenario_13_crypto_panic_stablecoin_crisis.json` - Stablecoin Crisis
- **USDT**: $200B supply with weak backing (60% quality)
- **Intervention**: Weak (30% power)
- **Trigger**: USDT depeg (90% intensity)
- **Focus**: Testing systemic stablecoin risks

## Usage Examples

### Basic Usage
```python
from src.models.crypto_panic import run_crypto_panic_scenario

# Quick scenario test
results = run_crypto_panic_scenario(
    trigger_type='whale_dump', 
    intensity=0.6
)
print(f"BTC Return: {results['summary']['btc_total_return_pct']:.2f}%")
```

### Using Example Scenarios
```python
from src.engine import SimulationEngine

# Load and run a pre-configured scenario
engine = SimulationEngine()
results = engine.run_scenario_file('examples/scenario_10_crypto_panic.json')

# Extract results
summary = results['results']['summary']
print(f"BTC Return: {summary['btc_total_return_pct']:.2f}%")
print(f"Market Survived: {summary['market_survived']}")
```

### Advanced Configuration
```python
from src.models.crypto_panic import CryptoPanicModel

model = CryptoPanicModel({
    'periods': 30,
    'btc_initial_price': 50000.0,
    'eth_initial_price': 3500.0,
    'num_exchanges': 25,
    'retail_panic_threshold': 0.03,  # Lower threshold = more sensitive retail
    'whale_coordination_prob': 0.3,  # Higher coordination probability
    'stablecoin_intervention_power': 0.8,  # Stronger peg defense
})

simulation_config = {
    'panic': {
        'trigger_type': 'exchange_halt',
        'trigger_intensity': 0.8,
        'panic_duration': 10,
        'start_period': 2,
        'contagion_factor': 0.25
    }
}

results = model.simulate(simulation_config)
```

### Custom JSON Scenario Template
```json
{
  "model": "crypto_panic",
  "description": "Your custom scenario description",
  "parameters": {
    "periods": 25,
    
    "// === INITIAL ASSET PRICES ===": "",
    "btc_initial_price": 45000.0,
    "eth_initial_price": 3000.0,
    "usdt_supply": 80000000000,
    
    "// === MARKET STRUCTURE ===": "",
    "num_exchanges": 20,
    "num_retail_investors": 1000000,
    "num_whales": 100,
    
    "// === AGENT BEHAVIOR ===": "",
    "retail_panic_threshold": 0.05,
    "retail_sell_probability": 0.3,
    "whale_coordination_prob": 0.2,
    
    "// === EXCHANGE DYNAMICS ===": "",
    "exchange_liquidity_ratio": 0.15,
    "exchange_freeze_threshold": 0.4,
    
    "// === STABLECOIN MECHANICS ===": "",
    "stablecoin_intervention_power": 0.7,
    "backing_asset_quality": 0.85,
    
    "random_seed": 42
  },
  "simulation": {
    "panic": {
      "trigger_type": "whale_dump",
      "trigger_intensity": 0.6,
      "panic_duration": 7,
      "start_period": 0
    }
  }
}
```

## Key Parameters for Manipulation

### Starting Market Conditions
- `btc_initial_price`: Starting BTC price (default: $45,000)
- `eth_initial_price`: Starting ETH price (default: $3,000)
- `usdt_supply`: Total USDT supply (default: $80B)
- `num_exchanges`: Number of exchanges (default: 20)

### Agent Behavior
- `retail_panic_threshold`: Price drop % that triggers retail panic (default: 5%)
- `retail_sell_probability`: % of retail that sells during panic (default: 30%)
- `whale_coordination_prob`: Probability of whale coordination (default: 20%)
- `whale_average_holding`: Average whale BTC holding (default: 1000 BTC)

### Exchange Dynamics
- `exchange_liquidity_ratio`: % of holdings in liquid reserves (default: 15%)
- `exchange_freeze_threshold`: Liquidity level that triggers freeze (default: 40%)
- `exchange_recovery_rate`: Recovery rate per period (default: 10%)

### Stablecoin Mechanics
- `stablecoin_intervention_power`: Effectiveness of peg defense (default: 70%)
- `backing_asset_quality`: Quality of backing assets (default: 85%)
- `usdt_peg_tolerance`: Deviation before intervention (default: 2%)

## Output Interpretation

### Summary Metrics
- `btc_total_return_pct`: Total BTC price change from start to finish
- `btc_max_drawdown_pct`: Maximum price decline during simulation
- `usdt_max_depeg_pct`: Maximum stablecoin deviation from $1
- `max_frozen_exchanges`: Peak number of frozen exchanges
- `market_survived`: Boolean indicating if BTC retained >50% of initial value
- `system_stability`: Boolean indicating overall system health

### Time Series Data
All results include period-by-period data for:
- Asset prices and volumes
- Exchange liquidity and frozen count
- Panic intensity and agent behaviors
- Fear & Greed Index

## Testing and Validation

### Test Individual Scenarios
```bash
# Test basic functionality
python test_crypto_panic.py

# Run demo with different scenarios
python demo_crypto_panic.py

# Test all example scenarios
python test_example_scenarios.py
```

### Run Specific Example Scenarios
```bash
# Using the Jinn engine directly
python -c "
from src.engine import SimulationEngine
engine = SimulationEngine()
results = engine.run_scenario_file('examples/scenario_12_crypto_panic_bull_market.json')
print(f'Bull market result: {results[\"results\"][\"summary\"][\"btc_total_return_pct\"]:.1f}%')
"
```

## Extending the Model

### Adding New Trigger Types
1. Add trigger impacts to `trigger_impacts` dict in `simulate_crypto_panic()`
2. Update `_calculate_panic_intensity()` for custom timing
3. Modify agent behaviors in `_update_agent_behaviors()` if needed

### New Agent Types
1. Add agent initialization in `_initialize_agents()`
2. Update behavior in `_update_agent_behaviors()`
3. Include impact in `_update_asset_prices()`

### Additional Assets
1. Add price tracking in simulation initialization
2. Implement price update logic in `_update_asset_prices()`
3. Update correlation parameters and summary calculations

### Custom Metrics
1. Add metric tracking to results initialization
2. Calculate values in appropriate update functions
3. Include in summary statistics

## Integration with Jinn Engine

The model is fully integrated with the Jinn simulation engine:
- Registered as `'crypto_panic'` model type
- Supports JSON scenario loading
- Standard result format with metadata
- Compatible with existing Jinn utilities

## Research Applications

This model can be used to study:
- Systemic risk in crypto markets
- Contagion effects between assets
- Exchange liquidity management
- Stablecoin stability mechanisms
- Regulatory impact assessment
- Market resilience under stress
- Effect of different market conditions on panic outcomes

## Limitations

- Simplified agent behaviors (real markets are more complex)
- Limited to BTC, ETH, and USDT (can be extended)
- No options/derivatives markets
- No cross-chain effects
- Static network effects (no dynamic relationship changes)

## Future Enhancements

Potential areas for improvement:
- More sophisticated agent psychology
- Options and futures markets
- Cross-chain contagion effects
- Dynamic network topology
- Machine learning-based behavior patterns
- Integration with real market data 