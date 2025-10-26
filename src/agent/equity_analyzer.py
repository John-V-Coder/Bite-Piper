# Equity impact analysis and bias detection

"""
Equity Analyzer Module for Bite-Piper
Analyzes equity impacts and detects biases using civic data and philosophical frameworks
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from civic_client import CivicDataClient, CivicDataException
from philosophical_framework import PhilosophicalFramework


class EquityDimension(Enum):
    """Dimensions of equity to analyze"""
    ECONOMIC = "economic"
    EDUCATIONAL = "educational"
    HEALTH = "health"
    GEOGRAPHIC = "geographic"
    DEMOGRAPHIC = "demographic"
    INTERSECTIONAL = "intersectional"


@dataclass
class EquityImpact:
    """Result of equity impact analysis"""
    dimension: EquityDimension
    affected_regions: List[str]
    impact_score: float  # -1.0 (negative) to +1.0 (positive)
    severity: str
    evidence: List[str]
    recommendations: List[str]


class EquityAnalyzer:
    """Analyzes equity impacts using civic data and philosophical frameworks"""
    
    def __init__(self, civic_client: Optional[CivicDataClient] = None, 
                 api_keys: Optional[Dict[str, str]] = None):
        self.civic_client = civic_client or CivicDataClient(api_keys)
        self.framework = PhilosophicalFramework()
    
    def analyze_equity_impact(
        self,
        decision_data: Dict[str, Any],
        regions: List[Dict[str, Any]],
        baseline_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Comprehensive equity impact analysis
        
        Args:
            decision_data: Decision or allocation data
            regions: List of regions to analyze
            baseline_data: Optional baseline for comparison
            
        Returns:
            Comprehensive equity analysis
        """
        
        analysis = {
            'decision_id': decision_data.get('id', 'unknown'),
            'regions_analyzed': len(regions),
            'equity_dimensions': {},
            'detected_biases': [],
            'impact_summary': {},
            'philosophical_assessments': [],
            'recommendations': [],
            'data_quality': {}
        }
        
        # Gather civic data for all regions
        regional_profiles = self._gather_regional_data(regions)
        analysis['regional_profiles'] = regional_profiles
        
        # Validate data quality
        data_quality = self._assess_data_quality(regional_profiles)
        analysis['data_quality'] = data_quality
        
        # Analyze each equity dimension
        for dimension in EquityDimension:
            dimension_analysis = self._analyze_dimension(
                dimension, decision_data, regional_profiles, baseline_data
            )
            analysis['equity_dimensions'][dimension.value] = dimension_analysis
        
        # Detect equity biases using civic data
        biases = self._detect_equity_biases(decision_data, regional_profiles)
        analysis['detected_biases'] = biases
        
        # Apply philosophical frameworks
        philosophical = self._apply_philosophical_equity_analysis(
            decision_data, regional_profiles
        )
        analysis['philosophical_assessments'] = philosophical
        
        # Generate impact summary
        analysis['impact_summary'] = self._generate_impact_summary(analysis)
        
        # Generate recommendations
        analysis['recommendations'] = self._generate_equity_recommendations(analysis)
        
        return analysis
    
    def _gather_regional_data(
        self,
        regions: List[Dict[str, Any]]
    ) -> Dict[str, Dict[str, Any]]:
        """Gather civic data for all regions"""
        
        regional_data = {}
        
        for region in regions:
            region_id = region.get('id', region.get('code', 'unknown'))
            
            try:
                # Get socio-economic profile from civic client
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
                    'indicators': profile.get('indicators', {}),
                    'data_sources': profile.get('data_sources', [])
                }
                
            except CivicDataException as e:
                regional_data[region_id] = {
                    'region': region,
                    'error': str(e),
                    'data_available': False
                }
        
        return regional_data
    
    def _assess_data_quality(
        self,
        regional_profiles: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Assess data quality across all regions"""
        
        quality_assessment = {
            'overall_quality': 'unknown',
            'completeness_scores': {},
            'timeliness_scores': {},
            'reliability': {},
            'concerns': []
        }
        
        total_completeness = 0
        total_timeliness = 0
        count = 0
        
        for region_id, data in regional_profiles.items():
            if data.get('data_available', True) and not data.get('error'):
                location = data['region']
                validation = self.civic_client.validate_data_quality({
                    'type': location.get('type', 'country'),
                    'code': location.get('code', region_id)
                })
                
                quality_assessment['completeness_scores'][region_id] = validation.get('completeness_score', 0)
                quality_assessment['timeliness_scores'][region_id] = validation.get('timeliness_score', 0)
                quality_assessment['reliability'][region_id] = validation.get('source_reliability', 'unknown')
                
                total_completeness += validation.get('completeness_score', 0)
                total_timeliness += validation.get('timeliness_score', 0)
                count += 1
                
                if validation.get('validation_errors'):
                    quality_assessment['concerns'].extend(validation['validation_errors'])
        
        # Calculate overall quality
        if count > 0:
            avg_completeness = total_completeness / count
            avg_timeliness = total_timeliness / count
            overall_score = (avg_completeness + avg_timeliness) / 2
            
            if overall_score >= 0.9:
                quality_assessment['overall_quality'] = 'excellent'
            elif overall_score >= 0.7:
                quality_assessment['overall_quality'] = 'good'
            elif overall_score >= 0.5:
                quality_assessment['overall_quality'] = 'fair'
            else:
                quality_assessment['overall_quality'] = 'poor'
        
        return quality_assessment
    
    def _analyze_dimension(
        self,
        dimension: EquityDimension,
        decision_data: Dict[str, Any],
        regional_profiles: Dict[str, Dict[str, Any]],
        baseline_data: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze a specific equity dimension"""
        
        if dimension == EquityDimension.ECONOMIC:
            return self._analyze_economic_equity(decision_data, regional_profiles)
        elif dimension == EquityDimension.EDUCATIONAL:
            return self._analyze_educational_equity(decision_data, regional_profiles)
        elif dimension == EquityDimension.HEALTH:
            return self._analyze_health_equity(decision_data, regional_profiles)
        elif dimension == EquityDimension.GEOGRAPHIC:
            return self._analyze_geographic_equity(decision_data, regional_profiles)
        elif dimension == EquityDimension.INTERSECTIONAL:
            return self._analyze_intersectional_equity(decision_data, regional_profiles)
        else:
            return {'dimension': dimension.value, 'analyzed': False}
    
    def _analyze_economic_equity(
        self,
        decision_data: Dict[str, Any],
        regional_profiles: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze economic equity using civic data"""
        
        analysis = {
            'dimension': 'economic',
            'equity_score': 0.0,
            'disparities': [],
            'insights': []
        }
        
        allocations = decision_data.get('allocations', {})
        
        # Compare poverty rates with allocations
        for region_id, profile_data in regional_profiles.items():
            if profile_data.get('error'):
                continue
            
            equity_scores = profile_data.get('equity_scores', {})
            poverty_score = equity_scores.get('dimension_scores', {}).get('poverty', 0)
            allocation = allocations.get(region_id, 0)
            
            # Rawlsian analysis: regions with higher poverty should get more
            if poverty_score < 0.3:  # High poverty (low score)
                avg_allocation = sum(allocations.values()) / len(allocations) if allocations else 0
                if allocation < avg_allocation * 0.8:
                    analysis['disparities'].append({
                        'region': region_id,
                        'type': 'economic_inequity',
                        'severity': 'high',
                        'evidence': f"High poverty (score: {poverty_score:.2f}) but receives {allocation/avg_allocation:.1f}x average allocation"
                    })
        
        # Calculate Gini coefficient of allocation distribution
        if len(allocations) > 1:
            allocation_values = sorted(allocations.values())
            n = len(allocation_values)
            sum_diff = sum((2 * i - n - 1) * val for i, val in enumerate(allocation_values, 1))
            mean_allocation = sum(allocation_values) / n
            gini = sum_diff / (n * n * mean_allocation) if mean_allocation > 0 else 0
            
            analysis['allocation_gini'] = gini
            if gini > 0.4:
                analysis['insights'].append(f"High allocation inequality (Gini: {gini:.2f}) - consider redistribution")
        
        return analysis
    
    def _analyze_educational_equity(
        self,
        decision_data: Dict[str, Any],
        regional_profiles: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze educational equity"""
        
        analysis = {
            'dimension': 'educational',
            'equity_score': 0.0,
            'disparities': [],
            'insights': []
        }
        
        # Analyze literacy rates and education indicators
        literacy_scores = []
        
        for region_id, profile_data in regional_profiles.items():
            if profile_data.get('error'):
                continue
            
            equity_scores = profile_data.get('equity_scores', {})
            education_score = equity_scores.get('dimension_scores', {}).get('education', 0)
            literacy_scores.append(education_score)
            
            if education_score < 0.5:
                analysis['disparities'].append({
                    'region': region_id,
                    'type': 'educational_gap',
                    'severity': 'high' if education_score < 0.3 else 'medium',
                    'evidence': f"Low education score: {education_score:.2f}"
                })
        
        # Calculate educational equity score
        if literacy_scores:
            min_score = min(literacy_scores)
            max_score = max(literacy_scores)
            analysis['equity_score'] = 1 - (max_score - min_score)  # Lower disparity = higher equity
            analysis['disparity_ratio'] = max_score / min_score if min_score > 0 else float('inf')
        
        return analysis
    
    def _analyze_health_equity(
        self,
        decision_data: Dict[str, Any],
        regional_profiles: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze health equity"""
        
        analysis = {
            'dimension': 'health',
            'equity_score': 0.0,
            'disparities': [],
            'insights': []
        }
        
        # Analyze health indicators from civic data
        for region_id, profile_data in regional_profiles.items():
            if profile_data.get('error'):
                continue
            
            indicators = profile_data.get('indicators', {})
            
            # Check health expenditure
            if 'SH.XPD.CHEX.GD.ZS' in indicators:
                health_exp_data = indicators['SH.XPD.CHEX.GD.ZS']
                if health_exp_data:
                    health_exp = health_exp_data[0].get('value', 0)
                    if health_exp < 5:  # Less than 5% of GDP
                        analysis['disparities'].append({
                            'region': region_id,
                            'type': 'low_health_investment',
                            'severity': 'medium',
                            'evidence': f"Health expenditure only {health_exp:.1f}% of GDP"
                        })
        
        return analysis
    
    def _analyze_geographic_equity(
        self,
        decision_data: Dict[str, Any],
        regional_profiles: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze geographic equity"""
        
        analysis = {
            'dimension': 'geographic',
            'equity_score': 0.0,
            'urban_rural_disparity': {},
            'insights': []
        }
        
        # Categorize by region type if available
        urban_equity = []
        rural_equity = []
        
        for region_id, profile_data in regional_profiles.items():
            if profile_data.get('error'):
                continue
            
            region = profile_data.get('region', {})
            region_type = region.get('region_type', 'unknown')
            equity_score = profile_data.get('equity_scores', {}).get('composite_equity_score', 0)
            
            if region_type == 'urban':
                urban_equity.append(equity_score)
            elif region_type == 'rural':
                rural_equity.append(equity_score)
        
        # Compare urban vs rural equity
        if urban_equity and rural_equity:
            avg_urban = sum(urban_equity) / len(urban_equity)
            avg_rural = sum(rural_equity) / len(rural_equity)
            
            analysis['urban_rural_disparity'] = {
                'urban_avg': avg_urban,
                'rural_avg': avg_rural,
                'disparity_ratio': avg_urban / avg_rural if avg_rural > 0 else float('inf')
            }
            
            if avg_urban > avg_rural * 1.3:
                analysis['insights'].append(
                    f"Significant urban-rural equity gap: urban {avg_urban:.2f} vs rural {avg_rural:.2f}"
                )
        
        return analysis
    
    def _analyze_intersectional_equity(
        self,
        decision_data: Dict[str, Any],
        regional_profiles: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze intersectional equity (multiple disadvantages)"""
        
        hooks = self.framework.get_thinker_perspective('hooks')
        
        analysis = {
            'dimension': 'intersectional',
            'compounded_disadvantages': [],
            'philosophical_framework': "hooks' Intersectionality"
        }
        
        # Identify regions with multiple disadvantages
        for region_id, profile_data in regional_profiles.items():
            if profile_data.get('error'):
                continue
            
            equity_scores = profile_data.get('equity_scores', {})
            dimension_scores = equity_scores.get('dimension_scores', {})
            
            disadvantages = []
            if dimension_scores.get('poverty', 1) < 0.3:
                disadvantages.append('economic')
            if dimension_scores.get('education', 1) < 0.5:
                disadvantages.append('educational')
            if dimension_scores.get('income', 1) < 0.4:
                disadvantages.append('income')
            
            # Compounded disadvantage if 2+ dimensions
            if len(disadvantages) >= 2:
                analysis['compounded_disadvantages'].append({
                    'region': region_id,
                    'disadvantages': disadvantages,
                    'count': len(disadvantages),
                    'composite_equity_score': equity_scores.get('composite_equity_score', 0)
                })
        
        return analysis
    
    def _detect_equity_biases(
        self,
        decision_data: Dict[str, Any],
        regional_profiles: Dict[str, Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Detect equity biases using civic data"""
        
        biases = []
        allocations = decision_data.get('allocations', {})
        
        # Inverse needs bias: High-equity regions getting more
        for region_id, profile_data in regional_profiles.items():
            if profile_data.get('error'):
                continue
            
            equity_score = profile_data.get('equity_scores', {}).get('composite_equity_score', 0.5)
            allocation = allocations.get(region_id, 0)
            avg_allocation = sum(allocations.values()) / len(allocations) if allocations else 0
            
            # If high equity but also high allocation (should go to low equity)
            if equity_score > 0.7 and allocation > avg_allocation * 1.3:
                biases.append({
                    'bias_type': 'inverse_needs_allocation',
                    'region': region_id,
                    'severity': 'high',
                    'evidence': f"High equity score ({equity_score:.2f}) receives {allocation/avg_allocation:.1f}x average",
                    'philosophical_critique': "Violates Rawlsian principle - benefits advantaged over disadvantaged"
                })
        
        return biases
    
    def _apply_philosophical_equity_analysis(
        self,
        decision_data: Dict[str, Any],
        regional_profiles: Dict[str, Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Apply philosophical frameworks to equity analysis"""
        
        assessments = []
        
        # Rawlsian assessment
        rawls = self.framework.get_thinker_perspective('rawls')
        if rawls:
            rawlsian = self._rawlsian_equity_assessment(decision_data, regional_profiles)
            assessments.append(rawlsian)
        
        # Sen's capability assessment
        sen = self.framework.get_thinker_perspective('sen')
        if sen:
            capability = self._capability_equity_assessment(decision_data, regional_profiles)
            assessments.append(capability)
        
        return assessments
    
    def _rawlsian_equity_assessment(
        self,
        decision_data: Dict[str, Any],
        regional_profiles: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Assess equity using Rawlsian difference principle"""
        
        # Find least advantaged region
        min_equity = float('inf')
        least_advantaged = None
        
        for region_id, profile_data in regional_profiles.items():
            if profile_data.get('error'):
                continue
            equity_score = profile_data.get('equity_scores', {}).get('composite_equity_score', 0.5)
            if equity_score < min_equity:
                min_equity = equity_score
                least_advantaged = region_id
        
        allocations = decision_data.get('allocations', {})
        avg_allocation = sum(allocations.values()) / len(allocations) if allocations else 0
        least_allocation = allocations.get(least_advantaged, 0)
        
        assessment = {
            'framework': 'Rawlsian Justice',
            'least_advantaged_region': least_advantaged,
            'least_equity_score': min_equity,
            'allocation_ratio': least_allocation / avg_allocation if avg_allocation > 0 else 0,
            'compliance': 'low'
        }
        
        if least_allocation >= avg_allocation * 1.2:
            assessment['compliance'] = 'high'
            assessment['assessment'] = "Decision benefits least advantaged - Rawlsian compliant"
        elif least_allocation >= avg_allocation:
            assessment['compliance'] = 'medium'
            assessment['assessment'] = "Decision provides fair allocation to least advantaged"
        else:
            assessment['assessment'] = "Concern: Least advantaged receives below-average allocation"
        
        return assessment
    
    def _capability_equity_assessment(
        self,
        decision_data: Dict[str, Any],
        regional_profiles: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Assess equity using Sen's capability approach"""
        
        assessment = {
            'framework': "Sen's Capability Approach",
            'capability_gaps': [],
            'recommendations': []
        }
        
        # Identify capability gaps
        for region_id, profile_data in regional_profiles.items():
            if profile_data.get('error'):
                continue
            
            equity_scores = profile_data.get('equity_scores', {})
            education = equity_scores.get('dimension_scores', {}).get('education', 1)
            income = equity_scores.get('dimension_scores', {}).get('income', 1)
            
            gaps = []
            if education < 0.5:
                gaps.append('education')
            if income < 0.4:
                gaps.append('economic opportunity')
            
            if gaps:
                assessment['capability_gaps'].append({
                    'region': region_id,
                    'gaps': gaps,
                    'priority': 'high' if len(gaps) > 1 else 'medium'
                })
        
        if assessment['capability_gaps']:
            assessment['recommendations'].append(
                "Target capability enhancement in regions with identified gaps"
            )
        
        return assessment
    
    def _generate_impact_summary(
        self,
        analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate summary of equity impacts"""
        
        total_disparities = sum(
            len(dim.get('disparities', [])) 
            for dim in analysis['equity_dimensions'].values()
        )
        
        critical_regions = set()
        for dim in analysis['equity_dimensions'].values():
            for disparity in dim.get('disparities', []):
                if disparity.get('severity') == 'high':
                    critical_regions.add(disparity.get('region'))
        
        return {
            'total_disparities_detected': total_disparities,
            'critical_regions': list(critical_regions),
            'biases_detected': len(analysis['detected_biases']),
            'overall_equity_assessment': 'needs_improvement' if total_disparities > 5 else 'acceptable',
            'data_quality': analysis['data_quality'].get('overall_quality', 'unknown')
        }
    
    def _generate_equity_recommendations(
        self,
        analysis: Dict[str, Any]
    ) -> List[str]:
        """Generate recommendations for improving equity"""
        
        recommendations = []
        
        # Data quality recommendations
        if analysis['data_quality'].get('overall_quality') in ['poor', 'fair']:
            recommendations.append(
                "Improve data quality and completeness before making major allocation decisions"
            )
        
        # Dimension-specific recommendations
        for dimension, dim_analysis in analysis['equity_dimensions'].items():
            if len(dim_analysis.get('disparities', [])) > 2:
                recommendations.append(
                    f"Address {len(dim_analysis['disparities'])} {dimension} equity disparities identified"
                )
        
        # Philosophical framework recommendations
        for assessment in analysis['philosophical_assessments']:
            if 'recommendations' in assessment:
                recommendations.extend(assessment['recommendations'])
        
        # Bias mitigation
        for bias in analysis['detected_biases']:
            if bias.get('severity') == 'high':
                recommendations.append(
                    f"Mitigate {bias['bias_type']} bias affecting {bias.get('region')}"
                )
        
        return recommendations or ["Continue monitoring equity indicators across all dimensions"]