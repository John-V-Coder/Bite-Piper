# Data integration and analysis module

"""
Data Bridge for Bite-Piper - Integrated data analysis and socio-economic indicator processing
Connects civic data sources with equitable decision-making frameworks
"""

import requests
from datetime import datetime, timedelta
from urllib.parse import urlencode
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from civic_client import CivicDataClient, CivicDataException

logger = logging.getLogger(__name__)

class DataBridge:
    """
    Data Bridge for Bite-Piper - Integrates socio-economic data with ethical decision-making
    Provides unified interface for data analysis, equity scoring, and allocation recommendations
    """
    
    def __init__(self, api_keys: Dict[str, str] = None):
        self.api_keys = api_keys or {}
        
        try:
            self.civic_client = CivicDataClient(api_keys)
            self.use_civic_client = True
            logger.info("[DataBridge] Initialized with CivicDataClient")
        except Exception as e:
            logger.warning(f"[DataBridge] Failed to initialize CivicDataClient: {e}")
            self.use_civic_client = False
            self.civic_client = None
        
        # Core socio-economic indicators for Bite-Piper
        self.core_indicators = [
            "household_income_per_capita",
            "poverty_headcount_ratio", 
            "wealth_index_iwi",
            "ppi_score",
            "consumption_expenditure",
            "literacy_rate"
        ]
        
        # Equity analysis frameworks
        self.equity_frameworks = {
            "progressive_allocation": {
                "description": "Progressive allocation favoring disadvantaged regions",
                "weights": {"poverty": 0.4, "wealth_gap": 0.3, "historical_disadvantage": 0.3}
            },
            "needs_based": {
                "description": "Direct needs-based allocation using poverty and development indicators",
                "weights": {"poverty": 0.5, "education": 0.3, "infrastructure": 0.2}
            },
            "capability_focused": {
                "description": "Focus on enhancing human capabilities and opportunities",
                "weights": {"education": 0.4, "health": 0.3, "economic_mobility": 0.3}
            }
        }
    
    def _get_mock_socioeconomic_data(self, region_id: str) -> Dict[str, Any]:
        """
        Generate mock socio-economic data for demonstration when real API is unavailable
        """
        import random
        
        # Base profiles for different region types
        region_profiles = {
            "urban_affluent": {
                "household_income_per_capita": 45000,
                "poverty_headcount_ratio": 0.12,
                "wealth_index_iwi": 78,
                "ppi_score": 0.15,
                "consumption_expenditure": 38000,
                "literacy_rate": 0.94
            },
            "rural_developing": {
                "household_income_per_capita": 12000,
                "poverty_headcount_ratio": 0.65,
                "wealth_index_iwi": 28,
                "ppi_score": 0.72,
                "consumption_expenditure": 11000,
                "literacy_rate": 0.55
            },
            "mixed_medium": {
                "household_income_per_capita": 25000,
                "poverty_headcount_ratio": 0.35,
                "wealth_index_iwi": 52,
                "ppi_score": 0.45,
                "consumption_expenditure": 21000,
                "literacy_rate": 0.78
            }
        }
        
        # Determine region type based on ID or random selection
        if "urban" in region_id.lower():
            profile_type = "urban_affluent"
        elif "rural" in region_id.lower():
            profile_type = "rural_developing"
        else:
            profile_type = random.choice(list(region_profiles.keys()))
        
        base_data = region_profiles[profile_type].copy()
        
        # Add some random variation
        for key in base_data:
            if isinstance(base_data[key], (int, float)):
                variation = random.uniform(0.9, 1.1)
                base_data[key] = base_data[key] * variation
        
        return {
            'region_id': region_id,
            'data_source': 'mock_demonstration',
            'collection_date': datetime.now().isoformat(),
            'indicators': base_data,
            'completeness_score': 0.95,
            'validation_status': 'mock_data'
        }
    
    def get_region_socioeconomic_data(self, region_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get comprehensive socio-economic data for a region
        :param region_info: Dictionary with region details (type, code, name, etc.)
        :return: Socio-economic data with validation information
        """
        if self.use_civic_client and self.civic_client:
            try:
                logger.info(f"[DataBridge] Fetching socio-economic data for {region_info}")
                
                # Convert region info to CivicDataClient format
                location = {
                    'type': region_info.get('type', 'country'),
                    'code': region_info.get('code', region_info.get('name', 'unknown'))
                }
                
                profile = self.civic_client.get_socioeconomic_profile(location)
                
                # Transform to Bite-Piper format
                transformed_data = {
                    'region_id': region_info.get('id', region_info.get('name', 'unknown')),
                    'region_name': region_info.get('name', 'Unknown Region'),
                    'region_type': region_info.get('type', 'unknown'),
                    'data_source': 'civic_data_api',
                    'collection_date': datetime.now().isoformat(),
                    'indicators': {},
                    'completeness_score': profile.get('completeness_score', 0.0),
                    'validation_status': 'validated' if profile.get('completeness_score', 0) > 0.7 else 'partial'
                }
                
                # Map indicators to Bite-Piper format
                indicator_mapping = {
                    'NY.ADJ.NNTY.PC.CD': 'household_income_per_capita',
                    'SI.POV.DDAY': 'poverty_headcount_ratio',
                    'NY.ADJ.SVNX.GN.ZS': 'wealth_index_iwi',
                    'SE.ADT.LITR.ZS': 'literacy_rate'
                }
                
                for api_indicator, bite_piper_indicator in indicator_mapping.items():
                    if api_indicator in profile.get('indicators', {}):
                        indicator_data = profile['indicators'][api_indicator]
                        if indicator_data:
                            # Use most recent data
                            latest_data = max(indicator_data, key=lambda x: x.get('year', 0))
                            transformed_data['indicators'][bite_piper_indicator] = latest_data.get('value')
                
                # Add mock data for missing core indicators
                for indicator in self.core_indicators:
                    if indicator not in transformed_data['indicators']:
                        # Generate reasonable mock values based on available data
                        if indicator == 'ppi_score':
                            # PPI correlates with poverty rate
                            poverty_rate = transformed_data['indicators'].get('poverty_headcount_ratio', 0.3)
                            transformed_data['indicators'][indicator] = min(1.0, poverty_rate * 1.2)
                        elif indicator == 'consumption_expenditure':
                            # Consumption typically 70-90% of income
                            income = transformed_data['indicators'].get('household_income_per_capita', 20000)
                            transformed_data['indicators'][indicator] = income * 0.8
                
                logger.info(f"[DataBridge] Successfully retrieved data for {region_info['name']}")
                return transformed_data
                
            except CivicDataException as e:
                logger.error(f"[DataBridge] Civic data error for {region_info}: {e}")
                return self._get_mock_socioeconomic_data(region_info.get('id', 'unknown'))
            except Exception as e:
                logger.error(f"[DataBridge] Unexpected error fetching data: {e}")
                return self._get_mock_socioeconomic_data(region_info.get('id', 'unknown'))
        else:
            logger.info("[DataBridge] Using mock data (civic client not available)")
            return self._get_mock_socioeconomic_data(region_info.get('id', 'unknown'))
    
    def calculate_equity_score(self, socio_data: Dict[str, Any], framework: str = "progressive_allocation") -> Dict[str, Any]:
        """
        Calculate equity score for a region using specified framework
        :param socio_data: Socio-economic data from get_region_socioeconomic_data
        :param framework: Equity framework to use
        :return: Comprehensive equity assessment
        """
        indicators = socio_data.get('indicators', {})
        
        if framework not in self.equity_frameworks:
            framework = "progressive_allocation"
        
        weights = self.equity_frameworks[framework]["weights"]
        
        # Calculate dimension scores
        dimension_scores = {}
        
        # Poverty dimension (inverse - lower poverty = higher score)
        poverty_rate = indicators.get('poverty_headcount_ratio', 0.5)
        dimension_scores['poverty'] = max(0, 1 - poverty_rate)
        
        # Wealth dimension (inverse - lower wealth index = higher need)
        wealth_index = indicators.get('wealth_index_iwi', 50) / 100  # Normalize to 0-1
        dimension_scores['wealth_gap'] = 1 - wealth_index
        
        # Education dimension
        literacy_rate = indicators.get('literacy_rate', 0.7)
        dimension_scores['education'] = literacy_rate
        
        # Economic capacity dimension
        income = indicators.get('household_income_per_capita', 25000)
        # Normalize income (cap at $50,000 for scoring)
        dimension_scores['economic_capacity'] = min(1.0, income / 50000)
        
        # PPI dimension (higher PPI = higher poverty probability = higher need)
        ppi_score = indicators.get('ppi_score', 0.5)
        dimension_scores['poverty_probability'] = ppi_score
        
        # Calculate weighted composite score
        composite_score = 0.0
        total_weight = 0.0
        
        for dimension, weight in weights.items():
            if dimension in dimension_scores:
                composite_score += dimension_scores[dimension] * weight
                total_weight += weight
        
        if total_weight > 0:
            composite_score = composite_score / total_weight
        
        # Determine priority level
        if composite_score >= 0.7:
            priority_level = "critical"
        elif composite_score >= 0.5:
            priority_level = "high" 
        elif composite_score >= 0.3:
            priority_level = "medium"
        else:
            priority_level = "low"
        
        return {
            'region_id': socio_data['region_id'],
            'equity_framework': framework,
            'composite_equity_score': round(composite_score, 3),
            'priority_level': priority_level,
            'dimension_scores': {k: round(v, 3) for k, v in dimension_scores.items()},
            'framework_weights': weights,
            'calculation_timestamp': datetime.now().isoformat()
        }
    
    def recommend_funding_allocation(self, region_data: Dict[str, Any], 
                                   total_budget: float = 1000000,
                                   strategy: str = "equity_focused") -> Dict[str, Any]:
        """
        Recommend funding allocation based on socio-economic data and equity analysis
        :param region_data: Socio-economic data for the region
        :param total_budget: Total budget available for allocation
        :param strategy: Allocation strategy (equity_focused, needs_based, balanced)
        :return: Funding recommendation with detailed rationale
        """
        # Calculate equity score
        equity_assessment = self.calculate_equity_score(region_data)
        
        # Base allocation amounts by priority level
        base_allocation = {
            "critical": 500000,
            "high": 300000, 
            "medium": 150000,
            "low": 50000
        }
        
        priority = equity_assessment['priority_level']
        base_amount = base_allocation.get(priority, 100000)
        
        # Apply equity multipliers based on specific indicators
        multipliers = {
            "poverty_multiplier": 1 + (region_data['indicators'].get('poverty_headcount_ratio', 0.3) * 0.8),
            "wealth_multiplier": 1 + ((100 - region_data['indicators'].get('wealth_index_iwi', 50)) / 100),
            "education_multiplier": 1 + ((1 - region_data['indicators'].get('literacy_rate', 0.7)) * 0.6),
            "historical_correction": 1.2  # Base historical disadvantage correction
        }
        
        # Calculate final allocation
        if strategy == "equity_focused":
            # Heavy weighting on equity factors
            allocation_amount = base_amount * multipliers["poverty_multiplier"] * multipliers["wealth_multiplier"]
        elif strategy == "needs_based":
            # Focus on basic needs indicators
            allocation_amount = base_amount * multipliers["poverty_multiplier"] * multipliers["education_multiplier"]
        else:  # balanced
            # Balanced approach
            allocation_amount = base_amount * (
                multipliers["poverty_multiplier"] * 0.4 +
                multipliers["wealth_multiplier"] * 0.3 +
                multipliers["education_multiplier"] * 0.3
            )
        
        # Apply historical correction
        allocation_amount *= multipliers["historical_correction"]
        
        # Ensure allocation doesn't exceed reasonable bounds
        max_allocation = total_budget * 0.6  # No single region gets more than 60%
        allocation_amount = min(allocation_amount, max_allocation)
        
        # Round to reasonable precision
        allocation_amount = round(allocation_amount, 2)
        
        return {
            'region_id': region_data['region_id'],
            'priority_level': priority,
            'recommended_allocation': allocation_amount,
            'allocation_strategy': strategy,
            'base_amount': base_amount,
            'applied_multipliers': multipliers,
            'equity_score': equity_assessment['composite_equity_score'],
            'confidence_score': region_data.get('completeness_score', 0.5),
            'rationale': self._generate_allocation_rationale(region_data, equity_assessment, allocation_amount)
        }
    
    def _generate_allocation_rationale(self, region_data: Dict, equity_assessment: Dict, allocation: float) -> str:
        """Generate detailed rationale for allocation decision"""
        indicators = region_data['indicators']
        
        rationale_parts = [
            f"Funding allocation for {region_data['region_id']} is based on comprehensive socio-economic analysis."
        ]
        
        # Key factors influencing allocation
        if indicators.get('poverty_headcount_ratio', 0) > 0.5:
            rationale_parts.append(f"High poverty rate ({indicators['poverty_headcount_ratio']:.1%}) indicates significant need for intervention.")
        
        if indicators.get('wealth_index_iwi', 50) < 40:
            rationale_parts.append(f"Low wealth index ({indicators['wealth_index_iwi']}/100) suggests limited local resources for development.")
        
        if indicators.get('literacy_rate', 0.7) < 0.7:
            rationale_parts.append(f"Educational challenges (literacy rate: {indicators['literacy_rate']:.1%}) require targeted investment.")
        
        rationale_parts.append(f"Equity score of {equity_assessment['composite_equity_score']:.3f} supports {equity_assessment['priority_level']} priority classification.")
        rationale_parts.append(f"Recommended allocation: ${allocation:,.2f}")
        
        return " ".join(rationale_parts)
    
    def compare_regions(self, regions_data: List[Dict[str, Any]], 
                       comparison_framework: str = "comprehensive") -> Dict[str, Any]:
        """
        Compare multiple regions for equitable resource allocation
        :param regions_data: List of socio-economic data for multiple regions
        :param comparison_framework: Framework for comparison
        :return: Comparative analysis with equity insights
        """
        comparisons = {
            'regions': [],
            'equity_disparities': [],
            'allocation_recommendations': [],
            'comparison_timestamp': datetime.now().isoformat(),
            'framework_used': comparison_framework
        }
        
        total_equity_score = 0
        min_equity_score = float('inf')
        max_equity_score = float('-inf')
        
        for region_data in regions_data:
            # Calculate equity score for each region
            equity_score = self.calculate_equity_score(region_data)
            
            # Generate funding recommendation
            funding_rec = self.recommend_funding_allocation(region_data)
            
            region_comparison = {
                'region_id': region_data['region_id'],
                'socioeconomic_data': region_data,
                'equity_assessment': equity_score,
                'funding_recommendation': funding_rec
            }
            
            comparisons['regions'].append(region_comparison)
            
            # Update equity score statistics
            score = equity_score['composite_equity_score']
            total_equity_score += score
            min_equity_score = min(min_equity_score, score)
            max_equity_score = max(max_equity_score, score)
        
        # Calculate equity disparities
        if len(regions_data) > 1:
            disparity_ratio = max_equity_score / min_equity_score if min_equity_score > 0 else float('inf')
            average_equity_score = total_equity_score / len(regions_data)
            
            comparisons['equity_disparities'] = {
                'disparity_ratio': round(disparity_ratio, 2),
                'average_equity_score': round(average_equity_score, 3),
                'min_equity_score': round(min_equity_score, 3),
                'max_equity_score': round(max_equity_score, 3),
                'equity_gap': round(max_equity_score - min_equity_score, 3)
            }
        
        # Generate overall allocation recommendations
        total_recommended = sum(rec['funding_recommendation']['recommended_allocation'] 
                              for rec in comparisons['regions'])
        
        comparisons['allocation_recommendations'] = {
            'total_recommended_funding': total_recommended,
            'region_count': len(regions_data),
            'priority_distribution': self._analyze_priority_distribution(comparisons['regions'])
        }
        
        return comparisons
    
    def _analyze_priority_distribution(self, regions_comparison: List[Dict]) -> Dict[str, int]:
        """Analyze distribution of priority levels across regions"""
        distribution = {}
        for region_comp in regions_comparison:
            priority = region_comp['equity_assessment']['priority_level']
            distribution[priority] = distribution.get(priority, 0) + 1
        return distribution
    
    def validate_data_for_decision(self, region_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate data quality and completeness for decision-making
        :param region_data: Socio-economic data to validate
        :return: Validation report with quality scores
        """
        indicators = region_data.get('indicators', {})
        
        validation = {
            'region_id': region_data['region_id'],
            'completeness_score': 0.0,
            'timeliness_score': 0.0,
            'consistency_score': 0.0,
            'overall_quality': 'unknown',
            'validation_errors': [],
            'recommendations': []
        }
        
        # Check completeness (all 6 core indicators)
        available_indicators = len([k for k in self.core_indicators if k in indicators and indicators[k] is not None])
        validation['completeness_score'] = available_indicators / len(self.core_indicators)
        
        # Check timeliness (based on collection date)
        collection_date_str = region_data.get('collection_date')
        if collection_date_str:
            try:
                collection_date = datetime.fromisoformat(collection_date_str.replace('Z', '+00:00'))
                days_old = (datetime.now().replace(tzinfo=collection_date.tzinfo) - collection_date).days
                validation['timeliness_score'] = max(0, 1 - (days_old / 365))  # 1 year maximum
            except:
                validation['timeliness_score'] = 0.5  # Default if date parsing fails
        
        # Check consistency between related indicators
        consistency_checks = 0
        consistency_passes = 0
        
        # Poverty and PPI consistency
        if 'poverty_headcount_ratio' in indicators and 'ppi_score' in indicators:
            consistency_checks += 1
            poverty = indicators['poverty_headcount_ratio']
            ppi = indicators['ppi_score']
            # PPI should generally correlate with poverty rate
            if abs(poverty - ppi) < 0.3:  # Allow some variation
                consistency_passes += 1
        
        # Income and consumption consistency  
        if 'household_income_per_capita' in indicators and 'consumption_expenditure' in indicators:
            consistency_checks += 1
            income = indicators['household_income_per_capita']
            consumption = indicators['consumption_expenditure']
            # Consumption shouldn't exceed income by too much
            if consumption <= income * 1.5:  # Allow for savings/dissavings
                consistency_passes += 1
        
        if consistency_checks > 0:
            validation['consistency_score'] = consistency_passes / consistency_checks
        
        # Determine overall quality
        overall_score = (
            validation['completeness_score'] * 0.4 +
            validation['timeliness_score'] * 0.3 +
            validation['consistency_score'] * 0.3
        )
        
        if overall_score >= 0.9:
            validation['overall_quality'] = 'excellent'
        elif overall_score >= 0.7:
            validation['overall_quality'] = 'good'
        elif overall_score >= 0.5:
            validation['overall_quality'] = 'fair'
        else:
            validation['overall_quality'] = 'poor'
        
        # Generate recommendations
        if validation['completeness_score'] < 0.8:
            validation['recommendations'].append(
                "Collect additional socio-economic indicators for more accurate analysis"
            )
        
        if validation['timeliness_score'] < 0.7:
            validation['recommendations'].append(
                "Consider updating with more recent data for current conditions"
            )
        
        return validation

# Example usage
if __name__ == "__main__":
    # Initialize Data Bridge
    data_bridge = DataBridge()
    
    # Example region data
    sample_region = {
        'id': 'rural_region_001',
        'name': 'Rural Development Zone',
        'type': 'rural'
    }
    
    # Get socio-economic data
    socio_data = data_bridge.get_region_socioeconomic_data(sample_region)
    print("Socio-economic Data:")
    print(json.dumps(socio_data, indent=2))
    
    # Calculate equity score
    equity_score = data_bridge.calculate_equity_score(socio_data)
    print("\nEquity Assessment:")
    print(json.dumps(equity_score, indent=2))
    
    # Recommend funding allocation
    funding_rec = data_bridge.recommend_funding_allocation(socio_data)
    print("\nFunding Recommendation:")
    print(json.dumps(funding_rec, indent=2))
    
    # Validate data quality
    validation = data_bridge.validate_data_for_decision(socio_data)
    print("\nData Validation:")
    print(json.dumps(validation, indent=2))
