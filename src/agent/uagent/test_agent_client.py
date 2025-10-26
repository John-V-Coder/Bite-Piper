"""
Test Client for Bite-Piper Agent
Demonstrates how to send requests to the agent
"""

from uagents import Agent, Context, Model
from uagents.query import query
import asyncio
import json


# Import the message models from main_agent
class DecisionRequest(Model):
    """Request for civic decision analysis"""
    decision_id: str
    decision_type: str
    decision_data: dict
    regions: list
    stakeholders: list = None
    explanation_depth: str = "full"


class DecisionResponse(Model):
    """Response with comprehensive decision analysis"""
    decision_id: str
    timestamp: str
    analysis: dict
    recommendations: list
    transparency_report: dict
    asi_insights: str = None


class HealthCheckRequest(Model):
    """Health check request"""
    ping: str


class HealthCheckResponse(Model):
    """Health check response"""
    status: str
    agent_name: str
    address: str
    modules_loaded: list


# Bite-Piper Agent Address (will be printed when agent starts)
# Replace this with your agent's actual address
BITE_PIPER_AGENT_ADDRESS = "agent1q..."  # Get this from agent startup logs


async def test_health_check():
    """Test agent health check"""
    print("\n" + "="*70)
    print("🏥 TESTING HEALTH CHECK")
    print("="*70)
    
    response = await query(
        destination=BITE_PIPER_AGENT_ADDRESS,
        message=HealthCheckRequest(ping="health_check"),
        timeout=15.0
    )
    
    print(f"✅ Agent Status: {response.status}")
    print(f"📛 Agent Name: {response.agent_name}")
    print(f"📍 Agent Address: {response.address}")
    print(f"📦 Modules Loaded: {len(response.modules_loaded)}")
    for module in response.modules_loaded:
        print(f"   • {module}")
    print("="*70)


async def test_allocation_decision():
    """Test allocation decision analysis"""
    print("\n" + "="*70)
    print("🎯 TESTING ALLOCATION DECISION ANALYSIS")
    print("="*70)
    
    # Sample allocation decision
    decision_request = DecisionRequest(
        decision_id="TEST-ALLOC-001",
        decision_type="allocation",
        decision_data={
            "id": "TEST-ALLOC-001",
            "total_budget": 10000000,
            "allocations": {
                "region_A": 4000000,
                "region_B": 3000000,
                "region_C": 2000000,
                "region_D": 1000000
            },
            "needs_data": {
                "region_A": {
                    "poverty_rate": 0.6,
                    "literacy_rate": 0.5,
                    "wealth_index": 30,
                    "region_type": "rural"
                },
                "region_B": {
                    "poverty_rate": 0.4,
                    "literacy_rate": 0.7,
                    "wealth_index": 50,
                    "region_type": "rural"
                },
                "region_C": {
                    "poverty_rate": 0.2,
                    "literacy_rate": 0.85,
                    "wealth_index": 70,
                    "region_type": "urban"
                },
                "region_D": {
                    "poverty_rate": 0.15,
                    "literacy_rate": 0.9,
                    "wealth_index": 80,
                    "region_type": "urban"
                }
            }
        },
        regions=[
            {"id": "region_A", "type": "country", "code": "REG-A", "region_type": "rural"},
            {"id": "region_B", "type": "country", "code": "REG-B", "region_type": "rural"},
            {"id": "region_C", "type": "country", "code": "REG-C", "region_type": "urban"},
            {"id": "region_D", "type": "country", "code": "REG-D", "region_type": "urban"}
        ],
        stakeholders=[
            {
                "id": "community_leaders",
                "type": "community",
                "interests": ["equitable distribution", "poverty reduction"],
                "concerns": ["urban bias", "insufficient rural funding"],
                "priorities": {"equity": 0.9, "efficiency": 0.6}
            },
            {
                "id": "government",
                "type": "government",
                "interests": ["economic growth", "efficient allocation"],
                "concerns": ["budget constraints"],
                "priorities": {"efficiency": 0.9, "equity": 0.7}
            }
        ],
        explanation_depth="full"
    )
    
    print("📤 Sending decision request...")
    print(f"   Decision ID: {decision_request.decision_id}")
    print(f"   Type: {decision_request.decision_type}")
    print(f"   Budget: ${decision_request.decision_data['total_budget']:,}")
    print(f"   Regions: {len(decision_request.regions)}")
    print(f"   Stakeholders: {len(decision_request.stakeholders)}")
    
    try:
        response = await query(
            destination=BITE_PIPER_AGENT_ADDRESS,
            message=decision_request,
            timeout=60.0  # Longer timeout for complex analysis
        )
        
        print("\n✅ ANALYSIS COMPLETE!")
        print("-"*70)
        print(f"📊 Decision ID: {response.decision_id}")
        print(f"⏰ Timestamp: {response.timestamp}")
        print(f"🔍 Analyses Performed: {len(response.analysis)}")
        
        for analysis_type in response.analysis.keys():
            print(f"   • {analysis_type}")
        
        print(f"\n💡 Recommendations: {len(response.recommendations)}")
        for i, rec in enumerate(response.recommendations[:5], 1):
            print(f"   {i}. [{rec.get('priority', 'medium').upper()}] {rec.get('recommendation', 'N/A')}")
            print(f"      Source: {rec.get('source', 'unknown')}")
        
        if response.asi_insights:
            print(f"\n🤖 ASI INSIGHTS:")
            print("-"*70)
            print(response.asi_insights)
        
        # Save full response to file
        output_file = f"agent_response_{response.decision_id}.json"
        with open(output_file, 'w') as f:
            json.dump({
                'decision_id': response.decision_id,
                'timestamp': response.timestamp,
                'analysis': response.analysis,
                'recommendations': response.recommendations,
                'transparency_report': response.transparency_report,
                'asi_insights': response.asi_insights
            }, f, indent=2)
        
        print(f"\n💾 Full response saved to: {output_file}")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("="*70)


async def main():
    """Main test function"""
    print("\n" + "="*70)
    print("🧪 BITE-PIPER AGENT TEST CLIENT")
    print("="*70)
    print(f"Target Agent: {BITE_PIPER_AGENT_ADDRESS}")
    print("="*70)
    
    # Test 1: Health Check
    await test_health_check()
    
    # Wait a bit
    await asyncio.sleep(2)
    
    # Test 2: Allocation Decision
    await test_allocation_decision()
    
    print("\n" + "="*70)
    print("✅ ALL TESTS COMPLETE")
    print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
