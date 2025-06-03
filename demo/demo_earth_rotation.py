#!/usr/bin/env python3
"""
Earth Rotation Shock Simulation Demo

Demonstrates the Earth rotation shock simulation capabilities of Jinn-Core,
modeling the economic and societal impacts of changes in Earth's rotation speed.
"""

import logging
from src.engine import SimulationEngine
from src.models.earth_rotation_shock import simulate_earth_rotation_shock

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def demo_simple_function():
    """Demonstrate the simple Earth rotation shock function."""
    print("🌍 EARTH ROTATION SHOCK - Simple Function Demo")
    print("=" * 65)
    
    # Scenario: 10% increase in Earth's rotation speed
    print("\n📊 Scenario: 10% Faster Earth Rotation")
    print("- Current Day Length: 24 hours")
    print("- New Day Length: 21.6 hours (10% faster rotation)")
    print("- Initial Global GDP: $100 trillion")
    print("- GDP Day/Night Dependency: 30%")
    print("- Infrastructure Adaptability: 50%")
    print("- Agricultural Sensitivity: 70%")
    print("- Climate Volatility Multiplier: 1.2x")
    
    result = simulate_earth_rotation_shock(
        rotation_change_percent=10.0,
        initial_gdp=100_000_000_000_000,  # $100 trillion
        gdp_day_night_dependency=0.3,
        infrastructure_adaptability=0.5,
        agricultural_sensitivity=0.7,
        climate_volatility_multiplier=1.2
    )
    
    print(f"\n📈 Physical & Economic Impact Results:")
    print(f"- New Day Length: {result['new_day_length_hours']:.1f} hours")
    print(f"- Initial GDP Loss: {result['initial_gdp_loss']:.1f}%")
    print(f"- Long-term GDP Loss: {result['long_term_gdp_loss']:.1f}%")
    print(f"- Adaptation Time: {result['adaptation_time_years']:.1f} years")
    print(f"- Sea Level Shift: {result['sea_level_shift_meters']:.1f} meters")
    print(f"- Climate Volatility Index: {result['climate_volatility_index']:.2f}")
    print(f"- Labor Productivity Change: {result['labor_productivity_change']:.1f}%")
    print(f"- Circadian Stress Index: {result['circadian_stress_index']:.2f}")
    print(f"- Sea Wave Intensity Change: {result['sea_wave_intensity_change']:.1f}%")
    print(f"- Population Drop: {result['population_drop_percent']:.1f}%")
    
    return result

def demo_rotation_scenarios():
    """Compare different rotation speed change scenarios."""
    print("\n\n🔄 ROTATION SCENARIOS - Speed Change Comparison")
    print("=" * 65)
    
    scenarios = [
        ("Minor Speed Change", 2.0),
        ("Moderate Speed Change", 5.0),
        ("Major Speed Change", 10.0),
        ("Extreme Speed Change", 20.0),
        ("Catastrophic Speed Change", 50.0)
    ]
    
    print("\n📋 Comparing different rotation speed changes:")
    
    for name, rotation_change in scenarios:
        result = simulate_earth_rotation_shock(
            rotation_change_percent=rotation_change,
            initial_gdp=100_000_000_000_000,
            gdp_day_night_dependency=0.3,
            infrastructure_adaptability=0.5,
            agricultural_sensitivity=0.7,
            climate_volatility_multiplier=1.2
        )
        
        print(f"\n🔸 {name} ({rotation_change}% faster):")
        print(f"  - New Day Length: {result['new_day_length_hours']:.1f} hours")
        print(f"  - Initial GDP Loss: {result['initial_gdp_loss']:.1f}%")
        print(f"  - Adaptation Time: {result['adaptation_time_years']:.1f} years")
        print(f"  - Population Impact: {result['population_drop_percent']:.1f}%")

def demo_adaptation_scenarios():
    """Compare different adaptation capability scenarios."""
    print("\n\n🏗️ ADAPTATION SCENARIOS - Infrastructure & Agricultural Resilience")
    print("=" * 65)
    
    scenarios = [
        ("Low Adaptability", 0.2, 0.9),      # Poor infrastructure, high ag sensitivity
        ("Medium Adaptability", 0.5, 0.7),   # Default scenario
        ("High Adaptability", 0.8, 0.4),     # Good infrastructure, low ag sensitivity
        ("Ultra Adaptability", 0.95, 0.1)    # Excellent infrastructure, minimal ag sensitivity
    ]
    
    print("\n📋 Comparing adaptation capabilities for 10% rotation increase:")
    
    for name, infra_adapt, ag_sens in scenarios:
        result = simulate_earth_rotation_shock(
            rotation_change_percent=10.0,
            initial_gdp=100_000_000_000_000,
            gdp_day_night_dependency=0.3,
            infrastructure_adaptability=infra_adapt,
            agricultural_sensitivity=ag_sens,
            climate_volatility_multiplier=1.2
        )
        
        print(f"\n🔸 {name}:")
        print(f"  - Infrastructure Adaptability: {infra_adapt*100:.0f}%")
        print(f"  - Agricultural Sensitivity: {ag_sens*100:.0f}%")
        print(f"  - Initial GDP Loss: {result['initial_gdp_loss']:.1f}%")
        print(f"  - Long-term GDP Loss: {result['long_term_gdp_loss']:.1f}%")
        print(f"  - Adaptation Time: {result['adaptation_time_years']:.1f} years")

def demo_full_simulation():
    """Demonstrate the full Earth rotation shock simulation."""
    print("\n\n🎯 EARTH ROTATION SHOCK - Full Model Demo")
    print("=" * 65)
    
    engine = SimulationEngine()
    print(f"🔧 Available Models: {', '.join(engine.models.keys())}")
    
    print("\n📋 Running Scenario: 10% Earth Rotation Speed Increase")
    print("- 30-year simulation")
    print("- Day length: 24h → 21.6h")
    print("- 30% GDP day/night dependency")
    print("- 50% infrastructure adaptability")
    print("- 70% agricultural sensitivity")
    print("- 1.2x climate volatility multiplier")
    print("- Comprehensive adaptation dynamics")
    
    # Run the simulation
    results = engine.run_scenario_file('examples/scenario_06_earth_rotation.json')
    
    # Extract key results
    simulation_results = results['results']
    summary = simulation_results['summary']
    
    print(f"\n📊 Simulation Results:")
    print(f"- New Day Length: {summary['new_day_length_hours']:.1f} hours")
    print(f"- Day Length Change: {summary['day_length_change_percent']:.1f}%")
    print(f"- Peak GDP Decline: {summary['peak_gdp_decline']:.1f}%")
    print(f"- Total GDP Loss: {summary['total_gdp_loss']:.1f}%")
    print(f"- Final GDP Level: {summary['final_gdp_level']:.1f}% of initial")
    print(f"- Min Agricultural Productivity: {summary['min_agricultural_productivity']:.1f}%")
    print(f"- Final Agricultural Productivity: {summary['final_agricultural_productivity']:.1f}%")
    print(f"- Min Infrastructure Adaptation: {summary['min_infrastructure_adaptation']:.1f}%")
    print(f"- Final Infrastructure Adaptation: {summary['final_infrastructure_adaptation']:.1f}%")
    print(f"- Total Population Decline: {summary['total_population_decline']:.1f}%")
    print(f"- Final Population Level: {summary['final_population_level']:.1f}%")
    
    # Physical effects
    print(f"\n🌊 Physical Effects:")
    print(f"- Max Sea Level Shift: {summary['max_sea_level_shift']:.1f} meters")
    print(f"- Max Climate Volatility: {summary['max_climate_volatility']:.2f}")
    print(f"- Max Circadian Stress: {summary['max_circadian_stress']:.2f}")
    
    # Adaptation assessment
    print(f"\n🔄 Adaptation Assessment:")
    print(f"- Severity: {summary['severity_assessment']}")
    print(f"- Adaptation Completion: Year {summary['adaptation_completion_year']}")
    
    # Final assessment from simple function
    final_assessment = summary['final_assessment']
    print(f"\n📋 Final Assessment:")
    print(f"- Day Length: {final_assessment['new_day_length_hours']:.1f} hours")
    print(f"- Economic Impact: {final_assessment['initial_gdp_loss']:.1f}% initial loss")
    print(f"- Long-term Impact: {final_assessment['long_term_gdp_loss']:.1f}% permanent loss")
    print(f"- Adaptation Challenge: {final_assessment['adaptation_time_years']:.1f} years")
    print(f"- Physical Impact: {final_assessment['sea_level_shift_meters']:.1f}m sea level shift")
    
    # Show time series highlights
    periods = simulation_results['periods']
    day_lengths = simulation_results['day_length_hours']
    gdp_growth = simulation_results['gdp_growth']
    ag_productivity = simulation_results['agricultural_productivity']
    adaptation_progress = simulation_results['adaptation_progress']
    
    print(f"\n📈 Timeline Highlights (First 15 Years):")
    for i in range(min(15, len(periods))):
        day_len = day_lengths[i]
        growth = gdp_growth[i] * 100
        ag_prod = ag_productivity[i] * 100
        adapt = adaptation_progress[i] * 100
        print(f"  Year {i}: Day {day_len:.1f}h | Growth {growth:.1f}% | Agriculture {ag_prod:.0f}% | Adaptation {adapt:.0f}%")
    
    return results

def demo_extreme_scenarios():
    """Analyze extreme rotation change scenarios."""
    print("\n\n⚠️ EXTREME SCENARIOS - Catastrophic Rotation Changes")
    print("=" * 65)
    
    print("\n📊 Extreme Rotation Scenarios:")
    
    # Extreme scenarios
    scenarios = [
        ("Double Speed (12h days)", 100.0),
        ("Triple Speed (8h days)", 200.0),
        ("Quadruple Speed (6h days)", 300.0)
    ]
    
    for name, rotation_change in scenarios:
        result = simulate_earth_rotation_shock(
            rotation_change_percent=rotation_change,
            initial_gdp=100_000_000_000_000,
            gdp_day_night_dependency=0.3,
            infrastructure_adaptability=0.5,
            agricultural_sensitivity=0.7,
            climate_volatility_multiplier=1.2
        )
        
        print(f"\n🔸 {name}:")
        print(f"  - New Day Length: {result['new_day_length_hours']:.1f} hours")
        print(f"  - Initial GDP Loss: {result['initial_gdp_loss']:.1f}%")
        print(f"  - Sea Level Shift: {result['sea_level_shift_meters']:.1f} meters")
        print(f"  - Population Impact: {result['population_drop_percent']:.1f}%")
        print(f"  - Adaptation Time: {result['adaptation_time_years']:.1f} years")
        print(f"  - Survivability: {'Questionable' if result['population_drop_percent'] > 30 else 'Challenging' if result['population_drop_percent'] > 15 else 'Difficult'}")

def main():
    """Run the Earth rotation shock simulation demo."""
    print("🚀 Jinn-Core Earth Rotation Shock Simulation Demo")
    print("Analyzing the economic and societal impacts of planetary rotation changes\n")
    
    # Run demonstrations
    simple_result = demo_simple_function()
    demo_rotation_scenarios()
    demo_adaptation_scenarios()
    full_result = demo_full_simulation()
    demo_extreme_scenarios()
    
    print("\n" + "=" * 65)
    print("✅ Earth Rotation Shock Simulation Demo Complete!")
    print("\nKey Insights:")
    print("- Even small rotation changes (2-5%) have significant economic impacts")
    print("- 10% rotation increase shortens days to 21.6h with major disruption")
    print("- Agricultural systems are highly vulnerable to day length changes")
    print("- Infrastructure adaptability is crucial for economic resilience")
    print("- Circadian disruption affects labor productivity substantially")
    print("- Sea level and climate changes compound economic impacts")
    print("- Adaptation takes 10-20 years even with good infrastructure")
    print("- Extreme scenarios (>50% speed increase) threaten civilization")
    print("- Early preparation and adaptive infrastructure are critical")

if __name__ == "__main__":
    main() 