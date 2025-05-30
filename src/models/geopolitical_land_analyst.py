"""
Geopolitical Land Price Analyst Model

Economic model for simulating global land price trends over 10-15 years based on:
- Urbanization and demographic shifts 🌆
- Climate change impacts ⚠️  
- Infrastructure development
- Water and food supply security
- Technology hub emergence
- Remote work adoption
- Economic and political risk factors
- Regional growth patterns 🧊

Identifies high-growth regions (🌆), high-risk zones (⚠️), and declining regions (🧊).
"""

import numpy as np
import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class RegionType(Enum):
    """Types of regions based on development and growth characteristics."""
    MATURE_CITIES = "mature_cities"           # Established, well-funded cities
    UPWARDLY_MOBILE = "upwardly_mobile"       # Fast-growing, lower-income regions  
    INNOVATION_FRONTRUNNERS = "innovation_frontrunners"  # Wealthy, rapid economic growth
    DECLINING_INDUSTRIAL = "declining_industrial"        # Former industrial centers
    EMERGING_MARKETS = "emerging_markets"                # Developing economies
    CLIMATE_VULNERABLE = "climate_vulnerable"           # High climate risk zones


class ClimatePressure(Enum):
    """Climate change pressure levels."""
    LOW = 1.0      # Minimal climate impacts
    MODERATE = 1.3  # Some adaptation needed
    HIGH = 1.8     # Significant adaptation costs
    EXTREME = 2.5  # Major displacement/abandonment risk


@dataclass
class RegionProfile:
    """Configuration for a regional land market analysis."""
    name: str
    region_type: RegionType
    initial_land_price_index: float = 100.0  # Base index (100 = baseline)
    
    # Economic fundamentals
    gdp_growth_rate: float = 0.03             # Annual GDP growth rate
    population_growth_rate: float = 0.01      # Annual population growth
    urbanization_rate: float = 0.02           # Annual urbanization increase
    tech_hub_score: float = 50.0              # Technology ecosystem score (0-100)
    
    # Infrastructure factors
    infrastructure_quality: float = 70.0      # Current infrastructure quality (0-100)
    infrastructure_investment_rate: float = 0.05  # Annual infrastructure investment as % GDP
    transportation_connectivity: float = 60.0  # Transportation network quality (0-100)
    
    # Climate and environmental
    climate_pressure: ClimatePressure = ClimatePressure.MODERATE
    water_security_index: float = 70.0        # Water availability/security (0-100)
    food_security_index: float = 75.0         # Food production/access (0-100)
    climate_adaptation_investment: float = 0.02  # Annual climate adaptation spending as % GDP
    
    # Social and political
    political_stability_index: float = 70.0   # Political stability (0-100)
    regulatory_environment: float = 60.0      # Ease of doing business (0-100)
    social_inequality_index: float = 40.0     # Inequality level (0-100, higher = more unequal)
    
    # Technology and remote work
    remote_work_adoption: float = 30.0        # Remote work adoption rate (0-100%)
    digital_infrastructure: float = 65.0     # Digital connectivity quality (0-100)
    innovation_investment: float = 0.03       # R&D investment as % GDP
    
    # Land supply constraints
    developable_land_ratio: float = 0.7       # Fraction of land available for development
    zoning_flexibility: float = 50.0          # Zoning policy flexibility (0-100)
    land_use_efficiency: float = 60.0         # Current land use efficiency (0-100)


@dataclass 
class GeopoliticalShock:
    """Configuration for geopolitical/economic shocks affecting land prices."""
    trade_war_intensity: float = 0.0          # Trade disruption intensity (0-1)
    energy_crisis_severity: float = 0.0       # Energy supply disruption (0-1)
    migration_pressure: float = 0.0           # Migration inflow pressure (0-1)
    financial_crisis_risk: float = 0.0        # Financial market stress (0-1)
    technology_disruption: float = 0.0        # Tech industry disruption (0-1)
    climate_disaster_frequency: float = 0.0   # Extreme weather events (0-1)
    start_period: int = 0                     # When shocks begin


def simulate_land_price_trends(region: RegionProfile, shock: GeopoliticalShock = None, 
                             years: int = 15) -> Dict[str, Any]:
    """
    Simple, interpretable function to simulate land price trends for a region.
    
    Args:
        region: Regional characteristics and parameters
        shock: Optional geopolitical/economic shocks
        years: Number of years to simulate
        
    Returns:
        Dict containing:
        - final_price_index: Land price index at end of period
        - annual_growth_rate: Average annual growth rate
        - price_volatility: Price volatility over period
        - region_classification: High-growth (🌆), high-risk (⚠️), or declining (🧊)
        - peak_price_year: Year of peak prices
        - growth_drivers: Main factors driving price changes
        - risk_factors: Key risk factors identified
    """
    if shock is None:
        shock = GeopoliticalShock()
    
    # Base growth rate calculation
    base_growth = (region.gdp_growth_rate + region.population_growth_rate + 
                  region.urbanization_rate) * 0.8  # Land prices correlate with fundamentals
    
    # Technology hub premium
    tech_premium = (region.tech_hub_score / 100) * 0.03
    
    # Infrastructure boost
    infrastructure_boost = (region.infrastructure_quality / 100) * 0.02
    
    # Climate adaptation costs
    climate_cost = -region.climate_pressure.value * 0.01
    
    # Remote work impact (reduces demand for expensive urban cores)
    remote_work_discount = -(region.remote_work_adoption / 100) * 0.015
    
    # Political risk discount
    political_discount = -(100 - region.political_stability_index) / 100 * 0.02
    
    # Supply constraints premium
    supply_constraint_premium = (1 - region.developable_land_ratio) * 0.025
    
    # Calculate total growth rate
    total_growth = (base_growth + tech_premium + infrastructure_boost + 
                   climate_cost + remote_work_discount + political_discount + 
                   supply_constraint_premium)
    
    # Apply shocks
    shock_impact = -(shock.trade_war_intensity + shock.energy_crisis_severity +
                    shock.financial_crisis_risk + shock.climate_disaster_frequency) * 0.01
    total_growth += shock_impact
    
    # Simulate price evolution with some volatility
    np.random.seed(42)  # For reproducible results
    annual_volatility = 0.1  # 10% annual volatility
    price_series = []
    current_price = region.initial_land_price_index
    
    for year in range(years):
        # Add random volatility
        yearly_shock = np.random.normal(0, annual_volatility)
        yearly_growth = total_growth + yearly_shock
        
        # Apply growth
        current_price *= (1 + yearly_growth)
        price_series.append(current_price)
    
    final_price_index = price_series[-1]
    annual_growth_rate = (final_price_index / region.initial_land_price_index) ** (1/years) - 1
    price_volatility = np.std(np.diff(np.log(price_series)))
    peak_price_year = np.argmax(price_series)
    
    # Classify region
    if annual_growth_rate > 0.05:
        classification = "🌆 High-Growth"
    elif annual_growth_rate < -0.01 or price_volatility > 0.15:
        classification = "⚠️ High-Risk" if price_volatility > 0.15 else "🧊 Declining"
    else:
        classification = "📈 Stable Growth"
    
    # Identify growth drivers
    growth_drivers = []
    if region.tech_hub_score > 75:
        growth_drivers.append("Technology ecosystem")
    if region.urbanization_rate > 0.03:
        growth_drivers.append("Rapid urbanization")
    if region.infrastructure_investment_rate > 0.07:
        growth_drivers.append("Infrastructure development")
    if region.population_growth_rate > 0.02:
        growth_drivers.append("Population growth")
    
    # Identify risk factors
    risk_factors = []
    if region.climate_pressure in [ClimatePressure.HIGH, ClimatePressure.EXTREME]:
        risk_factors.append("Climate vulnerability")
    if region.political_stability_index < 50:
        risk_factors.append("Political instability")
    if region.water_security_index < 40:
        risk_factors.append("Water stress")
    if shock.financial_crisis_risk > 0.3:
        risk_factors.append("Financial market stress")
    
    return {
        'final_price_index': final_price_index,
        'annual_growth_rate': annual_growth_rate * 100,  # Convert to percentage
        'price_volatility': price_volatility,
        'region_classification': classification,
        'peak_price_year': peak_price_year,
        'growth_drivers': growth_drivers,
        'risk_factors': risk_factors,
        'price_series': price_series
    }


class GeopoliticalLandAnalyst:
    """
    Geopolitical Land Price Analyst Model
    
    Simulates global land price trends over 10-15 years considering:
    - Economic fundamentals and demographic trends
    - Climate change impacts and adaptation costs
    - Technology sector development and remote work
    - Infrastructure investment and connectivity
    - Political stability and regulatory environment
    - Resource security (water, food, energy)
    - Geopolitical shocks and market disruptions
    """
    
    def __init__(self, parameters: Dict[str, Any]):
        """
        Initialize the Geopolitical Land Analyst Model.
        
        Args:
            parameters: Model calibration parameters
        """
        self.parameters = self._validate_parameters(parameters)
        logger.info("Geopolitical Land Analyst Model initialized")
    
    def _validate_parameters(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and set default parameters."""
        defaults = {
            # Global economic parameters
            'global_gdp_growth': 0.032,           # 3.2% global GDP growth baseline
            'global_population_growth': 0.009,    # 0.9% global population growth
            'global_urbanization_rate': 0.018,    # 1.8% annual urbanization
            'global_inflation_rate': 0.025,       # 2.5% baseline inflation
            
            # Technology trends
            'ai_productivity_boost': 0.015,       # 1.5% annual productivity from AI
            'remote_work_growth_rate': 0.05,     # 5% annual remote work adoption
            'digital_transformation_rate': 0.08,  # 8% annual digital upgrade
            'green_tech_investment_growth': 0.12, # 12% annual green tech investment growth
            
            # Climate change parameters
            'global_temperature_rise_annual': 0.02,  # 0.02°C annual temperature rise
            'climate_adaptation_cost_growth': 0.08,  # 8% annual adaptation cost increase
            'extreme_weather_frequency_growth': 0.04, # 4% annual increase in extreme events
            'sea_level_rise_annual': 0.003,         # 3mm annual sea level rise
            
            # Infrastructure parameters
            'global_infrastructure_deficit': 0.15,   # 15% infrastructure investment gap
            'infrastructure_productivity_multiplier': 1.3, # Infrastructure ROI multiplier
            'smart_city_adoption_rate': 0.06,       # 6% annual smart city feature adoption
            'transportation_electrification_rate': 0.15, # 15% annual EV adoption
            
            # Financial and regulatory
            'interest_rate_baseline': 0.04,         # 4% baseline interest rates
            'capital_mobility_index': 0.8,          # Global capital mobility (0-1)
            'regulatory_convergence_rate': 0.02,    # 2% annual regulatory harmonization
            'financial_crisis_probability': 0.15,   # 15% annual crisis probability
            
            # Resource security
            'water_stress_growth_rate': 0.03,       # 3% annual water stress increase
            'food_security_pressure': 0.02,         # 2% annual food security pressure
            'energy_transition_rate': 0.08,         # 8% annual renewable energy growth
            'resource_price_volatility': 0.2,       # 20% annual resource price volatility
            
            # Social and demographic
            'inequality_growth_rate': 0.01,         # 1% annual inequality increase
            'migration_pressure_growth': 0.05,      # 5% annual migration pressure increase
            'aging_population_effect': 0.008,       # 0.8% annual aging impact
            'education_improvement_rate': 0.03,     # 3% annual education improvement
            
            # Model parameters
            'simulation_years': 15,                 # Default simulation period
            'price_momentum_factor': 0.1,           # Price momentum coefficient
            'volatility_clustering_factor': 0.3,    # Volatility clustering coefficient
            'regional_correlation_factor': 0.4,     # Inter-regional correlation
        }
        
        # Merge with provided parameters
        for key, default_value in defaults.items():
            if key not in params:
                params[key] = default_value
        
        return params
    
    def simulate(self, simulation_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the geopolitical land price analysis simulation.
        
        Args:
            simulation_config: Simulation configuration including regions and scenarios
            
        Returns:
            Dictionary containing comprehensive simulation results
        """
        years = simulation_config.get('years', self.parameters['simulation_years'])
        
        # Parse regions configuration
        regions_config = simulation_config.get('regions', [])
        if not regions_config:
            # Use default global regions if none specified
            regions_config = self._get_default_regions()
        
        # Parse shock scenarios
        shock_config = simulation_config.get('shocks', {})
        shock = GeopoliticalShock(
            trade_war_intensity=shock_config.get('trade_war_intensity', 0.0),
            energy_crisis_severity=shock_config.get('energy_crisis_severity', 0.0),
            migration_pressure=shock_config.get('migration_pressure', 0.0),
            financial_crisis_risk=shock_config.get('financial_crisis_risk', 0.0),
            technology_disruption=shock_config.get('technology_disruption', 0.0),
            climate_disaster_frequency=shock_config.get('climate_disaster_frequency', 0.0),
            start_period=shock_config.get('start_period', 0)
        )
        
        logger.info(f"Simulating land price trends for {len(regions_config)} regions over {years} years")
        
        # Initialize results structure
        results = {
            'years': list(range(years)),
            'regions': {},
            'global_trends': {
                'average_price_index': [],
                'price_volatility': [],
                'high_growth_regions': [],
                'high_risk_regions': [],
                'declining_regions': []
            },
            'market_dynamics': {
                'technology_impact': [],
                'climate_adaptation_costs': [],
                'infrastructure_investment': [],
                'migration_flows': [],
                'political_risk_index': []
            }
        }
        
        # Simulate each region
        region_results = {}
        for region_config in regions_config:
            region = self._create_region_profile(region_config)
            regional_analysis = self._simulate_regional_trends(region, shock, years)
            region_results[region.name] = regional_analysis
            results['regions'][region.name] = regional_analysis
        
        # Calculate global trends and market dynamics
        self._calculate_global_trends(results, region_results, years)
        self._calculate_market_dynamics(results, years, shock)
        
        # Generate summary and classifications
        results['summary'] = self._generate_summary(region_results, years)
        results['regional_rankings'] = self._rank_regions(region_results)
        results['investment_recommendations'] = self._generate_investment_recommendations(region_results)
        
        logger.info("Geopolitical land price analysis completed")
        return results
    
    def _get_default_regions(self) -> List[Dict[str, Any]]:
        """Get default global regions for analysis."""
        return [
            {
                'name': 'North American Tech Hubs',
                'region_type': 'innovation_frontrunners',
                'gdp_growth_rate': 0.028,
                'tech_hub_score': 90.0,
                'remote_work_adoption': 65.0,
                'climate_pressure': 'MODERATE'
            },
            {
                'name': 'European Urban Centers', 
                'region_type': 'mature_cities',
                'gdp_growth_rate': 0.022,
                'infrastructure_quality': 85.0,
                'climate_adaptation_investment': 0.04,
                'climate_pressure': 'MODERATE'
            },
            {
                'name': 'Asian Megacities',
                'region_type': 'upwardly_mobile',
                'gdp_growth_rate': 0.055,
                'population_growth_rate': 0.025,
                'urbanization_rate': 0.035,
                'climate_pressure': 'HIGH'
            },
            {
                'name': 'Southeast Asian Growth Corridors',
                'region_type': 'emerging_markets',
                'gdp_growth_rate': 0.048,
                'infrastructure_investment_rate': 0.08,
                'climate_pressure': 'EXTREME'
            },
            {
                'name': 'Sub-Saharan African Cities',
                'region_type': 'emerging_markets',
                'gdp_growth_rate': 0.042,
                'population_growth_rate': 0.032,
                'water_security_index': 45.0,
                'climate_pressure': 'HIGH'
            },
            {
                'name': 'Latin American Coastal Cities',
                'region_type': 'upwardly_mobile', 
                'gdp_growth_rate': 0.035,
                'political_stability_index': 60.0,
                'climate_pressure': 'HIGH'
            },
            {
                'name': 'Middle Eastern Business Hubs',
                'region_type': 'innovation_frontrunners',
                'gdp_growth_rate': 0.038,
                'tech_hub_score': 75.0,
                'water_security_index': 35.0,
                'climate_pressure': 'EXTREME'
            },
            {
                'name': 'Australian Urban Centers',
                'region_type': 'mature_cities',
                'gdp_growth_rate': 0.025,
                'remote_work_adoption': 55.0,
                'climate_pressure': 'HIGH'
            },
            {
                'name': 'Rust Belt Industrial Cities',
                'region_type': 'declining_industrial',
                'gdp_growth_rate': 0.008,
                'population_growth_rate': -0.005,
                'infrastructure_quality': 55.0,
                'climate_pressure': 'MODERATE'
            },
            {
                'name': 'Small Island Nations',
                'region_type': 'climate_vulnerable',
                'gdp_growth_rate': 0.018,
                'climate_pressure': 'EXTREME',
                'water_security_index': 30.0
            }
        ]
    
    def _create_region_profile(self, config: Dict[str, Any]) -> RegionProfile:
        """Create a RegionProfile from configuration dictionary."""
        climate_pressure_map = {
            'LOW': ClimatePressure.LOW,
            'MODERATE': ClimatePressure.MODERATE, 
            'HIGH': ClimatePressure.HIGH,
            'EXTREME': ClimatePressure.EXTREME
        }
        
        region_type_map = {
            'mature_cities': RegionType.MATURE_CITIES,
            'upwardly_mobile': RegionType.UPWARDLY_MOBILE,
            'innovation_frontrunners': RegionType.INNOVATION_FRONTRUNNERS,
            'declining_industrial': RegionType.DECLINING_INDUSTRIAL,
            'emerging_markets': RegionType.EMERGING_MARKETS,
            'climate_vulnerable': RegionType.CLIMATE_VULNERABLE
        }
        
        return RegionProfile(
            name=config['name'],
            region_type=region_type_map.get(config.get('region_type', 'mature_cities'), RegionType.MATURE_CITIES),
            initial_land_price_index=config.get('initial_land_price_index', 100.0),
            gdp_growth_rate=config.get('gdp_growth_rate', 0.03),
            population_growth_rate=config.get('population_growth_rate', 0.01),
            urbanization_rate=config.get('urbanization_rate', 0.02),
            tech_hub_score=config.get('tech_hub_score', 50.0),
            infrastructure_quality=config.get('infrastructure_quality', 70.0),
            infrastructure_investment_rate=config.get('infrastructure_investment_rate', 0.05),
            transportation_connectivity=config.get('transportation_connectivity', 60.0),
            climate_pressure=climate_pressure_map.get(config.get('climate_pressure', 'MODERATE'), ClimatePressure.MODERATE),
            water_security_index=config.get('water_security_index', 70.0),
            food_security_index=config.get('food_security_index', 75.0),
            climate_adaptation_investment=config.get('climate_adaptation_investment', 0.02),
            political_stability_index=config.get('political_stability_index', 70.0),
            regulatory_environment=config.get('regulatory_environment', 60.0),
            social_inequality_index=config.get('social_inequality_index', 40.0),
            remote_work_adoption=config.get('remote_work_adoption', 30.0),
            digital_infrastructure=config.get('digital_infrastructure', 65.0),
            innovation_investment=config.get('innovation_investment', 0.03),
            developable_land_ratio=config.get('developable_land_ratio', 0.7),
            zoning_flexibility=config.get('zoning_flexibility', 50.0),
            land_use_efficiency=config.get('land_use_efficiency', 60.0)
        )
    
    def _simulate_regional_trends(self, region: RegionProfile, shock: GeopoliticalShock, years: int) -> Dict[str, Any]:
        """Simulate detailed trends for a specific region."""
        # Use the simple function as the core engine
        simple_results = simulate_land_price_trends(region, shock, years)
        
        # Enhanced simulation with detailed dynamics
        price_series = []
        volatility_series = []
        affordability_series = []
        investment_attractiveness = []
        
        current_price = region.initial_land_price_index
        base_income = 50000  # Baseline household income
        
        # Set random seed for reproducible results
        np.random.seed(hash(region.name) % 2147483647)
        
        for year in range(years):
            # Technology impact evolution
            tech_boost = min(region.tech_hub_score / 100 * 0.03 * (1 + year * 0.1), 0.06)
            
            # Climate pressure escalation
            climate_impact = -region.climate_pressure.value * 0.01 * (1 + year * 0.05)
            
            # Infrastructure development impact
            infra_boost = region.infrastructure_investment_rate * 1.5 * (1 + year * 0.02)
            
            # Remote work displacement effect
            remote_effect = -(region.remote_work_adoption / 100) * 0.02 * (1 + year * 0.1)
            
            # Political stability impact
            political_factor = (region.political_stability_index / 100 - 0.5) * 0.02
            
            # Resource security impact
            resource_security = ((region.water_security_index + region.food_security_index) / 200 - 0.5) * 0.015
            
            # Compound growth calculation
            annual_growth = (region.gdp_growth_rate + region.population_growth_rate + 
                           region.urbanization_rate + tech_boost + climate_impact +
                           infra_boost + remote_effect + political_factor + resource_security)
            
            # Apply shocks after start period
            if year >= shock.start_period:
                shock_impact = -(shock.trade_war_intensity + shock.energy_crisis_severity +
                               shock.financial_crisis_risk + shock.climate_disaster_frequency) * 0.015
                annual_growth += shock_impact
            
            # Add market volatility
            market_volatility = 0.08 + (region.political_stability_index < 60) * 0.05
            volatility_shock = np.random.normal(0, market_volatility)
            annual_growth += volatility_shock
            
            # Update price
            current_price *= (1 + annual_growth)
            price_series.append(current_price)
            volatility_series.append(abs(volatility_shock))
            
            # Calculate affordability (inverse relationship with price)
            current_income = base_income * (1 + region.gdp_growth_rate) ** year
            affordability = (current_income / current_price) * 100
            affordability_series.append(affordability)
            
            # Investment attractiveness score
            attractiveness = (
                (annual_growth * 100) +  # Growth potential
                (region.political_stability_index / 2) +  # Stability
                (region.infrastructure_quality / 3) +    # Infrastructure
                -(market_volatility * 100)  # Risk penalty
            )
            investment_attractiveness.append(attractiveness)
        
        return {
            'region_profile': {
                'name': region.name,
                'type': region.region_type.value,
                'tech_hub_score': region.tech_hub_score,
                'climate_pressure': region.climate_pressure.name,
                'political_stability': region.political_stability_index
            },
            'price_evolution': {
                'initial_price': region.initial_land_price_index,
                'final_price': price_series[-1],
                'price_series': price_series,
                'annual_growth_rate': simple_results['annual_growth_rate'],
                'peak_year': simple_results['peak_price_year']
            },
            'market_characteristics': {
                'volatility_series': volatility_series,
                'average_volatility': np.mean(volatility_series),
                'affordability_series': affordability_series,
                'final_affordability': affordability_series[-1],
                'investment_attractiveness': investment_attractiveness
            },
            'classification': simple_results['region_classification'],
            'growth_drivers': simple_results['growth_drivers'],
            'risk_factors': simple_results['risk_factors'],
            'sustainability_metrics': {
                'climate_resilience': 100 - region.climate_pressure.value * 20,
                'resource_security': (region.water_security_index + region.food_security_index) / 2,
                'social_stability': region.political_stability_index,
                'economic_diversity': region.tech_hub_score * 0.3 + region.infrastructure_quality * 0.4 + region.regulatory_environment * 0.3
            }
        }
    
    def _calculate_global_trends(self, results: Dict[str, Any], region_results: Dict[str, Any], years: int):
        """Calculate global trend indicators."""
        all_prices = []
        volatilities = []
        
        for year in range(years):
            year_prices = []
            year_volatilities = []
            
            for region_name, region_data in region_results.items():
                if year < len(region_data['price_evolution']['price_series']):
                    year_prices.append(region_data['price_evolution']['price_series'][year])
                    year_volatilities.append(region_data['market_characteristics']['volatility_series'][year])
            
            results['global_trends']['average_price_index'].append(np.mean(year_prices) if year_prices else 100)
            results['global_trends']['price_volatility'].append(np.mean(year_volatilities) if year_volatilities else 0)
        
        # Classify regions
        for region_name, region_data in region_results.items():
            classification = region_data['classification']
            if '🌆' in classification:
                results['global_trends']['high_growth_regions'].append(region_name)
            elif '⚠️' in classification:
                results['global_trends']['high_risk_regions'].append(region_name)
            elif '🧊' in classification:
                results['global_trends']['declining_regions'].append(region_name)
    
    def _calculate_market_dynamics(self, results: Dict[str, Any], years: int, shock: GeopoliticalShock):
        """Calculate market dynamics and external factors."""
        for year in range(years):
            # Technology impact (growing over time)
            tech_impact = self.parameters['ai_productivity_boost'] * (1 + year * 0.1)
            results['market_dynamics']['technology_impact'].append(tech_impact)
            
            # Climate adaptation costs (accelerating)
            climate_costs = self.parameters['climate_adaptation_cost_growth'] * (1 + year * 0.08)
            results['market_dynamics']['climate_adaptation_costs'].append(climate_costs)
            
            # Infrastructure investment (varies by cycle)
            infra_investment = self.parameters['global_infrastructure_deficit'] * (1 + 0.1 * np.sin(year * 0.5))
            results['market_dynamics']['infrastructure_investment'].append(infra_investment)
            
            # Migration flows (increasing with pressures)
            migration = self.parameters['migration_pressure_growth'] * (1 + year * 0.05)
            if year >= shock.start_period:
                migration += shock.migration_pressure * 0.5
            results['market_dynamics']['migration_flows'].append(migration)
            
            # Political risk index
            political_risk = 50 + shock.trade_war_intensity * 30 + shock.financial_crisis_risk * 20
            results['market_dynamics']['political_risk_index'].append(political_risk)
    
    def _generate_summary(self, region_results: Dict[str, Any], years: int) -> Dict[str, Any]:
        """Generate comprehensive summary of analysis."""
        growth_rates = []
        volatilities = []
        final_prices = []
        
        high_growth_count = 0
        high_risk_count = 0
        declining_count = 0
        
        for region_data in region_results.values():
            growth_rates.append(region_data['price_evolution']['annual_growth_rate'])
            volatilities.append(region_data['market_characteristics']['average_volatility'])
            final_prices.append(region_data['price_evolution']['final_price'])
            
            classification = region_data['classification']
            if '🌆' in classification:
                high_growth_count += 1
            elif '⚠️' in classification:
                high_risk_count += 1
            elif '🧊' in classification:
                declining_count += 1
        
        return {
            'total_regions_analyzed': len(region_results),
            'average_annual_growth': np.mean(growth_rates),
            'median_annual_growth': np.median(growth_rates),
            'growth_rate_range': [np.min(growth_rates), np.max(growth_rates)],
            'average_volatility': np.mean(volatilities),
            'price_index_range': [np.min(final_prices), np.max(final_prices)],
            'regional_distribution': {
                'high_growth_regions': high_growth_count,
                'high_risk_regions': high_risk_count,
                'declining_regions': declining_count,
                'stable_regions': len(region_results) - high_growth_count - high_risk_count - declining_count
            },
            'market_outlook': self._determine_market_outlook(growth_rates, volatilities),
            'key_trends': self._identify_key_trends(region_results),
            'investment_climate': self._assess_investment_climate(growth_rates, volatilities)
        }
    
    def _rank_regions(self, region_results: Dict[str, Any]) -> Dict[str, List[Tuple[str, float]]]:
        """Rank regions by various criteria."""
        rankings = {
            'by_growth_rate': [],
            'by_investment_attractiveness': [],
            'by_sustainability': [],
            'by_risk_adjusted_return': []
        }
        
        for region_name, region_data in region_results.items():
            growth_rate = region_data['price_evolution']['annual_growth_rate']
            volatility = region_data['market_characteristics']['average_volatility']
            sustainability = np.mean(list(region_data['sustainability_metrics'].values()))
            investment_score = np.mean(region_data['market_characteristics']['investment_attractiveness'])
            risk_adjusted = growth_rate / (volatility + 0.01)  # Avoid division by zero
            
            rankings['by_growth_rate'].append((region_name, growth_rate))
            rankings['by_investment_attractiveness'].append((region_name, investment_score))
            rankings['by_sustainability'].append((region_name, sustainability))
            rankings['by_risk_adjusted_return'].append((region_name, risk_adjusted))
        
        # Sort all rankings
        for key in rankings:
            rankings[key].sort(key=lambda x: x[1], reverse=True)
        
        return rankings
    
    def _generate_investment_recommendations(self, region_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate investment recommendations based on analysis."""
        recommendations = {
            'top_growth_opportunities': [],
            'defensive_plays': [],
            'value_investments': [],
            'avoid_list': [],
            'sector_insights': {},
            'timing_recommendations': {}
        }
        
        for region_name, region_data in region_results.items():
            growth_rate = region_data['price_evolution']['annual_growth_rate']
            volatility = region_data['market_characteristics']['average_volatility']
            sustainability = np.mean(list(region_data['sustainability_metrics'].values()))
            classification = region_data['classification']
            
            # Growth opportunities (high growth, manageable risk)
            if growth_rate > 5 and volatility < 0.15:
                recommendations['top_growth_opportunities'].append({
                    'region': region_name,
                    'growth_rate': growth_rate,
                    'rationale': f"Strong fundamentals with {growth_rate:.1f}% annual growth"
                })
            
            # Defensive plays (stable, lower volatility)
            elif volatility < 0.08 and sustainability > 65:
                recommendations['defensive_plays'].append({
                    'region': region_name,
                    'stability_score': sustainability,
                    'rationale': "Low volatility with strong sustainability metrics"
                })
            
            # Value investments (currently underpriced)
            elif growth_rate > 2 and region_data['price_evolution']['final_price'] < 120:
                recommendations['value_investments'].append({
                    'region': region_name,
                    'value_score': growth_rate / (region_data['price_evolution']['final_price'] / 100),
                    'rationale': "Undervalued relative to growth potential"
                })
            
            # Avoid list (high risk, poor fundamentals)
            elif '⚠️' in classification or '🧊' in classification:
                recommendations['avoid_list'].append({
                    'region': region_name,
                    'risk_factors': region_data['risk_factors'],
                    'rationale': f"High risk profile: {classification}"
                })
        
        # Sort recommendations
        recommendations['top_growth_opportunities'].sort(key=lambda x: x['growth_rate'], reverse=True)
        recommendations['defensive_plays'].sort(key=lambda x: x['stability_score'], reverse=True)
        recommendations['value_investments'].sort(key=lambda x: x['value_score'], reverse=True)
        
        return recommendations
    
    def _determine_market_outlook(self, growth_rates: List[float], volatilities: List[float]) -> str:
        """Determine overall market outlook."""
        avg_growth = np.mean(growth_rates)
        avg_volatility = np.mean(volatilities)
        
        if avg_growth > 4 and avg_volatility < 0.12:
            return "📈 Optimistic - Strong growth with manageable risk"
        elif avg_growth > 2 and avg_volatility < 0.15:
            return "📊 Cautiously Optimistic - Moderate growth expected"
        elif avg_growth < 1 or avg_volatility > 0.2:
            return "⚠️ Cautious - High uncertainty and volatility"
        else:
            return "📉 Pessimistic - Weak growth outlook with elevated risks"
    
    def _identify_key_trends(self, region_results: Dict[str, Any]) -> List[str]:
        """Identify key market trends across regions."""
        trends = []
        
        # Technology hub premium
        tech_regions = [r for r in region_results.values() if r['region_profile']['tech_hub_score'] > 75]
        if len(tech_regions) > 0:
            avg_tech_growth = np.mean([r['price_evolution']['annual_growth_rate'] for r in tech_regions])
            trends.append(f"Technology hubs showing {avg_tech_growth:.1f}% average growth premium")
        
        # Climate vulnerability discount
        climate_vulnerable = [r for r in region_results.values() if 'Climate vulnerability' in r['risk_factors']]
        if len(climate_vulnerable) > 0:
            trends.append(f"{len(climate_vulnerable)} regions showing climate vulnerability impacts")
        
        # Remote work displacement
        high_remote = [r for r in region_results.values() if 'remote work' in str(r['growth_drivers']).lower()]
        if len(high_remote) > 0:
            trends.append("Remote work adoption creating new location preferences")
        
        # Infrastructure investment impact
        high_infra = [r for r in region_results.values() if 'Infrastructure development' in r['growth_drivers']]
        if len(high_infra) > 0:
            trends.append(f"Infrastructure investment driving growth in {len(high_infra)} regions")
        
        return trends
    
    def _assess_investment_climate(self, growth_rates: List[float], volatilities: List[float]) -> str:
        """Assess overall investment climate."""
        avg_growth = np.mean(growth_rates)
        avg_volatility = np.mean(volatilities)
        
        if avg_growth > 3 and avg_volatility < 0.1:
            return "Excellent - High returns with low risk"
        elif avg_growth > 2 and avg_volatility < 0.15:
            return "Good - Solid returns with moderate risk"
        elif avg_growth > 0 and avg_volatility < 0.2:
            return "Fair - Limited returns but manageable risk"
        else:
            return "Poor - High risk with uncertain returns" 