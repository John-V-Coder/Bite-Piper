# Cross-demographic impact assessment

"""
Impact Assessor Module for Bite-Piper
Assesses cross-demographic impacts of decisions using civic data and philosophical frameworks
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from civic_client import CivicDataClient, CivicDataException
from philosophical_framework import PhilosophicalFramework


class ImpactCategory(Enum):
    """Categories of impact to assess"""
    ECONOMIC = "economic"
    SOCIAL = "social"
    EDUCATIONAL = "educational"
    HEALTH = "health"
    ENVIRONMENTAL = "environmental"
    CULTURAL = "cultural"


class DemographicGroup(Enum):
    """Demographic groups to analyze"""
    LOW_INCOME = "low_income"
    RURAL = "rural"
    URBAN = "urban"
    YOUTH = "youth"
    ELDERLY = "elderly"
    WOMEN = "women"
    MINORITIES = "minorities"


@dataclass
class ImpactAssessment:
    """Result of impact assessment"""
    category: ImpactCategory
    affected_groups: List[str]
    impact_magnitude: float  # 0.0 to 1.0
    impact_direction: str  # positive, negative, neutral
    confidence: float
    evidence: List[str]


class ImpactAssessor:
    """Assesses cross-demographic impacts of civic decisions"""
    
    def __init__(self, civic_client: Optional[CivicDataClient] = None,
                 api_keys: Optional[Dict[str, str]] = None):
        self.civic_client = civic_client or CivicDataClient(api_keys)
        self.framework = PhilosophicalFramework()
    
    def assess_decision_impact(
        self,
        decision_data: Dict[str, Any],
        regions: List[Dict[str, Any]],
        demographic_groups: Optional[List[str]] = None,
        baseline_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Comprehensive cross-demographic impact assessment
        
        Args:
            decision_data: Decision or allocation data
            regions: Regions affected by decision
            demographic_groups: Specific demographic groups to analyze
            baseline_data: Baseline data for comparison
            
        Returns:
            Comprehensive impact assessment
        """
        
        assessment = {
            'decision_id': decision_data.get('id', 'unknown'),
            'impact_categories': {},
            'demographic_impacts': {},
            'intersectional_impacts': [],
            'positive_impacts': [],
            'negative_impacts': [],
            'mitigation_strategies': [],
            'philosophical_analysis': {},
            'overall_assessment': {}
        }
        
        # Gather civic data for impact analysis
        regional_data = self._gather_regional_impact_data(regions)
        
        # Assess impact across categories
        for category in ImpactCategory:
            category_impact = self._assess_category_impact(
                category, decision_data, regional_data, baseline_data
            )
            assessment['impact_categories'][category.value] = category_impact
        
        # Assess demographic-specific impacts
        demographic_impacts = self._assess_demographic_impacts(
            decision_data, regional_data, demographic_groups
        )
        assessment['demographic_impacts'] = demographic_impacts
        
        # Assess intersectional impacts (hooks' framework)
        intersectional = self._assess_intersectional_impacts(
            decision_data, regional_data, demographic_impacts
        )
        assessment['intersectional_impacts'] = intersectional
        
        # Identify positive and negative impacts
        positive, negative = self._categorize_impacts(assessment)
        assessment['positive_impacts'] = positive
        assessment['negative_impacts'] = negative
        
        # Generate mitigation strategies for negative impacts
        mitigation = self._generate_mitigation_strategies(negative)
        assessment['mitigation_strategies'] = mitigation
        
        # Apply philosophical analysis
        philosophical = self._apply_philosophical_impact_analysis(
            decision_data, assessment
        )
        assessment['philosophical_analysis'] = philosophical
        
        # Generate overall assessment
        assessment['overall_assessment'] = self._generate_overall_assessment(assessment)
        
        return assessment
    
    def _gather_regional_impact_data(
        self,
        regions: List[Dict[str, Any]]
    ) -> Dict[str, Dict[str, Any]]:
        """Gather data for impact assessment"""
        
        regional_data = {}
        
        for region in regions:
            region_id = region.get('id', region.get('code', 'unknown'))
            
            try:
                location = {
                    'type': region.get('type', 'country'),
                    'code': region.get('code', region_id)
                }
                
                profile = self.civic_client.get_socioeconomic_profile(location)
                equity_scores = self.civic_client.calculate_equity_scores(location)
                
                regional_data[region_id] = {
                    'region': region,
                    'profile': profile,
                    'equity_scores': equity_scores,
                    'indicators': profile.get('indicators', {})
                }
                
            except CivicDataException as e:
                regional_data[region_id] = {
                    'region': region,
                    'error': str(e)
                }
        
        return regional_data
    
    def _assess_category_impact(
        self,
        category: ImpactCategory,
        decision_data: Dict[str, Any],
        regional_data: Dict[str, Dict[str, Any]],
        baseline_data: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Assess impact in a specific category"""
        
        if category == ImpactCategory.ECONOMIC:
            return self._assess_economic_impact(decision_data, regional_data)
        elif category == ImpactCategory.EDUCATIONAL:
            return self._assess_educational_impact(decision_data, regional_data)
        elif category == ImpactCategory.HEALTH:
            return self._assess_health_impact(decision_data, regional_data)
        elif category == ImpactCategory.SOCIAL:
            return self._assess_social_impact(decision_data, regional_data)
        else:
            return {
                'category': category.value,
                'assessed': False,
                'reason': 'Data not available'
            }
    
    def _assess_economic_impact(
        self,
        decision_data: Dict[str, Any],
        regional_data: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Assess economic impact"""
        
        impact = {
            'category': 'economic',
            'overall_impact': 'positive',
            'magnitude': 0.0,
            'affected_regions': [],
            'evidence': []
        }
        
        allocations = decision_data.get('allocations', {})
        
        # Analyze poverty reduction potential
        for region_id, data in regional_data.items():
            if data.get('error'):
                continue
            
            equity_scores = data.get('equity_scores', {})
            poverty_score = equity_scores.get('dimension_scores', {}).get('poverty', 0.5)
            allocation = allocations.get(region_id, 0)
            
            # High allocation to high-poverty region = positive impact
            if poverty_score < 0.4 and allocation > 0:
                impact['affected_regions'].append(region_id)
                impact['evidence'].append(
                    f"Region {region_id}: Allocation targets high poverty (score: {poverty_score:.2f})"
                )
                impact['magnitude'] += 0.2
        
        # Calculate overall magnitude
        if impact['affected_regions']:
            impact['magnitude'] = min(1.0, impact['magnitude'])
        
        return impact
    
    def _assess_educational_impact(
        self,
        decision_data: Dict[str, Any],
        regional_data: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Assess educational impact"""
        
        impact = {
            'category': 'educational',
            'overall_impact': 'neutral',
            'magnitude': 0.0,
            'affected_regions': [],
            'evidence': []
        }
        
        # Check if decision includes education component
        if decision_data.get('education_focus'):
            impact['overall_impact'] = 'positive'
            impact['magnitude'] = 0.6
            impact['evidence'].append('Decision includes explicit education component')
        
        # Analyze education gaps
        for region_id, data in regional_data.items():
            if data.get('error'):
                continue
            
            equity_scores = data.get('equity_scores', {})
            education_score = equity_scores.get('dimension_scores', {}).get('education', 1.0)
            
            if education_score < 0.5:
                impact['affected_regions'].append(region_id)
                impact['evidence'].append(
                    f"Region {region_id}: Low education baseline (score: {education_score:.2f})"
                )
        
        return impact
    
    def _assess_health_impact(
        self,
        decision_data: Dict[str, Any],
        regional_data: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Assess health impact"""
        
        impact = {
            'category': 'health',
            'overall_impact': 'neutral',
            'magnitude': 0.0,
            'affected_regions': [],
            'evidence': []
        }
        
        # Analyze health indicators from civic data
        for region_id, data in regional_data.items():
            if data.get('error'):
                continue
            
            indicators = data.get('indicators', {})
            
            # Check health expenditure
            if 'SH.XPD.CHEX.GD.ZS' in indicators:
                health_data = indicators['SH.XPD.CHEX.GD.ZS']
                if health_data:
                    health_exp = health_data[0].get('value', 0)
                    if health_exp < 5:
                        impact['affected_regions'].append(region_id)
                        impact['evidence'].append(
                            f"Region {region_id}: Low health investment ({health_exp:.1f}% GDP)"
                        )
        
        if impact['affected_regions']:
            impact['overall_impact'] = 'positive'
            impact['magnitude'] = 0.4
            impact['evidence'].append('Funding may improve health outcomes in underserved regions')
        
        return impact
    
    def _assess_social_impact(
        self,
        decision_data: Dict[str, Any],
        regional_data: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Assess social impact"""
        
        impact = {
            'category': 'social',
            'overall_impact': 'positive',
            'magnitude': 0.5,
            'affected_regions': list(regional_data.keys()),
            'evidence': []
        }
        
        # Social cohesion and equity
        impact['evidence'].append(
            'Resource allocation addresses inequality, promoting social cohesion'
        )
        
        # Community empowerment (Freire)
        if decision_data.get('participatory_design'):
            impact['magnitude'] += 0.2
            impact['evidence'].append(
                'Participatory design empowers communities (Freirean framework)'
            )
        
        return impact
    
    def _assess_demographic_impacts(
        self,
        decision_data: Dict[str, Any],
        regional_data: Dict[str, Dict[str, Any]],
        demographic_groups: Optional[List[str]]
    ) -> Dict[str, Dict[str, Any]]:
        """Assess impacts on specific demographic groups"""
        
        demographic_impacts = {}
        
        # Assess impact on low-income populations
        low_income_impact = self._assess_low_income_impact(decision_data, regional_data)
        demographic_impacts['low_income'] = low_income_impact
        
        # Assess rural vs urban impact
        rural_urban = self._assess_rural_urban_impact(decision_data, regional_data)
        demographic_impacts['rural'] = rural_urban['rural']
        demographic_impacts['urban'] = rural_urban['urban']
        
        # Assess women's impact (if data available)
        women_impact = self._assess_women_impact(decision_data, regional_data)
        if women_impact:
            demographic_impacts['women'] = women_impact
        
        return demographic_impacts
    
    def _assess_low_income_impact(
        self,
        decision_data: Dict[str, Any],
        regional_data: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Assess impact on low-income populations"""
        
        impact = {
            'demographic': 'low_income',
            'impact_direction': 'positive',
            'magnitude': 0.0,
            'evidence': [],
            'affected_regions': []
        }
        
        allocations = decision_data.get('allocations', {})
        
        for region_id, data in regional_data.items():
            if data.get('error'):
                continue
            
            equity_scores = data.get('equity_scores', {})
            income_score = equity_scores.get('dimension_scores', {}).get('income', 0.5)
            poverty_score = equity_scores.get('dimension_scores', {}).get('poverty', 0.5)
            
            # Low income/poverty = benefits low-income population
            if income_score < 0.4 or poverty_score < 0.4:
                allocation = allocations.get(region_id, 0)
                if allocation > 0:
                    impact['affected_regions'].append(region_id)
                    impact['evidence'].append(
                        f"Region {region_id}: Targets low-income population (income: {income_score:.2f}, poverty: {poverty_score:.2f})"
                    )
                    impact['magnitude'] += 0.3
        
        impact['magnitude'] = min(1.0, impact['magnitude'])
        
        return impact
    
    def _assess_rural_urban_impact(
        self,
        decision_data: Dict[str, Any],
        regional_data: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Dict[str, Any]]:
        """Assess differential impact on rural vs urban areas"""
        
        rural_impact = {
            'demographic': 'rural',
            'impact_direction': 'neutral',
            'magnitude': 0.0,
            'evidence': []
        }
        
        urban_impact = {
            'demographic': 'urban',
            'impact_direction': 'neutral',
            'magnitude': 0.0,
            'evidence': []
        }
        
        allocations = decision_data.get('allocations', {})
        
        rural_allocations = []
        urban_allocations = []
        
        for region_id, data in regional_data.items():
            if data.get('error'):
                continue
            
            region = data.get('region', {})
            region_type = region.get('region_type', 'unknown')
            allocation = allocations.get(region_id, 0)
            
            if region_type == 'rural':
                rural_allocations.append(allocation)
            elif region_type == 'urban':
                urban_allocations.append(allocation)
        
        # Compare allocations
        if rural_allocations and urban_allocations:
            avg_rural = sum(rural_allocations) / len(rural_allocations)
            avg_urban = sum(urban_allocations) / len(urban_allocations)
            
            if avg_rural > avg_urban:
                rural_impact['impact_direction'] = 'positive'
                rural_impact['magnitude'] = 0.7
                rural_impact['evidence'].append(
                    f"Rural areas receive higher average allocation (${avg_rural:,.0f} vs ${avg_urban:,.0f})"
                )
            elif avg_urban > avg_rural:
                urban_impact['impact_direction'] = 'positive'
                urban_impact['magnitude'] = 0.6
                urban_impact['evidence'].append(
                    f"Urban areas receive higher average allocation"
                )
        
        return {'rural': rural_impact, 'urban': urban_impact}
    
    def _assess_women_impact(
        self,
        decision_data: Dict[str, Any],
        regional_data: Dict[str, Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """Assess impact on women (if gender data available)"""
        
        impact = {
            'demographic': 'women',
            'impact_direction': 'neutral',
            'magnitude': 0.0,
            'evidence': []
        }
        
        # Check if decision has explicit gender component
        if decision_data.get('gender_focus'):
            impact['impact_direction'] = 'positive'
            impact['magnitude'] = 0.7
            impact['evidence'].append('Decision includes explicit gender equity component')
            return impact
        
        return None
    
    def _assess_intersectional_impacts(
        self,
        decision_data: Dict[str, Any],
        regional_data: Dict[str, Dict[str, Any]],
        demographic_impacts: Dict[str, Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Assess intersectional impacts (hooks' framework)"""
        
        hooks = self.framework.get_thinker_perspective('hooks')
        
        intersectional = []
        
        # Identify groups with multiple disadvantages
        for region_id, data in regional_data.items():
            if data.get('error'):
                continue
            
            equity_scores = data.get('equity_scores', {})
            dimension_scores = equity_scores.get('dimension_scores', {})
            
            disadvantages = []
            if dimension_scores.get('poverty', 1) < 0.3:
                disadvantages.append('economic')
            if dimension_scores.get('education', 1) < 0.5:
                disadvantages.append('educational')
            if dimension_scores.get('income', 1) < 0.4:
                disadvantages.append('income')
            
            region = data.get('region', {})
            if region.get('region_type') == 'rural':
                disadvantages.append('geographic')
            
            # Intersectional impact if 2+ disadvantages
            if len(disadvantages) >= 2:
                intersectional.append({
                    'region': region_id,
                    'intersecting_disadvantages': disadvantages,
                    'count': len(disadvantages),
                    'impact': 'high_positive',
                    'explanation': f"Decision addresses {len(disadvantages)} intersecting disadvantages (hooks' intersectionality)"
                })
        
        return intersectional
    
    def _categorize_impacts(
        self,
        assessment: Dict[str, Any]
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Categorize impacts as positive or negative"""
        
        positive = []
        negative = []
        
        # Category impacts
        for category, impact in assessment['impact_categories'].items():
            if impact.get('overall_impact') == 'positive':
                positive.append({
                    'type': 'category',
                    'category': category,
                    'magnitude': impact.get('magnitude', 0),
                    'evidence': impact.get('evidence', [])
                })
            elif impact.get('overall_impact') == 'negative':
                negative.append({
                    'type': 'category',
                    'category': category,
                    'magnitude': impact.get('magnitude', 0),
                    'evidence': impact.get('evidence', [])
                })
        
        # Demographic impacts
        for demographic, impact in assessment['demographic_impacts'].items():
            if impact.get('impact_direction') == 'positive':
                positive.append({
                    'type': 'demographic',
                    'demographic': demographic,
                    'magnitude': impact.get('magnitude', 0),
                    'evidence': impact.get('evidence', [])
                })
            elif impact.get('impact_direction') == 'negative':
                negative.append({
                    'type': 'demographic',
                    'demographic': demographic,
                    'magnitude': impact.get('magnitude', 0),
                    'evidence': impact.get('evidence', [])
                })
        
        return positive, negative
    
    def _generate_mitigation_strategies(
        self,
        negative_impacts: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate strategies to mitigate negative impacts"""
        
        strategies = []
        
        for impact in negative_impacts:
            if impact['type'] == 'category':
                strategies.append({
                    'impact_addressed': f"{impact['category']} impact",
                    'strategy': f"Enhance {impact['category']} support programs",
                    'approach': 'Targeted intervention in affected regions'
                })
            elif impact['type'] == 'demographic':
                strategies.append({
                    'impact_addressed': f"{impact['demographic']} population",
                    'strategy': f"Specific programs for {impact['demographic']} groups",
                    'approach': 'Ensure inclusive benefits across all demographics'
                })
        
        return strategies
    
    def _apply_philosophical_impact_analysis(
        self,
        decision_data: Dict[str, Any],
        assessment: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply philosophical frameworks to impact analysis"""
        
        philosophical = {
            'frameworks_applied': [],
            'assessments': []
        }
        
        # Sen's capability approach
        sen = self.framework.get_thinker_perspective('sen')
        if sen:
            philosophical['frameworks_applied'].append("Sen's Capability Approach")
            philosophical['assessments'].append({
                'framework': "Sen's Capability Approach",
                'assessment': 'Decision enhances capabilities by targeting poverty and education gaps',
                'compliance': 'high'
            })
        
        # Nussbaum's capabilities list
        nussbaum = self.framework.get_thinker_perspective('nussbaum')
        if nussbaum:
            philosophical['frameworks_applied'].append("Nussbaum's Central Capabilities")
            philosophical['assessments'].append({
                'framework': "Nussbaum's Central Capabilities",
                'assessment': 'Decision supports central capabilities: life, health, education, practical reason',
                'compliance': 'medium'
            })
        
        return philosophical
    
    def _generate_overall_assessment(
        self,
        assessment: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate overall impact assessment"""
        
        overall = {
            'overall_impact': 'neutral',
            'impact_score': 0.0,
            'confidence': 0.0,
            'summary': '',
            'key_findings': []
        }
        
        # Calculate impact score
        positive_count = len(assessment['positive_impacts'])
        negative_count = len(assessment['negative_impacts'])
        
        if positive_count > negative_count * 2:
            overall['overall_impact'] = 'positive'
            overall['impact_score'] = 0.7
        elif negative_count > positive_count:
            overall['overall_impact'] = 'negative'
            overall['impact_score'] = -0.3
        else:
            overall['overall_impact'] = 'mixed'
            overall['impact_score'] = 0.3
        
        # Key findings
        overall['key_findings'] = [
            f"{positive_count} positive impacts identified",
            f"{negative_count} negative impacts identified",
            f"{len(assessment['intersectional_impacts'])} intersectional impacts addressed"
        ]
        
        # Summary
        if overall['overall_impact'] == 'positive':
            overall['summary'] = (
                f"Decision demonstrates predominantly positive impacts across {positive_count} dimensions, "
                f"with strong benefits for disadvantaged populations."
            )
        else:
            overall['summary'] = (
                f"Decision shows mixed impacts. Recommend implementing mitigation strategies "
                f"for {negative_count} identified negative impacts."
            )
        
        return overall
