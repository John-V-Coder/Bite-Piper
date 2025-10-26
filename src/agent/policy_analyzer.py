# Policy document and language analysis

"""
Policy Analyzer Module for Bite-Piper
Analyzes policy documents and language using philosophical frameworks (Foucault, Davidson)
"""

from typing import Dict, List, Any, Tuple, Set
from dataclasses import dataclass
from enum import Enum
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from philosophical_framework import PhilosophicalFramework


class PolicyBiasType(Enum):
    """Types of bias in policy language"""
    POWER_IMBALANCE = "power_imbalance"
    EXCLUSIONARY_LANGUAGE = "exclusionary_language"
    DEFICIT_FRAMING = "deficit_framing"
    PATERNALISTIC = "paternalistic"
    TECHNOCRATIC_OBSCURITY = "technocratic_obscurity"
    UNIVERSALIZING_CLAIMS = "universalizing_claims"


@dataclass
class PolicyAnalysisResult:
    """Result of policy analysis"""
    policy_id: str
    discourse_patterns: List[str]
    power_dynamics: Dict[str, Any]
    bias_indicators: List[Dict[str, Any]]
    philosophical_critique: str
    recommendations: List[str]


class PolicyAnalyzer:
    """Analyzes policy documents using Foucauldian discourse analysis and philosophical frameworks"""
    
    def __init__(self):
        self.framework = PhilosophicalFramework()
        self._build_analysis_patterns()
    
    def _build_analysis_patterns(self):
        """Build patterns for discourse analysis"""
        
        # Deficit language patterns (Freire's critique)
        self.deficit_patterns = [
            r'\b(lack|lacking|deficient|inadequate|insufficient|poor)\b',
            r'\b(unable|cannot|fail|failed|failure)\b',
            r'\b(disadvantaged|underserved|at-risk)\b'
        ]
        
        # Paternalistic patterns
        self.paternalistic_patterns = [
            r'\b(need[s]? to|must|should|require[s]?)\s+(be|have)\s+\w+ed\b',
            r'\b(provide|deliver|give)\s+\w+\s+to\s+(them|these communities)\b',
            r'\b(help|assist|aid)\s+(them|the poor|beneficiaries)\b'
        ]
        
        # Exclusionary language
        self.exclusionary_patterns = [
            r'\b(normal|standard|typical|mainstream)\b',
            r'\b(exception|special case|minority)\b',
            r'\b(they|them|those people)\s+(?!who)'
        ]
        
        # Technocratic obscurity
        self.technocratic_patterns = [
            r'\b(optimize|leverage|synergize|operationalize)\b',
            r'\b(framework|paradigm|mechanism|modality)\b',
            r'\b(stakeholder engagement|capacity building|best practices)\b'
        ]
        
        # Power-laden terms (Foucauldian)
        self.power_terms = [
            r'\b(manage|control|govern|regulate|administer)\b',
            r'\b(compliance|enforcement|implementation|rollout)\b',
            r'\b(target population|beneficiaries|recipients)\b'
        ]
    
    def analyze_policy_document(
        self,
        policy_text: str,
        policy_metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Comprehensive analysis of policy document
        
        Args:
            policy_text: The policy document text
            policy_metadata: Metadata about the policy
            
        Returns:
            Comprehensive policy analysis
        """
        metadata = policy_metadata or {}
        
        analysis = {
            'policy_id': metadata.get('id', 'unknown'),
            'policy_title': metadata.get('title', 'Untitled Policy'),
            'discourse_analysis': {},
            'power_dynamics': {},
            'bias_detection': [],
            'philosophical_critique': {},
            'recommendations': [],
            'overall_equity_score': 0.0
        }
        
        # Foucauldian discourse analysis
        discourse = self._foucauldian_discourse_analysis(policy_text)
        analysis['discourse_analysis'] = discourse
        
        # Power dynamics analysis
        power = self._analyze_power_dynamics(policy_text, metadata)
        analysis['power_dynamics'] = power
        
        # Detect bias patterns
        biases = self._detect_policy_biases(policy_text)
        analysis['bias_detection'] = biases
        
        # Apply philosophical frameworks
        philosophical = self._apply_philosophical_critique(policy_text, discourse, power)
        analysis['philosophical_critique'] = philosophical
        
        # Calculate equity score
        analysis['overall_equity_score'] = self._calculate_equity_score(
            discourse, power, biases
        )
        
        # Generate recommendations
        analysis['recommendations'] = self._generate_policy_recommendations(
            analysis
        )
        
        return analysis
    
    def _foucauldian_discourse_analysis(
        self,
        policy_text: str
    ) -> Dict[str, Any]:
        """Apply Foucauldian discourse analysis to policy text"""
        
        foucault = self.framework.get_thinker_perspective('foucault')
        
        analysis = {
            'framework': 'Foucauldian Discourse Analysis',
            'knowledge_power_relations': [],
            'subject_creation': [],
            'normalization_patterns': [],
            'governance_mechanisms': []
        }
        
        # Identify how policy creates subjects
        subject_patterns = [
            (r'\b(taxpayer|citizen|resident|household)\b', 'Normative subject'),
            (r'\b(beneficiary|recipient|client)\b', 'Dependent subject'),
            (r'\b(stakeholder|partner)\b', 'Participating subject'),
            (r'\b(target population|vulnerable groups)\b', 'Problematic subject')
        ]
        
        for pattern, subject_type in subject_patterns:
            matches = re.findall(pattern, policy_text, re.IGNORECASE)
            if matches:
                analysis['subject_creation'].append({
                    'type': subject_type,
                    'frequency': len(matches),
                    'examples': list(set(matches))[:3]
                })
        
        # Identify normalization patterns
        if re.search(r'\b(normal|standard|acceptable|appropriate)\b', policy_text, re.IGNORECASE):
            analysis['normalization_patterns'].append(
                "Policy establishes norms that may marginalize non-conforming groups"
            )
        
        # Identify governance mechanisms
        governance_terms = ['monitor', 'evaluate', 'measure', 'track', 'assess', 'audit']
        found_governance = [term for term in governance_terms if re.search(rf'\b{term}', policy_text, re.IGNORECASE)]
        if found_governance:
            analysis['governance_mechanisms'].append({
                'surveillance_mechanisms': found_governance,
                'foucauldian_insight': "Policy employs surveillance mechanisms characteristic of governmentality"
            })
        
        return analysis
    
    def _analyze_power_dynamics(
        self,
        policy_text: str,
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze power dynamics in policy (who decides, who is acted upon)
        """
        
        analysis = {
            'decision_makers': [],
            'affected_populations': [],
            'power_asymmetry_score': 0.0,
            'voice_distribution': {}
        }
        
        # Identify decision-making agency
        decision_patterns = [
            r'\b(shall|will|must)\s+(\w+)\b',
            r'\b(authority|department|agency|government)\s+(shall|will|must)\b'
        ]
        
        decision_count = 0
        for pattern in decision_patterns:
            decision_count += len(re.findall(pattern, policy_text, re.IGNORECASE))
        
        # Identify passive constructions (those acted upon)
        passive_pattern = r'\b(will be|shall be|are|is)\s+(\w+ed)\b'
        passive_count = len(re.findall(passive_pattern, policy_text, re.IGNORECASE))
        
        # Power asymmetry: ratio of passive to active constructions
        if decision_count > 0:
            analysis['power_asymmetry_score'] = passive_count / decision_count
        else:
            analysis['power_asymmetry_score'] = 0.0
        
        # High asymmetry (>2.0) indicates top-down power structure
        if analysis['power_asymmetry_score'] > 2.0:
            analysis['power_assessment'] = "High power asymmetry: Policy is predominantly top-down"
        elif analysis['power_asymmetry_score'] > 1.0:
            analysis['power_assessment'] = "Moderate power asymmetry"
        else:
            analysis['power_assessment'] = "Balanced power distribution in language"
        
        return analysis
    
    def _detect_policy_biases(
        self,
        policy_text: str
    ) -> List[Dict[str, Any]]:
        """Detect various forms of bias in policy language"""
        
        biases = []
        
        # Deficit framing (Freire's critique)
        deficit_matches = sum(len(re.findall(pattern, policy_text, re.IGNORECASE)) 
                            for pattern in self.deficit_patterns)
        if deficit_matches > 5:
            biases.append({
                'type': PolicyBiasType.DEFICIT_FRAMING.value,
                'severity': 'high' if deficit_matches > 15 else 'medium',
                'frequency': deficit_matches,
                'description': "Policy employs deficit framing that focuses on lacks rather than strengths",
                'philosophical_critique': "Freire warns against deficit models that disempower communities"
            })
        
        # Paternalistic language
        paternalistic_matches = sum(len(re.findall(pattern, policy_text, re.IGNORECASE)) 
                                   for pattern in self.paternalistic_patterns)
        if paternalistic_matches > 3:
            biases.append({
                'type': PolicyBiasType.PATERNALISTIC.value,
                'severity': 'high' if paternalistic_matches > 10 else 'medium',
                'frequency': paternalistic_matches,
                'description': "Paternalistic language treats communities as passive recipients",
                'philosophical_critique': "Violates Freirean principle of community agency and self-determination"
            })
        
        # Exclusionary language
        exclusionary_matches = sum(len(re.findall(pattern, policy_text, re.IGNORECASE)) 
                                  for pattern in self.exclusionary_patterns)
        if exclusionary_matches > 5:
            biases.append({
                'type': PolicyBiasType.EXCLUSIONARY_LANGUAGE.value,
                'severity': 'high',
                'frequency': exclusionary_matches,
                'description': "Language creates in-groups and out-groups",
                'philosophical_critique': "Butler's framework: Language performatively excludes certain identities"
            })
        
        # Technocratic obscurity
        technocratic_matches = sum(len(re.findall(pattern, policy_text, re.IGNORECASE)) 
                                  for pattern in self.technocratic_patterns)
        if technocratic_matches > 10:
            biases.append({
                'type': PolicyBiasType.TECHNOCRATIC_OBSCURITY.value,
                'severity': 'medium',
                'frequency': technocratic_matches,
                'description': "Excessive jargon limits accessibility and democratic participation",
                'philosophical_critique': "Foucault: Expert knowledge marginalizes local/lived experience"
            })
        
        return biases
    
    def _apply_philosophical_critique(
        self,
        policy_text: str,
        discourse: Dict,
        power: Dict
    ) -> Dict[str, Any]:
        """Apply multiple philosophical frameworks to critique policy"""
        
        critiques = {
            'foucauldian': self._foucauldian_critique(discourse, power),
            'freirean': self._freirean_critique(policy_text),
            'hooks': self._hooks_critique(policy_text),
            'haraway': self._haraway_critique(policy_text)
        }
        
        return critiques
    
    def _foucauldian_critique(
        self,
        discourse: Dict,
        power: Dict
    ) -> str:
        """Foucauldian power/knowledge critique"""
        
        subject_creation = len(discourse.get('subject_creation', []))
        governance = len(discourse.get('governance_mechanisms', []))
        
        if subject_creation > 2 and governance > 0:
            return ("Foucauldian Analysis: Policy creates subjects through categorization and "
                   "employs surveillance mechanisms. Consider how these power relations shape "
                   "possibilities for community self-determination.")
        else:
            return "Foucauldian Analysis: Limited evidence of problematic subject creation or surveillance."
    
    def _freirean_critique(self, policy_text: str) -> str:
        """Freirean critical pedagogy critique"""
        
        # Check for participatory language
        participatory_terms = ['participatory', 'community-led', 'co-design', 'dialogue', 'collaboration']
        participatory_count = sum(1 for term in participatory_terms if term in policy_text.lower())
        
        if participatory_count >= 2:
            return "Freirean Analysis: Policy shows promise of problem-posing approach with community participation."
        else:
            return ("Freirean Critique: Policy appears to employ 'banking model' - top-down approach lacking "
                   "genuine community participation and problem-posing dialogue.")
    
    def _hooks_critique(self, policy_text: str) -> str:
        """bell hooks intersectional critique"""
        
        # Check for intersectional awareness
        intersectional_terms = ['intersectional', 'race', 'gender', 'class', 'compounded', 'multiple']
        intersectional_count = sum(1 for term in intersectional_terms if term in policy_text.lower())
        
        if intersectional_count >= 3:
            return "hooks' Framework: Policy demonstrates intersectional awareness of compounded disadvantages."
        else:
            return ("hooks' Critique: Policy lacks intersectional analysis. Consider how race, class, and "
                   "gender intersect to create unique experiences of disadvantage.")
    
    def _haraway_critique(self, policy_text: str) -> str:
        """Haraway's situated knowledge critique"""
        
        # Check for acknowledgment of multiple knowledge systems
        knowledge_terms = ['local knowledge', 'indigenous', 'lived experience', 'community wisdom', 'situated']
        knowledge_count = sum(1 for term in knowledge_terms if term in policy_text.lower())
        
        if knowledge_count >= 2:
            return "Haraway's Framework: Policy recognizes multiple knowledge systems and situated perspectives."
        else:
            return ("Haraway's Critique: Policy assumes objective, universal knowledge. "
                   "Consider incorporating situated, local knowledge systems.")
    
    def _calculate_equity_score(
        self,
        discourse: Dict,
        power: Dict,
        biases: List
    ) -> float:
        """Calculate overall equity score for policy"""
        
        base_score = 1.0
        
        # Penalty for power asymmetry
        power_asymmetry = power.get('power_asymmetry_score', 0)
        if power_asymmetry > 2.0:
            base_score -= 0.3
        elif power_asymmetry > 1.0:
            base_score -= 0.15
        
        # Penalty for biases
        high_severity_biases = len([b for b in biases if b.get('severity') == 'high'])
        medium_severity_biases = len([b for b in biases if b.get('severity') == 'medium'])
        
        base_score -= (high_severity_biases * 0.15)
        base_score -= (medium_severity_biases * 0.08)
        
        return max(0.0, min(1.0, base_score))
    
    def _generate_policy_recommendations(
        self,
        analysis: Dict[str, Any]
    ) -> List[str]:
        """Generate recommendations for policy improvement"""
        
        recommendations = []
        
        equity_score = analysis['overall_equity_score']
        
        if equity_score < 0.6:
            recommendations.append(
                "Overall equity score is low. Major revision recommended to address power imbalances and biases."
            )
        
        # Address specific biases
        for bias in analysis['bias_detection']:
            if bias['type'] == PolicyBiasType.DEFICIT_FRAMING.value:
                recommendations.append(
                    "Reframe from deficit model to asset-based approach that recognizes community strengths."
                )
            elif bias['type'] == PolicyBiasType.PATERNALISTIC.value:
                recommendations.append(
                    "Replace paternalistic language with empowering, community-centered language."
                )
            elif bias['type'] == PolicyBiasType.EXCLUSIONARY_LANGUAGE.value:
                recommendations.append(
                    "Revise exclusionary language to be more inclusive and recognitional."
                )
            elif bias['type'] == PolicyBiasType.TECHNOCRATIC_OBSCURITY.value:
                recommendations.append(
                    "Simplify technical jargon to enhance accessibility and democratic participation."
                )
        
        # Power dynamics
        power_asymmetry = analysis['power_dynamics'].get('power_asymmetry_score', 0)
        if power_asymmetry > 2.0:
            recommendations.append(
                "Rebalance power dynamics by increasing community agency and participatory elements."
            )
        
        if not recommendations:
            recommendations.append(
                "Policy demonstrates strong equity foundations. Continue monitoring for inclusive language."
            )
        
        return recommendations
    
    def compare_policy_versions(
        self,
        original_text: str,
        revised_text: str,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Compare two versions of a policy to assess improvements"""
        
        original_analysis = self.analyze_policy_document(original_text, metadata)
        revised_analysis = self.analyze_policy_document(revised_text, metadata)
        
        comparison = {
            'original_equity_score': original_analysis['overall_equity_score'],
            'revised_equity_score': revised_analysis['overall_equity_score'],
            'improvement': revised_analysis['overall_equity_score'] - original_analysis['overall_equity_score'],
            'biases_addressed': [],
            'remaining_concerns': revised_analysis['bias_detection'],
            'recommendation': ''
        }
        
        # Identify which biases were addressed
        original_bias_types = {b['type'] for b in original_analysis['bias_detection']}
        revised_bias_types = {b['type'] for b in revised_analysis['bias_detection']}
        
        comparison['biases_addressed'] = list(original_bias_types - revised_bias_types)
        
        if comparison['improvement'] > 0.2:
            comparison['recommendation'] = "Significant improvement in equity. Revised version recommended."
        elif comparison['improvement'] > 0:
            comparison['recommendation'] = "Modest improvement. Consider additional revisions."
        else:
            comparison['recommendation'] = "No improvement or regression. Major revision needed."
        
        return comparison