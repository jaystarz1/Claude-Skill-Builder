"""
JSON Schema for Claude Skills - Master Schema
Comprehensive validation for world-class Skills that work across all platforms.
"""

SKILL_SPEC_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "title": "Claude Skill Specification",
    "description": "Complete specification for creating Skills that work on claude.ai, Claude Code, and API",
    "required": ["name", "description", "triggers", "inputs", "guardrails", "procedure", "output_contract"],
    "properties": {
        # === LEVEL 1: METADATA (Always loaded, ~100 tokens) ===
        "name": {
            "type": "string",
            "minLength": 1,
            "maxLength": 64,
            "description": "Skill name in gerund form (e.g., 'Processing PDFs', 'Analyzing Spreadsheets'). Max 64 chars per Anthropic spec."
        },
        "description": {
            "type": "string",
            "minLength": 1,
            "maxLength": 1024,
            "description": "One-line description including WHAT it does and WHEN to use it. Max 1024 chars per Anthropic spec. Active voice, no first/second person."
        },
        
        # === LEVEL 2: INSTRUCTIONS (Loaded when triggered, <5k tokens) ===
        "triggers": {
            "type": "array",
            "minItems": 2,
            "items": {"type": "string", "minLength": 1},
            "description": "Phrases that should activate this skill (minimum 2)"
        },
        "inputs": {
            "type": "array",
            "minItems": 1,
            "items": {"type": "string"},
            "description": "Expected inputs (files, text, parameters, context)"
        },
        "guardrails": {
            "type": "array",
            "minItems": 1,
            "items": {"type": "string"},
            "description": "Rules and constraints Claude must follow. Be specific and actionable."
        },
        "procedure": {
            "type": "array",
            "minItems": 1,
            "items": {"type": "string"},
            "description": "Step-by-step process to follow. Each step should be clear and actionable."
        },
        "output_contract": {
            "type": "object",
            "required": ["title", "sections"],
            "description": "Defines the expected output structure",
            "properties": {
                "title": {
                    "type": "string", 
                    "minLength": 1,
                    "description": "Title of the output document/report"
                },
                "sections": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "object",
                        "required": ["heading", "required"],
                        "properties": {
                            "heading": {
                                "type": "string", 
                                "minLength": 1,
                                "description": "Section heading"
                            },
                            "required": {
                                "type": "boolean",
                                "description": "Whether this section must be included"
                            },
                            "body_hint": {
                                "type": "string",
                                "description": "Guidance on what should be in this section"
                            }
                        }
                    },
                    "description": "Sections that make up the output"
                },
                "tables": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["name", "columns"],
                        "properties": {
                            "name": {"type": "string"},
                            "columns": {
                                "type": "array",
                                "minItems": 1,
                                "items": {"type": "string", "minLength": 1}
                            }
                        }
                    },
                    "description": "Optional tables in the output"
                }
            }
        },
        "example_triggers": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Sample activation phrases for testing"
        },
        
        # === LEVEL 3+: RESOURCES & CODE (Loaded as needed, unlimited) ===
        "reference_files": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["path", "purpose"],
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Relative path using forward slashes only (e.g., 'reference/api-docs.md')"
                    },
                    "purpose": {
                        "type": "string",
                        "description": "What this reference file provides"
                    },
                    "when_to_load": {
                        "type": "string",
                        "description": "Optional: Conditions for when Claude should read this file"
                    }
                }
            },
            "description": "Additional reference materials for progressive disclosure. Keep one level deep from SKILL.md."
        },
        "code_helper": {
            "type": "object",
            "properties": {
                "enabled": {
                    "type": "boolean",
                    "description": "Whether this skill includes executable scripts"
                },
                "scripts": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["path", "purpose", "execution_mode"],
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Path to script using forward slashes (e.g., 'code/validator.py')"
                            },
                            "purpose": {
                                "type": "string",
                                "description": "What this script does"
                            },
                            "execution_mode": {
                                "type": "string",
                                "enum": ["execute", "reference"],
                                "description": "execute: Run the script; reference: Read it for implementation details"
                            },
                            "required_packages": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Pre-installed packages this script requires"
                            }
                        }
                    },
                    "description": "Executable scripts that Claude can run. Scripts execute WITHOUT loading code into context."
                }
            },
            "description": "Configuration for executable code in this skill"
        },
        "validation": {
            "type": "object",
            "properties": {
                "feedback_loop": {
                    "type": "boolean",
                    "description": "Whether this skill uses a plan-validate-execute pattern"
                },
                "validator_script": {
                    "type": "string",
                    "description": "Path to validation script (e.g., 'code/validate.py')"
                },
                "validation_pattern": {
                    "type": "string",
                    "enum": ["plan-validate-execute", "generate-validate-fix", "custom"],
                    "description": "Type of validation workflow"
                }
            },
            "description": "Validation and quality assurance configuration"
        },
        "mcp_tools": {
            "type": "array",
            "items": {
                "type": "string",
                "pattern": "^[A-Za-z0-9_-]+:[A-Za-z0-9_-]+$",
                "description": "MCP tool in format 'ServerName:tool_name' (e.g., 'BigQuery:run_query')"
            },
            "description": "MCP (Model Context Protocol) tools this skill uses. Must be fully qualified."
        },
        "visual_analysis": {
            "type": "object",
            "properties": {
                "enabled": {
                    "type": "boolean",
                    "description": "Whether this skill analyzes images"
                },
                "image_types": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Types of images analyzed (e.g., 'PDF pages', 'UI mockups', 'diagrams')"
                },
                "conversion_script": {
                    "type": "string",
                    "description": "Script to convert inputs to images (e.g., 'code/pdf_to_images.py')"
                }
            },
            "description": "Configuration for visual analysis capabilities"
        },
        "skill_metadata": {
            "type": "object",
            "properties": {
                "version": {
                    "type": "string",
                    "description": "Skill version (e.g., '1.0.0')"
                },
                "author": {
                    "type": "string",
                    "description": "Skill creator"
                },
                "tested_models": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["haiku", "sonnet", "opus"]
                    },
                    "description": "Models this skill has been tested with"
                },
                "platform_compatibility": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["claude.ai", "api", "claude-code"]
                    },
                    "description": "Platforms this skill works on"
                }
            },
            "description": "Metadata about the skill itself"
        }
    }
}


def validate_best_practices(spec: dict) -> list:
    """
    Comprehensive best practices validation based on Anthropic's official guidelines.
    Returns list of warnings (non-blocking suggestions).
    """
    warnings = []
    
    # === NAME VALIDATION ===
    name = spec.get("name", "")
    if name:
        # Check gerund form (should contain a word ending with -ing)
        # Split on spaces and check if at least one word ends with 'ing'
        words = name.split()
        has_gerund = any(word.lower().endswith('ing') for word in words)
        
        if not has_gerund:
            warnings.append(
                f"⚠️  NAME: Consider using gerund form (verb + -ing). "
                f"Examples: 'Processing PDFs', 'Analyzing Spreadsheets', 'Managing Databases'. "
                f"Current: '{name}'. "
                f"See: MASTER_KNOWLEDGE.md - Anatomy of a Skill"
            )
        
        # Check for vague words
        vague_words = ["helper", "utils", "tools", "manager", "handler"]
        if any(word in name.lower() for word in vague_words):
            warnings.append(
                f"⚠️  NAME: Avoid vague terms like 'Helper', 'Utils', 'Tools'. "
                f"Be specific about what the skill does. "
                f"Current: '{name}'"
            )
    
    # === DESCRIPTION VALIDATION ===
    description = spec.get("description", "")
    if description:
        # Check for first/second person
        first_second_person = ["i can", "you can", "this will", "i will", "you will", "we can", "let me"]
        if any(phrase in description.lower() for phrase in first_second_person):
            warnings.append(
                f"⚠️  DESCRIPTION: Use active voice without first/second person. "
                f"Good: 'Processes Excel files and generates reports'. "
                f"Avoid: 'I can help you process' or 'You can use this to'. "
                f"Current starts: '{description[:50]}...'"
            )
        
        # Check for WHAT + WHEN
        when_indicators = [" when ", " for ", " use ", " helps ", " enables "]
        if not any(indicator in description.lower() for indicator in when_indicators):
            warnings.append(
                f"⚠️  DESCRIPTION: Include both WHAT it does and WHEN to use it. "
                f"Example: 'Analyzes spreadsheets to identify patterns (WHAT). "
                f"Use when you need data insights or trend analysis (WHEN).'"
            )
    
    # === FILE PATHS VALIDATION ===
    def check_paths_recursive(obj, path=""):
        """Recursively check for Windows-style backslashes in paths"""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, str) and "\\" in v:
                    warnings.append(
                        f"⚠️  FILE PATHS: Use forward slashes only. "
                        f"Found backslash in '{path}.{k}': {v}. "
                        f"Change to: {v.replace(chr(92), '/')}"
                    )
                check_paths_recursive(v, f"{path}.{k}")
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                check_paths_recursive(item, f"{path}[{i}]")
    
    check_paths_recursive(spec)
    
    # === TIME-SENSITIVE CONTENT ===
    time_sensitive_patterns = [
        "as of ", "current", "latest", "2024", "2025", "2026", "recent",
        "now uses", "currently", "at the moment", "today", "this year"
    ]
    
    def check_time_sensitive(text, field_name):
        if text and isinstance(text, str):
            text_lower = text.lower()
            for pattern in time_sensitive_patterns:
                if pattern in text_lower:
                    warnings.append(
                        f"⚠️  TIME-SENSITIVE: Potential time-sensitive information in '{field_name}': '{pattern}'. "
                        f"Consider moving to separate 'Current Configuration' section that can be updated. "
                        f"See: MASTER_KNOWLEDGE.md - Content Quality"
                    )
                    break
    
    check_time_sensitive(spec.get("description"), "description")
    for i, guard in enumerate(spec.get("guardrails", [])):
        check_time_sensitive(guard, f"guardrails[{i}]")
    
    # === MCP TOOLS VALIDATION ===
    for tool in spec.get("mcp_tools", []):
        if ":" not in tool:
            warnings.append(
                f"⚠️  MCP TOOLS: '{tool}' should use format 'ServerName:tool_name'. "
                f"Example: 'BigQuery:run_query', 'GitHub:create_issue'. "
                f"See: MASTER_KNOWLEDGE.md - MCP Integration"
            )
    
    # === VALIDATION FEEDBACK LOOP ===
    validation_keywords = ["validate", "verify", "check", "ensure", "confirm"]
    has_validation_mentions = any(
        keyword in str(spec).lower() 
        for keyword in validation_keywords
    )
    
    if has_validation_mentions and not spec.get("validation", {}).get("feedback_loop"):
        warnings.append(
            f"⚠️  VALIDATION: Skill mentions validation but doesn't define feedback loop. "
            f"Consider adding validation.feedback_loop = true and validation.validator_script. "
            f"Pattern: Generate → Validate → Fix → Repeat. "
            f"See: MASTER_KNOWLEDGE.md - Feedback Loops for Quality"
        )
    
    # === REFERENCE FILES STRUCTURE ===
    ref_files = spec.get("reference_files", [])
    if ref_files:
        # Check for deeply nested references
        for ref in ref_files:
            path = ref.get("path", "")
            if path.count("/") > 2:
                warnings.append(
                    f"⚠️  REFERENCE FILES: Path '{path}' is deeply nested. "
                    f"Keep references one level deep from SKILL.md for best performance. "
                    f"See: MASTER_KNOWLEDGE.md - Progressive Disclosure"
                )
    
    # === CODE SCRIPTS VALIDATION ===
    if spec.get("code_helper", {}).get("enabled"):
        scripts = spec.get("code_helper", {}).get("scripts", [])
        
        if not scripts:
            warnings.append(
                f"⚠️  CODE HELPER: code_helper.enabled = true but no scripts defined. "
                f"Add scripts array with at least one script, or set enabled = false."
            )
        
        for script in scripts:
            # Check execution mode clarity
            if script.get("execution_mode") == "execute":
                # Should have clear error handling
                if "validate" in script.get("path", "").lower() and not spec.get("validation"):
                    warnings.append(
                        f"⚠️  VALIDATION SCRIPT: Found validation script '{script.get('path')}' "
                        f"but validation config not defined. Consider adding validation section."
                    )
    
    # === SKILL.MD LENGTH WARNING ===
    # Estimate SKILL.md length from spec
    estimated_lines = 0
    estimated_lines += 10  # Frontmatter + headers
    estimated_lines += len(spec.get("triggers", []))
    estimated_lines += len(spec.get("inputs", []))
    estimated_lines += len(spec.get("guardrails", []))
    estimated_lines += len(spec.get("procedure", [])) * 2  # Numbered lists take more space
    estimated_lines += len(spec.get("output_contract", {}).get("sections", [])) * 3
    estimated_lines += len(spec.get("example_triggers", []))
    
    if estimated_lines > 400:  # Conservative estimate
        warnings.append(
            f"⚠️  SKILL.MD LENGTH: Estimated ~{estimated_lines} lines in SKILL.md. "
            f"Anthropic recommends under 500 lines for optimal performance. "
            f"Consider using progressive disclosure to move some content to reference files. "
            f"See: MASTER_KNOWLEDGE.md - Structure for Scale"
        )
    
    # === PLATFORM COMPATIBILITY ===
    if spec.get("code_helper", {}).get("enabled"):
        # Check for network-dependent code
        scripts = spec.get("code_helper", {}).get("scripts", [])
        network_keywords = ["requests", "urllib", "http", "api call", "fetch"]
        
        for script in scripts:
            script_str = str(script).lower()
            if any(keyword in script_str for keyword in network_keywords):
                warnings.append(
                    f"⚠️  NETWORK ACCESS: Script may require network access. "
                    f"Claude Skills run in sandboxed environment with NO network access. "
                    f"Script: '{script.get('path')}'. "
                    f"See: MASTER_KNOWLEDGE.md - Runtime Environment Constraints"
                )
    
    # === SECURITY CONSIDERATIONS ===
    if spec.get("reference_files"):
        for ref in spec.get("reference_files", []):
            if "url" in ref.get("path", "").lower() or "http" in ref.get("path", "").lower():
                warnings.append(
                    f"⚠️  SECURITY: Reference file path contains 'url' or 'http': '{ref.get('path')}'. "
                    f"Skills cannot fetch external resources. Bundle all files in skill directory. "
                    f"See: MASTER_KNOWLEDGE.md - Security & Trust Model"
                )
    
    return warnings


def load_schema():
    """Return the skill spec schema."""
    return SKILL_SPEC_SCHEMA
