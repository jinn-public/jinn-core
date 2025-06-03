#!/usr/bin/env python3
"""
AI Unemployment Shock Simulation Demo

Demonstrates the AI-driven unemployment shock simulation capabilities of Jinn-Core,
including UBI implementation and scenario comparison.
"""

import logging
from src.engine import SimulationEngine
from src.models.ai_unemployment_shock import simulate_ai_unemployment_shock

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def demo_simple_function():
    """Demonstrate the simple AI unemployment shock function."""
    print("🤖 AI UNEMPLOYMENT SHOCK SIMULATION - Simple Function Demo")
    print("=" * 70)
    
    # Scenario: Year 12 of AI displacement
    print("\n📊 Scenario: Year 12 of AI Displacement")
    print("- Current Employment Rate: 82% (down from 94%)")
    print("- AI Displacement Rate: 1% per year")
    print("- Current GDP: $30 trillion")
    print("- UBI Threshold: 12% unemployment")
    
    result = simulate_ai_unemployment_shock(
        current_employment_rate=82.0,
        ai_displacement_rate=1.0,
        current_gdp=30_000_000_000_000,
        current_year=12,
        max_displacement=30.0,
        ubi_threshold=12.0
    )
    
    print(f"\n📈 Results:")
    print(f"- New Unemployment Rate: {result['new_unemployment_rate']:.1f}%")
    print(f"- New Employment Rate: {result['new_employment_rate']:.1f}%")
    print(f"- AI Productivity Boost: {result['productivity_boost']:.1f}%")
    print(f"- UBI Activated: {'✅ YES' if result['ubi_activated'] else '❌ NO'}")
    if result['ubi_activated']:
        print(f"- UBI Coverage Rate: {result['ubi_coverage_rate']:.1%}")
        print(f"- Annual UBI Cost: ${result['ubi_cost']/1e12:.2f} trillion")
    
    return result

def demo_full_simulation():
    """Demonstrate the full AI unemployment shock simulation."""
    print("\n\n🏛️ AI UNEMPLOYMENT SHOCK SIMULATION - Full Model Demo")
    print("=" * 70)
    
    engine = SimulationEngine()
    print(f"🔧 Available Models: {', '.join(engine.models.keys())}")
    
    print("\n📋 Running Scenario: 30-Year AI Displacement Crisis")
    print("- AI displacement: 1% unemployment increase per year")
    print("- Maximum unemployment: 30% (reached in year 30)")
    print("- UBI threshold: 12% unemployment")
    print("- UBI benefit: $15,000 per person per year")
    print("- Comparison: With UBI vs Without UBI scenarios")
    
    # Run the simulation
    results = engine.run_scenario_file('examples/scenario_08_ai_unemployment.json')
    
    # Extract results for both scenarios
    with_ubi = results['results']['scenario_with_ubi']
    without_ubi = results['results']['scenario_without_ubi']
    comparison = results['results']['comparison']
    
    print(f"\n📊 Simulation Results - WITH UBI:")
    summary_with = with_ubi['summary']
    print(f"- Final Unemployment Rate: {summary_with['final_unemployment_rate']:.1f}%")
    print(f"- Final GDP: ${summary_with['final_gdp']/1e12:.1f} trillion")
    print(f"- Total GDP Growth: {summary_with['total_gdp_growth']:.1f}%")
    print(f"- UBI Triggered in Year: {summary_with['ubi_trigger_year']}")
    print(f"- Total UBI Cost: ${summary_with['total_ubi_cost']/1e12:.1f} trillion")
    print(f"- Final Tax Rate: {summary_with['final_tax_rate']:.1%}")
    print(f"- Years in Budget Deficit: {summary_with['years_in_deficit']}/30")
    
    print(f"\n📊 Simulation Results - WITHOUT UBI:")
    summary_without = without_ubi['summary']
    print(f"- Final Unemployment Rate: {summary_without['final_unemployment_rate']:.1f}%")
    print(f"- Final GDP: ${summary_without['final_gdp']/1e12:.1f} trillion")
    print(f"- Total GDP Growth: {summary_without['total_gdp_growth']:.1f}%")
    print(f"- Final Tax Rate: {summary_without['final_tax_rate']:.1%}")
    print(f"- Years in Budget Deficit: {summary_without['years_in_deficit']}/30")
    
    print(f"\n🔍 Scenario Comparison:")
    print(f"- GDP Difference (Final): ${comparison['gdp_difference']['final']/1e12:.2f} trillion")
    print(f"- GDP Growth Difference: {comparison['gdp_difference']['total_growth_difference']:.1f}pp")
    print(f"- Unemployment Difference (Final): {comparison['unemployment_difference']['final']:.1f}pp")
    print(f"- Tax Rate Difference: {comparison['fiscal_impact']['tax_rate_difference']:.1%}")
    
    print(f"\n🎯 Key Insights:")
    for insight in comparison['key_insights']:
        print(f"- {insight}")
    
    # Show key timeline points
    periods = with_ubi['periods']
    unemployment_with = with_ubi['unemployment_rate']
    ubi_activated = with_ubi['ubi_activated']
    productivity = with_ubi['productivity_growth']
    
    print(f"\n📈 Timeline Highlights (WITH UBI):")
    key_years = [0, 5, 10, 12, 15, 20, 25, 29]  # Key milestone years
    for year in key_years:
        if year < len(periods):
            status = ""
            if ubi_activated[year]:
                status += "🔴 UBI Active "
            if productivity[year] > 4.0:
                status += f"⚡ High Productivity ({productivity[year]:.1f}%) "
            print(f"  Year {year}: Unemployment {unemployment_with[year]:.1f}% {status}")
    
    return results

def analyze_trade_offs(results):
    """Analyze the productivity vs employment trade-offs."""
    print("\n\n📊 PRODUCTIVITY vs EMPLOYMENT TRADE-OFF ANALYSIS")
    print("=" * 70)
    
    with_ubi = results['results']['scenario_with_ubi']
    
    # Calculate key trade-off metrics
    initial_employment = with_ubi['employment_rate'][0]
    final_employment = with_ubi['employment_rate'][-1]
    initial_productivity = with_ubi['productivity_growth'][0]
    final_productivity = with_ubi['productivity_growth'][-1]
    
    employment_loss = initial_employment - final_employment
    productivity_gain = final_productivity - initial_productivity
    
    print(f"📉 Employment Change: {initial_employment:.1f}% → {final_employment:.1f}% (-{employment_loss:.1f}pp)")
    print(f"📈 Productivity Change: {initial_productivity:.1f}% → {final_productivity:.1f}% (+{productivity_gain:.1f}pp)")
    print(f"🔄 Trade-off Ratio: {productivity_gain/employment_loss:.2f} productivity points per employment point lost")
    
    # GDP analysis
    initial_gdp = with_ubi['gdp'][0] / 1e12
    final_gdp = with_ubi['gdp'][-1] / 1e12
    gdp_growth = ((final_gdp - initial_gdp) / initial_gdp) * 100
    
    print(f"\n💰 Net Economic Impact:")
    print(f"- Initial GDP: ${initial_gdp:.1f} trillion")
    print(f"- Final GDP: ${final_gdp:.1f} trillion") 
    print(f"- Total Growth: {gdp_growth:.1f}% over 30 years")
    print(f"- Average Annual Growth: {gdp_growth/30:.1f}%")
    
    # Determine if the trade-off is favorable
    if gdp_growth > 60:  # 60% growth over 30 years = 2% annual
        assessment = "✅ FAVORABLE - Strong net economic growth despite employment losses"
    elif gdp_growth > 30:
        assessment = "⚠️ MIXED - Moderate growth, but with significant social challenges"
    else:
        assessment = "❌ CHALLENGING - Limited growth may not offset employment disruption"
    
    print(f"\n🎯 Overall Assessment: {assessment}")

def main():
    """Run the AI unemployment shock simulation demo."""
    print("🚀 Jinn-Core AI Unemployment Shock Simulation Demo")
    print("Simulating the economic impact of AI-driven unemployment with UBI policy responses\n")
    
    # Run demonstrations
    simple_result = demo_simple_function()
    full_result = demo_full_simulation()
    analyze_trade_offs(full_result)
    
    print("\n" + "=" * 70)
    print("✅ AI Unemployment Shock Simulation Demo Complete!")
    print("\nKey Research Questions Answered:")
    print("- How does AI productivity growth offset employment losses?")
    print("- When should UBI be triggered and at what cost?")
    print("- Can government budgets sustain UBI programs?")
    print("- What are the long-term economic trade-offs?")
    print("- How do different policy responses compare?")
    
    print("\n🔬 Model Capabilities Demonstrated:")
    print("- 30-year longitudinal economic simulation")
    print("- Dynamic UBI implementation with threshold triggers")
    print("- Fiscal sustainability analysis with tax adjustments")
    print("- Scenario comparison (with/without UBI)")
    print("- Productivity vs employment trade-off quantification")

if __name__ == "__main__":
    main() 