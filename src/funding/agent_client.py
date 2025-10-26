"""
Django service client for communicating with Bite-Piper uAgent
Handles all agent communication and response processing
"""

import os
import asyncio
import json
from typing import Dict, Any, Optional
from datetime import datetime
import logging

from uagents import Model
from uagents.query import query

logger = logging.getLogger(__name__)

# Message Models for Agent Communication
class DecisionRequest(Model):
    """Request for civic decision analysis"""
    decision_id: str
    decision_type: str
    decision_data: Dict[str, Any]
    regions: list
    stakeholders: Optional[list] = None
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

class AgentClient:
    """Client for communicating with Bite-Piper Agent"""

    def __init__(self):
        self.agent_address = os.getenv("AGENT_ADDRESS", "")
        self.timeout = int(os.getenv("AGENT_TIMEOUT", "30"))

        if not self.agent_address:
            logger.warning("AGENT_ADDRESS not set in environment")

    async def health_check(self) -> Dict[str, Any]:
        """
        Check if agent is healthy and responsive
        
        Returns:
            Dict with status, agent info, and capabilities
        """
        try:
            response = await query(
                destination=self.agent_address,
                message=HealthCheckRequest(ping="health_check"),
                timeout=self.timeout
            )
            
            return {
                "status": response.status,
                "agent_name": response.agent_name,
                "address": response.address,
                "modules_loaded": response.modules_loaded,
            }
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }

    async def analyze_decision(self, decision_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send allocation decision to agent for comprehensive analysis
        """
        try:
            decision_id = f"decision-{datetime.now().timestamp()}"
            
            request = DecisionRequest(
                decision_id=decision_id,
                decision_type="funding_allocation",
                decision_data=decision_data,
                regions=[decision_data['region']],
                stakeholders=decision_data.get('stakeholders', [])
            )

            logger.info(f"Sending decision analysis request to agent: {decision_data.get('region')}")

            response = await query(
                destination=self.agent_address,
                message=request,
                timeout=self.timeout
            )
            
            logger.info(f"Received agent analysis for {decision_data.get('region')}")
            return {
                "status": "success",
                "analysis": response.analysis,
            }
        except Exception as e:
            logger.error(f"Decision analysis failed: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }

    async def batch_analyze_allocations(self, allocations: Dict[str, Any],
                                   priorities: list, budget: float) -> Dict[str, Any]:
        """
        Analyze multiple allocation decisions in batch
        """
        results = {}
        tasks = []

        for region_name, allocation_details in allocations.items():
            priority_data = next(
                (p for p in priorities if p['region'] == region_name),
                None
            )

            if not priority_data:
                continue

            decision_data = {
                "decision_type": "funding_allocation",
                "region": region_name,
                "amount": allocation_details['amount'],
                "budget": budget,
                "priority_score": priority_data['score'],
                "priority_level": priority_data['priority'],
                "indicators": priority_data.get('indicators', {}),
                "stakeholders": self._extract_stakeholders(priority_data),
                "percentage": allocation_details['percentage']
            }
            
            tasks.append(self.analyze_decision(decision_data))

        analysis_results = await asyncio.gather(*tasks)

        for i, (region_name, _) in enumerate(allocations.items()):
            analysis_result = analysis_results[i]
            if analysis_result['status'] == 'success':
                results[region_name] = analysis_result['analysis']
            else:
                results[region_name] = {
                    "error": analysis_result.get('message', 'Analysis failed')
                }

        return results

    def _extract_stakeholders(self, priority_data: Dict[str, Any]) -> list:
        """Extract stakeholder groups from priority data"""
        stakeholders = []
        indicators = priority_data.get('indicators', {})

        if indicators.get('poverty_rate', 0) > 0.3:
            stakeholders.append("Low-income families")
        if indicators.get('literacy_rate', 1) < 0.7:
            stakeholders.append("Educational institutions")
        if indicators.get('income', 0) < 20000:
            stakeholders.append("Unemployed workers")

        stakeholders.extend([
            "Local government",
            "Community organizations",
            "Social services"
        ])

        return stakeholders

# Singleton instance
_client_instance = None

def get_agent_client() -> "AgentClient":
    """Get singleton instance of AgentClient"""
    global _client_instance
    if _client_instance is None:
        _client_instance = AgentClient()
    return _client_instance
