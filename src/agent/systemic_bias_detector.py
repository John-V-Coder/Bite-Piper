# Structural inequality identification

"""
Systemic Bias Detector Module for Bite-Piper
Identifies structural inequalities and systemic biases using philosophical frameworks (Young, hooks, Fanon)
"""

from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from philosophical_framework import PhilosophicalFramework


class BiasCategory(Enum):
    """Categories of systemic bias"""
    SOCIOECONOMIC = "socioeconomic"
    GEOGRAPHIC = "geographic"
    DEMOGRAPHIC = "demographic"
    DATA_MANIPULATION = "data_manipulation"
    INSTITUTIONAL = "institutional"
    INTERSECTIONAL = "intersectional"


class OppressionType(Enum):
    """Young's five faces of oppression"""
    EXPLOITATION = "exploitation"
    MARGINALIZATION = "marginalization"
    POWERLESSNESS = "powerlessness"
    CULTURAL_IMPERIALISM = "cultural_imperialism"
    VIOLENCE = "violence"


@dataclass
class BiasDetection:
    """Result of bias detection"""
    bias_type: BiasCategory
    severity: str  # low, medium, high, critical
    affected_groups: List[str]
    evidence: List[str]
    philosophical_analysis: str
    mitigation_strategies: List[str]


class SystemicBiasDetector:
    """Detects systemic biases and structural inequalities in civic systems"""
    
    def __init__(self):
        self.framework = PhilosophicalFramework()
    
    def detect_systemic_biases(
        self,
        decision_data: Dict[str, Any],
        historical_data: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Comprehensive systemic bias detection
        
        Args:
            decision_data: Current decision or allocation data
            historical_data: Historical patterns for comparison
            context: Additional contextual information
            
        Returns:
            Comprehensive bias analysis
        """
        historical_data = historical_data or {}
        context = context or {}
        
        analysis = {
            'detected_biases': [],
            'oppression_analysis': {},
            'intersectional_analysis': {},
            'structural_patterns': [],
            'severity_assessment': 'unknown',
            'mitigation_priorities': [],
            'philosophical_frameworks_applied': []
        }
        
        # Detect socioeconomic bias
        socioeconomic_biases = self._detect_socioeconomic_bias(decision_data, historical_data)
        analysis['detected_biases'].extend(socioeconomic_biases)
        
        # Detect geographic bias
        geographic_biases = self._detect_geographic_bias(decision_data, context)
        analysis['detected_biases'].extend(geographic_biases)
        
        # Detect demographic bias
        demographic_biases = self._detect_demographic_bias(decision_data, context)
        analysis['detected_biases'].extend(demographic_biases)
        
        # Apply Young's five faces of oppression
        oppression_analysis = self._analyze_oppression_faces(decision_data, context)
        analysis['oppression_analysis'] = oppression_analysis
        
        # Intersectional analysis (hooks)
        intersectional = self._analyze_intersectional_bias(decision_data, context)
        analysis['intersectional_analysis'] = intersectional
        
        # Identify structural patterns
        structural = self._identify_structural_patterns(decision_data, historical_data)
        analysis['structural_patterns'] = structural
        
        # Assess overall severity
        analysis['severity_assessment'] = self._assess_overall_severity(analysis['detected_biases'])
        
        # Prioritize mitigations
        analysis['mitigation_priorities'] = self._prioritize_mitigations(analysis)
        
        # Record frameworks applied
        analysis['philosophical_frameworks_applied'] = [
            'Young (Five Faces of Oppression)',
            'hooks (Intersectionality)',
            'Fanon (Decolonial Analysis)',
            'Foucault (Power Structures)'
        ]
        
        return analysis
    
    def _detect_socioeconomic_bias(
        self,
        decision_data: Dict[str, Any],
        historical_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Detect socioeconomic biases (wealth-based, education privilege)"""
        
        biases = []
        allocations = decision_data.get('allocations', {})
        needs_data = decision_data.get('needs_data', {})
        
        # Check for wealth-based bias (inverse allocation)
        for region_id, allocation in allocations.items():
            needs = needs_data.get(region_id, {})
            poverty_rate = needs.get('poverty_rate', 0.3)
            wealth_index = needs.get('wealth_index', 50)
            
            # If wealthy region gets disproportionate allocation
            avg_allocation = sum(allocations.values()) / len(allocations) if allocations else 0
            if wealth_index > 70 and allocation > avg_allocation * 1.3:
                biases.append({
                    'bias_type': BiasCategory.SOCIOECONOMIC.value,
                    'severity': 'high',
                    'affected_groups': [region_id],
                    'evidence': [
                        f"Region {region_id} has high wealth index ({wealth_index}) but receives {allocation/avg_allocation:.1f}x average allocation"
                    ],
                    'philosophical_analysis': "Violates Rawlsian difference principle - benefits advantaged rather than disadvantaged",
                    'mitigation_strategies': [
                        "Apply progressive allocation formula favoring high-poverty regions",
                        "Implement wealth index correction factor"
                    ]
                })
            
            # Check for education privilege bias
            literacy_rate = needs.get('literacy_rate', 0.7)
            if literacy_rate > 0.9 and poverty_rate > 0.5 and allocation < avg_allocation * 0.7:
                biases.append({
                    'bias_type': BiasCategory.SOCIOECONOMIC.value,
                    'severity': 'medium',
                    'affected_groups': [region_id],
                    'evidence': [
                        f"High literacy ({literacy_rate:.1%}) masks high poverty ({poverty_rate:.1%})",
                        f"Region receives only {allocation/avg_allocation:.1f}x average allocation"
                    ],
                    'philosophical_analysis': "Education privilege bias - assumes literacy correlates with wealth",
                    'mitigation_strategies': [
                        "Separate education and economic indicators",
                        "Weight poverty rate more heavily"
                    ]
                })
        
        return biases
    
    def _detect_geographic_bias(
        self,
        decision_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Detect geographic biases (urban-centric, rural neglect)"""
        
        biases = []
        allocations = decision_data.get('allocations', {})
        needs_data = decision_data.get('needs_data', {})
        
        # Categorize regions
        urban_regions = {}
        rural_regions = {}
        
        for region_id, needs in needs_data.items():
            region_type = needs.get('region_type', 'unknown')
            allocation = allocations.get(region_id, 0)
            
            if region_type == 'urban':
                urban_regions[region_id] = allocation
            elif region_type == 'rural':
                rural_regions[region_id] = allocation
        
        # Compare urban vs rural allocation
        if urban_regions and rural_regions:
            avg_urban = sum(urban_regions.values()) / len(urban_regions)
            avg_rural = sum(rural_regions.values()) / len(rural_regions)
            
            # Urban-centric bias
            if avg_urban > avg_rural * 1.5:
                biases.append({
                    'bias_type': BiasCategory.GEOGRAPHIC.value,
                    'severity': 'high',
                    'affected_groups': list(rural_regions.keys()),
                    'evidence': [
                        f"Urban regions receive {avg_urban/avg_rural:.1f}x more than rural regions on average",
                        f"Urban avg: ${avg_urban:,.0f}, Rural avg: ${avg_rural:,.0f}"
                    ],
                    'philosophical_analysis': "Foucauldian power structures: Urban-centric governance marginalizes rural communities",
                    'mitigation_strategies': [
                        "Implement geographic equity multiplier",
                        "Add rural infrastructure penalty adjustment",
                        "Include rural access costs in allocation formula"
                    ]
                })
            
            # Rural neglect check (historical underinvestment)
            rural_poverty = {r: needs_data[r].get('poverty_rate', 0.3) for r in rural_regions}
            avg_rural_poverty = sum(rural_poverty.values()) / len(rural_poverty) if rural_poverty else 0
            
            if avg_rural_poverty > 0.5 and avg_rural < avg_urban * 0.7:
                biases.append({
                    'bias_type': BiasCategory.GEOGRAPHIC.value,
                    'severity': 'critical',
                    'affected_groups': list(rural_regions.keys()),
                    'evidence': [
                        f"Rural regions have {avg_rural_poverty:.1%} poverty rate but receive inadequate allocation",
                        "Pattern suggests historical underinvestment in rural infrastructure"
                    ],
                    'philosophical_analysis': "Structural injustice (Young): Rural marginalization through systematic underinvestment",
                    'mitigation_strategies': [
                        "Apply historical correction factor for rural regions",
                        "Establish minimum rural allocation threshold",
                        "Conduct participatory needs assessment in rural communities (Freire)"
                    ]
                })
        
        return biases
    
    def _detect_demographic_bias(
        self,
        decision_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Detect demographic biases"""
        
        biases = []
        demographic_data = context.get('demographic_data', {})
        allocations = decision_data.get('allocations', {})
        
        # Check for population-based bias (ignoring need intensity)
        for region_id, allocation in allocations.items():
            demographics = demographic_data.get(region_id, {})
            population = demographics.get('population', 0)
            needs = decision_data.get('needs_data', {}).get(region_id, {})
            poverty_rate = needs.get('poverty_rate', 0.3)
            
            # Per-capita allocation analysis
            per_capita = allocation / population if population > 0 else 0
            
            # If high population but low per-capita despite high need
            if population > 100000 and per_capita < 100 and poverty_rate > 0.5:
                biases.append({
                    'bias_type': BiasCategory.DEMOGRAPHIC.value,
                    'severity': 'medium',
                    'affected_groups': [region_id],
                    'evidence': [
                        f"Large population ({population:,}) receives only ${per_capita:.2f} per capita",
                        f"Despite {poverty_rate:.1%} poverty rate"
                    ],
                    'philosophical_analysis': "Utilitarian bias: Large populations diluted despite high need intensity",
                    'mitigation_strategies': [
                        "Use need-weighted per-capita allocation",
                        "Establish minimum per-capita thresholds for high-poverty regions"
                    ]
                })
        
        return biases
    
    def _analyze_oppression_faces(
        self,
        decision_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply Iris Marion Young's five faces of oppression framework"""
        
        young = self.framework.get_thinker_perspective('young')
        
        analysis = {
            'framework': "Young's Five Faces of Oppression",
            'faces_detected': []
        }
        
        allocations = decision_data.get('allocations', {})
        needs_data = decision_data.get('needs_data', {})
        process_data = decision_data.get('process', {})
        
        # 1. EXPLOITATION: Benefiting from labor without fair compensation
        # (Detected through wealth/income disparity)
        for region_id, needs in needs_data.items():
            income = needs.get('income_per_capita', 25000)
            wealth = needs.get('wealth_index', 50)
            
            if income < 15000 and wealth < 30:
                analysis['faces_detected'].append({
                    'type': OppressionType.EXPLOITATION.value,
                    'region': region_id,
                    'evidence': f"Low income (${income}) and wealth ({wealth}) suggest exploitation patterns",
                    'severity': 'high'
                })
        
        # 2. MARGINALIZATION: Exclusion from labor market participation
        # (Detected through unemployment, lack of economic opportunity)
        for region_id, needs in needs_data.items():
            literacy = needs.get('literacy_rate', 0.7)
            poverty = needs.get('poverty_rate', 0.3)
            
            if literacy < 0.5 and poverty > 0.6:
                analysis['faces_detected'].append({
                    'type': OppressionType.MARGINALIZATION.value,
                    'region': region_id,
                    'evidence': f"Low literacy ({literacy:.1%}) and high poverty ({poverty:.1%}) indicate marginalization",
                    'severity': 'critical'
                })
        
        # 3. POWERLESSNESS: Lack of authority and decision-making power
        # (Detected through participation data)
        marginalized_included = process_data.get('marginalized_groups_included', False)
        participatory = process_data.get('participatory_design', False)
        
        if not marginalized_included or not participatory:
            analysis['faces_detected'].append({
                'type': OppressionType.POWERLESSNESS.value,
                'region': 'all',
                'evidence': "Decision-making process excludes marginalized communities",
                'severity': 'high'
            })
        
        # 4. CULTURAL IMPERIALISM: Dominant group's culture as universal norm
        # (Detected through policy language and assumptions)
        indigenous_knowledge = decision_data.get('indigenous_knowledge_centered', False)
        diverse_knowledge = decision_data.get('diverse_knowledge_systems', False)
        
        if not indigenous_knowledge and not diverse_knowledge:
            analysis['faces_detected'].append({
                'type': OppressionType.CULTURAL_IMPERIALISM.value,
                'region': 'all',
                'evidence': "Decision framework doesn't recognize diverse cultural knowledge systems",
                'severity': 'medium'
            })
        
        # 5. VIOLENCE: Systematic threat or experience of violence
        # (Detected through vulnerability indicators)
        for region_id, needs in needs_data.items():
            vulnerability_score = needs.get('vulnerability_index', 0)
            if vulnerability_score > 0.7:
                analysis['faces_detected'].append({
                    'type': OppressionType.VIOLENCE.value,
                    'region': region_id,
                    'evidence': f"High vulnerability score ({vulnerability_score:.2f}) suggests systematic violence exposure",
                    'severity': 'critical'
                })
        
        return analysis
    
    def _analyze_intersectional_bias(
        self,
        decision_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply bell hooks' intersectional analysis"""
        
        hooks_perspective = self.framework.get_thinker_perspective('hooks')
        
        analysis = {
            'framework': "hooks' Intersectionality",
            'compounded_disadvantages': [],
            'overlooked_intersections': []
        }
        
        # Look for compounded disadvantages
        needs_data = decision_data.get('needs_data', {})
        allocations = decision_data.get('allocations', {})
        demographic_data = context.get('demographic_data', {})
        
        for region_id, needs in needs_data.items():
            disadvantage_count = 0
            disadvantage_types = []
            
            # Economic disadvantage
            if needs.get('poverty_rate', 0) > 0.5:
                disadvantage_count += 1
                disadvantage_types.append('economic')
            
            # Educational disadvantage
            if needs.get('literacy_rate', 1.0) < 0.6:
                disadvantage_count += 1
                disadvantage_types.append('educational')
            
            # Geographic disadvantage
            if needs.get('region_type') == 'rural':
                disadvantage_count += 1
                disadvantage_types.append('geographic')
            
            # Gender-based disadvantage (if data available)
            demographics = demographic_data.get(region_id, {})
            if demographics.get('female_headed_households_pct', 0) > 0.6:
                disadvantage_count += 1
                disadvantage_types.append('gender')
            
            # Compounded disadvantage (3+ intersecting)
            if disadvantage_count >= 3:
                allocation = allocations.get(region_id, 0)
                avg_allocation = sum(allocations.values()) / len(allocations) if allocations else 0
                
                if allocation < avg_allocation * 1.2:
                    analysis['compounded_disadvantages'].append({
                        'region': region_id,
                        'intersecting_disadvantages': disadvantage_types,
                        'disadvantage_count': disadvantage_count,
                        'allocation_ratio': allocation / avg_allocation if avg_allocation > 0 else 0,
                        'concern': "Multiple intersecting disadvantages not adequately addressed in allocation"
                    })
        
        # Check if intersectional analysis was conducted
        if not decision_data.get('intersectional_analysis', False):
            analysis['overlooked_intersections'].append(
                "Decision lacks explicit intersectional analysis - may miss compounded disadvantages"
            )
        
        return analysis
    
    def _identify_structural_patterns(
        self,
        decision_data: Dict[str, Any],
        historical_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Identify structural patterns of inequality"""
        
        patterns = []
        
        # Check for persistent underinvestment patterns
        current_allocations = decision_data.get('allocations', {})
        historical_allocations = historical_data.get('allocations', {})
        
        for region_id, current_alloc in current_allocations.items():
            historical_alloc = historical_allocations.get(region_id, [])
            
            # If consistently below average over time
            if len(historical_alloc) >= 3:
                avg_historical = sum(historical_alloc) / len(historical_alloc)
                overall_avg = sum(current_allocations.values()) / len(current_allocations) if current_allocations else 0
                
                if avg_historical < overall_avg * 0.7 and current_alloc < overall_avg * 0.8:
                    patterns.append({
                        'type': 'persistent_underinvestment',
                        'region': region_id,
                        'evidence': f"Consistently receives <80% of average allocation over {len(historical_alloc) + 1} periods",
                        'structural_analysis': "Pattern indicates systemic exclusion from resource distribution",
                        'mitigation': "Apply historical correction factor with reparative allocation"
                    })
        
        return patterns
    
    def _assess_overall_severity(
        self,
        detected_biases: List[Dict[str, Any]]
    ) -> str:
        """Assess overall severity of detected biases"""
        
        if not detected_biases:
            return 'none'
        
        critical_count = len([b for b in detected_biases if b.get('severity') == 'critical'])
        high_count = len([b for b in detected_biases if b.get('severity') == 'high'])
        
        if critical_count > 0:
            return 'critical'
        elif high_count >= 3:
            return 'high'
        elif high_count > 0:
            return 'medium'
        else:
            return 'low'
    
    def _prioritize_mitigations(
        self,
        analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Prioritize mitigation strategies based on severity and impact"""
        
        priorities = []
        
        # Critical biases first
        critical_biases = [b for b in analysis['detected_biases'] if b.get('severity') == 'critical']
        for bias in critical_biases:
            priorities.append({
                'priority': 'immediate',
                'bias_type': bias['bias_type'],
                'affected_groups': bias['affected_groups'],
                'strategies': bias['mitigation_strategies']
            })
        
        # Intersectional compounded disadvantages
        compounded = analysis['intersectional_analysis'].get('compounded_disadvantages', [])
        if compounded:
            priorities.append({
                'priority': 'high',
                'bias_type': 'intersectional',
                'affected_groups': [c['region'] for c in compounded],
                'strategies': [
                    "Implement intersectional scoring that accounts for compounded disadvantages",
                    "Apply multiplicative (not additive) factors for intersecting marginalization"
                ]
            })
        
        # Structural patterns
        structural = analysis.get('structural_patterns', [])
        if structural:
            priorities.append({
                'priority': 'high',
                'bias_type': 'structural',
                'affected_groups': [p['region'] for p in structural],
                'strategies': [
                    "Apply historical reparations framework (Fanon)",
                    "Implement minimum allocation thresholds for historically underserved regions"
                ]
            })
        
        return priorities