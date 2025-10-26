"""
Django service client for communicating with Bite-Piper uAgent
Handles all agent communication and response processing
"""

import os
import requests
import json
from typing import Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class AgentClient:
    """Client for communicating with Bite-Piper Agent"""
    
    def __init__(self):
        self.agent_address = os.getenv("AGENT_ADDRESS", "")
        self.agent_endpoint = os.getenv("AGENT_ENDPOINT", "http://localhost:8000/submit")
        self.timeout = int(os.getenv("AGENT_TIMEOUT", "30"))
        
        if not self.agent_address:
            logger.warning("AGENT_ADDRESS not set in environment")
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check if agent is healthy and responsive
        
        Returns:
            Dict with status, agent info, and capabilities
        """
        try:
            response = requests.post(
                self.agent_endpoint,
                json={
                    "type": "health_check",
                    "timestamp": datetime.now().isoformat()
                },
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "healthy",
                    "agent_name": data.get("agent_name"),
                    "address": data.get("address"),
                    "modules_loaded": data.get("modules_loaded", []),
                    "response_time": response.elapsed.total_seconds()
                }
            else:
                return {
                    "status": "error",
                    "message": f"Agent returned status {response.status_code}"
                }
                
        except requests.exceptions.Timeout:
            return {
                "status": "timeout",
                "message": f"Agent did not respond within {self.timeout} seconds"
            }
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def analyze_decision(self, decision_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send allocation decision to agent for comprehensive analysis
        
        Args:
            decision_data: Dictionary containing:
                - decision_type: Type of decision (allocation, policy, etc.)
                - region: Region name
                - amount: Allocated amount
                - budget: Total budget
                - priority_score: Priority score
                - indicators: Socioeconomic indicators
                - stakeholders: List of affected stakeholder groups
                
        Returns:
            Comprehensive analysis from all agent modules
        """
        try:
            payload = {
                "type": "decision_analysis",
                "data": decision_data,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"Sending decision analysis request to agent: {decision_data.get('region')}")
            
            response = requests.post(
                self.agent_endpoint,
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Received agent analysis for {decision_data.get('region')}")
                return {
                    "status": "success",
                    "analysis": result.get("analysis", {}),
                    "response_time": response.elapsed.total_seconds()
                }
            else:
                return {
                    "status": "error",
                    "message": f"Agent returned status {response.status_code}",
                    "details": response.text
                }
                
        except requests.exceptions.Timeout:
            return {
                "status": "timeout",
                "message": f"Agent analysis timed out after {self.timeout} seconds"
            }
        except Exception as e:
            logger.error(f"Decision analysis failed: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def batch_analyze_allocations(self, allocations: Dict[str, Any], 
                                   priorities: list, budget: float) -> Dict[str, Any]:
        """
        Analyze multiple allocation decisions in batch
        
        Args:
            allocations: Dictionary of region -> allocation details
            priorities: List of priority data for all regions
            budget: Total budget
            
        Returns:
            Dictionary of region -> agent analysis
        """
        results = {}
        
        for region_name, allocation_details in allocations.items():
            # Find priority data for this region
            priority_data = next(
                (p for p in priorities if p['region'] == region_name),
                None
            )
            
            if not priority_data:
                continue
            
            # Prepare decision data
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
            
            # Get agent analysis
            analysis_result = self.analyze_decision(decision_data)
            
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
        
        # Infer stakeholder groups from indicators
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
    
    def get_fairness_metrics(self, allocations: Dict[str, Any]) -> Dict[str, Any]:
        """
        Request fairness analysis for allocations
        
        Args:
            allocations: Dictionary of region allocations
            
        Returns:
            Fairness metrics and analysis
        """
        try:
            payload = {
                "type": "fairness_analysis",
                "data": {
                    "allocations": allocations
                },
                "timestamp": datetime.now().isoformat()
            }
            
            response = requests.post(
                self.agent_endpoint,
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return {
                    "status": "success",
                    "metrics": response.json()
                }
            else:
                return {
                    "status": "error",
                    "message": f"Status {response.status_code}"
                }
                
        except Exception as e:
            logger.error(f"Fairness analysis failed: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def get_transparency_report(self, decision_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Request transparency report for a decision
        
        Args:
            decision_data: Decision details
            
        Returns:
            Transparency report with explanations
        """
        try:
            payload = {
                "type": "transparency_report",
                "data": decision_data,
                "timestamp": datetime.now().isoformat()
            }
            
            response = requests.post(
                self.agent_endpoint,
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return {
                    "status": "success",
                    "report": response.json()
                }
            else:
                return {
                    "status": "error",
                    "message": f"Status {response.status_code}"
                }
                
        except Exception as e:
            logger.error(f"Transparency report failed: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }


# Singleton instance
_client_instance = None

def get_agent_client() -> AgentClient:
    """Get singleton instance of AgentClient"""
    global _client_instance
    if _client_instance is None:
        _client_instance = AgentClient()
    return _client_instance
