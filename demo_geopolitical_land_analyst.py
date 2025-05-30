#!/usr/bin/env python3
"""
Geopolitical Land Price Analyst Demo

This demo showcases the Geopolitical Land Price Analyst model for simulating
global land price trends over 10-15 years. The model identifies:

🌆 High-Growth Regions: Strong fundamentals, tech hubs, infrastructure development
⚠️ High-Risk Zones: Climate vulnerability, political instability, volatility  
🧊 Declining Regions: Economic decline, resource constraints, demographic shifts

Features demonstrated:
- Regional classification and risk assessment
- Climate change impact modeling
- Technology hub premiums and remote work effects
- Infrastructure investment impacts
- Political stability and regulatory environment analysis
- Investment recommendations and rankings
"""

import json
import logging
from datetime import datetime
from src.models.geopolitical_land_analyst import (
    GeopoliticalLandAnalyst, 
    RegionProfile, 
    GeopoliticalShock, 
    simulate_land_price_trends,
    RegionType,
    ClimatePressure
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def run_basic_scenario():
    """Run a basic scenario with default global regions."""
    print("\n" + "="*80)
    print("🌍 GEOPOLITICAL LAND PRICE ANALYST - GLOBAL BASELINE SCENARIO")
    print("="*80)
    
    # Initialize model with default parameters
    model = GeopoliticalLandAnalyst({})
    
    # Basic simulation configuration
    simulation_config = {
        'years': 15,
        'shocks': {
            'climate_disaster_frequency': 0.1,  # Moderate climate pressure
            'trade_war_intensity': 0.05,        # Minor trade tensions
            'start_period': 5                   # Shocks start in year 5
        }
    }
    
    # Run simulation
    results = model.simulate(simulation_config)
    
    # Display results
    print(f"\n📊 SIMULATION SUMMARY")
    print(f"Total regions analyzed: {results['summary']['total_regions_analyzed']}")
    print(f"Average annual growth: {results['summary']['average_annual_growth']:.2f}%")
    print(f"Growth rate range: {results['summary']['growth_rate_range'][0]:.2f}% to {results['summary']['growth_rate_range'][1]:.2f}%")
    print(f"Market outlook: {results['summary']['market_outlook']}")
    print(f"Investment climate: {results['summary']['investment_climate']}")
    
    print(f"\n🏙️ REGIONAL DISTRIBUTION")
    dist = results['summary']['regional_distribution']
    print(f"🌆 High-Growth Regions: {dist['high_growth_regions']}")
    print(f"⚠️ High-Risk Regions: {dist['high_risk_regions']}")
    print(f"🧊 Declining Regions: {dist['declining_regions']}")
    print(f"📈 Stable Regions: {dist['stable_regions']}")
    
    print(f"\n🔝 TOP REGIONAL PERFORMERS")
    for i, (region, growth) in enumerate(results['regional_rankings']['by_growth_rate'][:5]):
        print(f"{i+1}. {region}: {growth:.2f}% annual growth")
    
    print(f"\n💡 KEY MARKET TRENDS")
    for trend in results['summary']['key_trends']:
        print(f"• {trend}")
    
    print(f"\n🎯 INVESTMENT RECOMMENDATIONS")
    if results['investment_recommendations']['top_growth_opportunities']:
        print("Top Growth Opportunities:")
        for rec in results['investment_recommendations']['top_growth_opportunities'][:3]:
            print(f"  • {rec['region']}: {rec['rationale']}")
    
    if results['investment_recommendations']['defensive_plays']:
        print("\nDefensive Plays:")
        for rec in results['investment_recommendations']['defensive_plays'][:3]:
            print(f"  • {rec['region']}: {rec['rationale']}")
    
    return results


def run_climate_stress_scenario():
    """Run a scenario with heightened climate stress."""
    print("\n" + "="*80)
    print("🌡️ CLIMATE STRESS SCENARIO - ACCELERATED CLIMATE IMPACTS")
    print("="*80)
    
    # Enhanced climate stress parameters
    model = GeopoliticalLandAnalyst({
        'global_temperature_rise_annual': 0.035,       # Faster warming
        'climate_adaptation_cost_growth': 0.15,        # Higher adaptation costs
        'extreme_weather_frequency_growth': 0.08,      # More frequent disasters
        'sea_level_rise_annual': 0.005                 # Faster sea level rise
    })
    
    # Climate-focused regions with varying vulnerability
    regions_config = [
        {
            'name': 'Miami-Dade Coastal',
            'region_type': 'climate_vulnerable',
            'gdp_growth_rate': 0.025,
            'climate_pressure': 'EXTREME',
            'water_security_index': 45.0,
            'tech_hub_score': 70.0
        },
        {
            'name': 'Netherlands Delta Cities',
            'region_type': 'mature_cities',
            'gdp_growth_rate': 0.022,
            'climate_pressure': 'HIGH',
            'climate_adaptation_investment': 0.08,  # High adaptation investment
            'infrastructure_quality': 90.0
        },
        {
            'name': 'Bangladesh Coastal Cities',
            'region_type': 'emerging_markets',
            'gdp_growth_rate': 0.055,
            'climate_pressure': 'EXTREME',
            'population_growth_rate': 0.025,
            'water_security_index': 30.0
        },
        {
            'name': 'Australian Inland Cities',
            'region_type': 'mature_cities',
            'gdp_growth_rate': 0.028,
            'climate_pressure': 'MODERATE',  # Moving inland
            'remote_work_adoption': 70.0,
            'water_security_index': 80.0
        },
        {
            'name': 'Canadian Northern Cities',
            'region_type': 'emerging_markets',
            'gdp_growth_rate': 0.035,
            'climate_pressure': 'LOW',  # Climate beneficiary
            'infrastructure_investment_rate': 0.12,
            'population_growth_rate': 0.015
        }
    ]
    
    simulation_config = {
        'years': 15,
        'regions': regions_config,
        'shocks': {
            'climate_disaster_frequency': 0.4,  # High climate stress
            'energy_crisis_severity': 0.2,     # Energy transition challenges
            'migration_pressure': 0.3,         # Climate migration
            'start_period': 2
        }
    }
    
    results = model.simulate(simulation_config)
    
    print(f"\n🌊 CLIMATE IMPACT ANALYSIS")
    for region_name, region_data in results['regions'].items():
        classification = region_data['classification']
        climate_resilience = region_data['sustainability_metrics']['climate_resilience']
        growth_rate = region_data['price_evolution']['annual_growth_rate']
        
        print(f"{classification} {region_name}")
        print(f"  Climate Resilience: {climate_resilience:.1f}/100")
        print(f"  Growth Rate: {growth_rate:.2f}%")
        print(f"  Risk Factors: {', '.join(region_data['risk_factors'])}")
        print()
    
    return results


def run_tech_disruption_scenario():
    """Run a scenario focused on technology disruption and remote work."""
    print("\n" + "="*80)
    print("💻 TECHNOLOGY DISRUPTION SCENARIO - REMOTE WORK REVOLUTION")
    print("="*80)
    
    # Tech-focused parameters
    model = GeopoliticalLandAnalyst({
        'ai_productivity_boost': 0.025,        # Higher AI impact
        'remote_work_growth_rate': 0.15,       # Faster remote work adoption
        'digital_transformation_rate': 0.20,   # Rapid digitalization
    })
    
    # Technology-focused regions
    regions_config = [
        {
            'name': 'Silicon Valley',
            'region_type': 'innovation_frontrunners',
            'gdp_growth_rate': 0.035,
            'tech_hub_score': 95.0,
            'remote_work_adoption': 80.0,
            'initial_land_price_index': 300.0,  # Already expensive
            'developable_land_ratio': 0.3       # Limited land supply
        },
        {
            'name': 'Austin Tech Corridor',
            'region_type': 'upwardly_mobile',
            'gdp_growth_rate': 0.045,
            'tech_hub_score': 85.0,
            'remote_work_adoption': 60.0,
            'initial_land_price_index': 120.0,
            'population_growth_rate': 0.035
        },
        {
            'name': 'Rural Colorado Mountain Towns',
            'region_type': 'emerging_markets',
            'gdp_growth_rate': 0.025,
            'tech_hub_score': 40.0,
            'remote_work_adoption': 90.0,      # Remote work destination
            'initial_land_price_index': 80.0,
            'climate_pressure': 'LOW',
            'infrastructure_quality': 60.0
        },
        {
            'name': 'Manhattan Financial District',
            'region_type': 'mature_cities',
            'gdp_growth_rate': 0.018,
            'tech_hub_score': 75.0,
            'remote_work_adoption': 70.0,      # High remote work impact
            'initial_land_price_index': 400.0,
            'developable_land_ratio': 0.1      # Very limited space
        },
        {
            'name': 'Bangalore IT Hub',
            'region_type': 'innovation_frontrunners',
            'gdp_growth_rate': 0.068,
            'tech_hub_score': 88.0,
            'remote_work_adoption': 50.0,
            'initial_land_price_index': 90.0,
            'population_growth_rate': 0.042
        }
    ]
    
    simulation_config = {
        'years': 12,
        'regions': regions_config,
        'shocks': {
            'technology_disruption': 0.3,      # Major tech disruption
            'trade_war_intensity': 0.1,       # Some tech trade tensions
            'start_period': 3
        }
    }
    
    results = model.simulate(simulation_config)
    
    print(f"\n💡 TECHNOLOGY IMPACT ANALYSIS")
    for region_name, region_data in results['regions'].items():
        classification = region_data['classification']
        tech_score = region_data['region_profile']['tech_hub_score']
        growth_rate = region_data['price_evolution']['annual_growth_rate']
        final_price = region_data['price_evolution']['final_price']
        
        print(f"{classification} {region_name}")
        print(f"  Tech Hub Score: {tech_score}/100")
        print(f"  Growth Rate: {growth_rate:.2f}%")
        print(f"  Price Change: {region_data['price_evolution']['initial_price']:.0f} → {final_price:.0f}")
        print(f"  Growth Drivers: {', '.join(region_data['growth_drivers'])}")
        print()
    
    return results


def run_geopolitical_crisis_scenario():
    """Run a scenario with major geopolitical disruptions."""
    print("\n" + "="*80)
    print("⚔️ GEOPOLITICAL CRISIS SCENARIO - MAJOR GLOBAL DISRUPTIONS")
    print("="*80)
    
    model = GeopoliticalLandAnalyst({})
    
    # Crisis-affected regions
    regions_config = [
        {
            'name': 'Eastern European Border Cities',
            'region_type': 'emerging_markets',
            'gdp_growth_rate': 0.015,
            'political_stability_index': 45.0,  # Low stability
            'infrastructure_quality': 65.0,
            'population_growth_rate': -0.01     # Population decline
        },
        {
            'name': 'Middle Eastern Oil Cities',
            'region_type': 'mature_cities',
            'gdp_growth_rate': 0.025,
            'political_stability_index': 55.0,
            'water_security_index': 25.0,
            'climate_pressure': 'EXTREME'
        },
        {
            'name': 'Swiss Financial Centers',
            'region_type': 'mature_cities',
            'gdp_growth_rate': 0.022,
            'political_stability_index': 95.0,  # Safe haven
            'infrastructure_quality': 92.0,
            'initial_land_price_index': 250.0
        },
        {
            'name': 'Singapore Trade Hub',
            'region_type': 'innovation_frontrunners',
            'gdp_growth_rate': 0.032,
            'political_stability_index': 88.0,
            'tech_hub_score': 85.0,
            'initial_land_price_index': 280.0
        },
        {
            'name': 'Canadian Resource Cities',
            'region_type': 'mature_cities',
            'gdp_growth_rate': 0.028,
            'political_stability_index': 90.0,
            'water_security_index': 95.0,
            'climate_pressure': 'LOW'
        }
    ]
    
    simulation_config = {
        'years': 10,
        'regions': regions_config,
        'shocks': {
            'trade_war_intensity': 0.6,        # Major trade disruption
            'energy_crisis_severity': 0.5,     # Energy supply crisis
            'financial_crisis_risk': 0.4,      # Financial market stress
            'migration_pressure': 0.4,         # Refugee flows
            'start_period': 1                  # Crisis starts early
        }
    }
    
    results = model.simulate(simulation_config)
    
    print(f"\n⚡ CRISIS IMPACT ANALYSIS")
    safe_havens = []
    high_risk = []
    
    for region_name, region_data in results['regions'].items():
        classification = region_data['classification']
        stability = region_data['region_profile']['political_stability']
        growth_rate = region_data['price_evolution']['annual_growth_rate']
        volatility = region_data['market_characteristics']['average_volatility']
        
        print(f"{classification} {region_name}")
        print(f"  Political Stability: {stability}/100")
        print(f"  Growth Rate: {growth_rate:.2f}%")
        print(f"  Volatility: {volatility:.3f}")
        
        if stability > 80 and volatility < 0.1:
            safe_havens.append(region_name)
        elif stability < 60 or volatility > 0.15:
            high_risk.append(region_name)
        print()
    
    print(f"🏛️ Safe Haven Assets: {', '.join(safe_havens)}")
    print(f"⚠️ High-Risk Regions: {', '.join(high_risk)}")
    
    return results


def demonstrate_simple_function():
    """Demonstrate the simple simulate_land_price_trends function."""
    print("\n" + "="*80)
    print("🔧 SIMPLE FUNCTION DEMONSTRATION")
    print("="*80)
    
    # Create a sample region
    tech_hub = RegionProfile(
        name="Sample Tech Hub",
        region_type=RegionType.INNOVATION_FRONTRUNNERS,
        gdp_growth_rate=0.035,
        population_growth_rate=0.018,
        urbanization_rate=0.025,
        tech_hub_score=88.0,
        infrastructure_quality=82.0,
        climate_pressure=ClimatePressure.MODERATE,
        remote_work_adoption=65.0,
        political_stability_index=75.0
    )
    
    # Define a shock scenario
    shock = GeopoliticalShock(
        trade_war_intensity=0.2,
        climate_disaster_frequency=0.15,
        financial_crisis_risk=0.1,
        start_period=5
    )
    
    # Run simple simulation
    results = simulate_land_price_trends(tech_hub, shock, 15)
    
    print(f"Region: {tech_hub.name}")
    print(f"Classification: {results['region_classification']}")
    print(f"Annual Growth Rate: {results['annual_growth_rate']:.2f}%")
    print(f"Final Price Index: {results['final_price_index']:.1f}")
    print(f"Peak Price Year: {results['peak_price_year']}")
    print(f"Price Volatility: {results['price_volatility']:.3f}")
    print(f"Growth Drivers: {', '.join(results['growth_drivers'])}")
    print(f"Risk Factors: {', '.join(results['risk_factors'])}")
    
    return results


def save_results(results, filename):
    """Save simulation results to JSON file."""
    # Convert numpy arrays to lists for JSON serialization
    def convert_numpy(obj):
        if hasattr(obj, 'tolist'):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {k: convert_numpy(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_numpy(item) for item in obj]
        else:
            return obj
    
    serializable_results = convert_numpy(results)
    
    with open(filename, 'w') as f:
        json.dump(serializable_results, f, indent=2, default=str)
    
    print(f"💾 Results saved to {filename}")


def main():
    """Run all demonstration scenarios."""
    print("🌍 GEOPOLITICAL LAND PRICE ANALYST DEMONSTRATION")
    print("This demo showcases comprehensive land price trend analysis")
    print("considering geopolitical, climate, and economic factors.")
    
    try:
        # Run all scenarios
        baseline_results = run_basic_scenario()
        climate_results = run_climate_stress_scenario()
        tech_results = run_tech_disruption_scenario()
        crisis_results = run_geopolitical_crisis_scenario()
        simple_results = demonstrate_simple_function()
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_results(baseline_results, f"land_analyst_baseline_{timestamp}.json")
        save_results(climate_results, f"land_analyst_climate_{timestamp}.json")
        save_results(tech_results, f"land_analyst_tech_{timestamp}.json")
        save_results(crisis_results, f"land_analyst_crisis_{timestamp}.json")
        
        print("\n" + "="*80)
        print("✅ DEMONSTRATION COMPLETE")
        print("="*80)
        print("The Geopolitical Land Price Analyst successfully demonstrated:")
        print("• Regional classification (🌆 Growth, ⚠️ Risk, 🧊 Declining)")
        print("• Climate change impact modeling")
        print("• Technology disruption and remote work effects")
        print("• Geopolitical crisis scenarios")
        print("• Investment recommendations and rankings")
        print("• Multi-factor risk assessment")
        print("\nThe model provides comprehensive insights for land investment")
        print("decisions in an uncertain geopolitical and climate environment.")
        
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        raise


if __name__ == "__main__":
    main() 