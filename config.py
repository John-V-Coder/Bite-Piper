#!/usr/bin/env python3
"""
Configuration file for Bite-Piper
Centralized settings and parameters for the application
"""

import os
from pathlib import Path

# Try to load from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    ENV_LOADED = True
except ImportError:
    ENV_LOADED = False
    print("Warning: python-dotenv not installed. Using environment variables only.")

# ============================================================
# API KEYS & CREDENTIALS
# ============================================================

# OpenAI API (for ChatGPT integration)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o')
OPENAI_MAX_TOKENS = int(os.getenv('OPENAI_MAX_TOKENS', '4000'))
OPENAI_TEMPERATURE = float(os.getenv('OPENAI_TEMPERATURE', '0.7'))

# Anthropic API (optional - for Claude)
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')
ANTHROPIC_MODEL = os.getenv('ANTHROPIC_MODEL', 'claude-3-sonnet-20240229')

# External Data APIs (optional)
WORLD_BANK_API_KEY = os.getenv('WORLD_BANK_API_KEY', '')
UN_DATA_API_KEY = os.getenv('UN_DATA_API_KEY', '')

# ============================================================
# APPLICATION SETTINGS
# ============================================================

APP_NAME = "Bite-Piper"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Socio-Economic Data Analysis System using Minimal MeTTa"

# ============================================================
# MINIMAL METTA INTERPRETER SETTINGS
# ============================================================

# Interpreter mode: 'bare-minimal' or 'standard'
INTERPRETER_MODE = "standard"

# Enable debug mode for verbose logging
DEBUG_MODE = False

# Maximum recursion depth for chain operations
MAX_CHAIN_DEPTH = 100

# ============================================================
# DATA SETTINGS
# ============================================================

# Default data sources (can be extended with file paths, DB connections, etc.)
DATA_SOURCES = {
    "regions": ["RegionA", "RegionB"],
    "metrics": [
        "HouseholdIncomePerCapita",  # Income per household member
        "PovertyRate",                # % below poverty line
        "WealthIndex",                # IWI (0-100)
        "PPI",                        # Progress out of Poverty Index
        "ConsumptionExpenditure",     # Household spending
        "LiteracyRate"                # Education metric
    ]
}

# Data validation thresholds
DATA_THRESHOLDS = {
    "HouseholdIncomePerCapita": {"min": 0, "max": 100000},  # In currency units
    "PovertyRate": {"min": 0, "max": 100},                  # Percentage
    "WealthIndex": {"min": 0, "max": 100},                  # IWI score (0-100)
    "PPI": {"min": 0, "max": 100},                          # Probability (0-100)
    "ConsumptionExpenditure": {"min": 0, "max": 100000},    # In currency units
    "LiteracyRate": {"min": 0, "max": 100}                  # Percentage
}

# ============================================================
# ANALYSIS SETTINGS
# ============================================================

# Priority calculation weights (for future extensions)
PRIORITY_WEIGHTS = {
    "HouseholdIncomePerCapita": 0.15,  # 15% - Income level
    "PovertyRate": 0.25,                # 25% - Poverty headcount
    "WealthIndex": 0.20,                # 20% - Asset-based wealth
    "PPI": 0.15,                        # 15% - Poverty probability
    "ConsumptionExpenditure": 0.10,     # 10% - Spending capacity
    "LiteracyRate": 0.15                # 15% - Education level
}

# Funding priority levels
PRIORITY_LEVELS = {
    "CRITICAL": {"poverty_threshold": 70, "literacy_threshold": 40},
    "HIGH": {"poverty_threshold": 50, "literacy_threshold": 60},
    "MEDIUM": {"poverty_threshold": 30, "literacy_threshold": 70},
    "LOW": {"poverty_threshold": 0, "literacy_threshold": 80}
}

# ============================================================
# OUTPUT SETTINGS
# ============================================================

# Enable colored output in terminal (if supported)
ENABLE_COLORS = True

# Output format: 'text', 'json', 'csv'
OUTPUT_FORMAT = "text"

# Verbosity level: 'quiet', 'normal', 'verbose'
VERBOSITY = "normal"

# ============================================================
# ATOMSPACE SETTINGS
# ============================================================

# Initial AtomSpace capacity (for optimization in future versions)
INITIAL_ATOMSPACE_SIZE = 100

# Enable caching for frequent queries
ENABLE_QUERY_CACHE = False

# ============================================================
# ERROR HANDLING
# ============================================================

# Error handling strategy: 'strict', 'permissive'
ERROR_STRATEGY = "permissive"

# Enable error logging to file
LOG_ERRORS = False
ERROR_LOG_PATH = "logs/errors.log"

# ============================================================
# EXTENSION SETTINGS (for future development)
# ============================================================

# Enable REST API
ENABLE_API = False
API_HOST = "localhost"
API_PORT = 5000

# Enable database persistence
ENABLE_DB = False
DB_PATH = "data/bite_piper.db"

# Enable external data import
ENABLE_DATA_IMPORT = False
DATA_IMPORT_FORMATS = ["csv", "json", "xml"]

# ============================================================
# TESTING SETTINGS
# ============================================================

# Enable self-tests on startup
RUN_SELF_TESTS = True

# Test data path
TEST_DATA_PATH = "tests/data/"

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_config(key, default=None):
    """
    Get configuration value by key
    
    Args:
        key: Configuration key (e.g., 'APP_NAME')
        default: Default value if key not found
    
    Returns:
        Configuration value or default
    """
    return globals().get(key, default)


def update_config(key, value):
    """
    Update configuration value
    
    Args:
        key: Configuration key
        value: New value
    """
    globals()[key] = value


def print_config():
    """Print all configuration settings"""
    print("=" * 60)
    print(f"{APP_NAME} Configuration (v{APP_VERSION})")
    print("=" * 60)
    
    sections = [
        ("APPLICATION SETTINGS", ["APP_NAME", "APP_VERSION", "APP_DESCRIPTION"]),
        ("INTERPRETER SETTINGS", ["INTERPRETER_MODE", "DEBUG_MODE", "MAX_CHAIN_DEPTH"]),
        ("DATA SETTINGS", ["DATA_SOURCES", "DATA_THRESHOLDS"]),
        ("OUTPUT SETTINGS", ["OUTPUT_FORMAT", "VERBOSITY", "ENABLE_COLORS"]),
        ("ERROR HANDLING", ["ERROR_STRATEGY", "LOG_ERRORS"])
    ]
    
    for section_name, keys in sections:
        print(f"\n{section_name}:")
        for key in keys:
            value = globals().get(key)
            print(f"  {key}: {value}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    print_config()
