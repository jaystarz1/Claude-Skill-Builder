**ADD THIS TO PHASE 5 AS STEP 11 - AFTER ZIP CREATION AND BEFORE UPDATING.MD TEMPLATE:**

---

11. **GIT VERSION CONTROL INTEGRATION** (Automatic if Git MCP available)

**Initialize Git repository and create initial commit:**

After creating all skill files and ZIP, automatically set up Git version control:

```
STEP 1: Initialize Git repository
Tool: git:git_init
Parameters: {
  "repo_path": "{SKILLS_DIR}/{skill-slug}"
}

Expected result: "Initialized empty Git repository"

STEP 2: Stage all files
Tool: git:git_add
Parameters: {
  "repo_path": "{SKILLS_DIR}/{skill-slug}",
  "files": ["."]
}

Expected result: "Files staged successfully"

STEP 3: Create initial commit
Tool: git:git_commit
Parameters: {
  "repo_path": "{SKILLS_DIR}/{skill-slug}",
  "message": "feat: initial {skill-slug} skill creation\n\n- Created SKILL.md with core functionality\n- Added examples and reference materials\n- Configured for Claude Desktop and API deployment"
}

Expected result: Commit hash and success message

STEP 4: Remote setup (if user provides URL)
If user wants to push to GitHub/GitLab/etc, ask for remote URL then:

Create init-remote.sh script:
filesystem:write_file(
  path="{SKILLS_DIR}/{skill-slug}/init-remote.sh",
  content="""#!/bin/bash
cd "$(dirname "$0")"
git remote add origin [USER_PROVIDED_URL]
echo "✅ Remote configured. Run 'git push -u origin main' to push."
"""
)

Inform user: "Run ./init-remote.sh to configure your Git remote, then I can push for you."

STEP 5: Push to remote (after user runs init-remote.sh OR if remote already configured)
Tool: git:git_push
Parameters: {
  "repo_path": "{SKILLS_DIR}/{skill-slug}",
  "branch": "main"
}
```

**Benefits:**
- ✅ Automatic Git initialization - no manual setup
- ✅ Proper conventional commit message
- ✅ Ready to push to remote (after one-time remote setup)
- ✅ Full version history from day one
- ✅ Works with any Git hosting (GitHub, GitLab, Bitbucket)

**Error Handling:**
- If `git:git_init` fails with "unknown tool" → Git MCP not configured, skip Git setup
- If Git MCP unavailable → Inform user they can manually run `git init` if desired
- Never fail skill creation due to Git issues - it's optional enhancement

**When Updating Existing Skills:**

After making changes to skill files, automatically commit:

```
STEP 1: Check status
Tool: git:git_status
Parameters: {
  "repo_path": "{SKILLS_DIR}/{skill-slug}"
}

STEP 2: Stage modified files
Tool: git:git_add
Parameters: {
  "repo_path": "{SKILLS_DIR}/{skill-slug}",
  "files": ["SKILL.md"]  # or whichever files changed
}

STEP 3: Commit changes
Tool: git:git_commit
Parameters: {
  "repo_path": "{SKILLS_DIR}/{skill-slug}",
  "message": "fix: [describe what was changed]"
}

STEP 4: Push (if remote configured)
Tool: git:git_push
Parameters: {
  "repo_path": "{SKILLS_DIR}/{skill-slug}",
  "branch": "main"
}
```

**Commit Message Conventions:**
- `feat:` - New functionality
- `fix:` - Bug fixes, typos, corrections
- `docs:` - Documentation updates
- `refactor:` - Restructuring without changing functionality
- `chore:` - Maintenance tasks (ZIP rebuild, etc.)

---

**ALSO UPDATE "Updating Existing Skills" SECTION TO INCLUDE:**

After Step 5 "AUTOMATICALLY RECREATE ZIP FILE", add:

**6. AUTOMATICALLY COMMIT CHANGES** (if Git repo exists)

If the skill directory is a Git repository, automatically commit the changes:

```
git:git_status - Check what changed
git:git_add - Stage the modified files
git:git_commit - Commit with descriptive message (e.g., "fix: correct typo in examples")
git:git_push - Push to remote (if configured)
```

This ensures all skill updates are properly versioned and backed up.
