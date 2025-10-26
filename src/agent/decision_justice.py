 # Fairness assessment in resource allocation

"""
Decision Justice Module for Bite-Piper
Evaluates justice and fairness of civic decisions using philosophical frameworks
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from philosophical_framework import PhilosophicalFramework, PhilosophicalPerspective


class JusticeType(Enum):
    """Types of justice to evaluate"""
    DISTRIBUTIVE = "distributive"  # Fair distribution of resources
    PROCEDURAL = "procedural"  # Fair decision-making processes
    RECOGNITIONAL = "recognitional"  # Recognition and respect for all groups
    RESTORATIVE = "restorative"  # Addressing past injustices


@dataclass
class JusticeAssessment:
    """Result of justice evaluation"""
    decision_id: str
    justice_type: JusticeType
    score: float
    philosophical_frameworks_applied: List[str]
    strengths: List[str]
    concerns: List[str]
    recommendations: List[str]


class DecisionJusticeEvaluator:
    """Evaluates justice and fairness of civic decisions"""
    
    def __init__(self):
        self.framework = PhilosophicalFramework()
    
    def evaluate_decision_justice(
        self,
        decision_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Comprehensive justice evaluation of a decision
        
        Args:
            decision_data: Information about the decision
            context: Contextual information (stakeholders, history, etc.)
            
        Returns:
            Comprehensive justice assessment
        """
        assessment = {
            'decision_id': decision_data.get('id', 'unknown'),
            'decision_type': decision_data.get('type', 'resource_allocation'),
            'justice_dimensions': {},
            'overall_justice_score': 0.0,
            'philosophical_evaluations': [],
            'ethical_concerns': [],
            'recommendations': []
        }
        
        # Evaluate distributive justice
        distributive = self._evaluate_distributive_justice(decision_data, context)
        assessment['justice_dimensions']['distributive'] = distributive
        
        # Evaluate procedural justice
        procedural = self._evaluate_procedural_justice(decision_data, context)
        assessment['justice_dimensions']['procedural'] = procedural
        
        # Evaluate recognitional justice
        recognitional = self._evaluate_recognitional_justice(decision_data, context)
        assessment['justice_dimensions']['recognitional'] = recognitional
        
        # Evaluate restorative justice
        restorative = self._evaluate_restorative_justice(decision_data, context)
        assessment['justice_dimensions']['restorative'] = restorative
        
        # Apply philosophical frameworks
        philosophical_evals = self._apply_philosophical_frameworks(decision_data, context)
        assessment['philosophical_evaluations'] = philosophical_evals
        
        # Calculate overall justice score
        assessment['overall_justice_score'] = self._calculate_overall_justice_score(
            distributive, procedural, recognitional, restorative
        )
        
        # Generate recommendations
        assessment['recommendations'] = self._generate_justice_recommendations(assessment)
        
        return assessment
    
    def _evaluate_distributive_justice(
        self,
        decision_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Evaluate fairness of resource distribution (Rawls, Sen)"""
        
        rawls = self.framework.get_thinker_perspective('rawls')
        sen = self.framework.get_thinker_perspective('sen')
        
        evaluation = {
            'dimension': 'distributive_justice',
            'score': 0.0,
            'criteria_evaluated': [],
            'strengths': [],
            'concerns': []
        }
        
        allocations = decision_data.get('allocations', {})
        needs_data = context.get('needs_data', {})
        
        # Rawlsian criterion: Does it benefit the least advantaged?
        if allocations and needs_data:
            least_advantaged = self._identify_least_advantaged(needs_data)
            avg_allocation = sum(allocations.values()) / len(allocations) if allocations else 0
            least_allocation = allocations.get(least_advantaged, 0)
            
            if least_allocation >= avg_allocation:
                evaluation['strengths'].append(
                    f"Rawlsian: Benefits least advantaged ({least_advantaged})"
                )
                evaluation['score'] += 0.5
            else:
                evaluation['concerns'].append(
                    f"Rawlsian concern: Least advantaged ({least_advantaged}) receives below-average allocation"
                )
        
        # Sen's capability criterion: Does it enhance capabilities?
        capability_enhancement = decision_data.get('capability_enhancement', {})
        if capability_enhancement:
            evaluation['strengths'].append(
                "Sen's approach: Decision targets capability enhancement"
            )
            evaluation['score'] += 0.5
        else:
            evaluation['concerns'].append(
                "Sen's concern: No explicit capability enhancement strategy"
            )
        
        evaluation['criteria_evaluated'] = [
            "Rawlsian difference principle",
            "Sen's capability approach"
        ]
        
        return evaluation
    
    def _evaluate_procedural_justice(
        self,
        decision_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Evaluate fairness of decision-making process (Young, Freire, Ostrom)"""
        
        young = self.framework.get_thinker_perspective('young')
        freire = self.framework.get_thinker_perspective('freire')
        ostrom = self.framework.get_thinker_perspective('ostrom')
        
        evaluation = {
            'dimension': 'procedural_justice',
            'score': 0.0,
            'criteria_evaluated': [],
            'strengths': [],
            'concerns': []
        }
        
        process_data = decision_data.get('process', {})
        
        # Young: Inclusive participation across differences
        stakeholder_participation = process_data.get('stakeholder_participation', [])
        marginalized_included = process_data.get('marginalized_groups_included', False)
        
        if marginalized_included:
            evaluation['strengths'].append(
                "Young's framework: Marginalized groups included in decision-making"
            )
            evaluation['score'] += 0.35
        else:
            evaluation['concerns'].append(
                "Young's concern: Limited evidence of marginalized group participation"
            )
        
        # Freire: Problem-posing vs banking approach
        participatory_design = process_data.get('participatory_design', False)
        community_led = process_data.get('community_led', False)
        
        if participatory_design and community_led:
            evaluation['strengths'].append(
                "Freirean: Problem-posing, community-led approach evident"
            )
            evaluation['score'] += 0.35
        else:
            evaluation['concerns'].append(
                "Freirean concern: Decision appears top-down rather than participatory"
            )
        
        # Ostrom: Polycentric governance
        governance_levels = process_data.get('governance_levels', 1)
        if governance_levels > 1:
            evaluation['strengths'].append(
                "Ostrom's framework: Multi-level governance structure"
            )
            evaluation['score'] += 0.3
        
        evaluation['criteria_evaluated'] = [
            "Inclusive participation (Young)",
            "Community-led design (Freire)",
            "Polycentric governance (Ostrom)"
        ]
        
        return evaluation
    
    def _evaluate_recognitional_justice(
        self,
        decision_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Evaluate recognition and respect for all groups (hooks, Butler)"""
        
        hooks_perspective = self.framework.get_thinker_perspective('hooks')
        butler = self.framework.get_thinker_perspective('butler')
        
        evaluation = {
            'dimension': 'recognitional_justice',
            'score': 0.0,
            'criteria_evaluated': [],
            'strengths': [],
            'concerns': []
        }
        
        # hooks: Intersectional analysis
        intersectional_analysis = decision_data.get('intersectional_analysis', False)
        diverse_knowledge = decision_data.get('diverse_knowledge_systems', False)
        
        if intersectional_analysis:
            evaluation['strengths'].append(
                "hooks' framework: Intersectional analysis of impacts"
            )
            evaluation['score'] += 0.5
        else:
            evaluation['concerns'].append(
                "hooks' concern: No intersectional analysis of compounded disadvantages"
            )
        
        # Butler: Recognition across differences
        inclusive_categorization = decision_data.get('inclusive_categorization', False)
        if inclusive_categorization:
            evaluation['strengths'].append(
                "Butler's framework: Inclusive categorization respects differences"
            )
            evaluation['score'] += 0.5
        
        evaluation['criteria_evaluated'] = [
            "Intersectional analysis (hooks)",
            "Recognition ethics (Butler)"
        ]
        
        return evaluation
    
    def _evaluate_restorative_justice(
        self,
        decision_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Evaluate addressing of historical injustices (Fanon)"""
        
        fanon = self.framework.get_thinker_perspective('fanon')
        
        evaluation = {
            'dimension': 'restorative_justice',
            'score': 0.0,
            'criteria_evaluated': [],
            'strengths': [],
            'concerns': []
        }
        
        # Historical correction
        historical_correction = decision_data.get('historical_correction', False)
        reparations = decision_data.get('reparations_component', False)
        
        if historical_correction or reparations:
            evaluation['strengths'].append(
                "Fanon's framework: Addresses historical injustices and colonial patterns"
            )
            evaluation['score'] += 0.6
        else:
            evaluation['concerns'].append(
                "Fanon's concern: No explicit correction for historical disadvantage"
            )
        
        # Decolonial approach
        indigenous_knowledge = decision_data.get('indigenous_knowledge_centered', False)
        if indigenous_knowledge:
            evaluation['strengths'].append(
                "Decolonial: Centers indigenous and local knowledge systems"
            )
            evaluation['score'] += 0.4
        
        evaluation['criteria_evaluated'] = [
            "Historical reparations (Fanon)",
            "Decolonial knowledge systems"
        ]
        
        return evaluation
    
    def _apply_philosophical_frameworks(
        self,
        decision_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Apply multiple philosophical frameworks to evaluate decision"""
        
        evaluations = []
        
        # Apply Kantian ethics: Treat people as ends
        kant = self.framework.get_thinker_perspective('kant')
        if kant:
            kantian_eval = {
                'framework': 'Kantian Ethics',
                'principles': kant.core_principles,
                'assessment': self._kantian_assessment(decision_data),
                'compliance': 'high' if decision_data.get('respects_dignity', True) else 'low'
            }
            evaluations.append(kantian_eval)
        
        # Apply Aristotelian virtue ethics
        aristotle = self.framework.get_thinker_perspective('aristotle')
        if aristotle:
            aristotelian_eval = {
                'framework': 'Aristotelian Virtue Ethics',
                'principles': aristotle.core_principles,
                'assessment': self._aristotelian_assessment(decision_data),
                'compliance': 'medium'
            }
            evaluations.append(aristotelian_eval)
        
        return evaluations
    
    def _kantian_assessment(self, decision_data: Dict[str, Any]) -> str:
        """Assess from Kantian perspective"""
        respects_dignity = decision_data.get('respects_dignity', True)
        universalizable = decision_data.get('universalizable', False)
        
        if respects_dignity and universalizable:
            return "Decision treats individuals as ends in themselves and follows universalizable principles."
        elif respects_dignity:
            return "Decision respects human dignity but universalizability unclear."
        else:
            return "Concern: Decision may treat individuals as mere means to ends."
    
    def _aristotelian_assessment(self, decision_data: Dict[str, Any]) -> str:
        """Assess from Aristotelian perspective"""
        practical_wisdom = decision_data.get('practical_wisdom_applied', False)
        promotes_flourishing = decision_data.get('promotes_flourishing', False)
        
        if practical_wisdom and promotes_flourishing:
            return "Decision demonstrates practical wisdom (phronesis) and promotes human flourishing (eudaimonia)."
        else:
            return "Consider how decision can better promote community flourishing through practical wisdom."
    
    def _identify_least_advantaged(self, needs_data: Dict[str, Dict[str, Any]]) -> str:
        """Identify least advantaged region/group"""
        min_score = float('inf')
        least_advantaged = None
        
        for region_id, needs in needs_data.items():
            poverty = needs.get('poverty_rate', 0.3)
            literacy = needs.get('literacy_rate', 0.7)
            score = (1 - poverty) * 0.5 + literacy * 0.5
            
            if score < min_score:
                min_score = score
                least_advantaged = region_id
        
        return least_advantaged or 'unknown'
    
    def _calculate_overall_justice_score(
        self,
        distributive: Dict,
        procedural: Dict,
        recognitional: Dict,
        restorative: Dict
    ) -> float:
        """Calculate overall justice score"""
        return (
            distributive.get('score', 0) * 0.35 +
            procedural.get('score', 0) * 0.30 +
            recognitional.get('score', 0) * 0.20 +
            restorative.get('score', 0) * 0.15
        )
    
    def _generate_justice_recommendations(
        self,
        assessment: Dict[str, Any]
    ) -> List[str]:
        """Generate recommendations to improve justice"""
        recommendations = []
        
        for dimension_name, dimension_data in assessment['justice_dimensions'].items():
            if dimension_data.get('score', 0) < 0.6:
                recommendations.append(
                    f"Strengthen {dimension_name.replace('_', ' ')}: {', '.join(dimension_data.get('concerns', []))}"
                )
        
        if assessment['overall_justice_score'] >= 0.8:
            recommendations.append(
                "Strong justice foundations across multiple dimensions. Continue monitoring for equity."
            )
        
        return recommendations or ["Review decision against philosophical frameworks for justice improvements."]