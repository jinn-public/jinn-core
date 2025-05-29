"""
Bitcoin Price Projection Model

Economic model for projecting Bitcoin price trajectories under different
adoption scenarios, regulatory environments, and market conditions.
"""

import numpy as np
import logging
import math
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class BTCProjectionScenario:
    """Configuration for a Bitcoin price projection scenario."""
    name: str                    # Scenario name (e.g., "baseline", "institutional_adoption")
    annual_growth_rate: float    # Annual growth rate (e.g., 0.4 for 40%)
    description: str             # Scenario description
    volatility_factor: float = 0.2  # Price volatility multiplier
    adoption_curve: str = "linear"   # "linear", "exponential", "s_curve"
    regulatory_impact: float = 1.0   # Regulatory impact multiplier
    institutional_factor: float = 1.0  # Institutional adoption multiplier


def simulate_btc_price_projection(current_price_usd: float, target_price_usd: float,
                                annual_growth_rate: float, max_years: int = 30) -> Dict[str, Any]:
    """
    Simple, interpretable function to project Bitcoin price growth.
    
    Args:
        current_price_usd: Current Bitcoin price in USD
        target_price_usd: Target Bitcoin price in USD
        annual_growth_rate: Annual growth rate (e.g., 0.4 for 40%)
        max_years: Maximum years to project
        
    Returns:
        Dict containing:
        - years_to_target: Years needed to reach target price
        - final_price: Price after max_years
        - total_return_multiple: Total return multiple
        - annual_return_needed: Annual return needed for target
        - price_trajectory: Year-by-year price progression
        - feasibility_assessment: Whether target is achievable
    """
    # Calculate years to target using compound growth formula
    # target = current * (1 + growth_rate)^years
    # years = log(target/current) / log(1 + growth_rate)
    
    if annual_growth_rate <= 0:
        raise ValueError("Annual growth rate must be positive")
    
    if target_price_usd <= current_price_usd:
        raise ValueError("Target price must be higher than current price")
    
    # Calculate years to target
    growth_multiplier = target_price_usd / current_price_usd
    years_to_target = math.log(growth_multiplier) / math.log(1 + annual_growth_rate)
    
    # Calculate final price after max_years
    final_price = current_price_usd * ((1 + annual_growth_rate) ** max_years)
    
    # Calculate total return multiple
    total_return_multiple = final_price / current_price_usd
    
    # Calculate annual return needed to reach target in max_years
    annual_return_needed = (target_price_usd / current_price_usd) ** (1 / max_years) - 1
    
    # Generate price trajectory
    price_trajectory = []
    for year in range(max_years + 1):
        price = current_price_usd * ((1 + annual_growth_rate) ** year)
        price_trajectory.append({
            'year': year,
            'price': price,
            'return_multiple': price / current_price_usd
        })
    
    # Feasibility assessment
    feasibility = "Achievable" if years_to_target <= max_years else "Requires longer timeframe"
    if years_to_target <= 10:
        feasibility = "Highly achievable"
    elif years_to_target <= 20:
        feasibility = "Achievable with sustained growth"
    elif years_to_target <= max_years:
        feasibility = "Challenging but possible"
    else:
        feasibility = "Unlikely within timeframe"
    
    return {
        'years_to_target': years_to_target,
        'final_price': final_price,
        'total_return_multiple': total_return_multiple,
        'annual_return_needed': annual_return_needed,
        'price_trajectory': price_trajectory,
        'feasibility_assessment': feasibility,
        'target_achieved_in_timeframe': years_to_target <= max_years
    }


class BTCPriceProjectionModel:
    """
    Bitcoin Price Projection Model
    
    Projects Bitcoin price trajectories under different scenarios including:
    - Baseline adoption growth
    - Institutional adoption acceleration
    - Fiat currency crisis scenarios
    - Regulatory clarity impacts
    - Combined shock scenarios
    - Market volatility and adoption curves
    """
    
    def __init__(self, parameters: Dict[str, Any]):
        """
        Initialize the Bitcoin Price Projection Model.
        
        Args:
            parameters: Model calibration parameters
        """
        self.parameters = self._validate_parameters(parameters)
        self.scenarios = self._define_scenarios()
        logger.info("Bitcoin Price Projection Model initialized")
    
    def _validate_parameters(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and set default parameters."""
        defaults = {
            # Price parameters
            'current_price_usd': 70000.0,        # Current BTC price
            'target_price_usd': 1000000.0,       # Target BTC price ($1M)
            'max_years': 30,                     # Maximum projection years
            
            # Market parameters
            'baseline_volatility': 0.6,          # 60% annual volatility
            'market_maturity_factor': 0.95,      # Market maturation rate
            'liquidity_improvement': 0.02,       # Annual liquidity improvement
            
            # Adoption parameters
            'current_adoption_rate': 0.05,       # 5% global adoption
            'max_adoption_rate': 0.25,           # 25% maximum adoption
            'adoption_acceleration': 0.1,        # Adoption acceleration factor
            
            # Economic factors
            'inflation_hedge_premium': 0.05,     # 5% inflation hedge premium
            'store_of_value_multiplier': 1.2,    # Store of value premium
            'network_effect_exponent': 1.5,      # Network effect strength
            
            # Institutional factors
            'institutional_allocation': 0.01,    # 1% institutional allocation
            'sovereign_adoption_impact': 2.0,    # Sovereign adoption multiplier
            'etf_impact_factor': 1.3,           # ETF approval impact
            
            # Regulatory factors
            'regulatory_clarity_bonus': 0.1,     # 10% clarity bonus
            'regulatory_uncertainty_penalty': -0.15,  # -15% uncertainty penalty
            
            # Technical factors
            'halving_cycle_impact': 0.2,         # 20% halving impact
            'scaling_solution_impact': 0.05,     # 5% scaling improvement
            'energy_efficiency_improvement': 0.03, # 3% annual efficiency gain
            
            # Model parameters
            'simulation_runs': 1000,             # Monte Carlo runs
            'confidence_interval': 0.95,        # 95% confidence interval
        }
        
        # Merge with provided parameters
        for key, default_value in defaults.items():
            if key not in params:
                params[key] = default_value
        
        return params
    
    def _define_scenarios(self) -> Dict[str, BTCProjectionScenario]:
        """Define the different Bitcoin price projection scenarios."""
        scenarios = {
            'baseline': BTCProjectionScenario(
                name="baseline",
                annual_growth_rate=0.40,  # 40% annual growth
                description="Steady adoption with moderate institutional interest",
                volatility_factor=1.0,
                adoption_curve="linear",
                regulatory_impact=1.0,
                institutional_factor=1.0
            ),
            'institutional_adoption': BTCProjectionScenario(
                name="institutional_adoption",
                annual_growth_rate=0.55,  # 55% annual growth
                description="Accelerated institutional adoption and ETF approvals",
                volatility_factor=0.8,  # Lower volatility with institutions
                adoption_curve="exponential",
                regulatory_impact=1.1,
                institutional_factor=2.0
            ),
            'fiat_crisis': BTCProjectionScenario(
                name="fiat_crisis",
                annual_growth_rate=0.65,  # 65% annual growth
                description="Fiat currency crisis drives flight to Bitcoin",
                volatility_factor=1.5,  # Higher volatility during crisis
                adoption_curve="exponential",
                regulatory_impact=0.9,  # Some regulatory pushback
                institutional_factor=1.5
            ),
            'regulatory_clarity': BTCProjectionScenario(
                name="regulatory_clarity",
                annual_growth_rate=0.50,  # 50% annual growth
                description="Clear regulatory framework enables mainstream adoption",
                volatility_factor=0.7,  # Lower volatility with clarity
                adoption_curve="s_curve",
                regulatory_impact=1.3,
                institutional_factor=1.4
            ),
            'combined_shock': BTCProjectionScenario(
                name="combined_shock",
                annual_growth_rate=0.75,  # 75% annual growth
                description="Perfect storm: institutional adoption + fiat crisis + regulatory clarity",
                volatility_factor=1.2,  # Moderate volatility
                adoption_curve="exponential",
                regulatory_impact=1.2,
                institutional_factor=2.5
            )
        }
        
        return scenarios
    
    def simulate(self, simulation_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the Bitcoin price projection simulation.
        
        Args:
            simulation_config: Simulation configuration
            
        Returns:
            Dictionary containing simulation results for all scenarios
        """
        # Extract configuration
        current_price = simulation_config.get('current_price_usd', self.parameters['current_price_usd'])
        target_price = simulation_config.get('target_price_usd', self.parameters['target_price_usd'])
        max_years = simulation_config.get('max_years', self.parameters['max_years'])
        scenarios_to_run = simulation_config.get('scenarios', list(self.scenarios.keys()))
        
        logger.info(f"Simulating Bitcoin price projection: ${current_price:,.0f} → ${target_price:,.0f}")
        
        results = {
            'parameters': {
                'current_price_usd': current_price,
                'target_price_usd': target_price,
                'max_years': max_years,
                'scenarios_analyzed': scenarios_to_run
            },
            'scenarios': {},
            'comparison': {},
            'summary': {}
        }
        
        # Run each scenario
        for scenario_name in scenarios_to_run:
            if scenario_name not in self.scenarios:
                logger.warning(f"Unknown scenario: {scenario_name}")
                continue
            
            scenario = self.scenarios[scenario_name]
            scenario_results = self._simulate_scenario(scenario, current_price, target_price, max_years)
            results['scenarios'][scenario_name] = scenario_results
        
        # Generate comparison and summary
        results['comparison'] = self._generate_comparison(results['scenarios'])
        results['summary'] = self._generate_summary(results['scenarios'], current_price, target_price)
        
        logger.info("Bitcoin price projection simulation completed")
        return results
    
    def _simulate_scenario(self, scenario: BTCProjectionScenario, current_price: float,
                          target_price: float, max_years: int) -> Dict[str, Any]:
        """Simulate a single scenario with enhanced modeling."""
        
        # Base projection using simple function
        base_result = simulate_btc_price_projection(
            current_price, target_price, scenario.annual_growth_rate, max_years
        )
        
        # Enhanced modeling with scenario-specific factors
        enhanced_trajectory = []
        volatility_trajectory = []
        adoption_trajectory = []
        
        for year in range(max_years + 1):
            # Base price from compound growth
            base_price = current_price * ((1 + scenario.annual_growth_rate) ** year)
            
            # Apply scenario-specific modifications
            
            # Adoption curve effects
            adoption_factor = self._calculate_adoption_factor(year, max_years, scenario.adoption_curve)
            
            # Institutional impact (grows over time)
            institutional_impact = 1 + (scenario.institutional_factor - 1) * (year / max_years)
            
            # Regulatory impact (stabilizes over time)
            regulatory_impact = scenario.regulatory_impact
            
            # Volatility decreases over time as market matures
            volatility = scenario.volatility_factor * self.parameters['baseline_volatility'] * (1 - year / (max_years * 2))
            volatility = max(0.1, volatility)  # Minimum 10% volatility
            
            # Network effects (accelerate with adoption)
            network_effect = adoption_factor ** self.parameters['network_effect_exponent']
            
            # Calculate enhanced price
            enhanced_price = (base_price * adoption_factor * institutional_impact * 
                            regulatory_impact * network_effect)
            
            enhanced_trajectory.append({
                'year': year,
                'price': enhanced_price,
                'base_price': base_price,
                'adoption_factor': adoption_factor,
                'institutional_impact': institutional_impact,
                'regulatory_impact': regulatory_impact,
                'network_effect': network_effect,
                'return_multiple': enhanced_price / current_price
            })
            
            volatility_trajectory.append(volatility)
            adoption_trajectory.append(adoption_factor)
        
        # Calculate enhanced metrics
        final_enhanced_price = enhanced_trajectory[-1]['price']
        enhanced_return_multiple = final_enhanced_price / current_price
        
        # Find years to target with enhanced model
        enhanced_years_to_target = None
        for point in enhanced_trajectory:
            if point['price'] >= target_price:
                enhanced_years_to_target = point['year']
                break
        
        if enhanced_years_to_target is None:
            enhanced_years_to_target = float('inf')
        
        # Risk assessment
        risk_factors = self._assess_risk_factors(scenario, enhanced_years_to_target, max_years)
        
        return {
            'scenario_name': scenario.name,
            'description': scenario.description,
            'annual_growth_rate': scenario.annual_growth_rate,
            'base_projection': base_result,
            'enhanced_projection': {
                'years_to_target': enhanced_years_to_target,
                'final_price': final_enhanced_price,
                'total_return_multiple': enhanced_return_multiple,
                'target_achieved': enhanced_years_to_target <= max_years,
                'trajectory': enhanced_trajectory,
                'volatility_trajectory': volatility_trajectory,
                'adoption_trajectory': adoption_trajectory
            },
            'risk_assessment': risk_factors,
            'key_assumptions': {
                'volatility_factor': scenario.volatility_factor,
                'adoption_curve': scenario.adoption_curve,
                'regulatory_impact': scenario.regulatory_impact,
                'institutional_factor': scenario.institutional_factor
            }
        }
    
    def _calculate_adoption_factor(self, year: int, max_years: int, curve_type: str) -> float:
        """Calculate adoption factor based on curve type."""
        progress = year / max_years
        
        if curve_type == "linear":
            return 1 + progress * 0.5  # Linear growth to 1.5x
        elif curve_type == "exponential":
            return 1 + (np.exp(progress * 2) - 1) / (np.exp(2) - 1)  # Exponential curve
        elif curve_type == "s_curve":
            # Sigmoid curve: slow start, rapid middle, slow end
            x = (progress - 0.5) * 10  # Scale to -5 to +5
            sigmoid = 1 / (1 + np.exp(-x))
            return 1 + sigmoid * 0.8  # S-curve growth to 1.8x
        else:
            return 1.0
    
    def _assess_risk_factors(self, scenario: BTCProjectionScenario, years_to_target: float,
                           max_years: int) -> Dict[str, Any]:
        """Assess risk factors for the scenario."""
        
        # Time risk
        if years_to_target <= 5:
            time_risk = "Low"
        elif years_to_target <= 15:
            time_risk = "Medium"
        elif years_to_target <= max_years:
            time_risk = "High"
        else:
            time_risk = "Very High"
        
        # Volatility risk
        if scenario.volatility_factor <= 0.7:
            volatility_risk = "Low"
        elif scenario.volatility_factor <= 1.2:
            volatility_risk = "Medium"
        else:
            volatility_risk = "High"
        
        # Regulatory risk
        if scenario.regulatory_impact >= 1.2:
            regulatory_risk = "Low"
        elif scenario.regulatory_impact >= 0.9:
            regulatory_risk = "Medium"
        else:
            regulatory_risk = "High"
        
        # Overall risk assessment
        risk_scores = {
            "Low": 1, "Medium": 2, "High": 3, "Very High": 4
        }
        
        avg_risk_score = (risk_scores[time_risk] + risk_scores[volatility_risk] + 
                         risk_scores[regulatory_risk]) / 3
        
        if avg_risk_score <= 1.5:
            overall_risk = "Low"
        elif avg_risk_score <= 2.5:
            overall_risk = "Medium"
        else:
            overall_risk = "High"
        
        return {
            'time_risk': time_risk,
            'volatility_risk': volatility_risk,
            'regulatory_risk': regulatory_risk,
            'overall_risk': overall_risk,
            'risk_score': avg_risk_score,
            'key_risks': self._identify_key_risks(scenario)
        }
    
    def _identify_key_risks(self, scenario: BTCProjectionScenario) -> List[str]:
        """Identify key risks for the scenario."""
        risks = []
        
        if scenario.annual_growth_rate > 0.6:
            risks.append("Unsustainable growth rate assumptions")
        
        if scenario.volatility_factor > 1.3:
            risks.append("High market volatility")
        
        if scenario.regulatory_impact < 1.0:
            risks.append("Regulatory headwinds")
        
        if scenario.institutional_factor > 2.0:
            risks.append("Over-reliance on institutional adoption")
        
        if scenario.adoption_curve == "exponential":
            risks.append("Exponential adoption may not be sustainable")
        
        return risks
    
    def _generate_comparison(self, scenarios: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comparison between scenarios."""
        if not scenarios:
            return {}
        
        comparison = {
            'fastest_to_target': None,
            'highest_final_price': None,
            'lowest_risk': None,
            'most_realistic': None,
            'scenario_rankings': []
        }
        
        # Find fastest to target
        fastest_time = float('inf')
        for name, scenario in scenarios.items():
            years = scenario['enhanced_projection']['years_to_target']
            if years < fastest_time:
                fastest_time = years
                comparison['fastest_to_target'] = {
                    'scenario': name,
                    'years': years
                }
        
        # Find highest final price
        highest_price = 0
        for name, scenario in scenarios.items():
            price = scenario['enhanced_projection']['final_price']
            if price > highest_price:
                highest_price = price
                comparison['highest_final_price'] = {
                    'scenario': name,
                    'price': price
                }
        
        # Find lowest risk
        lowest_risk_score = float('inf')
        for name, scenario in scenarios.items():
            risk_score = scenario['risk_assessment']['risk_score']
            if risk_score < lowest_risk_score:
                lowest_risk_score = risk_score
                comparison['lowest_risk'] = {
                    'scenario': name,
                    'risk_score': risk_score,
                    'risk_level': scenario['risk_assessment']['overall_risk']
                }
        
        # Determine most realistic (balance of achievability and risk)
        best_score = 0
        for name, scenario in scenarios.items():
            years = scenario['enhanced_projection']['years_to_target']
            risk_score = scenario['risk_assessment']['risk_score']
            
            # Score based on achievability (lower years better) and risk (lower risk better)
            achievability_score = max(0, 10 - years / 3)  # 10 points for immediate, 0 for 30+ years
            risk_score_normalized = max(0, 5 - risk_score)  # 5 points for low risk, 0 for very high
            
            total_score = achievability_score + risk_score_normalized
            
            if total_score > best_score:
                best_score = total_score
                comparison['most_realistic'] = {
                    'scenario': name,
                    'score': total_score,
                    'years_to_target': years,
                    'risk_level': scenario['risk_assessment']['overall_risk']
                }
        
        # Rank scenarios
        scenario_scores = []
        for name, scenario in scenarios.items():
            years = scenario['enhanced_projection']['years_to_target']
            risk_score = scenario['risk_assessment']['risk_score']
            final_price = scenario['enhanced_projection']['final_price']
            
            achievability_score = max(0, 10 - years / 3)
            risk_score_normalized = max(0, 5 - risk_score)
            price_score = min(5, final_price / 1000000)  # Up to 5 points for reaching $1M+
            
            total_score = achievability_score + risk_score_normalized + price_score
            
            scenario_scores.append({
                'scenario': name,
                'total_score': total_score,
                'years_to_target': years,
                'final_price': final_price,
                'risk_level': scenario['risk_assessment']['overall_risk']
            })
        
        # Sort by total score
        scenario_scores.sort(key=lambda x: x['total_score'], reverse=True)
        comparison['scenario_rankings'] = scenario_scores
        
        return comparison
    
    def _generate_summary(self, scenarios: Dict[str, Any], current_price: float,
                         target_price: float) -> Dict[str, Any]:
        """Generate overall summary of projections."""
        if not scenarios:
            return {}
        
        # Calculate statistics across scenarios
        years_to_target = []
        final_prices = []
        return_multiples = []
        achievable_scenarios = 0
        
        for scenario in scenarios.values():
            years = scenario['enhanced_projection']['years_to_target']
            if years != float('inf'):
                years_to_target.append(years)
            
            final_prices.append(scenario['enhanced_projection']['final_price'])
            return_multiples.append(scenario['enhanced_projection']['total_return_multiple'])
            
            if scenario['enhanced_projection']['target_achieved']:
                achievable_scenarios += 1
        
        # Calculate statistics
        avg_years = np.mean(years_to_target) if years_to_target else float('inf')
        min_years = np.min(years_to_target) if years_to_target else float('inf')
        max_years = np.max(years_to_target) if years_to_target else float('inf')
        
        avg_final_price = np.mean(final_prices)
        min_final_price = np.min(final_prices)
        max_final_price = np.max(final_prices)
        
        avg_return_multiple = np.mean(return_multiples)
        
        # Success probability
        success_probability = achievable_scenarios / len(scenarios) if scenarios else 0
        
        return {
            'target_analysis': {
                'current_price': current_price,
                'target_price': target_price,
                'target_multiple': target_price / current_price,
                'scenarios_analyzed': len(scenarios),
                'scenarios_achieving_target': achievable_scenarios,
                'success_probability': success_probability
            },
            'time_to_target': {
                'average_years': avg_years,
                'fastest_scenario_years': min_years,
                'slowest_scenario_years': max_years,
                'range_years': max_years - min_years if years_to_target else 0
            },
            'price_projections': {
                'average_final_price': avg_final_price,
                'lowest_final_price': min_final_price,
                'highest_final_price': max_final_price,
                'average_return_multiple': avg_return_multiple
            },
            'investment_insights': {
                'most_likely_outcome': f"${avg_final_price:,.0f} in 30 years",
                'best_case_scenario': f"${max_final_price:,.0f} in 30 years",
                'target_achievability': "High" if success_probability > 0.7 else "Medium" if success_probability > 0.3 else "Low",
                'recommended_strategy': self._get_investment_recommendation(success_probability, avg_years)
            }
        }
    
    def _get_investment_recommendation(self, success_probability: float, avg_years: float) -> str:
        """Generate investment recommendation based on analysis."""
        if success_probability > 0.8 and avg_years < 15:
            return "Strong buy - High probability of reaching target within reasonable timeframe"
        elif success_probability > 0.6 and avg_years < 20:
            return "Buy - Good probability of significant returns"
        elif success_probability > 0.4:
            return "Hold/DCA - Moderate probability, consider dollar-cost averaging"
        elif success_probability > 0.2:
            return "Cautious - Low probability, high risk investment"
        else:
            return "Avoid - Very low probability of reaching target" 