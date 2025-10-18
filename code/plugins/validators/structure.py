"""
Generic structure validators for skill specs.
"""
from typing import Dict, List, Any


def validate_structure(spec: Dict[str, Any]) -> List[str]:
    """
    Validate basic structural requirements.
    """
    errors = []
    
    # Check name format
    name = spec.get("name", "")
    if len(name) > 100:
        errors.append("Name should be 100 characters or less")
    
    # Check purpose brevity
    purpose = spec.get("purpose", "")
    if len(purpose) > 500:
        errors.append("Purpose should be 500 characters or less (keep it concise)")
    
    return errors


def validate_triggers(spec: Dict[str, Any]) -> List[str]:
    """
    Validate trigger phrases are reasonable.
    """
    errors = []
    triggers = spec.get("triggers", [])
    
    for i, trigger in enumerate(triggers):
        if len(trigger) > 200:
            errors.append(f"Trigger {i+1} is too long (keep under 200 characters)")
        if len(trigger.strip()) == 0:
            errors.append(f"Trigger {i+1} is empty")
    
    return errors
