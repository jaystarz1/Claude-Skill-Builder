"""
Skill spec validation module.
Checks structural integrity and Claude Skills best practices.
"""
import json
from pathlib import Path
from typing import List, Dict, Any
from .schema import validate_best_practices


def validate_spec(spec_path: str) -> List[str]:
    """
    Validate a skill spec file.
    Returns list of error messages (empty if valid).
    Prints warnings for best practice suggestions.
    """
    errors = []
    
    try:
        with open(spec_path, 'r') as f:
            spec = json.load(f)
    except FileNotFoundError:
        return [f"Spec file not found: {spec_path}"]
    except json.JSONDecodeError as e:
        return [f"Invalid JSON: {e}"]
    
    # Required top-level fields (updated to match Claude requirements)
    required_fields = ["name", "description", "triggers", "inputs", "guardrails", "procedure", "output_contract"]
    for field in required_fields:
        if field not in spec:
            errors.append(f"Missing required field: {field}")
    
    # Name validation (Claude limit: 64 chars)
    name = spec.get("name", "")
    if not name:
        errors.append("Field 'name' cannot be empty")
    elif len(name) > 64:
        errors.append(f"Field 'name' must be 64 characters or less (currently {len(name)})")
    
    # Description validation (Claude limit: 1024 chars)
    description = spec.get("description", "")
    if not description:
        errors.append("Field 'description' cannot be empty")
    elif len(description) > 1024:
        errors.append(f"Field 'description' must be 1024 characters or less (currently {len(description)})")
    
    # Triggers validation
    triggers = spec.get("triggers", [])
    if not isinstance(triggers, list):
        errors.append("Field 'triggers' must be an array")
    elif len(triggers) < 2:
        errors.append("Field 'triggers' must have at least 2 items")
    
    # Inputs validation
    inputs = spec.get("inputs", [])
    if not isinstance(inputs, list):
        errors.append("Field 'inputs' must be an array")
    elif len(inputs) == 0:
        errors.append("Field 'inputs' must have at least 1 item")
    
    # Guardrails validation
    guardrails = spec.get("guardrails", [])
    if not isinstance(guardrails, list):
        errors.append("Field 'guardrails' must be an array")
    elif len(guardrails) == 0:
        errors.append("Field 'guardrails' must have at least 1 item")
    
    # Procedure validation
    procedure = spec.get("procedure", [])
    if not isinstance(procedure, list):
        errors.append("Field 'procedure' must be an array")
    elif len(procedure) == 0:
        errors.append("Field 'procedure' must have at least 1 item")
    
    # Output contract validation
    output_contract = spec.get("output_contract", {})
    if not isinstance(output_contract, dict):
        errors.append("Field 'output_contract' must be an object")
    else:
        if not output_contract.get("title"):
            errors.append("output_contract.title is required and cannot be empty")
        
        sections = output_contract.get("sections", [])
        if not isinstance(sections, list):
            errors.append("output_contract.sections must be an array")
        elif len(sections) == 0:
            errors.append("output_contract.sections must have at least 1 item")
        else:
            # Check section uniqueness
            headings = [s.get("heading") for s in sections if isinstance(s, dict)]
            if len(headings) != len(set(headings)):
                errors.append("Section headings must be unique")
            
            # Validate each section
            for i, section in enumerate(sections):
                if not isinstance(section, dict):
                    errors.append(f"Section {i} must be an object")
                    continue
                if not section.get("heading"):
                    errors.append(f"Section {i} missing 'heading'")
                if "required" not in section:
                    errors.append(f"Section {i} missing 'required' field")
        
        # Tables validation (optional)
        tables = output_contract.get("tables", [])
        if tables and isinstance(tables, list):
            for i, table in enumerate(tables):
                if not isinstance(table, dict):
                    errors.append(f"Table {i} must be an object")
                    continue
                columns = table.get("columns", [])
                if not columns or len(columns) == 0:
                    errors.append(f"Table {i} must have at least 1 column")
                elif len(columns) != len(set(columns)):
                    errors.append(f"Table {i} has duplicate column names")
    
    # Code helper validation (optional)
    if "code_helper" in spec:
        code_helper = spec["code_helper"]
        if not isinstance(code_helper, dict):
            errors.append("Field 'code_helper' must be an object")
    
    # MCP tools validation (optional)
    mcp_tools = spec.get("mcp_tools", [])
    if mcp_tools:
        if not isinstance(mcp_tools, list):
            errors.append("Field 'mcp_tools' must be an array")
        else:
            for i, tool in enumerate(mcp_tools):
                if not isinstance(tool, str):
                    errors.append(f"mcp_tools[{i}] must be a string")
                elif ":" not in tool:
                    errors.append(
                        f"mcp_tools[{i}] must use format 'ServerName:tool_name', got: {tool}"
                    )
    
    # Reference files validation (optional)
    ref_files = spec.get("reference_files", [])
    if ref_files:
        if not isinstance(ref_files, list):
            errors.append("Field 'reference_files' must be an array")
        else:
            for i, ref in enumerate(ref_files):
                if not isinstance(ref, dict):
                    errors.append(f"reference_files[{i}] must be an object")
                elif "\\" in ref.get("path", ""):
                    errors.append(
                        f"reference_files[{i}].path must use forward slashes, not backslashes"
                    )
    
    # If no structural errors, check best practices
    if not errors:
        print("\n✓ Spec structure is valid!")
        print("\nChecking best practices...\n")
        warnings = validate_best_practices(spec)
        if warnings:
            print("⚠️  Best Practice Suggestions:")
            for warning in warnings:
                print(f"  {warning}")
            print("\nNote: These are suggestions, not errors. The spec is valid.")
        else:
            print("✓ No best practice issues found!")
    
    return errors


def validate_rendered_template(template_content: str, spec: Dict[str, Any]) -> List[str]:
    """
    Check if a rendered template is valid (basic checks).
    Returns list of warnings/errors.
    """
    errors = []
    
    # Check for unresolved template variables (simple check)
    if "{{" in template_content or "{%" in template_content:
        errors.append("Template contains unresolved placeholders")
    
    # Check SKILL.md length recommendation
    line_count = len(template_content.split('\n'))
    if line_count > 500:
        errors.append(
            f"SKILL.md is {line_count} lines (recommended: under 500). "
            "Consider using progressive disclosure to split content into reference files."
        )
    
    return errors
