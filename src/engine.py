"""
Jinn-Core: Economic Simulation Engine

Main simulation engine for running economic models and scenarios.
"""

import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

try:
    # Try relative imports first (when used as a module)
    from .models.interest_rate import InterestRateModel
    from .models.inflation_shock import InflationShockModel
    from .models.bank_panic import BankPanicModel
    from .models.military_spending_shock import MilitarySpendingShockModel
    from .models.global_conflict import GlobalConflictModel
    from .models.earth_rotation_shock import EarthRotationShockModel
    from .models.btc_price_projection import BTCPriceProjectionModel
    from .models.ai_unemployment_shock import AIUnemploymentShockModel
    from .models.plastic_spread_simulation import PlasticSpreadSimulationModel
    from .models.geopolitical_land_analyst import GeopoliticalLandAnalyst
    from .models.crypto_panic import CryptoPanicModel
except ImportError:
    # Fall back to absolute imports (when used from tests)
    from models.interest_rate import InterestRateModel
    from models.inflation_shock import InflationShockModel
    from models.bank_panic import BankPanicModel
    from models.military_spending_shock import MilitarySpendingShockModel
    from models.global_conflict import GlobalConflictModel
    from models.earth_rotation_shock import EarthRotationShockModel
    from models.btc_price_projection import BTCPriceProjectionModel
    from models.ai_unemployment_shock import AIUnemploymentShockModel
    from models.plastic_spread_simulation import PlasticSpreadSimulationModel
    from models.geopolitical_land_analyst import GeopoliticalLandAnalyst
    from models.crypto_panic import CryptoPanicModel

logger = logging.getLogger(__name__)


class SimulationEngine:
    """Main simulation engine for economic modeling."""
    
    def __init__(self):
        """Initialize the simulation engine."""
        self.models = {}
        self.scenarios = {}
        self.results = {}
        self._register_models()
    
    def _register_models(self):
        """Register available economic models."""
        self.models['interest_rate'] = InterestRateModel
        self.models['inflation_shock'] = InflationShockModel
        self.models['bank_panic'] = BankPanicModel
        self.models['military_spending_shock'] = MilitarySpendingShockModel
        self.models['global_conflict'] = GlobalConflictModel
        self.models['earth_rotation_shock'] = EarthRotationShockModel
        self.models['btc_price_projection'] = BTCPriceProjectionModel
        self.models['ai_unemployment_shock'] = AIUnemploymentShockModel
        self.models['plastic_spread_simulation'] = PlasticSpreadSimulationModel
        self.models['geopolitical_land_analyst'] = GeopoliticalLandAnalyst
        self.models['crypto_panic'] = CryptoPanicModel
        logger.info(f"Registered {len(self.models)} economic models")
    
    def load_scenario(self, scenario_path: str) -> Dict[str, Any]:
        """
        Load a scenario from a JSON file.
        
        Args:
            scenario_path: Path to the scenario JSON file
            
        Returns:
            Dict containing scenario configuration
        """
        try:
            with open(scenario_path, 'r') as f:
                scenario = json.load(f)
            logger.info(f"Loaded scenario from {scenario_path}")
            return scenario
        except Exception as e:
            logger.error(f"Failed to load scenario from {scenario_path}: {e}")
            raise
    
    def run_simulation(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run a simulation based on the provided scenario.
        
        Args:
            scenario: Dictionary containing scenario configuration
            
        Returns:
            Dictionary containing simulation results
        """
        model_name = scenario.get('model')
        if model_name not in self.models:
            raise ValueError(f"Unknown model: {model_name}")
        
        # Initialize the model
        model_class = self.models[model_name]
        model = model_class(scenario.get('parameters', {}))
        
        # Run the simulation
        logger.info(f"Running simulation with {model_name} model")
        start_time = datetime.now()
        
        results = model.simulate(scenario.get('simulation', {}))
        
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        
        # Package results
        simulation_results = {
            'model': model_name,
            'scenario': scenario,
            'results': results,
            'metadata': {
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat(),
                'execution_time_seconds': execution_time
            }
        }
        
        logger.info(f"Simulation completed in {execution_time:.2f} seconds")
        return simulation_results
    
    def run_scenario_file(self, scenario_path: str) -> Dict[str, Any]:
        """
        Load and run a scenario from a file.
        
        Args:
            scenario_path: Path to the scenario JSON file
            
        Returns:
            Dictionary containing simulation results
        """
        scenario = self.load_scenario(scenario_path)
        return self.run_simulation(scenario)


if __name__ == "__main__":
    # Basic test run
    logging.basicConfig(level=logging.INFO)
    
    engine = SimulationEngine()
    print("Jinn-Core Economic Simulation Engine initialized")
    print(f"Available models: {list(engine.models.keys())}") 