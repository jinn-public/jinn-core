# 🌪️ Jinn-Core: Economic Simulation Engine

**Jinn** – *Joint Intelligence Non-Profit Network* – is an open-source economic simulation platform designed for transparent, auditable financial risk modeling and macroeconomic analysis.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-28%20passing-brightgreen.svg)](#testing)

---

## 🧭 Mission

To create an open, non-profit protocol for collective financial foresight—empowering communities, researchers, and public institutions to understand, plan for, and adapt to economic risks in a complex world.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/jinn-core.git
   cd jinn-core
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the demo**
   ```bash
   python demo.py
   ```

### Package Installation (Development)

For development installation:
```bash
pip install -e .
```

---

## 💡 Usage Examples

### Basic Simulation

```python
from src.engine import SimulationEngine

# Initialize the simulation engine
engine = SimulationEngine()
print(f"Available models: {list(engine.models.keys())}")

# Run a scenario from file
results = engine.run_scenario_file('examples/scenario_01.json')
```

### Interest Rate Shock Simulation

```python
# Create custom interest rate scenario
scenario = {
    'model': 'interest_rate',
    'parameters': {
        'periods': 12,
        'gdp_sensitivity': -0.3
    },
    'simulation': {
        'shock': {
            'magnitude': 0.0075,  # 75 basis points
            'duration': 6,
            'start_period': 1
        }
    }
}

results = engine.run_simulation(scenario)
```

### Inflation Shock Simulation

```python
from src.models.inflation_shock import simulate_inflation_shock

# Simple function for quick analysis
result = simulate_inflation_shock(
    current_inflation=2.0,    # 2% current rate
    inflation_spike=5.0,      # 5pp increase
    gdp=25000000000000.0,     # $25T GDP
    investment_level=5000000000000.0  # $5T investment
)

print(f"New inflation rate: {result['new_inflation']:.1f}%")
print(f"GDP after shock: ${result['real_gdp_estimate']:,.0f}")
```

---

## 📊 Available Models

### 1. Interest Rate Shock Model
- **Purpose**: Simulate Federal Reserve rate changes
- **Effects**: GDP growth, inflation, investment, consumption
- **Key Parameters**: Rate magnitude, duration, persistence
- **Example**: 75 basis point rate hike over 8 quarters

### 2. Inflation Shock Model  
- **Purpose**: Simulate supply chain disruptions and price spikes
- **Effects**: Real GDP contraction, investment decline, consumption reduction
- **Key Parameters**: Inflation spike magnitude, duration, decay rate
- **Example**: 5 percentage point inflation spike from supply chain crisis

---

## 🏗️ Project Structure

```
jinn-core/
├── src/                    # Main source code
│   ├── engine.py          # Core simulation engine
│   │   └── models/            # Economic models
│   │       ├── interest_rate.py    # Interest rate shock model
│   │       └── inflation_shock.py  # Inflation shock model
│   └── utils/             # Utility functions
│       ├── math_utils.py       # Mathematical functions
│       └── formatters.py       # Output formatting
├── examples/              # Example scenarios
│   ├── scenario_01.json       # Fed rate hike
│   └── scenario_02_inflation.json  # Supply chain crisis
├── tests/                 # Test suite
├── docs/                  # Documentation
│   └── roadmap.md           # Development roadmap
├── demo.py               # Interactive demonstration
├── requirements.txt      # Python dependencies
└── setup.py             # Package installation
```

---

## 🧪 Testing

Run the full test suite:
```bash
python tests/test_engine.py
```

Expected output:
```
Ran 28 tests in 0.006s
OK
```

**Test Coverage:**
- ✅ Engine initialization and model registration  
- ✅ Scenario loading and validation
- ✅ Interest rate shock simulation
- ✅ Inflation shock simulation  
- ✅ Mathematical utilities
- ✅ Output formatting
- ✅ Integration testing

---

## 📈 Example Scenarios

### Federal Reserve Rate Hike
```bash
python -c "
import sys; sys.path.append('src')
from engine import SimulationEngine
engine = SimulationEngine()
results = engine.run_scenario_file('examples/scenario_01.json')
print(f'Peak GDP impact: {min(results[\"results\"][\"gdp_growth\"]):.2%}')
"
```

### Supply Chain Inflation Crisis
```bash
python -c "
import sys; sys.path.append('src')
from engine import SimulationEngine  
engine = SimulationEngine()
results = engine.run_scenario_file('examples/scenario_02_inflation.json')
print(f'Peak inflation: {max(results[\"results\"][\"inflation_rate\"]):.1%}')
"
```

---

## 🛠️ Development

### Adding New Models

1. Create model file in `src/models/`
2. Implement the model class with `simulate()` method
3. Register in `src/engine.py` 
4. Add tests in `tests/test_engine.py`
5. Create example scenario in `examples/`

### Code Style

- Follow PEP 8 conventions
- Use type hints
- Add comprehensive docstrings
- Maintain test coverage above 90%

### Dependencies

**Core Requirements:**
- `numpy>=1.21.0` - Numerical computing
- `scipy>=1.7.0` - Scientific computing  
- `pandas>=1.3.0` - Data manipulation
- `jsonschema>=4.0.0` - JSON validation

**Development:**
- `pytest>=7.0.0` - Testing framework
- `pytest-cov>=4.0.0` - Coverage reporting

---

## 📚 Documentation

- 📋 [Development Roadmap](docs/roadmap.md) - Future features and milestones
- 🤝 [Contributing Guide](CONTRIBUTING.md) - How to contribute
- 📄 [License](LICENSE) - MIT License terms

---

## 🌍 What We're Building

- 🌍 A transparent **risk simulation engine**
- 🧠 Plug-in **scenario modules** (interest rates, inflation, sovereign defaults, energy crises)
- 📊 Clear, civic-focused **user interfaces** (coming soon)
- 🗳️ Community governance model (non-commercial, public-first)
- 🔍 Integrations with open data (IMF, World Bank, FRED)

---

## 🤝 Contributing

We're looking for:
- **Engineers** (Python, TypeScript, data modeling)
- **Financial analysts and economists**  
- **Civic technologists**
- **Designers and writers**

Ways to help:
- 🌱 [Open an issue](https://github.com/your-org/jinn-core/issues)
- 🔧 Submit a pull request
- 🧠 Share model ideas
- 🌍 Connect us with civic partners or funding

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📊 Current Capabilities

**Economic Models:** 2 implemented
- Interest Rate Shock Model ✅
- Inflation Shock Model ✅

**Scenario Analysis:**
- Federal Reserve policy changes ✅
- Supply chain disruptions ✅  
- Custom parameter configurations ✅

**Output Formats:**
- JSON results export ✅
- Formatted summary reports ✅
- Time series data tables ✅

---

## 🚧 Roadmap

**Phase 1 (Current):** Foundation ✅
- Core simulation engine
- Basic economic models
- Test suite and documentation

**Phase 2 (Next):** Model Expansion  
- Fiscal policy models
- Labor market dynamics
- International trade effects

**Phase 3 (Future):** Platform Features
- Web interface
- Real-time data integration
- Community scenario sharing

See [docs/roadmap.md](docs/roadmap.md) for detailed development plans.

---

## 📄 License

MIT License - Free and open to all.

> **Jinn will never be owned. Because financial foresight belongs to everyone.**

---

## 🔗 Links

- **Repository**: https://github.com/your-org/jinn-core
- **Issues**: https://github.com/your-org/jinn-core/issues  
- **Documentation**: https://jinn-core.readthedocs.io/ (coming soon)
- **Community**: [Join our discussions](https://github.com/your-org/jinn-core/discussions)
