#!/usr/bin/env python3
"""
Visualization for Cosmic Consciousness Timing

Creates graphs showing the relationship between consciousness emergence timing
and civilization survival probability.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import json
from src.models.cosmic_consciousness_timing import simulate_cosmic_consciousness_timing

def create_consciousness_vs_survival_graph():
    """Create a graph showing consciousness time vs survival probability."""
    print("📊 Creating Consciousness vs Survival Probability Graph")
    
    # Parameters for the analysis
    base_evolution = 4.0  # billion years
    time_left = 0.4      # billion years (more challenging)
    window_needed = 0.25  # billion years
    risk_tolerance = 0.2  # 20%
    
    # Test range of evolution delays
    delay_factors = np.linspace(0.0, 0.8, 50)  # 0% to 80% delays
    evolution_times = []
    survival_probabilities = []
    civilization_succeeds = []
    
    print(f"Testing {len(delay_factors)} evolution delay scenarios...")
    
    for delay_factor in delay_factors:
        evolution_duration = base_evolution * (1 + delay_factor)
        
        result = simulate_cosmic_consciousness_timing(
            evolution_duration=evolution_duration,
            time_left=time_left,
            window_needed=window_needed,
            risk_tolerance=risk_tolerance
        )
        
        evolution_times.append(evolution_duration)
        survival_probabilities.append(result['expansion_probability'])
        civilization_succeeds.append(result['civilization_succeeds'])
    
    # Create the plot
    plt.figure(figsize=(12, 8))
    
    # Main plot: Evolution time vs survival probability
    plt.subplot(2, 1, 1)
    plt.plot(evolution_times, survival_probabilities, 'b-', linewidth=2, label='Survival Probability')
    
    # Color the background based on success/failure
    for i, (evo_time, succeeds) in enumerate(zip(evolution_times, civilization_succeeds)):
        color = 'lightgreen' if succeeds else 'lightcoral'
        if i < len(evolution_times) - 1:
            plt.axvspan(evo_time, evolution_times[i+1], alpha=0.3, color=color)
    
    plt.xlabel('Consciousness Emergence Time (Billion Years)')
    plt.ylabel('Expansion Probability')
    plt.title('Cosmic Consciousness Timing: Survival vs Evolution Duration')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Add annotations
    earth_evolution = 4.0
    plt.axvline(x=earth_evolution, color='red', linestyle='--', alpha=0.7, label='Earth Timeline')
    plt.text(earth_evolution + 0.1, 0.5, 'Earth\n(4.0B years)', fontsize=10, color='red')
    
    # Second subplot: Success/Failure regions
    plt.subplot(2, 1, 2)
    success_mask = np.array(civilization_succeeds)
    failure_mask = ~success_mask
    
    plt.scatter(np.array(evolution_times)[success_mask], 
               np.ones(np.sum(success_mask)), 
               c='green', label='Success', alpha=0.7, s=30)
    plt.scatter(np.array(evolution_times)[failure_mask], 
               np.zeros(np.sum(failure_mask)), 
               c='red', label='Failure', alpha=0.7, s=30)
    
    plt.xlabel('Consciousness Emergence Time (Billion Years)')
    plt.ylabel('Civilization Outcome')
    plt.yticks([0, 1], ['Failure', 'Success'])
    plt.title('Success/Failure Threshold')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.axvline(x=earth_evolution, color='red', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('consciousness_vs_survival.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"📊 Graph saved as: consciousness_vs_survival.png")
    
    return {
        'evolution_times': evolution_times,
        'survival_probabilities': survival_probabilities,
        'civilization_succeeds': civilization_succeeds
    }

def create_parameter_sensitivity_analysis():
    """Create graphs showing sensitivity to different parameters."""
    print("\n📊 Creating Parameter Sensitivity Analysis")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Cosmic Consciousness Timing: Parameter Sensitivity Analysis', fontsize=16)
    
    base_params = {
        'evolution_duration': 4.0,
        'time_left': 0.4,  # More challenging
        'window_needed': 0.25,
        'risk_tolerance': 0.2
    }
    
    # 1. Window needed sensitivity
    axes[0, 0].set_title('Window Needed Sensitivity')
    window_values = np.linspace(0.1, 0.6, 30)
    probs = []
    for window in window_values:
        result = simulate_cosmic_consciousness_timing(
            evolution_duration=base_params['evolution_duration'],
            time_left=base_params['time_left'],
            window_needed=window,
            risk_tolerance=base_params['risk_tolerance']
        )
        probs.append(result['expansion_probability'])
    
    axes[0, 0].plot(window_values, probs, 'g-', linewidth=2)
    axes[0, 0].set_xlabel('Window Needed (Billion Years)')
    axes[0, 0].set_ylabel('Expansion Probability')
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].axvline(x=base_params['window_needed'], color='red', linestyle='--', alpha=0.7)
    
    # 2. Time left sensitivity
    axes[0, 1].set_title('Time Left Sensitivity')
    time_values = np.linspace(0.2, 0.8, 30)
    probs = []
    for time_val in time_values:
        result = simulate_cosmic_consciousness_timing(
            evolution_duration=base_params['evolution_duration'],
            time_left=time_val,
            window_needed=base_params['window_needed'],
            risk_tolerance=base_params['risk_tolerance']
        )
        probs.append(result['expansion_probability'])
    
    axes[0, 1].plot(time_values, probs, 'b-', linewidth=2)
    axes[0, 1].set_xlabel('Time Left (Billion Years)')
    axes[0, 1].set_ylabel('Expansion Probability')
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].axvline(x=base_params['time_left'], color='red', linestyle='--', alpha=0.7)
    
    # 3. Risk tolerance sensitivity
    axes[1, 0].set_title('Risk Tolerance Sensitivity')
    risk_values = np.linspace(0.0, 0.5, 30)
    probs = []
    for risk in risk_values:
        result = simulate_cosmic_consciousness_timing(
            evolution_duration=base_params['evolution_duration'],
            time_left=base_params['time_left'],
            window_needed=base_params['window_needed'],
            risk_tolerance=risk
        )
        probs.append(result['expansion_probability'])
    
    axes[1, 0].plot(risk_values * 100, probs, 'orange', linewidth=2)
    axes[1, 0].set_xlabel('Risk Tolerance (%)')
    axes[1, 0].set_ylabel('Expansion Probability')
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].axvline(x=base_params['risk_tolerance'] * 100, color='red', linestyle='--', alpha=0.7)
    
    # 4. Evolution duration sensitivity
    axes[1, 1].set_title('Evolution Duration Sensitivity')
    evo_values = np.linspace(3.5, 5.5, 30)
    probs = []
    for evo in evo_values:
        result = simulate_cosmic_consciousness_timing(
            evolution_duration=evo,
            time_left=base_params['time_left'],
            window_needed=base_params['window_needed'],
            risk_tolerance=base_params['risk_tolerance']
        )
        probs.append(result['expansion_probability'])
    
    axes[1, 1].plot(evo_values, probs, 'purple', linewidth=2)
    axes[1, 1].set_xlabel('Evolution Duration (Billion Years)')
    axes[1, 1].set_ylabel('Expansion Probability')
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].axvline(x=base_params['evolution_duration'], color='red', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('parameter_sensitivity.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"📊 Sensitivity analysis saved as: parameter_sensitivity.png")

def create_fermi_paradox_illustration():
    """Create a visualization illustrating the Fermi Paradox connection."""
    print("\n📊 Creating Fermi Paradox Illustration")
    
    # Simulate many civilizations with different parameters
    np.random.seed(42)  # For reproducible results
    
    n_civilizations = 1000
    success_count = 0
    
    evolution_times = []
    windows_needed = []
    success_status = []
    
    for i in range(n_civilizations):
        # Random variations in parameters
        evolution_duration = np.random.normal(4.0, 0.5)  # ±0.5B years variation
        time_left = np.random.normal(0.4, 0.1)  # ±0.1B years variation, more challenging
        window_needed = np.random.normal(0.25, 0.05)  # ±0.05B years variation
        risk_tolerance = np.random.uniform(0.1, 0.3)  # 10-30% range
        
        # Ensure positive values
        evolution_duration = max(0.1, evolution_duration)
        time_left = max(0.1, time_left)
        window_needed = max(0.05, window_needed)
        
        result = simulate_cosmic_consciousness_timing(
            evolution_duration=evolution_duration,
            time_left=time_left,
            window_needed=window_needed,
            risk_tolerance=risk_tolerance
        )
        
        evolution_times.append(evolution_duration)
        windows_needed.append(window_needed)
        success_status.append(result['civilization_succeeds'])
        
        if result['civilization_succeeds']:
            success_count += 1
    
    # Create the visualization
    plt.figure(figsize=(12, 8))
    
    # Convert to numpy arrays for easier indexing
    evolution_times = np.array(evolution_times)
    windows_needed = np.array(windows_needed)
    success_status = np.array(success_status)
    
    # Scatter plot
    success_mask = success_status
    failure_mask = ~success_status
    
    plt.scatter(evolution_times[failure_mask], windows_needed[failure_mask], 
               c='red', alpha=0.6, s=20, label=f'Failed Civilizations ({np.sum(failure_mask)})')
    plt.scatter(evolution_times[success_mask], windows_needed[success_mask], 
               c='green', alpha=0.8, s=20, label=f'Successful Civilizations ({np.sum(success_mask)})')
    
    plt.xlabel('Evolution Duration (Billion Years)')
    plt.ylabel('Window Needed for Expansion (Billion Years)')
    plt.title(f'Fermi Paradox Illustration: {n_civilizations} Simulated Civilizations\n'
              f'Success Rate: {success_count/n_civilizations:.1%}')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Add Earth marker
    plt.scatter([4.0], [0.25], c='blue', s=100, marker='*', 
               label='Earth-like Conditions', edgecolors='black', linewidth=1)
    
    plt.legend()
    plt.tight_layout()
    plt.savefig('fermi_paradox_illustration.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"📊 Fermi Paradox illustration saved as: fermi_paradox_illustration.png")
    print(f"🎯 Simulation Results:")
    print(f"   - Total Civilizations: {n_civilizations}")
    print(f"   - Successful Civilizations: {success_count}")
    print(f"   - Success Rate: {success_count/n_civilizations:.1%}")
    print(f"   - This low success rate helps explain the apparent")
    print(f"     rarity of space-faring civilizations in our universe!")
    
    return {
        'total_civilizations': n_civilizations,
        'successful_civilizations': success_count,
        'success_rate': success_count/n_civilizations
    }

def main():
    """Run all visualizations."""
    print("🚀 Cosmic Consciousness Timing - Visualization Suite")
    print("Creating graphs to illustrate the fragile window for space expansion\n")
    
    # Create all visualizations
    consciousness_data = create_consciousness_vs_survival_graph()
    create_parameter_sensitivity_analysis()
    fermi_data = create_fermi_paradox_illustration()
    
    # Export summary data
    summary = {
        'visualization_type': 'cosmic_consciousness_timing_graphs',
        'consciousness_vs_survival': consciousness_data,
        'fermi_paradox_simulation': fermi_data
    }
    
    with open('visualization_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("\n" + "=" * 60)
    print("✅ All Visualizations Complete!")
    print("\n📊 Generated Files:")
    print("   - consciousness_vs_survival.png")
    print("   - parameter_sensitivity.png")
    print("   - fermi_paradox_illustration.png")
    print("   - visualization_summary.json")
    print("\n🌌 These graphs illustrate the narrow window for")
    print("   interplanetary expansion and help explain the")
    print("   Fermi Paradox - why we don't observe many")
    print("   space-faring civilizations in our universe.")

if __name__ == "__main__":
    main() 