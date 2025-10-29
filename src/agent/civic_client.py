# Civic data API client

"""
Civic Data API Client - Standalone implementation for Bite-Piper
Integrated data sources for socio-economic indicators, governance data, and equity metrics
"""

import datetime as dt
import logging
from typing import Any, Dict, List, Optional, Tuple, Union
import requests
import json
from urllib.parse import urlencode

logger = logging.getLogger(__name__)

VERSION = "bite-piper-civic-1.0"


class CivicDataException(Exception):
    """Civic Data API Exception"""
    pass


class BaseCivicApi:
    """Base API client for civic data sources"""
    
    TIMEOUT_SECS = 90  # Longer timeout for government data sources
    
    USER_AGENT_STRING = f"bite-piper-civic {VERSION}"
    
    def __init__(self, api_keys: Optional[Dict[str, str]] = None):
        self._api_keys = api_keys or {}
        
        self._session = requests.Session()
        self._session.headers.update({
            'Accept': 'application/json',
            'User-Agent': self.USER_AGENT_STRING,
            'Content-Type': 'application/json'
        })
    
    def _query(self, url: str, params: Optional[Dict] = None, method: str = 'GET', 
               headers: Optional[Dict] = None, api_key_name: Optional[str] = None) -> Dict:
        """
        Centralize making the actual queries for easy maintenance and testing
        """
        try:
            # Add API key if specified
            request_headers = self._session.headers.copy()
            if headers:
                request_headers.update(headers)
            
            if api_key_name and api_key_name in self._api_keys:
                # Different APIs use different authentication methods
                if 'worldbank' in api_key_name:
                    params = params or {}
                    params['format'] = 'json'
                elif 'census' in api_key_name:
                    params = params or {}
                    params['key'] = self._api_keys[api_key_name]
            
            if method == 'GET':
                r = self._session.get(url, params=params, headers=request_headers, timeout=self.TIMEOUT_SECS)
            elif method == 'POST':
                r = self._session.post(url, json=params, headers=request_headers, timeout=self.TIMEOUT_SECS)
            else:
                raise RuntimeError(f"Unsupported method: '{method}'")
            
            if r.status_code == 401:
                logger.warning(f"API authentication required: {url}")
                raise CivicDataException(f"Authentication required for {url}")
            elif r.status_code == 403:
                logger.warning(f"API access forbidden: {url}")
                raise CivicDataException(f"Access forbidden for {url}")
            elif r.status_code == 404:
                logger.warning(f"API endpoint not found: {url}")
                raise CivicDataException(f"Endpoint not found: {url}")
            elif r.status_code == 429:
                logger.warning(f"API rate limit exceeded: {url}")
                raise CivicDataException(f"Rate limit exceeded for {url}")
            elif r.status_code != 200:
                logger.error(f"API Error {r.status_code} for: {url}")
                raise CivicDataException(f"API Error {r.status_code} for {url}")
            
            return r.json()
            
        except requests.exceptions.Timeout:
            logger.error(f"API request timeout: {url}")
            raise CivicDataException(f"Request timeout for {url}")
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {url}: {e}")
            raise CivicDataException(f"Request failed: {e}")
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error for: {url}: {e}")
            raise CivicDataException(f"Invalid JSON response from {url}")


class WorldBankApi(BaseCivicApi):
    """API client for World Bank Development Indicators"""
    
    BASE_URL = "https://api.worldbank.org/v2"
    
    # Core socio-economic indicators for Bite-Piper
    CORE_INDICATORS = {
        "household_income": "NY.ADJ.NNTY.PC.CD",  # Adjusted net national income per capita
        "poverty_headcount": "SI.POV.DDAY",       # Poverty headcount ratio
        "gini_index": "SI.POV.GINI",              # Gini coefficient
        "wealth_index": "NY.ADJ.SVNX.GN.ZS",     # Adjusted savings: net national savings
        "education_expenditure": "SE.XPD.TOTL.GD.ZS",  # Government expenditure on education
        "health_expenditure": "SH.XPD.CHEX.GD.ZS",     # Current health expenditure
        "literacy_rate": "SE.ADT.LITR.ZS",             # Literacy rate
        "unemployment": "SL.UEM.TOTL.ZS",              # Unemployment rate
        "electricity_access": "EG.ELC.ACCS.ZS",        # Access to electricity
        "sanitation_access": "SH.STA.ACSN",            # People using basic sanitation services
    }
    
    def get_country_indicators(self, country_code: str, indicators: List[str], 
                              year: Optional[int] = None, 
                              start_year: Optional[int] = None,
                              end_year: Optional[int] = None) -> List[Dict]:
        """Get development indicators for a specific country"""
        
        # Use core indicators if specific ones not provided
        if not indicators:
            indicators = list(self.CORE_INDICATORS.values())
        else:
            # Map indicator names to codes
            indicator_codes = []
            for indicator in indicators:
                if indicator in self.CORE_INDICATORS:
                    indicator_codes.append(self.CORE_INDICATORS[indicator])
                else:
                    indicator_codes.append(indicator)
            indicators = indicator_codes
        
        params = {
            'country': country_code,
            'indicator': ';'.join(indicators),
            'format': 'json',
            'per_page': 1000
        }
        
        if year:
            params['date'] = str(year)
        elif start_year and end_year:
            params['date'] = f"{start_year}:{end_year}"
        
        url = f"{self.BASE_URL}/country/{country_code}/indicator/"
        results = self._query(url, params, api_key_name='worldbank')
        
        # Process the nested World Bank API response
        processed_data = []
        if isinstance(results, list) and len(results) > 1:
            for item in results[1]:
                if item.get('value') is not None:
                    processed_data.append({
                        'country': item['countryiso3code'],
                        'indicator': item['indicator']['id'],
                        'indicator_name': item['indicator']['value'],
                        'year': int(item['date']),
                        'value': item['value'],
                        'unit': item.get('unit', ''),
                        'country_name': item['country']['value']
                    })
        
        return processed_data
    
    def get_region_data(self, region_code: str, indicators: List[str], 
                       year: Optional[int] = None) -> List[Dict]:
        """Get development indicators for a specific region"""
        params = {
            'region': region_code,
            'indicator': ';'.join(indicators),
            'format': 'json',
            'per_page': 1000
        }
        
        if year:
            params['date'] = str(year)
        
        url = f"{self.BASE_URL}/region/{region_code}/indicator/"
        return self._query(url, params, api_key_name='worldbank')
    
    def search_indicators(self, query: str) -> List[Dict]:
        """Search for development indicators by keyword"""
        params = {
            'q': query,
            'format': 'json',
            'per_page': 50
        }
        
        url = f"{self.BASE_URL}/indicator"
        results = self._query(url, params, api_key_name='worldbank')
        
        if isinstance(results, list) and len(results) > 1:
            return results[1]
        return []


class CensusApi(BaseCivicApi):
    """API client for US Census Bureau data"""
    
    BASE_URL = "https://api.census.gov/data"
    
    def get_acs_data(self, variables: List[str], geography: str, 
                    year: int = 2022, dataset: str = "acs/acs5") -> List[Dict]:
        """Get American Community Survey data"""
        
        params = {
            'get': ','.join(variables),
            'for': geography,
            'key': self._api_keys.get('census', '')
        }
        
        url = f"{self.BASE_URL}/{year}/{dataset}"
        results = self._query(url, params, api_key_name='census')
        
        # Convert Census API matrix format to list of dicts
        if results and len(results) > 1:
            headers = results[0]
            data = []
            for row in results[1:]:
                item = {}
                for i, header in enumerate(headers):
                    item[header] = row[i]
                data.append(item)
            return data
        
        return []
    
    def get_poverty_data(self, geography: str, year: int = 2022) -> List[Dict]:
        """Get poverty statistics for geographic areas"""
        poverty_variables = [
            'B17001_001E',  # Poverty status in past 12 months
            'B17001_002E',  # Income in past 12 months below poverty level
            'B17001_031E',  # Income in past 12 months at or above poverty level
        ]
        
        return self.get_acs_data(poverty_variables, geography, year)
    
    def get_income_data(self, geography: str, year: int = 2022) -> List[Dict]:
        """Get income distribution data"""
        income_variables = [
            'B19013_001E',  # Median household income
            'B19001_001E',  # Household income distribution
            'B19301_001E',  # Per capita income
        ]
        
        return self.get_acs_data(income_variables, geography, year)


class OpenGovernmentApi(BaseCivicApi):
    """API client for open government data portals"""
    
    def get_ckan_datasets(self, portal_url: str, query: str = "", 
                         organization: str = "", limit: int = 100) -> List[Dict]:
        """Search datasets from CKAN-based open data portals"""
        
        params = {
            'q': query,
            'rows': limit
        }
        
        if organization:
            params['organization'] = organization
        
        url = f"{portal_url.rstrip('/')}/api/3/action/package_search"
        results = self._query(url, params)
        
        if results.get('success'):
            return results['result'].get('results', [])
        return []
    
    def get_dataset_resources(self, portal_url: str, dataset_id: str) -> List[Dict]:
        """Get resources for a specific dataset"""
        url = f"{portal_url.rstrip('/')}/api/3/action/package_show"
        params = {'id': dataset_id}
        
        results = self._query(url, params)
        if results.get('success'):
            return results['result'].get('resources', [])
        return []


class EquityDataApi(BaseCivicApi):
    """API client for equity and social justice data sources"""
    
    def get_opportunity_atlas(self, geography_type: str = "tract") -> List[Dict]:
        """Get data from Opportunity Atlas on economic mobility"""
        # This would integrate with Opportunity Atlas API
        # Placeholder implementation
        return []
    
    def get_environmental_justice(self, latitude: float, longitude: float, 
                                radius_km: int = 10) -> Dict:
        """Get environmental justice data for a location"""
        # This would integrate with EPA EJSCREEN or similar APIs
        # Placeholder implementation
        return {}


class CivicDataClient:
    """Main client for accessing all civic data sources with unified interface"""
    
    def __init__(self, api_keys: Optional[Dict[str, str]] = None):
        self.api_keys = api_keys or {}
        
        # Initialize API clients
        self.worldbank = WorldBankApi(api_keys)
        self.census = CensusApi(api_keys)
        self.opengov = OpenGovernmentApi(api_keys)
        self.equity = EquityDataApi(api_keys)
        
        # Cache for frequently accessed data
        self._cache = {}
        self._cache_ttl = 3600  # 1 hour cache
        
    def get_socioeconomic_profile(self, location: Dict, indicators: List[str] = None) -> Dict:
        """
        Get comprehensive socio-economic profile for a location
        location: {'type': 'country|region|county|tract', 'code': 'USA|NY|36061...'}
        """
        cache_key = f"profile_{location['type']}_{location['code']}"
        if cache_key in self._cache:
            cached_data, timestamp = self._cache[cache_key]
            if (dt.datetime.now() - timestamp).seconds < self._cache_ttl:
                return cached_data
        
        profile = {
            'location': location,
            'indicators': {},
            'timestamp': dt.datetime.now().isoformat(),
            'data_sources': []
        }
        
        try:
            if location['type'] in ['country', 'region']:
                # Use World Bank data for countries and regions
                if not indicators:
                    indicators = ['household_income', 'poverty_headcount', 'wealth_index', 
                                 'education_expenditure', 'literacy_rate']
                
                data = self.worldbank.get_country_indicators(
                    location['code'], indicators, year=2023
                )
                
                # Process World Bank data
                for item in data:
                    indicator_key = item['indicator']
                    if indicator_key not in profile['indicators']:
                        profile['indicators'][indicator_key] = []
                    profile['indicators'][indicator_key].append({
                        'year': item['year'],
                        'value': item['value'],
                        'source': 'worldbank'
                    })
                
                profile['data_sources'].append('World Bank')
                
            elif location['type'] in ['county', 'tract', 'state']:
                # Use Census data for US geographic areas
                if not indicators:
                    indicators = ['poverty', 'income']
                
                if 'poverty' in indicators:
                    poverty_data = self.census.get_poverty_data(location['code'])
                    profile['indicators']['poverty'] = poverty_data
                
                if 'income' in indicators:
                    income_data = self.census.get_income_data(location['code'])
                    profile['indicators']['income'] = income_data
                
                profile['data_sources'].append('US Census Bureau')
            
            # Cache the results
            self._cache[cache_key] = (profile, dt.datetime.now())
            
        except CivicDataException as e:
            logger.error(f"Error getting socio-economic profile for {location}: {e}")
            profile['error'] = str(e)
        
        return profile
    
    def calculate_equity_scores(self, location: Dict, reference_locations: List[Dict] = None) -> Dict:
        """Calculate equity scores based on socio-economic indicators"""
        
        profile = self.get_socioeconomic_profile(location)
        
        if 'error' in profile:
            return {'error': profile['error']}
        
        scores = {
            'location': location,
            'composite_equity_score': 0.0,
            'dimension_scores': {},
            'benchmark_comparison': {},
            'priority_level': 'unknown'
        }
        
        # Calculate dimension scores
        indicators = profile['indicators']
        
        # Poverty dimension (inverse - lower poverty = higher score)
        if 'SI.POV.DDAY' in indicators:
            poverty_data = indicators['SI.POV.DDAY']
            if poverty_data:
                poverty_rate = poverty_data[0]['value']
                scores['dimension_scores']['poverty'] = max(0, 1 - (poverty_rate / 100))
        
        # Income dimension
        if 'NY.ADJ.NNTY.PC.CD' in indicators:
            income_data = indicators['NY.ADJ.NNTY.PC.CD']
            if income_data:
                income = income_data[0]['value'] or 0
                # Normalize income score (cap at $50,000 for scoring)
                scores['dimension_scores']['income'] = min(1.0, income / 50000)
        
        # Education dimension
        if 'SE.ADT.LITR.ZS' in indicators:
            literacy_data = indicators['SE.ADT.LITR.ZS']
            if literacy_data:
                literacy_rate = literacy_data[0]['value'] or 0
                scores['dimension_scores']['education'] = literacy_rate / 100
        
        # Calculate composite score (weighted average)
        dimension_weights = {
            'poverty': 0.4,
            'income': 0.3,
            'education': 0.3
        }
        
        composite_score = 0.0
        total_weight = 0.0
        
        for dimension, weight in dimension_weights.items():
            if dimension in scores['dimension_scores']:
                composite_score += scores['dimension_scores'][dimension] * weight
                total_weight += weight
        
        if total_weight > 0:
            scores['composite_equity_score'] = composite_score / total_weight
        
        # Determine priority level based on composite score
        if scores['composite_equity_score'] < 0.3:
            scores['priority_level'] = 'critical'
        elif scores['composite_equity_score'] < 0.5:
            scores['priority_level'] = 'high'
        elif scores['composite_equity_score'] < 0.7:
            scores['priority_level'] = 'medium'
        else:
            scores['priority_level'] = 'low'
        
        return scores
    
    def compare_regions(self, regions: List[Dict], indicators: List[str] = None) -> Dict:
        """Compare multiple regions across socio-economic indicators"""
        
        comparison = {
            'regions': [],
            'comparison_metrics': {},
            'equity_disparities': [],
            'timestamp': dt.datetime.now().isoformat()
        }
        
        for region in regions:
            profile = self.get_socioeconomic_profile(region, indicators)
            equity_scores = self.calculate_equity_scores(region)
            
            region_data = {
                'region': region,
                'profile': profile,
                'equity_scores': equity_scores
            }
            
            comparison['regions'].append(region_data)
        
        # Calculate disparities
        if len(comparison['regions']) >= 2:
            equity_scores = [r['equity_scores']['composite_equity_score'] 
                           for r in comparison['regions']]
            max_score = max(equity_scores)
            min_score = min(equity_scores)
            
            disparity_ratio = max_score / min_score if min_score > 0 else float('inf')
            comparison['equity_disparities'].append({
                'disparity_ratio': disparity_ratio,
                'max_min_difference': max_score - min_score
            })
        
        return comparison
    
    def validate_data_quality(self, location: Dict) -> Dict:
        """Validate data quality and completeness for decision-making"""
        
        profile = self.get_socioeconomic_profile(location)
        
        validation = {
            'location': location,
            'completeness_score': 0.0,
            'timeliness_score': 0.0,
            'source_reliability': 'unknown',
            'validation_errors': [],
            'recommendations': []
        }
        
        # Check completeness (all 6 core indicators for Bite-Piper)
        core_indicators = [
            'household_income', 'poverty_headcount', 'wealth_index',
            'education_expenditure', 'literacy_rate', 'unemployment'
        ]
        
        available_indicators = len(profile['indicators'])
        total_indicators = len(core_indicators)
        
        validation['completeness_score'] = available_indicators / total_indicators
        
        # Check timeliness (data should be within 3 years)
        current_year = dt.datetime.now().year
        for indicator_data in profile['indicators'].values():
            if indicator_data:
                latest_year = max([item['year'] for item in indicator_data])
                if current_year - latest_year <= 3:
                    validation['timeliness_score'] += 1
        
        if profile['indicators']:
            validation['timeliness_score'] /= len(profile['indicators'])
        
        # Generate recommendations
        if validation['completeness_score'] < 0.8:
            validation['recommendations'].append(
                "Collect additional socio-economic indicators for comprehensive analysis"
            )
        
        if validation['timeliness_score'] < 0.8:
            validation['recommendations'].append(
                "Seek more recent data sources for accurate decision-making"
            )
        
        # Determine overall data quality
        overall_score = (validation['completeness_score'] + validation['timeliness_score']) / 2
        if overall_score >= 0.9:
            validation['source_reliability'] = 'excellent'
        elif overall_score >= 0.7:
            validation['source_reliability'] = 'good'
        elif overall_score >= 0.5:
            validation['source_reliability'] = 'fair'
        else:
            validation['source_reliability'] = 'poor'
        
        return validation


# Factory functions for easy client creation
def create_civic_client(api_keys: Optional[Dict[str, str]] = None) -> CivicDataClient:
    """Create a CivicDataClient instance with optional API keys"""
    return CivicDataClient(api_keys)


def create_worldbank_client(api_keys: Optional[Dict[str, str]] = None) -> WorldBankApi:
    """Create a WorldBankApi instance"""
    return WorldBankApi(api_keys)


def create_census_client(api_keys: Optional[Dict[str, str]] = None) -> CensusApi:
    """Create a CensusApi instance (requires Census API key)"""
    return CensusApi(api_keys)


# Example usage
if __name__ == "__main__":
    # Example API keys (should be stored in environment variables in production)
    api_keys = {
        'census': 'YOUR_CENSUS_API_KEY',
        'worldbank': 'OPTIONAL_WORLDBANK_KEY'
    }
    
    client = create_civic_client(api_keys)
    
    # Get socio-economic profile for a country
    profile = client.get_socioeconomic_profile({
        'type': 'country',
        'code': 'USA'
    })
    
    print("Socio-economic Profile:")
    print(json.dumps(profile, indent=2))
    
    # Calculate equity scores
    scores = client.calculate_equity_scores({
        'type': 'country', 
        'code': 'USA'
    })
    
    print("\nEquity Scores:")
    print(json.dumps(scores, indent=2))
    
    # Validate data quality
    validation = client.validate_data_quality({
        'type': 'country',
        'code': 'USA'
    })
    
    print("\nData Quality Validation:")
    print(json.dumps(validation, indent=2))