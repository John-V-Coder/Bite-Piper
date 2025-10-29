 # Tool definitions for data analysis

from typing import List, Dict, Any

TOOLS: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "analyze_socioeconomic_equity",
            "description": "Comprehensive analysis of socio-economic data to determine equitable funding allocation priorities. Evaluates poverty, wealth, income, and development indicators to identify regions most in need.",
            "parameters": {
                "type": "object",
                "properties": {
                    "region_data": {
                        "type": "object",
                        "description": "Socio-economic data for the region including household income, poverty rates, wealth index, PPI scores, consumption expenditure, and literacy rates."
                    },
                    "analysis_framework": {
                        "type": "string",
                        "enum": ["comprehensive", "poverty_focused", "development_index", "equity_weighted"],
                        "description": "Framework for analysis: comprehensive (all indicators), poverty_focused, development_index, or equity_weighted with historical correction."
                    },
                    "include_bias_assessment": {
                        "type": "boolean",
                        "description": "Whether to include bias detection and mitigation analysis in the assessment."
                    }
                },
                "required": ["region_data"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_funding_allocation",
            "description": "Calculate equitable funding allocation based on socio-economic indicators, priority levels, and historical equity considerations. Applies progressive allocation formulas with bias mitigation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "priority_level": {
                        "type": "string",
                        "enum": ["critical", "high", "medium", "low"],
                        "description": "Priority level determined from socio-economic analysis: critical, high, medium, or low."
                    },
                    "socioeconomic_indicators": {
                        "type": "object",
                        "description": "Key socio-economic indicators including poverty rate, wealth index, PPI score, and household income."
                    },
                    "historical_correction": {
                        "type": "boolean",
                        "description": "Apply historical equity correction for regions with past underinvestment."
                    },
                    "allocation_strategy": {
                        "type": "string",
                        "enum": ["progressive", "needs_based", "capability_focused", "hybrid"],
                        "description": "Allocation strategy: progressive (equity-weighted), needs_based, capability_focused, or hybrid approach."
                    }
                },
                "required": ["priority_level", "socioeconomic_indicators"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "detect_systemic_bias",
            "description": "Advanced bias detection across socioeconomic, geographic, and demographic dimensions. Identifies structural inequalities and suggests mitigation strategies.",
            "parameters": {
                "type": "object",
                "properties": {
                    "decision_data": {
                        "type": "object",
                        "description": "Decision data including allocation criteria, regional characteristics, and historical patterns."
                    },
                    "bias_categories": {
                        "type": "array",
                        "items": {"type": "string"},
                        "enum": ["socioeconomic", "geographic", "demographic", "data_manipulation", "all"],
                        "description": "Specific bias categories to analyze or 'all' for comprehensive assessment."
                    },
                    "severity_threshold": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 1,
                        "description": "Minimum severity threshold for flagging biases (0-1 scale, default: 0.3)."
                    }
                },
                "required": ["decision_data"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "generate_ethical_explanation",
            "description": "Generate comprehensive, philosophically-grounded explanations for funding decisions. Applies multiple ethical frameworks and provides transparent reasoning.",
            "parameters": {
                "type": "object",
                "properties": {
                    "decision_components": {
                        "type": "object",
                        "description": "Key decision components including allocation amount, priority level, and influencing factors."
                    },
                    "philosophical_frameworks": {
                        "type": "array",
                        "items": {"type": "string"},
                        "enum": ["socratic", "foucauldian", "freirean", "aristotelian", "rawlsian", "capability_approach", "all"],
                        "description": "Philosophical frameworks to apply in explanation."
                    },
                    "explanation_depth": {
                        "type": "string",
                        "enum": ["summary", "detailed", "comprehensive"],
                        "description": "Depth of explanation: summary, detailed, or comprehensive with full philosophical analysis."
                    },
                    "include_audit_trail": {
                        "type": "boolean",
                        "description": "Include decision atoms and audit trail references in explanation."
                    }
                },
                "required": ["decision_components"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "assess_policy_impact",
            "description": "Simulate and assess the impact of funding policies across different demographic groups and regions. Evaluates equity outcomes and potential unintended consequences.",
            "parameters": {
                "type": "object",
                "properties": {
                    "policy_parameters": {
                        "type": "object",
                        "description": "Policy parameters including allocation rules, target groups, and implementation timeline."
                    },
                    "impact_categories": {
                        "type": "array",
                        "items": {"type": "string"},
                        "enum": ["poverty_reduction", "wealth_distribution", "education_access", "health_improvement", "economic_mobility", "all"],
                        "description": "Impact categories to assess or 'all' for comprehensive analysis."
                    },
                    "time_horizon": {
                        "type": "string",
                        "enum": ["immediate", "short_term", "medium_term", "long_term"],
                        "description": "Time horizon for impact assessment: immediate (1 year), short_term (2-3 years), medium_term (5 years), long_term (10+ years)."
                    },
                    "include_equity_analysis": {
                        "type": "boolean",
                        "description": "Include detailed equity analysis across demographic groups."
                    }
                },
                "required": ["policy_parameters"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "validate_data_governance",
            "description": "Comprehensive data governance validation ensuring data quality, completeness, and ethical usage compliance. Verifies all 6 core socio-economic indicators.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data_input": {
                        "type": "object",
                        "description": "Input data to validate, including socio-economic indicators and metadata."
                    },
                    "validation_criteria": {
                        "type": "object",
                        "properties": {
                            "completeness_threshold": {"type": "number", "minimum": 0, "maximum": 1},
                            "timeliness_days": {"type": "integer", "minimum": 1, "maximum": 365},
                            "source_verification": {"type": "boolean"},
                            "accuracy_checks": {"type": "boolean"}
                        },
                        "description": "Validation criteria including completeness threshold, timeliness, source verification, and accuracy checks."
                    },
                    "generate_compliance_report": {
                        "type": "boolean",
                        "description": "Generate detailed compliance report with violations and recommendations."
                    }
                },
                "required": ["data_input"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_governance_compliance_check",
            "description": "Execute comprehensive governance compliance check across data governance, decision-making, ethical AI, and security policies. Generates audit report.",
            "parameters": {
                "type": "object",
                "properties": {
                    "check_categories": {
                        "type": "array",
                        "items": {"type": "string"},
                        "enum": ["data_governance", "decision_governance", "ethical_ai", "security_privacy", "all"],
                        "description": "Specific compliance categories to check or 'all' for comprehensive audit."
                    },
                    "include_success_metrics": {
                        "type": "boolean",
                        "description": "Include success metrics assessment in compliance report."
                    },
                    "generate_recommendations": {
                        "type": "boolean",
                        "description": "Generate actionable recommendations for compliance improvements."
                    }
                },
                "required": [],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "simulate_resource_allocation",
            "description": "Simulate different resource allocation scenarios to compare equity outcomes, efficiency, and impact across multiple regions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "regions_data": {
                        "type": "array",
                        "items": {"type": "object"},
                        "description": "Socio-economic data for multiple regions to compare allocation scenarios."
                    },
                    "allocation_scenarios": {
                        "type": "array",
                        "items": {"type": "string"},
                        "enum": ["equity_focused", "efficiency_focused", "needs_based", "historical_correction", "hybrid"],
                        "description": "Allocation scenarios to simulate and compare."
                    },
                    "budget_constraints": {
                        "type": "object",
                        "properties": {
                            "total_budget": {"type": "number"},
                            "minimum_allocation": {"type": "number"},
                            "maximum_allocation": {"type": "number"}
                        },
                        "description": "Budget constraints including total budget and allocation limits."
                    },
                    "evaluation_metrics": {
                        "type": "array",
                        "items": {"type": "string"},
                        "enum": ["poverty_reduction", "wealth_equality", "education_access", "health_improvement", "economic_mobility", "all"],
                        "description": "Metrics to evaluate scenario performance."
                    }
                },
                "required": ["regions_data", "allocation_scenarios"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "generate_philosophical_analysis",
            "description": "Apply philosophical frameworks to analyze civic decisions, examining power dynamics, ethical dimensions, and underlying assumptions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "decision_context": {
                        "type": "object",
                        "description": "Decision context including stakeholders, historical background, and ethical considerations."
                    },
                    "frameworks": {
                        "type": "array",
                        "items": {"type": "string"},
                        "enum": ["socratic", "foucauldian", "freirean", "aristotelian", "rawlsian", "haraway", "hooks", "all"],
                        "description": "Philosophical frameworks to apply in analysis."
                    },
                    "analysis_depth": {
                        "type": "string",
                        "enum": ["basic", "comprehensive", "critical"],
                        "description": "Depth of philosophical analysis: basic, comprehensive, or critical examination."
                    },
                    "include_practical_implications": {
                        "type": "boolean",
                        "description": "Include practical implications and actionable insights from philosophical analysis."
                    }
                },
                "required": ["decision_context"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_audit_trail",
            "description": "Create comprehensive audit trail for decisions with complete data lineage, reasoning steps, and compliance documentation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "decision_data": {
                        "type": "object",
                        "description": "Decision data including inputs, processing steps, and final outcomes."
                    },
                    "audit_components": {
                        "type": "array",
                        "items": {"type": "string"},
                        "enum": ["data_lineage", "reasoning_steps", "compliance_docs", "stakeholder_input", "all"],
                        "description": "Components to include in audit trail."
                    },
                    "format": {
                        "type": "string",
                        "enum": ["structured", "human_readable", "both"],
                        "description": "Audit trail format: structured for systems, human_readable for stakeholders, or both."
                    }
                },
                "required": ["decision_data"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    }
]