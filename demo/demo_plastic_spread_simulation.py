#!/usr/bin/env python3
"""
Plastic Spread Simulation Demo

Demonstrates the plastic waste accumulation simulation capabilities of Jinn-Core,
including environmental coverage progression and policy intervention scenarios.
"""

import logging
from src.engine import SimulationEngine
from src.models.plastic_spread_simulation import simulate_plastic_spread

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def demo_simple_function():
    """Demonstrate the simple plastic spread function."""
    print("🌍 PLASTIC SPREAD SIMULATION - Simple Function Demo")
    print("=" * 70)
    
    # Scenario: Year 25 of plastic accumulation
    print("\n📊 Scenario: Year 25 of Global Plastic Accumulation")
    print("- Annual Production: 400 million tonnes (2023 baseline)")
    print("- Growth Rate: 3% per year")
    print("- Coverage Density: 1,000 kg per sq km for visible coverage")
    print("- Earth Surface Area: 510 million sq km")
    
    result = simulate_plastic_spread(
        annual_production_tonnes=400_000_000,
        annual_growth_rate=0.03,
        coverage_density_kg_per_sq_km=1_000,
        earth_surface_area_sq_km=510_000_000,
        ocean_area_sq_km=361_000_000,
        current_year=25
    )
    
    print(f"\n📈 Results:")
    print(f"- Current Production: {result['current_production_tonnes']/1e6:.1f} million tonnes")
    print(f"- Total Plastic Accumulated: {result['total_plastic_accumulated_kg']/1e12:.2f} trillion kg")
    print(f"- Earth Coverage: {result['earth_coverage_percent']:.3f}%")
    print(f"- Ocean Coverage: {result['ocean_coverage_percent']:.3f}%")
    print(f"- Cleanup Cost: ${result['cleanup_cost_billion_usd']:.1f} billion")
    print(f"- Environmental Damage Cost: ${result['environmental_damage_cost_billion_usd']:.1f} billion")
    
    # Calculate years to critical thresholds
    coverage_rate = result['earth_coverage_percent'] / 25  # % per year
    years_to_1_percent = 1.0 / coverage_rate if coverage_rate > 0 else float('inf')
    
    print(f"\n⚠️ Projections:")
    print(f"- Years to reach 1% Earth coverage: {years_to_1_percent:.0f} years")
    print(f"- Coverage rate: {coverage_rate:.4f}% per year")
    
    return result

def demo_full_simulation():
    """Demonstrate the full plastic spread simulation."""
    print("\n\n🌊 PLASTIC SPREAD SIMULATION - Full Model Demo")
    print("=" * 70)
    
    engine = SimulationEngine()
    print(f"🔧 Available Models: {', '.join(engine.models.keys())}")
    
    print("\n📋 Running Scenario: 50-Year Plastic Accumulation Crisis")
    print("- Baseline production: 400 million tonnes/year")
    print("- 3% annual growth in production")
    print("- Multiple intervention scenarios")
    print("- Coverage progression tracking")
    print("- Economic cost analysis")
    
    # Run the simulation
    results = engine.run_scenario_file('examples/scenario_09_plastic_spread.json')
    
    # Extract results for all scenarios
    baseline = results['results']['baseline_scenario']
    production_cap = results['results']['production_cap_scenario']
    recycling = results['results']['recycling_improvement_scenario']
    combined = results['results']['combined_intervention_scenario']
    comparison = results['results']['comparison']
    
    print(f"\n📊 Simulation Results Summary (50 years):")
    print(f"{'Scenario':<25} {'Earth Coverage':<15} {'Ocean Coverage':<15} {'Total Cost (B$)':<15} {'Plastic Acc. (Gt)':<15}")
    print("-" * 85)
    
    scenarios = [
        ('Baseline', baseline['summary']),
        ('Production Cap', production_cap['summary']),
        ('Recycling Improve', recycling['summary']),
        ('Combined', combined['summary'])
    ]
    
    for name, summary in scenarios:
        print(f"{name:<25} {summary['final_earth_coverage_percent']:<14.3f}% {summary['final_ocean_coverage_percent']:<14.3f}% "
              f"{summary['total_economic_cost_billion_usd']:<14.1f} {summary['total_plastic_accumulated_tonnes']/1e9:<14.2f}")
    
    print(f"\n🎯 Critical Threshold Analysis:")
    for name, summary in scenarios:
        critical_year = summary['critical_coverage_year']
        ocean_year = summary['ocean_saturation_year']
        print(f"{name}:")
        print(f"  - 1% Earth coverage: {'Year ' + str(critical_year) if critical_year else 'Never reached'}")
        print(f"  - 10% Ocean coverage: {'Year ' + str(ocean_year) if ocean_year else 'Never reached'}")
    
    print(f"\n💰 Economic Impact Comparison:")
    print(f"- Production Cap Savings: ${comparison['cost_savings']['production_cap']['total_savings_billion']:.1f}B")
    print(f"- Recycling Improvement Savings: ${comparison['cost_savings']['recycling_improvement']['total_savings_billion']:.1f}B") 
    print(f"- Combined Intervention Savings: ${comparison['cost_savings']['combined_intervention']['total_savings_billion']:.1f}B")
    
    print(f"\n🌍 Environmental Benefits:")
    print(f"- Production Cap Plastic Reduction: {comparison['environmental_benefits']['production_cap']['plastic_reduction_tonnes']/1e9:.2f} Gt")
    print(f"- Recycling Plastic Reduction: {comparison['environmental_benefits']['recycling_improvement']['plastic_reduction_tonnes']/1e9:.2f} Gt")
    print(f"- Combined Plastic Reduction: {comparison['environmental_benefits']['combined_intervention']['plastic_reduction_tonnes']/1e9:.2f} Gt")
    
    print(f"\n🔍 Key Insights:")
    for insight in comparison['key_insights']:
        print(f"- {insight}")
    
    # Show timeline progression for baseline scenario
    print(f"\n📈 Baseline Timeline Highlights:")
    periods = baseline['periods']
    earth_coverage = baseline['earth_coverage_percent']
    ocean_coverage = baseline['ocean_coverage_percent']
    costs = baseline['environmental_damage_cost_billion_usd']
    
    key_years = [0, 10, 20, 30, 40, 49]  # Key milestone years
    for year in key_years:
        if year < len(periods):
            status = ""
            if earth_coverage[year] >= 0.1:
                status += "⚠️ Critical Coverage "
            if ocean_coverage[year] >= 1.0:
                status += "🌊 Ocean Saturation "
            if costs[year] >= 1000:
                status += "💰 High Economic Cost "
            
            print(f"  Year {year}: Earth {earth_coverage[year]:.3f}%, Ocean {ocean_coverage[year]:.3f}%, Cost ${costs[year]:.0f}B {status}")
    
    return results

def analyze_intervention_effectiveness(results):
    """Analyze the effectiveness of different intervention strategies."""
    print("\n\n📊 INTERVENTION EFFECTIVENESS ANALYSIS")
    print("=" * 70)
    
    baseline = results['results']['baseline_scenario']['summary']
    comparison = results['results']['comparison']
    
    print("🎯 Intervention Rankings by Total Economic Savings:")
    
    savings_ranking = [
        ('Combined Intervention', comparison['cost_savings']['combined_intervention']['total_savings_billion']),
        ('Recycling Improvement', comparison['cost_savings']['recycling_improvement']['total_savings_billion']),
        ('Production Cap', comparison['cost_savings']['production_cap']['total_savings_billion'])
    ]
    
    savings_ranking.sort(key=lambda x: x[1], reverse=True)
    
    for i, (intervention, savings) in enumerate(savings_ranking, 1):
        roi_percent = (savings / baseline['total_economic_cost_billion_usd']) * 100
        print(f"{i}. {intervention}: ${savings:.1f}B saved ({roi_percent:.1f}% of baseline cost)")
    
    print(f"\n🌍 Environmental Impact Rankings by Plastic Reduction:")
    
    plastic_ranking = [
        ('Combined Intervention', comparison['environmental_benefits']['combined_intervention']['plastic_reduction_tonnes']/1e9),
        ('Recycling Improvement', comparison['environmental_benefits']['recycling_improvement']['plastic_reduction_tonnes']/1e9),
        ('Production Cap', comparison['environmental_benefits']['production_cap']['plastic_reduction_tonnes']/1e9)
    ]
    
    plastic_ranking.sort(key=lambda x: x[1], reverse=True)
    
    for i, (intervention, reduction) in enumerate(plastic_ranking, 1):
        reduction_percent = (reduction / (baseline['total_plastic_accumulated_tonnes']/1e9)) * 100
        print(f"{i}. {intervention}: {reduction:.2f}Gt reduced ({reduction_percent:.1f}% of baseline)")
    
    # Timeline analysis
    print(f"\n⏰ Timeline Impact Analysis:")
    combined = results['results']['combined_intervention_scenario']['summary']
    
    coverage_delay = (combined['critical_coverage_year'] or 999) - (baseline['critical_coverage_year'] or 999)
    ocean_delay = (combined['ocean_saturation_year'] or 999) - (baseline['ocean_saturation_year'] or 999)
    
    print(f"- Combined interventions delay 1% Earth coverage by: {coverage_delay} years")
    print(f"- Combined interventions delay 10% ocean coverage by: {ocean_delay} years")
    
    # Cost-effectiveness analysis
    print(f"\n💡 Cost-Effectiveness Insights:")
    
    # Calculate cost per tonne of plastic prevented
    for intervention, savings in savings_ranking:
        if intervention in comparison['environmental_benefits']:
            plastic_prevented = comparison['environmental_benefits'][intervention.lower().replace(' ', '_')]['plastic_reduction_tonnes']
            if plastic_prevented > 0:
                cost_per_tonne = savings * 1e9 / plastic_prevented  # Convert billions to actual cost per tonne
                print(f"- {intervention}: ${cost_per_tonne:.0f} economic return per tonne of plastic prevented")
    
    # Overall assessment
    best_intervention = savings_ranking[0][0]
    best_savings = savings_ranking[0][1]
    
    if best_savings > baseline['total_economic_cost_billion_usd'] * 0.5:
        assessment = "✅ HIGHLY EFFECTIVE - Major economic and environmental benefits"
    elif best_savings > baseline['total_economic_cost_billion_usd'] * 0.2:
        assessment = "⚠️ MODERATELY EFFECTIVE - Significant but limited benefits"
    else:
        assessment = "❌ LIMITED EFFECTIVENESS - Interventions provide minimal benefits"
    
    print(f"\n🎯 Overall Assessment: {assessment}")

def main():
    """Run the plastic spread simulation demo."""
    print("🚀 Jinn-Core Plastic Spread Simulation Demo")
    print("Simulating global plastic waste accumulation and policy intervention effectiveness\n")
    
    # Run demonstrations
    simple_result = demo_simple_function()
    full_result = demo_full_simulation()
    analyze_intervention_effectiveness(full_result)
    
    print("\n" + "=" * 70)
    print("✅ Plastic Spread Simulation Demo Complete!")
    print("\nKey Research Questions Answered:")
    print("- How quickly will plastic waste visibly cover Earth's surface?")
    print("- What are the economic costs of plastic accumulation?")
    print("- How effective are production caps vs recycling improvements?")
    print("- When do we reach critical environmental tipping points?")
    print("- What are the long-term consequences of current trends?")
    
    print("\n🔬 Model Capabilities Demonstrated:")
    print("- 50-year environmental progression simulation")
    print("- Multi-scenario policy intervention comparison")
    print("- Economic cost modeling (cleanup + environmental damage)")
    print("- Critical threshold identification (coverage tipping points)")
    print("- Cost-effectiveness analysis of interventions")
    print("- Timeline impact assessment")
    
    print("\n🌍 Environmental Insights:")
    baseline_summary = full_result['results']['baseline_scenario']['summary']
    combined_summary = full_result['results']['combined_intervention_scenario']['summary']
    
    print(f"- Baseline: {baseline_summary['final_earth_coverage_percent']:.3f}% Earth coverage in 50 years")
    print(f"- With interventions: {combined_summary['final_earth_coverage_percent']:.3f}% Earth coverage")
    print(f"- Economic savings from interventions: ${full_result['results']['comparison']['cost_savings']['combined_intervention']['total_savings_billion']:.1f}B")
    print(f"- Plastic reduction: {full_result['results']['comparison']['environmental_benefits']['combined_intervention']['plastic_reduction_tonnes']/1e12:.2f} trillion tonnes")

if __name__ == "__main__":
    main() 