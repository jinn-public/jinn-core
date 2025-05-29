"""
Cosmic Consciousness Timing Model

Astronomical model for simulating the emergence of intelligent life and the available 
window for interplanetary expansion before planetary extinction.

Key factors:
- Evolution duration for consciousness to emerge
- Remaining time before planetary extinction
- Time needed to reach another planet after consciousness
- Risk tolerance of civilizations
- Kardashev Scale technological advancement levels
"""

import numpy as np
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# Kardashev Scale definitions
KARDASHEV_SCALE = {
    0.0: {"name": "Primitive", "energy": 1e12, "description": "Basic tool use, fire"},
    0.5: {"name": "Pre-industrial", "energy": 1e14, "description": "Pre-fossil energy, small cities"},
    0.73: {"name": "Modern Humans", "energy": 2e16, "description": "Current Earth state (approx 2025)"},
    1.0: {"name": "Type I", "energy": 1.74e17, "description": "Full use of Earth's energy (~global sustainability)"},
    1.5: {"name": "Planetary-AI Hybrid", "energy": 1e18, "description": "AI-managed infrastructure, advanced fusion"},
    2.0: {"name": "Type II", "energy": 3.86e26, "description": "Harnessing the Sun's full power (e.g. Dyson Sphere)"},
    3.0: {"name": "Type III", "energy": 1e36, "description": "Control over galaxy-scale energy"}
}


@dataclass
class CosmicTimingScenario:
    """Configuration for a cosmic consciousness timing scenario."""
    evolution_duration_factor: float  # Multiplier for baseline evolution time (e.g., 1.05 for +5%)
    window_needed: float  # Time needed to reach another planet (billions of years)
    risk_tolerance: float  # How close to extinction threshold civilization operates (0-1)
    random_delay: bool = False  # Whether to add random delays
    # Kardashev Scale parameters
    starting_kardashev_level: float = 0.0  # Initial Kardashev level when consciousness emerges
    kardashev_growth_rate: float = 0.1  # Kardashev level increase per billion years
    kardashev_enabled: bool = True  # Whether to use Kardashev scaling


def estimate_kardashev_progress(start_level: float, growth_rate: float, years: float) -> float:
    """
    Estimate Kardashev level progression over time.
    
    Args:
        start_level: Starting Kardashev level
        growth_rate: Growth rate per billion years
        years: Time elapsed in billions of years
        
    Returns:
        Final Kardashev level (capped at 3.0)
    """
    # Exponential growth model with diminishing returns
    if start_level >= 3.0:
        return 3.0
    
    # Growth becomes slower at higher levels
    effective_growth = growth_rate * (3.0 - start_level) / 3.0
    final_level = start_level + (effective_growth * years)
    
    return min(final_level, 3.0)


def get_kardashev_expansion_multiplier(kardashev_level: float) -> float:
    """
    Calculate expansion capability multiplier based on Kardashev level.
    
    Args:
        kardashev_level: Current Kardashev level
        
    Returns:
        Multiplier for expansion speed (lower = faster expansion)
    """
    if kardashev_level < 0.5:
        return 2.0  # Primitive civilizations take much longer
    elif kardashev_level < 1.0:
        return 1.5  # Pre-Type I civilizations still struggle
    elif kardashev_level < 1.5:
        return 1.0  # Type I baseline
    elif kardashev_level < 2.0:
        return 0.7  # Type I+ with AI assistance
    elif kardashev_level < 2.5:
        return 0.3  # Type II civilizations much faster
    else:
        return 0.1  # Type II+ and Type III have near-instantaneous expansion


def get_kardashev_survival_bonus(kardashev_level: float) -> float:
    """
    Calculate survival probability bonus based on Kardashev level.
    
    Args:
        kardashev_level: Current Kardashev level
        
    Returns:
        Additive bonus to expansion probability (0.0 to 0.3)
    """
    if kardashev_level < 0.5:
        return 0.0  # No bonus for primitive civilizations
    elif kardashev_level < 1.0:
        return 0.05  # Small bonus for developing civilizations
    elif kardashev_level < 1.5:
        return 0.15  # Significant bonus for Type I
    elif kardashev_level < 2.0:
        return 0.25  # Large bonus for advanced Type I
    else:
        return 0.3  # Maximum bonus for Type II+


def get_kardashev_level_name(kardashev_level: float) -> str:
    """Get the name/description for a Kardashev level."""
    closest_level = min(KARDASHEV_SCALE.keys(), key=lambda x: abs(x - kardashev_level))
    return KARDASHEV_SCALE[closest_level]["name"]


def simulate_cosmic_consciousness_timing(evolution_duration: float, time_left: float,
                                       window_needed: float, risk_tolerance: float = 0.1,
                                       starting_kardashev_level: float = 0.0,
                                       kardashev_growth_rate: float = 0.1,
                                       kardashev_enabled: bool = True) -> Dict[str, Any]:
    """
    Simple, interpretable function to simulate cosmic consciousness timing with Kardashev Scale.
    
    Args:
        evolution_duration: Time for consciousness to evolve (billions of years)
        time_left: Remaining time before planetary extinction (billions of years)
        window_needed: Time required to reach another planet (billions of years)
        risk_tolerance: Safety margin civilization requires (fraction of time_left)
        starting_kardashev_level: Kardashev level when consciousness emerges
        kardashev_growth_rate: Kardashev level growth per billion years
        kardashev_enabled: Whether to apply Kardashev effects
        
    Returns:
        Dict containing simulation results including Kardashev progression
    """
    # Constants (billions of years)
    UNIVERSE_AGE = 13.8
    EARTH_AGE = 4.5
    
    # When consciousness emerges relative to Earth's formation
    consciousness_emergence_time = evolution_duration
    
    # Available window for expansion
    expansion_window = time_left
    
    # Calculate Kardashev progression if enabled
    if kardashev_enabled and expansion_window > 0:
        # Kardashev level at the end of available expansion window
        final_kardashev_level = estimate_kardashev_progress(
            starting_kardashev_level, kardashev_growth_rate, expansion_window
        )
        
        # Use average Kardashev level during expansion period for calculations
        avg_kardashev_level = (starting_kardashev_level + final_kardashev_level) / 2
        
        # Apply Kardashev effects
        expansion_multiplier = get_kardashev_expansion_multiplier(avg_kardashev_level)
        survival_bonus = get_kardashev_survival_bonus(avg_kardashev_level)
        
        # Adjust window needed based on technological capability
        effective_window_needed = window_needed * expansion_multiplier
    else:
        final_kardashev_level = starting_kardashev_level
        avg_kardashev_level = starting_kardashev_level
        expansion_multiplier = 1.0
        survival_bonus = 0.0
        effective_window_needed = window_needed
    
    # Safety margin required
    safety_margin_needed = time_left * risk_tolerance
    minimum_time_needed = effective_window_needed + safety_margin_needed
    
    # Does civilization succeed?
    civilization_succeeds = expansion_window >= minimum_time_needed
    
    # Actual safety margin achieved
    actual_safety_margin = max(0, expansion_window - effective_window_needed)
    safety_margin_ratio = actual_safety_margin / expansion_window if expansion_window > 0 else 0
    
    # Expansion probability based on available time vs needed time
    if expansion_window <= 0:
        expansion_probability = 0.0
    elif expansion_window >= minimum_time_needed * 2:
        base_probability = 0.95  # High probability with plenty of time
    else:
        # Linear probability between minimum needed and 2x minimum needed
        time_ratio = expansion_window / minimum_time_needed
        base_probability = max(0.0, min(0.95, (time_ratio - 1.0) * 0.95))
    
    # Apply Kardashev survival bonus
    expansion_probability = min(0.99, base_probability + survival_bonus) if kardashev_enabled else base_probability
    
    return {
        'consciousness_emergence_time': consciousness_emergence_time,
        'expansion_window': expansion_window,
        'minimum_time_needed': minimum_time_needed,
        'civilization_succeeds': civilization_succeeds,
        'safety_margin': actual_safety_margin,
        'safety_margin_ratio': safety_margin_ratio,
        'expansion_probability': expansion_probability,
        'window_needed': window_needed,
        'effective_window_needed': effective_window_needed,
        'risk_tolerance': risk_tolerance,
        # Kardashev-specific results
        'kardashev_enabled': kardashev_enabled,
        'starting_kardashev_level': starting_kardashev_level,
        'final_kardashev_level': final_kardashev_level,
        'avg_kardashev_level': avg_kardashev_level,
        'kardashev_growth_rate': kardashev_growth_rate,
        'expansion_multiplier': expansion_multiplier,
        'survival_bonus': survival_bonus,
        'starting_kardashev_name': get_kardashev_level_name(starting_kardashev_level),
        'final_kardashev_name': get_kardashev_level_name(final_kardashev_level)
    }


class CosmicConsciousnessTimingModel:
    """
    Cosmic Consciousness Timing Model with Kardashev Scale Integration
    
    Simulates the emergence of intelligent life and timing constraints for:
    - Evolution of consciousness
    - Window for interplanetary expansion
    - Planetary extinction deadlines
    - Civilization survival probabilities
    - Kardashev Scale technological progression
    - Statistical analysis across multiple scenarios
    """
    
    def __init__(self, parameters: Dict[str, Any]):
        """
        Initialize the Cosmic Consciousness Timing Model.
        
        Args:
            parameters: Model calibration parameters
        """
        self.parameters = self._validate_parameters(parameters)
        logger.info("Cosmic Consciousness Timing Model with Kardashev Scale initialized")
    
    def _validate_parameters(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and set default parameters."""
        defaults = {
            # Cosmic constants (billions of years)
            'universe_age': 13.8,
            'earth_age': 4.5,
            'earth_extinction_time': 0.5,  # Time until Earth becomes uninhabitable
            'baseline_evolution_duration': 4.0,  # Time for consciousness to evolve
            
            # Expansion parameters
            'baseline_window_needed': 0.2,  # Time needed to reach another planet after consciousness
            'baseline_risk_tolerance': 0.1,  # Safety margin civilizations prefer
            
            # Kardashev Scale parameters
            'baseline_starting_kardashev': 0.0,  # Starting Kardashev level
            'baseline_kardashev_growth_rate': 0.15,  # Kardashev growth per billion years
            'kardashev_enabled': True,  # Whether to use Kardashev scaling
            
            # Variation parameters
            'evolution_delay_scenarios': [0.0, 0.05, 0.10, 0.20],  # +0%, +5%, +10%, +20%
            'kardashev_scenarios': [0.0, 0.5, 0.73, 1.0],  # Different starting tech levels
            'random_variation_range': 0.3,  # ±30% random variation for probabilistic runs
            
            # Simulation parameters
            'num_probabilistic_runs': 1000,  # Number of randomized simulations
            'confidence_intervals': [0.25, 0.5, 0.75, 0.9, 0.95],  # Percentiles to report
        }
        
        # Merge with provided parameters
        for key, default_value in defaults.items():
            if key not in params:
                params[key] = default_value
        
        return params
    
    def simulate(self, simulation_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the cosmic consciousness timing simulation with Kardashev Scale.
        
        Args:
            simulation_config: Simulation configuration
            
        Returns:
            Dictionary containing simulation results
        """
        scenario_config = simulation_config.get('scenario', {})
        
        # Parse scenario configuration
        scenario = CosmicTimingScenario(
            evolution_duration_factor=scenario_config.get('evolution_duration_factor', 1.0),
            window_needed=scenario_config.get('window_needed', self.parameters['baseline_window_needed']),
            risk_tolerance=scenario_config.get('risk_tolerance', self.parameters['baseline_risk_tolerance']),
            random_delay=scenario_config.get('random_delay', False),
            starting_kardashev_level=scenario_config.get('starting_kardashev_level', self.parameters['baseline_starting_kardashev']),
            kardashev_growth_rate=scenario_config.get('kardashev_growth_rate', self.parameters['baseline_kardashev_growth_rate']),
            kardashev_enabled=scenario_config.get('kardashev_enabled', self.parameters['kardashev_enabled'])
        )
        
        logger.info(f"Simulating cosmic consciousness timing with Kardashev Scale - "
                   f"Starting K-level: {scenario.starting_kardashev_level:.2f}, "
                   f"Growth rate: {scenario.kardashev_growth_rate:.2f}/Gy")
        
        # Run deterministic scenarios
        deterministic_results = self._run_deterministic_scenarios(scenario)
        
        # Run Kardashev comparison scenarios
        kardashev_comparison = self._run_kardashev_comparison(scenario)
        
        # Run probabilistic scenarios
        probabilistic_results = self._run_probabilistic_scenarios(scenario)
        
        # Calculate summary statistics
        summary = self._calculate_summary(deterministic_results, probabilistic_results, kardashev_comparison)
        
        return {
            'deterministic_scenarios': deterministic_results,
            'kardashev_comparison': kardashev_comparison,
            'probabilistic_scenarios': probabilistic_results,
            'summary': summary,
            'parameters': self.parameters
        }
    
    def _run_deterministic_scenarios(self, scenario: CosmicTimingScenario) -> List[Dict[str, Any]]:
        """Run predefined deterministic scenarios."""
        results = []
        
        baseline_evolution = self.parameters['baseline_evolution_duration']
        time_left = self.parameters['earth_extinction_time']
        
        for delay_factor in self.parameters['evolution_delay_scenarios']:
            evolution_duration = baseline_evolution * (1 + delay_factor)
            
            result = simulate_cosmic_consciousness_timing(
                evolution_duration=evolution_duration,
                time_left=time_left,
                window_needed=scenario.window_needed,
                risk_tolerance=scenario.risk_tolerance,
                starting_kardashev_level=scenario.starting_kardashev_level,
                kardashev_growth_rate=scenario.kardashev_growth_rate,
                kardashev_enabled=scenario.kardashev_enabled
            )
            
            result['scenario_name'] = f"+{delay_factor:.0%} evolution delay"
            result['evolution_delay_factor'] = delay_factor
            result['evolution_duration'] = evolution_duration
            
            results.append(result)
        
        return results
    
    def _run_kardashev_comparison(self, scenario: CosmicTimingScenario) -> List[Dict[str, Any]]:
        """Run scenarios comparing different Kardashev starting levels."""
        results = []
        
        baseline_evolution = self.parameters['baseline_evolution_duration']
        time_left = self.parameters['earth_extinction_time']
        
        for k_level in self.parameters['kardashev_scenarios']:
            result = simulate_cosmic_consciousness_timing(
                evolution_duration=baseline_evolution,
                time_left=time_left,
                window_needed=scenario.window_needed,
                risk_tolerance=scenario.risk_tolerance,
                starting_kardashev_level=k_level,
                kardashev_growth_rate=scenario.kardashev_growth_rate,
                kardashev_enabled=scenario.kardashev_enabled
            )
            
            result['scenario_name'] = f"Kardashev {k_level:.2f} ({get_kardashev_level_name(k_level)})"
            result['kardashev_scenario'] = k_level
            
            results.append(result)
        
        return results
    
    def _run_probabilistic_scenarios(self, scenario: CosmicTimingScenario) -> Dict[str, Any]:
        """Run probabilistic scenarios with random variations."""
        if not scenario.random_delay:
            return {'enabled': False}
        
        num_runs = self.parameters['num_probabilistic_runs']
        baseline_evolution = self.parameters['baseline_evolution_duration']
        time_left = self.parameters['earth_extinction_time']
        variation_range = self.parameters['random_variation_range']
        
        success_rates = []
        expansion_probabilities = []
        safety_margins = []
        evolution_durations = []
        kardashev_progressions = []
        
        for _ in range(num_runs):
            # Random variation in evolution duration
            random_factor = np.random.uniform(-variation_range, variation_range)
            evolution_duration = baseline_evolution * (1 + random_factor)
            
            # Random variation in other parameters
            window_needed = scenario.window_needed * np.random.uniform(0.8, 1.2)
            risk_tolerance = scenario.risk_tolerance * np.random.uniform(0.5, 1.5)
            starting_kardashev = max(0.0, scenario.starting_kardashev_level + np.random.normal(0, 0.1))
            kardashev_growth = max(0.01, scenario.kardashev_growth_rate * np.random.uniform(0.5, 2.0))
            
            result = simulate_cosmic_consciousness_timing(
                evolution_duration=evolution_duration,
                time_left=time_left,
                window_needed=window_needed,
                risk_tolerance=risk_tolerance,
                starting_kardashev_level=starting_kardashev,
                kardashev_growth_rate=kardashev_growth,
                kardashev_enabled=scenario.kardashev_enabled
            )
            
            success_rates.append(1 if result['civilization_succeeds'] else 0)
            expansion_probabilities.append(result['expansion_probability'])
            safety_margins.append(result['safety_margin'])
            evolution_durations.append(evolution_duration)
            kardashev_progressions.append(result['final_kardashev_level'] - result['starting_kardashev_level'])
        
        # Calculate statistics
        success_rate = np.mean(success_rates)
        avg_expansion_probability = np.mean(expansion_probabilities)
        avg_kardashev_progression = np.mean(kardashev_progressions)
        
        # Calculate confidence intervals
        percentiles = {}
        for conf in self.parameters['confidence_intervals']:
            percentiles[f'p{int(conf*100)}'] = {
                'success_rate': np.percentile(success_rates, conf * 100),
                'expansion_probability': np.percentile(expansion_probabilities, conf * 100),
                'safety_margin': np.percentile(safety_margins, conf * 100),
                'evolution_duration': np.percentile(evolution_durations, conf * 100),
                'kardashev_progression': np.percentile(kardashev_progressions, conf * 100)
            }
        
        return {
            'enabled': True,
            'num_runs': num_runs,
            'success_rate': success_rate,
            'avg_expansion_probability': avg_expansion_probability,
            'avg_kardashev_progression': avg_kardashev_progression,
            'percentiles': percentiles,
            'raw_data': {
                'success_rates': success_rates,
                'expansion_probabilities': expansion_probabilities,
                'safety_margins': safety_margins,
                'evolution_durations': evolution_durations,
                'kardashev_progressions': kardashev_progressions
            }
        }
    
    def _calculate_summary(self, deterministic: List[Dict[str, Any]], 
                         probabilistic: Dict[str, Any],
                         kardashev_comparison: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate summary statistics and insights."""
        # Deterministic summary
        det_success_count = sum(1 for r in deterministic if r['civilization_succeeds'])
        det_success_rate = det_success_count / len(deterministic)
        
        # Kardashev comparison summary
        kardashev_success_count = sum(1 for r in kardashev_comparison if r['civilization_succeeds'])
        kardashev_success_rate = kardashev_success_count / len(kardashev_comparison)
        
        # Find critical thresholds
        baseline_result = deterministic[0]  # No delay scenario
        critical_delay = None
        
        for result in deterministic:
            if not result['civilization_succeeds'] and critical_delay is None:
                critical_delay = result['evolution_delay_factor']
                break
        
        summary = {
            'deterministic_success_rate': det_success_rate,
            'deterministic_scenarios_passing': det_success_count,
            'total_deterministic_scenarios': len(deterministic),
            'kardashev_success_rate': kardashev_success_rate,
            'kardashev_scenarios_passing': kardashev_success_count,
            'total_kardashev_scenarios': len(kardashev_comparison),
            'baseline_expansion_window': baseline_result['expansion_window'],
            'baseline_success': baseline_result['civilization_succeeds'],
            'baseline_kardashev_progression': baseline_result['final_kardashev_level'] - baseline_result['starting_kardashev_level'],
            'critical_evolution_delay': critical_delay,
            'window_fragility': 'HIGH' if det_success_rate < 0.5 else 'MODERATE' if det_success_rate < 0.8 else 'LOW',
            'kardashev_impact': 'CRITICAL' if kardashev_success_rate > det_success_rate + 0.2 else 'MODERATE' if kardashev_success_rate > det_success_rate + 0.1 else 'LOW'
        }
        
        if probabilistic['enabled']:
            summary['probabilistic_success_rate'] = probabilistic['success_rate']
            summary['probabilistic_confidence'] = probabilistic['percentiles']
            summary['avg_kardashev_progression'] = probabilistic['avg_kardashev_progression']
        
        return summary 