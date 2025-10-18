"""
Scaffold a new skill from a spec file.
"""
import json
from pathlib import Path
from typing import Dict, Any
import sys

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from plugins.renderers.jinja_renderer import render


def scaffold_skill(spec_path: str, output_dir: str) -> Path:
    """
    Create a new skill folder from a spec file.
    Returns the path to the created skill directory.
    """
    # Load spec
    with open(spec_path, 'r') as f:
        spec = json.load(f)
    
    skill_name = spec["name"].lower().replace(" ", "-")
    skill_dir = Path(output_dir) / skill_name
    skill_dir.mkdir(parents=True, exist_ok=True)
    
    # Load templates
    templates_dir = Path(__file__).parent.parent.parent / "templates"
    
    # 1. Render skill.md
    with open(templates_dir / "skill_md.tmpl", 'r') as f:
        skill_template = f.read()
    
    skill_md = render(skill_template, spec)
    (skill_dir / "skill.md").write_text(skill_md)
    
    # 2. Create templates directory and render output contract
    templates_output_dir = skill_dir / "templates"
    templates_output_dir.mkdir(exist_ok=True)
    
    with open(templates_dir / "output_contract.tmpl", 'r') as f:
        output_template = f.read()
    
    output_contract = render(output_template, spec["output_contract"])
    (templates_output_dir / "output_doc.tmpl").write_text(output_contract)
    
    # 3. Optional: code helper
    if spec.get("code_helper", {}).get("enabled"):
        code_dir = skill_dir / "code"
        code_dir.mkdir(exist_ok=True)
        
        with open(templates_dir / "code_stub.tmpl", 'r') as f:
            code_template = f.read()
        
        (code_dir / "helper.py").write_text(code_template)
    
    # 4. Create README
    with open(templates_dir / "README.tmpl", 'r') as f:
        readme_template = f.read()
    
    readme = render(readme_template, spec)
    (skill_dir / "README.md").write_text(readme)
    
    return skill_dir
