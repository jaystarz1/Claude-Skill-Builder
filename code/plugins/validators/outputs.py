"""
Output contract validators.
"""
from typing import Dict, List, Any


def validate_outputs(spec: Dict[str, Any]) -> List[str]:
    """
    Validate output contract makes sense.
    """
    errors = []
    
    output_contract = spec.get("output_contract", {})
    sections = output_contract.get("sections", [])
    
    # Check for overly long section names
    for i, section in enumerate(sections):
        heading = section.get("heading", "")
        if len(heading) > 100:
            errors.append(f"Section {i+1} heading is too long (keep under 100 characters)")
    
    # Warn about too many sections
    if len(sections) > 20:
        errors.append("Output contract has many sections - consider grouping related content")
    
    return errors
