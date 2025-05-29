"""
Test Suite for Bitcoin Price Projection Model

Tests covering the Bitcoin price projection model functionality.
"""

import unittest
import sys
import os
import math

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models.btc_price_projection import BTCPriceProjectionModel, BTCProjectionScenario, simulate_btc_price_projection
from engine import SimulationEngine


class TestBTCPriceProjectionModel(unittest.TestCase):
    """Test cases for the Bitcoin Price Projection Model."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.model = BTCPriceProjectionModel({})
    
    def test_model_initialization(self):
        """Test model initialization with default parameters."""
        self.assertIsInstance(self.model, BTCPriceProjectionModel)
        self.assertIn('current_price_usd', self.model.parameters)
        self.assertIn('target_price_usd', self.model.parameters)
        self.assertIn('max_years', self.model.parameters)
        self.assertEqual(self.model.parameters['current_price_usd'], 70000.0)
        self.assertEqual(self.model.parameters['target_price_usd'], 1000000.0)
        self.assertEqual(self.model.parameters['max_years'], 30)
        
        # Check scenarios are defined
        self.assertIn('baseline', self.model.scenarios)
        self.assertIn('institutional_adoption', self.model.scenarios)
        self.assertIn('fiat_crisis', self.model.scenarios)
        self.assertIn('regulatory_clarity', self.model.scenarios)
        self.assertIn('combined_shock', self.model.scenarios)
    
    def test_model_initialization_custom_params(self):
        """Test model initialization with custom parameters."""
        custom_params = {
            'current_price_usd': 100000.0,
            'target_price_usd': 500000.0,
            'max_years': 20,
            'baseline_volatility': 0.4
        }
        model = BTCPriceProjectionModel(custom_params)
        
        self.assertEqual(model.parameters['current_price_usd'], 100000.0)
        self.assertEqual(model.parameters['target_price_usd'], 500000.0)
        self.assertEqual(model.parameters['max_years'], 20)
        self.assertEqual(model.parameters['baseline_volatility'], 0.4)
        # Check that default values are still present
        self.assertIn('institutional_allocation', model.parameters)
    
    def test_scenario_definitions(self):
        """Test that scenarios are properly defined."""
        scenarios = self.model.scenarios
        
        # Check baseline scenario
        baseline = scenarios['baseline']
        self.assertEqual(baseline.annual_growth_rate, 0.40)
        self.assertEqual(baseline.volatility_factor, 1.0)
        self.assertEqual(baseline.adoption_curve, "linear")
        
        # Check institutional adoption scenario
        institutional = scenarios['institutional_adoption']
        self.assertEqual(institutional.annual_growth_rate, 0.55)
        self.assertEqual(institutional.volatility_factor, 0.8)
        self.assertEqual(institutional.adoption_curve, "exponential")
        
        # Check combined shock scenario
        combined = scenarios['combined_shock']
        self.assertEqual(combined.annual_growth_rate, 0.75)
        self.assertEqual(combined.institutional_factor, 2.5)
    
    def test_simulate_all_scenarios(self):
        """Test simulation with all scenarios."""
        simulation_config = {
            'current_price_usd': 70000.0,
            'target_price_usd': 1000000.0,
            'max_years': 30,
            'scenarios': ['baseline', 'institutional_adoption', 'fiat_crisis', 'regulatory_clarity', 'combined_shock']
        }
        
        results = self.model.simulate(simulation_config)
        
        self.assertIsInstance(results, dict)
        self.assertIn('parameters', results)
        self.assertIn('scenarios', results)
        self.assertIn('comparison', results)
        self.assertIn('summary', results)
        
        # Check that all scenarios were run
        self.assertEqual(len(results['scenarios']), 5)
        for scenario_name in simulation_config['scenarios']:
            self.assertIn(scenario_name, results['scenarios'])
    
    def test_simulate_single_scenario(self):
        """Test simulation with a single scenario."""
        simulation_config = {
            'current_price_usd': 70000.0,
            'target_price_usd': 1000000.0,
            'max_years': 30,
            'scenarios': ['baseline']
        }
        
        results = self.model.simulate(simulation_config)
        
        self.assertIsInstance(results, dict)
        self.assertEqual(len(results['scenarios']), 1)
        self.assertIn('baseline', results['scenarios'])
        
        # Check scenario results structure
        baseline_results = results['scenarios']['baseline']
        self.assertIn('scenario_name', baseline_results)
        self.assertIn('description', baseline_results)
        self.assertIn('annual_growth_rate', baseline_results)
        self.assertIn('base_projection', baseline_results)
        self.assertIn('enhanced_projection', baseline_results)
        self.assertIn('risk_assessment', baseline_results)


class TestSimpleBTCProjectionFunction(unittest.TestCase):
    """Test cases for the simple Bitcoin price projection function."""
    
    def test_simple_function_basic(self):
        """Test the simple Bitcoin price projection function with basic inputs."""
        result = simulate_btc_price_projection(
            current_price_usd=70000.0,
            target_price_usd=1000000.0,
            annual_growth_rate=0.40,  # 40% annual growth
            max_years=30
        )
        
        self.assertIsInstance(result, dict)
        self.assertIn('years_to_target', result)
        self.assertIn('final_price', result)
        self.assertIn('total_return_multiple', result)
        self.assertIn('annual_return_needed', result)
        self.assertIn('price_trajectory', result)
        self.assertIn('feasibility_assessment', result)
        self.assertIn('target_achieved_in_timeframe', result)
        
        # Check calculations
        expected_years = math.log(1000000 / 70000) / math.log(1.40)
        self.assertAlmostEqual(result['years_to_target'], expected_years, places=2)
        
        # Check that final price is calculated correctly
        expected_final_price = 70000 * (1.40 ** 30)
        self.assertAlmostEqual(result['final_price'], expected_final_price, places=0)
        
        # Check return multiple
        expected_multiple = result['final_price'] / 70000
        self.assertAlmostEqual(result['total_return_multiple'], expected_multiple, places=2)
    
    def test_growth_rate_scaling(self):
        """Test that higher growth rates result in faster target achievement."""
        # Low growth rate
        result_low = simulate_btc_price_projection(70000, 1000000, 0.20, 30)
        
        # High growth rate
        result_high = simulate_btc_price_projection(70000, 1000000, 0.60, 30)
        
        # High growth should reach target faster
        self.assertLess(result_high['years_to_target'], result_low['years_to_target'])
        self.assertGreater(result_high['final_price'], result_low['final_price'])
    
    def test_price_trajectory(self):
        """Test that price trajectory is calculated correctly."""
        result = simulate_btc_price_projection(70000, 1000000, 0.40, 10)
        
        trajectory = result['price_trajectory']
        self.assertEqual(len(trajectory), 11)  # 0 to 10 years inclusive
        
        # Check first and last points
        self.assertEqual(trajectory[0]['year'], 0)
        self.assertEqual(trajectory[0]['price'], 70000)
        self.assertEqual(trajectory[0]['return_multiple'], 1.0)
        
        self.assertEqual(trajectory[10]['year'], 10)
        expected_price_year_10 = 70000 * (1.40 ** 10)
        self.assertAlmostEqual(trajectory[10]['price'], expected_price_year_10, places=0)
    
    def test_feasibility_assessment(self):
        """Test feasibility assessment logic."""
        # Highly achievable (fast growth)
        result_fast = simulate_btc_price_projection(70000, 200000, 0.50, 30)
        self.assertIn("Highly achievable", result_fast['feasibility_assessment'])
        
        # Challenging (slow growth, high target, but still within timeframe)
        result_challenging = simulate_btc_price_projection(70000, 10000000, 0.20, 30)
        self.assertIn("Challenging but possible", result_challenging['feasibility_assessment'])
        
        # Unlikely (very slow growth, extremely high target)
        result_unlikely = simulate_btc_price_projection(70000, 50000000, 0.15, 30)
        self.assertIn("Unlikely", result_unlikely['feasibility_assessment'])
    
    def test_error_handling(self):
        """Test error handling for invalid inputs."""
        # Negative growth rate
        with self.assertRaises(ValueError):
            simulate_btc_price_projection(70000, 1000000, -0.1, 30)
        
        # Zero growth rate
        with self.assertRaises(ValueError):
            simulate_btc_price_projection(70000, 1000000, 0.0, 30)
        
        # Target price lower than current price
        with self.assertRaises(ValueError):
            simulate_btc_price_projection(70000, 50000, 0.40, 30)


class TestBTCProjectionScenario(unittest.TestCase):
    """Test cases for BTCProjectionScenario dataclass."""
    
    def test_scenario_creation(self):
        """Test creating a Bitcoin projection scenario."""
        scenario = BTCProjectionScenario(
            name="test_scenario",
            annual_growth_rate=0.45,
            description="Test scenario for unit testing",
            volatility_factor=0.9,
            adoption_curve="exponential",
            regulatory_impact=1.1,
            institutional_factor=1.5
        )
        
        self.assertEqual(scenario.name, "test_scenario")
        self.assertEqual(scenario.annual_growth_rate, 0.45)
        self.assertEqual(scenario.description, "Test scenario for unit testing")
        self.assertEqual(scenario.volatility_factor, 0.9)
        self.assertEqual(scenario.adoption_curve, "exponential")
        self.assertEqual(scenario.regulatory_impact, 1.1)
        self.assertEqual(scenario.institutional_factor, 1.5)
    
    def test_scenario_defaults(self):
        """Test scenario creation with default values."""
        scenario = BTCProjectionScenario(
            name="minimal_scenario",
            annual_growth_rate=0.30,
            description="Minimal scenario"
        )
        
        self.assertEqual(scenario.name, "minimal_scenario")
        self.assertEqual(scenario.annual_growth_rate, 0.30)
        self.assertEqual(scenario.volatility_factor, 0.2)  # Default value
        self.assertEqual(scenario.adoption_curve, "linear")  # Default value
        self.assertEqual(scenario.regulatory_impact, 1.0)  # Default value
        self.assertEqual(scenario.institutional_factor, 1.0)  # Default value


class TestBTCProjectionIntegration(unittest.TestCase):
    """Integration tests for Bitcoin price projection model."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.engine = SimulationEngine()
        self.btc_projection_scenario = {
            'model': 'btc_price_projection',
            'parameters': {
                'current_price_usd': 70000.0,
                'target_price_usd': 1000000.0,
                'max_years': 30
            },
            'simulation': {
                'current_price_usd': 70000.0,
                'target_price_usd': 1000000.0,
                'max_years': 30,
                'scenarios': ['baseline', 'institutional_adoption']
            }
        }
    
    def test_model_loads_and_runs(self):
        """Test that the model loads and runs successfully."""
        self.assertIn('btc_price_projection', self.engine.models)
        self.assertEqual(self.engine.models['btc_price_projection'], BTCPriceProjectionModel)
        
        # Run simulation
        results = self.engine.run_simulation(self.btc_projection_scenario)
        
        # Verify structure
        self.assertIn('model', results)
        self.assertIn('scenario', results)
        self.assertIn('results', results)
        self.assertIn('metadata', results)
        
        # Verify content
        self.assertEqual(results['model'], 'btc_price_projection')
    
    def test_outputs_match_expected_pattern(self):
        """Test that outputs follow expected patterns."""
        results = self.engine.run_simulation(self.btc_projection_scenario)
        simulation_results = results['results']
        
        # Check main structure
        self.assertIn('parameters', simulation_results)
        self.assertIn('scenarios', simulation_results)
        self.assertIn('comparison', simulation_results)
        self.assertIn('summary', simulation_results)
        
        # Check scenario results
        scenarios = simulation_results['scenarios']
        self.assertIn('baseline', scenarios)
        self.assertIn('institutional_adoption', scenarios)
        
        # Check that institutional adoption has higher growth than baseline
        baseline_growth = scenarios['baseline']['annual_growth_rate']
        institutional_growth = scenarios['institutional_adoption']['annual_growth_rate']
        self.assertGreater(institutional_growth, baseline_growth)
    
    def test_price_projections_are_positive(self):
        """Test that all price projections are positive and increasing."""
        results = self.engine.run_simulation(self.btc_projection_scenario)
        scenarios = results['results']['scenarios']
        
        for scenario_name, scenario_data in scenarios.items():
            # Check base projection
            base_proj = scenario_data['base_projection']
            self.assertGreater(base_proj['final_price'], base_proj['price_trajectory'][0]['price'])
            self.assertGreater(base_proj['total_return_multiple'], 1.0)
            
            # Check enhanced projection
            enhanced_proj = scenario_data['enhanced_projection']
            self.assertGreater(enhanced_proj['final_price'], 0)
            self.assertGreater(enhanced_proj['total_return_multiple'], 1.0)
    
    def test_risk_assessment_present(self):
        """Test that risk assessment is properly calculated."""
        results = self.engine.run_simulation(self.btc_projection_scenario)
        scenarios = results['results']['scenarios']
        
        for scenario_name, scenario_data in scenarios.items():
            risk_assessment = scenario_data['risk_assessment']
            
            # Check risk categories
            self.assertIn('time_risk', risk_assessment)
            self.assertIn('volatility_risk', risk_assessment)
            self.assertIn('regulatory_risk', risk_assessment)
            self.assertIn('overall_risk', risk_assessment)
            self.assertIn('risk_score', risk_assessment)
            self.assertIn('key_risks', risk_assessment)
            
            # Check risk levels are valid
            valid_risk_levels = ['Low', 'Medium', 'High', 'Very High']
            self.assertIn(risk_assessment['time_risk'], valid_risk_levels)
            self.assertIn(risk_assessment['volatility_risk'], valid_risk_levels)
            self.assertIn(risk_assessment['regulatory_risk'], valid_risk_levels)
            self.assertIn(risk_assessment['overall_risk'], ['Low', 'Medium', 'High'])
    
    def test_comparison_and_summary(self):
        """Test that comparison and summary are generated correctly."""
        results = self.engine.run_simulation(self.btc_projection_scenario)
        
        # Check comparison
        comparison = results['results']['comparison']
        self.assertIn('fastest_to_target', comparison)
        self.assertIn('highest_final_price', comparison)
        self.assertIn('lowest_risk', comparison)
        self.assertIn('most_realistic', comparison)
        self.assertIn('scenario_rankings', comparison)
        
        # Check summary
        summary = results['results']['summary']
        self.assertIn('target_analysis', summary)
        self.assertIn('time_to_target', summary)
        self.assertIn('price_projections', summary)
        self.assertIn('investment_insights', summary)
        
        # Check target analysis
        target_analysis = summary['target_analysis']
        self.assertEqual(target_analysis['current_price'], 70000.0)
        self.assertEqual(target_analysis['target_price'], 1000000.0)
        self.assertAlmostEqual(target_analysis['target_multiple'], 1000000 / 70000, places=2)


class TestBTCProjectionScenarios(unittest.TestCase):
    """Test specific Bitcoin projection scenarios."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.model = BTCPriceProjectionModel({})
    
    def test_baseline_scenario(self):
        """Test baseline scenario specifically."""
        simulation_config = {
            'current_price_usd': 70000.0,
            'target_price_usd': 1000000.0,
            'max_years': 30,
            'scenarios': ['baseline']
        }
        
        results = self.model.simulate(simulation_config)
        baseline = results['scenarios']['baseline']
        
        # Check growth rate
        self.assertEqual(baseline['annual_growth_rate'], 0.40)
        
        # Check that years to target is reasonable for 40% growth
        years_to_target = baseline['enhanced_projection']['years_to_target']
        self.assertGreater(years_to_target, 5)  # Should take more than 5 years
        self.assertLess(years_to_target, 15)    # Should take less than 15 years
    
    def test_combined_shock_scenario(self):
        """Test combined shock scenario (highest growth)."""
        simulation_config = {
            'current_price_usd': 70000.0,
            'target_price_usd': 1000000.0,
            'max_years': 30,
            'scenarios': ['combined_shock']
        }
        
        results = self.model.simulate(simulation_config)
        combined_shock = results['scenarios']['combined_shock']
        
        # Check growth rate
        self.assertEqual(combined_shock['annual_growth_rate'], 0.75)
        
        # Should reach target faster than baseline
        years_to_target = combined_shock['enhanced_projection']['years_to_target']
        self.assertLess(years_to_target, 10)  # Should be very fast with 75% growth
    
    def test_scenario_comparison(self):
        """Test comparison between different scenarios."""
        simulation_config = {
            'current_price_usd': 70000.0,
            'target_price_usd': 1000000.0,
            'max_years': 30,
            'scenarios': ['baseline', 'institutional_adoption', 'combined_shock']
        }
        
        results = self.model.simulate(simulation_config)
        scenarios = results['scenarios']
        
        # Get years to target for each scenario
        baseline_years = scenarios['baseline']['enhanced_projection']['years_to_target']
        institutional_years = scenarios['institutional_adoption']['enhanced_projection']['years_to_target']
        combined_years = scenarios['combined_shock']['enhanced_projection']['years_to_target']
        
        # Combined shock should be fastest, baseline should be slowest
        self.assertLess(combined_years, institutional_years)
        self.assertLess(institutional_years, baseline_years)


if __name__ == '__main__':
    # Set up logging to suppress info messages during tests
    import logging
    logging.getLogger().setLevel(logging.WARNING)
    
    # Run the tests
    unittest.main() 