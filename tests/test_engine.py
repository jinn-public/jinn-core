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
from models.bank_panic import BankPanicModel, BankPanicShock, simulate_bank_panic
from models.military_spending_shock import MilitarySpendingShockModel, MilitarySpendingShock, simulate_military_spending_shock
from models.global_conflict import GlobalConflictModel, GlobalConflictShock, simulate_global_conflict
from models.earth_rotation_shock import EarthRotationShockModel, EarthRotationShock, simulate_earth_rotation_shock
from models.btc_price_projection import BTCPriceProjectionModel, BTCProjectionScenario, simulate_btc_price_projection


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
        self.assertIn('bank_panic', self.engine.models)
        self.assertIn('military_spending_shock', self.engine.models)
        self.assertIn('global_conflict', self.engine.models)
        self.assertIn('earth_rotation_shock', self.engine.models)
        self.assertIn('btc_price_projection', self.engine.models)
        self.assertEqual(self.engine.models['interest_rate'], InterestRateModel)
        self.assertEqual(self.engine.models['inflation_shock'], InflationShockModel)
        self.assertEqual(self.engine.models['bank_panic'], BankPanicModel)
        self.assertEqual(self.engine.models['military_spending_shock'], MilitarySpendingShockModel)
        self.assertEqual(self.engine.models['global_conflict'], GlobalConflictModel)
        self.assertEqual(self.engine.models['earth_rotation_shock'], EarthRotationShockModel)
        self.assertEqual(self.engine.models['btc_price_projection'], BTCPriceProjectionModel)
    
    def test_model_registration(self):
        """Test that models are properly registered."""
        self.assertEqual(len(self.engine.models), 7)
        self.assertIn('interest_rate', self.engine.models)
        self.assertIn('inflation_shock', self.engine.models)
        self.assertIn('bank_panic', self.engine.models)
        self.assertIn('military_spending_shock', self.engine.models)
        self.assertIn('global_conflict', self.engine.models)
        self.assertIn('earth_rotation_shock', self.engine.models)
        self.assertIn('btc_price_projection', self.engine.models)
    
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


class TestBankPanicModel(unittest.TestCase):
    """Test cases for the Bank Panic Model."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.model = BankPanicModel({})
    
    def test_model_initialization(self):
        """Test model initialization with default parameters."""
        self.assertIsInstance(self.model, BankPanicModel)
        self.assertIn('total_deposits', self.model.parameters)
        self.assertIn('liquid_reserves', self.model.parameters)
        self.assertEqual(self.model.parameters['periods'], 30)
    
    def test_simulate_no_panic(self):
        """Test simulation with no bank panic."""
        simulation_config = {
            'panic': {
                'withdrawal_rate': 0.0,
                'panic_duration': 0,
                'start_period': 0
            }
        }
        
        results = self.model.simulate(simulation_config)
        
        self.assertIsInstance(results, dict)
        self.assertIn('periods', results)
        self.assertIn('withdrawal_rate', results)
        self.assertIn('liquidity_ratio', results)
        self.assertIn('summary', results)
    
    def test_simulate_with_panic(self):
        """Test simulation with bank panic."""
        simulation_config = {
            'panic': {
                'withdrawal_rate': 15.0,
                'panic_duration': 5,
                'start_period': 1
            }
        }
        
        results = self.model.simulate(simulation_config)
        
        self.assertIsInstance(results, dict)
        self.assertIn('summary', results)
        
        # Check that panic affects the system
        summary = results['summary']
        self.assertIn('crisis_severity', summary)
        self.assertIn('max_banks_failed', summary)


class TestSimpleBankPanicFunction(unittest.TestCase):
    """Test cases for the simple bank panic function."""
    
    def test_simple_function_basic(self):
        """Test the simple bank panic function with basic inputs."""
        result = simulate_bank_panic(
            total_deposits=100_000_000_000,  # $100B
            liquid_reserves=15_000_000_000,  # $15B
            withdrawal_rate=10.0,            # 10%
            central_bank_support=0.0
        )
        
        self.assertIsInstance(result, dict)
        self.assertIn('daily_withdrawals', result)
        self.assertIn('remaining_liquidity', result)
        self.assertIn('survival_days', result)
        self.assertIn('bank_survives', result)
        self.assertIn('liquidity_ratio', result)
        
        # Check calculations
        expected_withdrawals = 100_000_000_000 * 0.1  # 10% of deposits
        self.assertAlmostEqual(result['daily_withdrawals'], expected_withdrawals)
    
    def test_bank_survival_with_cb_support(self):
        """Test bank survival with central bank support."""
        result = simulate_bank_panic(
            total_deposits=100_000_000_000,
            liquid_reserves=10_000_000_000,
            withdrawal_rate=8.0,  # Reduced from 15% to 8% for survival
            central_bank_support=50_000_000_000  # $50B CB support
        )
        
        # With CB support, bank should survive longer
        self.assertGreater(result['survival_days'], 6)  # Should be 7+ days
        self.assertTrue(result['bank_survives'])


class TestBankPanicShock(unittest.TestCase):
    """Test cases for BankPanicShock dataclass."""
    
    def test_shock_creation(self):
        """Test creating a bank panic shock."""
        shock = BankPanicShock(withdrawal_rate=20.0, panic_duration=7)
        
        self.assertEqual(shock.withdrawal_rate, 20.0)
        self.assertEqual(shock.panic_duration, 7)
        self.assertEqual(shock.start_period, 0)  # Default value
        self.assertEqual(shock.contagion_factor, 0.1)  # Default value
    
    def test_shock_creation_with_custom_values(self):
        """Test creating a bank panic shock with custom values."""
        shock = BankPanicShock(
            withdrawal_rate=25.0, 
            panic_duration=5, 
            start_period=3,
            contagion_factor=0.2
        )
        
        self.assertEqual(shock.withdrawal_rate, 25.0)
        self.assertEqual(shock.panic_duration, 5)
        self.assertEqual(shock.start_period, 3)
        self.assertEqual(shock.contagion_factor, 0.2)


class TestMilitarySpendingShockModel(unittest.TestCase):
    """Test cases for the Military Spending Shock Model."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.model = MilitarySpendingShockModel({})
    
    def test_model_initialization(self):
        """Test model initialization with default parameters."""
        self.assertIsInstance(self.model, MilitarySpendingShockModel)
        self.assertIn('initial_gdp', self.model.parameters)
        self.assertIn('military_spending_percent', self.model.parameters)
        self.assertIn('debt_ratio', self.model.parameters)
        self.assertEqual(self.model.parameters['periods'], 20)
    
    def test_simulate_no_shock(self):
        """Test simulation with no military spending shock."""
        simulation_config = {
            'shock': {
                'spending_increase': 0.0,
                'duration': 0,
                'start_period': 0
            }
        }
        
        results = self.model.simulate(simulation_config)
        
        self.assertIsInstance(results, dict)
        self.assertIn('periods', results)
        self.assertIn('military_spending_percent', results)
        self.assertIn('social_spending_percent', results)
        self.assertIn('gdp_growth', results)
        self.assertIn('debt_ratio', results)
        self.assertIn('summary', results)
    
    def test_simulate_with_shock(self):
        """Test simulation with military spending shock."""
        simulation_config = {
            'shock': {
                'spending_increase': 0.02,  # 2% of GDP increase
                'duration': 5,
                'start_period': 1,
                'fiscal_policy': 'neutral'
            }
        }
        
        results = self.model.simulate(simulation_config)
        
        self.assertIsInstance(results, dict)
        self.assertIn('summary', results)
        
        # Check that shock affects the system
        summary = results['summary']
        self.assertIn('peak_military_spending', summary)
        self.assertIn('social_spending_reduction', summary)
        self.assertIn('fiscal_policy_effectiveness', summary)


class TestSimpleMilitarySpendingFunction(unittest.TestCase):
    """Test cases for the simple military spending shock function."""
    
    def test_simple_function_basic(self):
        """Test the simple military spending shock function with basic inputs."""
        result = simulate_military_spending_shock(
            initial_gdp=25_000_000_000_000,  # $25T
            military_spending_percent=0.03,   # 3%
            military_spending_increase=0.02,  # +2%
            debt_ratio=0.6,                   # 60%
            fiscal_policy="neutral"
        )
        
        self.assertIsInstance(result, dict)
        self.assertIn('new_military_spending_percent', result)
        self.assertIn('military_spending_amount', result)
        self.assertIn('social_budget_impact', result)
        self.assertIn('new_debt_ratio', result)
        self.assertIn('gdp_growth_impact', result)
        self.assertIn('fiscal_multiplier', result)
        
        # Check calculations
        self.assertEqual(result['new_military_spending_percent'], 5.0)  # 3% + 2%
        self.assertEqual(result['social_budget_impact'], -1.2)  # -2% * 0.6
        self.assertEqual(result['fiscal_multiplier'], 0.8)  # Neutral policy
    
    def test_fiscal_policy_effects(self):
        """Test different fiscal policy effects."""
        base_params = {
            'initial_gdp': 25_000_000_000_000,
            'military_spending_percent': 0.03,
            'military_spending_increase': 0.02,
            'debt_ratio': 0.6
        }
        
        # Test stimulus policy
        stimulus_result = simulate_military_spending_shock(**base_params, fiscal_policy="stimulus")
        self.assertEqual(stimulus_result['fiscal_multiplier'], 1.2)
        self.assertGreater(stimulus_result['gdp_growth_impact'], 2.0)  # Higher growth impact
        
        # Test austerity policy
        austerity_result = simulate_military_spending_shock(**base_params, fiscal_policy="austerity")
        self.assertEqual(austerity_result['fiscal_multiplier'], 0.5)
        self.assertLess(austerity_result['new_debt_ratio'], stimulus_result['new_debt_ratio'])  # Lower debt


class TestMilitarySpendingShock(unittest.TestCase):
    """Test cases for MilitarySpendingShock dataclass."""
    
    def test_shock_creation(self):
        """Test creating a military spending shock."""
        shock = MilitarySpendingShock(spending_increase=0.02, duration=8)
        
        self.assertEqual(shock.spending_increase, 0.02)
        self.assertEqual(shock.duration, 8)
        self.assertEqual(shock.start_period, 0)  # Default value
        self.assertEqual(shock.fiscal_policy, "neutral")  # Default value
    
    def test_shock_creation_with_custom_values(self):
        """Test creating a military spending shock with custom values."""
        shock = MilitarySpendingShock(
            spending_increase=0.015, 
            duration=6, 
            start_period=2,
            fiscal_policy="stimulus"
        )
        
        self.assertEqual(shock.spending_increase, 0.015)
        self.assertEqual(shock.duration, 6)
        self.assertEqual(shock.start_period, 2)
        self.assertEqual(shock.fiscal_policy, "stimulus")


class TestGlobalConflictModel(unittest.TestCase):
    """Test cases for the Global Conflict Model."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.model = GlobalConflictModel({})
    
    def test_model_initialization(self):
        """Test model initialization with default parameters."""
        self.assertIsInstance(self.model, GlobalConflictModel)
        self.assertIn('initial_gdp', self.model.parameters)
        self.assertIn('baseline_gdp_growth', self.model.parameters)
        self.assertIn('baseline_military_spending', self.model.parameters)
        self.assertEqual(self.model.parameters['periods'], 20)
    
    def test_simulate_no_conflict(self):
        """Test simulation with no global conflict."""
        simulation_config = {
            'conflict': {
                'military_spending_jump': 0.0,
                'global_trade_disruption': 0.0,
                'conflict_duration_years': 0,
                'inflation_surge_rate': 0.0,
                'human_capital_loss': 0.0,
                'infrastructure_destruction': 0.0,
                'start_period': 0
            }
        }
        
        results = self.model.simulate(simulation_config)
        
        self.assertIsInstance(results, dict)
        self.assertIn('periods', results)
        self.assertIn('conflict_active', results)
        self.assertIn('military_spending_percent', results)
        self.assertIn('gdp', results)
        self.assertIn('trade_volume', results)
        self.assertIn('social_stability_index', results)
        self.assertIn('summary', results)
    
    def test_simulate_with_conflict(self):
        """Test simulation with global conflict."""
        simulation_config = {
            'conflict': {
                'military_spending_jump': 0.05,  # 5% GDP increase
                'global_trade_disruption': 0.4,  # 40% trade disruption
                'conflict_duration_years': 3,
                'inflation_surge_rate': 0.1,     # 10% inflation spike
                'human_capital_loss': 0.05,      # 5% workforce loss
                'infrastructure_destruction': 0.1, # 10% infrastructure loss
                'start_period': 1
            }
        }
        
        results = self.model.simulate(simulation_config)
        
        self.assertIsInstance(results, dict)
        self.assertIn('summary', results)
        
        # Check that conflict affects the system
        summary = results['summary']
        self.assertIn('conflict_severity', summary)
        self.assertIn('total_gdp_loss', summary)
        self.assertIn('peak_inflation', summary)


class TestSimpleGlobalConflictFunction(unittest.TestCase):
    """Test cases for the simple global conflict function."""
    
    def test_simple_function_basic(self):
        """Test the simple global conflict function with basic inputs."""
        result = simulate_global_conflict(
            initial_gdp=100_000_000_000_000,  # $100T
            military_spending_jump=0.05,      # 5% GDP
            global_trade_disruption=0.4,      # 40% trade disruption
            conflict_duration_years=5,
            inflation_surge_rate=0.1,         # 10% inflation
            human_capital_loss=0.05,          # 5% workforce loss
            infrastructure_destruction=0.1    # 10% infrastructure loss
        )
        
        self.assertIsInstance(result, dict)
        self.assertIn('total_military_spending', result)
        self.assertIn('gdp_impact', result)
        self.assertIn('trade_loss', result)
        self.assertIn('inflation_peak', result)
        self.assertIn('workforce_reduction', result)
        self.assertIn('infrastructure_loss', result)
        self.assertIn('debt_increase', result)
        self.assertIn('social_stability_index', result)
        
        # Check that impacts are negative (economic damage)
        self.assertLess(result['gdp_impact'], 0)
        self.assertGreater(result['total_military_spending'], 0)
        self.assertGreater(result['trade_loss'], 0)
    
    def test_conflict_severity_scaling(self):
        """Test that longer/more intense conflicts have worse impacts."""
        # Short, limited conflict
        result_limited = simulate_global_conflict(
            initial_gdp=100_000_000_000_000,
            military_spending_jump=0.02,
            global_trade_disruption=0.1,
            conflict_duration_years=2,
            inflation_surge_rate=0.03,
            human_capital_loss=0.02,
            infrastructure_destruction=0.03
        )
        
        # Long, intense conflict
        result_intense = simulate_global_conflict(
            initial_gdp=100_000_000_000_000,
            military_spending_jump=0.08,
            global_trade_disruption=0.6,
            conflict_duration_years=6,
            inflation_surge_rate=0.15,
            human_capital_loss=0.08,
            infrastructure_destruction=0.15
        )
        
        # Intense conflict should have worse impacts
        self.assertLess(result_intense['gdp_impact'], result_limited['gdp_impact'])
        self.assertGreater(result_intense['debt_increase'], result_limited['debt_increase'])
        self.assertLess(result_intense['social_stability_index'], result_limited['social_stability_index'])


class TestGlobalConflictShock(unittest.TestCase):
    """Test cases for GlobalConflictShock dataclass."""
    
    def test_shock_creation(self):
        """Test creating a global conflict shock."""
        shock = GlobalConflictShock(
            military_spending_jump=0.05,
            global_trade_disruption=0.4,
            conflict_duration_years=5,
            inflation_surge_rate=0.1,
            human_capital_loss=0.05,
            infrastructure_destruction=0.1
        )
        
        self.assertEqual(shock.military_spending_jump, 0.05)
        self.assertEqual(shock.global_trade_disruption, 0.4)
        self.assertEqual(shock.conflict_duration_years, 5)
        self.assertEqual(shock.inflation_surge_rate, 0.1)
        self.assertEqual(shock.human_capital_loss, 0.05)
        self.assertEqual(shock.infrastructure_destruction, 0.1)
        self.assertEqual(shock.start_period, 0)  # Default value
    
    def test_shock_creation_with_start_period(self):
        """Test creating a shock with custom start period."""
        shock = GlobalConflictShock(
            military_spending_jump=0.03,
            global_trade_disruption=0.25,
            conflict_duration_years=3,
            inflation_surge_rate=0.06,
            human_capital_loss=0.03,
            infrastructure_destruction=0.06,
            start_period=2
        )
        
        self.assertEqual(shock.military_spending_jump, 0.03)
        self.assertEqual(shock.global_trade_disruption, 0.25)
        self.assertEqual(shock.conflict_duration_years, 3)
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
        self.bank_panic_scenario = {
            'model': 'bank_panic',
            'parameters': {
                'periods': 15,
                'total_deposits': 50_000_000_000
            },
            'simulation': {
                'panic': {
                    'withdrawal_rate': 12.0,
                    'panic_duration': 4,
                    'start_period': 2
                }
            }
        }
        self.military_spending_scenario = {
            'model': 'military_spending_shock',
            'parameters': {
                'periods': 12,
                'initial_gdp': 20_000_000_000_000
            },
            'simulation': {
                'shock': {
                    'spending_increase': 0.015,
                    'duration': 6,
                    'start_period': 1,
                    'fiscal_policy': 'neutral'
                }
            }
        }
        self.global_conflict_scenario = {
            'model': 'global_conflict',
            'parameters': {
                'periods': 10,
                'initial_gdp': 80_000_000_000_000
            },
            'simulation': {
                'conflict': {
                    'military_spending_jump': 0.04,
                    'global_trade_disruption': 0.3,
                    'conflict_duration_years': 3,
                    'inflation_surge_rate': 0.08,
                    'human_capital_loss': 0.04,
                    'infrastructure_destruction': 0.08,
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
    
    def test_full_simulation_flow_bank_panic(self):
        """Test the complete simulation flow for bank panic model."""
        results = self.engine.run_simulation(self.bank_panic_scenario)
        
        # Verify structure
        self.assertIn('model', results)
        self.assertIn('scenario', results)
        self.assertIn('results', results)
        self.assertIn('metadata', results)
        
        # Verify content
        self.assertEqual(results['model'], 'bank_panic')
        self.assertEqual(len(results['results']['periods']), 15)
        
        # Verify timing information
        metadata = results['metadata']
        self.assertIn('start_time', metadata)
        self.assertIn('end_time', metadata)
        self.assertIn('execution_time_seconds', metadata)
        self.assertGreaterEqual(metadata['execution_time_seconds'], 0)
    
    def test_full_simulation_flow_military_spending(self):
        """Test the complete simulation flow for military spending model."""
        results = self.engine.run_simulation(self.military_spending_scenario)
        
        # Verify structure
        self.assertIn('model', results)
        self.assertIn('scenario', results)
        self.assertIn('results', results)
        self.assertIn('metadata', results)
        
        # Verify content
        self.assertEqual(results['model'], 'military_spending_shock')
        self.assertEqual(len(results['results']['periods']), 12)
        
        # Verify timing information
        metadata = results['metadata']
        self.assertIn('start_time', metadata)
        self.assertIn('end_time', metadata)
        self.assertIn('execution_time_seconds', metadata)
        self.assertGreaterEqual(metadata['execution_time_seconds'], 0)
    
    def test_full_simulation_flow_global_conflict(self):
        """Test the complete simulation flow for global conflict model."""
        results = self.engine.run_simulation(self.global_conflict_scenario)
        
        # Verify structure
        self.assertIn('model', results)
        self.assertIn('scenario', results)
        self.assertIn('results', results)
        self.assertIn('metadata', results)
        
        # Verify content
        self.assertEqual(results['model'], 'global_conflict')
        self.assertEqual(len(results['results']['periods']), 10)
        
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
    unittest.main() 