"""
Package a skill directory into a .zip file for upload to Claude.
"""
import zipfile
from pathlib import Path


def pack_skill(skill_dir: str, output_path: str) -> Path:
    """
    Create a .zip archive of a skill directory.
    Returns the path to the created .zip file.
    """
    skill_path = Path(skill_dir)
    output_file = Path(output_path)
    
    if not skill_path.exists():
        raise FileNotFoundError(f"Skill directory not found: {skill_dir}")
    
    # Create parent directory if needed
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Create zip archive
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in skill_path.rglob('*'):
            if file_path.is_file():
                # Add file with relative path
                arcname = file_path.relative_to(skill_path.parent)
                zipf.write(file_path, arcname)
    
    return output_file
