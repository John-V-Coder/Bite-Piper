# Multi-stakeholder interest balancing

"""
Stakeholder Mediator Module for Bite-Piper
Balances multiple stakeholder interests using philosophical frameworks and civic data
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from civic_client import CivicDataClient
from philosophical_framework import PhilosophicalFramework


class StakeholderType(Enum):
    """Types of stakeholders"""
    COMMUNITY = "community"
    GOVERNMENT = "government"
    NGO = "ngo"
    PRIVATE_SECTOR = "private_sector"
    BENEFICIARIES = "beneficiaries"
    EXPERTS = "experts"


class ConflictType(Enum):
    """Types of conflicts between stakeholders"""
    RESOURCE_ALLOCATION = "resource_allocation"
    PRIORITY_SETTING = "priority_setting"
    METHODOLOGY = "methodology"
    TRANSPARENCY = "transparency"
    IMPLEMENTATION = "implementation"


@dataclass
class StakeholderPosition:
    """Position of a stakeholder on a decision"""
    stakeholder_id: str
    stakeholder_type: StakeholderType
    interests: List[str]
    concerns: List[str]
    priorities: Dict[str, float]
    influence_level: float


class StakeholderMediator:
    """Mediates between multiple stakeholders using deliberative democracy principles"""
    
    def __init__(self, civic_client: Optional[CivicDataClient] = None,
                 api_keys: Optional[Dict[str, str]] = None):
        self.civic_client = civic_client or CivicDataClient(api_keys)
        self.framework = PhilosophicalFramework()
    
    def mediate_stakeholders(
        self,
        decision_data: Dict[str, Any],
        stakeholders: List[Dict[str, Any]],
        conflict_areas: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Mediate between multiple stakeholders to find balanced solution
        
        Args:
            decision_data: Decision or allocation data
            stakeholders: List of stakeholder positions
            conflict_areas: Specific areas of conflict to address
            
        Returns:
            Mediation analysis with recommendations
        """
        
        mediation = {
            'decision_id': decision_data.get('id', 'unknown'),
            'stakeholder_analysis': {},
            'conflicts_identified': [],
            'common_ground': [],
            'mediation_strategies': [],
            'balanced_solution': {},
            'philosophical_approach': {}
        }
        
        # Analyze each stakeholder position
        stakeholder_positions = self._analyze_stakeholder_positions(stakeholders, decision_data)
        mediation['stakeholder_analysis'] = stakeholder_positions
        
        # Identify conflicts
        conflicts = self._identify_conflicts(stakeholder_positions, conflict_areas)
        mediation['conflicts_identified'] = conflicts
        
        # Find common ground (Young's communicative democracy)
        common_ground = self._find_common_ground(stakeholder_positions)
        mediation['common_ground'] = common_ground
        
        # Apply philosophical frameworks for mediation
        philosophical = self._apply_mediation_frameworks(stakeholder_positions, conflicts)
        mediation['philosophical_approach'] = philosophical
        
        # Generate mediation strategies
        strategies = self._generate_mediation_strategies(conflicts, stakeholder_positions)
        mediation['mediation_strategies'] = strategies
        
        # Propose balanced solution
        balanced = self._propose_balanced_solution(decision_data, stakeholder_positions, conflicts)
        mediation['balanced_solution'] = balanced
        
        return mediation
    
    def _analyze_stakeholder_positions(
        self,
        stakeholders: List[Dict[str, Any]],
        decision_data: Dict[str, Any]
    ) -> Dict[str, Dict[str, Any]]:
        """Analyze positions of each stakeholder"""
        
        positions = {}
        
        for stakeholder in stakeholders:
            stakeholder_id = stakeholder.get('id', 'unknown')
            stakeholder_type = stakeholder.get('type', 'community')
            
            position = {
                'id': stakeholder_id,
                'type': stakeholder_type,
                'interests': stakeholder.get('interests', []),
                'concerns': stakeholder.get('concerns', []),
                'priorities': stakeholder.get('priorities', {}),
                'influence': stakeholder.get('influence', 0.5),
                'affected_regions': stakeholder.get('regions', []),
                'position_on_decision': 'neutral'
            }
            
            # Determine position on decision
            if stakeholder.get('supports_decision'):
                position['position_on_decision'] = 'supportive'
            elif stakeholder.get('opposes_decision'):
                position['position_on_decision'] = 'opposed'
            
            # Assess power dynamics (Foucault)
            position['power_assessment'] = self._assess_stakeholder_power(stakeholder, decision_data)
            
            positions[stakeholder_id] = position
        
        return positions
    
    def _assess_stakeholder_power(
        self,
        stakeholder: Dict[str, Any],
        decision_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Assess power dynamics of stakeholder (Foucauldian analysis)"""
        
        foucault = self.framework.get_thinker_perspective('foucault')
        
        power_assessment = {
            'formal_authority': 0.0,
            'resource_control': 0.0,
            'knowledge_expertise': 0.0,
            'network_influence': 0.0,
            'overall_power': 0.0
        }
        
        stakeholder_type = stakeholder.get('type', 'community')
        
        # Assign power levels based on stakeholder type
        if stakeholder_type == 'government':
            power_assessment['formal_authority'] = 0.9
            power_assessment['resource_control'] = 0.8
        elif stakeholder_type == 'community':
            power_assessment['formal_authority'] = 0.2
            power_assessment['network_influence'] = 0.6
        elif stakeholder_type == 'experts':
            power_assessment['knowledge_expertise'] = 0.9
            power_assessment['formal_authority'] = 0.4
        elif stakeholder_type == 'ngo':
            power_assessment['network_influence'] = 0.7
            power_assessment['knowledge_expertise'] = 0.6
        elif stakeholder_type == 'beneficiaries':
            power_assessment['formal_authority'] = 0.1
            power_assessment['network_influence'] = 0.3
        
        # Calculate overall power
        power_assessment['overall_power'] = (
            power_assessment['formal_authority'] * 0.3 +
            power_assessment['resource_control'] * 0.3 +
            power_assessment['knowledge_expertise'] * 0.2 +
            power_assessment['network_influence'] * 0.2
        )
        
        return power_assessment
    
    def _identify_conflicts(
        self,
        stakeholder_positions: Dict[str, Dict[str, Any]],
        conflict_areas: Optional[List[str]]
    ) -> List[Dict[str, Any]]:
        """Identify conflicts between stakeholder positions"""
        
        conflicts = []
        
        # Check for priority conflicts
        priority_conflict = self._check_priority_conflicts(stakeholder_positions)
        if priority_conflict:
            conflicts.append(priority_conflict)
        
        # Check for power imbalance conflicts
        power_conflict = self._check_power_imbalances(stakeholder_positions)
        if power_conflict:
            conflicts.append(power_conflict)
        
        # Check for opposing positions
        position_conflicts = self._check_position_conflicts(stakeholder_positions)
        conflicts.extend(position_conflicts)
        
        return conflicts
    
    def _check_priority_conflicts(
        self,
        stakeholder_positions: Dict[str, Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """Check for conflicting priorities"""
        
        all_priorities = {}
        
        for stakeholder_id, position in stakeholder_positions.items():
            priorities = position.get('priorities', {})
            for priority, value in priorities.items():
                if priority not in all_priorities:
                    all_priorities[priority] = []
                all_priorities[priority].append((stakeholder_id, value))
        
        # Find priorities with high variance
        conflicted_priorities = []
        for priority, values in all_priorities.items():
            if len(values) > 1:
                priority_values = [v[1] for v in values]
                variance = sum((x - sum(priority_values)/len(priority_values))**2 for x in priority_values) / len(priority_values)
                
                if variance > 0.3:  # High variance threshold
                    conflicted_priorities.append({
                        'priority': priority,
                        'variance': variance,
                        'stakeholders': [v[0] for v in values]
                    })
        
        if conflicted_priorities:
            return {
                'conflict_type': ConflictType.PRIORITY_SETTING.value,
                'severity': 'medium',
                'description': 'Stakeholders have conflicting priorities',
                'details': conflicted_priorities
            }
        
        return None
    
    def _check_power_imbalances(
        self,
        stakeholder_positions: Dict[str, Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """Check for power imbalances (Foucauldian critique)"""
        
        power_levels = []
        for position in stakeholder_positions.values():
            power_assessment = position.get('power_assessment', {})
            power_levels.append(power_assessment.get('overall_power', 0))
        
        if power_levels:
            max_power = max(power_levels)
            min_power = min(power_levels)
            power_ratio = max_power / min_power if min_power > 0 else float('inf')
            
            if power_ratio > 3.0:  # Significant power imbalance
                return {
                    'conflict_type': 'power_imbalance',
                    'severity': 'high',
                    'description': f'Significant power imbalance (ratio: {power_ratio:.1f}:1)',
                    'philosophical_critique': 'Foucault: Power asymmetry may marginalize less powerful stakeholders',
                    'recommendation': 'Apply deliberative democracy principles to amplify marginalized voices'
                }
        
        return None
    
    def _check_position_conflicts(
        self,
        stakeholder_positions: Dict[str, Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Check for directly opposing positions"""
        
        conflicts = []
        
        supportive = [s for s, p in stakeholder_positions.items() if p['position_on_decision'] == 'supportive']
        opposed = [s for s, p in stakeholder_positions.items() if p['position_on_decision'] == 'opposed']
        
        if supportive and opposed:
            conflicts.append({
                'conflict_type': 'direct_opposition',
                'severity': 'high',
                'description': f'{len(supportive)} stakeholder(s) support vs {len(opposed)} oppose',
                'supportive_stakeholders': supportive,
                'opposed_stakeholders': opposed
            })
        
        return conflicts
    
    def _find_common_ground(
        self,
        stakeholder_positions: Dict[str, Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Find common ground between stakeholders (Young's communicative democracy)"""
        
        young = self.framework.get_thinker_perspective('young')
        
        common_ground = []
        
        # Find shared interests
        all_interests = {}
        for position in stakeholder_positions.values():
            for interest in position.get('interests', []):
                if interest not in all_interests:
                    all_interests[interest] = []
                all_interests[interest].append(position['id'])
        
        # Identify interests shared by multiple stakeholders
        for interest, stakeholders in all_interests.items():
            if len(stakeholders) >= 2:
                common_ground.append({
                    'type': 'shared_interest',
                    'interest': interest,
                    'stakeholders': stakeholders,
                    'strength': len(stakeholders) / len(stakeholder_positions)
                })
        
        # Find shared concerns
        all_concerns = {}
        for position in stakeholder_positions.values():
            for concern in position.get('concerns', []):
                if concern not in all_concerns:
                    all_concerns[concern] = []
                all_concerns[concern].append(position['id'])
        
        for concern, stakeholders in all_concerns.items():
            if len(stakeholders) >= 2:
                common_ground.append({
                    'type': 'shared_concern',
                    'concern': concern,
                    'stakeholders': stakeholders,
                    'strength': len(stakeholders) / len(stakeholder_positions)
                })
        
        return common_ground
    
    def _apply_mediation_frameworks(
        self,
        stakeholder_positions: Dict[str, Dict[str, Any]],
        conflicts: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Apply philosophical frameworks for mediation"""
        
        frameworks = {
            'primary_approach': '',
            'frameworks_applied': [],
            'principles': []
        }
        
        # Young's communicative democracy
        young = self.framework.get_thinker_perspective('young')
        if young:
            frameworks['frameworks_applied'].append("Young's Communicative Democracy")
            frameworks['principles'].extend([
                "Inclusion of all affected stakeholders",
                "Respectful listening across differences",
                "Recognition of situated knowledge"
            ])
        
        # Freire's problem-posing approach
        freire = self.framework.get_thinker_perspective('freire')
        if freire:
            frameworks['frameworks_applied'].append("Freire's Problem-Posing Dialogue")
            frameworks['principles'].append("Participatory problem-solving with community")
        
        # Ostrom's polycentric governance
        ostrom = self.framework.get_thinker_perspective('ostrom')
        if ostrom:
            frameworks['frameworks_applied'].append("Ostrom's Polycentric Governance")
            frameworks['principles'].append("Multiple decision-making centers with coordination")
        
        frameworks['primary_approach'] = "Deliberative Democracy"
        
        return frameworks
    
    def _generate_mediation_strategies(
        self,
        conflicts: List[Dict[str, Any]],
        stakeholder_positions: Dict[str, Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate strategies for mediating conflicts"""
        
        strategies = []
        
        for conflict in conflicts:
            conflict_type = conflict.get('conflict_type')
            
            if conflict_type == ConflictType.PRIORITY_SETTING.value:
                strategies.append({
                    'conflict_addressed': conflict_type,
                    'strategy': 'Multi-criteria consensus building',
                    'approach': 'Facilitate deliberative dialogue to identify shared priorities',
                    'methods': [
                        'Structured stakeholder workshops',
                        'Priority ranking exercises',
                        'Trade-off analysis'
                    ]
                })
            
            elif conflict_type == 'power_imbalance':
                strategies.append({
                    'conflict_addressed': conflict_type,
                    'strategy': 'Power balancing through process design',
                    'approach': 'Amplify marginalized voices (Freirean empowerment)',
                    'methods': [
                        'Weighted voting that considers power asymmetries',
                        'Community-led participatory sessions',
                        'Provide resources for less powerful stakeholders to participate'
                    ]
                })
            
            elif conflict_type == 'direct_opposition':
                strategies.append({
                    'conflict_addressed': conflict_type,
                    'strategy': 'Interest-based mediation',
                    'approach': 'Focus on underlying interests rather than positions',
                    'methods': [
                        'Individual stakeholder consultations',
                        'Joint problem-solving sessions',
                        'Explore alternative scenarios that address core concerns'
                    ]
                })
        
        # General strategy: Build on common ground
        strategies.append({
            'conflict_addressed': 'all',
            'strategy': 'Common ground building',
            'approach': "Young's communicative democracy",
            'methods': [
                'Identify and emphasize shared interests',
                'Address shared concerns collaboratively',
                'Build trust through transparent communication'
            ]
        })
        
        return strategies
    
    def _propose_balanced_solution(
        self,
        decision_data: Dict[str, Any],
        stakeholder_positions: Dict[str, Dict[str, Any]],
        conflicts: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Propose balanced solution that addresses stakeholder concerns"""
        
        balanced = {
            'approach': 'Consensus-oriented with fairness safeguards',
            'modifications': [],
            'safeguards': [],
            'implementation': {}
        }
        
        # Propose modifications based on conflicts
        if any(c.get('conflict_type') == 'power_imbalance' for c in conflicts):
            balanced['modifications'].append({
                'modification': 'Enhanced community participation',
                'rationale': 'Address power imbalances by amplifying community voice',
                'implementation': 'Establish community advisory board with decision-making authority'
            })
        
        # Safeguards based on philosophical principles
        balanced['safeguards'] = [
            {
                'principle': 'Rawlsian safeguard',
                'description': 'Ensure least advantaged stakeholders benefit',
                'mechanism': 'Minimum allocation threshold for most disadvantaged regions'
            },
            {
                'principle': 'Procedural fairness',
                'description': 'Transparent and inclusive decision process',
                'mechanism': 'Public explanation of all allocation decisions'
            },
            {
                'principle': 'Participatory design',
                'description': 'Community involvement in implementation',
                'mechanism': 'Co-design implementation plans with affected communities'
            }
        ]
        
        # Implementation approach
        balanced['implementation'] = {
            'phase_1': 'Stakeholder consultation and consensus building',
            'phase_2': 'Pilot implementation with community feedback',
            'phase_3': 'Full rollout with ongoing monitoring',
            'oversight': 'Multi-stakeholder oversight committee'
        }
        
        return balanced
    
    def assess_stakeholder_satisfaction(
        self,
        decision_data: Dict[str, Any],
        stakeholders: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Assess stakeholder satisfaction with decision"""
        
        assessment = {
            'overall_satisfaction': 0.0,
            'by_stakeholder': {},
            'concerns_addressed': [],
            'concerns_unaddressed': []
        }
        
        total_satisfaction = 0.0
        count = 0
        
        for stakeholder in stakeholders:
            stakeholder_id = stakeholder.get('id', 'unknown')
            
            # Calculate satisfaction based on concerns addressed
            concerns = stakeholder.get('concerns', [])
            interests = stakeholder.get('interests', [])
            
            addressed = stakeholder.get('concerns_addressed', [])
            satisfaction = len(addressed) / len(concerns) if concerns else 0.5
            
            assessment['by_stakeholder'][stakeholder_id] = {
                'satisfaction': satisfaction,
                'concerns_addressed': addressed,
                'interests_met': stakeholder.get('interests_met', [])
            }
            
            total_satisfaction += satisfaction
            count += 1
        
        if count > 0:
            assessment['overall_satisfaction'] = total_satisfaction / count
        
        return assessment