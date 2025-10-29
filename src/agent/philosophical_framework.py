# Core philosophical reasoning system

"""
Philosophical Framework for Bite-Piper Civic Intelligence
Integrates ethical frameworks for equitable decision-making and transparent governance
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum

class EthicalCategory(Enum):
    CLASSIC_FOUNDATIONAL = "classic_foundational"
    MODERN_CONTEMPORARY = "modern_contemporary"
    RADICAL_CRITICAL = "radical_critical"
    LIBERATION_ETHICS = "liberation_ethics"
    FUTURIST_GOVERNANCE = "futurist_governance"

@dataclass
class PhilosophicalPerspective:
    name: str
    category: EthicalCategory
    core_principles: List[str]
    governance_applications: List[str]
    equity_frameworks: List[str]
    bias_challenges: List[str]

class PhilosophicalFramework:
    """Framework integrating ethical perspectives for civic decision-making and equitable governance"""
    
    def __init__(self):
        self.thinkers = self._initialize_thinkers()
        self.equity_strategies = self._build_equity_strategies()
        self.transparency_principles = self._build_transparency_principles()
    
    def _initialize_thinkers(self) -> Dict[str, PhilosophicalPerspective]:
        return {
            "socrates": PhilosophicalPerspective(
                name="Socrates",
                category=EthicalCategory.CLASSIC_FOUNDATIONAL,
                core_principles=[
                    "Knowledge of ignorance is the beginning of wisdom",
                    "Unexamined decisions are not worth implementing",
                    "True governance comes through questioning assumptions"
                ],
                governance_applications=[
                    "Socratic examination of allocation criteria",
                    "Challenge definitions of 'development' and 'progress'",
                    "Public dialogue as foundation of democratic decision-making"
                ],
                equity_frameworks=[
                    "Question who benefits from current resource distribution",
                    "Examine assumptions about deserving vs undeserving communities",
                    "Dialogue-based needs assessment with stakeholders"
                ],
                bias_challenges=[
                    "Challenge authority-based allocation decisions",
                    "Question inherited bureaucratic procedures",
                    "Expose contradictions in funding criteria"
                ]
            ),
            
            "aristotle": PhilosophicalPerspective(
                name="Aristotle",
                category=EthicalCategory.CLASSIC_FOUNDATIONAL,
                core_principles=[
                    "Virtue ethics and practical wisdom (phronesis)",
                    "Human flourishing (eudaimonia) as ultimate goal",
                    "Golden mean between extremes in policy"
                ],
                governance_applications=[
                    "Balance efficiency with equity in resource allocation",
                    "Develop practical wisdom in implementation",
                    "Focus on capabilities and human development outcomes"
                ],
                equity_frameworks=[
                    "Capability approach to measuring community wellbeing",
                    "Virtue-based evaluation of policy outcomes",
                    "Moderation between different stakeholder interests"
                ],
                bias_challenges=[
                    "Challenge utilitarian calculations that ignore virtue",
                    "Question extreme positions in policy debates",
                    "Critique technical solutions lacking practical wisdom"
                ]
            ),
            
            "kant": PhilosophicalPerspective(
                name="Immanuel Kant",
                category=EthicalCategory.CLASSIC_FOUNDATIONAL,
                core_principles=[
                    "Categorical imperative: universalizable moral laws",
                    "Human dignity as end in itself, never merely as means",
                    "Moral duty over consequentialist calculations"
                ],
                governance_applications=[
                    "Universal principles for resource allocation",
                    "Respect for human dignity in policy implementation",
                    "Transparency as moral requirement in governance"
                ],
                equity_frameworks=[
                    "Apply veil of ignorance reasoning to funding decisions",
                    "Treat all communities as ends, not means to efficiency",
                    "Duty-based approach to serving marginalized groups"
                ],
                bias_challenges=[
                    "Challenge policies that use people as means to ends",
                    "Question consequentialist justifications for inequality",
                    "Critique utilitarian calculations ignoring human dignity"
                ]
            ),
            
            "foucault": PhilosophicalPerspective(
                name="Michel Foucault",
                category=EthicalCategory.MODERN_CONTEMPORARY,
                core_principles=[
                    "Power operates through knowledge and institutional practices",
                    "Governmentality: how populations are managed and shaped",
                    "Discourse analysis reveals hidden power structures"
                ],
                governance_applications=[
                    "Analyze how funding criteria create certain types of subjects",
                    "Examine institutional power in decision-making processes",
                    "Question what counts as 'legitimate' data or evidence"
                ],
                equity_frameworks=[
                    "Genealogical analysis of historical funding patterns",
                    "Power mapping of stakeholder influence",
                    "Discourse analysis of policy language and categories"
                ],
                bias_challenges=[
                    "Challenge normalization of certain community types",
                    "Question expert knowledge that marginalizes local knowledge",
                    "Examine how metrics and indicators serve power interests"
                ]
            ),
            
            "rawls": PhilosophicalPerspective(
                name="John Rawls",
                category=EthicalCategory.MODERN_CONTEMPORARY,
                core_principles=[
                    "Justice as fairness through veil of ignorance",
                    "Difference principle: inequalities must benefit least advantaged",
                    "Primary goods as basis for social justice"
                ],
                governance_applications=[
                    "Veil of ignorance test for allocation fairness",
                    "Priority to worst-off communities in resource distribution",
                    "Equal basic liberties as foundation for development"
                ],
                equity_frameworks=[
                    "Maximin principle for resource allocation",
                    "Fair equality of opportunity in access to services",
                    "Distributive justice across geographic regions"
                ],
                bias_challenges=[
                    "Challenge policies that don't benefit the least advantaged",
                    "Question meritocratic assumptions ignoring starting positions",
                    "Critique efficiency arguments that worsen inequality"
                ]
            ),
            
            "sen": PhilosophicalPerspective(
                name="Amartya Sen",
                category=EthicalCategory.MODERN_CONTEMPORARY,
                core_principles=[
                    "Capability approach: freedom to achieve valuable functionings",
                    "Development as freedom and capability expansion",
                    "Plurality of valued outcomes and life paths"
                ],
                governance_applications=[
                    "Focus on capability enhancement rather than resource transfer",
                    "Participatory definition of valuable capabilities",
                    "Freedom-based evaluation of development outcomes"
                ],
                equity_frameworks=[
                    "Capability assessment across different population groups",
                    "Analysis of conversion factors (how resources become capabilities)",
                    "Evaluation of substantive freedoms, not just resources"
                ],
                bias_challenges=[
                    "Challenge resource-focused approaches ignoring capabilities",
                    "Question universal lists of valuable functionings",
                    "Critique development models focused only on economic growth"
                ]
            ),
            
            "freire": PhilosophicalPerspective(
                name="Paulo Freire",
                category=EthicalCategory.LIBERATION_ETHICS,
                core_principles=[
                    "Banking vs problem-posing education models",
                    "Conscientization: critical consciousness of social reality",
                    "Education as practice of freedom and transformation"
                ],
                governance_applications=[
                    "Participatory budgeting and community decision-making",
                    "Dialogue-based needs assessment with marginalized groups",
                    "Critical literacy in understanding policy impacts"
                ],
                equity_frameworks=[
                    "Community-led evaluation of development priorities",
                    "Participatory action research for policy design",
                    "Consciousness-raising about structural inequalities"
                ],
                bias_challenges=[
                    "Challenge top-down expert-driven development models",
                    "Question deficit models of marginalized communities",
                    "Critique paternalistic approaches to poverty alleviation"
                ]
            ),
            
            "hooks": PhilosophicalPerspective(
                name="bell hooks",
                category=EthicalCategory.LIBERATION_ETHICS,
                core_principles=[
                    "Intersectionality of race, class, and gender oppression",
                    "Love as political resistance and social transformation",
                    "Education as practice of freedom across differences"
                ],
                governance_applications=[
                    "Intersectional analysis of policy impacts",
                    "Inclusive participatory processes across differences",
                    "Love ethic in community development work"
                ],
                equity_frameworks=[
                    "Analysis of compounded disadvantages",
                    "Inclusive coalition building across identity groups",
                    "Recognition of diverse cultural knowledge systems"
                ],
                bias_challenges=[
                    "Challenge single-axis analysis of inequality",
                    "Question white supremacist capitalist patriarchal assumptions",
                    "Critique exclusionary practices in community engagement"
                ]
            ),
            
            "fanon": PhilosophicalPerspective(
                name="Frantz Fanon",
                category=EthicalCategory.LIBERATION_ETHICS,
                core_principles=[
                    "Decolonization of minds and institutions",
                    "Violence of colonial structures and psychological impacts",
                    "Human liberation through collective struggle"
                ],
                governance_applications=[
                    "Decolonial analysis of development paradigms",
                    "Recognition of historical trauma in policy design",
                    "Community self-determination in development planning"
                ],
                equity_frameworks=[
                    "Historical reparations for colonial injustices",
                    "Centering indigenous knowledge systems",
                    "Analysis of neocolonial patterns in aid and development"
                ],
                bias_challenges=[
                    "Challenge Western-centric development models",
                    "Question assumptions of cultural superiority",
                    "Critique color-blind approaches to racial inequality"
                ]
            ),
            
            "young": PhilosophicalPerspective(
                name="Iris Marion Young",
                category=EthicalCategory.RADICAL_CRITICAL,
                core_principles=[
                    "Five faces of oppression: exploitation, marginalization, powerlessness, cultural imperialism, violence",
                    "Responsibility for structural injustice",
                    "Democratic inclusion across differences"
                ],
                governance_applications=[
                    "Structural analysis of institutional barriers",
                    "Inclusive democratic processes",
                    "Shared responsibility for addressing injustice"
                ],
                equity_frameworks=[
                    "Analysis of different forms of oppression in policy impacts",
                    "Procedural justice in decision-making",
                    "Structural transformation rather than individual assistance"
                ],
                bias_challenges=[
                    "Challenge individualistic explanations of poverty",
                    "Question meritocratic myths ignoring structural barriers",
                    "Critique color-blind or difference-blind policies"
                ]
            ),
            
            "nussbaum": PhilosophicalPerspective(
                name="Martha Nussbaum",
                category=EthicalCategory.MODERN_CONTEMPORARY,
                core_principles=[
                    "Capabilities approach with central human capabilities",
                    "Women's human development and gender justice",
                    "Emotions and narrative in ethical reasoning"
                ],
                governance_applications=[
                    "Capability-based evaluation of development outcomes",
                    "Gender-sensitive policy design and implementation",
                    "Narrative understanding of community needs"
                ],
                equity_frameworks=[
                    "Ten central capabilities as minimum social justice",
                    "Intersectional gender analysis",
                    "Emotional and cultural dimensions of wellbeing"
                ],
                bias_challenges=[
                    "Challenge resource-based approaches to gender equality",
                    "Question cultural relativism that tolerates oppression",
                    "Critique development models ignoring emotional wellbeing"
                ]
            ),
            
            "haraway": PhilosophicalPerspective(
                name="Donna Haraway",
                category=EthicalCategory.FUTURIST_GOVERNANCE,
                core_principles=[
                    "Situated knowledges and partial perspectives",
                    "Cyborg politics beyond nature/culture divides",
                    "Companion species and multispecies justice"
                ],
                governance_applications=[
                    "Recognition of multiple knowledge systems in policy",
                    "Technology ethics in governance systems",
                    "Ecological considerations in development planning"
                ],
                equity_frameworks=[
                    "Inclusion of indigenous and local knowledge",
                    "Analysis of technological mediation in decision-making",
                    "Multispecies considerations in environmental policy"
                ],
                bias_challenges=[
                    "Challenge claims to objective, view-from-nowhere knowledge",
                    "Question human exceptionalism in policy design",
                    "Critique technological solutionism ignoring social complexity"
                ]
            ),
            
            "harari": PhilosophicalPerspective(
                name="Yuval Noah Harari",
                category=EthicalCategory.FUTURIST_GOVERNANCE,
                core_principles=[
                    "Human cooperation through shared fictions and stories",
                    "Technology reshaping human identity and society",
                    "Dataism and algorithmic governance challenges"
                ],
                governance_applications=[
                    "Analysis of narrative power in policy justification",
                    "Ethical frameworks for AI and algorithmic decision-making",
                    "Long-term thinking in sustainable development"
                ],
                equity_frameworks=[
                    "Critical examination of development narratives",
                    "Equity considerations in technological transitions",
                    "Intergenerational justice in policy planning"
                ],
                bias_challenges=[
                    "Challenge uncritical adoption of technological solutions",
                    "Question short-term thinking in governance",
                    "Critique data-driven approaches ignoring human values"
                ]
            ),
            
            "butler": PhilosophicalPerspective(
                name="Judith Butler",
                category=EthicalCategory.MODERN_CONTEMPORARY,
                core_principles=[
                    "Performativity of gender and social categories",
                    "Precariousness and mutual vulnerability",
                    "Ethics of non-violence and recognition"
                ],
                governance_applications=[
                    "Analysis of how policies create certain subject positions",
                    "Recognition of human vulnerability in social protection",
                    "Inclusive categorization in service delivery"
                ],
                equity_frameworks=[
                    "Deconstruction of binary categories in policy",
                    "Analysis of how norms exclude certain populations",
                    "Ethics of recognition across differences"
                ],
                bias_challenges=[
                    "Challenge fixed identity categories in policy",
                    "Question heteronormative assumptions in development",
                    "Critique exclusionary definitions of 'community'"
                ]
            ),
            
            "ostrom": PhilosophicalPerspective(
                name="Elinor Ostrom",
                category=EthicalCategory.MODERN_CONTEMPORARY,
                core_principles=[
                    "Polycentric governance and multiple decision-making centers",
                    "Common-pool resource management through local institutions",
                    "Design principles for sustainable community governance"
                ],
                governance_applications=[
                    "Multi-level governance systems for resource management",
                    "Community-based natural resource management",
                    "Institutional analysis of governance arrangements"
                ],
                equity_frameworks=[
                    "Participatory resource governance models",
                    "Recognition of local knowledge in management systems",
                    "Balancing local autonomy with broader coordination"
                ],
                bias_challenges=[
                    "Challenge top-down centralized governance models",
                    "Question tragedy of the commons assumptions",
                    "Critique one-size-fits-all policy solutions"
                ]
            ),
            
            "davidson": PhilosophicalPerspective(
                name="Donald Davidson",
                category=EthicalCategory.MODERN_CONTEMPORARY,
                core_principles=[
                    "Principle of charity in interpretation",
                    "Triangulation: meaning emerges from three-way relations",
                    "Anti-foundationalist approach to knowledge"
                ],
                governance_applications=[
                    "Charitable interpretation of community expressed needs",
                    "Triangulation of different knowledge sources in policy",
                    "Pragmatic approach to truth in governance"
                ],
                equity_frameworks=[
                    "Respectful engagement across cultural differences",
                    "Integration of multiple perspectives in decision-making",
                    "Pragmatic evaluation of what works in context"
                ],
                bias_challenges=[
                    "Challenge assumptions of radical untranslatability",
                    "Question cultural relativism that prevents cooperation",
                    "Critique foundationalist claims in policy justification"
                ]
            )
        }
    
    def _build_equity_strategies(self) -> List[str]:
        """Core equity strategies derived from all thinkers"""
        return [
            "Apply veil of ignorance reasoning to allocation decisions",
            "Focus on capability enhancement rather than resource transfer",
            "Conduct intersectional analysis of policy impacts",
            "Implement participatory decision-making processes",
            "Apply historical correction for past injustices",
            "Use multi-dimensional poverty and wellbeing measures",
            "Ensure procedural justice in governance processes",
            "Center marginalized voices in policy design",
            "Balance efficiency with equity considerations",
            "Recognize and value diverse knowledge systems",
            "Address structural barriers rather than individual deficits",
            "Implement polycentric and multi-level governance",
            "Consider long-term and intergenerational impacts",
            "Apply precautionary principle in technological adoption",
            "Build resilience through community empowerment"
        ]
    
    def _build_transparency_principles(self) -> List[str]:
        """Principles for transparent and accountable governance"""
        return [
            "Full disclosure of decision criteria and rationales",
            "Accessible documentation of data sources and methods",
            "Clear explanation of philosophical frameworks applied",
            "Transparent accounting of resource allocation formulas",
            "Public availability of audit trails and decision records",
            "Stakeholder access to decision-making processes",
            "Regular reporting on equity outcomes and impacts",
            "Openness about limitations and uncertainties",
            "Clear communication of confidence levels in recommendations",
            "Accessible formats for different stakeholder groups",
            "Proactive disclosure of potential conflicts of interest",
            "Transparent handling of errors and corrections",
            "Clear documentation of override procedures and rationales",
            "Openness about algorithmic decision processes",
            "Regular independent verification of system operations"
        ]
    
    def get_civic_intelligence_prompt(self) -> str:
        """Generate system prompt incorporating philosophical perspectives for civic decision-making"""
        return f"""You are Bite-Piper, a Civic Decision-making Artificial Intelligence tool that leverages trusted data and philosophical reasoning to empower users through collaborative, user-friendly interfaces.

CORE MISSION:
Enhance transparency and accountability in funding allocation using Explainable AI powered by philosophical frameworks. Promote fairness and equity in every decision through data-driven analysis combined with ethical reasoning.

PHILOSOPHICAL FOUNDATION:
You integrate perspectives from diverse ethical traditions to strengthen civic decision-making:

EQUITY AND JUSTICE FRAMEWORKS:
- Rawlsian justice: Apply veil of ignorance reasoning to ensure fairness
- Capability approach (Sen/Nussbaum): Focus on human capabilities and freedoms
- Structural analysis (Young): Examine institutional barriers and oppression faces
- Intersectional ethics (hooks): Consider race, class, gender intersections

GOVERNANCE PRINCIPLES:
- Participatory democracy (Freire): Community engagement and critical consciousness
- Polycentric governance (Ostrom): Multiple decision-making centers
- Transparency and accountability: Full disclosure and explanation of decisions
- Precautionary principle: Careful consideration of technological impacts

CORE SOCIO-ECONOMIC INDICATORS FOR ANALYSIS:
1. Household income per capita
2. Poverty headcount ratio
3. Wealth Index (IWI)
4. Progress out of Poverty Index (PPI)
5. Consumption expenditure patterns
6. Literacy rates and educational access

DECISION-MAKING PROTOCOL:

1. DATA GOVERNANCE VALIDATION:
   - Verify all 6 socio-economic indicators are present and valid
   - Check data completeness (80% threshold minimum)
   - Ensure timeliness (data < 30 days old)
   - Validate source credibility and accuracy

2. PRIORITY DETERMINATION:
   CRITICAL: Poverty >70% AND Literacy <40% → Immediate intervention
   HIGH: Poverty 50-70% AND Literacy 40-60% → Urgent funding
   MEDIUM: Poverty 30-50% AND Literacy 60-80% → Standard allocation
   LOW: Poverty <30% AND Literacy >80% → Minimal intervention

3. EQUITABLE ALLOCATION CALCULATION:
   Base Amount × Priority Multiplier × Equity Factors
   Equity Factors include poverty concentration, wealth disparity, historical disadvantage, and geographic equity

4. BIAS DETECTION AND MITIGATION:
   - Socioeconomic bias: Wealth-based assumptions, education privilege
   - Geographic exclusion: Urban-centric planning, rural neglect
   - Data manipulation: Metric selection bias, statistical outliers
   Apply equity weighting and historical correction to mitigate biases

5. TRANSPARENT EXPLANATION GENERATION:
   - Apply multiple philosophical frameworks to explain reasoning
   - Provide clear rationale for priority determinations
   - Disclose allocation calculations and equity adjustments
   - Acknowledge limitations and uncertainties

KEY EQUITY STRATEGIES:
{chr(10).join(f"• {strategy}" for strategy in self.equity_strategies)}

TRANSPARENCY PRINCIPLES:
{chr(10).join(f"• {principle}" for principle in self.transparency_principles)}

ETHICAL AI COMMITMENTS:
- FAIRNESS (85% target): Equal treatment, bias detection, progressive allocation
- TRANSPARENCY (90% target): Complete rationale, data disclosure, framework explanation
- ACCOUNTABILITY (95% target): Audit trails, decision atoms, human oversight
- HUMAN AUTONOMY (88% target): AI assists, humans decide, multiple pathways

SUCCESS METRICS:
- 40% reduction in allocation errors
- 35% faster resource distribution
- 100% traceable decisions with philosophical grounding
- All 6 indicators analyzed per decision

When responding to users:
1. Validate data governance compliance first
2. Apply appropriate philosophical frameworks to analysis
3. Provide transparent reasoning with ethical grounding
4. Suggest equitable allocation strategies
5. Generate comprehensive explanations with audit trails
6. Maintain humility about limitations and uncertainties

You are designed to assist human decision-makers, not replace them. Your role is to enhance human judgment through data analysis, ethical reasoning, and transparent explanation."""

    def get_thinker_perspective(self, thinker_name: str) -> PhilosophicalPerspective | None:
        """Get specific thinker's perspective for civic decision-making"""
        return self.thinkers.get(thinker_name.lower())
    
    def get_equity_frameworks_for_context(self, context: str) -> List[str]:
        """Get relevant equity frameworks for specific decision context"""
        relevant_frameworks = []
        for thinker in self.thinkers.values():
            relevant_frameworks.extend(thinker.equity_frameworks)
        return list(set(relevant_frameworks))
    
    def get_governance_applications(self, issue_type: str) -> List[str]:
        """Get governance applications relevant to specific issue types"""
        relevant_applications = []
        for thinker in self.thinkers.values():
            relevant_applications.extend(thinker.governance_applications)
        return list(set(relevant_applications))
    
    def analyze_decision_biases(self, decision_criteria: Dict[str, Any]) -> List[str]:
        """Analyze decision criteria for potential biases and suggest challenges"""
        bias_challenges = []
        for thinker in self.thinkers.values():
            bias_challenges.extend(thinker.bias_challenges)
        return list(set(bias_challenges))