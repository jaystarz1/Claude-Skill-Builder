# FILESYSTEM MCP MANDATORY UPDATE

This document contains the updates needed for skills-builder SKILL.md to:
1. Make filesystem MCP mandatory
2. Prevent container file creation
3. Ensure all child skills inherit filesystem MCP knowledge

---

## Part 1: Add After "When to Use" Section

Insert this immediately after "When to Use" and before "Configuration":

```markdown
## ⚠️ CRITICAL REQUIREMENT: Filesystem MCP

**This skill REQUIRES the filesystem MCP to function properly.**

### Why Filesystem MCP is Mandatory

Without filesystem MCP, Claude can only create files in a temporary container (`/home/claude/`) that:
- ❌ Disappear when the session ends
- ❌ Are NOT accessible on your computer
- ❌ Cannot be uploaded to Claude Desktop
- ❌ Waste your time with fake success messages

**With filesystem MCP:**
- ✅ Files created directly on your computer in ~/skills/
- ✅ Skills immediately available
- ✅ No manual copying required
- ✅ Works reliably every time

### Installation Guide

**1. Locate your Claude Desktop config file:**

- **macOS/Linux**: `~/.config/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

**2. Add filesystem MCP configuration:**

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/YOUR_USERNAME"
      ]
    }
  }
}
```

**Important:** Replace `/Users/YOUR_USERNAME` with your actual home directory:
- macOS: `/Users/yourname`
- Linux: `/home/yourname`
- Windows: `C:\\Users\\yourname` (note double backslashes)

**3. Restart Claude Desktop**

**4. Verify installation:**

Ask Claude: "List allowed directories"

If working, you'll see your home directory path.

### Official Documentation

- **Filesystem MCP**: https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem
- **MCP Setup Guide**: https://modelcontextprotocol.io/quickstart/user
```

---

## Part 2: Add After "Configuration" Section

Insert this new section after "Configuration" and before "Ground Rules":

```markdown
## 🔧 Filesystem MCP Tools - Mandatory Usage

**CRITICAL: Every file operation in skills-builder MUST use filesystem MCP tools.**

### Available Filesystem MCP Tools

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `filesystem:list_allowed_directories` | Get allowed paths | Phase 0 - path detection |
| `filesystem:create_directory` | Create folders | Creating skill structure |
| `filesystem:write_file` | Create/overwrite files | SKILL.md, scripts, examples |
| `filesystem:read_text_file` | Read file contents | Reading existing skills |
| `filesystem:list_directory` | List folder contents | Verification |
| `filesystem:directory_tree` | Show folder tree | Display final structure |
| `filesystem:edit_file` | Edit existing files | Updating skills |
| `filesystem:move_file` | Move/rename files | Reorganization |
| `filesystem:search_files` | Find files by pattern | Locating existing skills |
| `filesystem:get_file_info` | Get file metadata | Check if file exists |

### 🚨 NEVER Use Container Tools

**These tools only work in temporary container - DO NOT USE:**

- ❌ `create_file` → Use `filesystem:write_file` instead
- ❌ `str_replace` → Use `filesystem:edit_file` instead  
- ❌ `view` for file creation → Use filesystem MCP tools
- ❌ `bash` for file operations → Use filesystem MCP tools

**Exception: bash_tool is OK for:**
- ✅ Making scripts executable: `chmod +x script.sh`
- ✅ Running Python scripts: `python3 script.py`
- ✅ Git operations (if Git MCP unavailable)
- ❌ NOT for creating/writing/moving files

### Path Rules

**ALWAYS use absolute paths:**
- ✅ `/Users/alice/skills/my-skill/SKILL.md`
- ❌ `~/skills/my-skill/SKILL.md` (tilde may not expand)
- ❌ `my-skill/SKILL.md` (relative path)
- ❌ `/home/claude/my-skill/SKILL.md` (container - WRONG!)

**ALWAYS resolve {SKILLS_DIR} to absolute path before use:**
- Detected: `{SKILLS_DIR}` = `/Users/alice/skills/`
- In tool calls: `filesystem:write_file(path="/Users/alice/skills/my-skill/SKILL.md", ...)`

### Tool Selection Rules

| Operation | CORRECT Tool | WRONG Tool |
|-----------|--------------|------------|
| Create directory | `filesystem:create_directory` | ❌ `bash mkdir` |
| Write new file | `filesystem:write_file` | ❌ `create_file` |
| Read file | `filesystem:read_text_file` | ⚠️ `view` (container only) |
| Edit file | `filesystem:edit_file` | ❌ `str_replace` (container) |
| List directory | `filesystem:list_directory` | ❌ `bash ls` |
| Check if exists | `filesystem:get_file_info` | ❌ `bash test -f` |
| Move file | `filesystem:move_file` | ❌ `bash mv` |
| Search files | `filesystem:search_files` | ❌ `bash find` |

### Verification After File Operations

After creating/modifying files, ALWAYS verify with:

```
filesystem:directory_tree(path="{absolute_path_to_skill}")
```

**Signs you're using container (BAD):**
- ❌ Paths contain `/home/claude/`
- ❌ User says "I don't see the files"
- ❌ Using `create_file` or `str_replace` tools

**Signs you're using filesystem MCP (GOOD):**
- ✅ Paths contain `/Users/` or `/home/{real-username}/`
- ✅ `filesystem:directory_tree` shows the structure
- ✅ User confirms files exist on their computer
```

---

## Part 3: REPLACE Existing Phase 0

**Replace the entire Phase 0 section with this:**

```markdown
### Phase 0: Pre-flight Validation (CRITICAL - DO THIS FIRST)

**STEP 1: TEST FILESYSTEM MCP (MANDATORY - BLOCKS EVERYTHING)**

1. **Attempt to call filesystem MCP:**
   
   ```
   Tool: filesystem:list_allowed_directories
   ```
   
   **If SUCCESS:**
   - ✅ Filesystem MCP is available
   - Store the allowed directories list
   - Proceed to Step 2
   
   **If FAILS (error contains "unknown tool" or "not found"):**
   - ❌ STOP IMMEDIATELY - DO NOT PROCEED
   - Display the error message below
   - DO NOT create any files
   - DO NOT use container tools as fallback

2. **Error Message When Filesystem MCP Missing:**

```
❌ FILESYSTEM MCP REQUIRED

The skills-builder cannot function without the filesystem MCP.

Without it, I can only create temporary files in /home/claude/ that:
- Disappear when this session ends
- Are NOT accessible on your computer
- Cannot be uploaded to Claude Desktop
- Waste your time

📚 How to Install Filesystem MCP:

1. Open your Claude Desktop config file:
   - macOS/Linux: ~/.config/Claude/claude_desktop_config.json
   - Windows: %APPDATA%\Claude\claude_desktop_config.json

2. Add this configuration:
   
   {
     "mcpServers": {
       "filesystem": {
         "command": "npx",
         "args": [
           "-y",
           "@modelcontextprotocol/server-filesystem",
           "/Users/YOUR_USERNAME"
         ]
       }
     }
   }
   
   Replace /Users/YOUR_USERNAME with your home directory:
   - macOS: /Users/yourname
   - Linux: /home/yourname
   - Windows: C:\\Users\\yourname

3. Restart Claude Desktop

4. Try again: "Build a skill for [your task]"

📖 Official Documentation:
https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem

⚠️ I cannot create skills without filesystem MCP installed.
```

**STEP 2: DETECT SKILLS DIRECTORY**

Only proceed here if Step 1 succeeded.

1. **Get allowed directories from Step 1:**
   ```python
   # Already called: filesystem:list_allowed_directories
   # Result stored - typically shows user's home directory
   ```

2. **Detect or create skills directory:**
   ```python
   import os
   from pathlib import Path
   
   # Priority 1: Check environment variable
   env_skills_dir = os.getenv('SKILLS_DIR')
   if env_skills_dir:
       SKILLS_DIR = Path(env_skills_dir).expanduser().resolve()
   else:
       # Priority 2: Check for ~/skills/ or ~/Skills/
       home = Path.home()
       if (home / 'skills').exists():
           SKILLS_DIR = home / 'skills'
       elif (home / 'Skills').exists():
           SKILLS_DIR = home / 'Skills'
       else:
           # Priority 3: Create ~/skills/
           SKILLS_DIR = home / 'skills'
   
   # Convert to absolute path string
   SKILLS_DIR = str(SKILLS_DIR.resolve())
   ```

3. **Verify skills directory is within allowed directories:**
   ```python
   # Check if SKILLS_DIR starts with any allowed directory
   # If not, show error and stop
   ```

**STEP 3: CREATE OR VERIFY SKILLS DIRECTORY**

```
Tool: filesystem:list_directory(path=SKILLS_DIR)

If directory doesn't exist:
  Tool: filesystem:create_directory(path=SKILLS_DIR)
  Inform user: "Created skills directory at {SKILLS_DIR}"

If directory exists:
  Display: "✅ Using skills directory: {SKILLS_DIR}"
```

**STEP 4: DETERMINE SKILL SLUG**

1. Convert user's skill name to lowercase-with-hyphens
2. Remove forbidden words ('claude', 'anthropic', 'ai')
3. Validate ≤ 64 characters
4. Check if skill already exists:
   ```
   Tool: filesystem:list_directory(path=SKILLS_DIR)
   ```
   If slug exists, ask user: update existing or create new version?

**STEP 5: CONFIRM PATH WITH USER**

Display to user:
```
✅ Filesystem MCP: Available
✅ Skills directory: {SKILLS_DIR}
✅ Creating skill at: {SKILLS_DIR}/{skill-slug}/

Ready to proceed?
```

**Only proceed to Phase 0.5 after all 5 steps succeed.**
```

---

## Part 4: Update Phase 3 (Structure Creation)

**Replace Phase 3 with this:**

```markdown
### Phase 3: Structure & Organization

**CRITICAL: Use filesystem MCP for ALL directory and file operations.**

**Step 1: Create base skill directory**

```
Tool: filesystem:create_directory(path="{SKILLS_DIR}/{skill-slug}/")

Example: filesystem:create_directory(path="/Users/alice/skills/meeting-notes/")
```

**Step 2: Create subdirectories (as needed)**

```
If examples provided:
  Tool: filesystem:create_directory(path="{SKILLS_DIR}/{skill-slug}/examples/")

If reference files needed:
  Tool: filesystem:create_directory(path="{SKILLS_DIR}/{skill-slug}/references/")

If code helpers needed:
  Tool: filesystem:create_directory(path="{SKILLS_DIR}/{skill-slug}/code/")
```

**Step 3: Verify structure created**

```
Tool: filesystem:directory_tree(path="{SKILLS_DIR}/{skill-slug}/")

Expected output shows:
skill-slug/
├── examples/ (if created)
├── references/ (if created)
└── code/ (if created)
```

**🚨 REMINDER: NEVER use:**
- ❌ `bash mkdir` commands
- ❌ `create_file` tool
- ❌ Container paths (`/home/claude/`)

**ALWAYS use:**
- ✅ `filesystem:create_directory` with absolute paths
- ✅ Paths resolved from {SKILLS_DIR} variable
```

---

## Part 5: Update Phase 5 (File Generation)

**Replace the file creation parts of Phase 5 with this:**

```markdown
### Phase 5: Generation & Packaging

**CRITICAL: EVERY file creation uses filesystem:write_file**

**Step 1: Create SKILL.md**

```
Tool: filesystem:write_file(
  path="{SKILLS_DIR}/{skill-slug}/SKILL.md",
  content="---
name: {skill-slug}
description: {description}
---

[Full SKILL.md content here]
"
)

Example:
filesystem:write_file(
  path="/Users/alice/skills/meeting-notes/SKILL.md",
  content="[content]"
)
```

**Step 2: Create examples (if user provided any)**

```
For each example:
  Tool: filesystem:write_file(
    path="{SKILLS_DIR}/{skill-slug}/examples/example-1-name.md",
    content="[example content]"
  )
```

**Step 3: Create UPDATING.md**

```
Tool: filesystem:write_file(
  path="{SKILLS_DIR}/{skill-slug}/UPDATING.md",
  content="[updating instructions]"
)
```

**Step 4: Create API deployment scripts**

```
Tool: filesystem:write_file(
  path="{SKILLS_DIR}/{skill-slug}/deploy-to-api.sh",
  content="#!/bin/bash
[deployment script content]"
)

Tool: filesystem:write_file(
  path="{SKILLS_DIR}/{skill-slug}/deploy-to-api.py",
  content="#!/usr/bin/env python3
[deployment script content]"
)
```

**Step 5: Make scripts executable (bash OK for this)**

```
bash_tool: chmod +x {SKILLS_DIR}/{skill-slug}/deploy-to-api.sh
bash_tool: chmod +x {SKILLS_DIR}/{skill-slug}/deploy-to-api.py
```

**Step 6: Verify all files created**

```
Tool: filesystem:directory_tree(path="{SKILLS_DIR}/{skill-slug}/")

Expected output:
skill-slug/
├── SKILL.md
├── UPDATING.md
├── deploy-to-api.sh
├── deploy-to-api.py
├── examples/
│   └── example-1-name.md
└── ...
```

**Step 7: Create ZIP file**

[Keep existing ZIP creation logic]

**🚨 CRITICAL REMINDER:**
- NEVER use `create_file` - it goes to container
- ALWAYS use `filesystem:write_file` with absolute paths
- ALWAYS verify with `filesystem:directory_tree` after creation
```

---

## Part 6: Template for ALL Generated Skills

**CRITICAL: Every skill created by skills-builder must include this section.**

Add this template to the skill generation code. This goes into EVERY generated SKILL.md:

```markdown
## 🔧 Using Filesystem MCP (Mother MCP)

**This skill inherits filesystem MCP knowledge from skills-builder.**

### What is Filesystem MCP?

The filesystem MCP is your "mother MCP" - it gives Claude access to your computer's filesystem so skills can:
- ✅ Read files you created
- ✅ Write output files
- ✅ Update their own SKILL.md
- ✅ Create and organize directories

### When This Skill Needs Filesystem Access

**This skill uses filesystem MCP when:**
[List specific use cases for this skill]

Examples:
- Reading input documents from ~/Documents/
- Writing analysis reports to ~/output/
- Updating this skill's examples folder
- Creating configuration files

### Self-Editing Capability

**This skill can update itself using filesystem MCP:**

If you ask to:
- "Add a new example to this skill"
- "Update the procedure in this skill"
- "Fix a typo in the skill instructions"

Claude will:
1. Use `filesystem:read_text_file` to read current SKILL.md
2. Use `filesystem:edit_file` to make changes
3. Recreate the ZIP file
4. Remind you to upload the new ZIP

### Filesystem MCP Tools This Skill May Use

| Tool | Purpose |
|------|---------|
| `filesystem:read_text_file` | Read input files, read this SKILL.md |
| `filesystem:write_file` | Create output files, update skill |
| `filesystem:list_directory` | Browse directories |
| `filesystem:create_directory` | Organize output |
| `filesystem:edit_file` | Update this skill |

### Important Notes

- **Filesystem MCP must be installed** for this skill to work properly
- **Never creates files in /home/claude/** - always uses your real filesystem
- **Always asks before modifying files** outside the skill directory
- **Can self-update** its own SKILL.md when you request changes

### If Filesystem MCP is Not Available

If you see errors like "unknown tool: filesystem:read_text_file":

1. Install filesystem MCP (see skills-builder documentation)
2. Restart Claude Desktop
3. This skill will then work properly

**Without filesystem MCP, this skill cannot access your files.**
```

---

## Part 7: Update "Updating Existing Skills" Section

**Replace the existing "Updating Existing Skills" section with this:**

```markdown
## Updating Existing Skills

When the user wants to modify, fix, or improve an existing skill:

### Update Procedure

**CRITICAL: Use filesystem MCP for all read/write operations.**

**Step 1: Locate the skill**

```
Tool: filesystem:list_directory(path="{SKILLS_DIR}")

Look for skill directory matching requested name
```

**Step 2: Read existing SKILL.md**

```
Tool: filesystem:read_text_file(path="{SKILLS_DIR}/{skill-slug}/SKILL.md")

Parse the content to understand current structure
```

**Step 3: Identify what needs to change**

Ask user to confirm specific changes needed.

**Step 4: Make the changes**

```
For small changes (typos, adding lines):
  Tool: filesystem:edit_file(
    path="{SKILLS_DIR}/{skill-slug}/SKILL.md",
    edits=[
      {oldText: "...", newText: "..."}
    ]
  )

For large changes (rewriting sections):
  Tool: filesystem:write_file(
    path="{SKILLS_DIR}/{skill-slug}/SKILL.md",
    content="[complete new content]"
  )
```

**Step 5: Recreate ZIP file**

[Use existing ZIP creation logic]

**Step 6: Remind user to upload**

```
✅ Updated: {SKILLS_DIR}/{skill-slug}/
✅ Recreated: {skill-slug}.zip

🔴 UPLOAD REQUIRED: Upload new ZIP to claude.ai to apply changes
```

**🚨 NEVER use:**
- ❌ `view` to read files (container only)
- ❌ `str_replace` to edit files (container only)
- ❌ `create_file` to write files (container only)

**ALWAYS use:**
- ✅ `filesystem:read_text_file` to read
- ✅ `filesystem:edit_file` to edit  
- ✅ `filesystem:write_file` to rewrite
```

---

## Summary of Changes

1. ✅ Added mandatory filesystem MCP requirement section
2. ✅ Added filesystem MCP tools reference
3. ✅ Replaced Phase 0 with filesystem MCP detection first
4. ✅ Updated Phase 3 to use only filesystem:create_directory
5. ✅ Updated Phase 5 to use only filesystem:write_file
6. ✅ Added template section for all generated skills
7. ✅ Updated skill updating section to use filesystem MCP
8. ✅ Made all file operations explicit with correct tool names
9. ✅ Added verification steps after each operation
10. ✅ Ensured child skills inherit filesystem MCP knowledge

**Every generated skill will now know:**
- Filesystem MCP is its "mother MCP"
- How to use it for file operations
- How to self-update using filesystem MCP
- Never to use container tools
