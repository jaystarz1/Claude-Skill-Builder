"""
File system operations with safety checks.
"""
from pathlib import Path
from typing import List


def safe_path(base_dir: Path, target: str) -> Path:
    """
    Ensure target path is within base_dir (prevent directory traversal).
    """
    base = base_dir.resolve()
    full_path = (base / target).resolve()
    
    if not str(full_path).startswith(str(base)):
        raise ValueError(f"Path {target} is outside allowed directory")
    
    return full_path


def list_files(directory: Path, pattern: str = "*") -> List[Path]:
    """List all files matching pattern in directory."""
    return [f for f in directory.rglob(pattern) if f.is_file()]
