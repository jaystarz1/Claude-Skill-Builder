"""
Custom validator registry (empty by default).
Users can add domain-specific validators here.
"""
from typing import Dict, List, Any, Callable

# Registry of custom validators
CUSTOM_VALIDATORS: Dict[str, Callable] = {}


def register_validator(name: str, func: Callable[[Dict[str, Any]], List[str]]):
    """
    Register a custom validator function.
    
    Args:
        name: Validator name
        func: Function that takes a spec dict and returns list of error messages
    """
    CUSTOM_VALIDATORS[name] = func


def run_custom_validators(spec: Dict[str, Any]) -> List[str]:
    """Run all registered custom validators on a spec."""
    errors = []
    for name, validator in CUSTOM_VALIDATORS.items():
        try:
            validator_errors = validator(spec)
            errors.extend(validator_errors)
        except Exception as e:
            errors.append(f"Custom validator '{name}' failed: {e}")
    return errors
