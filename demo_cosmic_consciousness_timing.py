#!/usr/bin/env python3
"""
Cosmic Consciousness Timing Simulation Demo

Demonstrates the cosmic consciousness timing simulation capabilities of Jinn-Core.
Simulates the emergence of intelligent life and the window for interplanetary expansion.
"""

import json
import logging
from src.models.cosmic_consciousness_timing import simulate_cosmic_consciousness_timing, CosmicConsciousnessTimingModel

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def demo_simple_function():
    """Demonstrate the simple cosmic consciousness timing function."""
    print("🌌 COSMIC CONSCIOUSNESS TIMING - Simple Function Demo")
    print("=" * 70)
    
    # Scenario 1: Baseline (Earth-like conditions)
    print("\n📊 Scenario 1: Baseline Earth Conditions")
    print("- Evolution Duration: 4.0 billion years")
    print("- Time Left: 0.5 billion years")  
    print("- Window Needed: 0.2 billion years")
    print("- Risk Tolerance: 10%")
    
    result1 = simulate_cosmic_consciousness_timing(
        evolution_duration=4.0,
        time_left=0.5,
        window_needed=0.2,
        risk_tolerance=0.1
    )
    
    print(f"\n📈 Results:")
    print(f"- Consciousness Emerges: {result1['consciousness_emergence_time']:.1f} billion years after planet formation")
    print(f"- Expansion Window: {result1['expansion_window']:.2f} billion years")
    print(f"- Minimum Time Needed: {result1['minimum_time_needed']:.2f} billion years")
    print(f"- Civilization Succeeds: {'✅ YES' if result1['civilization_succeeds'] else '❌ NO'}")
    print(f"- Safety Margin: {result1['safety_margin']:.2f} billion years")
    print(f"- Expansion Probability: {result1['expansion_probability']:.1%}")
    
    # Scenario 2: Delayed evolution (+10%)
    print("\n\n📊 Scenario 2: Delayed Evolution (+10%)")
    print("- Evolution Duration: 4.4 billion years (+10%)")
    print("- Time Left: 0.5 billion years")
    print("- Window Needed: 0.2 billion years")
    print("- Risk Tolerance: 10%")
    
    result2 = simulate_cosmic_consciousness_timing(
        evolution_duration=4.4,
        time_left=0.5,
        window_needed=0.2,
        risk_tolerance=0.1
    )
    
    print(f"\n📈 Results:")
    print(f"- Consciousness Emerges: {result2['consciousness_emergence_time']:.1f} billion years after planet formation")
    print(f"- Expansion Window: {result2['expansion_window']:.2f} billion years")
    print(f"- Minimum Time Needed: {result2['minimum_time_needed']:.2f} billion years")
    print(f"- Civilization Succeeds: {'✅ YES' if result2['civilization_succeeds'] else '❌ NO'}")
    print(f"- Safety Margin: {result2['safety_margin']:.2f} billion years")
    print(f"- Expansion Probability: {result2['expansion_probability']:.1%}")
    
    # Scenario 3: More conservative civilization
    print("\n\n📊 Scenario 3: Conservative Civilization (Higher Risk Tolerance)")
    print("- Evolution Duration: 4.0 billion years")
    print("- Time Left: 0.5 billion years")
    print("- Window Needed: 0.3 billion years (longer journey)")
    print("- Risk Tolerance: 20% (more conservative)")
    
    result3 = simulate_cosmic_consciousness_timing(
        evolution_duration=4.0,
        time_left=0.5,
        window_needed=0.3,
        risk_tolerance=0.2
    )
    
    print(f"\n📈 Results:")
    print(f"- Consciousness Emerges: {result3['consciousness_emergence_time']:.1f} billion years after planet formation")
    print(f"- Expansion Window: {result3['expansion_window']:.2f} billion years")
    print(f"- Minimum Time Needed: {result3['minimum_time_needed']:.2f} billion years")
    print(f"- Civilization Succeeds: {'✅ YES' if result3['civilization_succeeds'] else '❌ NO'}")
    print(f"- Safety Margin: {result3['safety_margin']:.2f} billion years")
    print(f"- Expansion Probability: {result3['expansion_probability']:.1%}")
    
    return [result1, result2, result3]

def demo_full_simulation():
    """Demonstrate the full cosmic consciousness timing simulation."""
    print("\n\n🌟 COSMIC CONSCIOUSNESS TIMING - Full Model Demo")
    print("=" * 70)
    
    # Initialize the model
    model = CosmicConsciousnessTimingModel({})
    print("🔧 Model initialized with default cosmic parameters")
    
    print("\n📋 Running Scenario: Evolution Timing Analysis")
    print("- Testing multiple evolution delay scenarios")
    print("- Baseline: 4.0B years, +5%, +10%, +20% delays")
    print("- Window needed: 0.2B years")
    print("- Risk tolerance: 10%")
    
    # Configuration for deterministic scenarios
    simulation_config = {
        'scenario': {
            'evolution_duration_factor': 1.0,
            'window_needed': 0.2,
            'risk_tolerance': 0.1,
            'random_delay': False
        }
    }
    
    # Run the simulation
    results = model.simulate(simulation_config)
    
    # Extract results
    deterministic = results['deterministic_scenarios']
    summary = results['summary']
    
    print(f"\n📊 Deterministic Scenario Results:")
    print("-" * 50)
    
    for result in deterministic:
        status = "✅ SUCCESS" if result['civilization_succeeds'] else "❌ FAILURE"
        print(f"{result['scenario_name']:>20}: {status} "
              f"(Prob: {result['expansion_probability']:>5.1%}, "
              f"Window: {result['expansion_window']:.2f}B years)")
    
    print(f"\n🎯 Summary Statistics:")
    print(f"- Overall Success Rate: {summary['deterministic_success_rate']:.1%}")
    print(f"- Scenarios Passing: {summary['deterministic_scenarios_passing']}/{summary['total_deterministic_scenarios']}")
    print(f"- Baseline Window: {summary['baseline_expansion_window']:.2f} billion years")
    print(f"- Window Fragility: {summary['window_fragility']}")
    if summary['critical_evolution_delay'] is not None:
        print(f"- Critical Evolution Delay: +{summary['critical_evolution_delay']:.0%}")
    else:
        print(f"- Critical Evolution Delay: None (all scenarios succeed)")
    
    return results

def demo_probabilistic_analysis():
    """Demonstrate probabilistic analysis with random variations."""
    print("\n\n🎲 COSMIC CONSCIOUSNESS TIMING - Probabilistic Analysis")
    print("=" * 70)
    
    # Initialize the model
    model = CosmicConsciousnessTimingModel({
        'num_probabilistic_runs': 1000
    })
    
    print("\n📋 Running Probabilistic Scenario:")
    print("- 1000 randomized simulations")
    print("- ±30% variation in evolution duration")
    print("- ±20% variation in window needed")
    print("- ±50% variation in risk tolerance")
    
    # Configuration for probabilistic scenarios
    simulation_config = {
        'scenario': {
            'evolution_duration_factor': 1.0,
            'window_needed': 0.2,
            'risk_tolerance': 0.1,
            'random_delay': True
        }
    }
    
    # Run the simulation
    results = model.simulate(simulation_config)
    
    # Extract results
    probabilistic = results['probabilistic_scenarios']
    summary = results['summary']
    
    print(f"\n📊 Probabilistic Results:")
    print("-" * 40)
    print(f"- Overall Success Rate: {probabilistic['success_rate']:.1%}")
    print(f"- Average Expansion Probability: {probabilistic['avg_expansion_probability']:.1%}")
    
    print(f"\n📈 Confidence Intervals:")
    for percentile, data in probabilistic['percentiles'].items():
        print(f"- {percentile:>3}: Success Rate {data['success_rate']:.1%}, "
              f"Expansion Prob {data['expansion_probability']:.1%}")
    
    # Compare with deterministic
    print(f"\n🔄 Comparison:")
    print(f"- Deterministic Success Rate: {summary['deterministic_success_rate']:.1%}")
    print(f"- Probabilistic Success Rate: {summary['probabilistic_success_rate']:.1%}")
    print(f"- Difference: {summary['probabilistic_success_rate'] - summary['deterministic_success_rate']:+.1%}")
    
    return results

def export_results_json(simple_results, full_results, probabilistic_results):
    """Export results to JSON for further analysis."""
    output = {
        'simulation_type': 'cosmic_consciousness_timing',
        'timestamp': str(np.datetime64('now')),
        'simple_function_results': simple_results,
        'full_model_deterministic': full_results['deterministic_scenarios'],
        'full_model_summary': full_results['summary'],
        'probabilistic_analysis': {
            'success_rate': probabilistic_results['probabilistic_scenarios']['success_rate'],
            'confidence_intervals': probabilistic_results['probabilistic_scenarios']['percentiles']
        }
    }
    
    with open('cosmic_consciousness_timing_results.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n💾 Results exported to: cosmic_consciousness_timing_results.json")

def main():
    """Run the cosmic consciousness timing simulation demo."""
    print("🚀 Jinn-Core Cosmic Consciousness Timing Simulation Demo")
    print("Exploring the fragile window for interplanetary expansion\n")
    
    # Run demonstrations
    simple_results = demo_simple_function()
    full_results = demo_full_simulation()
    probabilistic_results = demo_probabilistic_analysis()
    
    # Export results
    export_results_json(simple_results, full_results, probabilistic_results)
    
    print("\n" + "=" * 70)
    print("✅ Cosmic Consciousness Timing Simulation Demo Complete!")
    print("\n🔍 Key Insights:")
    print("- The window for space expansion is extremely narrow")
    print("- Small delays in evolution can lead to complete failure")
    print("- Conservative civilizations face higher extinction risk")
    print("- Timing is more critical than technological capability")
    print("- The fragility highlights the rarity of space-faring life")
    
    print(f"\n🌌 Cosmic Perspective:")
    print("This simulation shows how easily the window for")
    print("interplanetary expansion can be missed, helping explain")
    print("the Fermi Paradox and the apparent rarity of")
    print("space-faring civilizations in our universe.")

if __name__ == "__main__":
    import numpy as np
    main() 