# Resource distribution fairness logic

"""
Allocation Fairness Module for Bite-Piper
Evaluates fairness of resource allocation using multiple philosophical frameworks
"""

from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from philosophical_framework import PhilosophicalFramework, PhilosophicalPerspective, EthicalCategory


class FairnessMetric(Enum):
    """Different metrics for evaluating allocation fairness"""
    RAWLSIAN_MAXIMIN = "rawlsian_maximin"  # Maximize minimum allocation
    UTILITARIAN = "utilitarian"  # Maximize total welfare
    PROPORTIONAL = "proportional"  # Proportional to need
    EGALITARIAN = "egalitarian"  # Equal distribution
    CAPABILITY_BASED = "capability_based"  # Based on capability gaps


@dataclass
class AllocationResult:
    """Result of allocation analysis"""
    region_id: str
    allocated_amount: float
    needs_score: float
    fairness_score: float
    philosophical_justification: str
    equity_adjustments: Dict[str, float]


class AllocationFairnessAnalyzer:
    """Analyzes fairness of resource allocations using philosophical frameworks"""
    
    def __init__(self):
        self.framework = PhilosophicalFramework()
        
    def evaluate_allocation_fairness(
        self,
        allocations: Dict[str, float],
        needs_data: Dict[str, Dict[str, Any]],
        metric: FairnessMetric = FairnessMetric.RAWLSIAN_MAXIMIN
    ) -> Dict[str, Any]:
        """
        Evaluate fairness of proposed allocations
        
        Args:
            allocations: Dict mapping region_id to allocated amount
            needs_data: Dict mapping region_id to needs indicators
            metric: Fairness metric to use
            
        Returns:
            Comprehensive fairness assessment
        """
        assessment = {
            'metric_used': metric.value,
            'overall_fairness_score': 0.0,
            'regional_assessments': [],
            'philosophical_analysis': [],
            'equity_violations': [],
            'recommendations': []
        }
        
        # Apply Rawlsian analysis
        rawlsian_analysis = self._apply_rawlsian_analysis(allocations, needs_data)
        assessment['philosophical_analysis'].append(rawlsian_analysis)
        
        # Apply Sen's capability approach
        capability_analysis = self._apply_capability_analysis(allocations, needs_data)
        assessment['philosophical_analysis'].append(capability_analysis)
        
        # Apply Aristotelian virtue ethics
        virtue_analysis = self._apply_aristotelian_analysis(allocations, needs_data)
        assessment['philosophical_analysis'].append(virtue_analysis)
        
        # Detect equity violations
        violations = self._detect_equity_violations(allocations, needs_data)
        assessment['equity_violations'] = violations
        
        # Calculate overall fairness score
        assessment['overall_fairness_score'] = self._calculate_fairness_score(
            rawlsian_analysis,
            capability_analysis,
            virtue_analysis,
            violations
        )
        
        # Generate recommendations
        assessment['recommendations'] = self._generate_fairness_recommendations(
            assessment
        )
        
        return assessment
    
    def _apply_rawlsian_analysis(
        self,
        allocations: Dict[str, float],
        needs_data: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Apply Rawlsian justice principles (difference principle)"""
        
        rawls = self.framework.get_thinker_perspective('rawls')
        
        # Find least advantaged region
        least_advantaged = None
        min_wellbeing = float('inf')
        
        for region_id, needs in needs_data.items():
            wellbeing_score = self._calculate_wellbeing_score(needs)
            if wellbeing_score < min_wellbeing:
                min_wellbeing = wellbeing_score
                least_advantaged = region_id
        
        # Check if allocation benefits least advantaged
        least_advantaged_allocation = allocations.get(least_advantaged, 0)
        avg_allocation = sum(allocations.values()) / len(allocations) if allocations else 0
        
        benefits_least_advantaged = least_advantaged_allocation >= avg_allocation
        
        return {
            'framework': 'Rawlsian Justice',
            'principles_applied': rawls.core_principles if rawls else [],
            'least_advantaged_region': least_advantaged,
            'least_advantaged_allocation': least_advantaged_allocation,
            'average_allocation': avg_allocation,
            'benefits_least_advantaged': benefits_least_advantaged,
            'compliance_score': 1.0 if benefits_least_advantaged else 0.3,
            'rationale': f"Rawls' difference principle requires that inequalities benefit the least advantaged. "
                        f"Region {least_advantaged} is least advantaged and receives "
                        f"{'above' if benefits_least_advantaged else 'below'} average allocation."
        }
    
    def _apply_capability_analysis(
        self,
        allocations: Dict[str, float],
        needs_data: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Apply Sen's capability approach"""
        
        sen = self.framework.get_thinker_perspective('sen')
        
        capability_gaps = {}
        for region_id, needs in needs_data.items():
            # Calculate capability gaps (lower scores = bigger gaps)
            capability_gaps[region_id] = {
                'education': 1.0 - needs.get('literacy_rate', 0.7),
                'economic': 1.0 - min(1.0, needs.get('income_per_capita', 25000) / 50000),
                'health': 1.0 - needs.get('health_index', 0.7),
                'total_gap': 0.0
            }
            capability_gaps[region_id]['total_gap'] = sum([
                capability_gaps[region_id]['education'],
                capability_gaps[region_id]['economic'],
                capability_gaps[region_id]['health']
            ]) / 3
        
        # Check if allocation prioritizes capability enhancement
        allocation_per_gap = {}
        for region_id in allocations:
            gap = capability_gaps[region_id]['total_gap']
            allocation_per_gap[region_id] = allocations[region_id] / max(gap, 0.1)
        
        # Variance in allocation per gap (lower is more fair)
        values = list(allocation_per_gap.values())
        avg = sum(values) / len(values) if values else 0
        variance = sum((v - avg) ** 2 for v in values) / len(values) if values else 0
        
        compliance_score = max(0, 1.0 - (variance / (avg ** 2)) if avg > 0 else 0)
        
        return {
            'framework': 'Capability Approach (Sen)',
            'principles_applied': sen.core_principles if sen else [],
            'capability_gaps': capability_gaps,
            'allocation_per_gap': allocation_per_gap,
            'variance': variance,
            'compliance_score': compliance_score,
            'rationale': "Sen's capability approach focuses on enhancing freedoms and capabilities. "
                        f"Allocation {'effectively' if compliance_score > 0.7 else 'insufficiently'} "
                        "targets capability gaps across regions."
        }
    
    def _apply_aristotelian_analysis(
        self,
        allocations: Dict[str, float],
        needs_data: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Apply Aristotelian virtue ethics (golden mean)"""
        
        aristotle = self.framework.get_thinker_perspective('aristotle')
        
        # Check for balance (avoiding extremes)
        allocation_values = list(allocations.values())
        if not allocation_values:
            return {
                'framework': 'Aristotelian Virtue Ethics',
                'compliance_score': 0.0,
                'rationale': 'No allocations to analyze'
            }
        
        max_allocation = max(allocation_values)
        min_allocation = min(allocation_values)
        avg_allocation = sum(allocation_values) / len(allocation_values)
        
        # Golden mean: allocations shouldn't have extreme disparities
        disparity_ratio = max_allocation / min_allocation if min_allocation > 0 else float('inf')
        
        # Score based on avoiding extremes (ratio should be < 5 for good balance)
        if disparity_ratio < 2:
            compliance_score = 1.0
        elif disparity_ratio < 5:
            compliance_score = 0.7
        elif disparity_ratio < 10:
            compliance_score = 0.4
        else:
            compliance_score = 0.2
        
        return {
            'framework': 'Aristotelian Virtue Ethics',
            'principles_applied': aristotle.core_principles if aristotle else [],
            'max_allocation': max_allocation,
            'min_allocation': min_allocation,
            'disparity_ratio': disparity_ratio,
            'compliance_score': compliance_score,
            'rationale': f"Aristotle's golden mean advocates avoiding extremes. "
                        f"Allocation disparity ratio of {disparity_ratio:.2f} "
                        f"{'achieves' if compliance_score > 0.7 else 'violates'} balanced distribution."
        }
    
    def _detect_equity_violations(
        self,
        allocations: Dict[str, float],
        needs_data: Dict[str, Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Detect violations of equity principles"""
        
        violations = []
        
        # Check for regressive allocation (wealthy get more)
        for region_id, allocation in allocations.items():
            needs = needs_data.get(region_id, {})
            poverty_rate = needs.get('poverty_rate', 0.3)
            
            # If low poverty but high allocation, flag it
            if poverty_rate < 0.2 and allocation > sum(allocations.values()) / len(allocations) * 1.5:
                violations.append({
                    'type': 'regressive_allocation',
                    'region': region_id,
                    'severity': 'high',
                    'description': f"Region {region_id} has low poverty ({poverty_rate:.1%}) "
                                  f"but receives disproportionately high allocation",
                    'philosophical_challenge': "Violates Rawlsian difference principle and equity frameworks"
                })
        
        # Check for geographic bias
        urban_regions = [r for r, n in needs_data.items() if n.get('region_type') == 'urban']
        rural_regions = [r for r, n in needs_data.items() if n.get('region_type') == 'rural']
        
        if urban_regions and rural_regions:
            avg_urban = sum(allocations.get(r, 0) for r in urban_regions) / len(urban_regions)
            avg_rural = sum(allocations.get(r, 0) for r in rural_regions) / len(rural_regions)
            
            if avg_urban > avg_rural * 1.5:
                violations.append({
                    'type': 'geographic_bias',
                    'severity': 'medium',
                    'description': f"Urban regions receive {avg_urban/avg_rural:.1f}x more than rural regions on average",
                    'philosophical_challenge': "Foucauldian analysis: urban-centric power structures evident"
                })
        
        return violations
    
    def _calculate_wellbeing_score(self, needs: Dict[str, Any]) -> float:
        """Calculate overall wellbeing score from needs indicators"""
        
        # Higher score = better wellbeing
        poverty_rate = needs.get('poverty_rate', 0.3)
        literacy_rate = needs.get('literacy_rate', 0.7)
        income = needs.get('income_per_capita', 25000)
        
        # Normalize and combine
        poverty_component = 1.0 - poverty_rate
        literacy_component = literacy_rate
        income_component = min(1.0, income / 50000)
        
        return (poverty_component * 0.4 + literacy_component * 0.3 + income_component * 0.3)
    
    def _calculate_fairness_score(
        self,
        rawlsian: Dict,
        capability: Dict,
        aristotelian: Dict,
        violations: List
    ) -> float:
        """Calculate overall fairness score"""
        
        # Weighted combination of framework compliance scores
        base_score = (
            rawlsian.get('compliance_score', 0) * 0.4 +
            capability.get('compliance_score', 0) * 0.4 +
            aristotelian.get('compliance_score', 0) * 0.2
        )
        
        # Penalty for violations
        violation_penalty = len([v for v in violations if v['severity'] == 'high']) * 0.15
        violation_penalty += len([v for v in violations if v['severity'] == 'medium']) * 0.08
        
        return max(0.0, min(1.0, base_score - violation_penalty))
    
    def _generate_fairness_recommendations(
        self,
        assessment: Dict[str, Any]
    ) -> List[str]:
        """Generate recommendations to improve fairness"""
        
        recommendations = []
        
        fairness_score = assessment['overall_fairness_score']
        
        if fairness_score < 0.7:
            recommendations.append(
                "Overall fairness score is below target. Consider rebalancing allocations."
            )
        
        # Check Rawlsian compliance
        for analysis in assessment['philosophical_analysis']:
            if analysis['framework'] == 'Rawlsian Justice':
                if not analysis.get('benefits_least_advantaged', False):
                    recommendations.append(
                        f"Increase allocation to least advantaged region ({analysis['least_advantaged_region']}) "
                        "to comply with Rawlsian difference principle."
                    )
        
        # Address violations
        for violation in assessment['equity_violations']:
            if violation['type'] == 'regressive_allocation':
                recommendations.append(
                    f"Review allocation to {violation['region']} - appears regressive given low poverty rate."
                )
            elif violation['type'] == 'geographic_bias':
                recommendations.append(
                    "Address urban-rural allocation disparity through equity adjustments."
                )
        
        if not recommendations:
            recommendations.append("Allocation demonstrates strong fairness across multiple philosophical frameworks.")
        
        return recommendations
    
    def compare_allocation_scenarios(
        self,
        scenarios: Dict[str, Dict[str, float]],
        needs_data: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Compare fairness of multiple allocation scenarios"""
        
        comparisons = {
            'scenarios': {},
            'recommended_scenario': None,
            'recommendation_rationale': ''
        }
        
        best_score = 0.0
        best_scenario = None
        
        for scenario_name, allocations in scenarios.items():
            assessment = self.evaluate_allocation_fairness(allocations, needs_data)
            comparisons['scenarios'][scenario_name] = assessment
            
            if assessment['overall_fairness_score'] > best_score:
                best_score = assessment['overall_fairness_score']
                best_scenario = scenario_name
        
        comparisons['recommended_scenario'] = best_scenario
        comparisons['recommendation_rationale'] = (
            f"Scenario '{best_scenario}' achieves highest fairness score ({best_score:.2f}) "
            "based on Rawlsian, capability, and Aristotelian frameworks."
        )
        
        return comparisons