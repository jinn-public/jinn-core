#!/usr/bin/env python3
"""
Military Spending Shock Simulation Demo

Demonstrates the military spending shock simulation capabilities of Jinn-Core.
"""

import logging
from src.engine import SimulationEngine
from src.models.military_spending_shock import simulate_military_spending_shock

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def demo_simple_function():
    """Demonstrate the simple military spending shock function."""
    print("🎖️ MILITARY SPENDING SHOCK - Simple Function Demo")
    print("=" * 65)
    
    # Scenario: Major defense budget increase
    print("\n📊 Scenario: Defense Budget Expansion")
    print("- Initial GDP: $25 trillion")
    print("- Current Military Spending: 3% of GDP ($750B)")
    print("- Proposed Increase: +2% of GDP (+$500B)")
    print("- Initial Debt Ratio: 60% of GDP")
    print("- Fiscal Policy: Neutral")
    
    result = simulate_military_spending_shock(
        initial_gdp=25_000_000_000_000,
        military_spending_percent=0.03,
        military_spending_increase=0.02,
        debt_ratio=0.6,
        fiscal_policy="neutral"
    )
    
    print(f"\n📈 Results:")
    print(f"- New Military Spending: {result['new_military_spending_percent']:.1f}% of GDP")
    print(f"- Total Military Budget: ${result['military_spending_amount']/1e12:.1f} trillion")
    print(f"- Social Budget Impact: {result['social_budget_impact']:.1f}% of GDP (crowding out)")
    print(f"- New Debt Ratio: {result['new_debt_ratio']:.1f}% of GDP")
    print(f"- GDP Growth Boost: +{result['gdp_growth_impact']:.1f} percentage points")
    print(f"- Fiscal Multiplier: {result['fiscal_multiplier']:.1f}")
    
    return result

def demo_policy_comparison():
    """Compare different fiscal policy approaches."""
    print("\n\n🏛️ POLICY COMPARISON - Different Fiscal Approaches")
    print("=" * 65)
    
    policies = ["neutral", "stimulus", "austerity"]
    policy_names = {"neutral": "Neutral Policy", "stimulus": "Stimulus Policy", "austerity": "Austerity Policy"}
    
    print("\n📋 Comparing 2% GDP military spending increase under different policies:")
    
    for policy in policies:
        result = simulate_military_spending_shock(
            initial_gdp=25_000_000_000_000,
            military_spending_percent=0.03,
            military_spending_increase=0.02,
            debt_ratio=0.6,
            fiscal_policy=policy
        )
        
        print(f"\n🔸 {policy_names[policy]}:")
        print(f"  - GDP Growth Impact: +{result['gdp_growth_impact']:.1f}pp")
        print(f"  - Social Budget Impact: {result['social_budget_impact']:.1f}% of GDP")
        print(f"  - Debt Ratio: {result['new_debt_ratio']:.1f}% of GDP")
        print(f"  - Fiscal Multiplier: {result['fiscal_multiplier']:.1f}")

def demo_full_simulation():
    """Demonstrate the full military spending shock simulation."""
    print("\n\n🎯 MILITARY SPENDING SHOCK - Full Model Demo")
    print("=" * 65)
    
    engine = SimulationEngine()
    print(f"🔧 Available Models: {', '.join(engine.models.keys())}")
    
    print("\n📋 Running Scenario: Defense Budget Expansion")
    print("- 15-period simulation (quarters/years)")
    print("- 2% GDP military spending increase")
    print("- 8-period duration with gradual decay")
    print("- Neutral fiscal policy stance")
    print("- 60% crowding out of social spending")
    
    # Run the simulation
    results = engine.run_scenario_file('examples/scenario_04_military_spending.json')
    
    # Extract key results
    simulation_results = results['results']
    summary = simulation_results['summary']
    
    print(f"\n📊 Simulation Results:")
    print(f"- Peak Military Spending: {summary['peak_military_spending']:.1f}% of GDP")
    print(f"- Minimum Social Spending: {summary['min_social_spending']:.1f}% of GDP")
    print(f"- Social Spending Reduction: {summary['social_spending_reduction']:.1f}% of GDP")
    print(f"- Average GDP Growth: {summary['avg_gdp_growth']:.3f}%")
    print(f"- GDP Growth Range: {summary['min_gdp_growth']:.3f}% to {summary['max_gdp_growth']:.3f}%")
    print(f"- Final Debt Ratio: {summary['final_debt_ratio']:.1f}% of GDP")
    print(f"- Total Debt Increase: {summary['debt_increase']:.1f}% of GDP")
    print(f"- Total GDP Change: {summary['total_gdp_change']:.2f}%")
    
    # Policy effectiveness assessment
    print(f"\n🎯 Policy Assessment:")
    print(f"- Fiscal Policy Effectiveness: {summary['fiscal_policy_effectiveness']}")
    print(f"- Debt Sustainability Warning: {'⚠️ YES' if summary['sustainability_warning'] else '✅ NO'}")
    print(f"- Peak Debt Risk Score: {summary['peak_debt_risk']:.2f}")
    
    # Final assessment from simple function
    final_assessment = summary['final_assessment']
    print(f"\n📋 Final Assessment:")
    print(f"- Military Spending Level: {final_assessment['new_military_spending_percent']:.1f}% of GDP")
    print(f"- Economic Stimulus: +{final_assessment['gdp_growth_impact']:.1f} percentage points")
    print(f"- Social Budget Trade-off: {final_assessment['social_budget_impact']:.1f}% of GDP")
    print(f"- Fiscal Multiplier Applied: {final_assessment['fiscal_multiplier']:.1f}")
    
    # Show time series highlights
    periods = simulation_results['periods']
    military_spending = simulation_results['military_spending_percent']
    social_spending = simulation_results['social_spending_percent']
    gdp_growth = simulation_results['gdp_growth']
    debt_ratio = simulation_results['debt_ratio']
    
    print(f"\n📈 Timeline Highlights (First 8 Periods):")
    for i in range(min(8, len(periods))):
        mil_pct = military_spending[i] * 100
        soc_pct = social_spending[i] * 100
        growth = gdp_growth[i] * 100
        debt = debt_ratio[i] * 100
        print(f"  Period {i}: Military {mil_pct:.1f}%, Social {soc_pct:.1f}%, Growth {growth:.2f}%, Debt {debt:.1f}%")
    
    return results

def main():
    """Run the military spending shock simulation demo."""
    print("🚀 Jinn-Core Military Spending Shock Simulation Demo")
    print("Analyzing fiscal policy impacts on defense, social spending, and debt\n")
    
    # Run demonstrations
    simple_result = demo_simple_function()
    demo_policy_comparison()
    full_result = demo_full_simulation()
    
    print("\n" + "=" * 65)
    print("✅ Military Spending Shock Simulation Demo Complete!")
    print("\nKey Insights:")
    print("- Military spending increases provide economic stimulus but with lower multipliers")
    print("- Social spending faces significant crowding out (60% rate under neutral policy)")
    print("- Fiscal policy stance dramatically affects both growth and debt outcomes")
    print("- Austerity reduces debt impact but limits economic benefits")
    print("- Stimulus amplifies growth but increases debt sustainability risks")
    print("- Trade-offs between defense capabilities and social investment are quantifiable")

if __name__ == "__main__":
    main() 