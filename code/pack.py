"""
Package a skill directory into a .zip file for upload to Claude.
"""
import zipfile
from pathlib import Path


def pack_skill(skill_dir: str, output_path: str) -> Path:
    """
    Create a .zip archive of a skill directory.
    Returns the path to the created .zip file.
    
    The ZIP file will have files at the root level (not in a subdirectory)
    as required by Claude's skill upload format.
    """
    skill_path = Path(skill_dir)
    output_file = Path(output_path)
    
    if not skill_path.exists():
        raise FileNotFoundError(f"Skill directory not found: {skill_dir}")
    
    # Create parent directory if needed
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Create zip archive with files at root level
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in skill_path.rglob('*'):
            if file_path.is_file():
                # Add file with path relative to the skill directory itself
                # This puts files at the root of the ZIP, not in a subdirectory
                arcname = file_path.relative_to(skill_path)
                zipf.write(file_path, arcname)
    
    return output_file
