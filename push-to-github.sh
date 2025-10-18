#!/bin/bash

# Navigate to the repo directory
cd /Users/jaytarzwell/skills/skills-builder

# Initialize git if not already initialized
if [ ! -d ".git" ]; then
    git init
fi

# Add remote (ignore error if already exists)
git remote add origin https://github.com/jaystarz1/Claude-Skill-Builder.git 2>/dev/null || true

# Add all files
git add .

# Commit
git commit -m "Initial commit: Complete Claude Skills Builder with comprehensive knowledge base"

# Push to main branch
git push -u origin main

echo "✅ Successfully pushed to GitHub!"
