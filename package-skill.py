#!/usr/bin/env python3
"""
Package the skills-builder skill itself for upload to Claude
"""
import zipfile
from pathlib import Path

# Files to include in the skill
skill_files = [
    'skill.md',                      # The skill definition
    'MASTER_KNOWLEDGE.md',           # Referenced knowledge base
    'CLAUDE_BEST_PRACTICES.md',     # Referenced best practices
]

base_dir = Path('/Users/jaytarzwell/skills/skills-builder')
output_zip = base_dir / 'skills-builder-skill.zip'

print("Packaging skills-builder skill for Claude upload...")
print()

with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for file in skill_files:
        file_path = base_dir / file
        if file_path.exists():
            zipf.write(file_path, file)
            print(f"✓ Added: {file}")
        else:
            print(f"✗ Missing: {file}")

print()
print(f"✓ Created: {output_zip}")
print()
print("Upload this to Claude:")
print("1. Go to Settings → Capabilities → Skills")
print("2. Click 'Upload skill'")
print("3. Select skills-builder-skill.zip")
