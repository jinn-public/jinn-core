#!/usr/bin/env python3
"""
Global Conflict Simulation Demo

Demonstrates the global conflict simulation capabilities of Jinn-Core,
modeling the comprehensive economic impacts of large-scale warfare.
"""

import logging
from src.engine import SimulationEngine
from src.models.global_conflict import simulate_global_conflict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def demo_simple_function():
    """Demonstrate the simple global conflict function."""
    print("⚔️ GLOBAL CONFLICT - Simple Function Demo")
    print("=" * 65)
    
    # Scenario: Large-scale global conflict
    print("\n📊 Scenario: Large-Scale Global War")
    print("- Initial Global GDP: $100 trillion")
    print("- Military Spending Jump: +5% of GDP annually")
    print("- Trade Disruption: 40% of global trade")
    print("- Conflict Duration: 5 years")
    print("- Inflation Surge: 10% initial spike")
    print("- Workforce Loss: 5% annually")
    print("- Infrastructure Destruction: 10% annually")
    
    result = simulate_global_conflict(
        initial_gdp=100_000_000_000_000,  # $100 trillion
        military_spending_jump=0.05,      # 5% of GDP
        global_trade_disruption=0.4,      # 40% trade disruption
        conflict_duration_years=5,
        inflation_surge_rate=0.1,         # 10% inflation spike
        human_capital_loss=0.05,          # 5% workforce loss
        infrastructure_destruction=0.1    # 10% infrastructure loss
    )
    
    print(f"\n📈 Economic Impact Results:")
    print(f"- Total Military Spending: ${result['total_military_spending']/1e12:.1f} trillion")
    print(f"- GDP Impact: {result['gdp_impact']:.1f}%")
    print(f"- Trade Volume Lost: ${result['trade_loss']/1e12:.1f} trillion")
    print(f"- Peak Inflation: {result['inflation_peak']:.1f}%")
    print(f"- Workforce Reduction: {result['workforce_reduction']:.1f}%")
    print(f"- Infrastructure Loss: {result['infrastructure_loss']:.1f}%")
    print(f"- Public Debt Increase: {result['debt_increase']:.1f}% of GDP")
    print(f"- Social Stability Index: {result['social_stability_index']:.2f} (0=chaos, 1=stable)")
    
    return result

def demo_conflict_scenarios():
    """Compare different conflict intensity scenarios."""
    print("\n\n🌍 CONFLICT SCENARIOS - Intensity Comparison")
    print("=" * 65)
    
    scenarios = [
        ("Limited Regional Conflict", 0.02, 0.15, 2, 0.03, 0.02, 0.03),
        ("Major Regional War", 0.035, 0.25, 3, 0.06, 0.035, 0.06),
        ("Global Conflict", 0.05, 0.4, 5, 0.1, 0.05, 0.1),
        ("World War Scale", 0.08, 0.6, 6, 0.15, 0.08, 0.15)
    ]
    
    print("\n📋 Comparing different conflict scenarios:")
    
    for name, mil_jump, trade_disr, duration, inflation, workforce, infra in scenarios:
        result = simulate_global_conflict(
            initial_gdp=100_000_000_000_000,
            military_spending_jump=mil_jump,
            global_trade_disruption=trade_disr,
            conflict_duration_years=duration,
            inflation_surge_rate=inflation,
            human_capital_loss=workforce,
            infrastructure_destruction=infra
        )
        
        print(f"\n🔸 {name}:")
        print(f"  - GDP Impact: {result['gdp_impact']:.1f}%")
        print(f"  - Peak Inflation: {result['inflation_peak']:.1f}%")
        print(f"  - Debt Increase: {result['debt_increase']:.1f}% of GDP")
        print(f"  - Social Stability: {result['social_stability_index']:.2f}")

def demo_full_simulation():
    """Demonstrate the full global conflict simulation."""
    print("\n\n🎯 GLOBAL CONFLICT - Full Model Demo")
    print("=" * 65)
    
    engine = SimulationEngine()
    print(f"🔧 Available Models: {', '.join(engine.models.keys())}")
    
    print("\n📋 Running Scenario: Large-Scale Global Conflict")
    print("- 15-period simulation (years)")
    print("- 5% GDP military spending increase")
    print("- 40% global trade disruption")
    print("- 5-year conflict duration")
    print("- 10% inflation surge")
    print("- 5% annual workforce loss")
    print("- 10% annual infrastructure destruction")
    print("- Post-conflict recovery dynamics")
    
    # Run the simulation
    results = engine.run_scenario_file('examples/scenario_05_global_conflict.json')
    
    # Extract key results
    simulation_results = results['results']
    summary = simulation_results['summary']
    
    print(f"\n📊 Simulation Results:")
    print(f"- Total GDP Loss: {summary['total_gdp_loss']:.1f}%")
    print(f"- Peak GDP Decline: {summary['peak_gdp_decline']:.1f}%")
    print(f"- Final GDP Level: {summary['final_gdp_level']:.1f}% of initial")
    print(f"- Peak Inflation: {summary['peak_inflation']:.1f}%")
    print(f"- Maximum Debt Ratio: {summary['max_debt_ratio']:.1f}% of GDP")
    print(f"- Minimum Social Stability: {summary['min_social_stability']:.2f}")
    print(f"- Total Workforce Loss: {summary['total_workforce_loss']:.1f}%")
    print(f"- Total Infrastructure Loss: {summary['total_infrastructure_loss']:.1f}%")
    print(f"- Trade Volume Loss: {summary['trade_volume_loss']:.1f}%")
    
    # Conflict assessment
    print(f"\n🎯 Conflict Assessment:")
    print(f"- Conflict Severity: {summary['conflict_severity']}")
    print(f"- Recovery Time: {summary['recovery_years']} years")
    print(f"- Peak Refugee Population: {summary['peak_refugee_population']:.1f}% of workforce")
    print(f"- Total Reconstruction Cost: ${summary['total_reconstruction_cost']:.1f} trillion")
    
    # Final assessment from simple function
    final_assessment = summary['final_assessment']
    print(f"\n📋 Final Assessment:")
    print(f"- Military Spending: ${final_assessment['total_military_spending']/1e12:.1f} trillion")
    print(f"- Economic Devastation: {final_assessment['gdp_impact']:.1f}% GDP loss")
    print(f"- Trade Collapse: ${final_assessment['trade_loss']/1e12:.1f} trillion lost")
    print(f"- Social Collapse Risk: {1-final_assessment['social_stability_index']:.2f}")
    
    # Show time series highlights
    periods = simulation_results['periods']
    conflict_active = simulation_results['conflict_active']
    military_spending = simulation_results['military_spending_percent']
    gdp_growth = simulation_results['gdp_growth']
    inflation_rate = simulation_results['inflation_rate']
    social_stability = simulation_results['social_stability_index']
    
    print(f"\n📈 Timeline Highlights (First 10 Years):")
    for i in range(min(10, len(periods))):
        status = "🔥 WAR" if conflict_active[i] else "🕊️ PEACE"
        mil_pct = military_spending[i] * 100
        growth = gdp_growth[i] * 100
        inflation = inflation_rate[i] * 100
        stability = social_stability[i]
        print(f"  Year {i}: {status} | Military {mil_pct:.1f}% | Growth {growth:.1f}% | Inflation {inflation:.1f}% | Stability {stability:.2f}")
    
    return results

def demo_recovery_analysis():
    """Analyze post-conflict recovery patterns."""
    print("\n\n🔄 POST-CONFLICT RECOVERY ANALYSIS")
    print("=" * 65)
    
    print("\n📊 Recovery Scenarios:")
    
    # Different conflict durations
    durations = [2, 3, 5, 7]
    
    for duration in durations:
        result = simulate_global_conflict(
            initial_gdp=100_000_000_000_000,
            military_spending_jump=0.05,
            global_trade_disruption=0.4,
            conflict_duration_years=duration,
            inflation_surge_rate=0.1,
            human_capital_loss=0.05,
            infrastructure_destruction=0.1
        )
        
        print(f"\n🔸 {duration}-Year Conflict:")
        print(f"  - GDP Impact: {result['gdp_impact']:.1f}%")
        print(f"  - Infrastructure Loss: {result['infrastructure_loss']:.1f}%")
        print(f"  - Social Stability: {result['social_stability_index']:.2f}")
        print(f"  - Recovery Complexity: {'High' if duration > 4 else 'Medium' if duration > 2 else 'Low'}")

def main():
    """Run the global conflict simulation demo."""
    print("🚀 Jinn-Core Global Conflict Simulation Demo")
    print("Analyzing the comprehensive economic impacts of large-scale warfare\n")
    
    # Run demonstrations
    simple_result = demo_simple_function()
    demo_conflict_scenarios()
    full_result = demo_full_simulation()
    demo_recovery_analysis()
    
    print("\n" + "=" * 65)
    print("✅ Global Conflict Simulation Demo Complete!")
    print("\nKey Insights:")
    print("- Large-scale conflicts cause catastrophic economic damage (-20%+ GDP)")
    print("- Military spending escalation creates massive fiscal burdens")
    print("- Trade disruption amplifies economic contraction globally")
    print("- Human capital and infrastructure losses compound over time")
    print("- Social stability deteriorates rapidly under economic stress")
    print("- Recovery takes many years even after conflict ends")
    print("- Early intervention and peace-building are economically critical")
    print("- Reconstruction costs can exceed original conflict spending")

if __name__ == "__main__":
    main() 