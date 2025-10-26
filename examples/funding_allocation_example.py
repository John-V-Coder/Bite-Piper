#!/usr/bin/env python3
"""
funding_allocation_example.py - BITE-PIPER Funding Allocation Example

Demonstrates how to use BITE-PIPER for automated funding allocation
based on socio-economic indicators and priority calculations.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from application import BitePiperApp
from metta_atoms import Symbol
from socioeconomic_model import RegionA, RegionB

def example_basic_allocation():
    """Example 1: Basic funding allocation with default budget"""
    print("=" * 70)
    print("EXAMPLE 1: Basic Funding Allocation ($1 Million)")
    print("=" * 70)
    
    # Create app with default $1 million budget
    app = BitePiperApp(total_budget=1000000)
    
    # Run analysis and allocation
    results = app.run()
    
    return results

def example_custom_budget():
    """Example 2: Custom budget allocation"""
    print("\n\n")
    print("=" * 70)
    print("EXAMPLE 2: Custom Budget Allocation ($5 Million)")
    print("=" * 70)
    
    # Create app with $5 million budget
    app = BitePiperApp(total_budget=5000000)
    
    # Run analysis
    results = app.run()
    
    return results

def example_manual_priority_calculation():
    """Example 3: Manually calculate and inspect priority scores"""
    print("\n\n")
    print("=" * 70)
    print("EXAMPLE 3: Manual Priority Score Inspection")
    print("=" * 70)
    
    app = BitePiperApp(total_budget=1000000)
    
    # Calculate priority for Region A
    print("\n🔍 Inspecting Region A:")
    region_a_data = app.calculate_priority_score(RegionA)
    
    print(f"  Region: {region_a_data['region']}")
    print(f"  Priority Level: {region_a_data['priority']}")
    print(f"  Priority Score: {region_a_data['score']}")
    print(f"  Explanation: {region_a_data['explanation']}")
    print(f"\n  Indicator Details:")
    for indicator, value in region_a_data['indicators'].items():
        print(f"    - {indicator}: {value}")
    
    # Calculate priority for Region B
    print("\n🔍 Inspecting Region B:")
    region_b_data = app.calculate_priority_score(RegionB)
    
    print(f"  Region: {region_b_data['region']}")
    print(f"  Priority Level: {region_b_data['priority']}")
    print(f"  Priority Score: {region_b_data['score']}")
    print(f"  Explanation: {region_b_data['explanation']}")
    print(f"\n  Indicator Details:")
    for indicator, value in region_b_data['indicators'].items():
        print(f"    - {indicator}: {value}")
    
    # Perform allocation
    region_priorities = [region_a_data, region_b_data]
    allocations = app.allocate_funding(region_priorities)
    
    print("\n💰 Allocation Results:")
    for region, allocation in allocations.items():
        print(f"\n  {region}:")
        print(f"    Amount: ${allocation['amount']:,.2f}")
        print(f"    Percentage: {allocation['percentage']}%")
        print(f"    Priority: {allocation['priority']}")

def example_scenario_comparison():
    """Example 4: Compare different budget scenarios"""
    print("\n\n")
    print("=" * 70)
    print("EXAMPLE 4: Budget Scenario Comparison")
    print("=" * 70)
    
    budgets = [500000, 1000000, 2000000, 5000000]
    
    print("\nComparing allocation across different budget levels:\n")
    
    for budget in budgets:
        app = BitePiperApp(total_budget=budget)
        
        # Calculate priorities (without full output)
        region_priorities = []
        for region in app.regions:
            priority_data = app.calculate_priority_score(region)
            region_priorities.append(priority_data)
        
        allocations = app.allocate_funding(region_priorities)
        
        print(f"Budget: ${budget:,}")
        for region, allocation in allocations.items():
            print(f"  {region}: ${allocation['amount']:,.2f} ({allocation['percentage']}%)")
        print()

def example_export_to_json():
    """Example 5: Export allocation results to JSON"""
    print("\n")
    print("=" * 70)
    print("EXAMPLE 5: Export Results to JSON")
    print("=" * 70)
    
    import json
    
    app = BitePiperApp(total_budget=1000000)
    
    # Calculate priorities without printing
    region_priorities = []
    for region in app.regions:
        priority_data = app.calculate_priority_score(region)
        region_priorities.append(priority_data)
    
    allocations = app.allocate_funding(region_priorities)
    
    # Prepare export data
    export_data = {
        "total_budget": app.total_budget,
        "allocations": allocations,
        "priorities": region_priorities
    }
    
    # Export to JSON file
    output_file = Path(__file__).parent / 'allocation_results.json'
    with open(output_file, 'w') as f:
        json.dump(export_data, f, indent=2, default=str)
    
    print(f"\n✅ Results exported to: {output_file}")
    print("\nExported data structure:")
    print(json.dumps(export_data, indent=2, default=str)[:500] + "...")

def example_metta_rule_query():
    """Example 6: Query MeTTa allocation rules directly"""
    print("\n\n")
    print("=" * 70)
    print("EXAMPLE 6: Query MeTTa Allocation Rules")
    print("=" * 70)
    
    from metta_atoms import Expression, Symbol
    
    app = BitePiperApp(total_budget=1000000)
    
    priority_levels = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
    
    print("\n📋 MeTTa Allocation Weight Rules:")
    print("-" * 70)
    
    for level in priority_levels:
        # Query: (allocation_weight LEVEL)
        query = Expression([Symbol("allocation_weight"), Symbol(level)])
        weight = app.interpreter.eval(query)
        
        print(f"  Priority Level: {level}")
        print(f"    MeTTa Rule: (= (allocation_weight {level}) {weight})")
        print(f"    Weight Value: {weight}")
        print()
    
    print("📏 MeTTa Priority Threshold Rules:")
    print("-" * 70)
    
    for level in priority_levels:
        # Query: (threshold LEVEL)
        query = Expression([Symbol("threshold"), Symbol(level)])
        threshold = app.interpreter.eval(query)
        
        print(f"  Priority Level: {level}")
        print(f"    MeTTa Rule: (= (threshold {level}) {threshold})")
        print(f"    Score Threshold: {threshold}")
        print()

if __name__ == "__main__":
    print("\n🎯 BITE-PIPER Funding Allocation Examples")
    print("=" * 70)
    print("Demonstrating automated, transparent funding allocation")
    print("based on socio-economic indicators using Minimal MeTTa.")
    print("=" * 70)
    
    # Run all examples
    try:
        # Example 1: Basic allocation
        results1 = example_basic_allocation()
        
        # Example 2: Custom budget
        results2 = example_custom_budget()
        
        # Example 3: Manual inspection
        example_manual_priority_calculation()
        
        # Example 4: Scenario comparison
        example_scenario_comparison()
        
        # Example 5: Export to JSON
        example_export_to_json()
        
        # Example 6: Query MeTTa rules
        example_metta_rule_query()
        
        print("\n" + "=" * 70)
        print("✅ All examples completed successfully!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()
