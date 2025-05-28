#!/usr/bin/env python3
"""
Jinn-Core Demo Script

This script demonstrates how to use the Jinn-Core economic simulation engine
to run interest rate shock scenarios and analyze the results.
"""

import sys
import os
import json
import logging

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from engine import SimulationEngine
from utils.formatters import format_simulation_summary, format_time_series


def main():
    """Run the demonstration."""
    print("=" * 60)
    print("JINN-CORE ECONOMIC SIMULATION ENGINE DEMO")
    print("=" * 60)
    
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        # Initialize the simulation engine
        print("\n1. Initializing Simulation Engine...")
        engine = SimulationEngine()
        print(f"   Available models: {list(engine.models.keys())}")
        
        # Load and run the example scenario
        print("\n2. Loading Example Scenario...")
        scenario_path = "examples/scenario_01.json"
        
        if not os.path.exists(scenario_path):
            print(f"   Error: Scenario file not found: {scenario_path}")
            return
        
        with open(scenario_path, 'r') as f:
            scenario = json.load(f)
        
        print(f"   Scenario: {scenario['name']}")
        print(f"   Description: {scenario['description']}")
        
        shock = scenario['simulation']['shock']
        print(f"   Shock: {shock['magnitude']*10000:.0f} basis points for {shock['duration']} periods")
        
        # Run the simulation
        print("\n3. Running Simulation...")
        results = engine.run_simulation(scenario)
        
        # Display formatted results
        print("\n4. Simulation Results:")
        summary = format_simulation_summary(results)
        print(summary)
        
        # Show time series data (first 10 periods)
        print("\n5. Time Series Data (First 10 Periods):")
        time_series_data = {
            'Period': results['results']['periods'][:10],
            'Rate Shock (bp)': [x*10000 for x in results['results']['interest_rate_shock'][:10]],
            'GDP Growth (%)': [x*100 for x in results['results']['gdp_growth'][:10]],
            'Inflation (%)': [x*100 for x in results['results']['inflation'][:10]]
        }
        
        table = format_time_series(time_series_data, "Key Economic Indicators")
        print(table)
        
        # Show how to create custom scenarios
        print("\n6. Custom Scenario Example:")
        custom_scenario = {
            'model': 'interest_rate',
            'parameters': {
                'periods': 12,
                'gdp_sensitivity': -0.4,  # More sensitive economy
                'baseline_gdp_growth': 0.02
            },
            'simulation': {
                'shock': {
                    'magnitude': 0.005,  # 50 basis points
                    'duration': 6,
                    'start_period': 1
                }
            }
        }
        
        print("   Running custom scenario (50bp shock, high sensitivity)...")
        custom_results = engine.run_simulation(custom_scenario)
        custom_summary = format_simulation_summary(custom_results)
        print(custom_summary)
        
        # Export results
        print("\n7. Exporting Results...")
        
        # Export to JSON
        output_file = "demo_results.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"   Results exported to: {output_file}")
        
        # Show how to access specific data
        print("\n8. Accessing Specific Data:")
        gdp_data = results['results']['gdp_growth']
        min_gdp = min(gdp_data)
        max_gdp = max(gdp_data)
        avg_gdp = sum(gdp_data) / len(gdp_data)
        
        print(f"   GDP Growth Analysis:")
        print(f"     Average: {avg_gdp*100:.2f}%")
        print(f"     Minimum: {min_gdp*100:.2f}%")
        print(f"     Maximum: {max_gdp*100:.2f}%")
        print(f"     Impact: {(min_gdp - scenario['parameters']['baseline_gdp_growth'])*100:.2f}pp")
        
        print("\n" + "=" * 60)
        print("DEMO COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
        print("\nNext Steps:")
        print("- Modify examples/scenario_01.json to test different scenarios")
        print("- Run tests with: python -m pytest tests/")
        print("- Check docs/roadmap.md for future development plans")
        
    except Exception as e:
        print(f"\nError during demo: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 