#!/usr/bin/env python3
"""
Demo script for the Crypto Panic Model

This script demonstrates the crypto panic simulation model with different
trigger scenarios and shows how various agent types react to market stress.
"""

import sys
import os
import logging

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models.crypto_panic import CryptoPanicModel, run_crypto_panic_scenario

def demo_simple_scenario():
    """Run a simple crypto panic scenario."""
    print("=" * 60)
    print("DEMO 1: Simple Whale Dump Scenario")
    print("=" * 60)
    
    # Run a simple whale dump scenario
    results = run_crypto_panic_scenario(trigger_type='whale_dump', intensity=0.5)
    
    print("\nSUMMARY:")
    summary = results['summary']
    print(f"Trigger Type: {summary['trigger_type']}")
    print(f"BTC Total Return: {summary['btc_total_return_pct']:.2f}%")
    print(f"BTC Max Drawdown: {summary['btc_max_drawdown_pct']:.2f}%")
    print(f"ETH Total Return: {summary['eth_total_return_pct']:.2f}%")
    print(f"ETH Max Drawdown: {summary['eth_max_drawdown_pct']:.2f}%")
    print(f"DOGE Total Return: {summary['doge_total_return_pct']:.2f}%")
    print(f"DOGE Max Drawdown: {summary['doge_max_drawdown_pct']:.2f}%")
    print(f"DOGE Max Pump: {summary['doge_max_pump_pct']:.2f}%")
    print(f"Max Frozen Exchanges: {summary['max_frozen_exchanges']:.0f}")
    print(f"Market Survived: {summary['market_survived']}")
    print(f"System Stability: {summary['system_stability']}")
    
    return results

def demo_severe_panic():
    """Run a severe crypto panic scenario."""
    print("\n" + "=" * 60)
    print("DEMO 2: Severe Exchange Halt Panic")
    print("=" * 60)
    
    # Create a more severe scenario
    model = CryptoPanicModel({
        'periods': 20,  # Shorter simulation
        'btc_initial_price': 50000.0,  # Higher starting price
        'eth_initial_price': 3500.0,
        'doge_initial_price': 0.20,
    })
    
    simulation_config = {
        'panic': {
            'trigger_type': 'exchange_halt',
            'trigger_intensity': 0.8,  # High intensity
            'panic_duration': 10,      # Longer panic
            'start_period': 2,         # Start on day 2
            'contagion_factor': 0.25   # Higher contagion
        }
    }
    
    results = model.simulate(simulation_config)
    
    print("\nSUMMARY:")
    summary = results['summary']
    print(f"Trigger Type: {summary['trigger_type']}")
    print(f"Max Panic Intensity: {summary['max_panic_intensity']:.3f}")
    print(f"Panic Periods: {summary['panic_periods']}")
    print(f"BTC Total Return: {summary['btc_total_return_pct']:.2f}%")
    print(f"BTC Max Drawdown: {summary['btc_max_drawdown_pct']:.2f}%")
    print(f"ETH Total Return: {summary['eth_total_return_pct']:.2f}%")
    print(f"ETH Max Drawdown: {summary['eth_max_drawdown_pct']:.2f}%")
    print(f"DOGE Total Return: {summary['doge_total_return_pct']:.2f}%")
    print(f"DOGE Max Drawdown: {summary['doge_max_drawdown_pct']:.2f}%")
    print(f"DOGE Max Pump: {summary['doge_max_pump_pct']:.2f}%")
    print(f"Max Frozen Exchanges: {summary['max_frozen_exchanges']:.0f}")
    print(f"Min Exchange Liquidity: {summary['min_exchange_liquidity']:.2f}")
    print(f"Min DOGE Social Media Index: {summary['min_doge_social_media_index']:.1f}")
    print(f"Recovery Period: {summary['recovery_period']}")
    print(f"Total Liquidation Volume: ${summary['total_liquidation_volume']:,.0f}")
    print(f"Market Survived: {summary['market_survived']}")
    print(f"System Stability: {summary['system_stability']}")
    
    return results

def demo_doge_pump():
    """Run a DOGE pump scenario."""
    print("\n" + "=" * 60)
    print("DEMO 3: DOGE Pump Mania")
    print("=" * 60)
    
    # DOGE pump scenario
    model = CryptoPanicModel({
        'doge_initial_price': 0.08,           # Starting low
        'doge_social_media_factor': 2.5,      # High social media influence
        'doge_celebrity_effect': 0.6,         # Strong celebrity effect
        'doge_volatility_multiplier': 5.0,    # Very volatile
        'doge_pump_probability': 0.25,        # High pump probability
        'whale_doge_pump_power': 3.0,         # Enhanced whale pump power
        'retail_doge_fomo': 1.2,              # Strong FOMO
    })
    
    simulation_config = {
        'panic': {
            'trigger_type': 'doge_pump',
            'trigger_intensity': 0.7,
            'panic_duration': 8,
            'start_period': 1,
        }
    }
    
    results = model.simulate(simulation_config)
    
    print("\nSUMMARY:")
    summary = results['summary']
    print(f"Trigger Type: {summary['trigger_type']}")
    print(f"BTC Total Return: {summary['btc_total_return_pct']:.2f}%")
    print(f"ETH Total Return: {summary['eth_total_return_pct']:.2f}%")
    print(f"DOGE Total Return: {summary['doge_total_return_pct']:.2f}%")
    print(f"DOGE Max Pump: {summary['doge_max_pump_pct']:.2f}%")
    print(f"DOGE Max Drawdown: {summary['doge_max_drawdown_pct']:.2f}%")
    print(f"Max Frozen Exchanges: {summary['max_frozen_exchanges']:.0f}")
    print(f"Market Survived: {summary['market_survived']}")
    print(f"System Stability: {summary['system_stability']}")
    
    return results

def demo_regulatory_shock():
    """Run a regulatory shock scenario.""" 
    print("\n" + "=" * 60)
    print("DEMO 4: Regulatory Shock")
    print("=" * 60)
    
    # Regulatory shock with customized retail behavior
    model = CryptoPanicModel({
        'retail_panic_threshold': 0.03,  # Lower threshold (retail panics easier)
        'retail_sell_probability': 0.4,  # Higher sell probability
        'whale_coordination_prob': 0.3,  # Higher whale coordination
        'periods': 25,
    })
    
    simulation_config = {
        'panic': {
            'trigger_type': 'regulatory',
            'trigger_intensity': 0.6,
            'panic_duration': 6,
            'start_period': 3,
            'contagion_factor': 0.2
        }
    }
    
    results = model.simulate(simulation_config)
    
    print("\nSUMMARY:")
    summary = results['summary']
    print(f"Trigger Type: {summary['trigger_type']}")
    print(f"BTC Total Return: {summary['btc_total_return_pct']:.2f}%")
    print(f"ETH Total Return: {summary['eth_total_return_pct']:.2f}%")
    print(f"DOGE Total Return: {summary['doge_total_return_pct']:.2f}%")
    print(f"Recovery Period: {summary['recovery_period']}")
    print(f"Market Survived: {summary['market_survived']}")
    
    return results

def compare_scenarios():
    """Compare different trigger scenarios."""
    print("\n" + "=" * 60)
    print("SCENARIO COMPARISON")
    print("=" * 60)
    
    scenarios = [
        ('Whale Dump', 'whale_dump', 0.4),
        ('Exchange Halt', 'exchange_halt', 0.6),
        ('DOGE Pump', 'doge_pump', 0.5),
        ('Regulatory', 'regulatory', 0.5),
    ]
    
    results = []
    for name, trigger_type, intensity in scenarios:
        result = run_crypto_panic_scenario(trigger_type=trigger_type, intensity=intensity)
        results.append((name, result['summary']))
    
    print(f"{'Scenario':<15} {'BTC Return%':<12} {'BTC Drawdown%':<15} {'DOGE Depeg%':<12} {'Frozen Exch':<12} {'Survived':<10}")
    print("-" * 80)
    
    for name, summary in results:
        print(f"{name:<15} {summary['btc_total_return_pct']:<12.1f} "
              f"{summary['btc_max_drawdown_pct']:<15.1f} {summary['doge_max_drawdown_pct']:<12.2f} "
              f"{summary['max_frozen_exchanges']:<12.0f} {str(summary['market_survived']):<10}")

def main():
    """Run all demos."""
    logging.basicConfig(level=logging.INFO)
    
    print("Crypto Panic Model Demo")
    print("This demo shows different crypto market panic scenarios\n")
    
    try:
        # Run individual demos
        demo_simple_scenario()
        demo_severe_panic()
        demo_doge_pump()
        demo_regulatory_shock()
        
        # Compare scenarios
        compare_scenarios()
        
        print("\n" + "=" * 60)
        print("All demos completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error running demos: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 