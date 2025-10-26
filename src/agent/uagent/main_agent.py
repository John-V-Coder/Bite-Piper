"""
Bite-Piper Main Agent - Civic Decision-Making AI Agent
Integrates all philosophical frameworks, civic data, and ASI intelligence
"""

import os
import sys
from typing import Dict, Any, Optional
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import uagents framework
from uagents import Agent, Context, Model

# Import OpenAI for ASI integration
from openai import OpenAI

# Import all Bite-Piper modules
from allocation_fairness import AllocationFairnessAnalyzer
from civic_client import CivicDataClient, create_civic_client
from decision_justice import DecisionJusticeEvaluator
from equity_analyzer import EquityAnalyzer
from impact_assessor import ImpactAssessor
from philosophical_framework import PhilosophicalFramework
from policy_analyzer import PolicyAnalyzer
from stakeholder_mediator import StakeholderMediator
from systemic_bias_detector import SystemicBiasDetector
from transparency_engine import TransparencyEngine

# Message Models for Agent Communication
class DecisionRequest(Model):
    """Request for civic decision analysis"""
    decision_id: str
    decision_type: str  # allocation, policy, stakeholder_mediation
    decision_data: Dict[str, Any]
    regions: list
    stakeholders: Optional[list] = None
    explanation_depth: str = "full"  # brief, standard, full


class DecisionResponse(Model):
    """Response with comprehensive decision analysis"""
    decision_id: str
    timestamp: str
    analysis: Dict[str, Any]
    recommendations: list
    transparency_report: Dict[str, Any]
    asi_insights: Optional[str] = None


class HealthCheckRequest(Model):
    """Health check request"""
    ping: str


class HealthCheckResponse(Model):
    """Health check response"""
    status: str
    agent_name: str
    address: str
    modules_loaded: list


# Agent Configuration from Environment
AGENT_NAME = os.getenv("AGENT_NAME", "bite-piper-agent")
AGENT_SEED = os.getenv("AGENT_SEED", "agent1hcjnknnkmafknininfinkmnmkndajnjnjnjcnknc")
AGENT_PORT = int(os.getenv("AGENT_PORT", "8000"))
AGENT_ENDPOINT = os.getenv("AGENT_ENDPOINT", f"http://localhost:{AGENT_PORT}/submit")

# ASI Configuration
ASI_API_KEY = os.getenv("ASI_API_KEY", "")
ASI_BASE_URL = os.getenv("ASI_BASE_URL", "https://api.asi1.ai/v1")
ASI_MODEL = os.getenv("ASI_MODEL", "asi1-graph")

# Civic Data API Keys
WORLDBANK_API_KEY = os.getenv("WORLDBANK_API_KEY", "")
CENSUS_API_KEY = os.getenv("CENSUS_API_KEY", "")


class BitePiperAgent:
    """Main Bite-Piper Agent with all capabilities"""
    
    def __init__(self):
        # Initialize API keys dictionary
        self.api_keys = {
            'worldbank': WORLDBANK_API_KEY,
            'census': CENSUS_API_KEY
        }
        
        # Initialize all modules
        self.civic_client = create_civic_client(self.api_keys)
        self.framework = PhilosophicalFramework()
        self.fairness_analyzer = AllocationFairnessAnalyzer()
        self.justice_evaluator = DecisionJusticeEvaluator()
        self.equity_analyzer = EquityAnalyzer(
            civic_client=self.civic_client,
            api_keys=self.api_keys
        )
        self.impact_assessor = ImpactAssessor(
            civic_client=self.civic_client,
            api_keys=self.api_keys
        )
        self.policy_analyzer = PolicyAnalyzer()
        self.stakeholder_mediator = StakeholderMediator(
            civic_client=self.civic_client,
            api_keys=self.api_keys
        )
        self.bias_detector = SystemicBiasDetector()
        self.transparency_engine = TransparencyEngine(
            civic_client=self.civic_client,
            api_keys=self.api_keys
        )
        
        # Initialize ASI client if API key provided
        self.asi_client = None
        if ASI_API_KEY:
            self.asi_client = OpenAI(
                api_key=ASI_API_KEY,
                base_url=ASI_BASE_URL
            )
        
        self.modules_loaded = [
            "PhilosophicalFramework",
            "AllocationFairnessAnalyzer",
            "DecisionJusticeEvaluator",
            "EquityAnalyzer",
            "ImpactAssessor",
            "PolicyAnalyzer",
            "StakeholderMediator",
            "SystemicBiasDetector",
            "TransparencyEngine",
            "CivicDataClient"
        ]
        
        if self.asi_client:
            self.modules_loaded.append("ASI_Intelligence")
    
    def analyze_decision(
        self,
        decision_id: str,
        decision_type: str,
        decision_data: Dict[str, Any],
        regions: list,
        stakeholders: Optional[list] = None,
        explanation_depth: str = "full"
    ) -> Dict[str, Any]:
        """
        Comprehensive decision analysis using all modules
        """
        
        analysis_result = {
            'decision_id': decision_id,
            'decision_type': decision_type,
            'timestamp': datetime.now().isoformat(),
            'analyses': {},
            'recommendations': [],
            'transparency_report': {},
            'asi_insights': None
        }
        
        try:
            # 1. Fairness Analysis
            if decision_type == "allocation":
                fairness = self.fairness_analyzer.analyze_allocation_fairness(
                    decision_data.get('allocations', {}),
                    decision_data.get('needs_data', {}),
                    regions
                )
                analysis_result['analyses']['fairness'] = fairness
            
            # 2. Justice Evaluation
            justice = self.justice_evaluator.evaluate_decision_justice(
                decision_data, regions
            )
            analysis_result['analyses']['justice'] = justice
            
            # 3. Equity Analysis
            equity = self.equity_analyzer.analyze_equity_impact(
                decision_data, regions
            )
            analysis_result['analyses']['equity'] = equity
            
            # 4. Impact Assessment
            impact = self.impact_assessor.assess_decision_impact(
                decision_data, regions
            )
            analysis_result['analyses']['impact'] = impact
            
            # 5. Bias Detection
            bias = self.bias_detector.detect_systemic_biases(
                decision_data
            )
            analysis_result['analyses']['bias'] = bias
            
            # 6. Stakeholder Mediation (if stakeholders provided)
            if stakeholders:
                mediation = self.stakeholder_mediator.mediate_stakeholders(
                    decision_data, stakeholders
                )
                analysis_result['analyses']['stakeholder_mediation'] = mediation
            
            # 7. Transparency & Explainability
            transparency = self.transparency_engine.explain_decision(
                decision_data, regions, explanation_depth
            )
            analysis_result['transparency_report'] = transparency
            
            # 8. Generate Recommendations
            recommendations = self._generate_recommendations(analysis_result['analyses'])
            analysis_result['recommendations'] = recommendations
            
            # 9. ASI Enhancement (if available)
            if self.asi_client:
                asi_insights = self._get_asi_insights(analysis_result)
                analysis_result['asi_insights'] = asi_insights
            
        except Exception as e:
            analysis_result['error'] = str(e)
            analysis_result['status'] = 'failed'
        
        return analysis_result
    
    def _generate_recommendations(self, analyses: Dict[str, Any]) -> list:
        """Generate actionable recommendations from all analyses"""
        
        recommendations = []
        
        # From equity analysis
        if 'equity' in analyses:
            equity_recs = analyses['equity'].get('recommendations', [])
            recommendations.extend([
                {'source': 'equity_analysis', 'recommendation': rec, 'priority': 'high'}
                for rec in equity_recs[:3]  # Top 3
            ])
        
        # From bias detection
        if 'bias' in analyses:
            mitigation = analyses['bias'].get('mitigation_priorities', [])
            for m in mitigation[:3]:  # Top 3
                recommendations.append({
                    'source': 'bias_detection',
                    'recommendation': f"Mitigate {m.get('bias_type')} bias",
                    'priority': m.get('priority', 'medium'),
                    'strategies': m.get('strategies', [])
                })
        
        # From impact assessment
        if 'impact' in analyses:
            impact_mitigation = analyses['impact'].get('mitigation_strategies', [])
            recommendations.extend([
                {'source': 'impact_assessment', 'recommendation': m.get('strategy'), 'priority': 'medium'}
                for m in impact_mitigation[:2]
            ])
        
        # From stakeholder mediation
        if 'stakeholder_mediation' in analyses:
            mediation_strategies = analyses['stakeholder_mediation'].get('mediation_strategies', [])
            recommendations.extend([
                {'source': 'stakeholder_mediation', 'recommendation': s.get('strategy'), 'priority': 'high'}
                for s in mediation_strategies[:2]
            ])
        
        return recommendations
    
    def _get_asi_insights(self, analysis_result: Dict[str, Any]) -> str:
        """Get enhanced insights from ASI"""
        
        try:
            # Prepare analysis summary for ASI
            summary = self._prepare_asi_prompt(analysis_result)
            
            response = self.asi_client.chat.completions.create(
                model=ASI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert civic decision analyst with deep knowledge of "
                            "justice theory, equity frameworks, and public policy. Analyze the "
                            "provided decision analysis and provide strategic insights."
                        )
                    },
                    {
                        "role": "user",
                        "content": summary
                    }
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"ASI insights unavailable: {str(e)}"
    
    def _prepare_asi_prompt(self, analysis_result: Dict[str, Any]) -> str:
        """Prepare prompt for ASI analysis"""
        
        prompt = f"**Civic Decision Analysis Summary**\n\n"
        prompt += f"Decision ID: {analysis_result['decision_id']}\n"
        prompt += f"Type: {analysis_result['decision_type']}\n\n"
        
        # Equity summary
        if 'equity' in analysis_result['analyses']:
            equity = analysis_result['analyses']['equity']
            prompt += f"**Equity Assessment:**\n"
            prompt += f"- Disparities Detected: {equity.get('impact_summary', {}).get('total_disparities_detected', 0)}\n"
            prompt += f"- Overall: {equity.get('impact_summary', {}).get('overall_equity_assessment', 'unknown')}\n\n"
        
        # Bias summary
        if 'bias' in analysis_result['analyses']:
            bias = analysis_result['analyses']['bias']
            prompt += f"**Bias Detection:**\n"
            prompt += f"- Severity: {bias.get('severity_assessment', 'unknown')}\n"
            prompt += f"- Biases Found: {len(bias.get('detected_biases', []))}\n\n"
        
        # Impact summary
        if 'impact' in analysis_result['analyses']:
            impact = analysis_result['analyses']['impact']
            overall = impact.get('overall_assessment', {})
            prompt += f"**Impact Assessment:**\n"
            prompt += f"- Overall Impact: {overall.get('overall_impact', 'unknown')}\n"
            prompt += f"- Positive Impacts: {len(impact.get('positive_impacts', []))}\n"
            prompt += f"- Negative Impacts: {len(impact.get('negative_impacts', []))}\n\n"
        
        prompt += "**Question:** Based on this analysis, what are the top 3 strategic recommendations "
        prompt += "to improve this decision's equity, fairness, and positive impact? "
        prompt += "Consider philosophical frameworks (Rawls, Sen, Young, hooks) and practical implementation."
        
        return prompt


# Instantiate the main agent
agent = Agent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=AGENT_PORT,
    endpoint=[AGENT_ENDPOINT]
)

# Initialize Bite-Piper Agent
bite_piper = BitePiperAgent()


# Startup handler
@agent.on_event("startup")
async def startup_function(ctx: Context):
    ctx.logger.info("=" * 70)
    ctx.logger.info("🚀 BITE-PIPER CIVIC DECISION AI AGENT STARTING")
    ctx.logger.info("=" * 70)
    ctx.logger.info(f"Agent Name: {agent.name}")
    ctx.logger.info(f"Agent Address: {agent.address}")
    ctx.logger.info(f"Agent Port: {AGENT_PORT}")
    ctx.logger.info(f"Agent Endpoint: {AGENT_ENDPOINT}")
    ctx.logger.info("-" * 70)
    ctx.logger.info("📦 Loaded Modules:")
    for module in bite_piper.modules_loaded:
        ctx.logger.info(f"  ✓ {module}")
    ctx.logger.info("-" * 70)
    ctx.logger.info("🌐 Data Sources:")
    ctx.logger.info(f"  • World Bank API: {'✓ Configured' if WORLDBANK_API_KEY else '⚠ Not configured'}")
    ctx.logger.info(f"  • Census API: {'✓ Configured' if CENSUS_API_KEY else '⚠ Not configured'}")
    ctx.logger.info(f"  • ASI Intelligence: {'✓ Enabled' if ASI_API_KEY else '⚠ Disabled'}")
    ctx.logger.info("-" * 70)
    ctx.logger.info("🎯 Capabilities:")
    ctx.logger.info("  • Allocation Fairness Analysis (Rawls, Sen, Aristotle)")
    ctx.logger.info("  • Decision Justice Evaluation (4 dimensions)")
    ctx.logger.info("  • Equity Impact Analysis (6 dimensions)")
    ctx.logger.info("  • Cross-Demographic Impact Assessment")
    ctx.logger.info("  • Systemic Bias Detection (Young, hooks, Fanon)")
    ctx.logger.info("  • Policy Discourse Analysis (Foucault)")
    ctx.logger.info("  • Stakeholder Mediation (Young, Freire, Ostrom)")
    ctx.logger.info("  • Explainable AI & Transparency")
    ctx.logger.info("=" * 70)
    ctx.logger.info("✅ Agent ready to receive decision requests!")
    ctx.logger.info("=" * 70)


# Health check endpoint
@agent.on_query(model=HealthCheckRequest, replies={HealthCheckResponse})
async def handle_health_check(ctx: Context, sender: str, msg: HealthCheckRequest):
    ctx.logger.info(f"Health check from {sender}")
    
    await ctx.send(
        sender,
        HealthCheckResponse(
            status="healthy",
            agent_name=agent.name,
            address=agent.address,
            modules_loaded=bite_piper.modules_loaded
        )
    )


# Main decision analysis endpoint
@agent.on_query(model=DecisionRequest, replies=DecisionResponse)
async def handle_decision_request(ctx: Context, sender: str, msg: DecisionRequest):
    ctx.logger.info(f"📥 Received decision request: {msg.decision_id} from {sender}")
    ctx.logger.info(f"   Type: {msg.decision_type}")
    ctx.logger.info(f"   Regions: {len(msg.regions)}")
    ctx.logger.info(f"   Stakeholders: {len(msg.stakeholders) if msg.stakeholders else 0}")
    
    try:
        # Perform comprehensive analysis
        ctx.logger.info(f"🔍 Analyzing decision {msg.decision_id}...")
        
        analysis = bite_piper.analyze_decision(
            decision_id=msg.decision_id,
            decision_type=msg.decision_type,
            decision_data=msg.decision_data,
            regions=msg.regions,
            stakeholders=msg.stakeholders,
            explanation_depth=msg.explanation_depth
        )
        
        ctx.logger.info(f"✅ Analysis complete for {msg.decision_id}")
        ctx.logger.info(f"   Recommendations: {len(analysis['recommendations'])}")
        ctx.logger.info(f"   Analyses performed: {len(analysis['analyses'])}")
        
        # Send response
        await ctx.send(
            sender,
            DecisionResponse(
                decision_id=msg.decision_id,
                timestamp=analysis['timestamp'],
                analysis=analysis['analyses'],
                recommendations=analysis['recommendations'],
                transparency_report=analysis['transparency_report'],
                asi_insights=analysis.get('asi_insights')
            )
        )
        
    except Exception as e:
        ctx.logger.error(f"❌ Error analyzing decision {msg.decision_id}: {str(e)}")
        
        # Send error response
        await ctx.send(
            sender,
            DecisionResponse(
                decision_id=msg.decision_id,
                timestamp=datetime.now().isoformat(),
                analysis={"error": str(e)},
                recommendations=[],
                transparency_report={},
                asi_insights=None
            )
        )


# Shutdown handler
@agent.on_event("shutdown")
async def shutdown_function(ctx: Context):
    ctx.logger.info("=" * 70)
    ctx.logger.info("🛑 BITE-PIPER AGENT SHUTTING DOWN")
    ctx.logger.info("=" * 70)
    ctx.logger.info("Thank you for using Bite-Piper Civic Decision AI!")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("🏛️  BITE-PIPER - Civic Decision-Making AI Agent")
    print("=" * 70)
    print(f"Starting agent '{AGENT_NAME}' on port {AGENT_PORT}...")
    print(f"Endpoint: {AGENT_ENDPOINT}")
    print("=" * 70 + "\n")
    
    agent.run()
