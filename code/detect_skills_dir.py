#!/usr/bin/env python3
"""
Detect the user's skills directory location.
Works cross-platform for macOS, Linux, and Windows.
"""
import os
import sys
from pathlib import Path


def detect_skills_directory():
    """
    Detect the user's skills directory.
    
    Priority order:
    1. $SKILLS_DIR environment variable (if set)
    2. ~/skills/ directory (if exists)
    3. Return None (will need to create it)
    
    Returns:
        Path object or None
    """
    # Check for environment variable override
    env_skills_dir = os.getenv('SKILLS_DIR')
    if env_skills_dir:
        path = Path(env_skills_dir).expanduser().resolve()
        if path.exists() and path.is_dir():
            return path
    
    # Check for ~/skills directory
    home_skills = Path.home() / 'skills'
    if home_skills.exists() and home_skills.is_dir():
        return home_skills
    
    # Return None - directory doesn't exist yet
    return None


def get_or_create_skills_directory():
    """
    Get the skills directory path, creating it if necessary.
    
    Returns:
        Path object
    """
    skills_dir = detect_skills_directory()
    
    if skills_dir is None:
        # Create ~/skills directory
        skills_dir = Path.home() / 'skills'
        try:
            skills_dir.mkdir(parents=True, exist_ok=True)
            print(f"Created skills directory at: {skills_dir}", file=sys.stderr)
        except Exception as e:
            print(f"Error creating skills directory: {e}", file=sys.stderr)
            return None
    
    return skills_dir


def main():
    """Print the skills directory path."""
    skills_dir = get_or_create_skills_directory()
    if skills_dir:
        print(str(skills_dir))
        return 0
    else:
        print("Error: Could not detect or create skills directory", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
