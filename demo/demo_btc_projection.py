#!/usr/bin/env python3
"""
Bitcoin Price Projection Demo

Demonstrates the Bitcoin price projection capabilities of Jinn-Core,
modeling different scenarios for Bitcoin reaching $1,000,000.
"""

import logging
from src.engine import SimulationEngine
from src.models.btc_price_projection import simulate_btc_price_projection

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def demo_simple_function():
    """Demonstrate the simple Bitcoin price projection function."""
    print("₿ BITCOIN PRICE PROJECTION - Simple Function Demo")
    print("=" * 65)
    
    # Example scenario: $70,000 to $1,000,000 with 40% annual growth
    print("\n📊 Scenario: Bitcoin $70K → $1M (40% Annual Growth)")
    print("- Current Price: $70,000")
    print("- Target Price: $1,000,000")
    print("- Annual Growth Rate: 40%")
    print("- Maximum Years: 30")
    
    result = simulate_btc_price_projection(
        current_price_usd=70000.0,
        target_price_usd=1000000.0,
        annual_growth_rate=0.40,  # 40% annual growth
        max_years=30
    )
    
    print(f"\n📈 Projection Results:")
    print(f"- Years to Target: {result['years_to_target']:.1f} years")
    print(f"- Final Price (30 years): ${result['final_price']:,.0f}")
    print(f"- Total Return Multiple: {result['total_return_multiple']:.1f}x")
    print(f"- Annual Return Needed: {result['annual_return_needed']*100:.1f}%")
    print(f"- Feasibility: {result['feasibility_assessment']}")
    print(f"- Target Achieved: {'Yes' if result['target_achieved_in_timeframe'] else 'No'}")
    
    # Show price trajectory highlights
    trajectory = result['price_trajectory']
    print(f"\n📅 Price Trajectory Highlights:")
    milestones = [0, 5, 10, 15, 20, 25, 30]
    for year in milestones:
        if year < len(trajectory):
            point = trajectory[year]
            print(f"  Year {year}: ${point['price']:,.0f} ({point['return_multiple']:.1f}x)")
    
    return result

def demo_growth_rate_scenarios():
    """Compare different growth rate scenarios."""
    print("\n\n📈 GROWTH RATE SCENARIOS - Impact of Different Annual Returns")
    print("=" * 65)
    
    scenarios = [
        ("Conservative Growth", 0.20),  # 20% annual
        ("Moderate Growth", 0.30),      # 30% annual
        ("Baseline Growth", 0.40),      # 40% annual
        ("Aggressive Growth", 0.50),    # 50% annual
        ("Hypergrowth", 0.60),         # 60% annual
        ("Parabolic Growth", 0.75)      # 75% annual
    ]
    
    print("\n📋 Comparing growth rates for $70K → $1M target:")
    
    for name, growth_rate in scenarios:
        result = simulate_btc_price_projection(
            current_price_usd=70000.0,
            target_price_usd=1000000.0,
            annual_growth_rate=growth_rate,
            max_years=30
        )
        
        print(f"\n🔸 {name} ({growth_rate*100:.0f}% annual):")
        print(f"  - Years to $1M: {result['years_to_target']:.1f} years")
        print(f"  - 30-year price: ${result['final_price']:,.0f}")
        print(f"  - Feasibility: {result['feasibility_assessment']}")

def demo_price_targets():
    """Compare different price targets with baseline growth."""
    print("\n\n🎯 PRICE TARGET SCENARIOS - Different Bitcoin Targets")
    print("=" * 65)
    
    targets = [
        ("Conservative Target", 200000),    # $200K
        ("Moderate Target", 500000),        # $500K
        ("Ambitious Target", 1000000),      # $1M
        ("Moonshot Target", 2000000),       # $2M
        ("Hyperbitcoinization", 5000000)    # $5M
    ]
    
    print("\n📋 Comparing price targets with 40% annual growth:")
    
    for name, target_price in targets:
        result = simulate_btc_price_projection(
            current_price_usd=70000.0,
            target_price_usd=target_price,
            annual_growth_rate=0.40,
            max_years=30
        )
        
        multiple = target_price / 70000
        print(f"\n🔸 {name} (${target_price:,} - {multiple:.1f}x):")
        print(f"  - Years to target: {result['years_to_target']:.1f} years")
        print(f"  - Target achieved: {'Yes' if result['target_achieved_in_timeframe'] else 'No'}")
        print(f"  - Feasibility: {result['feasibility_assessment']}")

def demo_full_simulation():
    """Demonstrate the full Bitcoin price projection simulation."""
    print("\n\n🎯 BITCOIN PRICE PROJECTION - Full Model Demo")
    print("=" * 65)
    
    engine = SimulationEngine()
    print(f"🔧 Available Models: {', '.join(engine.models.keys())}")
    
    print("\n📋 Running All Scenarios: $70K → $1M Bitcoin Projection")
    print("- Baseline: 40% annual growth (steady adoption)")
    print("- Institutional Adoption: 55% annual growth (ETFs, corporate treasuries)")
    print("- Fiat Crisis: 65% annual growth (currency debasement)")
    print("- Regulatory Clarity: 50% annual growth (clear legal framework)")
    print("- Combined Shock: 75% annual growth (perfect storm scenario)")
    
    # Run the simulation
    results = engine.run_scenario_file('examples/scenario_07_btc_projection.json')
    
    # Extract key results
    simulation_results = results['results']
    scenarios = simulation_results['scenarios']
    comparison = simulation_results['comparison']
    summary = simulation_results['summary']
    
    print(f"\n📊 Scenario Results:")
    for scenario_name, scenario_data in scenarios.items():
        enhanced = scenario_data['enhanced_projection']
        risk = scenario_data['risk_assessment']
        
        print(f"\n🔸 {scenario_name.replace('_', ' ').title()}:")
        print(f"  - Growth Rate: {scenario_data['annual_growth_rate']*100:.0f}% annual")
        print(f"  - Years to $1M: {enhanced['years_to_target']:.1f} years")
        print(f"  - 30-year price: ${enhanced['final_price']:,.0f}")
        print(f"  - Return Multiple: {enhanced['total_return_multiple']:.1f}x")
        print(f"  - Target Achieved: {'Yes' if enhanced['target_achieved'] else 'No'}")
        print(f"  - Risk Level: {risk['overall_risk']}")
    
    # Show comparison insights
    print(f"\n🏆 Scenario Comparison:")
    if comparison['fastest_to_target']:
        fastest = comparison['fastest_to_target']
        print(f"- Fastest to $1M: {fastest['scenario'].replace('_', ' ').title()} ({fastest['years']:.1f} years)")
    
    if comparison['highest_final_price']:
        highest = comparison['highest_final_price']
        print(f"- Highest 30-year price: {highest['scenario'].replace('_', ' ').title()} (${highest['price']:,.0f})")
    
    if comparison['lowest_risk']:
        lowest_risk = comparison['lowest_risk']
        print(f"- Lowest risk: {lowest_risk['scenario'].replace('_', ' ').title()} ({lowest_risk['risk_level']} risk)")
    
    if comparison['most_realistic']:
        realistic = comparison['most_realistic']
        print(f"- Most realistic: {realistic['scenario'].replace('_', ' ').title()} ({realistic['years_to_target']:.1f} years, {realistic['risk_level']} risk)")
    
    # Show investment insights
    print(f"\n💡 Investment Insights:")
    target_analysis = summary['target_analysis']
    time_analysis = summary['time_to_target']
    investment_insights = summary['investment_insights']
    
    print(f"- Target Multiple: {target_analysis['target_multiple']:.1f}x (${target_analysis['current_price']:,} → ${target_analysis['target_price']:,})")
    print(f"- Success Probability: {target_analysis['success_probability']*100:.0f}% ({target_analysis['scenarios_achieving_target']}/{target_analysis['scenarios_analyzed']} scenarios)")
    print(f"- Average Time to Target: {time_analysis['average_years']:.1f} years")
    print(f"- Time Range: {time_analysis['fastest_scenario_years']:.1f} - {time_analysis['slowest_scenario_years']:.1f} years")
    print(f"- Most Likely Outcome: {investment_insights['most_likely_outcome']}")
    print(f"- Best Case Scenario: {investment_insights['best_case_scenario']}")
    print(f"- Target Achievability: {investment_insights['target_achievability']}")
    print(f"- Investment Recommendation: {investment_insights['recommended_strategy']}")
    
    # Show scenario rankings
    print(f"\n🥇 Scenario Rankings (by overall score):")
    rankings = comparison['scenario_rankings']
    for i, ranking in enumerate(rankings[:5], 1):
        print(f"  {i}. {ranking['scenario'].replace('_', ' ').title()}")
        print(f"     - Score: {ranking['total_score']:.1f}/20")
        print(f"     - Time: {ranking['years_to_target']:.1f} years")
        print(f"     - Price: ${ranking['final_price']:,.0f}")
        print(f"     - Risk: {ranking['risk_level']}")
    
    return results

def demo_custom_scenarios():
    """Demonstrate custom Bitcoin price scenarios."""
    print("\n\n🔧 CUSTOM SCENARIOS - User-Defined Projections")
    print("=" * 65)
    
    custom_scenarios = [
        {
            "name": "Current Bull Market",
            "current": 110000,  # Current higher price
            "target": 1000000,
            "growth": 0.35,
            "years": 25
        },
        {
            "name": "Bear Market Entry",
            "current": 45000,   # Lower entry point
            "target": 1000000,
            "growth": 0.45,
            "years": 30
        },
        {
            "name": "Conservative Retiree",
            "current": 70000,
            "target": 300000,   # More modest target
            "growth": 0.25,
            "years": 20
        },
        {
            "name": "Aggressive Trader",
            "current": 70000,
            "target": 2000000,  # Higher target
            "growth": 0.55,
            "years": 15
        }
    ]
    
    print("\n📋 Custom scenario analysis:")
    
    for scenario in custom_scenarios:
        result = simulate_btc_price_projection(
            current_price_usd=scenario["current"],
            target_price_usd=scenario["target"],
            annual_growth_rate=scenario["growth"],
            max_years=scenario["years"]
        )
        
        print(f"\n🔸 {scenario['name']}:")
        print(f"  - Entry: ${scenario['current']:,} → Target: ${scenario['target']:,}")
        print(f"  - Growth Rate: {scenario['growth']*100:.0f}% annual")
        print(f"  - Years to target: {result['years_to_target']:.1f} years")
        print(f"  - Final price ({scenario['years']}y): ${result['final_price']:,.0f}")
        print(f"  - Feasibility: {result['feasibility_assessment']}")
        print(f"  - Annual return needed: {result['annual_return_needed']*100:.1f}%")

def demo_risk_analysis():
    """Analyze risk factors across different scenarios."""
    print("\n\n⚠️ RISK ANALYSIS - Bitcoin Investment Risk Assessment")
    print("=" * 65)
    
    # Run a quick simulation to get risk data
    engine = SimulationEngine()
    model = engine.models['btc_price_projection']({})
    
    simulation_config = {
        'current_price_usd': 70000.0,
        'target_price_usd': 1000000.0,
        'max_years': 30,
        'scenarios': ['baseline', 'institutional_adoption', 'fiat_crisis', 'regulatory_clarity', 'combined_shock']
    }
    
    results = model.simulate(simulation_config)
    scenarios = results['scenarios']
    
    print("\n📊 Risk Assessment by Scenario:")
    
    for scenario_name, scenario_data in scenarios.items():
        risk = scenario_data['risk_assessment']
        
        print(f"\n🔸 {scenario_name.replace('_', ' ').title()}:")
        print(f"  - Overall Risk: {risk['overall_risk']} (Score: {risk['risk_score']:.1f}/4)")
        print(f"  - Time Risk: {risk['time_risk']}")
        print(f"  - Volatility Risk: {risk['volatility_risk']}")
        print(f"  - Regulatory Risk: {risk['regulatory_risk']}")
        
        if risk['key_risks']:
            print(f"  - Key Risks: {', '.join(risk['key_risks'])}")
        else:
            print(f"  - Key Risks: None identified")
    
    # Risk mitigation strategies
    print(f"\n🛡️ Risk Mitigation Strategies:")
    print("- Dollar-Cost Averaging: Reduces timing risk and volatility impact")
    print("- Diversification: Don't put all investments in Bitcoin")
    print("- Regulatory Monitoring: Stay informed about regulatory developments")
    print("- Long-term Perspective: Bitcoin's volatility decreases over longer timeframes")
    print("- Position Sizing: Only invest what you can afford to lose")
    print("- Technical Analysis: Use charts and indicators for entry/exit timing")

def main():
    """Run the Bitcoin price projection demo."""
    print("🚀 Jinn-Core Bitcoin Price Projection Demo")
    print("Analyzing Bitcoin's path to $1,000,000 across multiple scenarios\n")
    
    # Run demonstrations
    simple_result = demo_simple_function()
    demo_growth_rate_scenarios()
    demo_price_targets()
    full_result = demo_full_simulation()
    demo_custom_scenarios()
    demo_risk_analysis()
    
    print("\n" + "=" * 65)
    print("✅ Bitcoin Price Projection Demo Complete!")
    print("\nKey Insights:")
    print("- Bitcoin reaching $1M is achievable with sustained 40%+ annual growth")
    print("- Institutional adoption scenarios show the highest probability of success")
    print("- Combined shock scenario (75% growth) reaches $1M in ~4 years")
    print("- Regulatory clarity significantly reduces investment risk")
    print("- Fiat crisis scenarios show high returns but increased volatility")
    print("- Success probability varies from 60-100% depending on scenario")
    print("- Time to target ranges from 4-12 years across realistic scenarios")
    print("- Risk management and long-term perspective are crucial for success")
    print("- Dollar-cost averaging recommended for most investors")

if __name__ == "__main__":
    main() 