#!/usr/bin/env python3
"""
ses_agents.py - Socio-Economic Supply Chain Agents

Enhanced MeTTa-Motto agent with:
- Recursive Data Types for Supply Chain modeling
- Custom Types for Domain Modeling (socio-economic indicators)
- Error Tracing and Transparency
- Explainable AI with Atom Types
- Arrow Types for Decision Functions
- Visualization and Comparison features

Integrates with Bite-Piper's socio-economic analysis system.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for config imports
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

# Import configuration (includes API keys)
try:
    import config
    API_KEY = config.OPENAI_API_KEY
    MODEL_NAME = config.OPENAI_MODEL
except ImportError:
    print("Warning: config.py not found. Set OPENAI_API_KEY manually.")
    API_KEY = os.getenv('OPENAI_API_KEY', '')
    MODEL_NAME = os.getenv('OPENAI_MODEL', 'gpt-4o')

# Try to import OpenAI
try:
    import openai
    openai.api_key = API_KEY
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("Warning: openai package not installed. Run: pip install openai")

# Try to import MeTTa-Motto agents
try:
    from motto.agents import MettaAgent
    MOTTO_AVAILABLE = True
except ImportError:
    MOTTO_AVAILABLE = False
    print("Warning: motto.agents not available. Using Bite-Piper agents.")

import json
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum

# ============================================================
# CUSTOM DOMAIN TYPES FOR SOCIO-ECONOMIC MODELING
# ============================================================

class PriorityLevel(Enum):
    """Priority levels for funding allocation"""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    NONE = "NONE"

class DecisionType(Enum):
    """Arrow types for decision functions"""
    FUND_ALLOCATION = "FundAllocation"
    RESOURCE_DISTRIBUTION = "ResourceDistribution"
    INTERVENTION_PRIORITY = "InterventionPriority"
    SUPPLY_CHAIN_OPTIMIZATION = "SupplyChainOptimization"

class ErrorType(Enum):
    """Error types for tracing and transparency"""
    DATA_MISSING = "DataMissing"
    THRESHOLD_EXCEEDED = "ThresholdExceeded"
    VALIDATION_FAILED = "ValidationFailed"
    COMPUTATION_ERROR = "ComputationError"

# ============================================================
# RECURSIVE DATA TYPES FOR SUPPLY CHAIN
# ============================================================

@dataclass
class SupplyChainNode:
    """Recursive supply chain node representing hierarchical structure"""
    node_id: str
    node_type: str  # "region", "district", "community", "household"
    name: str
    
    # Socio-economic indicators
    income_per_capita: Optional[float] = None
    poverty_rate: Optional[float] = None
    wealth_index: Optional[float] = None
    ppi_score: Optional[float] = None
    consumption_expenditure: Optional[float] = None
    literacy_rate: Optional[float] = None
    
    # Supply chain properties
    resources_available: Optional[Dict[str, float]] = None
    resources_needed: Optional[Dict[str, float]] = None
    
    # Recursive children nodes
    children: Optional[List['SupplyChainNode']] = None
    
    # Decision metadata
    priority: Optional[str] = None
    decision_path: Optional[List[str]] = None
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        result = asdict(self)
        if self.children:
            result['children'] = [child.to_dict() if hasattr(child, 'to_dict') else child for child in self.children]
        return result

@dataclass
class DecisionNode:
    """Decision tree node with explainable AI atoms"""
    decision_id: str
    decision_type: str
    condition: str
    action: str
    confidence: float
    explanation: str
    
    # Arrow type for decision function
    input_type: str  # e.g., "SocioEconomicData"
    output_type: str  # e.g., "PriorityRecommendation"
    
    # Recursive children decisions
    children: Optional[List['DecisionNode']] = None

@dataclass
class ErrorTrace:
    """Error tracing for transparency"""
    error_id: str
    error_type: str
    location: str
    message: str
    timestamp: str
    context: Dict[str, Any]
    recovery_action: Optional[str] = None

@dataclass
class ExplainableAtom:
    """Atom type for explainable AI"""
    atom_id: str
    atom_type: str  # "fact", "rule", "inference", "decision"
    content: str
    confidence: float
    source: str
    dependencies: List[str]  # References to other atoms
    explanation: str

# ============================================================
# CONVERT JSON / CSV TO METTA FACTS WITH TYPE ANNOTATIONS
# ============================================================
def json_to_facts(data, parent_key="", type_hint=None):
    """Convert JSON to typed MeTTa facts with domain annotations"""
    facts = []

    if isinstance(data, dict):
        for k, v in data.items():
            full_key = f"{parent_key}.{k}" if parent_key else k
            # Determine type hint based on key
            new_type = infer_type_from_key(k)
            facts.extend(json_to_facts(v, full_key, new_type))
    elif isinstance(data, list):
        for i, item in enumerate(data):
            full_key = f"{parent_key}[{i}]"
            facts.extend(json_to_facts(item, full_key, type_hint))
    else:
        # Convert leaf node to a typed MeTTa fact
        # Example: (: (Fact "income_per_capita" 1500) Number)
        key_clean = parent_key.replace(" ", "_").replace("-", "_").replace(".", "_")
        
        if isinstance(data, str):
            fact = f'(Fact "{key_clean}" "{data}")'
            typed_fact = f'(: {fact} String)' if type_hint else fact
        elif isinstance(data, (int, float)):
            fact = f'(Fact "{key_clean}" {data})'
            typed_fact = f'(: {fact} {type_hint or "Number"})'
        elif isinstance(data, bool):
            fact = f'(Fact "{key_clean}" {str(data)})'
            typed_fact = f'(: {fact} Bool)'
        else:
            fact = f'(Fact "{key_clean}" {data})'
            typed_fact = fact
        
        facts.append(typed_fact)

    return facts

def infer_type_from_key(key: str) -> Optional[str]:
    """Infer MeTTa type from key name for domain modeling"""
    key_lower = key.lower()
    
    # Income & Wealth indicators
    if any(x in key_lower for x in ['income', 'wealth', 'expenditure', 'consumption']):
        return 'Currency'
    elif any(x in key_lower for x in ['poverty_rate', 'literacy_rate', 'ppi']):
        return 'Percentage'
    elif 'wealth_index' in key_lower or 'iwi' in key_lower:
        return 'Score_0_100'
    
    # Priority and decisions
    elif 'priority' in key_lower:
        return 'PriorityLevel'
    elif 'decision' in key_lower:
        return 'Decision'
    
    # Location and hierarchy
    elif any(x in key_lower for x in ['region', 'district', 'community', 'node']):
        return 'LocationNode'
    
    return None

# ============================================================
# SUPPLY CHAIN DATA LOADER
# ============================================================

def load_supply_chain_data(data_path: str) -> Dict[str, Any]:
    """Load socio-economic supply chain data from JSON"""
    try:
        with open(data_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: Data file {data_path} not found.")
        return {}

def create_supply_chain_hierarchy(data: Dict) -> Optional[SupplyChainNode]:
    """Convert flat data to recursive supply chain hierarchy"""
    if not data:
        return None
    
    # Create root node
    root = SupplyChainNode(
        node_id=data.get("node_id", "root"),
        node_type=data.get("node_type", "region"),
        name=data.get("name", "Root"),
        income_per_capita=data.get("income_per_capita"),
        poverty_rate=data.get("poverty_rate"),
        wealth_index=data.get("wealth_index"),
        ppi_score=data.get("ppi_score"),
        consumption_expenditure=data.get("consumption_expenditure"),
        literacy_rate=data.get("literacy_rate"),
        resources_available=data.get("resources_available"),
        resources_needed=data.get("resources_needed"),
        priority=data.get("priority"),
        decision_path=data.get("decision_path"),
        children=[]
    )
    
    # Recursively create children
    if "children" in data and data["children"]:
        for child_data in data["children"]:
            child_node = create_supply_chain_hierarchy(child_data)
            if child_node:
                root.children.append(child_node)
    
    return root

# ============================================================
# DECISION FUNCTION ARROWS
# ============================================================

def arrow_fund_allocation(node: SupplyChainNode) -> Dict[str, Any]:
    """
    Arrow Type: SocioEconomicData -> FundingDecision
    Decision function for fund allocation based on indicators
    """
    score = 0.0
    explanation_parts = []
    
    # Weight-based scoring
    if node.poverty_rate and node.poverty_rate > 50:
        score += 0.3
        explanation_parts.append(f"High poverty rate ({node.poverty_rate}%)")
    
    if node.income_per_capita and node.income_per_capita < 2000:
        score += 0.2
        explanation_parts.append(f"Low income (${node.income_per_capita}/year)")
    
    if node.wealth_index and node.wealth_index < 30:
        score += 0.25
        explanation_parts.append(f"Low wealth index ({node.wealth_index}/100)")
    
    if node.ppi_score and node.ppi_score > 70:
        score += 0.15
        explanation_parts.append(f"High poverty probability ({node.ppi_score}%)")
    
    if node.literacy_rate and node.literacy_rate < 50:
        score += 0.1
        explanation_parts.append(f"Low literacy ({node.literacy_rate}%)")
    
    # Determine priority
    if score >= 0.7:
        priority = PriorityLevel.CRITICAL.value
    elif score >= 0.5:
        priority = PriorityLevel.HIGH.value
    elif score >= 0.3:
        priority = PriorityLevel.MEDIUM.value
    else:
        priority = PriorityLevel.LOW.value
    
    return {
        "node_id": node.node_id,
        "priority": priority,
        "score": round(score, 2),
        "explanation": " | ".join(explanation_parts) if explanation_parts else "Moderate indicators",
        "decision_type": DecisionType.FUND_ALLOCATION.value
    }

def arrow_resource_distribution(node: SupplyChainNode) -> Dict[str, Any]:
    """
    Arrow Type: SupplyChainNode -> ResourceAllocation
    Determine resource distribution based on needs vs available
    """
    if not node.resources_needed or not node.resources_available:
        return {"status": "insufficient_data"}
    
    allocations = {}
    gaps = {}
    
    for resource, needed in node.resources_needed.items():
        available = node.resources_available.get(resource, 0)
        gap = needed - available
        gaps[resource] = gap
        
        if gap > 0:
            allocations[resource] = {
                "needed": needed,
                "available": available,
                "gap": gap,
                "priority": "CRITICAL" if gap / needed > 0.5 else "MODERATE"
            }
    
    return {
        "node_id": node.node_id,
        "allocations": allocations,
        "total_gaps": len([g for g in gaps.values() if g > 0]),
        "decision_type": DecisionType.RESOURCE_DISTRIBUTION.value
    }

# ============================================================
# EXPLAINABLE AI GENERATION
# ============================================================

def generate_explainable_atoms(node: SupplyChainNode, decision: Dict) -> List[ExplainableAtom]:
    """Generate explainable AI atoms from decision process"""
    atoms = []
    
    # Fact atoms
    atoms.append(ExplainableAtom(
        atom_id=f"fact_{node.node_id}_poverty",
        atom_type="fact",
        content=f"(Poverty {node.name} {node.poverty_rate})",
        confidence=1.0,
        source="data",
        dependencies=[],
        explanation=f"{node.name} has {node.poverty_rate}% poverty rate"
    ))
    
    # Rule atom
    atoms.append(ExplainableAtom(
        atom_id=f"rule_priority_{node.node_id}",
        atom_type="rule",
        content=f"(Priority {node.name} {decision.get('priority')})",
        confidence=0.9,
        source="decision_function",
        dependencies=[f"fact_{node.node_id}_poverty"],
        explanation=f"Priority {decision.get('priority')} assigned due to: {decision.get('explanation')}"
    ))
    
    # Inference atom
    atoms.append(ExplainableAtom(
        atom_id=f"inference_{node.node_id}",
        atom_type="inference",
        content=f"(Recommend {node.name} FundingIntervention)",
        confidence=decision.get('score', 0.5),
        source="inference_engine",
        dependencies=[f"rule_priority_{node.node_id}"],
        explanation=f"Funding intervention recommended with confidence {decision.get('score')}"
    ))
    
    return atoms

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("Socio-Economic Supply Chain Agent")
    print("Recursive Types | Custom Domains | Explainable AI")
    print("=" * 70)
    
    # Load data
    data_path = Path(__file__).parent.parent / "socioeconomic_supply_chain_data.json"
    
    if data_path.exists():
        print(f"\nLoading data from: {data_path}")
        data = load_supply_chain_data(str(data_path))
        
        # Create supply chain hierarchy
        if "supply_chain" in data:
            root_node = create_supply_chain_hierarchy(data["supply_chain"])
            
            if root_node:
                print(f"\nSupply Chain Root: {root_node.name}")
                print(f"Node Type: {root_node.node_type}")
                print(f"Children: {len(root_node.children) if root_node.children else 0}")
                
                # Apply decision functions
                print("\n" + "="*70)
                print("DECISION FUNCTION ARROWS")
                print("="*70)
                
                funding_decision = arrow_fund_allocation(root_node)
                print(f"\nFunding Decision for {root_node.name}:")
                print(f"  Priority: {funding_decision['priority']}")
                print(f"  Score: {funding_decision['score']}")
                print(f"  Explanation: {funding_decision['explanation']}")
                
                # Generate explainable atoms
                atoms = generate_explainable_atoms(root_node, funding_decision)
                print(f"\n  Explainable Atoms Generated: {len(atoms)}")
                
                # Process children recursively
                if root_node.children:
                    print("\n" + "-"*70)
                    print("CHILD NODES ANALYSIS")
                    print("-"*70)
                    for i, child in enumerate(root_node.children, 1):
                        child_decision = arrow_fund_allocation(child)
                        print(f"\n{i}. {child.name} ({child.node_type})")
                        print(f"   Priority: {child_decision['priority']}")
                        print(f"   Score: {child_decision['score']}")
        
        # Convert to MeTTa facts
        print("\n" + "="*70)
        print("METTA FACTS GENERATION")
        print("="*70)
        facts = json_to_facts(data)
        print(f"\nGenerated {len(facts)} typed MeTTa facts")
        print("\nSample facts (first 5):")
        for fact in facts[:5]:
            print(f"  {fact}")
    
    else:
        print(f"\nData file not found: {data_path}")
        print("Please create 'socioeconomic_supply_chain_data.json' in the project root.")
    
    print("\n" + "="*70)
    print("Analysis Complete")
    print("="*70)
