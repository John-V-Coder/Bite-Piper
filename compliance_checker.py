#!/usr/bin/env python3
"""
compliance_checker.py - BITE-PIPER Governance Compliance Checker

Verifies that the codebase follows BITE-PIPER policies and governance standards.
Run this script before commits to ensure compliance.
"""

import os
import sys
from pathlib import Path

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    """Print formatted header."""
    print(f"\n{BLUE}{'='*70}{RESET}")
    print(f"{BLUE}{text}{RESET}")
    print(f"{BLUE}{'='*70}{RESET}")

def print_check(passed, message):
    """Print check result."""
    status = f"{GREEN}✅ PASS{RESET}" if passed else f"{RED}❌ FAIL{RESET}"
    print(f"{status}: {message}")
    return passed

def check_file_exists(filepath, description):
    """Check if required file exists."""
    exists = Path(filepath).exists()
    return print_check(exists, f"{description}: {filepath}")

def check_file_content(filepath, required_strings, description):
    """Check if file contains required content."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        missing = [s for s in required_strings if s not in content]
        passed = len(missing) == 0
        
        if not passed:
            print_check(False, f"{description}: Missing {missing}")
        else:
            print_check(True, f"{description}")
        
        return passed
    except FileNotFoundError:
        return print_check(False, f"{description}: File not found")

def check_atom_structure():
    """Verify metta_atoms.py has correct structure."""
    required_classes = ['class Atom:', 'class Symbol:', 'class Variable:', 'class Expression:']
    required_atoms = ['NotReducible', 'Empty', 'TrueAtom', 'FalseAtom']
    
    all_required = required_classes + required_atoms
    return check_file_content(
        'src/metta_atoms.py',
        all_required,
        "metta_atoms.py structure (Atom classes)"
    )

def check_minimal_metta():
    """Verify metta_interpreter.py has core instructions."""
    required = ['def eval(', 'def chain(', 'def unify(', 'class MeTTaInterpreter:']
    return check_file_content(
        'src/metta_interpreter.py',
        required,
        "metta_interpreter.py (eval, chain, unify)"
    )

def check_data_types():
    """Verify socioeconomic_model.py has required indicators."""
    indicators = [
        'HouseholdIncomePerCapita',
        'PovertyRate',
        'WealthIndex',
        'PPI',
        'ConsumptionExpenditure',
        'LiteracyRate',
        'RegionData',
        'FundingPriority'
    ]
    return check_file_content(
        'src/socioeconomic_model.py',
        indicators,
        "socioeconomic_model.py (6 indicators + query symbols)"
    )

def check_bite_piper_main():
    """Verify application.py uses Minimal MeTTa."""
    required = [
        'class BitePiperApp:',
        'from metta_interpreter import MeTTaInterpreter',
        'def determine_priority(',
        'def _load_knowledge('
    ]
    return check_file_content(
        'src/application.py',
        required,
        "application.py (BitePiperApp with Minimal MeTTa)"
    )

def check_ses_agents():
    """Verify ses_agents.py has MeTTa-Motto integration."""
    required = [
        'from motto.agents import MettaAgent',
        'MOTTO_AVAILABLE',
        'def integrate_with_bite_piper(',
        'class SupplyChainNode:',
        'def arrow_fund_allocation('
    ]
    # Check original file (we can check both old and new)
    return check_file_content(
        'src/ses_agents.py',
        required,
        "ses_agents.py (MeTTa-Motto integration)"
    )

def check_requirements():
    """Verify requirements.txt has all dependencies."""
    required = ['python-dotenv', 'openai', 'hyperon']
    return check_file_content(
        'requirements.txt',
        required,
        "requirements.txt (all dependencies)"
    )

def check_config():
    """Verify config.py exists and has proper structure."""
    required = [
        'OPENAI_API_KEY',
        'DATA_SOURCES',
        'PRIORITY_WEIGHTS',
        'DATA_THRESHOLDS'
    ]
    return check_file_content(
        'config.py',
        required,
        "config.py (centralized configuration)"
    )

def check_documentation():
    """Verify documentation files exist."""
    checks = [
        check_file_exists('README.md', 'README.md'),
        check_file_exists('ARCHITECTURE.md', 'ARCHITECTURE.md'),
        check_file_exists('GOVERNANCE.md', 'GOVERNANCE.md')
    ]
    return all(checks)

def check_no_merge_conflicts():
    """Check for Git merge conflict markers."""
    conflict_markers = ['<<<<<<<', '>>>>>>>', '=======']
    files_to_check = [
        'README.md',
        'src/metta_atoms.py',
        'src/application.py',
        'src/ses_agents.py'
    ]
    
    all_clean = True
    for filepath in files_to_check:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            has_conflict = any(marker in content for marker in conflict_markers)
            if has_conflict:
                print_check(False, f"Merge conflict detected in {filepath}")
                all_clean = False
        except FileNotFoundError:
            pass
    
    if all_clean:
        print_check(True, "No merge conflicts detected")
    
    return all_clean

def check_api_key_security():
    """Verify API keys are not hardcoded."""
    files_to_check = [
        'src/application.py',
        'src/ses_agents.py',
        'config.py'
    ]
    
    all_secure = True
    for filepath in files_to_check:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for common API key patterns
            dangerous_patterns = [
                'api_key = "sk-',
                'OPENAI_API_KEY = "sk-',
                'api_key = \'sk-'
            ]
            
            for pattern in dangerous_patterns:
                if pattern in content:
                    print_check(False, f"Hardcoded API key detected in {filepath}")
                    all_secure = False
        except FileNotFoundError:
            pass
    
    if all_secure:
        print_check(True, "No hardcoded API keys detected")
    
    return all_secure

def main():
    """Run all compliance checks."""
    print_header("BITE-PIPER Governance Compliance Verification")
    
    results = []
    
    # Core file structure
    print_header("1. Core File Structure (New Names)")
    results.append(check_file_exists('src/metta_atoms.py', 'metta_atoms.py'))
    results.append(check_file_exists('src/knowledge_base.py', 'knowledge_base.py'))
    results.append(check_file_exists('src/metta_interpreter.py', 'metta_interpreter.py'))
    results.append(check_file_exists('src/socioeconomic_model.py', 'socioeconomic_model.py'))
    results.append(check_file_exists('src/application.py', 'application.py'))
    
    # Content verification
    print_header("2. Code Structure Compliance")
    results.append(check_atom_structure())
    results.append(check_minimal_metta())
    results.append(check_data_types())
    results.append(check_bite_piper_main())
    results.append(check_ses_agents())
    
    # Dependencies
    print_header("3. Dependencies & Configuration")
    results.append(check_requirements())
    results.append(check_config())
    
    # Documentation
    print_header("4. Documentation")
    results.append(check_documentation())
    
    # Code quality
    print_header("5. Code Quality & Security")
    results.append(check_no_merge_conflicts())
    results.append(check_api_key_security())
    
    # Summary
    print_header("Compliance Summary")
    passed = sum(results)
    total = len(results)
    percentage = (passed / total) * 100 if total > 0 else 0
    
    print(f"\nTotal Checks: {total}")
    print(f"Passed: {GREEN}{passed}{RESET}")
    print(f"Failed: {RED}{total - passed}{RESET}")
    print(f"Compliance Rate: {GREEN if percentage == 100 else YELLOW}{percentage:.1f}%{RESET}")
    
    if percentage == 100:
        print(f"\n{GREEN}🎉 All compliance checks passed! Code is policy-compliant.{RESET}")
        return 0
    else:
        print(f"\n{YELLOW}⚠️  Some checks failed. Please review and fix before committing.{RESET}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
