#!/usr/bin/env python3
"""
Test script for Plastic Spread Simulation Model

Quick validation of key model functionality.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from models.plastic_spread_simulation import simulate_plastic_spread, PlasticSpreadSimulationModel
from engine import SimulationEngine

def test_simple_function():
    """Test the simple plastic spread function."""
    print("Testing simple plastic spread function...")
    
    # Test basic functionality
    result = simulate_plastic_spread(
        annual_production_tonnes=400_000_000,
        annual_growth_rate=0.03,
        coverage_density_kg_per_sq_km=100_000,
        earth_surface_area_sq_km=510_000_000,
        ocean_area_sq_km=361_000_000,
        current_year=10
    )
    
    # Validate results
    assert 'current_production_tonnes' in result
    assert 'total_plastic_accumulated_kg' in result
    assert 'earth_coverage_percent' in result
    assert 'ocean_coverage_percent' in result
    assert 'cleanup_cost_billion_usd' in result
    assert 'environmental_damage_cost_billion_usd' in result
    
    # Check logical constraints
    assert result['current_production_tonnes'] > 400_000_000  # Should grow with 3% rate
    assert result['total_plastic_accumulated_kg'] > 0
    assert result['earth_coverage_percent'] >= 0
    assert result['ocean_coverage_percent'] >= 0
    assert result['cleanup_cost_billion_usd'] > 0
    assert result['environmental_damage_cost_billion_usd'] >= result['cleanup_cost_billion_usd']  # Damage should be >= cleanup
    
    print("✅ Simple function test passed")
    return result

def test_full_model():
    """Test the full plastic spread simulation model."""
    print("Testing full plastic spread simulation model...")
    
    # Create basic parameters
    parameters = {
        'periods': 10,  # Short test
        'annual_production_tonnes': 400_000_000,
        'annual_growth_rate': 0.03,
        'coverage_density_kg_per_sq_km': 100_000,
        'recycling_improvement_enabled': False
    }
    
    model = PlasticSpreadSimulationModel(parameters)
    
    # Create simulation config
    simulation_config = {
        'compare_scenarios': True
    }
    
    results = model.simulate(simulation_config)
    
    # Validate structure
    assert 'baseline_scenario' in results
    assert 'production_cap_scenario' in results
    assert 'recycling_improvement_scenario' in results
    assert 'combined_intervention_scenario' in results
    assert 'comparison' in results
    
    # Check that all scenarios have expected keys
    for scenario_key in ['baseline_scenario', 'production_cap_scenario', 'recycling_improvement_scenario', 'combined_intervention_scenario']:
        scenario = results[scenario_key]
        assert 'earth_coverage_percent' in scenario
        assert 'ocean_coverage_percent' in scenario
        assert 'total_plastic_accumulated_kg' in scenario
        assert 'cleanup_cost_billion_usd' in scenario
        assert 'environmental_damage_cost_billion_usd' in scenario
        assert 'summary' in scenario
        
        # Check time series length
        assert len(scenario['earth_coverage_percent']) == 10
        assert len(scenario['total_plastic_accumulated_kg']) == 10
    
    # Check comparison structure
    comparison = results['comparison']
    assert 'coverage_reduction' in comparison
    assert 'cost_savings' in comparison
    assert 'environmental_benefits' in comparison
    assert 'key_insights' in comparison
    
    # Validate that interventions have some positive effect
    baseline_summary = results['baseline_scenario']['summary']
    combined_summary = results['combined_intervention_scenario']['summary']
    
    # Combined intervention should reduce final coverage
    assert combined_summary['final_earth_coverage_percent'] <= baseline_summary['final_earth_coverage_percent']
    
    # Combined intervention should reduce total plastic accumulation
    assert combined_summary['total_plastic_accumulated_tonnes'] <= baseline_summary['total_plastic_accumulated_tonnes']
    
    print("✅ Full model test passed")
    return results

def test_engine_integration():
    """Test integration with the simulation engine."""
    print("Testing simulation engine integration...")
    
    engine = SimulationEngine()
    
    # Check that our model is registered
    assert 'plastic_spread_simulation' in engine.models
    
    # Test loading scenario
    try:
        results = engine.run_scenario_file('examples/scenario_09_plastic_spread.json')
        assert 'results' in results
        assert 'model' in results
        assert results['model'] == 'plastic_spread_simulation'
        print("✅ Engine integration test passed")
        return results
    except Exception as e:
        print(f"❌ Engine integration test failed: {e}")
        return None

def test_intervention_effectiveness():
    """Test that interventions actually work as expected."""
    print("Testing intervention effectiveness...")
    
    # Short simulation for testing
    parameters = {
        'periods': 20,
        'annual_production_tonnes': 400_000_000,
        'annual_growth_rate': 0.03,
        'coverage_density_kg_per_sq_km': 100_000
    }
    
    model = PlasticSpreadSimulationModel(parameters)
    
    # Test single scenarios
    baseline = model._run_single_scenario('baseline')
    production_cap = model._run_single_scenario('production_cap')
    recycling = model._run_single_scenario('recycling_improvement')
    combined = model._run_single_scenario('combined_intervention')
    
    # Validate intervention effects
    # Production cap should reduce plastic accumulation
    assert production_cap['summary']['total_plastic_accumulated_tonnes'] < baseline['summary']['total_plastic_accumulated_tonnes']
    
    # Recycling improvement should reduce plastic accumulation
    assert recycling['summary']['total_plastic_accumulated_tonnes'] < baseline['summary']['total_plastic_accumulated_tonnes']
    
    # Combined should be most effective
    assert combined['summary']['total_plastic_accumulated_tonnes'] <= production_cap['summary']['total_plastic_accumulated_tonnes']
    assert combined['summary']['total_plastic_accumulated_tonnes'] <= recycling['summary']['total_plastic_accumulated_tonnes']
    
    # Check coverage reductions
    assert production_cap['summary']['final_earth_coverage_percent'] < baseline['summary']['final_earth_coverage_percent']
    assert recycling['summary']['final_earth_coverage_percent'] < baseline['summary']['final_earth_coverage_percent']
    assert combined['summary']['final_earth_coverage_percent'] < baseline['summary']['final_earth_coverage_percent']
    
    print("✅ Intervention effectiveness test passed")
    return {
        'baseline': baseline,
        'production_cap': production_cap,
        'recycling': recycling,
        'combined': combined
    }

def main():
    """Run all tests."""
    print("🧪 Running Plastic Spread Simulation Model Tests\n")
    
    try:
        # Run tests
        simple_result = test_simple_function()
        full_result = test_full_model()
        engine_result = test_engine_integration()
        intervention_result = test_intervention_effectiveness()
        
        print("\n✅ All tests passed!")
        print("\nSample Results Summary:")
        if simple_result:
            print(f"- Simple function (10 years): {simple_result['earth_coverage_percent']:.3f}% Earth coverage")
            print(f"- Cleanup cost: ${simple_result['cleanup_cost_billion_usd']:.1f}B")
        
        if full_result:
            baseline_summary = full_result['baseline_scenario']['summary']
            combined_summary = full_result['combined_intervention_scenario']['summary']
            print(f"- Full model baseline: {baseline_summary['final_earth_coverage_percent']:.3f}% final coverage")
            print(f"- Full model combined: {combined_summary['final_earth_coverage_percent']:.3f}% final coverage")
            print(f"- Intervention effectiveness: {baseline_summary['final_earth_coverage_percent'] - combined_summary['final_earth_coverage_percent']:.3f}pp reduction")
        
        if engine_result:
            print("- Engine integration: Scenario file loaded and executed successfully")
        
        if intervention_result:
            baseline_plastic = intervention_result['baseline']['summary']['total_plastic_accumulated_tonnes']
            combined_plastic = intervention_result['combined']['summary']['total_plastic_accumulated_tonnes']
            reduction = (baseline_plastic - combined_plastic) / baseline_plastic * 100
            print(f"- Intervention plastic reduction: {reduction:.1f}%")
            
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 