"""
Plastic Spread Simulation Model

Environmental and economic model for simulating the accumulation of plastic waste
and its impact on Earth's surface coverage, marine ecosystems, and economic costs.
"""

import numpy as np
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class PlasticSpreadShock:
    """Configuration for plastic waste accumulation simulation."""
    annual_production_tonnes: float    # Initial annual plastic production (tonnes)
    annual_growth_rate: float          # Annual growth rate in production
    coverage_density_kg_per_sq_km: float  # kg of plastic needed for visible coverage per sq km
    simulation_years: int              # Number of years to simulate


def simulate_plastic_spread(
    annual_production_tonnes: float,
    annual_growth_rate: float,
    coverage_density_kg_per_sq_km: float,
    earth_surface_area_sq_km: float = 510_000_000,
    ocean_area_sq_km: float = 361_000_000,
    current_year: int = 0
) -> Dict[str, float]:
    """
    Simple, interpretable function to simulate plastic waste accumulation.
    
    Args:
        annual_production_tonnes: Annual plastic production in tonnes
        annual_growth_rate: Annual growth rate in production (decimal)
        coverage_density_kg_per_sq_km: kg of plastic per sq km for visible coverage
        earth_surface_area_sq_km: Total Earth surface area
        ocean_area_sq_km: Ocean surface area
        current_year: Current simulation year
        
    Returns:
        Dict containing:
        - current_production_tonnes: Current year production
        - total_plastic_accumulated_kg: Total plastic accumulated to date
        - earth_coverage_percent: Percentage of Earth's surface covered
        - ocean_coverage_percent: Percentage of ocean surface covered
        - cleanup_cost_billion_usd: Estimated cleanup cost
        - environmental_damage_cost_billion_usd: Environmental damage cost
    """
    # Calculate current year production with compound growth
    current_production_tonnes = annual_production_tonnes * ((1 + annual_growth_rate) ** current_year)
    
    # Estimate total accumulated plastic (assuming 80% of all plastic ever produced still exists)
    total_years_production = sum(
        annual_production_tonnes * ((1 + annual_growth_rate) ** year) 
        for year in range(current_year + 1)
    )
    total_plastic_accumulated_kg = total_years_production * 1000 * 0.8  # 80% persistence rate
    
    # Calculate coverage percentages
    total_coverage_area = total_plastic_accumulated_kg / coverage_density_kg_per_sq_km
    earth_coverage_percent = min((total_coverage_area / earth_surface_area_sq_km) * 100, 100)
    ocean_coverage_percent = min((total_coverage_area * 0.7 / ocean_area_sq_km) * 100, 100)  # 70% ends up in oceans
    
    # Economic cost calculations
    # Cleanup cost: $1,000 per tonne of plastic
    cleanup_cost_billion_usd = (total_plastic_accumulated_kg / 1000) * 1000 / 1e9
    
    # Environmental damage cost based on coverage (exponential increase)
    damage_multiplier = 1 + (earth_coverage_percent / 10) ** 2  # Accelerating damage
    environmental_damage_cost_billion_usd = cleanup_cost_billion_usd * damage_multiplier
    
    return {
        'current_production_tonnes': current_production_tonnes,
        'total_plastic_accumulated_kg': total_plastic_accumulated_kg,
        'earth_coverage_percent': earth_coverage_percent,
        'ocean_coverage_percent': ocean_coverage_percent,
        'cleanup_cost_billion_usd': cleanup_cost_billion_usd,
        'environmental_damage_cost_billion_usd': environmental_damage_cost_billion_usd
    }


class PlasticSpreadSimulationModel:
    """
    Plastic Spread Simulation Model
    
    Simulates the environmental and economic effects of plastic waste accumulation including:
    - Global plastic production growth
    - Surface coverage progression (land and ocean)
    - Economic costs of cleanup and environmental damage
    - Policy intervention scenarios (production caps, recycling improvements)
    - Tipping points for ecosystem collapse
    """
    
    def __init__(self, parameters: Dict[str, Any]):
        """
        Initialize the Plastic Spread Simulation Model.
        
        Args:
            parameters: Model calibration parameters
        """
        self.parameters = self._validate_parameters(parameters)
        logger.info("Plastic Spread Simulation Model initialized")
    
    def _validate_parameters(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and set default parameters."""
        defaults = {
            # Plastic production parameters
            'annual_production_tonnes': 400_000_000,    # 400 million tonnes (2023 estimate)
            'annual_growth_rate': 0.03,                 # 3% annual growth
            'production_cap_enabled': False,            # Whether to apply production caps
            'production_cap_year': 10,                  # Year when cap is applied
            'production_cap_multiplier': 1.5,           # Max production as multiple of initial
            
            # Coverage and spread parameters
            'coverage_density_kg_per_sq_km': 1_000,     # kg plastic per sq km for visible coverage
            'earth_surface_area_sq_km': 510_000_000,    # Total Earth surface area
            'ocean_area_sq_km': 361_000_000,            # Ocean surface area
            'land_area_sq_km': 149_000_000,             # Land surface area
            'plastic_persistence_rate': 0.8,            # Percentage of plastic that persists
            'ocean_allocation_rate': 0.7,               # Percentage that ends up in oceans
            
            # Economic parameters
            'cleanup_cost_per_tonne': 1000.0,           # USD per tonne cleanup cost
            'environmental_damage_multiplier': 2.0,     # Damage cost multiplier
            'gdp_impact_threshold': 0.1,                # Coverage % where GDP impact starts
            'gdp_impact_sensitivity': -0.02,            # GDP impact per % coverage
            
            # Recycling and intervention parameters
            'recycling_improvement_enabled': False,     # Whether recycling improves
            'recycling_improvement_year': 5,            # Year when recycling improves
            'initial_recycling_rate': 0.09,             # Current recycling rate (9%)
            'target_recycling_rate': 0.5,               # Target recycling rate (50%)
            'recycling_improvement_rate': 0.05,         # Annual improvement in recycling
            
            # Simulation parameters
            'periods': 50,                              # 50 years simulation
            'baseline_gdp': 100_000_000_000_000.0,      # $100 trillion global GDP
        }
        
        # Merge with provided parameters
        for key, default_value in defaults.items():
            if key not in params:
                params[key] = default_value
        
        return params
    
    def simulate(self, simulation_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the plastic spread simulation.
        
        Args:
            simulation_config: Simulation configuration including intervention scenarios
            
        Returns:
            Dictionary containing simulation results
        """
        periods = self.parameters['periods']
        
        # Parse simulation configuration
        compare_scenarios = simulation_config.get('compare_scenarios', True)
        
        logger.info(f"Simulating plastic spread over {periods} years")
        
        if compare_scenarios:
            # Run multiple scenarios
            baseline_scenario = self._run_single_scenario('baseline')
            production_cap_scenario = self._run_single_scenario('production_cap')
            recycling_improvement_scenario = self._run_single_scenario('recycling_improvement')
            combined_intervention_scenario = self._run_single_scenario('combined_intervention')
            
            results = {
                'baseline_scenario': baseline_scenario,
                'production_cap_scenario': production_cap_scenario,
                'recycling_improvement_scenario': recycling_improvement_scenario,
                'combined_intervention_scenario': combined_intervention_scenario,
                'comparison': self._compare_scenarios({
                    'baseline': baseline_scenario,
                    'production_cap': production_cap_scenario,
                    'recycling_improvement': recycling_improvement_scenario,
                    'combined_intervention': combined_intervention_scenario
                })
            }
        else:
            # Run single scenario
            scenario_type = simulation_config.get('scenario_type', 'baseline')
            results = self._run_single_scenario(scenario_type)
        
        logger.info("Plastic spread simulation completed")
        return results
    
    def _run_single_scenario(self, scenario_type: str) -> Dict[str, Any]:
        """Run a single scenario simulation."""
        periods = self.parameters['periods']
        
        # Configure scenario-specific parameters
        scenario_params = self._configure_scenario(scenario_type)
        
        # Initialize time series
        results = {
            'periods': list(range(periods)),
            'annual_production_tonnes': np.zeros(periods),
            'total_plastic_accumulated_kg': np.zeros(periods),
            'earth_coverage_percent': np.zeros(periods),
            'ocean_coverage_percent': np.zeros(periods),
            'land_coverage_percent': np.zeros(periods),
            'cleanup_cost_billion_usd': np.zeros(periods),
            'environmental_damage_cost_billion_usd': np.zeros(periods),
            'recycling_rate': np.full(periods, scenario_params['initial_recycling_rate']),
            'gdp_impact_percent': np.zeros(periods),
            'scenario_type': scenario_type
        }
        
        # Run simulation year by year
        cumulative_plastic = 0
        current_production = self.parameters['annual_production_tonnes']
        
        for t in range(periods):
            # Apply production controls if enabled
            if scenario_params['production_cap_enabled'] and t >= scenario_params['production_cap_year']:
                max_production = self.parameters['annual_production_tonnes'] * scenario_params['production_cap_multiplier']
                current_production = min(current_production, max_production)
            else:
                current_production *= (1 + self.parameters['annual_growth_rate'])
            
            # Apply recycling improvements
            if scenario_params['recycling_improvement_enabled'] and t >= scenario_params['recycling_improvement_year']:
                improvement = min(
                    scenario_params['recycling_improvement_rate'],
                    scenario_params['target_recycling_rate'] - results['recycling_rate'][t-1] if t > 0 else 0
                )
                results['recycling_rate'][t] = results['recycling_rate'][t-1] + improvement if t > 0 else scenario_params['initial_recycling_rate']
            
            # Calculate net plastic production (after recycling)
            net_production = current_production * (1 - results['recycling_rate'][t])
            results['annual_production_tonnes'][t] = net_production
            
            # Accumulate plastic
            cumulative_plastic += net_production * 1000 * self.parameters['plastic_persistence_rate']
            results['total_plastic_accumulated_kg'][t] = cumulative_plastic
            
            # Calculate coverage using simple function
            simple_result = simulate_plastic_spread(
                annual_production_tonnes=net_production,
                annual_growth_rate=0,  # Growth already applied above
                coverage_density_kg_per_sq_km=self.parameters['coverage_density_kg_per_sq_km'],
                earth_surface_area_sq_km=self.parameters['earth_surface_area_sq_km'],
                ocean_area_sq_km=self.parameters['ocean_area_sq_km'],
                current_year=0  # Use accumulated plastic directly
            )
            
            # Override with our accumulated values
            total_coverage_area = cumulative_plastic / self.parameters['coverage_density_kg_per_sq_km']
            results['earth_coverage_percent'][t] = min(
                (total_coverage_area / self.parameters['earth_surface_area_sq_km']) * 100, 100
            )
            results['ocean_coverage_percent'][t] = min(
                (total_coverage_area * self.parameters['ocean_allocation_rate'] / self.parameters['ocean_area_sq_km']) * 100, 100
            )
            results['land_coverage_percent'][t] = min(
                (total_coverage_area * (1 - self.parameters['ocean_allocation_rate']) / self.parameters['land_area_sq_km']) * 100, 100
            )
            
            # Economic impacts
            results['cleanup_cost_billion_usd'][t] = (cumulative_plastic / 1000) * self.parameters['cleanup_cost_per_tonne'] / 1e9
            
            damage_multiplier = 1 + (results['earth_coverage_percent'][t] / 10) ** 2
            results['environmental_damage_cost_billion_usd'][t] = results['cleanup_cost_billion_usd'][t] * damage_multiplier
            
            # GDP impact
            if results['earth_coverage_percent'][t] > self.parameters['gdp_impact_threshold']:
                excess_coverage = results['earth_coverage_percent'][t] - self.parameters['gdp_impact_threshold']
                results['gdp_impact_percent'][t] = excess_coverage * self.parameters['gdp_impact_sensitivity']
        
        # Convert numpy arrays to lists for JSON serialization
        for key, value in results.items():
            if isinstance(value, np.ndarray):
                results[key] = value.tolist()
        
        # Add summary statistics
        results['summary'] = self._calculate_summary(results)
        
        return results
    
    def _configure_scenario(self, scenario_type: str) -> Dict[str, Any]:
        """Configure parameters for different scenarios."""
        base_config = {
            'production_cap_enabled': False,
            'recycling_improvement_enabled': False,
            'production_cap_year': self.parameters['production_cap_year'],
            'production_cap_multiplier': self.parameters['production_cap_multiplier'],
            'recycling_improvement_year': self.parameters['recycling_improvement_year'],
            'initial_recycling_rate': self.parameters['initial_recycling_rate'],
            'target_recycling_rate': self.parameters['target_recycling_rate'],
            'recycling_improvement_rate': self.parameters['recycling_improvement_rate']
        }
        
        if scenario_type == 'production_cap':
            base_config.update({
                'production_cap_enabled': True
            })
        elif scenario_type == 'recycling_improvement':
            base_config.update({
                'recycling_improvement_enabled': True
            })
        elif scenario_type == 'combined_intervention':
            base_config.update({
                'production_cap_enabled': True,
                'recycling_improvement_enabled': True
            })
        
        return base_config
    
    def _calculate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate summary statistics for the simulation."""
        earth_coverage = np.array(results['earth_coverage_percent'])
        ocean_coverage = np.array(results['ocean_coverage_percent'])
        cleanup_costs = np.array(results['cleanup_cost_billion_usd'])
        damage_costs = np.array(results['environmental_damage_cost_billion_usd'])
        total_plastic = np.array(results['total_plastic_accumulated_kg'])
        gdp_impact = np.array(results['gdp_impact_percent'])
        
        # Find critical thresholds
        critical_coverage_year = None
        if np.any(earth_coverage >= 1.0):  # 1% coverage threshold
            critical_coverage_year = int(np.argmax(earth_coverage >= 1.0))
        
        ocean_saturation_year = None
        if np.any(ocean_coverage >= 10.0):  # 10% ocean coverage threshold
            ocean_saturation_year = int(np.argmax(ocean_coverage >= 10.0))
        
        return {
            'final_earth_coverage_percent': float(earth_coverage[-1]),
            'final_ocean_coverage_percent': float(ocean_coverage[-1]),
            'peak_earth_coverage_percent': float(np.max(earth_coverage)),
            'peak_ocean_coverage_percent': float(np.max(ocean_coverage)),
            'total_plastic_accumulated_tonnes': float(total_plastic[-1] / 1000),
            'final_cleanup_cost_billion_usd': float(cleanup_costs[-1]),
            'final_environmental_damage_cost_billion_usd': float(damage_costs[-1]),
            'total_economic_cost_billion_usd': float(cleanup_costs[-1] + damage_costs[-1]),
            'critical_coverage_year': critical_coverage_year,
            'ocean_saturation_year': ocean_saturation_year,
            'max_gdp_impact_percent': float(np.min(gdp_impact)),  # Most negative impact
            'final_recycling_rate': float(results['recycling_rate'][-1]),
            'scenario_type': results['scenario_type'],
            'years_to_1_percent_coverage': critical_coverage_year,
            'cumulative_production_reduction_percent': float(
                ((self.parameters['annual_production_tonnes'] * self.parameters['periods'] * 
                  ((1 + self.parameters['annual_growth_rate']) ** self.parameters['periods'] - 1) / 
                  self.parameters['annual_growth_rate']) - 
                 np.sum(results['annual_production_tonnes'])) /
                (self.parameters['annual_production_tonnes'] * self.parameters['periods']) * 100
            ) if results['scenario_type'] != 'baseline' else 0.0
        }
    
    def _compare_scenarios(self, scenarios: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Compare multiple scenarios."""
        baseline = scenarios['baseline']['summary']
        
        comparison = {
            'coverage_reduction': {},
            'cost_savings': {},
            'environmental_benefits': {},
            'key_insights': []
        }
        
        for scenario_name, scenario_data in scenarios.items():
            if scenario_name == 'baseline':
                continue
            
            summary = scenario_data['summary']
            
            comparison['coverage_reduction'][scenario_name] = {
                'earth_coverage_reduction_pp': baseline['final_earth_coverage_percent'] - summary['final_earth_coverage_percent'],
                'ocean_coverage_reduction_pp': baseline['final_ocean_coverage_percent'] - summary['final_ocean_coverage_percent'],
                'delayed_critical_coverage_years': (summary['critical_coverage_year'] or 999) - (baseline['critical_coverage_year'] or 999)
            }
            
            comparison['cost_savings'][scenario_name] = {
                'cleanup_cost_savings_billion': baseline['final_cleanup_cost_billion_usd'] - summary['final_cleanup_cost_billion_usd'],
                'environmental_damage_savings_billion': baseline['final_environmental_damage_cost_billion_usd'] - summary['final_environmental_damage_cost_billion_usd'],
                'total_savings_billion': baseline['total_economic_cost_billion_usd'] - summary['total_economic_cost_billion_usd']
            }
            
            comparison['environmental_benefits'][scenario_name] = {
                'plastic_reduction_tonnes': baseline['total_plastic_accumulated_tonnes'] - summary['total_plastic_accumulated_tonnes'],
                'gdp_impact_reduction_pp': baseline['max_gdp_impact_percent'] - summary['max_gdp_impact_percent']
            }
        
        # Generate insights
        best_scenario = max(scenarios.keys(), 
                           key=lambda x: scenarios[x]['summary']['total_economic_cost_billion_usd'] 
                           if x != 'baseline' else float('inf'))
        
        comparison['key_insights'] = [
            f"Best scenario: {best_scenario} saves ${comparison['cost_savings'].get(best_scenario, {}).get('total_savings_billion', 0):.1f}B",
            f"Combined interventions reduce final coverage by {comparison['coverage_reduction'].get('combined_intervention', {}).get('earth_coverage_reduction_pp', 0):.2f}pp",
            f"Production caps alone delay critical coverage by {comparison['coverage_reduction'].get('production_cap', {}).get('delayed_critical_coverage_years', 0)} years",
            f"Recycling improvements reduce plastic accumulation by {comparison['environmental_benefits'].get('recycling_improvement', {}).get('plastic_reduction_tonnes', 0)/1e9:.1f}B tonnes"
        ]
        
        return comparison 