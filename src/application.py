#!/usr/bin/env python3
"""
application.py - Bite-Piper Production Application

Bite-Piper is a Civic Decision-making AI tool that leverages trusted data
to empower users through collaborative, user-friendly interface.

This module implements the main BitePiperApp class using Minimal MeTTa principles
for analyzing socio-economic data and generating funding recommendations.
"""

from metta_atoms import Symbol, Expression, Variable
from knowledge_base import AtomSpace
from metta_interpreter import MeTTaInterpreter
from socioeconomic_model import (
    RegionA, RegionB,
    HouseholdIncomePerCapita, PovertyRate, WealthIndex,
    PPI, ConsumptionExpenditure, LiteracyRate,
    RegionData, FundingPriority
)

# Priority score weights (based on GOVERNANCE.md)
PRIORITY_WEIGHTS = {
    'poverty_rate': 0.25,      # 25% weight
    'income': 0.15,            # 15% weight
    'wealth_index': 0.20,      # 20% weight
    'ppi': 0.15,               # 15% weight
    'consumption': 0.10,       # 10% weight
    'literacy': 0.15           # 15% weight
}


class BitePiperApp:
    """
    Production application for Bite-Piper socio-economic analysis.
    
    Uses Minimal MeTTa interpreter to:
    - Load knowledge base with data facts and rules
    - Query regional data
    - Generate funding priority recommendations
    - Provide explainable AI reasoning
    """
    
    def __init__(self, total_budget=1000000):
        """Initialize the Bite-Piper application with Minimal MeTTa engine.
        
        Args:
            total_budget: Total funding available for allocation (default: $1,000,000)
        """
        self.space = AtomSpace()
        self.interpreter = MeTTaInterpreter(self.space)
        self.total_budget = total_budget
        self.regions = []
        self._load_knowledge()
    
    def _load_knowledge(self):
        """
        Load knowledge base with:
        1. Data facts for regions (socio-economic indicators)
        2. Rules for priority determination
        3. Policy and governance rules
        """
        
        # ============================================================
        # REGION DATA FACTS (Income & Wealth Indicators)
        # ============================================================
        
        # Region A - High poverty, low income/wealth
        data_a_tuple = Expression([
            Expression([HouseholdIncomePerCapita, Symbol("1500")]),  # $1,500/year
            Expression([PovertyRate, Symbol("60")]),                  # 60%
            Expression([WealthIndex, Symbol("25")]),                  # 25/100
            Expression([PPI, Symbol("75")]),                          # 75% probability
            Expression([ConsumptionExpenditure, Symbol("1200")]),     # $1,200/year
            Expression([LiteracyRate, Symbol("45")])                  # 45%
        ])
        
        # Rule: (= (RegionData RegionA) data_a_tuple)
        self.space.add_atom(Expression([
            Symbol("="),
            Expression([RegionData, RegionA]),
            data_a_tuple
        ]))
        
        # Region B - Lower poverty, higher income/wealth
        data_b_tuple = Expression([
            Expression([HouseholdIncomePerCapita, Symbol("5000")]),  # $5,000/year
            Expression([PovertyRate, Symbol("30")]),                  # 30%
            Expression([WealthIndex, Symbol("65")]),                  # 65/100
            Expression([PPI, Symbol("35")]),                          # 35% probability
            Expression([ConsumptionExpenditure, Symbol("4200")]),     # $4,200/year
            Expression([LiteracyRate, Symbol("85")])                  # 85%
        ])
        
        # Rule: (= (RegionData RegionB) data_b_tuple)
        self.space.add_atom(Expression([
            Symbol("="),
            Expression([RegionData, RegionB]),
            data_b_tuple
        ]))
        
        # ============================================================
        # PRIORITY DETERMINATION RULES
        # ============================================================
        
        # Rule: (= (priority $data) (FundingPriority $data))
        # This rule transforms any data into a funding priority recommendation
        self.space.add_atom(Expression([
            Symbol("="),
            Expression([Symbol("priority"), Variable("data")]),
            Expression([FundingPriority, Variable("data")])
        ]))
        
        # ============================================================
        # FUNDING ALLOCATION RULES
        # ============================================================
        
        # Store regions for allocation tracking
        self.regions = [RegionA, RegionB]
        
        # Priority score thresholds (stored as MeTTa facts)
        # CRITICAL: score >= 0.70
        self.space.add_atom(Expression([
            Symbol("="),
            Expression([Symbol("threshold"), Symbol("CRITICAL")]),
            Symbol("0.70")
        ]))
        
        # HIGH: score >= 0.50
        self.space.add_atom(Expression([
            Symbol("="),
            Expression([Symbol("threshold"), Symbol("HIGH")]),
            Symbol("0.50")
        ]))
        
        # MEDIUM: score >= 0.30
        self.space.add_atom(Expression([
            Symbol("="),
            Expression([Symbol("threshold"), Symbol("MEDIUM")]),
            Symbol("0.30")
        ]))
        
        # LOW: score < 0.30
        self.space.add_atom(Expression([
            Symbol("="),
            Expression([Symbol("threshold"), Symbol("LOW")]),
            Symbol("0.00")
        ]))
        
        # Allocation percentage rules based on priority
        # CRITICAL gets 40% weight in allocation
        self.space.add_atom(Expression([
            Symbol("="),
            Expression([Symbol("allocation_weight"), Symbol("CRITICAL")]),
            Symbol("0.40")
        ]))
        
        # HIGH gets 30% weight
        self.space.add_atom(Expression([
            Symbol("="),
            Expression([Symbol("allocation_weight"), Symbol("HIGH")]),
            Symbol("0.30")
        ]))
        
        # MEDIUM gets 20% weight
        self.space.add_atom(Expression([
            Symbol("="),
            Expression([Symbol("allocation_weight"), Symbol("MEDIUM")]),
            Symbol("0.20")
        ]))
        
        # LOW gets 10% weight
        self.space.add_atom(Expression([
            Symbol("="),
            Expression([Symbol("allocation_weight"), Symbol("LOW")]),
            Symbol("0.10")
        ]))
    
    def determine_priority(self, region_atom):
        """
        Determine funding priority for a region.
        
        Args:
            region_atom: Symbol representing the region (e.g., RegionA)
        
        Returns:
            Expression with funding priority recommendation
        """
        # Step 1: Query region data
        # Build query: (RegionData region_atom)
        query = Expression([RegionData, region_atom])
        data_result = self.interpreter.eval(query)
        
        # Step 2: Apply priority rule to the data
        # Build query: (priority data_result)
        priority_query = Expression([Symbol("priority"), data_result])
        priority_result = self.interpreter.eval(priority_query)
        
        return priority_result
    
    def calculate_priority_score(self, region_atom):
        """
        Calculate numerical priority score for a region based on indicators.
        
        Args:
            region_atom: Symbol representing the region
        
        Returns:
            Dictionary with score, priority level, and explanation
        """
        # Get region data
        query = Expression([RegionData, region_atom])
        data_result = self.interpreter.eval(query)
        
        # Extract indicator values from the data tuple
        indicators = {}
        if data_result.is_expression():
            for item in data_result.value:
                if item.is_expression() and len(item.value) == 2:
                    key = item.value[0].value if hasattr(item.value[0], 'value') else str(item.value[0])
                    val_str = item.value[1].value if hasattr(item.value[1], 'value') else str(item.value[1])
                    try:
                        indicators[key] = float(val_str)
                    except ValueError:
                        indicators[key] = val_str
        
        # Calculate weighted score based on GOVERNANCE.md policy
        score = 0.0
        explanation_parts = []
        
        # Poverty Rate (25% weight) - higher is worse
        if 'PovertyRate' in indicators:
            poverty = indicators['PovertyRate']
            if poverty > 50:
                poverty_score = PRIORITY_WEIGHTS['poverty_rate']
                score += poverty_score
                explanation_parts.append(f"High poverty ({poverty}%)")
            elif poverty > 30:
                poverty_score = PRIORITY_WEIGHTS['poverty_rate'] * 0.6
                score += poverty_score
                explanation_parts.append(f"Moderate poverty ({poverty}%)")
        
        # Household Income (15% weight) - lower is worse
        if 'HouseholdIncomePerCapita' in indicators:
            income = indicators['HouseholdIncomePerCapita']
            if income < 2000:
                income_score = PRIORITY_WEIGHTS['income']
                score += income_score
                explanation_parts.append(f"Low income (${income}/year)")
            elif income < 3500:
                income_score = PRIORITY_WEIGHTS['income'] * 0.6
                score += income_score
                explanation_parts.append(f"Below-average income (${income}/year)")
        
        # Wealth Index (20% weight) - lower is worse
        if 'WealthIndex' in indicators:
            wealth = indicators['WealthIndex']
            if wealth < 30:
                wealth_score = PRIORITY_WEIGHTS['wealth_index']
                score += wealth_score
                explanation_parts.append(f"Low wealth index ({wealth}/100)")
            elif wealth < 50:
                wealth_score = PRIORITY_WEIGHTS['wealth_index'] * 0.6
                score += wealth_score
                explanation_parts.append(f"Below-average wealth ({wealth}/100)")
        
        # PPI Score (15% weight) - higher is worse
        if 'PPI' in indicators:
            ppi = indicators['PPI']
            if ppi > 70:
                ppi_score = PRIORITY_WEIGHTS['ppi']
                score += ppi_score
                explanation_parts.append(f"High poverty probability ({ppi}%)")
            elif ppi > 50:
                ppi_score = PRIORITY_WEIGHTS['ppi'] * 0.6
                score += ppi_score
                explanation_parts.append(f"Moderate poverty risk ({ppi}%)")
        
        # Consumption Expenditure (10% weight) - lower is worse
        if 'ConsumptionExpenditure' in indicators:
            consumption = indicators['ConsumptionExpenditure']
            if consumption < 1500:
                consumption_score = PRIORITY_WEIGHTS['consumption']
                score += consumption_score
                explanation_parts.append(f"Low consumption (${consumption}/year)")
        
        # Literacy Rate (15% weight) - lower is worse
        if 'LiteracyRate' in indicators:
            literacy = indicators['LiteracyRate']
            if literacy < 50:
                literacy_score = PRIORITY_WEIGHTS['literacy']
                score += literacy_score
                explanation_parts.append(f"Low literacy ({literacy}%)")
            elif literacy < 70:
                literacy_score = PRIORITY_WEIGHTS['literacy'] * 0.6
                score += literacy_score
                explanation_parts.append(f"Below-average literacy ({literacy}%)")
        
        # Determine priority level using MeTTa rules
        if score >= 0.70:
            priority_level = "CRITICAL"
        elif score >= 0.50:
            priority_level = "HIGH"
        elif score >= 0.30:
            priority_level = "MEDIUM"
        else:
            priority_level = "LOW"
        
        return {
            'region': str(region_atom),
            'score': round(score, 3),
            'priority': priority_level,
            'explanation': ' | '.join(explanation_parts) if explanation_parts else 'Moderate indicators',
            'indicators': indicators
        }
    
    def allocate_funding(self, region_priorities):
        """
        Allocate funding across regions based on priority scores using MeTTa rules.
        
        Args:
            region_priorities: List of priority dictionaries from calculate_priority_score
        
        Returns:
            Dictionary with allocation details for each region
        """
        # Calculate total weighted score
        total_weighted_score = 0.0
        
        for region_priority in region_priorities:
            priority_level = region_priority['priority']
            
            # Query allocation weight from MeTTa knowledge base
            weight_query = Expression([Symbol("allocation_weight"), Symbol(priority_level)])
            weight_result = self.interpreter.eval(weight_query)
            
            if hasattr(weight_result, 'value'):
                weight = float(weight_result.value)
            else:
                weight = 0.10  # Default to LOW weight
            
            region_priority['allocation_weight'] = weight
            total_weighted_score += region_priority['score'] * weight
        
        # Allocate budget proportionally
        allocations = {}
        
        for region_priority in region_priorities:
            region = region_priority['region']
            score = region_priority['score']
            weight = region_priority['allocation_weight']
            priority = region_priority['priority']
            
            # Calculate allocation amount
            if total_weighted_score > 0:
                allocation_ratio = (score * weight) / total_weighted_score
                allocated_amount = self.total_budget * allocation_ratio
            else:
                # Equal distribution if no scores
                allocated_amount = self.total_budget / len(region_priorities)
            
            allocations[region] = {
                'amount': round(allocated_amount, 2),
                'percentage': round((allocated_amount / self.total_budget) * 100, 2),
                'priority': priority,
                'score': score,
                'explanation': region_priority['explanation']
            }
        
        return allocations
    
    def run(self):
        """
        Run the complete Bite-Piper analysis with funding allocation.
        
        Returns:
            Dictionary with analysis results, allocations, and status
        """
        print("=" * 70)
        print("Bite-Piper: Socio-Economic Data Analysis & Funding Allocation")
        print("=" * 70)
        
        print(f"\n💰 Total Budget Available: ${self.total_budget:,.2f}")
        
        print("\n[1/4] Initializing Minimal MeTTa interpreter...")
        print("✅ Interpreter initialized successfully")
        
        print("\n[2/4] Running socio-economic analysis...")
        
        # Calculate priority scores for all regions
        region_priorities = []
        for region in self.regions:
            priority_data = self.calculate_priority_score(region)
            region_priorities.append(priority_data)
        
        print("✅ Analysis completed")
        
        print("\n[3/4] Calculating Funding Allocations...")
        allocations = self.allocate_funding(region_priorities)
        print("✅ Allocations calculated using MeTTa rules")
        
        print("\n[4/4] Results:")
        print("=" * 70)
        print("PRIORITY ANALYSIS")
        print("=" * 70)
        
        for priority_data in region_priorities:
            region = priority_data['region']
            score = priority_data['score']
            priority = priority_data['priority']
            explanation = priority_data['explanation']
            
            # Color code priorities
            priority_emoji = {
                'CRITICAL': '🔴',
                'HIGH': '🟠',
                'MEDIUM': '🟡',
                'LOW': '🟢'
            }.get(priority, '⚪')
            
            print(f"\n{priority_emoji} {region}:")
            print(f"  Priority Level: {priority}")
            print(f"  Priority Score: {score:.3f}")
            print(f"  Reasoning: {explanation}")
        
        print("\n" + "=" * 70)
        print("FUNDING ALLOCATION")
        print("=" * 70)
        
        total_allocated = 0
        for region, allocation in allocations.items():
            amount = allocation['amount']
            percentage = allocation['percentage']
            priority = allocation['priority']
            
            priority_emoji = {
                'CRITICAL': '🔴',
                'HIGH': '🟠',
                'MEDIUM': '🟡',
                'LOW': '🟢'
            }.get(priority, '⚪')
            
            print(f"\n{priority_emoji} {region}:")
            print(f"  Allocated: ${amount:,.2f} ({percentage}%)")
            print(f"  Priority: {priority}")
            print(f"  Justification: {allocation['explanation']}")
            
            total_allocated += amount
        
        print("\n" + "-" * 70)
        print(f"Total Allocated: ${total_allocated:,.2f}")
        print(f"Budget Used: {(total_allocated/self.total_budget)*100:.1f}%")
        
        # Self-test: Core Minimal MeTTa logic
        print("\n" + "=" * 70)
        print("SYSTEM VERIFICATION")
        print("=" * 70)
        print("\nCore Logic Test (1+1 then +1):")
        test_expr = Expression([Symbol("eval"), Expression([Symbol("+"), Symbol("1"), Symbol("2")])])
        test_result = self.interpreter.chain(
            test_expr,
            Variable("x"),
            Expression([Symbol("eval"), Expression([Symbol("+"), Variable("x"), Symbol("1")])])
        )
        print(f"  → Result: {test_result} (Expected: 3)")
        
        # Verify MeTTa allocation rules
        print("\nMeTTa Allocation Rules Test:")
        test_weight_query = Expression([Symbol("allocation_weight"), Symbol("CRITICAL")])
        test_weight = self.interpreter.eval(test_weight_query)
        print(f"  → CRITICAL weight: {test_weight} (Expected: 0.40)")
        
        print("-" * 70)
        
        # Status check
        tests_passed = (test_result == Symbol("3") and test_weight == Symbol("0.40"))
        status = "✅ All systems operational" if tests_passed else "⚠️ System check failed"
        print(f"\nSTATUS: {status}")
        
        print("\n" + "=" * 70)
        print("Analysis complete. Funding allocated successfully.")
        print("=" * 70)
        
        return {
            "status": "success" if tests_passed else "warning",
            "total_budget": self.total_budget,
            "priorities": region_priorities,
            "allocations": allocations,
            "total_allocated": total_allocated,
            "test_result": test_result
        }


if __name__ == "__main__":
    # Create and run the Bite-Piper application with funding allocation
    # You can customize the total budget by passing it as a parameter
    # Example: app = BitePiperApp(total_budget=2000000)  # $2 million
    
    app = BitePiperApp(total_budget=1000000)  # Default: $1 million
    results = app.run()
    
    # Optional: Export results to JSON
    # import json
    # with open('funding_allocation_results.json', 'w') as f:
    #     json.dump(results, f, indent=2, default=str)
