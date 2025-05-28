"""
Test Suite for Jinn-Core Economic Simulation Engine

MVP tests covering basic functionality of the simulation engine and models.
"""

import unittest
import sys
import os
import json
from unittest.mock import patch, mock_open

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from engine import SimulationEngine
from models.interest_rate import InterestRateModel, InterestRateShock
from models.inflation_shock import InflationShockModel, InflationShock, simulate_inflation_shock


class TestSimulationEngine(unittest.TestCase):
    """Test cases for the main simulation engine."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.engine = SimulationEngine()
    
    def test_engine_initialization(self):
        """Test that the engine initializes correctly."""
        self.assertIsInstance(self.engine, SimulationEngine)
        self.assertIn('interest_rate', self.engine.models)
        self.assertIn('inflation_shock', self.engine.models)
        self.assertEqual(self.engine.models['interest_rate'], InterestRateModel)
        self.assertEqual(self.engine.models['inflation_shock'], InflationShockModel)
    
    def test_model_registration(self):
        """Test that models are properly registered."""
        self.assertEqual(len(self.engine.models), 2)
        self.assertIn('interest_rate', self.engine.models)
        self.assertIn('inflation_shock', self.engine.models)
    
    @patch('builtins.open', new_callable=mock_open, read_data='{"model": "interest_rate", "test": true}')
    def test_load_scenario(self, mock_file):
        """Test scenario loading from JSON file."""
        scenario = self.engine.load_scenario('test_scenario.json')
        self.assertIsInstance(scenario, dict)
        self.assertEqual(scenario['model'], 'interest_rate')
        self.assertTrue(scenario['test'])
        mock_file.assert_called_once_with('test_scenario.json', 'r')
    
    def test_load_scenario_file_not_found(self):
        """Test handling of missing scenario file."""
        with self.assertRaises(FileNotFoundError):
            self.engine.load_scenario('nonexistent_file.json')
    
    def test_run_simulation_basic(self):
        """Test basic simulation execution."""
        scenario = {
            'model': 'interest_rate',
            'parameters': {},
            'simulation': {
                'shock': {
                    'magnitude': 0.005,
                    'duration': 5,
                    'start_period': 0
                }
            }
        }
        
        results = self.engine.run_simulation(scenario)
        
        self.assertIsInstance(results, dict)
        self.assertEqual(results['model'], 'interest_rate')
        self.assertIn('results', results)
        self.assertIn('metadata', results)
        self.assertIn('execution_time_seconds', results['metadata'])
    
    def test_run_simulation_inflation_shock(self):
        """Test inflation shock simulation execution."""
        scenario = {
            'model': 'inflation_shock',
            'parameters': {},
            'simulation': {
                'shock': {
                    'spike_magnitude': 3.0,
                    'duration': 4,
                    'start_period': 1
                }
            }
        }
        
        results = self.engine.run_simulation(scenario)
        
        self.assertIsInstance(results, dict)
        self.assertEqual(results['model'], 'inflation_shock')
        self.assertIn('results', results)
        self.assertIn('metadata', results)
        self.assertIn('execution_time_seconds', results['metadata'])
    
    def test_run_simulation_unknown_model(self):
        """Test handling of unknown model."""
        scenario = {
            'model': 'unknown_model',
            'parameters': {},
            'simulation': {}
        }
        
        with self.assertRaises(ValueError) as context:
            self.engine.run_simulation(scenario)
        
        self.assertIn('Unknown model: unknown_model', str(context.exception))


class TestInterestRateModel(unittest.TestCase):
    """Test cases for the Interest Rate Model."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.model = InterestRateModel({})
    
    def test_model_initialization(self):
        """Test model initialization with default parameters."""
        self.assertIsInstance(self.model, InterestRateModel)
        self.assertIn('gdp_sensitivity', self.model.parameters)
        self.assertIn('baseline_gdp_growth', self.model.parameters)
        self.assertEqual(self.model.parameters['periods'], 20)
    
    def test_model_initialization_custom_params(self):
        """Test model initialization with custom parameters."""
        custom_params = {
            'gdp_sensitivity': -0.5,
            'periods': 12,
            'baseline_gdp_growth': 0.025
        }
        model = InterestRateModel(custom_params)
        
        self.assertEqual(model.parameters['gdp_sensitivity'], -0.5)
        self.assertEqual(model.parameters['periods'], 12)
        self.assertEqual(model.parameters['baseline_gdp_growth'], 0.025)
        # Check that default values are still present
        self.assertIn('inflation_sensitivity', model.parameters)
    
    def test_simulate_no_shock(self):
        """Test simulation with no shock."""
        simulation_config = {
            'shock': {
                'magnitude': 0.0,
                'duration': 0,
                'start_period': 0
            }
        }
        
        results = self.model.simulate(simulation_config)
        
        self.assertIsInstance(results, dict)
        self.assertIn('periods', results)
        self.assertIn('gdp_growth', results)
        self.assertIn('inflation', results)
        self.assertIn('investment', results)
        self.assertIn('consumption', results)
        self.assertIn('summary', results)
        
        # Check that baseline values are maintained
        gdp_values = results['gdp_growth']
        expected_baseline = self.model.parameters['baseline_gdp_growth']
        for value in gdp_values:
            self.assertAlmostEqual(value, expected_baseline, places=6)
    
    def test_simulate_with_shock(self):
        """Test simulation with interest rate shock."""
        simulation_config = {
            'shock': {
                'magnitude': 0.01,  # 100 basis points
                'duration': 5,
                'start_period': 0
            }
        }
        
        results = self.model.simulate(simulation_config)
        
        self.assertIsInstance(results, dict)
        
        # Check that shock is applied
        shock_values = results['interest_rate_shock']
        self.assertGreater(shock_values[0], 0)  # First period should have shock
        self.assertEqual(shock_values[10], 0)   # Later periods should have no shock
        
        # Check that GDP is affected negatively (due to negative sensitivity)
        gdp_values = results['gdp_growth']
        baseline_gdp = self.model.parameters['baseline_gdp_growth']
        self.assertLess(gdp_values[0], baseline_gdp)
    
    def test_shock_persistence(self):
        """Test that shock persistence is correctly applied."""
        simulation_config = {
            'shock': {
                'magnitude': 0.01,
                'duration': 3,
                'start_period': 0
            }
        }
        
        results = self.model.simulate(simulation_config)
        shock_values = results['interest_rate_shock']
        
        # First period should have full shock
        self.assertAlmostEqual(shock_values[0], 0.01, places=6)
        
        # Second period should be smaller due to persistence
        persistence = self.model.parameters['persistence']
        expected_second = 0.01 * persistence
        self.assertAlmostEqual(shock_values[1], expected_second, places=6)
        
        # Third period should be even smaller
        expected_third = 0.01 * (persistence ** 2)
        self.assertAlmostEqual(shock_values[2], expected_third, places=6)
    
    def test_summary_statistics(self):
        """Test that summary statistics are calculated correctly."""
        simulation_config = {
            'shock': {
                'magnitude': 0.005,
                'duration': 3,
                'start_period': 1
            }
        }
        
        results = self.model.simulate(simulation_config)
        summary = results['summary']
        
        # Check that all expected summary fields are present
        expected_fields = [
            'avg_gdp_growth', 'min_gdp_growth', 'max_gdp_growth',
            'avg_inflation', 'min_inflation', 'max_inflation',
            'total_investment_change', 'total_consumption_change'
        ]
        
        for field in expected_fields:
            self.assertIn(field, summary)
            self.assertIsInstance(summary[field], float)


class TestInflationShockModel(unittest.TestCase):
    """Test cases for the Inflation Shock Model."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.model = InflationShockModel({})
    
    def test_model_initialization(self):
        """Test model initialization with default parameters."""
        self.assertIsInstance(self.model, InflationShockModel)
        self.assertIn('gdp_contraction_rate', self.model.parameters)
        self.assertIn('baseline_inflation', self.model.parameters)
        self.assertEqual(self.model.parameters['periods'], 20)
    
    def test_model_initialization_custom_params(self):
        """Test model initialization with custom parameters."""
        custom_params = {
            'gdp_contraction_rate': -0.06,
            'periods': 12,
            'baseline_inflation': 0.03
        }
        model = InflationShockModel(custom_params)
        
        self.assertEqual(model.parameters['gdp_contraction_rate'], -0.06)
        self.assertEqual(model.parameters['periods'], 12)
        self.assertEqual(model.parameters['baseline_inflation'], 0.03)
        # Check that default values are still present
        self.assertIn('investment_sensitivity', model.parameters)
    
    def test_simulate_no_shock(self):
        """Test simulation with no inflation shock."""
        simulation_config = {
            'shock': {
                'spike_magnitude': 0.0,
                'duration': 0,
                'start_period': 0
            }
        }
        
        results = self.model.simulate(simulation_config)
        
        self.assertIsInstance(results, dict)
        self.assertIn('periods', results)
        self.assertIn('inflation_rate', results)
        self.assertIn('real_gdp', results)
        self.assertIn('investment', results)
        self.assertIn('consumption', results)
        self.assertIn('summary', results)
        
        # Check that baseline values are maintained
        inflation_values = results['inflation_rate']
        expected_baseline = self.model.parameters['baseline_inflation']
        for value in inflation_values:
            self.assertAlmostEqual(value, expected_baseline, places=6)
    
    def test_simulate_with_shock(self):
        """Test simulation with inflation shock."""
        simulation_config = {
            'shock': {
                'spike_magnitude': 3.0,  # 3 percentage points
                'duration': 4,
                'start_period': 1
            }
        }
        
        results = self.model.simulate(simulation_config)
        
        self.assertIsInstance(results, dict)
        
        # Check that shock is applied
        shock_values = results['inflation_shock']
        self.assertEqual(shock_values[0], 0)    # No shock in first period
        self.assertGreater(shock_values[1], 0)  # Shock starts in period 1
        self.assertEqual(shock_values[10], 0)   # Later periods should have no shock
        
        # Check that inflation rate is affected
        inflation_values = results['inflation_rate']
        baseline_inflation = self.model.parameters['baseline_inflation']
        self.assertGreater(inflation_values[1], baseline_inflation)
    
    def test_shock_persistence(self):
        """Test that inflation shock persistence is correctly applied."""
        simulation_config = {
            'shock': {
                'spike_magnitude': 4.0,
                'duration': 3,
                'start_period': 0
            }
        }
        
        results = self.model.simulate(simulation_config)
        shock_values = results['inflation_shock']
        
        # First period should have full shock
        self.assertAlmostEqual(shock_values[0], 4.0, places=6)
        
        # Second period should be smaller due to persistence
        persistence = self.model.parameters['shock_persistence']
        expected_second = 4.0 * persistence
        self.assertAlmostEqual(shock_values[1], expected_second, places=6)
        
        # Third period should be even smaller
        expected_third = 4.0 * (persistence ** 2)
        self.assertAlmostEqual(shock_values[2], expected_third, places=6)
    
    def test_summary_statistics(self):
        """Test that summary statistics are calculated correctly."""
        simulation_config = {
            'shock': {
                'spike_magnitude': 2.0,
                'duration': 3,
                'start_period': 1
            }
        }
        
        results = self.model.simulate(simulation_config)
        summary = results['summary']
        
        # Check that all expected summary fields are present
        expected_fields = [
            'avg_inflation_rate', 'peak_inflation', 'min_inflation',
            'avg_real_gdp', 'min_real_gdp', 'max_real_gdp',
            'total_gdp_loss', 'total_investment_loss', 'total_consumption_loss',
            'gdp_contraction_percent'
        ]
        
        for field in expected_fields:
            self.assertIn(field, summary)
            self.assertIsInstance(summary[field], float)


class TestSimpleInflationFunction(unittest.TestCase):
    """Test cases for the simple simulate_inflation_shock function."""
    
    def test_simple_function_basic(self):
        """Test basic functionality of the simple inflation shock function."""
        result = simulate_inflation_shock(
            current_inflation=2.0,
            inflation_spike=3.0,
            gdp=1000000.0,
            investment_level=200000.0
        )
        
        # Check all expected keys are present
        expected_keys = ['new_inflation', 'real_gdp_estimate', 'expected_investment_drop', 'expected_consumption_change']
        for key in expected_keys:
            self.assertIn(key, result)
        
        # Check calculations
        self.assertEqual(result['new_inflation'], 5.0)  # 2 + 3
        self.assertEqual(result['real_gdp_estimate'], 960000.0)  # 1M * 0.96
        self.assertEqual(result['expected_investment_drop'], 6.0)  # 3 * 2
        self.assertEqual(result['expected_consumption_change'], -4.0)
    
    def test_investment_drop_cap(self):
        """Test that investment drop is capped at 20%."""
        result = simulate_inflation_shock(
            current_inflation=2.0,
            inflation_spike=15.0,  # Would normally cause 30% drop
            gdp=1000000.0,
            investment_level=200000.0
        )
        
        # Should be capped at 20%
        self.assertEqual(result['expected_investment_drop'], 20.0)


class TestInterestRateShock(unittest.TestCase):
    """Test cases for the InterestRateShock dataclass."""
    
    def test_shock_creation(self):
        """Test creating an interest rate shock."""
        shock = InterestRateShock(magnitude=0.005, duration=4)
        
        self.assertEqual(shock.magnitude, 0.005)
        self.assertEqual(shock.duration, 4)
        self.assertEqual(shock.start_period, 0)  # Default value
    
    def test_shock_creation_with_start_period(self):
        """Test creating a shock with custom start period."""
        shock = InterestRateShock(magnitude=0.01, duration=6, start_period=3)
        
        self.assertEqual(shock.magnitude, 0.01)
        self.assertEqual(shock.duration, 6)
        self.assertEqual(shock.start_period, 3)


class TestInflationShock(unittest.TestCase):
    """Test cases for the InflationShock dataclass."""
    
    def test_shock_creation(self):
        """Test creating an inflation shock."""
        shock = InflationShock(spike_magnitude=3.0, duration=5)
        
        self.assertEqual(shock.spike_magnitude, 3.0)
        self.assertEqual(shock.duration, 5)
        self.assertEqual(shock.start_period, 0)  # Default value
    
    def test_shock_creation_with_start_period(self):
        """Test creating a shock with custom start period."""
        shock = InflationShock(spike_magnitude=2.5, duration=4, start_period=2)
        
        self.assertEqual(shock.spike_magnitude, 2.5)
        self.assertEqual(shock.duration, 4)
        self.assertEqual(shock.start_period, 2)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete simulation flow."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.engine = SimulationEngine()
        self.interest_rate_scenario = {
            'model': 'interest_rate',
            'parameters': {
                'periods': 10,
                'gdp_sensitivity': -0.3
            },
            'simulation': {
                'shock': {
                    'magnitude': 0.0075,
                    'duration': 4,
                    'start_period': 1
                }
            }
        }
        self.inflation_shock_scenario = {
            'model': 'inflation_shock',
            'parameters': {
                'periods': 8,
                'gdp_contraction_rate': -0.05
            },
            'simulation': {
                'shock': {
                    'spike_magnitude': 3.0,
                    'duration': 3,
                    'start_period': 1
                }
            }
        }
    
    def test_full_simulation_flow_interest_rate(self):
        """Test the complete simulation flow for interest rate model."""
        results = self.engine.run_simulation(self.interest_rate_scenario)
        
        # Verify structure
        self.assertIn('model', results)
        self.assertIn('scenario', results)
        self.assertIn('results', results)
        self.assertIn('metadata', results)
        
        # Verify content
        self.assertEqual(results['model'], 'interest_rate')
        self.assertEqual(len(results['results']['periods']), 10)
        
        # Verify timing information
        metadata = results['metadata']
        self.assertIn('start_time', metadata)
        self.assertIn('end_time', metadata)
        self.assertIn('execution_time_seconds', metadata)
        self.assertGreaterEqual(metadata['execution_time_seconds'], 0)
    
    def test_full_simulation_flow_inflation_shock(self):
        """Test the complete simulation flow for inflation shock model."""
        results = self.engine.run_simulation(self.inflation_shock_scenario)
        
        # Verify structure
        self.assertIn('model', results)
        self.assertIn('scenario', results)
        self.assertIn('results', results)
        self.assertIn('metadata', results)
        
        # Verify content
        self.assertEqual(results['model'], 'inflation_shock')
        self.assertEqual(len(results['results']['periods']), 8)
        
        # Verify timing information
        metadata = results['metadata']
        self.assertIn('start_time', metadata)
        self.assertIn('end_time', metadata)
        self.assertIn('execution_time_seconds', metadata)
        self.assertGreaterEqual(metadata['execution_time_seconds'], 0)
    
    @patch('builtins.open', new_callable=mock_open)
    def test_run_scenario_file_integration(self, mock_file):
        """Test running a scenario from file."""
        # Mock file content
        mock_file.return_value.read.return_value = json.dumps(self.interest_rate_scenario)
        
        # This would normally read from file
        results = self.engine.run_simulation(self.interest_rate_scenario)
        
        self.assertIsInstance(results, dict)
        self.assertEqual(results['model'], 'interest_rate')


if __name__ == '__main__':
    # Set up logging to suppress info messages during tests
    import logging
    logging.getLogger().setLevel(logging.WARNING)
    
    # Run the tests
    unittest.main(verbosity=2) 