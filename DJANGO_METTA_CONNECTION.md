# 🔗 Django ↔ MeTTa Connection Explained

## How Django Views Connect to MeTTa and Use Python MeTTa Implementation

---

## 📊 Complete Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                 │
│                     (Web Browser)                            │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP Request
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                    DJANGO LAYER                              │
│                                                              │
│  views.py:                                                   │
│  ┌─────────────────────────────────────────────┐           │
│  │ def calculate_allocation(request):          │           │
│  │     budget = request.POST.get('budget')     │           │
│  │     app = BitePiperApp(total_budget=budget) │ ← Creates │
│  │     priorities = []                          │   MeTTa   │
│  │     for region in app.regions:              │   Instance│
│  │         priority_data =                      │           │
│  │             app.calculate_priority_score()   │ ← Calls   │
│  │     allocations =                            │   MeTTa   │
│  │             app.allocate_funding()           │ ← Uses    │
│  │     return render('results.html', data)     │   MeTTa   │
│  └─────────────────────────────────────────────┘           │
└────────────────────────┬────────────────────────────────────┘
                         │ Python Function Call
                         ↓
┌─────────────────────────────────────────────────────────────┐
│              APPLICATION LAYER (BitePiperApp)                │
│                                                              │
│  application.py:                                             │
│  ┌─────────────────────────────────────────────┐           │
│  │ class BitePiperApp:                         │           │
│  │     def __init__(self, total_budget):       │           │
│  │         self.space = AtomSpace()            │ ← MeTTa   │
│  │         self.interpreter =                  │   Knowledge│
│  │             MeTTaInterpreter(self.space)    │   Base    │
│  │         self._load_knowledge()              │ ← Loads   │
│  │                                             │   Rules   │
│  │     def calculate_priority_score(region):   │           │
│  │         query = Expression([RegionData, r]) │ ← MeTTa   │
│  │         result = self.interpreter.eval(q)   │   Query   │
│  │         # Calculate scores...               │           │
│  │                                             │           │
│  │     def allocate_funding(priorities):       │           │
│  │         # Query MeTTa allocation weights    │           │
│  │         weight_query = Expression([         │           │
│  │             allocation_weight, priority])   │ ← MeTTa   │
│  │         weight = interpreter.eval(query)    │   Query   │
│  └─────────────────────────────────────────────┘           │
└────────────────────────┬────────────────────────────────────┘
                         │ Symbolic Queries
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                   METTA LAYER                                │
│                                                              │
│  metta_interpreter.py:                                       │
│  ┌─────────────────────────────────────────────┐           │
│  │ class MeTTaInterpreter:                     │           │
│  │     def eval(self, expression):             │           │
│  │         # Pattern matching                  │           │
│  │         # Variable unification              │           │
│  │         # Rule application                  │           │
│  │         return result                       │           │
│  │                                             │           │
│  │     def chain(self, expr, var, result):    │           │
│  │         # Chained reasoning                 │           │
│  │                                             │           │
│  │     def unify(self, pattern, target):      │           │
│  │         # Variable binding                  │           │
│  └─────────────────────────────────────────────┘           │
└────────────────────────┬────────────────────────────────────┘
                         │ Knowledge Queries
                         ↓
┌─────────────────────────────────────────────────────────────┐
│              KNOWLEDGE BASE (AtomSpace)                      │
│                                                              │
│  knowledge_base.py:                                          │
│  ┌─────────────────────────────────────────────┐           │
│  │ class AtomSpace:                            │           │
│  │     self.atoms = []                         │           │
│  │                                             │           │
│  │ Stored Facts:                               │           │
│  │ ┌─────────────────────────────────────┐   │           │
│  │ │ (= (RegionData RegionA)             │   │           │
│  │ │    ((Income 1500)(Poverty 60)...))  │   │ ← Data    │
│  │ │                                     │   │   Facts   │
│  │ │ (= (RegionData RegionB)             │   │           │
│  │ │    ((Income 5000)(Poverty 30)...))  │   │           │
│  │ └─────────────────────────────────────┘   │           │
│  │                                             │           │
│  │ Stored Rules:                               │           │
│  │ ┌─────────────────────────────────────┐   │           │
│  │ │ (= (allocation_weight CRITICAL)     │   │           │
│  │ │     0.40)                            │   │ ← Rules   │
│  │ │ (= (allocation_weight HIGH) 0.30)   │   │           │
│  │ │ (= (allocation_weight MEDIUM) 0.20) │   │           │
│  │ │ (= (allocation_weight LOW) 0.10)    │   │           │
│  │ │                                     │   │           │
│  │ │ (= (threshold CRITICAL) 0.70)       │   │           │
│  │ │ (= (threshold HIGH) 0.50)           │   │           │
│  │ └─────────────────────────────────────┘   │           │
│  └─────────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔍 Step-by-Step Connection

### Step 1: User Makes HTTP Request

```http
POST /calculate/ HTTP/1.1
Content-Type: application/x-www-form-urlencoded

budget=1000000&use_advanced=true
```

---

### Step 2: Django View Receives Request

**File**: `src/funding/views.py` (Line 28-44)

```python
@require_http_methods(["POST"])
def calculate_allocation(request):
    """Django view function"""
    
    # Extract budget from HTTP request
    budget = int(request.POST.get('budget', 1000000))
    
    # ┌─────────────────────────────────────────┐
    # │ THIS IS WHERE DJANGO MEETS METTA!       │
    # └─────────────────────────────────────────┘
    
    # Create BitePiperApp instance (contains MeTTa engine)
    app = BitePiperApp(total_budget=budget)
    #    ↑
    #    └── This creates MeTTa interpreter + knowledge base
```

---

### Step 3: BitePiperApp Initializes MeTTa

**File**: `src/application.py` (Lines 44-54)

```python
class BitePiperApp:
    def __init__(self, total_budget=1000000):
        """
        Django creates this object, which then:
        1. Creates MeTTa AtomSpace (knowledge base)
        2. Creates MeTTa Interpreter
        3. Loads MeTTa rules and facts
        """
        
        # Step 1: Create MeTTa Knowledge Base
        self.space = AtomSpace()
        #            ↑
        #            └── Empty MeTTa knowledge base
        
        # Step 2: Create MeTTa Interpreter
        self.interpreter = MeTTaInterpreter(self.space)
        #                  ↑
        #                  └── MeTTa reasoning engine
        
        self.total_budget = total_budget
        self.regions = []
        
        # Step 3: Load knowledge into MeTTa
        self._load_knowledge()
        #   ↑
        #   └── Populates MeTTa with data facts and rules
```

---

### Step 4: Loading Knowledge into MeTTa

**File**: `src/application.py` (Lines 56-177)

```python
def _load_knowledge(self):
    """Load MeTTa knowledge base with facts and rules"""
    
    # ┌─────────────────────────────────────────────┐
    # │ LOADING DATA FACTS INTO METTA               │
    # └─────────────────────────────────────────────┘
    
    # Create data tuple for Region A
    data_a_tuple = Expression([
        Expression([HouseholdIncomePerCapita, Symbol("1500")]),
        Expression([PovertyRate, Symbol("60")]),
        Expression([WealthIndex, Symbol("25")]),
        Expression([PPI, Symbol("75")]),
        Expression([ConsumptionExpenditure, Symbol("1200")]),
        Expression([LiteracyRate, Symbol("45")])
    ])
    
    # Store as MeTTa fact: (= (RegionData RegionA) data_a_tuple)
    self.space.add_atom(Expression([
        Symbol("="),
        Expression([RegionData, RegionA]),
        data_a_tuple
    ]))
    #   ↑
    #   └── MeTTa now knows: "When asked about RegionA, return this data"
    
    # ┌─────────────────────────────────────────────┐
    # │ LOADING ALLOCATION RULES INTO METTA         │
    # └─────────────────────────────────────────────┘
    
    # MeTTa rule: CRITICAL priority gets 40% weight
    self.space.add_atom(Expression([
        Symbol("="),
        Expression([Symbol("allocation_weight"), Symbol("CRITICAL")]),
        Symbol("0.40")
    ]))
    #   ↑
    #   └── MeTTa now knows: allocation_weight(CRITICAL) = 0.40
    
    # MeTTa rule: HIGH priority gets 30% weight
    self.space.add_atom(Expression([
        Symbol("="),
        Expression([Symbol("allocation_weight"), Symbol("HIGH")]),
        Symbol("0.30")
    ]))
    
    # ... more rules for MEDIUM (0.20) and LOW (0.10)
```

**What MeTTa Knowledge Base Contains After Loading**:

```
AtomSpace Contents:
├── DATA FACTS:
│   ├── (= (RegionData RegionA) ((Income 1500)(Poverty 60)...))
│   └── (= (RegionData RegionB) ((Income 5000)(Poverty 30)...))
│
├── ALLOCATION RULES:
│   ├── (= (allocation_weight CRITICAL) 0.40)
│   ├── (= (allocation_weight HIGH) 0.30)
│   ├── (= (allocation_weight MEDIUM) 0.20)
│   └── (= (allocation_weight LOW) 0.10)
│
└── THRESHOLD RULES:
    ├── (= (threshold CRITICAL) 0.70)
    ├── (= (threshold HIGH) 0.50)
    ├── (= (threshold MEDIUM) 0.30)
    └── (= (threshold LOW) 0.00)
```

---

### Step 5: Django Calls MeTTa to Calculate Priorities

**File**: `src/funding/views.py` (Lines 51-74)

```python
# Django view continues...
for region in app.regions:
    # ┌─────────────────────────────────────────────┐
    # │ DJANGO CALLS METTA TO ANALYZE REGION!       │
    # └─────────────────────────────────────────────┘
    
    priority_data = app.calculate_priority_score(region)
    #               ↑
    #               └── This method uses MeTTa queries!
    
    region_priorities.append(priority_data)
```

**File**: `src/application.py` (Lines 201-226)

```python
def calculate_priority_score(self, region_atom):
    """Uses MeTTa to query region data"""
    
    # ┌─────────────────────────────────────────────┐
    # │ QUERY 1: GET REGION DATA FROM METTA         │
    # └─────────────────────────────────────────────┘
    
    # Build MeTTa query: (RegionData RegionA)
    query = Expression([RegionData, region_atom])
    
    # Ask MeTTa interpreter to evaluate
    data_result = self.interpreter.eval(query)
    #             ↑
    #             └── MeTTa searches knowledge base and returns:
    #                 ((Income 1500)(Poverty 60)(Wealth 25)...)
    
    # Extract indicator values from MeTTa result
    indicators = {}
    if data_result.is_expression():
        for item in data_result.value:
            if item.is_expression() and len(item.value) == 2:
                key = str(item.value[0])     # e.g., "PovertyRate"
                value = float(item.value[1])  # e.g., 60
                indicators[key] = value
    
    # Now indicators = {
    #     'PovertyRate': 60,
    #     'HouseholdIncomePerCapita': 1500,
    #     'WealthIndex': 25,
    #     ...
    # }
    
    # Calculate score based on indicators
    # (Python calculation using indicator values from MeTTa)
    score = calculate_weighted_score(indicators)
    
    return {
        'region': str(region_atom),
        'score': score,
        'priority': determine_priority_level(score),
        'indicators': indicators
    }
```

---

### Step 6: Django Uses MeTTa for Allocation Weights

**File**: `src/application.py` (Lines 330-370)

```python
def allocate_funding(self, region_priorities):
    """Use MeTTa to get allocation weights"""
    
    allocations = {}
    
    # Calculate weighted scores
    for region_priority in region_priorities:
        priority = region_priority['priority']  # e.g., "CRITICAL"
        score = region_priority['score']        # e.g., 0.850
        
        # ┌─────────────────────────────────────────────┐
        # │ QUERY 2: GET ALLOCATION WEIGHT FROM METTA   │
        # └─────────────────────────────────────────────┘
        
        # Build MeTTa query: (allocation_weight CRITICAL)
        weight_query = Expression([
            Symbol("allocation_weight"),
            Symbol(priority)
        ])
        
        # Ask MeTTa for the allocation weight
        weight_result = self.interpreter.eval(weight_query)
        #               ↑
        #               └── MeTTa returns: 0.40 (for CRITICAL)
        
        weight = float(str(weight_result))  # Convert to Python float
        
        # Calculate weighted score
        weighted_score = score × weight
        #                0.850 × 0.40 = 0.340
    
    # Distribute budget proportionally
    total_weighted = sum(all weighted_scores)
    
    for region_priority in region_priorities:
        allocation_ratio = weighted_score / total_weighted
        allocated_amount = total_budget × allocation_ratio
        
        allocations[region] = {
            'amount': allocated_amount,
            'percentage': allocation_ratio × 100,
            'priority': priority
        }
    
    return allocations
```

---

### Step 7: Django Returns Results to User

**File**: `src/funding/views.py` (Lines 83-92)

```python
# Prepare context with MeTTa results
context = {
    'budget': budget,
    'priorities': region_priorities,      # ← From MeTTa queries
    'allocations': allocations,            # ← Using MeTTa weights
    'regions_analyzed': len(region_priorities)
}

# Render HTML template with MeTTa-derived data
return render(request, 'funding/partials/editable_results.html', context)
```

---

## 🎯 How MeTTa Helps Django

### 1. **Knowledge Representation**

**Without MeTTa** (traditional Django):
```python
# Hard-coded data in Python dictionaries
REGION_DATA = {
    'RegionA': {
        'poverty': 60,
        'income': 1500,
        'wealth': 25
    }
}

ALLOCATION_WEIGHTS = {
    'CRITICAL': 0.40,
    'HIGH': 0.30
}
```

**With MeTTa** (your system):
```python
# Declarative knowledge in MeTTa
space.add_atom(Expression([
    Symbol("="),
    Expression([RegionData, RegionA]),
    data_tuple
]))

# Rules are queryable facts, not hard-coded logic
space.add_atom(Expression([
    Symbol("="),
    Expression([Symbol("allocation_weight"), Symbol("CRITICAL")]),
    Symbol("0.40")
]))
```

**Benefits**:
- ✅ **Declarative**: State facts, not procedures
- ✅ **Queryable**: Ask questions about knowledge
- ✅ **Maintainable**: Change rules without changing code
- ✅ **Explainable**: Can trace reasoning steps

---

### 2. **Symbolic Reasoning**

**MeTTa provides**:
```python
# Pattern matching
query = Expression([RegionData, Variable("X")])
# Finds ALL regions matching pattern

# Variable unification
interpreter.unify(pattern, target)
# Binds variables to values

# Rule application
interpreter.eval(Expression([Symbol("priority"), data]))
# Applies rules to transform data
```

**Django benefits**:
- ✅ **Flexible queries**: Ask complex questions
- ✅ **Rule-based logic**: Change rules, not code
- ✅ **Symbolic computation**: Work with concepts, not just numbers

---

### 3. **Separation of Concerns**

```
┌─────────────────────────┐
│ Django Layer            │ ← HTTP, routing, rendering
├─────────────────────────┤
│ Application Layer       │ ← Business logic, orchestration
├─────────────────────────┤
│ MeTTa Layer            │ ← Knowledge, reasoning, rules
├─────────────────────────┤
│ Knowledge Base         │ ← Facts, data, policies
└─────────────────────────┘
```

**Benefits**:
- ✅ Django handles web concerns
- ✅ MeTTa handles reasoning concerns
- ✅ Clean separation
- ✅ Easy to test each layer

---

### 4. **Explainable AI**

**MeTTa enables**:
```python
# Can trace WHY a decision was made
query_result = interpreter.eval(query)

# "RegionA gets CRITICAL because:"
# 1. Query: (RegionData RegionA) → returned poverty=60
# 2. Rule: poverty > 50% → CRITICAL
# 3. Query: (allocation_weight CRITICAL) → returned 0.40
# 4. Calculation: 0.850 × 0.40 = allocation
```

**Django can show**:
- ✅ Full reasoning chain
- ✅ Which rules applied
- ✅ What data was used
- ✅ How conclusion reached

---

## 📊 Complete Example Flow

### User Action: "Calculate allocation for $1M"

```
1. HTTP POST to /calculate/
   └─> budget=1000000

2. Django view: calculate_allocation()
   └─> app = BitePiperApp(total_budget=1000000)
       └─> Creates MeTTa interpreter
       └─> Loads knowledge base

3. Django: app.calculate_priority_score(RegionA)
   └─> MeTTa query: (RegionData RegionA)
       └─> MeTTa returns: ((Income 1500)(Poverty 60)...)
   └─> Python calculates: score = 0.850, priority = CRITICAL

4. Django: app.allocate_funding(priorities)
   └─> MeTTa query: (allocation_weight CRITICAL)
       └─> MeTTa returns: 0.40
   └─> Calculation: $1M × (0.850 × 0.40) / total = $826,087

5. Django renders HTML
   └─> Shows: RegionA gets $826,087 (CRITICAL priority)

6. User sees result in browser
```

---

## 💡 Key Insights

### Why Use MeTTa in Django?

**Option A - Pure Django (No MeTTa)**:
```python
# Hard-coded logic
def calculate_allocation(region):
    if region == 'A':
        if poverty > 50:
            return 0.40
    # Must change code to change logic!
```

**Option B - Django + MeTTa (Your System)**:
```python
# Query knowledge base
weight = interpreter.eval(
    Expression([allocation_weight, priority])
)
# Change rules without changing code!
```

### MeTTa Advantages:

1. **Declarative Knowledge**: Rules as data, not code
2. **Flexible Querying**: Ask questions about knowledge
3. **Symbolic Reasoning**: Pattern matching, unification
4. **Explainability**: Trace reasoning steps
5. **Maintainability**: Change rules separately from code

---

## ✅ Summary

**How Django uses MeTTa**:

1. **Django View** creates `BitePiperApp`
2. **BitePiperApp** creates `MeTTaInterpreter` + `AtomSpace`
3. **Knowledge Loading** populates MeTTa with facts and rules
4. **Query Time** Django asks MeTTa for data and rules
5. **Reasoning** MeTTa applies pattern matching and unification
6. **Results** Flow back to Django for rendering

**MeTTa provides**:
- 🧠 **Knowledge Base**: Store facts and rules
- 🔍 **Query Engine**: Ask questions symbolically
- ⚖️ **Reasoning**: Apply rules to derive conclusions
- 📊 **Explainability**: Trace decision process

**Django provides**:
- 🌐 **Web Interface**: HTTP, routing, sessions
- 📱 **User Interface**: HTML rendering, HTMX
- 🔐 **Security**: CSRF, authentication
- 💾 **Persistence**: Database (if needed)

**Together**: Powerful AI-driven web application with explainable reasoning!

---

**Files to Explore**:
- `src/funding/views.py` - Django ↔ MeTTa interface
- `src/application.py` - MeTTa wrapper for Django
- `src/metta_interpreter.py` - MeTTa reasoning engine
- `src/knowledge_base.py` - MeTTa knowledge storage
