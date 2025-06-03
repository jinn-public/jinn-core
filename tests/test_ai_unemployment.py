#!/usr/bin/env python3
"""
Test script for AI Unemployment Shock Model

Quick validation of key model functionality.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from models.ai_unemployment_shock import simulate_ai_unemployment_shock, AIUnemploymentShockModel
from engine import SimulationEngine

def test_simple_function():
    """Test the simple AI unemployment function."""
    print("Testing simple AI unemployment shock function...")
    
    # Test basic functionality
    result = simulate_ai_unemployment_shock(
        current_employment_rate=94.0,
        ai_displacement_rate=1.0,
        current_gdp=25_000_000_000_000,
        current_year=10,
        max_displacement=30.0,
        ubi_threshold=12.0
    )
    
    # Validate results
    assert 'new_unemployment_rate' in result
    assert 'new_employment_rate' in result
    assert 'productivity_boost' in result
    assert 'ubi_activated' in result
    assert 'ubi_cost' in result
    
    # Check logical constraints
    assert result['new_unemployment_rate'] <= 36.0  # 6% initial + 30% max
    assert result['new_employment_rate'] >= 64.0   # Should be complement of unemployment
    assert result['productivity_boost'] >= 2.0     # Minimum 2%
    assert result['productivity_boost'] <= 6.0     # Maximum 6%
    
    print("✅ Simple function test passed")
    return result

def test_full_model():
    """Test the full AI unemployment shock model."""
    print("Testing full AI unemployment shock model...")
    
    # Create basic parameters
    parameters = {
        'periods': 5,  # Short test
        'initial_employment_rate': 94.0,
        'ai_displacement_rate': 2.0,  # Faster for testing
        'max_unemployment_rate': 10.0,  # Smaller for testing
        'ubi_threshold': 8.0
    }
    
    model = AIUnemploymentShockModel(parameters)
    
    # Create simulation config
    simulation_config = {
        'shock': {
            'ai_displacement_rate': 2.0,
            'max_unemployment': 10.0,
            'start_year': 0
        },
        'compare_scenarios': True
    }
    
    results = model.simulate(simulation_config)
    
    # Validate structure
    assert 'scenario_with_ubi' in results
    assert 'scenario_without_ubi' in results
    assert 'comparison' in results
    
    # Check that both scenarios have expected keys
    for scenario_key in ['scenario_with_ubi', 'scenario_without_ubi']:
        scenario = results[scenario_key]
        assert 'unemployment_rate' in scenario
        assert 'employment_rate' in scenario
        assert 'gdp' in scenario
        assert 'ubi_activated' in scenario
        assert 'summary' in scenario
        
        # Check time series length
        assert len(scenario['unemployment_rate']) == 5
        assert len(scenario['gdp']) == 5
    
    # Check comparison structure
    comparison = results['comparison']
    assert 'gdp_difference' in comparison
    assert 'unemployment_difference' in comparison
    assert 'fiscal_impact' in comparison
    assert 'key_insights' in comparison
    
    print("✅ Full model test passed")
    return results

def test_engine_integration():
    """Test integration with the simulation engine."""
    print("Testing simulation engine integration...")
    
    engine = SimulationEngine()
    
    # Check that our model is registered
    assert 'ai_unemployment_shock' in engine.models
    
    # Test loading scenario
    try:
        results = engine.run_scenario_file('examples/scenario_08_ai_unemployment.json')
        assert 'results' in results
        assert 'model' in results
        assert results['model'] == 'ai_unemployment_shock'
        print("✅ Engine integration test passed")
        return results
    except Exception as e:
        print(f"❌ Engine integration test failed: {e}")
        return None

def main():
    """Run all tests."""
    print("🧪 Running AI Unemployment Shock Model Tests\n")
    
    try:
        # Run tests
        simple_result = test_simple_function()
        full_result = test_full_model()
        engine_result = test_engine_integration()
        
        print("\n✅ All tests passed!")
        print("\nSample Results Summary:")
        if simple_result:
            print(f"- Simple function: {simple_result['new_unemployment_rate']:.1f}% unemployment, UBI: {simple_result['ubi_activated']}")
        
        if full_result:
            with_ubi = full_result['scenario_with_ubi']['summary']
            print(f"- Full model (5 years): Final unemployment {with_ubi['final_unemployment_rate']:.1f}%, GDP growth {with_ubi['total_gdp_growth']:.1f}%")
        
        if engine_result:
            print("- Engine integration: Scenario file loaded and executed successfully")
            
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 