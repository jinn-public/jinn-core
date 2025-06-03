#!/usr/bin/env python3
"""
Bank Panic Simulation Demo

Demonstrates the bank panic simulation capabilities of Jinn-Core.
"""

import logging
from src.engine import SimulationEngine
from src.models.bank_panic import simulate_bank_panic

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def demo_simple_function():
    """Demonstrate the simple bank panic function."""
    print("🏦 BANK PANIC SIMULATION - Simple Function Demo")
    print("=" * 60)
    
    # Scenario: Major regional bank under stress
    print("\n📊 Scenario: Major Regional Bank Crisis")
    print("- Total Deposits: $100 billion")
    print("- Liquid Reserves: $15 billion (15% ratio)")
    print("- Panic Withdrawal Rate: 20% per day")
    print("- Central Bank Support: $10 billion")
    
    result = simulate_bank_panic(
        total_deposits=100_000_000_000,
        liquid_reserves=15_000_000_000,
        withdrawal_rate=20.0,
        central_bank_support=10_000_000_000
    )
    
    print(f"\n📈 Results:")
    print(f"- Daily Withdrawals: ${result['daily_withdrawals']/1e9:.1f} billion")
    print(f"- Remaining Liquidity: ${result['remaining_liquidity']/1e9:.1f} billion")
    print(f"- Bank Can Survive: {result['survival_days']} days")
    print(f"- Bank Survives Crisis: {'✅ YES' if result['bank_survives'] else '❌ NO'}")
    print(f"- Final Liquidity Ratio: {result['liquidity_ratio']:.1f}%")
    
    return result

def demo_full_simulation():
    """Demonstrate the full bank panic simulation."""
    print("\n\n🏛️ BANK PANIC SIMULATION - Full Model Demo")
    print("=" * 60)
    
    engine = SimulationEngine()
    print(f"🔧 Available Models: {', '.join(engine.models.keys())}")
    
    print("\n📋 Running Scenario: Regional Banking Crisis")
    print("- 8 banks in the system")
    print("- 20% daily withdrawal rate during panic")
    print("- 5-day panic duration starting on day 3")
    print("- Central bank intervention threshold: 15%")
    print("- Maximum CB support: $50 billion")
    
    # Run the simulation
    results = engine.run_scenario_file('examples/scenario_03_bank_panic.json')
    
    # Extract key results
    simulation_results = results['results']
    summary = simulation_results['summary']
    
    print(f"\n📊 Simulation Results:")
    print(f"- Crisis Severity: {summary['crisis_severity']}")
    print(f"- Banks Failed: {summary['max_banks_failed']}/8")
    print(f"- Banks Surviving: {summary['final_banks_surviving']}/8")
    print(f"- Total Central Bank Support: ${summary['total_cb_support']/1e9:.1f} billion")
    print(f"- Minimum Liquidity Ratio: {summary['min_liquidity_ratio']:.1f}%")
    print(f"- Maximum Daily Withdrawals: ${summary['max_daily_withdrawals']/1e9:.1f} billion")
    print(f"- Total Economic Impact: {summary['total_gdp_impact']:.3f}% GDP")
    print(f"- Peak Economic Impact: {summary['peak_gdp_impact']:.3f}% GDP")
    
    # Final assessment
    final_assessment = summary['final_assessment']
    print(f"\n🎯 Final Assessment:")
    print(f"- System Survival: {'✅ STABLE' if final_assessment['bank_survives'] else '❌ FAILED'}")
    print(f"- Survival Capacity: {final_assessment['survival_days']} days")
    print(f"- Final Liquidity Ratio: {final_assessment['liquidity_ratio']:.1f}%")
    
    # Show time series highlights
    periods = simulation_results['periods']
    panic_intensity = simulation_results['panic_intensity']
    liquidity_ratio = simulation_results['liquidity_ratio']
    cb_support = simulation_results['central_bank_support']
    
    print(f"\n📈 Crisis Timeline Highlights:")
    for i, period in enumerate(periods[:10]):  # Show first 10 days
        if panic_intensity[i] > 0 or cb_support[i] > 0:
            status = ""
            if panic_intensity[i] > 0:
                status += f"🚨 Panic: {panic_intensity[i]:.1%} "
            if cb_support[i] > 0:
                status += f"🏛️ CB Support: ${cb_support[i]/1e9:.1f}B "
            print(f"  Day {period}: Liquidity {liquidity_ratio[i]:.1f}% {status}")
    
    return results

def main():
    """Run the bank panic simulation demo."""
    print("🚀 Jinn-Core Bank Panic Simulation Demo")
    print("Simulating banking crises and systemic risk scenarios\n")
    
    # Run demonstrations
    simple_result = demo_simple_function()
    full_result = demo_full_simulation()
    
    print("\n" + "=" * 60)
    print("✅ Bank Panic Simulation Demo Complete!")
    print("\nKey Insights:")
    print("- The simple function provides quick crisis assessment")
    print("- The full model simulates complex multi-bank scenarios")
    print("- Central bank intervention can prevent systemic collapse")
    print("- Contagion effects amplify individual bank failures")
    print("- Economic impacts extend beyond the banking sector")

if __name__ == "__main__":
    main() 