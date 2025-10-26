# Bite-Piper Architecture Documentation

## System Overview

Bite-Piper is a production-grade socio-economic data analysis system built on **Minimal MeTTa** principles. The architecture emphasizes clean code, minimal dependencies, and explicit control over evaluation.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     BitePiperApp                            │
│  (Production Application Layer)                             │
│  - Orchestrates analysis workflow                           │
│  - Manages knowledge base loading                           │
│  - Provides high-level API                                  │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                  MeTTaInterpreter                           │
│  (Minimal MeTTa Engine)                                     │
│  - eval: One-step evaluation                                │
│  - chain: Variable binding & chaining                       │
│  - unify: Pattern matching                                  │
│  - Grounded functions: +, -, <, ==                          │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                    AtomSpace                                │
│  (Knowledge Base)                                           │
│  - Stores equality rules: (= pattern body)                  │
│  - Provides pattern matching & query                        │
│  - In-memory storage (extensible to DB)                     │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                  Atom Structures                            │
│  - Symbol: Constants (e.g., RegionA, +)                     │
│  - Variable: Logic variables (e.g., $x, $data)              │
│  - Expression: Compound atoms (e.g., (+ 1 2))               │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Atom Layer (`atom.py`)

**Purpose**: Foundation data structures for Minimal MeTTa

**Classes**:
- `Atom`: Base class with equality and hashing
- `Symbol`: Named constants and function names
- `Variable`: Logic variables (prefixed with `$`)
- `Expression`: S-expressions for compound atoms

**Design Decisions**:
- Immutable by design (tuples for Expression values)
- Hash-based equality for efficient lookups
- Clean separation between atom types

### 2. AtomSpace (`space.py`)

**Purpose**: Knowledge base for storing and querying facts

**Key Features**:
- Stores equality rules: `(= pattern body)`
- Simple linear search (O(n) - optimizable with indexing)
- Pattern matching for queries

**Storage Format**:
```python
(= (RegionData RegionA) ((PovertyRate 60) (LiteracyRate 45)))
(= (priority $data) (FundingPriority $data))
```

**Extension Points**:
- Add indexing for O(1) lookups
- Integrate with databases (SQLite/PostgreSQL)
- Support more complex pattern matching

### 3. MeTTa Interpreter (`minimal_metta.py`)

**Purpose**: Core execution engine implementing Minimal MeTTa instructions

#### Instruction: `eval`

**Signature**: `eval(arg) -> Atom`

**Behavior**:
1. If `arg` is an expression with grounded function head → execute function
2. If `arg` matches pattern in AtomSpace → return body
3. Otherwise → return `NotReducible`

**Example**:
```python
eval((+ 1 2)) → 3
eval((RegionData RegionA)) → ((PovertyRate 60) (LiteracyRate 45))
eval((unknown)) → NotReducible
```

#### Instruction: `chain`

**Signature**: `chain(arg, var, result) -> Atom`

**Behavior**:
1. Execute `arg` (must be a Minimal MeTTa instruction)
2. Bind result to `var`
3. Substitute `var` in `result`
4. Execute the substituted result

**Example**:
```python
chain((eval (+ 1 2)), $x, (eval (+ $x 3)))
  → Execute: (eval (+ 1 2)) → 3
  → Bind: $x = 3
  → Substitute: (eval (+ 3 3))
  → Execute: (eval (+ 3 3)) → 6
  → Result: 6
```

#### Instruction: `unify`

**Signature**: `unify(arg1, arg2, unified, not_unified) -> Atom`

**Behavior**:
- Attempts to unify `arg1` and `arg2`
- Returns `unified` if successful
- Returns `not_unified` otherwise

**Current Implementation**: Simplified version (full unification is complex)

### 4. Data Types (`data_types.py`)

**Purpose**: Domain-specific types and constants for Bite-Piper

**Parametric Types**:
- `List(type)`: Generic list type
- `Metric(name, type)`: Socio-economic metrics

**Data Structures**:
- `SocioEconomicData(region, metrics, datapoint)`

**Constants**:
- Regions: `RegionA`, `RegionB`
- Metrics: `PovertyRate`, `LiteracyRate`

### 5. Application Layer (`bite_piper_main.py`)

**Purpose**: Production application orchestrating the analysis

**Key Methods**:

```python
__init__()
  → Initialize interpreter and AtomSpace
  → Load knowledge base (rules + data facts)

determine_priority(region)
  → Query: (RegionData region) → data
  → Apply: (priority data) → recommendation
  → Return: FundingPriority recommendation

run()
  → Analyze all regions
  → Run self-tests
  → Return results with status
```

## Data Flow

### Complete Analysis Flow

```
1. User Request
   ↓
2. BitePiperApp.determine_priority(RegionA)
   ↓
3. Build query: (RegionData RegionA)
   ↓
4. interpreter.eval((RegionData RegionA))
   ↓
5. AtomSpace.query((RegionData RegionA))
   ↓
6. Match: (= (RegionData RegionA) ((PovertyRate 60) (LiteracyRate 45)))
   ↓
7. Return: ((PovertyRate 60) (LiteracyRate 45))
   ↓
8. Build priority query: (priority ((PovertyRate 60) (LiteracyRate 45)))
   ↓
9. interpreter.eval((priority data))
   ↓
10. AtomSpace.query((priority $data))
    ↓
11. Match: (= (priority $data) (FundingPriority $data))
    ↓
12. Return: (FundingPriority ((PovertyRate 60) (LiteracyRate 45)))
    ↓
13. Result returned to user
```

## Design Patterns

### 1. Strategy Pattern
- Different evaluation strategies (eval, chain, unify)
- Pluggable grounded functions

### 2. Repository Pattern
- AtomSpace as repository for facts
- Query interface abstracts storage

### 3. Interpreter Pattern
- MeTTaInterpreter interprets Minimal MeTTa instructions
- Recursive evaluation through chain

### 4. Factory Pattern
- Helper methods in BitePiperApp for atom creation
- `_parse_atom()`, `_parse_expression()`

## Performance Characteristics

### Time Complexity

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| `eval` (grounded function) | O(1) | Direct function call |
| `eval` (AtomSpace query) | O(n) | Linear search through rules |
| `chain` | O(1) + eval | Variable substitution + eval call |
| `unify` (simplified) | O(1) | Basic comparison |

### Space Complexity

| Component | Complexity | Notes |
|-----------|-----------|-------|
| AtomSpace | O(n) | n = number of rules |
| Bindings (in chain) | O(m) | m = number of bound variables |
| Expression | O(d) | d = depth of expression tree |

### Optimization Opportunities

1. **AtomSpace Indexing**
   - Use hash maps for O(1) pattern lookup
   - Index by head symbol

2. **Caching**
   - Memoize frequent eval results
   - Cache compiled patterns

3. **Lazy Evaluation**
   - Don't evaluate subexpressions until needed
   - Implement thunks for delayed computation

## Extensibility Points

### Adding New Grounded Functions

```python
# In minimal_metta.py
self.grounded_functions[Symbol("*")] = \
    lambda args: self._arithmetic(args, lambda a, b: a * b)
```

### Adding New Data Sources

```python
# In data_types.py
HealthcareAccess = Symbol("HealthcareAccess")

# In bite_piper_main.py (_load_knowledge)
data_c_tuple = Expression([
    Expression([HealthcareAccess, Symbol("70")])
])
```

### Extending Analysis Rules

```python
# Add custom priority calculation
self.space.add_atom(Expression([
    Symbol("="),
    Expression([Symbol("critical_priority"), Variable("data")]),
    Expression([Symbol("CRITICAL"), Variable("data")])
]))
```

### Database Integration

```python
# Replace AtomSpace with DB-backed version
class DBAtomSpace(AtomSpace):
    def __init__(self, db_connection):
        self.db = db_connection
    
    def query(self, pattern):
        # SQL query to fetch matching rules
        pass
```

## Error Handling Strategy

### Error Types

1. **NotReducible**: No matching rule or function
2. **Error Symbols**: `Error_NoData_X`, `Error_InvalidInput_X`
3. **Exceptions**: Python exceptions for critical failures

### Error Flow

```
Input → Validation → Execution → Result
         ↓            ↓           ↓
      Error_*     NotReducible  Success
         ↓            ↓           ↓
      Return       Return      Return
```

### Production Safeguards

- Input validation in `determine_priority()`
- Try-catch blocks for exception handling
- Status tracking in `run()` results
- Self-tests on application startup

## Testing Strategy

### Test Levels

1. **Unit Tests**: Individual components (Atom, AtomSpace, Interpreter)
2. **Integration Tests**: Component interactions
3. **System Tests**: Full application workflow
4. **Self-Tests**: Built-in validation in `run()`

### Test Coverage

- Atom classes: Equality, hashing, representation
- AtomSpace: Add, query, pattern matching
- Interpreter: eval, chain, unify
- Application: End-to-end analysis flow

## Security Considerations

### Current Implementation
- No external input (safe)
- No file I/O operations (safe)
- No network operations (safe)

### Future Considerations
- Sanitize user input if accepting external data
- Validate data sources before loading
- Implement rate limiting for API endpoints
- Use prepared statements for DB queries

## Scalability

### Current Limitations
- In-memory storage (limited by RAM)
- Linear search (O(n) queries)
- Single-threaded execution

### Scaling Strategies

1. **Horizontal Scaling**
   - Partition AtomSpace by region
   - Distribute analysis across multiple processes

2. **Vertical Scaling**
   - Optimize AtomSpace with indexing
   - Compile frequently-used patterns

3. **Caching Layer**
   - Redis for distributed caching
   - In-memory LRU cache for eval results

## Future Enhancements

### Short-term
- [ ] Add more grounded functions (*, /, %, logical operators)
- [ ] Implement full unification algorithm
- [ ] Add support for `function` and `return` instructions
- [ ] Create web API with Flask/FastAPI

### Medium-term
- [ ] Database persistence (SQLite/PostgreSQL)
- [ ] Data import from CSV/JSON
- [ ] Visualization dashboard
- [ ] Advanced analytics (trends, predictions)

### Long-term
- [ ] Distributed processing
- [ ] Machine learning integration
- [ ] Real-time data streams
- [ ] Multi-tenant architecture

## Conclusion

Bite-Piper demonstrates how Minimal MeTTa principles enable:
- **Explicit Control**: Every evaluation step is traceable
- **Clean Architecture**: Clear separation of concerns
- **Extensibility**: Easy to add new features
- **Maintainability**: Minimal dependencies, clear code

The architecture balances simplicity with production readiness, providing a solid foundation for socio-economic data analysis.
