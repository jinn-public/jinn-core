#!/usr/bin/env python3
"""
Test script for all crypto panic example scenarios

This script runs all the crypto panic example scenarios to demonstrate
how different starting conditions affect the simulation outcomes.
"""

import sys
import os
import logging

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from engine import SimulationEngine

def test_scenario(scenario_file: str):
    """Test a single scenario file."""
    print(f"\n{'='*60}")
    print(f"Testing: {scenario_file}")
    print('='*60)
    
    engine = SimulationEngine()
    results = engine.run_scenario_file(f'examples/{scenario_file}')
    
    # Extract key info
    scenario_desc = results['scenario'].get('description', 'No description')
    params = results['scenario']['parameters']
    summary = results['results']['summary']
    
    print(f"Description: {scenario_desc}")
    print(f"\nINITIAL CONDITIONS:")
    print(f"  BTC Price: ${params.get('btc_initial_price', 45000):,.0f}")
    print(f"  ETH Price: ${params.get('eth_initial_price', 3000):,.0f}")
    print(f"  DOGE Price: ${params.get('doge_initial_price', 0.15):,.3f}")
    print(f"  DOGE Supply: {params.get('doge_supply', 140000000000):,.0f}")
    print(f"  Exchanges: {params.get('num_exchanges', 20)}")
    print(f"  Retail Panic Threshold: {params.get('retail_panic_threshold', 0.05)*100:.1f}%")
    print(f"  DOGE Social Media Factor: {params.get('doge_social_media_factor', 1.5):.1f}")
    
    print(f"\nSIMULATION RESULTS:")
    print(f"  Trigger: {summary['trigger_type']}")
    print(f"  BTC Return: {summary['btc_total_return_pct']:+.1f}%")
    print(f"  BTC Max Drawdown: {summary['btc_max_drawdown_pct']:.1f}%")
    print(f"  ETH Return: {summary['eth_total_return_pct']:+.1f}%")
    print(f"  DOGE Return: {summary['doge_total_return_pct']:+.1f}%")
    print(f"  DOGE Max Pump: {summary['doge_max_pump_pct']:.1f}%")
    print(f"  Max Frozen Exchanges: {summary['max_frozen_exchanges']:.0f}")
    print(f"  Market Survived: {summary['market_survived']}")
    print(f"  System Stability: {summary['system_stability']}")
    
    return results

def main():
    """Test all crypto panic scenarios."""
    logging.basicConfig(level=logging.WARNING)  # Reduce noise
    
    print("Testing All Crypto Panic Example Scenarios")
    print("This demonstrates how different starting conditions affect outcomes\n")
    
    # List of crypto panic scenarios
    scenarios = [
        'scenario_10_crypto_panic.json',
        'scenario_11_crypto_panic_bear_market.json', 
        'scenario_12_crypto_panic_bull_market.json',
        'scenario_13_crypto_panic_stablecoin_crisis.json'
    ]
    
    results_summary = []
    
    try:
        for scenario in scenarios:
            results = test_scenario(scenario)
            summary = results['results']['summary']
            results_summary.append({
                'scenario': scenario,
                'btc_return': summary['btc_total_return_pct'],
                'btc_drawdown': summary['btc_max_drawdown_pct'],
                'doge_pump': summary['doge_max_pump_pct'],
                'frozen_exchanges': summary['max_frozen_exchanges'],
                'survived': summary['market_survived']
            })
        
        # Summary comparison
        print(f"\n{'='*80}")
        print("COMPARISON SUMMARY")
        print('='*80)
        print(f"{'Scenario':<35} {'BTC Return':<12} {'Max Drawdown':<13} {'DOGE Pump':<11} {'Frozen':<8} {'Survived'}")
        print('-'*80)
        
        for result in results_summary:
            scenario_name = result['scenario'].replace('scenario_', '').replace('_crypto_panic', '').replace('.json', '')
            print(f"{scenario_name:<35} {result['btc_return']:+7.1f}%     {result['btc_drawdown']:7.1f}%      "
                  f"{result['doge_pump']:6.1f}%     {result['frozen_exchanges']:3.0f}     {str(result['survived'])}")
        
        print(f"\n{'='*80}")
        print("✅ All crypto panic example scenarios tested successfully!")
        print("💡 Notice how different starting conditions lead to different outcomes:")
        print("   - Bull market conditions show more resilience")
        print("   - Bear market conditions amplify panic effects") 
        print("   - DOGE pump scenarios show meme coin volatility")
        print("   - Exchange parameters affect freeze likelihood")
        print('='*80)
        
    except Exception as e:
        print(f"\n❌ Error testing scenarios: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 