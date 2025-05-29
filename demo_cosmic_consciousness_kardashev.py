#!/usr/bin/env python3
"""
Cosmic Consciousness Timing with Kardashev Scale Demo

Demonstrates the enhanced cosmic consciousness timing simulation with Kardashev Scale
technological advancement levels and their impact on civilization survival.
"""

import json
import logging
from src.models.cosmic_consciousness_timing import (
    simulate_cosmic_consciousness_timing, 
    CosmicConsciousnessTimingModel,
    KARDASHEV_SCALE,
    estimate_kardashev_progress,
    get_kardashev_level_name
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def demo_kardashev_scale_basics():
    """Demonstrate basic Kardashev Scale concepts and progression."""
    print("🌌 KARDASHEV SCALE INTEGRATION - Basic Concepts")
    print("=" * 80)
    
    print("\n📊 Kardashev Scale Levels:")
    print("-" * 50)
    for level, data in KARDASHEV_SCALE.items():
        print(f"Level {level:>4}: {data['name']:<20} - {data['description']}")
        print(f"         Energy: {data['energy']:.2e} Watts")
        print()
    
    print("\n⚡ Kardashev Progression Examples:")
    print("-" * 40)
    
    # Example 1: Human civilization progression
    print("🌍 Human Civilization (Starting at 0.73 - Modern Humans):")
    time_periods = [0.1, 0.5, 1.0, 2.0]  # billion years
    growth_rate = 0.15  # per billion years
    
    for period in time_periods:
        final_level = estimate_kardashev_progress(0.73, growth_rate, period)
        print(f"  After {period:.1f}B years: Level {final_level:.2f} ({get_kardashev_level_name(final_level)})")
    
    # Example 2: Primitive civilization progression
    print("\n🔥 Primitive Civilization (Starting at 0.0):")
    for period in time_periods:
        final_level = estimate_kardashev_progress(0.0, growth_rate, period)
        print(f"  After {period:.1f}B years: Level {final_level:.2f} ({get_kardashev_level_name(final_level)})")
    
    print("\n🎯 Key Insight: Higher Kardashev levels dramatically improve")
    print("   expansion capabilities and survival probabilities!")

def demo_kardashev_impact_comparison():
    """Compare civilization outcomes across different Kardashev starting levels."""
    print("\n\n🚀 KARDASHEV IMPACT COMPARISON")
    print("=" * 80)
    
    # Standard scenario parameters
    evolution_duration = 4.0
    time_left = 0.4  # Challenging scenario
    window_needed = 0.25
    risk_tolerance = 0.2
    kardashev_growth_rate = 0.15
    
    kardashev_levels = [0.0, 0.5, 0.73, 1.0, 1.5, 2.0]
    
    print(f"📋 Scenario Parameters:")
    print(f"- Evolution Duration: {evolution_duration:.1f} billion years")
    print(f"- Time Left: {time_left:.1f} billion years")
    print(f"- Window Needed: {window_needed:.2f} billion years")
    print(f"- Risk Tolerance: {risk_tolerance:.0%}")
    print(f"- Kardashev Growth Rate: {kardashev_growth_rate:.2f} per billion years")
    
    print(f"\n📊 Results by Starting Kardashev Level:")
    print("-" * 80)
    print(f"{'Level':<6} {'Name':<20} {'Final K':<8} {'Success':<8} {'Expansion Prob':<14} {'Window Reduction'}")
    print("-" * 80)
    
    results = []
    
    for k_level in kardashev_levels:
        result = simulate_cosmic_consciousness_timing(
            evolution_duration=evolution_duration,
            time_left=time_left,
            window_needed=window_needed,
            risk_tolerance=risk_tolerance,
            starting_kardashev_level=k_level,
            kardashev_growth_rate=kardashev_growth_rate,
            kardashev_enabled=True
        )
        
        success_symbol = "✅" if result['civilization_succeeds'] else "❌"
        window_reduction = (1 - result['expansion_multiplier']) * 100
        
        print(f"{k_level:<6.2f} {result['starting_kardashev_name']:<20} "
              f"{result['final_kardashev_level']:<8.2f} {success_symbol:<8} "
              f"{result['expansion_probability']:<14.1%} {window_reduction:>12.0f}%")
        
        results.append(result)
    
    # Summary insights
    success_count = sum(1 for r in results if r['civilization_succeeds'])
    print(f"\n🎯 Summary:")
    print(f"- Successful Civilizations: {success_count}/{len(results)}")
    print(f"- Kardashev levels ≥1.0 have significant advantages")
    print(f"- Type II civilizations (≥2.0) have near-guaranteed success")
    
    return results

def demo_technological_evolution_paths():
    """Demonstrate different technological evolution paths."""
    print("\n\n🛸 TECHNOLOGICAL EVOLUTION PATHS")
    print("=" * 80)
    
    scenarios = [
        {
            'name': 'Slow Tech Progress',
            'description': 'Conservative technological advancement',
            'starting_kardashev': 0.0,
            'growth_rate': 0.08,
            'time_left': 0.5
        },
        {
            'name': 'Moderate Tech Progress',
            'description': 'Earth-like technological advancement',
            'starting_kardashev': 0.73,
            'growth_rate': 0.15,
            'time_left': 0.5
        },
        {
            'name': 'Rapid Tech Progress',
            'description': 'AI-accelerated technological advancement',
            'starting_kardashev': 1.0,
            'growth_rate': 0.25,
            'time_left': 0.5
        },
        {
            'name': 'Advanced Start',
            'description': 'Civilization already at Type I+',
            'starting_kardashev': 1.5,
            'growth_rate': 0.12,
            'time_left': 0.3  # Less time but higher tech
        }
    ]
    
    print(f"📋 Comparing different technological evolution paths:")
    print(f"    Each civilization needs 0.25B years to reach another planet")
    print(f"    Risk tolerance: 20%\n")
    
    for scenario in scenarios:
        print(f"🔬 {scenario['name']}: {scenario['description']}")
        
        result = simulate_cosmic_consciousness_timing(
            evolution_duration=4.0,
            time_left=scenario['time_left'],
            window_needed=0.25,
            risk_tolerance=0.2,
            starting_kardashev_level=scenario['starting_kardashev'],
            kardashev_growth_rate=scenario['growth_rate'],
            kardashev_enabled=True
        )
        
        print(f"   Starting Level: {result['starting_kardashev_level']:.2f} ({result['starting_kardashev_name']})")
        print(f"   Final Level: {result['final_kardashev_level']:.2f} ({result['final_kardashev_name']})")
        print(f"   Effective Window Needed: {result['effective_window_needed']:.2f}B years")
        print(f"   Expansion Probability: {result['expansion_probability']:.1%}")
        print(f"   Outcome: {'✅ SUCCESS' if result['civilization_succeeds'] else '❌ FAILURE'}")
        print()

def demo_full_model_with_kardashev():
    """Demonstrate the full model with Kardashev Scale comparisons."""
    print("\n\n🌟 FULL MODEL WITH KARDASHEV SCALE")
    print("=" * 80)
    
    # Initialize model with Kardashev parameters
    model = CosmicConsciousnessTimingModel({
        'earth_extinction_time': 0.4,  # More challenging
        'baseline_starting_kardashev': 0.73,  # Start at modern human level
        'baseline_kardashev_growth_rate': 0.15,
        'kardashev_scenarios': [0.0, 0.5, 0.73, 1.0, 1.5, 2.0],
        'num_probabilistic_runs': 500
    })
    
    print("🔧 Model initialized with Kardashev Scale integration")
    print("📋 Running comprehensive Kardashev analysis...")
    
    simulation_config = {
        'scenario': {
            'evolution_duration_factor': 1.0,
            'window_needed': 0.25,
            'risk_tolerance': 0.2,
            'starting_kardashev_level': 0.73,
            'kardashev_growth_rate': 0.15,
            'kardashev_enabled': True,
            'random_delay': True
        }
    }
    
    results = model.simulate(simulation_config)
    
    # Display Kardashev comparison results
    print(f"\n📊 Kardashev Level Comparison:")
    print("-" * 60)
    
    for result in results['kardashev_comparison']:
        status = "✅ SUCCESS" if result['civilization_succeeds'] else "❌ FAILURE"
        print(f"{result['scenario_name']:>30}: {status} "
              f"(Prob: {result['expansion_probability']:>5.1%}, "
              f"Multiplier: {result['expansion_multiplier']:.2f}x)")
    
    # Display summary
    summary = results['summary']
    print(f"\n🎯 Analysis Summary:")
    print(f"- Evolution Delay Success Rate: {summary['deterministic_success_rate']:.1%}")
    print(f"- Kardashev Comparison Success Rate: {summary['kardashev_success_rate']:.1%}")
    print(f"- Kardashev Impact Level: {summary['kardashev_impact']}")
    print(f"- Average Kardashev Progression: {summary['baseline_kardashev_progression']:.2f} levels")
    
    if results['probabilistic_scenarios']['enabled']:
        prob_results = results['probabilistic_scenarios']
        print(f"- Probabilistic Success Rate: {prob_results['success_rate']:.1%}")
        print(f"- Average Kardashev Progression (Random): {prob_results['avg_kardashev_progression']:.2f} levels")
    
    return results

def demo_human_civilization_trajectory():
    """Analyze Earth's civilization trajectory with Kardashev Scale."""
    print("\n\n🌍 EARTH CIVILIZATION TRAJECTORY ANALYSIS")
    print("=" * 80)
    
    print("📊 Earth's Current Status (2025):")
    print("- Kardashev Level: 0.73 (Modern Humans)")
    print("- Energy Usage: ~2×10¹⁶ Watts")
    print("- Time until Earth uninhabitable: ~0.5B years")
    print("- Estimated time to reach another planet: 0.2B years")
    
    # Different growth scenarios for humanity
    growth_scenarios = [
        {'name': 'Conservative Growth', 'rate': 0.08, 'description': 'Slow technological progress'},
        {'name': 'Current Trend', 'rate': 0.15, 'description': 'Continuation of current growth'},
        {'name': 'AI Acceleration', 'rate': 0.25, 'description': 'AI-driven rapid advancement'},
        {'name': 'Breakthrough', 'rate': 0.40, 'description': 'Major scientific breakthroughs'}
    ]
    
    print(f"\n🚀 Human Civilization Outcomes by Growth Rate:")
    print("-" * 70)
    print(f"{'Scenario':<18} {'Growth Rate':<12} {'Final K-Level':<12} {'Outcome':<10} {'Prob'}")
    print("-" * 70)
    
    for scenario in growth_scenarios:
        result = simulate_cosmic_consciousness_timing(
            evolution_duration=4.0,
            time_left=0.5,
            window_needed=0.2,
            risk_tolerance=0.15,
            starting_kardashev_level=0.73,
            kardashev_growth_rate=scenario['rate'],
            kardashev_enabled=True
        )
        
        success = "✅ SUCCESS" if result['civilization_succeeds'] else "❌ FAILURE"
        
        print(f"{scenario['name']:<18} {scenario['rate']:<12.2f} "
              f"{result['final_kardashev_level']:<12.2f} {success:<10} "
              f"{result['expansion_probability']:.1%}")
    
    print(f"\n🎯 Key Insights for Humanity:")
    print("- Current growth rate gives reasonable survival chances")
    print("- Reaching Type I (K=1.0) significantly improves odds")
    print("- AI acceleration could be crucial for survival")
    print("- Time is critical - delays reduce success probability")

def export_kardashev_results(comparison_results, model_results, human_results):
    """Export comprehensive Kardashev analysis results."""
    output = {
        'simulation_type': 'cosmic_consciousness_kardashev_integration',
        'timestamp': str(np.datetime64('now')),
        'kardashev_scale_data': KARDASHEV_SCALE,
        'kardashev_comparison': comparison_results,
        'full_model_results': {
            'kardashev_comparison': model_results['kardashev_comparison'],
            'summary': model_results['summary']
        },
        'human_trajectory_analysis': human_results,
        'key_insights': [
            "Kardashev Scale dramatically affects civilization survival",
            "Type I civilizations (K≥1.0) have significant advantages",
            "Type II civilizations (K≥2.0) have near-guaranteed success",
            "Technological growth rate is as important as timing",
            "Current human trajectory gives moderate survival chances"
        ]
    }
    
    with open('kardashev_cosmic_analysis.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n💾 Comprehensive Kardashev analysis exported to: kardashev_cosmic_analysis.json")

def main():
    """Run the comprehensive Kardashev Scale cosmic consciousness demo."""
    print("🚀 Jinn-Core: Cosmic Consciousness Timing with Kardashev Scale")
    print("Exploring how technological advancement affects civilization survival\n")
    
    # Run all demonstrations
    demo_kardashev_scale_basics()
    comparison_results = demo_kardashev_impact_comparison()
    demo_technological_evolution_paths()
    model_results = demo_full_model_with_kardashev()
    human_results = demo_human_civilization_trajectory()
    
    # Export comprehensive results
    export_kardashev_results(comparison_results, model_results, human_results)
    
    print("\n" + "=" * 80)
    print("✅ Kardashev Scale Cosmic Consciousness Analysis Complete!")
    print("\n🌌 Revolutionary Insights:")
    print("- The Kardashev Scale is a critical factor in cosmic survival")
    print("- Technology advancement can overcome timing constraints")
    print("- Type I civilizations have dramatically better survival odds")
    print("- Humanity's current trajectory offers moderate hope")
    print("- AI acceleration could be key to our species' survival")
    print("\n🔮 This analysis suggests that technological advancement")
    print("   is as important as timing in explaining the Fermi Paradox!")

if __name__ == "__main__":
    import numpy as np
    main() 