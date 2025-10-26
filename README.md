# Bite-Piper: Interactive Funding Allocation System

## 🎯 Main Features

### 1. **Advanced Logical Scoring** 🧠 (NEW!)
**Sophisticated priority calculation** based on 6 socio-economic indicators with:
- **5 Severity Levels**: EXTREME, SEVERE, MODERATE, LOW, MINIMAL
- **Urgency Multipliers**: Recognizes compounding crises (×1.05 to ×1.20)
- **Cross-Validation**: 3 consistency checks for data quality
- **International Standards**: World Bank & UN poverty thresholds
- **Detailed Breakdown**: See each indicator's contribution

### 2. **Editable Priority Scores** ✏️ (CORE FEATURE)
**Human-in-the-loop AI** - manually adjust scores and see real-time impact:
- **Three Edit Methods**: Number input, sliders, quick action buttons
- **Real-Time Updates**: Allocation recalculates automatically (500ms)
- **Compare Modes**: Automated vs. custom allocations side-by-side
- **Reset Function**: Return to calculated values anytime
- **Full Transparency**: Original scores always visible

---

## 🚀 Quick Start (Web Interface)

```bash
cd src
python manage.py runserver
```

Visit: **http://localhost:8000**

### Using the Interface:

1. **Enable Advanced Scoring** → Check "🧠 Advanced Scoring Mode" (enabled by default)
2. **Enter Budget** → e.g., $1,000,000
3. **Calculate** → Click "🚀 Calculate Allocation"
4. **Review Analysis** → See automated priority scores with detailed breakdown
5. **Edit Scores** (Optional) → Adjust using sliders or input fields
6. **See Impact** → Allocation updates automatically in real-time
7. **Export Results** → Download JSON or print report

---

## 📊 The 6 Socio-Economic Indicators

| Indicator | Weight | What It Measures | Why It Matters |
|-----------|--------|------------------|----------------|
| **Poverty Rate** 🔴 | 25% | % below poverty line | Most direct poverty measure |
| **Wealth Index** 🏠 | 20% | Asset ownership (0-100) | Shows accumulated disadvantage |
| **Household Income** 💰 | 15% | Annual income/capita | Reflects purchasing power |
| **PPI Score** 📈 | 15% | Poverty probability (%) | Predicts future poverty risk |
| **Literacy Rate** 📚 | 15% | % can read/write | Education = pathway out of poverty |
| **Consumption** 🛒 | 10% | Annual spending | Shows actual living standards |

**Total**: 100% (weights validated by international poverty research)

---

## ✨ Key Features

### 1. **Editable Priority Scores** 🎯 (MAIN FEATURE)
- Adjust scores from 0.0 to 1.0
- Use number inputs, sliders, or quick action buttons
- Real-time allocation recalculation
- Compare original vs. custom scores
- Reset to calculated values anytime

### 2. **Automated Calculation** 🤖
- Analyzes 6 socio-economic indicators
- Calculates weighted priority scores
- Assigns priority levels (CRITICAL, HIGH, MEDIUM, LOW)
- Provides transparent reasoning

### 3. **MeTTa-Powered Allocation** 🧠
- Uses Minimal MeTTa for rule-based decisions
- Allocation weights as queryable facts
- Symbolic reasoning engine
- 100% policy-compliant

### 4. **Modern Web Interface** 💻
- Django + HTMX (minimal JavaScript)
- Real-time updates without page reloads
- Beautiful, responsive design
- Mobile-friendly

---

## 📊 How It Works

```
User Adjusts Score (0.850 → 0.650)
    ↓
HTMX sends POST request
    ↓
Django recalculates allocation
    ↓
MeTTa applies allocation rules
    ↓
New allocation displayed
    ↓
User sees: RegionA $680K → $565K
```

**Result**: $115K shifts to other regions!

---

## 🎓 Use Cases

### Policy Override
```
Automated: RegionA = 0.450 (MEDIUM)
Disaster strikes!
User adjusts: RegionA = 0.900 (CRITICAL)
Allocation: 32% → 58% of budget
```

### Budget Balancing
```
Start: 68% | 22% | 10%
Adjust scores to balance
Result: 52% | 31% | 17%
Fair distribution achieved!
```

### What-If Analysis
```
Scenario A: Poverty focus (automated)
Scenario B: Education focus (custom)
Compare allocations
Present both to stakeholders
```

---

## 📚 Documentation

- **🎯 Editable Scores Guide**: [`EDITABLE_SCORES_GUIDE.md`](EDITABLE_SCORES_GUIDE.md) - Complete user guide
- **💰 Allocation Guide**: [`FUNDING_ALLOCATION_GUIDE.md`](FUNDING_ALLOCATION_GUIDE.md) - Formulas & algorithms
- **🔧 Django Integration**: [`DJANGO_HTMX_INTEGRATION.md`](DJANGO_HTMX_INTEGRATION.md) - Technical setup
- **📖 Quick Summary**: [`FUNDING_ALLOCATION_SUMMARY.md`](FUNDING_ALLOCATION_SUMMARY.md) - Overview

---

## 🏗️ Architecture Overview

Built on **Minimal MeTTa** principles with clean, maintainable architecture.

## Architecture

### Core Components

```
Bite-Piper/
├── src/
│   ├── atom.py              # Minimal MeTTa atom structures (Symbol, Expression, Variable)
│   ├── space.py             # AtomSpace for storing equality rules and facts
│   ├── minimal_metta.py     # Minimal MeTTa interpreter (eval, unify, chain)
│   ├── data_types.py        # Parametric types for socio-economic data
│   └── bite_piper_main.py   # Production application entry point
├── meTTa/                   # Python virtual environment
└── requirements.txt         # Project dependencies
```

### Clean Code Principles

1. **Separation of Concerns**: Each module has a single, well-defined responsibility
2. **Minimal Backend**: Uses only Python standard library (no external dependencies)
3. **Type Safety**: Parametric type system for data validation
4. **Minimal MeTTa**: Implements core instructions (eval, unify, chain)

## Minimal MeTTa Implementation

### Core Instructions

#### 1. `eval`
Performs one step of evaluation:
- Searches for pattern `(= ARG $body)` in the AtomSpace
- Executes grounded functions (+, -, <, ==)
- Returns `NotReducible` if no match found

#### 2. `unify`
Attempts to unify two atoms:
```python
(unify ARG1 ARG2 UNIFIED NOT-UNIFIED)
```
Returns `UNIFIED` if successful, `NOT-UNIFIED` otherwise.

#### 3. `chain`
Executes one instruction, binds result, and substitutes:
```python
(chain ARG $VAR RESULT)
```
Enables chained evaluation of custom functions.

### Grounded Functions

- **Arithmetic**: `+`, `-`
- **Comparison**: `<`, `==`

## Data Model

### Socio-Economic Data Structure

```python
SocioEconomicData(
    region: Symbol,         # e.g., RegionA, RegionB
    metrics: List[Metric],  # Income & wealth + education indicators
    datapoint: Expression   # Actual data values
)
```

### Income & Wealth Indicators

The system tracks **5 comprehensive income & wealth indicators**:

1. **Household Income Per Capita** - Average income per household member
2. **Poverty Rate** - % of population below the national poverty line
3. **Wealth Index (IWI)** - Composite asset-based score (0-100)
4. **PPI (Progress out of Poverty Index)** - Probability below poverty threshold (0-100)
5. **Consumption Expenditure** - Household spending on goods and services

Plus **education indicator**: Literacy Rate

### Example Data Facts

**Region A** (High poverty, low income/wealth):
- Household Income Per Capita: $1,500/year
- Poverty Rate: 60%
- Wealth Index (IWI): 25/100
- PPI: 75% (probability below poverty)
- Consumption Expenditure: $1,200/year
- Literacy Rate: 45%

**Region B** (Lower poverty, higher income/wealth):
- Household Income Per Capita: $5,000/year
- Poverty Rate: 30%
- Wealth Index (IWI): 65/100
- PPI: 35% (probability below poverty)
- Consumption Expenditure: $4,200/year
- Literacy Rate: 85%

## Usage

### Running the Application

```bash
# Activate virtual environment (if not already activated)
cd Bite-Piper
source meTTa/bin/activate  # On Windows: meTTa\Scripts\activate

# Run the main application
python src/bite_piper_main.py
```

### Expected Output

```
============================================================
Bite-Piper: Socio-Economic Data Analysis System
============================================================

[1/3] Initializing Minimal MeTTa interpreter...
✅ Interpreter initialized successfully

[2/3] Running socio-economic analysis...
✅ Analysis completed

[3/3] Results:
------------------------------------------------------------
Region A (RegionA):
  → (FundingPriority ((HouseholdIncomePerCapita 1500) (PovertyRate 60) 
     (WealthIndex 25) (PPI 75) (ConsumptionExpenditure 1200) (LiteracyRate 45)))

Region B (RegionB):
  → (FundingPriority ((HouseholdIncomePerCapita 5000) (PovertyRate 30) 
     (WealthIndex 65) (PPI 35) (ConsumptionExpenditure 4200) (LiteracyRate 85)))

Core Logic Test (1+1 then +1):
  → 3 (Expected: 3)
------------------------------------------------------------

STATUS: ✅ All systems operational

============================================================
Analysis complete. System ready for production use.
============================================================
```

### Programmatic Usage

```python
from src.bite_piper_main import BitePiperApp
from src.data_types import RegionA

# Initialize application
app = BitePiperApp()

# Determine priority for a region
result = app.determine_priority(RegionA)
print(f"Priority for Region A: {result}")

# Run complete analysis
all_results = app.run()
```

## API Reference

### BitePiperApp

Main application class that orchestrates the Minimal MeTTa interpreter.

#### Methods

- `__init__()`: Initializes the interpreter and loads knowledge base
- `determine_priority(region_atom)`: Analyzes a specific region and returns priority recommendation
- `run()`: Executes complete analysis for all regions and returns results

### MeTTaInterpreter

Core interpreter implementing Minimal MeTTa instructions.

#### Methods

- `eval(arg)`: Evaluates an atom (one step)
- `unify(arg1, arg2, unified, not_unified)`: Attempts unification
- `chain(arg, var, result)`: Chains evaluation with variable binding

### AtomSpace

Storage for equality rules and data facts.

#### Methods

- `add_atom(atom)`: Adds an equality rule to the space
- `query(pattern)`: Searches for matching patterns

## Development

### Code Quality Standards

1. **Type Annotations**: All functions should have clear type hints
2. **Documentation**: Docstrings for all classes and public methods
3. **Error Handling**: Graceful degradation with meaningful error messages
4. **Testing**: Self-validation tests in main execution

### Extending the System

#### Adding New Data Sources

1. Define new data types in `data_types.py`:
```python
UnemploymentRate = Symbol("UnemploymentRate")
```

2. Add data facts in `_load_knowledge()`:
```python
data_c_tuple = Expression([
    Expression([UnemploymentRate, Symbol("15")])
])
```

#### Adding New Grounded Functions

Extend `grounded_functions` in `minimal_metta.py`:
```python
self.grounded_functions[Symbol("*")] = lambda args: self._arithmetic(args, lambda a, b: a * b)
```

#### Adding New Regions

Define new region symbols in `data_types.py`:
```python
RegionC = Symbol("RegionC")
```

## Technical Details

### Why Minimal MeTTa?

1. **Explicit Control**: Each evaluation step is explicit and controllable
2. **Transparency**: Easy to trace how decisions are made
3. **Flexibility**: Can implement custom interpreters with different strategies
4. **Minimal Dependencies**: No external libraries required

### Performance Considerations

- **Space Complexity**: O(n) for n rules in AtomSpace
- **Query Time**: O(n) linear search through rules (can be optimized with indexing)
- **Evaluation Depth**: Controlled by explicit chaining

## Troubleshooting

### Common Issues

1. **ImportError**: Ensure you're in the correct directory and virtual environment is activated
2. **NotReducible Results**: Check that all required equality rules are loaded in `_load_knowledge()`
3. **Type Errors in Chain**: Verify that the second argument to `chain` is a `Variable` instance

## Future Enhancements

- [ ] Add persistent storage (SQLite/PostgreSQL)
- [ ] Implement REST API with Flask
- [ ] Add more grounded functions (multiplication, division, logical operators)
- [ ] Implement full unification algorithm
- [ ] Add support for `function` and `return` instructions
- [ ] Create web-based visualization dashboard
- [ ] Add data import from CSV/JSON files

## License

Copyright (c) 2025. All rights reserved.

## Contact

For questions or support, please refer to the project documentation or create an issue in the repository.

---

**Built with Minimal MeTTa principles for clarity, maintainability, and explainability.**
