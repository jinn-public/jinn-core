"""
Test Suite for Earth Rotation Shock Model

Tests covering the Earth rotation shock model functionality.
"""

import unittest
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models.earth_rotation_shock import EarthRotationShockModel, EarthRotationShock, simulate_earth_rotation_shock
from engine import SimulationEngine


class TestEarthRotationShockModel(unittest.TestCase):
    """Test cases for the Earth Rotation Shock Model."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.model = EarthRotationShockModel({})
    
    def test_model_initialization(self):
        """Test model initialization with default parameters."""
        self.assertIsInstance(self.model, EarthRotationShockModel)
        self.assertIn('rotation_change_percent', self.model.parameters)
        self.assertIn('baseline_day_length', self.model.parameters)
        self.assertIn('initial_gdp', self.model.parameters)
        self.assertEqual(self.model.parameters['periods'], 50)
        self.assertEqual(self.model.parameters['rotation_change_percent'], 10.0)
        self.assertEqual(self.model.parameters['baseline_day_length'], 24.0)
    
    def test_model_initialization_custom_params(self):
        """Test model initialization with custom parameters."""
        custom_params = {
            'rotation_change_percent': 15.0,
            'periods': 25,
            'gdp_day_night_dependency': 0.4,
            'infrastructure_adaptability': 0.6
        }
        model = EarthRotationShockModel(custom_params)
        
        self.assertEqual(model.parameters['rotation_change_percent'], 15.0)
        self.assertEqual(model.parameters['periods'], 25)
        self.assertEqual(model.parameters['gdp_day_night_dependency'], 0.4)
        self.assertEqual(model.parameters['infrastructure_adaptability'], 0.6)
        # Check that default values are still present
        self.assertIn('agricultural_sensitivity', model.parameters)
    
    def test_simulate_no_rotation_change(self):
        """Test simulation with no rotation change."""
        simulation_config = {
            'shock': {
                'rotation_change_percent': 0.0,
                'adaptation_cost_factor': 1.0,
                'climate_volatility_multiplier': 1.0,
                'agriculture_loss_rate': 0.0,
                'infrastructure_disruption_index': 0.0,
                'start_period': 0
            }
        }
        
        results = self.model.simulate(simulation_config)
        
        self.assertIsInstance(results, dict)
        self.assertIn('periods', results)
        self.assertIn('day_length_hours', results)
        self.assertIn('gdp', results)
        self.assertIn('agricultural_productivity', results)
        self.assertIn('climate_volatility_index', results)
        self.assertIn('summary', results)
        
        # With no rotation change, day length should remain 24 hours
        day_lengths = results['day_length_hours']
        for day_length in day_lengths:
            self.assertAlmostEqual(day_length, 24.0, places=1)
    
    def test_simulate_with_rotation_shock(self):
        """Test simulation with 10% rotation speed increase."""
        simulation_config = {
            'shock': {
                'rotation_change_percent': 10.0,
                'adaptation_cost_factor': 1.5,
                'climate_volatility_multiplier': 1.2,
                'agriculture_loss_rate': 0.7,
                'infrastructure_disruption_index': 0.5,
                'start_period': 0
            }
        }
        
        results = self.model.simulate(simulation_config)
        
        self.assertIsInstance(results, dict)
        self.assertIn('summary', results)
        
        # Check that rotation affects the system
        summary = results['summary']
        self.assertIn('new_day_length_hours', summary)
        self.assertIn('day_length_change_percent', summary)
        self.assertIn('severity_assessment', summary)
        
        # Day length should be shorter (21.6 hours for 10% increase)
        expected_day_length = 24 / 1.1  # 21.818... hours
        self.assertAlmostEqual(summary['new_day_length_hours'], expected_day_length, places=1)
        
        # Day length change should be negative (shorter days)
        self.assertLess(summary['day_length_change_percent'], 0)
    
    def test_summary_statistics(self):
        """Test that summary statistics are calculated correctly."""
        simulation_config = {
            'shock': {
                'rotation_change_percent': 5.0,  # Smaller shock for testing
                'adaptation_cost_factor': 1.2,
                'climate_volatility_multiplier': 1.1,
                'agriculture_loss_rate': 0.5,
                'infrastructure_disruption_index': 0.3,
                'start_period': 0
            }
        }
        
        results = self.model.simulate(simulation_config)
        summary = results['summary']
        
        # Check that all expected summary fields are present
        expected_fields = [
            'new_day_length_hours', 'day_length_change_percent', 'peak_gdp_decline',
            'total_gdp_loss', 'final_gdp_level', 'min_agricultural_productivity',
            'adaptation_completion_year', 'max_sea_level_shift', 'max_climate_volatility',
            'severity_assessment', 'final_assessment'
        ]
        
        for field in expected_fields:
            self.assertIn(field, summary)
        
        # Check that numeric fields are reasonable
        self.assertGreater(summary['new_day_length_hours'], 20)  # Should be > 20 hours
        self.assertLess(summary['new_day_length_hours'], 24)     # Should be < 24 hours
        self.assertGreaterEqual(summary['adaptation_completion_year'], 0)


class TestSimpleEarthRotationFunction(unittest.TestCase):
    """Test cases for the simple Earth rotation shock function."""
    
    def test_simple_function_basic(self):
        """Test the simple Earth rotation shock function with basic inputs."""
        result = simulate_earth_rotation_shock(
            rotation_change_percent=10.0,
            initial_gdp=100_000_000_000_000,  # $100T
            gdp_day_night_dependency=0.3,
            infrastructure_adaptability=0.5,
            agricultural_sensitivity=0.7,
            climate_volatility_multiplier=1.2
        )
        
        self.assertIsInstance(result, dict)
        self.assertIn('new_day_length_hours', result)
        self.assertIn('initial_gdp_loss', result)
        self.assertIn('long_term_gdp_loss', result)
        self.assertIn('adaptation_time_years', result)
        self.assertIn('sea_level_shift_meters', result)
        self.assertIn('climate_volatility_index', result)
        self.assertIn('labor_productivity_change', result)
        self.assertIn('circadian_stress_index', result)
        self.assertIn('sea_wave_intensity_change', result)
        self.assertIn('population_drop_percent', result)
        
        # Check calculations
        expected_day_length = 24 / 1.1  # 21.818... hours
        self.assertAlmostEqual(result['new_day_length_hours'], expected_day_length, places=1)
        
        # GDP impact should be negative
        self.assertGreater(result['initial_gdp_loss'], 0)
        self.assertGreater(result['long_term_gdp_loss'], 0)
        
        # Labor productivity should decrease
        self.assertLess(result['labor_productivity_change'], 0)
        
        # Climate volatility should increase
        self.assertGreater(result['climate_volatility_index'], 1.0)
    
    def test_rotation_speed_scaling(self):
        """Test that larger rotation changes have proportionally larger impacts."""
        # Small rotation change
        result_small = simulate_earth_rotation_shock(
            rotation_change_percent=5.0,
            initial_gdp=100_000_000_000_000,
            gdp_day_night_dependency=0.3,
            infrastructure_adaptability=0.5,
            agricultural_sensitivity=0.7,
            climate_volatility_multiplier=1.2
        )
        
        # Large rotation change
        result_large = simulate_earth_rotation_shock(
            rotation_change_percent=20.0,
            initial_gdp=100_000_000_000_000,
            gdp_day_night_dependency=0.3,
            infrastructure_adaptability=0.5,
            agricultural_sensitivity=0.7,
            climate_volatility_multiplier=1.2
        )
        
        # Large change should have worse impacts
        self.assertGreater(result_large['initial_gdp_loss'], result_small['initial_gdp_loss'])
        self.assertGreater(result_large['adaptation_time_years'], result_small['adaptation_time_years'])
        self.assertGreater(result_large['sea_level_shift_meters'], result_small['sea_level_shift_meters'])
        self.assertGreater(result_large['population_drop_percent'], result_small['population_drop_percent'])
    
    def test_day_length_calculation(self):
        """Test that day length calculations are correct."""
        # 10% faster rotation should give 21.818... hour days
        result_10 = simulate_earth_rotation_shock(10.0, 100e12, 0.3, 0.5, 0.7, 1.2)
        expected_10 = 24 / 1.1
        self.assertAlmostEqual(result_10['new_day_length_hours'], expected_10, places=2)
        
        # 50% faster rotation should give 16 hour days
        result_50 = simulate_earth_rotation_shock(50.0, 100e12, 0.3, 0.5, 0.7, 1.2)
        expected_50 = 24 / 1.5
        self.assertAlmostEqual(result_50['new_day_length_hours'], expected_50, places=2)
        
        # 100% faster rotation should give 12 hour days
        result_100 = simulate_earth_rotation_shock(100.0, 100e12, 0.3, 0.5, 0.7, 1.2)
        expected_100 = 24 / 2.0
        self.assertAlmostEqual(result_100['new_day_length_hours'], expected_100, places=2)


class TestEarthRotationShock(unittest.TestCase):
    """Test cases for EarthRotationShock dataclass."""
    
    def test_shock_creation(self):
        """Test creating an Earth rotation shock."""
        shock = EarthRotationShock(
            rotation_change_percent=10.0,
            adaptation_cost_factor=1.5,
            climate_volatility_multiplier=1.2,
            agriculture_loss_rate=0.7,
            infrastructure_disruption_index=0.5
        )
        
        self.assertEqual(shock.rotation_change_percent, 10.0)
        self.assertEqual(shock.adaptation_cost_factor, 1.5)
        self.assertEqual(shock.climate_volatility_multiplier, 1.2)
        self.assertEqual(shock.agriculture_loss_rate, 0.7)
        self.assertEqual(shock.infrastructure_disruption_index, 0.5)
        self.assertEqual(shock.start_period, 0)  # Default value
    
    def test_shock_creation_with_start_period(self):
        """Test creating a shock with custom start period."""
        shock = EarthRotationShock(
            rotation_change_percent=15.0,
            adaptation_cost_factor=2.0,
            climate_volatility_multiplier=1.5,
            agriculture_loss_rate=0.8,
            infrastructure_disruption_index=0.6,
            start_period=5
        )
        
        self.assertEqual(shock.rotation_change_percent, 15.0)
        self.assertEqual(shock.adaptation_cost_factor, 2.0)
        self.assertEqual(shock.climate_volatility_multiplier, 1.5)
        self.assertEqual(shock.agriculture_loss_rate, 0.8)
        self.assertEqual(shock.infrastructure_disruption_index, 0.6)
        self.assertEqual(shock.start_period, 5)


class TestEarthRotationIntegration(unittest.TestCase):
    """Integration tests for Earth rotation shock model."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.engine = SimulationEngine()
        self.earth_rotation_scenario = {
            'model': 'earth_rotation_shock',
            'parameters': {
                'periods': 20,
                'rotation_change_percent': 8.0
            },
            'simulation': {
                'shock': {
                    'rotation_change_percent': 8.0,
                    'adaptation_cost_factor': 1.3,
                    'climate_volatility_multiplier': 1.15,
                    'agriculture_loss_rate': 0.6,
                    'infrastructure_disruption_index': 0.4,
                    'start_period': 0
                }
            }
        }
    
    def test_model_loads_and_runs(self):
        """Test that the model loads and runs successfully."""
        self.assertIn('earth_rotation_shock', self.engine.models)
        self.assertEqual(self.engine.models['earth_rotation_shock'], EarthRotationShockModel)
        
        # Run simulation
        results = self.engine.run_simulation(self.earth_rotation_scenario)
        
        # Verify structure
        self.assertIn('model', results)
        self.assertIn('scenario', results)
        self.assertIn('results', results)
        self.assertIn('metadata', results)
        
        # Verify content
        self.assertEqual(results['model'], 'earth_rotation_shock')
        self.assertEqual(len(results['results']['periods']), 20)
    
    def test_outputs_match_expected_pattern(self):
        """Test that outputs follow expected patterns."""
        results = self.engine.run_simulation(self.earth_rotation_scenario)
        simulation_results = results['results']
        
        # Check time series exist
        self.assertIn('day_length_hours', simulation_results)
        self.assertIn('gdp', simulation_results)
        self.assertIn('agricultural_productivity', simulation_results)
        self.assertIn('climate_volatility_index', simulation_results)
        
        # Check that day length changes
        day_lengths = simulation_results['day_length_hours']
        self.assertLess(day_lengths[-1], 24.0)  # Should be shorter than 24 hours
        
        # Check that agricultural productivity decreases
        ag_productivity = simulation_results['agricultural_productivity']
        self.assertLess(ag_productivity[10], 1.0)  # Should decrease from baseline
    
    def test_gdp_impact_is_negative(self):
        """Test that GDP impact is negative as expected."""
        results = self.engine.run_simulation(self.earth_rotation_scenario)
        summary = results['results']['summary']
        
        # GDP should decline initially
        self.assertLess(summary['peak_gdp_decline'], 0)
        self.assertGreater(summary['total_gdp_loss'], 0)
        # Check that there was some negative impact during the simulation
        self.assertGreater(summary['total_gdp_loss'], 0)  # Should have some GDP loss during the shock
    
    def test_adaptation_time_estimated_properly(self):
        """Test that adaptation time is estimated within reasonable bounds."""
        results = self.engine.run_simulation(self.earth_rotation_scenario)
        summary = results['results']['summary']
        
        # Adaptation should take some time but not be infinite
        self.assertGreaterEqual(summary['adaptation_completion_year'], 5)   # At least 5 years
        self.assertLessEqual(summary['adaptation_completion_year'], 50)     # At most 50 years
        
        # Final assessment should include adaptation time
        final_assessment = summary['final_assessment']
        self.assertIn('adaptation_time_years', final_assessment)
        self.assertGreater(final_assessment['adaptation_time_years'], 0)


if __name__ == '__main__':
    # Set up logging to suppress info messages during tests
    import logging
    logging.getLogger().setLevel(logging.WARNING)
    
    # Run the tests
    unittest.main() 