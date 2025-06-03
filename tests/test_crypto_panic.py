#!/usr/bin/env python3
"""
Test script for Crypto Panic Model integration with Jinn Engine

This script tests the crypto panic model through the main Jinn engine
to ensure proper integration and JSON scenario support.
"""

import sys
import os
import json
import logging

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from engine import SimulationEngine

def test_basic_integration():
    """Test basic crypto panic model integration with Jinn engine."""
    print("Testing Crypto Panic Model integration with Jinn Engine...")
    
    # Initialize engine
    engine = SimulationEngine()
    
    # Verify model is registered
    assert 'crypto_panic' in engine.models, "Crypto panic model not registered"
    print("✓ Crypto panic model successfully registered")
    
    # Test basic scenario
    scenario = {
        "model": "crypto_panic",
        "parameters": {
            "periods": 10,
            "btc_initial_price": 40000.0,
            "eth_initial_price": 2500.0
        },
        "simulation": {
            "panic": {
                "trigger_type": "whale_dump",
                "trigger_intensity": 0.3,
                "panic_duration": 5,
                "start_period": 1
            }
        }
    }
    
    # Run simulation
    results = engine.run_simulation(scenario)
    
    # Verify results structure
    assert 'model' in results
    assert results['model'] == 'crypto_panic'
    assert 'results' in results
    assert 'summary' in results['results']
    
    summary = results['results']['summary']
    assert 'trigger_type' in summary
    assert 'btc_total_return_pct' in summary
    assert 'market_survived' in summary
    
    print("✓ Basic simulation completed successfully")
    print(f"  - Trigger: {summary['trigger_type']}")
    print(f"  - BTC Return: {summary['btc_total_return_pct']:.2f}%")
    print(f"  - Market Survived: {summary['market_survived']}")
    
    return results

def test_json_scenario():
    """Test loading and running a crypto panic scenario from JSON."""
    print("\nTesting JSON scenario loading...")
    
    # Create a test scenario file
    scenario_data = {
        "model": "crypto_panic",
        "description": "Test USDT depeg scenario",
        "parameters": {
            "periods": 15,
            "btc_initial_price": 45000.0,
            "eth_initial_price": 3000.0,
            "usdt_supply": 90000000000,
            "stablecoin_intervention_power": 0.6,
            "backing_asset_quality": 0.8,
            "num_exchanges": 15
        },
        "simulation": {
            "panic": {
                "trigger_type": "usdt_depeg",
                "trigger_intensity": 0.5,
                "panic_duration": 8,
                "start_period": 2,
                "contagion_factor": 0.2
            }
        }
    }
    
    # Save to file
    scenario_path = "test_crypto_panic_scenario.json"
    with open(scenario_path, 'w') as f:
        json.dump(scenario_data, f, indent=2)
    
    # Load and run via engine
    engine = SimulationEngine()
    results = engine.run_scenario_file(scenario_path)
    
    # Verify results
    assert results['model'] == 'crypto_panic'
    summary = results['results']['summary']
    
    print("✓ JSON scenario loaded and executed successfully")
    print(f"  - Scenario: {scenario_data['description']}")
    print(f"  - Trigger: {summary['trigger_type']}")
    print(f"  - USDT Max Depeg: {summary['usdt_max_depeg_pct']:.2f}%")
    print(f"  - Max Frozen Exchanges: {summary['max_frozen_exchanges']}")
    print(f"  - System Stability: {summary['system_stability']}")
    
    # Cleanup
    os.remove(scenario_path)
    
    return results

def test_extreme_scenarios():
    """Test extreme panic scenarios."""
    print("\nTesting extreme panic scenarios...")
    
    engine = SimulationEngine()
    
    scenarios = [
        {
            "name": "Extreme Exchange Halt",
            "config": {
                "model": "crypto_panic",
                "parameters": {"periods": 12},
                "simulation": {
                    "panic": {
                        "trigger_type": "exchange_halt",
                        "trigger_intensity": 0.9,
                        "panic_duration": 8,
                        "start_period": 1
                    }
                }
            }
        },
        {
            "name": "Mild Regulatory Pressure",
            "config": {
                "model": "crypto_panic",
                "parameters": {"periods": 20},
                "simulation": {
                    "panic": {
                        "trigger_type": "regulatory",
                        "trigger_intensity": 0.2,
                        "panic_duration": 3,
                        "start_period": 5
                    }
                }
            }
        }
    ]
    
    for scenario in scenarios:
        print(f"\n  Testing: {scenario['name']}")
        results = engine.run_simulation(scenario['config'])
        summary = results['results']['summary']
        
        print(f"    - BTC Drawdown: {summary['btc_max_drawdown_pct']:.1f}%")
        print(f"    - Market Survived: {summary['market_survived']}")
        print(f"    - Max Panic: {summary['max_panic_intensity']:.3f}")
    
    print("✓ Extreme scenarios completed")

def test_simple_function():
    """Test the simple simulate_crypto_panic function."""
    print("\nTesting simple function interface...")
    
    from models.crypto_panic import simulate_crypto_panic
    
    result = simulate_crypto_panic(
        btc_price=50000.0,
        eth_price=3200.0,
        usdt_supply=85000000000,
        trigger_type='whale_dump',
        panic_intensity=0.6
    )
    
    # Verify result structure
    expected_keys = ['btc_price_change', 'eth_price_change', 'usdt_peg_stability', 
                     'exchange_freeze_risk', 'liquidation_volume']
    
    for key in expected_keys:
        assert key in result, f"Missing key: {key}"
    
    print("✓ Simple function interface working")
    print(f"  - BTC Price Change: {result['btc_price_change']:.2f}%")
    print(f"  - ETH Price Change: {result['eth_price_change']:.2f}%")
    print(f"  - Exchange Freeze Risk: {result['exchange_freeze_risk']:.2f}")
    print(f"  - Liquidation Volume: ${result['liquidation_volume']:,.0f}")

def main():
    """Run all tests."""
    logging.basicConfig(level=logging.WARNING)  # Reduce noise for tests
    
    print("Crypto Panic Model Integration Tests")
    print("=" * 40)
    
    try:
        test_basic_integration()
        test_json_scenario()
        test_extreme_scenarios()
        test_simple_function()
        
        print("\n" + "=" * 40)
        print("✅ All tests passed successfully!")
        print("The crypto panic model is properly integrated with Jinn.")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 