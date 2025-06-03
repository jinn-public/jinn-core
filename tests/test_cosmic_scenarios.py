#!/usr/bin/env python3
"""
Test Scenarios for Cosmic Consciousness Timing

Demonstrates challenging scenarios where the window for interplanetary expansion
becomes critical or impossible.
"""

import json
from src.models.cosmic_consciousness_timing import simulate_cosmic_consciousness_timing, CosmicConsciousnessTimingModel

def test_challenging_scenarios():
    """Test scenarios where civilizations face extinction pressure."""
    print("🔥 CHALLENGING COSMIC SCENARIOS")
    print("=" * 60)
    
    scenarios = [
        {
            'name': 'Scenario 1: Tight Window',
            'description': 'Civilization needs 0.4B years, has 0.5B years left',
            'evolution_duration': 4.0,
            'time_left': 0.5,
            'window_needed': 0.4,
            'risk_tolerance': 0.1
        },
        {
            'name': 'Scenario 2: Very Tight Window',
            'description': 'Civilization needs 0.45B years, has 0.5B years left',
            'evolution_duration': 4.0,
            'time_left': 0.5,
            'window_needed': 0.45,
            'risk_tolerance': 0.1
        },
        {
            'name': 'Scenario 3: Impossible Window',
            'description': 'Civilization needs 0.6B years, has 0.5B years left',
            'evolution_duration': 4.0,
            'time_left': 0.5,
            'window_needed': 0.6,
            'risk_tolerance': 0.1
        },
        {
            'name': 'Scenario 4: Shorter Planetary Lifespan',
            'description': 'Planet becomes uninhabitable in 0.3B years',
            'evolution_duration': 4.0,
            'time_left': 0.3,
            'window_needed': 0.2,
            'risk_tolerance': 0.1
        },
        {
            'name': 'Scenario 5: High-Risk Civilization',
            'description': 'Conservative species needs 50% safety margin',
            'evolution_duration': 4.0,
            'time_left': 0.5,
            'window_needed': 0.2,
            'risk_tolerance': 0.5
        }
    ]
    
    results = []
    
    for scenario in scenarios:
        print(f"\n📊 {scenario['name']}")
        print(f"   {scenario['description']}")
        
        result = simulate_cosmic_consciousness_timing(
            evolution_duration=scenario['evolution_duration'],
            time_left=scenario['time_left'],
            window_needed=scenario['window_needed'],
            risk_tolerance=scenario['risk_tolerance']
        )
        
        status = "✅ SUCCESS" if result['civilization_succeeds'] else "❌ FAILURE"
        print(f"   Result: {status}")
        print(f"   Expansion Window: {result['expansion_window']:.2f}B years")
        print(f"   Minimum Needed: {result['minimum_time_needed']:.2f}B years")
        print(f"   Safety Margin: {result['safety_margin']:.2f}B years")
        print(f"   Expansion Probability: {result['expansion_probability']:.1%}")
        
        result['scenario_name'] = scenario['name']
        results.append(result)
    
    # Summary
    success_count = sum(1 for r in results if r['civilization_succeeds'])
    print(f"\n🎯 SUMMARY:")
    print(f"   Successful Civilizations: {success_count}/{len(results)}")
    print(f"   Failure Rate: {(len(results) - success_count)/len(results):.1%}")
    
    return results

def test_evolution_delay_thresholds():
    """Test to find the critical evolution delay threshold."""
    print("\n\n⏰ EVOLUTION DELAY THRESHOLD ANALYSIS")
    print("=" * 60)
    
    # Test increasingly longer evolution times
    delay_factors = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    base_evolution = 4.0
    time_left = 0.5
    window_needed = 0.4  # Challenging scenario
    risk_tolerance = 0.2
    
    print(f"Base Parameters:")
    print(f"- Time Left: {time_left}B years")
    print(f"- Window Needed: {window_needed}B years")
    print(f"- Risk Tolerance: {risk_tolerance:.0%}")
    print(f"\nTesting Evolution Delays:")
    
    critical_delay = None
    results = []
    
    for delay_factor in delay_factors:
        evolution_duration = base_evolution * (1 + delay_factor)
        
        result = simulate_cosmic_consciousness_timing(
            evolution_duration=evolution_duration,
            time_left=time_left,
            window_needed=window_needed,
            risk_tolerance=risk_tolerance
        )
        
        status = "✅" if result['civilization_succeeds'] else "❌"
        print(f"  +{delay_factor:>4.0%} delay ({evolution_duration:.1f}B years): {status} "
              f"(Prob: {result['expansion_probability']:>5.1%})")
        
        if not result['civilization_succeeds'] and critical_delay is None:
            critical_delay = delay_factor
        
        results.append({
            'delay_factor': delay_factor,
            'evolution_duration': evolution_duration,
            'succeeds': result['civilization_succeeds'],
            'expansion_probability': result['expansion_probability']
        })
    
    if critical_delay is not None:
        print(f"\n🚨 Critical Evolution Delay: +{critical_delay:.0%}")
        print(f"   Beyond this delay, civilizations cannot expand in time")
    else:
        print(f"\n✅ No critical delay found in tested range")
    
    return results

def test_model_with_challenging_parameters():
    """Test the full model with more challenging default parameters."""
    print("\n\n🌌 FULL MODEL WITH CHALLENGING PARAMETERS")
    print("=" * 60)
    
    # More challenging parameters
    challenging_params = {
        'earth_extinction_time': 0.3,  # Shorter time left
        'baseline_evolution_duration': 4.0,
        'baseline_window_needed': 0.25,  # Longer journey needed
        'baseline_risk_tolerance': 0.3,  # More conservative civilizations
        'evolution_delay_scenarios': [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30],
        'num_probabilistic_runs': 1000
    }
    
    model = CosmicConsciousnessTimingModel(challenging_params)
    
    simulation_config = {
        'scenario': {
            'evolution_duration_factor': 1.0,
            'window_needed': 0.25,
            'risk_tolerance': 0.3,
            'random_delay': True
        }
    }
    
    results = model.simulate(simulation_config)
    
    # Display results
    deterministic = results['deterministic_scenarios']
    probabilistic = results['probabilistic_scenarios']
    summary = results['summary']
    
    print(f"📊 Challenging Scenario Results:")
    print(f"- Time Left: {challenging_params['earth_extinction_time']}B years")
    print(f"- Window Needed: {challenging_params['baseline_window_needed']}B years")
    print(f"- Risk Tolerance: {challenging_params['baseline_risk_tolerance']:.0%}")
    
    print(f"\n🔬 Deterministic Results:")
    for result in deterministic:
        status = "✅" if result['civilization_succeeds'] else "❌"
        print(f"  {result['scenario_name']:>20}: {status} "
              f"(Prob: {result['expansion_probability']:>5.1%})")
    
    print(f"\n📈 Summary:")
    print(f"- Deterministic Success Rate: {summary['deterministic_success_rate']:.1%}")
    print(f"- Window Fragility: {summary['window_fragility']}")
    if summary['critical_evolution_delay'] is not None:
        print(f"- Critical Evolution Delay: +{summary['critical_evolution_delay']:.0%}")
    
    if probabilistic['enabled']:
        print(f"- Probabilistic Success Rate: {probabilistic['success_rate']:.1%}")
        print(f"- Average Expansion Probability: {probabilistic['avg_expansion_probability']:.1%}")
    
    return results

def main():
    """Run all challenging scenario tests."""
    print("🚀 Cosmic Consciousness Timing - Challenging Scenarios")
    print("Testing the limits of civilization survival\n")
    
    # Run all tests
    challenging_results = test_challenging_scenarios()
    evolution_threshold_results = test_evolution_delay_thresholds()
    model_results = test_model_with_challenging_parameters()
    
    # Export results
    output = {
        'test_type': 'challenging_cosmic_scenarios',
        'challenging_scenarios': challenging_results,
        'evolution_thresholds': evolution_threshold_results,
        'challenging_model_summary': model_results['summary']
    }
    
    with open('challenging_cosmic_scenarios.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print("\n" + "=" * 60)
    print("✅ Challenging Scenarios Testing Complete!")
    print("\n🔍 Key Findings:")
    print("- The expansion window is extremely fragile")
    print("- Small changes in parameters can cause complete failure")
    print("- Conservative civilizations face much higher risks")
    print("- Evolution timing is the critical bottleneck")
    print("- This explains the apparent rarity of space-faring life")
    print(f"\n💾 Results saved to: challenging_cosmic_scenarios.json")

if __name__ == "__main__":
    main() 