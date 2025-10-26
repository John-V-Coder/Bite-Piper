# data_types.py - Parametric Types for Bite-Piper Data

from atom import Symbol, Expression

# The 'Type' Symbol for Metta
TypeSymbol = Symbol("Type")

# --- PARAMETRIC TYPE DEFINITIONS ---

def List(type_atom):
    """
    (List $t) - A parametric type for a list of elements of type $t.
    Example: (List Number), (List Region)
    """
    return Expression([Symbol("List"), type_atom])

def Metric(metric_name, type_atom):
    """
    (Metric Name Type) - A specific socioeconomic indicator.
    Example: (Metric "PovertyRate" Number)
    """
    return Expression([Symbol("Metric"), Symbol(metric_name), type_atom])

# --- DATA STRUCTURES (as MeTTa Expressions) ---

# The core data type for Bite-Piper, defined in the prompt:
# (: SocioEconomicData (-> Region (List Metric) DataPoint))
def SocioEconomicData(region, metrics_list, datapoint):
    """
    (SocioEconomicData Region (List Metric) DataPoint)
    A fact storing collected data.
    """
    return Expression([
        Symbol("SocioEconomicData"),
        region,
        metrics_list,
        datapoint
    ])

# Example region and metric symbols
RegionA = Symbol("RegionA")
RegionB = Symbol("RegionB")

# --- INCOME & WEALTH INDICATORS ---

# 1. Household Income Per Capita
# Average income per household member
HouseholdIncomePerCapita = Symbol("HouseholdIncomePerCapita")

# 2. Poverty Headcount Ratio
# % of population below the national poverty line
PovertyRate = Symbol("PovertyRate")

# 3. Wealth Index (IWI)
# Composite asset-based score measuring households' wealth (0-100)
WealthIndex = Symbol("WealthIndex")

# 4. PPI (Progress out of Poverty Index)
# Probability that a household lives below a poverty threshold (0-100)
PPI = Symbol("PPI")

# 5. Consumption Expenditure
# Household spending on goods and services
ConsumptionExpenditure = Symbol("ConsumptionExpenditure")

# --- EDUCATION INDICATORS ---
LiteracyRate = Symbol("LiteracyRate")