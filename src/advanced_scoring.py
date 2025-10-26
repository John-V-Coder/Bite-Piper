"""
Advanced Priority Scoring System with Logical Analysis

This module implements sophisticated logic for calculating priority scores
based on socio-economic indicators with cross-validation and risk assessment.
"""

# Indicator Thresholds (based on international poverty standards)
THRESHOLDS = {
    'poverty_rate': {
        'extreme': 60,      # Extreme poverty
        'severe': 40,       # Severe poverty
        'moderate': 20,     # Moderate poverty
        'low': 10          # Low poverty
    },
    'income': {
        'extreme': 1200,    # < $1200/year (~$3.3/day - below World Bank extreme poverty)
        'severe': 2000,     # < $2000/year (~$5.5/day)
        'moderate': 3500,   # < $3500/year (~$9.6/day)
        'adequate': 6000    # > $6000/year (~$16.4/day)
    },
    'wealth_index': {
        'extreme': 20,      # Extremely low assets
        'severe': 35,       # Very low assets
        'moderate': 50,     # Moderate assets
        'good': 70          # Good assets
    },
    'ppi': {
        'extreme': 80,      # Very high poverty probability
        'severe': 60,       # High poverty probability
        'moderate': 40,     # Moderate poverty probability
        'low': 20          # Low poverty probability
    },
    'consumption': {
        'extreme': 1000,    # Subsistence level
        'severe': 1800,     # Below basic needs
        'moderate': 3000,   # Basic needs met
        'adequate': 5000    # Comfortable level
    },
    'literacy': {
        'extreme': 40,      # Critical literacy crisis
        'severe': 55,       # Very low literacy
        'moderate': 70,     # Moderate literacy
        'good': 85          # High literacy
    }
}

# Indicator Weights (must sum to 1.0)
INDICATOR_WEIGHTS = {
    'poverty_rate': 0.25,
    'income': 0.15,
    'wealth_index': 0.20,
    'ppi': 0.15,
    'consumption': 0.10,
    'literacy': 0.15
}


def validate_indicators(indicators):
    """
    Validate and check consistency across indicators
    
    Returns: dict with validation results and warnings
    """
    warnings = []
    
    # Check for missing indicators
    required = ['PovertyRate', 'HouseholdIncomePerCapita', 'WealthIndex', 
                'PPI', 'ConsumptionExpenditure', 'LiteracyRate']
    missing = [ind for ind in required if ind not in indicators]
    if missing:
        warnings.append(f"Missing indicators: {', '.join(missing)}")
    
    # Consistency check: High poverty should correlate with low income
    if 'PovertyRate' in indicators and 'HouseholdIncomePerCapita' in indicators:
        poverty = indicators['PovertyRate']
        income = indicators['HouseholdIncomePerCapita']
        
        if poverty > 50 and income > 5000:
            warnings.append("Inconsistency: High poverty (>50%) but high income (>$5000)")
        elif poverty < 20 and income < 2000:
            warnings.append("Inconsistency: Low poverty (<20%) but low income (<$2000)")
    
    # Consistency check: PPI should align with poverty rate
    if 'PovertyRate' in indicators and 'PPI' in indicators:
        poverty = indicators['PovertyRate']
        ppi = indicators['PPI']
        
        if poverty > 50 and ppi < 40:
            warnings.append("Inconsistency: High poverty but low PPI score")
        elif poverty < 20 and ppi > 60:
            warnings.append("Inconsistency: Low poverty but high PPI score")
    
    # Consistency check: Wealth index should correlate with income
    if 'WealthIndex' in indicators and 'HouseholdIncomePerCapita' in indicators:
        wealth = indicators['WealthIndex']
        income = indicators['HouseholdIncomePerCapita']
        
        if wealth < 30 and income > 5000:
            warnings.append("Inconsistency: Low wealth but high income")
        elif wealth > 70 and income < 2000:
            warnings.append("Inconsistency: High wealth but low income")
    
    return {
        'valid': len(warnings) == 0,
        'warnings': warnings
    }


def calculate_indicator_score(indicator_name, value):
    """
    Calculate normalized score for a single indicator (0.0 to 1.0)
    
    Returns: tuple (score, severity_level, explanation)
    """
    if indicator_name == 'PovertyRate':
        if value >= THRESHOLDS['poverty_rate']['extreme']:
            return 1.0, 'EXTREME', f"Extreme poverty crisis ({value}%)"
        elif value >= THRESHOLDS['poverty_rate']['severe']:
            return 0.8, 'SEVERE', f"Severe poverty ({value}%)"
        elif value >= THRESHOLDS['poverty_rate']['moderate']:
            return 0.5, 'MODERATE', f"Moderate poverty ({value}%)"
        elif value >= THRESHOLDS['poverty_rate']['low']:
            return 0.2, 'LOW', f"Low poverty ({value}%)"
        else:
            return 0.0, 'MINIMAL', f"Minimal poverty ({value}%)"
    
    elif indicator_name == 'HouseholdIncomePerCapita':
        if value < THRESHOLDS['income']['extreme']:
            return 1.0, 'EXTREME', f"Extreme poverty income (${value}/year, < $3.3/day)"
        elif value < THRESHOLDS['income']['severe']:
            return 0.8, 'SEVERE', f"Very low income (${value}/year)"
        elif value < THRESHOLDS['income']['moderate']:
            return 0.5, 'MODERATE', f"Below-average income (${value}/year)"
        elif value < THRESHOLDS['income']['adequate']:
            return 0.2, 'LOW', f"Moderate income (${value}/year)"
        else:
            return 0.0, 'ADEQUATE', f"Adequate income (${value}/year)"
    
    elif indicator_name == 'WealthIndex':
        if value < THRESHOLDS['wealth_index']['extreme']:
            return 1.0, 'EXTREME', f"Extremely low assets ({value}/100)"
        elif value < THRESHOLDS['wealth_index']['severe']:
            return 0.8, 'SEVERE', f"Very low assets ({value}/100)"
        elif value < THRESHOLDS['wealth_index']['moderate']:
            return 0.5, 'MODERATE', f"Limited assets ({value}/100)"
        elif value < THRESHOLDS['wealth_index']['good']:
            return 0.2, 'LOW', f"Moderate assets ({value}/100)"
        else:
            return 0.0, 'GOOD', f"Good assets ({value}/100)"
    
    elif indicator_name == 'PPI':
        if value >= THRESHOLDS['ppi']['extreme']:
            return 1.0, 'EXTREME', f"Very high poverty probability ({value}%)"
        elif value >= THRESHOLDS['ppi']['severe']:
            return 0.8, 'SEVERE', f"High poverty probability ({value}%)"
        elif value >= THRESHOLDS['ppi']['moderate']:
            return 0.5, 'MODERATE', f"Moderate poverty risk ({value}%)"
        elif value >= THRESHOLDS['ppi']['low']:
            return 0.2, 'LOW', f"Low poverty risk ({value}%)"
        else:
            return 0.0, 'MINIMAL', f"Minimal poverty risk ({value}%)"
    
    elif indicator_name == 'ConsumptionExpenditure':
        if value < THRESHOLDS['consumption']['extreme']:
            return 1.0, 'EXTREME', f"Subsistence-level spending (${value}/year)"
        elif value < THRESHOLDS['consumption']['severe']:
            return 0.8, 'SEVERE', f"Below basic needs (${value}/year)"
        elif value < THRESHOLDS['consumption']['moderate']:
            return 0.5, 'MODERATE', f"Basic needs barely met (${value}/year)"
        elif value < THRESHOLDS['consumption']['adequate']:
            return 0.2, 'LOW', f"Modest spending (${value}/year)"
        else:
            return 0.0, 'ADEQUATE', f"Adequate spending (${value}/year)"
    
    elif indicator_name == 'LiteracyRate':
        if value < THRESHOLDS['literacy']['extreme']:
            return 1.0, 'EXTREME', f"Critical literacy crisis ({value}%)"
        elif value < THRESHOLDS['literacy']['severe']:
            return 0.8, 'SEVERE', f"Very low literacy ({value}%)"
        elif value < THRESHOLDS['literacy']['moderate']:
            return 0.5, 'MODERATE', f"Moderate literacy ({value}%)"
        elif value < THRESHOLDS['literacy']['good']:
            return 0.2, 'LOW', f"Good literacy ({value}%)"
        else:
            return 0.0, 'HIGH', f"High literacy ({value}%)"
    
    return 0.0, 'UNKNOWN', f"Unknown indicator: {indicator_name}"


def calculate_urgency_multiplier(indicators):
    """
    Calculate urgency multiplier based on combined critical conditions
    
    Multiplier increases score when multiple extreme conditions exist
    """
    extreme_count = 0
    severe_count = 0
    
    # Count extreme and severe conditions
    for indicator_name, value in indicators.items():
        score, severity, _ = calculate_indicator_score(indicator_name, value)
        if severity == 'EXTREME':
            extreme_count += 1
        elif severity == 'SEVERE':
            severe_count += 1
    
    # Urgency multiplier logic
    if extreme_count >= 4:
        return 1.20, "CRISIS: Multiple extreme conditions (4+)"
    elif extreme_count >= 3:
        return 1.15, "EMERGENCY: Multiple extreme conditions (3)"
    elif extreme_count >= 2:
        return 1.10, "URGENT: Two extreme conditions"
    elif extreme_count >= 1 and severe_count >= 3:
        return 1.08, "High urgency: 1 extreme + 3 severe conditions"
    elif severe_count >= 4:
        return 1.05, "Elevated urgency: Multiple severe conditions"
    else:
        return 1.00, "Standard assessment"


def calculate_advanced_priority_score(indicators):
    """
    Calculate comprehensive priority score with advanced logic
    
    Returns:
        dict with:
        - score: float (0.0 - 1.0+, can exceed 1.0 with urgency multiplier)
        - priority_level: str (CRITICAL, HIGH, MEDIUM, LOW)
        - explanation: str (detailed reasoning)
        - indicator_breakdown: dict (individual indicator analysis)
        - warnings: list (consistency warnings)
        - urgency: dict (urgency assessment)
    """
    
    # Validate indicators
    validation = validate_indicators(indicators)
    
    # Calculate individual indicator scores
    indicator_breakdown = {}
    weighted_score = 0.0
    explanation_parts = []
    
    for indicator_name, value in indicators.items():
        # Calculate normalized score
        norm_score, severity, explanation = calculate_indicator_score(indicator_name, value)
        
        # Get weight for this indicator
        weight = INDICATOR_WEIGHTS.get(indicator_name.lower().replace('householdincomepe capita', 'income')
                                                    .replace('consumptionexpenditure', 'consumption')
                                                    .replace('literacyrate', 'literacy')
                                                    .replace('wealthindex', 'wealth_index')
                                                    .replace('povertyrate', 'poverty_rate'), 0.0)
        
        # Calculate weighted contribution
        weighted_contribution = norm_score * weight
        weighted_score += weighted_contribution
        
        # Store breakdown
        indicator_breakdown[indicator_name] = {
            'value': value,
            'normalized_score': norm_score,
            'severity': severity,
            'weight': weight,
            'contribution': weighted_contribution,
            'explanation': explanation
        }
        
        # Add to explanation if significant
        if severity in ['EXTREME', 'SEVERE', 'MODERATE']:
            explanation_parts.append(explanation)
    
    # Apply urgency multiplier
    urgency_multiplier, urgency_reason = calculate_urgency_multiplier(indicators)
    final_score = weighted_score * urgency_multiplier
    
    # Cap at 1.0 for display purposes (but keep higher for allocation)
    display_score = min(final_score, 1.0)
    
    # Determine priority level
    if display_score >= 0.70:
        priority_level = 'CRITICAL'
    elif display_score >= 0.50:
        priority_level = 'HIGH'
    elif display_score >= 0.30:
        priority_level = 'MEDIUM'
    else:
        priority_level = 'LOW'
    
    # Build comprehensive explanation
    full_explanation = " | ".join(explanation_parts)
    if urgency_multiplier > 1.0:
        full_explanation += f" | {urgency_reason}"
    
    return {
        'score': final_score,
        'display_score': display_score,
        'priority_level': priority_level,
        'explanation': full_explanation,
        'indicator_breakdown': indicator_breakdown,
        'warnings': validation['warnings'],
        'urgency': {
            'multiplier': urgency_multiplier,
            'reason': urgency_reason
        },
        'methodology': 'Advanced Multi-Indicator Assessment with Urgency Factors'
    }


def explain_priority_decision(result):
    """
    Generate detailed human-readable explanation of priority decision
    """
    lines = []
    lines.append(f"Priority Level: {result['priority_level']}")
    lines.append(f"Priority Score: {result['display_score']:.3f} (weighted: {result['score']:.3f})")
    lines.append(f"")
    lines.append(f"Indicator Analysis:")
    
    for indicator, details in result['indicator_breakdown'].items():
        severity_emoji = {
            'EXTREME': '🔴',
            'SEVERE': '🟠',
            'MODERATE': '🟡',
            'LOW': '🟢',
            'MINIMAL': '⚪',
            'ADEQUATE': '✅',
            'GOOD': '✅',
            'HIGH': '✅'
        }.get(details['severity'], '⚪')
        
        lines.append(f"  {severity_emoji} {indicator}: {details['explanation']}")
        lines.append(f"     Normalized: {details['normalized_score']:.2f} | Weight: {details['weight']*100:.0f}% | Contribution: {details['contribution']:.3f}")
    
    lines.append(f"")
    lines.append(f"Urgency Assessment:")
    lines.append(f"  Multiplier: {result['urgency']['multiplier']:.2f}x")
    lines.append(f"  Reason: {result['urgency']['reason']}")
    
    if result['warnings']:
        lines.append(f"")
        lines.append(f"⚠️ Data Consistency Warnings:")
        for warning in result['warnings']:
            lines.append(f"  • {warning}")
    
    return "\n".join(lines)
