# 🌪️ Jinn-Core: Economic Simulation Engine

**Jinn** – *Joint Intelligence Non-Profit Network* – is an open-source economic simulation platform designed for transparent, auditable financial risk modeling and macroeconomic analysis.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-32%20passing-brightgreen.svg)](#testing)

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

### AI Unemployment Shock Simulation

```python
from src.models.ai_unemployment_shock import simulate_ai_unemployment_shock

# Quick assessment of AI displacement effects
result = simulate_ai_unemployment_shock(
    current_employment_rate=94.0,
    ai_displacement_rate=1.0,     # 1% per year
    current_gdp=25000000000000.0, # $25T GDP
    current_year=12,              # Year 12 of displacement
    max_displacement=30.0,        # 30% max unemployment
    ubi_threshold=12.0            # UBI at 12% unemployment
)

print(f"Unemployment: {result['new_unemployment_rate']:.1f}%")
print(f"AI Productivity Boost: {result['productivity_boost']:.1f}%")
print(f"UBI Activated: {result['ubi_activated']}")
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

### 3. AI Unemployment Shock Model
- **Purpose**: Simulate economic effects of AI-driven unemployment with UBI policy responses
- **Effects**: Employment/unemployment dynamics, productivity growth, GDP evolution, UBI implementation, fiscal sustainability
- **Key Parameters**: AI displacement rate (1%/year), max unemployment (30%), UBI threshold (12%), productivity boost (2-6%)
- **Example**: 30-year simulation with UBI vs. no-UBI scenario comparison
- **Key Insights**: Can reveal trade-offs between AI productivity gains and employment losses

### 4. Bank Panic Model
- **Purpose**: Simulate banking crises and systemic financial risk
- **Effects**: Bank failures, liquidity crises, central bank interventions, economic contraction
- **Key Parameters**: Withdrawal rates, liquidity ratios, central bank support
- **Example**: Regional banking crisis with Federal Reserve intervention

### 5. Military Spending Shock Model
- **Purpose**: Simulate effects of defense spending changes
- **Effects**: GDP growth, employment, government deficit, sector reallocation
- **Key Parameters**: Spending magnitude, duration, economic multipliers
- **Example**: Defense spending surge during geopolitical tensions

### 6. Global Conflict Model
- **Purpose**: Simulate economic impacts of international conflicts
- **Effects**: Trade disruption, energy price shocks, defense spending, supply chains
- **Key Parameters**: Conflict intensity, duration, geographic scope
- **Example**: Major power conflict affecting global trade routes

### 7. Earth Rotation Shock Model
- **Purpose**: Simulate extreme geological/astronomical disruptions
- **Effects**: Infrastructure damage, agricultural disruption, energy systems
- **Key Parameters**: Rotation change magnitude, adaptation timeframe
- **Example**: Sudden changes in Earth's rotation affecting global systems

### 8. Bitcoin Price Projection Model
- **Purpose**: Simulate cryptocurrency market dynamics and adoption scenarios
- **Effects**: Bitcoin price evolution, market adoption, institutional investment
- **Key Parameters**: Adoption rates, regulatory environment, market sentiment
- **Example**: Long-term Bitcoin price projections under different adoption scenarios

---

## 🏗️ Project Structure

```
jinn-core/
├── src/                    # Main source code
│   ├── engine.py          # Core simulation engine
│   └── models/            # Economic models
│       ├── interest_rate.py         # Interest rate shock model
│       ├── inflation_shock.py       # Inflation shock model
│       ├── ai_unemployment_shock.py # AI unemployment & UBI model
│       ├── bank_panic.py           # Banking crisis model
│       ├── military_spending_shock.py # Defense spending model
│       ├── global_conflict.py       # International conflict model
│       ├── earth_rotation_shock.py  # Geological disruption model
│       ├── btc_price_projection.py  # Bitcoin price model
│       └── cosmic_consciousness_timing.py # Advanced civilization model
├── examples/              # Example scenarios
│   ├── scenario_01.json                # Fed rate hike
│   ├── scenario_02_inflation.json      # Supply chain crisis
│   ├── scenario_03_bank_panic.json     # Banking crisis
│   ├── scenario_04_military_spending.json # Defense spending
│   ├── scenario_05_global_conflict.json   # International conflict
│   ├── scenario_06_earth_rotation.json    # Geological disruption
│   ├── scenario_07_btc_projection.json    # Bitcoin price projection
│   └── scenario_08_ai_unemployment.json   # AI unemployment & UBI
├── tests/                 # Test suite
├── docs/                  # Documentation
│   └── roadmap.md           # Development roadmap
├── demo*.py              # Model demonstration scripts
├── requirements.txt      # Python dependencies
└── setup.py             # Package installation
```

---

## 🧪 Testing

Run the full test suite:
```bash
python tests/test_engine.py
```

Run individual model tests:
```bash
python test_ai_unemployment.py
```

Expected output:
```
🧪 Running AI Unemployment Shock Model Tests
✅ All tests passed!
```

**Test Coverage:**
- ✅ Engine initialization and model registration  
- ✅ Scenario loading and validation
- ✅ Interest rate shock simulation
- ✅ Inflation shock simulation
- ✅ AI unemployment shock simulation
- ✅ Banking crisis simulation
- ✅ Military spending shock simulation
- ✅ Global conflict simulation
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

### AI Unemployment & UBI Crisis
```bash
python demo_ai_unemployment_shock.py
```

Expected key output:
```
📊 Simulation Results - WITH UBI:
- Final Unemployment Rate: 35.0%
- Final GDP: $63.0 trillion  
- Total GDP Growth: 151.9%
- UBI Triggered in Year: 6
- Total UBI Cost: $9.6 trillion
- Final Tax Rate: 21.2%

🎯 Overall Assessment: ✅ FAVORABLE - Strong net economic growth despite employment losses
```

### Banking Crisis Simulation
```bash
python demo_bank_panic.py
```

---

## 🛠️ Development

### Adding New Models

1. Create model file in `src/models/`
2. Implement the model class with `simulate()` method
3. Register in `src/engine.py` 
4. Update `src/models/__init__.py`
5. Add tests and create demo script
6. Create example scenario in `examples/`
7. Update README documentation

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
- 🧠 Plug-in **scenario modules** (interest rates, inflation, AI unemployment, banking crises, conflicts)
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

**Economic Models:** 8 implemented
- Interest Rate Shock Model ✅
- Inflation Shock Model ✅
- AI Unemployment Shock Model ✅ **NEW**
- Bank Panic Model ✅
- Military Spending Shock Model ✅
- Global Conflict Model ✅
- Earth Rotation Shock Model ✅
- Bitcoin Price Projection Model ✅

**Scenario Analysis:**
- Federal Reserve policy changes ✅
- Supply chain disruptions ✅
- AI-driven unemployment with UBI responses ✅ **NEW**
- Banking system crises ✅
- Defense spending changes ✅
- International conflicts ✅
- Geological disruptions ✅
- Cryptocurrency market dynamics ✅
- Custom parameter configurations ✅

**Output Formats:**
- JSON results export ✅
- Formatted summary reports ✅
- Time series data tables ✅
- Scenario comparison analysis ✅ **NEW**
- Multi-decade projections ✅ **NEW**

**Key Research Capabilities:**
- **Productivity vs Employment Trade-offs**: Quantify how AI productivity gains offset job losses
- **UBI Fiscal Sustainability**: Model when and how Universal Basic Income can be implemented
- **Long-term Economic Projections**: 30-year simulations with complex feedback loops
- **Policy Scenario Comparison**: Side-by-side analysis of different policy responses
- **Dynamic Tax Adjustment**: Progressive taxation that responds to economic conditions

---

## 🚧 Roadmap

**Phase 1 (Current):** Foundation ✅
- Core simulation engine
- 8 economic models including AI unemployment
- Test suite and documentation
- Scenario comparison capabilities

**Phase 2 (Next):** Model Expansion  
- Climate change economic impacts
- Healthcare system shocks
- Immigration policy effects
- Housing market dynamics

**Phase 3 (Future):** Platform Features
- Web interface
- Real-time data integration
- Community scenario sharing
- Visualization dashboard

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
