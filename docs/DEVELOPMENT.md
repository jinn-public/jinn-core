# 🛠️ Development Guide

This guide covers everything you need to know to develop and contribute to Jinn-Core.

---

## 🚀 Quick Setup

### Automated Setup (Recommended)

```bash
# Clone repository
git clone https://github.com/your-org/jinn-core.git
cd jinn-core

# Run automated setup
chmod +x setup.sh
./setup.sh
```

### Manual Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .

# Run tests
python tests/test_engine.py

# Run demo
python demo.py
```

---

## 🏗️ Architecture Overview

### Core Components

```
jinn-core/
├── src/                    # Source code
│   ├── engine.py          # Main simulation engine
│   ├── models/            # Economic models
│   │   ├── __init__.py   
│   │   ├── interest_rate.py    # Federal Reserve rate shock model
│   │   └── inflation_shock.py  # Supply chain inflation model
│   └── utils/             # Utility functions
│       ├── math_utils.py       # Mathematical operations
│       └── formatters.py       # Output formatting
├── examples/              # Example scenarios
├── tests/                 # Test suite
├── docs/                  # Documentation
└── demo.py               # Interactive demo
```

### Design Patterns

1. **Model Registry Pattern**: All models registered in `engine.py`
2. **Factory Pattern**: Dynamic model instantiation based on scenario type
3. **Configuration Pattern**: JSON-based scenario configuration
4. **Plugin Architecture**: Easy addition of new economic models

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python tests/test_engine.py

# Run tests with verbose output
python tests/test_engine.py -v

# Run specific test class
python -m unittest tests.test_engine.TestSimulationEngine
```

### Test Coverage

Current test coverage includes:

- ✅ **Engine Tests** (8 tests)
  - Engine initialization and model registration
  - Scenario loading and execution
  - Error handling and validation

- ✅ **Interest Rate Model Tests** (8 tests) 
  - Model initialization and parameters
  - Shock simulation and persistence
  - Summary statistics calculation

- ✅ **Inflation Shock Model Tests** (8 tests)
  - Model initialization and parameters
  - Shock simulation and persistence  
  - Summary statistics calculation

- ✅ **Simple Function Tests** (2 tests)
  - Basic inflation shock calculation
  - Investment drop caps and limits

- ✅ **Dataclass Tests** (4 tests)
  - Shock object creation and validation

**Total: 28 tests, 100% pass rate**

### Adding New Tests

When adding new functionality:

1. Add tests to `tests/test_engine.py`
2. Follow existing naming conventions: `test_[feature]_[scenario]`
3. Include positive and negative test cases
4. Test edge cases and error conditions

---

## 📊 Adding New Economic Models

### 1. Create Model File

Create `src/models/your_model.py`:

```python
"""
Your Economic Model

Description of what the model simulates.
"""

import numpy as np
import logging
from typing import Dict, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class YourShock:
    """Configuration for your economic shock."""
    magnitude: float
    duration: int
    start_period: int = 0

class YourModel:
    """Your Economic Model implementation."""
    
    def __init__(self, parameters: Dict[str, Any]):
        """Initialize with parameters."""
        self.parameters = self._validate_parameters(parameters)
        logger.info("Your Model initialized")
    
    def _validate_parameters(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and set default parameters."""
        defaults = {
            'baseline_value': 1.0,
            'sensitivity': -0.5,
            'periods': 20,
            # Add your defaults here
        }
        
        for key, default_value in defaults.items():
            if key not in params:
                params[key] = default_value
        
        return params
    
    def simulate(self, simulation_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the simulation.
        
        Args:
            simulation_config: Configuration including shock details
            
        Returns:
            Dictionary containing simulation results
        """
        periods = self.parameters['periods']
        
        # Parse shock configuration
        shock_config = simulation_config.get('shock', {})
        shock = YourShock(
            magnitude=shock_config.get('magnitude', 0.0),
            duration=shock_config.get('duration', 5),
            start_period=shock_config.get('start_period', 0)
        )
        
        # Initialize results
        results = {
            'periods': list(range(periods)),
            'your_variable': np.zeros(periods),
            # Add your time series here
        }
        
        # Apply shock logic
        for t in range(periods):
            if shock.start_period <= t < shock.start_period + shock.duration:
                # Apply your shock effects
                pass
        
        # Convert to lists for JSON serialization
        for key, value in results.items():
            if isinstance(value, np.ndarray):
                results[key] = value.tolist()
        
        # Add summary statistics
        results['summary'] = self._calculate_summary(results)
        
        logger.info("Your Model simulation completed")
        return results
    
    def _calculate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate summary statistics."""
        return {
            'avg_your_variable': float(np.mean(results['your_variable'])),
            # Add your summary stats here
        }
```

### 2. Register Model

Add to `src/models/__init__.py`:

```python
from .your_model import YourModel, YourShock

__all__ = [
    # ... existing exports ...
    'YourModel',
    'YourShock'
]
```

Add to `src/engine.py` in `_register_models()`:

```python
def _register_models(self):
    """Register available economic models."""
    self.models['interest_rate'] = InterestRateModel
    self.models['inflation_shock'] = InflationShockModel
    self.models['your_model'] = YourModel  # Add this line
```

### 3. Create Example Scenario

Create `examples/scenario_your_model.json`:

```json
{
  "model": "your_model",
  "name": "Your Scenario Name",
  "description": "Description of your scenario",
  "parameters": {
    "baseline_value": 1.0,
    "sensitivity": -0.3,
    "periods": 16
  },
  "simulation": {
    "shock": {
      "magnitude": 0.05,
      "duration": 4,
      "start_period": 1
    }
  },
  "metadata": {
    "created_by": "Your Name",
    "created_date": "2024-01-15",
    "version": "1.0"
  }
}
```

### 4. Add Tests

Add test class to `tests/test_engine.py`:

```python
class TestYourModel(unittest.TestCase):
    """Test cases for Your Model."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.model = YourModel({})
    
    def test_model_initialization(self):
        """Test model initialization."""
        self.assertIsInstance(self.model, YourModel)
        self.assertIn('baseline_value', self.model.parameters)
    
    def test_simulate_basic(self):
        """Test basic simulation."""
        simulation_config = {
            'shock': {
                'magnitude': 0.05,
                'duration': 3,
                'start_period': 1
            }
        }
        
        results = self.model.simulate(simulation_config)
        
        self.assertIsInstance(results, dict)
        self.assertIn('your_variable', results)
        self.assertIn('summary', results)
```

---

## 🎨 Code Style Guidelines

### Python Style

- Follow **PEP 8** conventions
- Use **type hints** for all function signatures
- Write comprehensive **docstrings** for all classes and methods
- Use **meaningful variable names**
- Keep functions **focused and small** (< 50 lines)

### Example Function:

```python
def calculate_economic_impact(
    baseline_value: float,
    shock_magnitude: float,
    sensitivity: float
) -> float:
    """
    Calculate the economic impact of a shock.
    
    Args:
        baseline_value: The baseline economic indicator value
        shock_magnitude: Size of the economic shock
        sensitivity: How sensitive the indicator is to shocks
        
    Returns:
        The adjusted value after applying the shock
        
    Raises:
        ValueError: If any parameter is negative
    """
    if baseline_value < 0 or shock_magnitude < 0:
        raise ValueError("Values must be non-negative")
    
    impact = baseline_value * (1 + shock_magnitude * sensitivity)
    return max(0, impact)  # Ensure non-negative result
```

### Documentation Standards

1. **Docstrings**: Use Google-style docstrings
2. **Comments**: Explain *why*, not *what*
3. **Type Hints**: Always include for public APIs
4. **Examples**: Include usage examples in docstrings

---

## 🔄 Development Workflow

### 1. Setting Up Development Environment

```bash
# Fork and clone
git clone https://github.com/your-username/jinn-core.git
cd jinn-core

# Set up development environment
./setup.sh --dev

# Create feature branch
git checkout -b feature/your-feature-name
```

### 2. Making Changes

```bash
# Make your changes
# Add tests for new functionality
# Update documentation

# Run tests
python tests/test_engine.py

# Check code style (if you have dev dependencies)
black src/ tests/
flake8 src/ tests/
```

### 3. Testing Your Changes

```bash
# Run all tests
python tests/test_engine.py

# Test with your new scenario
python -c "
import sys; sys.path.append('src')
from engine import SimulationEngine
engine = SimulationEngine()
results = engine.run_scenario_file('examples/your_scenario.json')
print('Success!')
"

# Run demo to ensure nothing broke
python demo.py
```

### 4. Submitting Changes

```bash
# Commit changes
git add .
git commit -m "feat: add your feature description"

# Push to your fork
git push origin feature/your-feature-name

# Create Pull Request on GitHub
```

---

## 📦 Building and Distribution

### Local Development Install

```bash
# Install in development mode
pip install -e .

# This allows you to import jinn_core from anywhere
python -c "from jinn_core import SimulationEngine; print('Success!')"
```

### Package Building

```bash
# Install build tools
pip install build twine

# Build package
python -m build

# Check package
twine check dist/*
```

---

## 🐛 Debugging

### Common Issues

1. **Import Errors**: Make sure you're in virtual environment and installed dependencies
2. **Path Issues**: Use `sys.path.append('src')` for development
3. **JSON Errors**: Validate scenario files with online JSON validators
4. **Test Failures**: Check if you modified default parameters

### Debugging Tools

```python
# Add logging to your model
import logging
logging.basicConfig(level=logging.DEBUG)

# Use pdb for debugging
import pdb; pdb.set_trace()

# Print intermediate values
print(f"Debug: variable = {variable}")
```

---

## 🚀 Performance Considerations

### Optimization Tips

1. **Use NumPy arrays** for numerical computations
2. **Vectorize operations** instead of loops when possible
3. **Cache expensive calculations** in model parameters
4. **Profile code** with `cProfile` for performance bottlenecks

### Example Optimization:

```python
# Slow: Using loops
results = []
for i in range(periods):
    result = baseline * (1 + shock[i] * sensitivity)
    results.append(result)

# Fast: Using NumPy vectorization
results = baseline * (1 + shock * sensitivity)
```

---

## 📚 Resources

### Economic Modeling References

- [Federal Reserve Economic Data (FRED)](https://fred.stlouisfed.org/)
- [IMF World Economic Outlook Database](https://www.imf.org/external/pubs/ft/weo/2023/02/weodata/index.aspx)
- [OECD Economic Indicators](https://www.oecd.org/economy/)

### Technical References

- [NumPy Documentation](https://numpy.org/doc/)
- [SciPy Documentation](https://scipy.org/doc/)
- [Python Testing with unittest](https://docs.python.org/3/library/unittest.html)

### Contributing

- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)

---

## 🤝 Getting Help

- **Issues**: [GitHub Issues](https://github.com/your-org/jinn-core/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/jinn-core/discussions)  
- **Email**: research@jinncore.org

---

*Last updated: January 2024* 