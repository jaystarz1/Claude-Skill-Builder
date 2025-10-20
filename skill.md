---
name: skills-builder
description: Creates world-class agent Skills following Anthropic's official specifications and best practices. Use when building custom Skills for web, desktop, or API - handles validation, generation, and packaging.
license: Apache-2.0
---

# Building Claude Skills

A comprehensive skill-builder that creates production-ready Claude Skills following all official Anthropic guidelines.

## When to Use
- User wants to create a new Claude Skill
- User says "build a skill", "create a skill", "make a skill"
- **User wants to update, modify, or fix an existing skill**
- User wants to validate or improve an existing skill
- User needs to package a skill for upload
- User asks about Skills best practices or architecture

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

## Configuration

### DYNAMIC SKILLS DIRECTORY DETECTION

**Skills Directory Location Strategy:**

The skills-builder automatically detects the user's skills directory using this priority order:

1. **Environment Variable** (highest priority):
   - Check for `$SKILLS_DIR` environment variable
   - If set and exists: use that path
   
2. **Standard Location** (default):
   - Check for `~/skills/` directory (user's home directory + `/skills/`)
   - If exists: use that path
   
3. **Auto-Create** (fallback):
   - If neither above exist: create `~/skills/` directory
   - Inform user of the new location

**Detection Method:**

**BEFORE starting ANY skill creation or update, run this detection:**

```python
import os
from pathlib import Path

# Method 1: Check environment variable
env_skills_dir = os.getenv('SKILLS_DIR')
if env_skills_dir:
    skills_base = Path(env_skills_dir).expanduser().resolve()
    if skills_base.exists():
        use_skills_dir = skills_base
        
# Method 2: Check ~/skills/
if not skills_base or not skills_base.exists():
    skills_base = Path.home() / 'skills'
    if skills_base.exists():
        use_skills_dir = skills_base
        
# Method 3: Create ~/skills/
if not skills_base or not skills_base.exists():
    skills_base = Path.home() / 'skills'
    try:
        skills_base.mkdir(parents=True, exist_ok=True)
        use_skills_dir = skills_base
        # Inform user: "Created skills directory at {skills_base}"
    except Exception as e:
        # ERROR - cannot create directory
        use_skills_dir = None

# Result: use_skills_dir contains the absolute path
```

**OR use the helper script:**

```bash
python3 code/detect_skills_dir.py
# Returns the absolute path to skills directory
```

**Examples of Detected Paths:**
- macOS: `/Users/alice/skills/`
- Linux: `/home/alice/skills/`
- Windows: `C:\Users\alice\skills\`

**Throughout this skill, whenever you see `{SKILLS_DIR}`, replace it with the detected skills directory path.**

### CRITICAL PATH REQUIREMENTS

**NEVER create skills in:**
- ❌ `/home/claude/` (container - files are temporary and disappear)
- ❌ `/tmp/` (temporary - files are deleted)
- ❌ Any relative path without full validation
- ❌ Any path not explicitly confirmed to be on user's filesystem

**ALWAYS create skills in:**
- ✅ `{SKILLS_DIR}/{skill-slug}/` (dynamically detected path)
- ✅ Full absolute paths only
- ✅ Using filesystem MCP tools exclusively
- ✅ After validating directory exists and is accessible

**Before starting ANY skill creation:**
1. **TEST FILESYSTEM MCP** - verify it's available (Phase 0 Step 1)
2. **DETECT SKILLS DIRECTORY** using method above - store as `{SKILLS_DIR}`
3. Call `filesystem:list_directory` on `{SKILLS_DIR}`
4. If this fails, STOP and report error to user
5. If this succeeds, proceed with skill creation IN THIS DIRECTORY

## 🔧 Filesystem MCP Tools - Mandatory Usage

**CRITICAL: Every file operation MUST use filesystem MCP tools.**

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

## Inputs
- User's description of what the skill should do
- Workflow/procedures the skill should follow
- **CRITICAL: Examples of good outputs or use cases** (ALWAYS ASK FOR THESE)
- Optional: existing skill.spec.json file
- Optional: reference materials to include
- Optional: scripts or code to bundle

## Ground Rules
- Follow ALL Anthropic specifications (64-char names, 1024-char descriptions)
- **CRITICAL**: Generated skills MUST use `SKILL.md` (uppercase) - Claude requires this exact filename
- **CRITICAL**: Skill names in SKILL.md YAML must be lowercase-with-hyphens-only (e.g., 'processing-pdfs', 'analyzing-data')
- **CRITICAL**: Skill names CANNOT contain reserved words: 'claude', 'anthropic', 'ai'
- **CRITICAL**: ALL filenames must be lowercase (SKILL.md, README.md are exceptions)
- **CRITICAL**: ALL folder names must be lowercase (e.g., 'examples/', 'references/', 'code/')
- **CRITICAL**: Example filenames must be lowercase with hyphens (e.g., 'example-1-posting-grievance.md')
- Use gerund form for spec names in examples ("Processing PDFs" becomes 'processing-pdfs' in SKILL.md)
- Descriptions must include WHAT it does AND WHEN to use it
- Always use forward slashes in paths (never backslashes)
- Keep SKILL.md under 500 lines (use progressive disclosure for more)
- No network access in scripts (Skills run in sandboxed environment)
- Only use pre-installed packages (no runtime installation)
- Validate against security best practices
- Generate skills that work on web, desktop, API, AND Claude Code
- **ALWAYS use filesystem MCP tools for ALL file operations**

## Knowledge Base

This skill has access to comprehensive knowledge about Claude Skills:

### Core References
- **MASTER_KNOWLEDGE.md** - 15,000+ word complete reference covering:
  - What Skills are and how they work
  - Three-level loading architecture (metadata, instructions, resources)
  - Progressive disclosure patterns
  - Platform-specific deployment (claude.ai, API, Claude Code)
  - Security and trust model
  - Development best practices
  - API integration
  - Advanced patterns

- **CLAUDE_BEST_PRACTICES.md** - Anthropic's official guidelines including:
  - Naming conventions
  - Content quality standards
  - Progressive disclosure patterns
  - Workflow and feedback loop patterns
  - Testing requirements

### Technical Implementation
- **Schema validation** (`code/schema.py`) - Comprehensive validation rules
- **Templates** (`templates/`) - Production-ready skill templates
- **Examples** (`examples/`) - Reference implementations
- **Helper Script** (`code/detect_skills_dir.py`) - Dynamic path detection

## Procedure

### Phase 0: Pre-flight Validation (CRITICAL - DO THIS FIRST)

**STEP 1: TEST FILESYSTEM MCP (MANDATORY - BLOCKS EVERYTHING)**

1. **Attempt to call filesystem MCP:**
   
   Tool: `filesystem:list_allowed_directories`
   
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

Tool: `filesystem:list_directory(path=SKILLS_DIR)`

If directory doesn't exist:
  Tool: `filesystem:create_directory(path=SKILLS_DIR)`
  Inform user: "Created skills directory at {SKILLS_DIR}"

If directory exists:
  Display: "✅ Using skills directory: {SKILLS_DIR}"

**STEP 4: DETERMINE SKILL SLUG**

1. Convert user's skill name to lowercase-with-hyphens
2. Remove forbidden words ('claude', 'anthropic', 'ai')
3. Validate ≤ 64 characters
4. Check if skill already exists:
   Tool: `filesystem:list_directory(path=SKILLS_DIR)`
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

### Phase 0.5: Claude Code Integration Detection (Optional)

**After detecting skills directory, check for Claude Code installation:**

This step enables automatic symlink creation so skills work in BOTH Claude Desktop AND Claude Code.

1. **Detect Claude Code directory:**
   ```python
   from pathlib import Path
   
   claude_code_dir = Path.home() / '.claude' / 'skills'
   has_claude_code = claude_code_dir.exists()
   ```

2. **Ask user about Claude Code integration (ONLY if Claude Code detected):**
   ```
   If claude_code_dir.exists():
       Ask: "I detected Claude Code installed. Would you like this skill to work automatically in Claude Code? (y/n)"
       - Yes: Set enable_claude_code_integration = True
       - No: Set enable_claude_code_integration = False
   
   If not claude_code_dir.exists():
       Set enable_claude_code_integration = False
       Skip asking (user doesn't have Claude Code)
   ```

3. **Store preference for this session:**
   - This preference applies to ALL skills created/updated in this conversation
   - Don't ask again unless user explicitly requests

4. **Inform user:**
   ```
   If enabled:
       "✅ Claude Code integration enabled - skills will work in both Claude Desktop and Claude Code"
   
   If not enabled:
       "ℹ️  Claude Code integration disabled - skill will work in Claude Desktop only"
   ```

**What This Does:**
- If enabled: Auto-creates symlink in `~/.claude/skills/` pointing to `~/skills/` 
- Changes to skill files automatically reflected in Claude Code
- No duplication - one source of truth in `~/skills/`
- Fallback to copy on Windows if symlinks require admin rights

**Only after this check completes, proceed to Phase 1.**

### Phase 1: Discovery & Specification
1. Ask user what the skill should do (be specific)
2. Identify the workflow/procedure the skill follows
3. Determine inputs the skill needs
4. Establish guardrails and constraints
5. Define expected output format
6. **CRITICAL: Ask about examples** - Does the user have example outputs, documents, or use cases?
7. Identify any reference materials or scripts needed

**Key Questions:**
- What specific task does this skill perform?
- When should Claude use this skill? (triggers)
- What inputs does it need? (files, parameters, context)
- What rules must it follow? (guardrails)
- What's the step-by-step procedure?
- What should the output look like?
- **Do you have examples of good outputs/documents this skill should produce?** (ALWAYS ASK)
- **Do you have sample inputs or use cases to include as examples?** (ALWAYS ASK)
- Does it need reference files? (progressive disclosure)
- Does it need executable scripts? (code helper)
- Does it need validation? (feedback loops)

### Phase 2: Specification Creation
1. Create skill.spec.json following schema
2. Apply naming conventions (gerund form)
3. Craft description (WHAT + WHEN, active voice)
4. Define all required sections
5. Add optional features (reference files, code, validation)
6. Reference MASTER_KNOWLEDGE.md for patterns

**Validation Checkpoints:**
- Name ≤ 64 characters?
- **Name is lowercase-with-hyphens-only?** (e.g., 'processing-pdfs')
- **Name does NOT contain 'claude', 'anthropic', or 'ai'?**
- Spec uses gerund form in examples? ("Processing PDFs")
- Description ≤ 1024 characters, includes WHAT + WHEN?
- At least 2 triggers defined?
- All required fields present?
- File paths use forward slashes?
- No time-sensitive content?
- MCP tools properly formatted (ServerName:tool_name)?

### Phase 3: Structure & Organization

**CRITICAL: Use filesystem MCP for ALL directory operations.**

**Step 1: Create base skill directory**

Tool: `filesystem:create_directory(path="{SKILLS_DIR}/{skill-slug}/")`

Example: `filesystem:create_directory(path="/Users/alice/skills/meeting-notes/")`

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

Tool: `filesystem:directory_tree(path="{SKILLS_DIR}/{skill-slug}/")`

Expected output shows:
```
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

**CRITICAL: Examples Folder**
- **ALWAYS create examples/ folder if user provided ANY examples**
- Save each example with descriptive filename (example-1-posting-grievance.md)
- **ALL example filenames MUST be lowercase with hyphens** (no capitals, no underscores, no spaces)
- Include README.md in examples/ explaining what each example demonstrates
- Reference examples from SKILL.md so Claude knows they exist

**CRITICAL: Folder and Filename Rules**
- Folder names: lowercase only (examples/, references/, code/)
- File names: lowercase-with-hyphens.md (except SKILL.md and README.md)
- NO capital letters in filenames (SYNOPSIS.md ❌, synopsis.md ✅)
- NO underscores (example_1.md ❌, example-1.md ✅)
- NO spaces (example 1.md ❌, example-1.md ✅)

**Organization Patterns:**
- **Simple skills**: Just SKILL.md
- **Medium skills**: SKILL.md + reference files
- **Complex skills**: SKILL.md + reference/ + code/ + examples/
- **Multi-domain**: Separate reference files per domain

### Phase 4: Validation
1. Run structural validation (blocking errors)
2. Run best practices validation (warnings)
3. Check against CLAUDE_BEST_PRACTICES.md
4. Verify platform compatibility
5. Security audit (no network, proper error handling)

**Validation Categories:**
- ❌ **Errors** (must fix): Missing fields, limit violations, invalid formats
- ⚠️ **Warnings** (should fix): Best practice violations, suboptimal patterns

### Phase 5: Generation & Packaging

**CRITICAL: EVERY file creation uses filesystem:write_file**

**Step 1: Create SKILL.md**

Tool: `filesystem:write_file(
  path="{SKILLS_DIR}/{skill-slug}/SKILL.md",
  content="---
name: {skill-slug}
description: {description}
---

[Full SKILL.md content here]
"
)`

Example:
```
filesystem:write_file(
  path="/Users/alice/skills/meeting-notes/SKILL.md",
  content="[content]"
)
```

**IMPORTANT: Include Filesystem MCP Section in Every Generated Skill**

Every generated SKILL.md MUST include this section after "When to Use":

```markdown
## 🔧 Filesystem MCP - Your Mother MCP

**This skill was created by skills-builder and inherits filesystem MCP knowledge.**

### What is Filesystem MCP?

Filesystem MCP is your "mother MCP" - it gives Claude access to your computer's filesystem:
- ✅ Read files you've created
- ✅ Write output files  
- ✅ Update this skill's own files
- ✅ Create and organize directories
- ✅ Self-edit when you request changes

**Without filesystem MCP, this skill cannot access your files.**

### When This Skill Uses Filesystem Access

**Common operations this skill performs:**

[Customize based on skill - examples:]
- 📖 **Reading files**: [Describe what files this skill reads]
- 📝 **Writing files**: [Describe what files this skill creates]
- 📁 **Directory access**: [Describe what directories this skill uses]
- 🔄 **Self-updating**: Can modify its own SKILL.md when you request changes

### Filesystem MCP Tools This Skill Uses

| Tool | Purpose in This Skill |
|------|----------------------|
| `filesystem:read_text_file` | Read input files, read this SKILL.md for updates |
| `filesystem:write_file` | Create output files, update this skill |
| `filesystem:list_directory` | Browse directories for files |
| `filesystem:create_directory` | Organize output into folders |
| `filesystem:edit_file` | Make targeted updates to this skill |

### Self-Editing Capability

**This skill can update itself!**

You can ask:
- "Add a new example to this skill"
- "Update the procedure section"
- "Fix that typo in the instructions"
- "Add a new guardrail"

**What happens:**
1. Claude reads the current SKILL.md using `filesystem:read_text_file`
2. Makes requested changes using `filesystem:edit_file` or `filesystem:write_file`
3. Recreates the ZIP file
4. Reminds you to upload the new ZIP to claude.ai

### Path Rules for This Skill

**All file operations use absolute paths:**
- ✅ `/Users/yourname/Documents/input.txt`
- ✅ `/Users/yourname/output/report.md`
- ❌ `~/Documents/input.txt` (may not expand correctly)
- ❌ `./output/report.md` (relative paths fail)
- ❌ `/home/claude/temp.txt` (container - doesn't persist)

### If You See Filesystem Errors

**Error: "unknown tool: filesystem:read_text_file"**

This means filesystem MCP is not installed. To fix:

1. Open Claude Desktop config:
   - macOS/Linux: `~/.config/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. Add this configuration:
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

3. Replace `/Users/YOUR_USERNAME` with your actual home directory
4. Restart Claude Desktop
5. Try again

**Official docs**: https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem

### Important Notes

- ✅ **Always asks before modifying files** outside the skill directory
- ✅ **Never creates files in /home/claude/** (temporary container)
- ✅ **Uses your real filesystem** with persistent files
- ✅ **Can update itself** when you request changes
- ⚠️ **Requires filesystem MCP to be installed** to function

---

**Remember**: Filesystem MCP is this skill's "mother" - it needs it to work properly!
```

**Step 2: Create examples (if user provided any)**

Tool: `filesystem:write_file(
  path="{SKILLS_DIR}/{skill-slug}/examples/example-1-name.md",
  content="[example content]"
)`

**Step 3: Create UPDATING.md**

Tool: `filesystem:write_file(
  path="{SKILLS_DIR}/{skill-slug}/UPDATING.md",
  content="[updating instructions]"
)`

**Step 4: Create API deployment scripts**

Tool: `filesystem:write_file(
  path="{SKILLS_DIR}/{skill-slug}/deploy-to-api.sh",
  content="#!/bin/bash
[deployment script content]"
)`

Tool: `filesystem:write_file(
  path="{SKILLS_DIR}/{skill-slug}/deploy-to-api.py",
  content="#!/usr/bin/env python3
[deployment script content]"
)`

**Step 5: Make scripts executable (bash OK for this)**

bash_tool: `chmod +x {SKILLS_DIR}/{skill-slug}/deploy-to-api.sh`
bash_tool: `chmod +x {SKILLS_DIR}/{skill-slug}/deploy-to-api.py`

**Step 6: Verify all files created**

Tool: `filesystem:directory_tree(path="{SKILLS_DIR}/{skill-slug}/")`

Expected output:
```
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

[Use existing ZIP creation logic with MCP or Python fallback]

**Step 8: Git pre-commit hook setup** (if git repo exists)

[Use existing git hook setup logic]

**Step 9: Claude Code symlink** (if enabled in Phase 0.5)

[Use existing Claude Code symlink logic]

**Step 10: API deployment scripts** (already created in Step 4)

**Step 11: Git initialization** (optional - ask user)

[Use existing git initialization logic]

**🚨 CRITICAL REMINDER:**
- NEVER use `create_file` - it goes to container
- ALWAYS use `filesystem:write_file` with absolute paths
- ALWAYS verify with `filesystem:directory_tree` after creation

### Phase 6: Packaging & Deployment
1. Use `python -m code.cli pack` to create ZIP (if CLI tool available)
2. Provide upload instructions per platform:
   - **claude.ai**: Settings → Capabilities → Upload skill
   - **API**: POST to /v1/skills endpoint
   - **Claude Code**: Install to ~/.claude/skills/ or .claude/skills/

**Platform-Specific Notes:**
- claude.ai: Individual user, requires Pro/Max/Team/Enterprise
- API: Organization-wide, requires beta headers
- Claude Code: Filesystem-based, plugin or manual install

### Phase 7: Testing & Iteration
1. Test with example triggers
2. Try on Haiku, Sonnet, and Opus (if possible)
3. Observe Claude's usage patterns
4. Iterate based on feedback
5. Reference MASTER_KNOWLEDGE.md - Development Best Practices

## Updating Existing Skills

When the user wants to modify, fix, or improve an existing skill:

### Update Procedure

**CRITICAL: Use filesystem MCP for all read/write operations.**

**Step 1: Locate the skill**

Tool: `filesystem:list_directory(path="{SKILLS_DIR}")`

Look for skill directory matching requested name

**Step 2: Read existing SKILL.md**

Tool: `filesystem:read_text_file(path="{SKILLS_DIR}/{skill-slug}/SKILL.md")`

Parse the content to understand current structure

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

### Changes That Require ZIP Recreation
- ✅ **ANY change to SKILL.md** - Procedure updates, wording fixes, new sections
- ✅ **ANY change to examples/** - New examples, editing existing examples
- ✅ **ANY change to references/** - Updated guides, new reference files
- ✅ **ANY change to code/** - Script fixes, new helper scripts
- ✅ **Even tiny typo fixes** - ALL changes need new ZIP

### Update Output Format

```markdown
# Skill Update Report

## Changes Made
- [List specific changes made]
- [Files modified]
- [New files added]

## Updated ZIP File
✅ **`skill-name.zip` has been recreated with all changes**

## 🔴 CRITICAL: Upload Required
**Your changes will NOT take effect until you upload the new ZIP file!**

### To Apply Changes:
1. Go to Settings → Capabilities in claude.ai
2. Remove the old version of this skill
3. Click "Upload skill"
4. Select the NEW `skill-name.zip` file
5. Test the updated skill

**The skill files on disk ≠ the skill Claude Desktop is using**

Changes are only applied when you upload the new ZIP file.
```

## Error Handling

### If filesystem MCP not available:

```
❌ **FILESYSTEM MCP NOT AVAILABLE**

I cannot create skills without filesystem MCP. The files would only exist
temporarily in /home/claude/ and disappear when this session ends.

Please install filesystem MCP (see installation guide above) and try again.

I cannot proceed with skill creation.
```

### If target directory doesn't exist:

```
❌ **ERROR: Skills directory not found**

Expected location: {SKILLS_DIR}
This directory doesn't exist or isn't accessible.

Please:
1. Create the directory: {SKILLS_DIR}
2. Ensure filesystem MCP has access to your home directory
3. Try again

Cannot proceed with skill creation.
```

### If skill already exists (for new skill creation):

```
⚠️ **SKILL ALREADY EXISTS**

A skill with this name already exists at:
{SKILLS_DIR}/{skill-slug}/

Options:
1. Update the existing skill (I'll modify the current files)
2. Create with a different name (e.g., {skill-slug}-v2)
3. Cancel

Which would you like to do?
```

## Output Format

# Skill Creation Report

## Skill Specification
**Name**: [Skill name]  
**Description**: [Full description]  
**Platform**: claude.ai | API | Claude Code | All  
**Location**: `{SKILLS_DIR}/{skill-slug}/`
**Claude Code**: ✅ Symlink created at `~/.claude/skills/{skill-slug}/` (if integration enabled) | ❌ Not enabled

## Generated Files
```
skill-name/
├── SKILL.md
├── skill-name.zip ⭐ (ready to upload)
├── UPDATING.md ⭐ (critical reminder)
├── .git/ ⭐ (git repository - if enabled)
│   └── hooks/pre-commit ⭐ (auto-rebuild hook)
├── deploy-to-api.sh ⭐ (API deployment - bash)
├── deploy-to-api.py ⭐ (API deployment - python)
├── [other files]
```

**ZIP File**: `skill-name.zip` has been automatically created and is ready to upload to claude.ai

**Git Repository**: ✅ Initialized with initial commit (if user enabled) | ⏭️  Skipped (user can initialize later)

**Git Hook**: Pre-commit hook has been set up (if git repo exists) - ZIP will auto-rebuild on every commit

**API Scripts**: Deployment scripts created - ready to deploy to Anthropic API

## Validation Results
### ✅ Passed
- [Validation checks that passed]

### ⚠️ Warnings
- [Best practice suggestions]

### ❌ Errors (if any)
- [Issues that must be fixed]

## Deployment Instructions

### For claude.ai
1. Go to Settings → Capabilities
2. Enable "Code execution and file creation"
3. Click "Upload skill"
4. Select the generated ZIP file: `skill-name.zip`

### For API

**Skills created by skills-builder include ready-to-run API deployment scripts!**

#### Option 1: Use Deployment Scripts (Easiest)

**Bash script:**
```bash
cd ~/skills/skill-name/
export ANTHROPIC_API_KEY='your-api-key-here'
./deploy-to-api.sh
```

**Python script:**
```bash
cd ~/skills/skill-name/
export ANTHROPIC_API_KEY='your-api-key-here'
python3 deploy-to-api.py
```

**Get your API key:** https://console.anthropic.com

#### Option 2: Manual curl Command

If you prefer manual deployment:
```bash
curl -X POST https://api.anthropic.com/v1/skills \
  -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02,files-api-2025-04-14" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -F "skill_files=@skill-name.zip"
```

**Important Notes:**
- API deployment makes skills **organization-wide** (all team members get access)
- Save the `skill_id` from the response for future updates
- Skills deployed via API don't need manual upload to Claude Desktop/Code

### For Claude Code

**If you enabled Claude Code integration during creation:**
✅ **Already done!** Symlink created automatically at `~/.claude/skills/skill-name/`

**If you didn't enable it, or want to add it manually:**
```bash
# Option 1: Symlink (recommended - keeps files in sync)
ln -s ~/skills/skill-name ~/.claude/skills/skill-name

# Option 2: Copy (if symlinks don't work on your system)
cp -r ~/skills/skill-name/ ~/.claude/skills/
```

**Note:** With symlink, updates to `~/skills/skill-name/` automatically work in Claude Code!

## Testing
Try these example triggers:
- [Trigger 1]
- [Trigger 2]
- [Trigger 3]

## Next Steps
1. **Upload the ZIP file to claude.ai** (Settings → Capabilities → Upload skill)
2. Test with real tasks
3. Observe Claude's usage
4. Iterate based on feedback
5. Share with team (if applicable)

## Advanced Features Used
- [ ] Progressive disclosure (reference files)
- [ ] Code execution (helper scripts)
- [ ] Validation feedback loops
- [ ] MCP tool integration
- [ ] Visual analysis

## Example Triggers
- "Build a skill for [specific task]"
- "Create a custom skill that [does something]"
- "Help me build a skill for my [workflow]"
- **"Update the [skill-name] skill to add/fix [something]"**
- **"Fix a typo in the synopsis skill"**
- **"Add a new example to the [skill-name] skill"**
- "Validate my skill spec"
- "Package my skill for upload"
- "How should I structure a skill for [use case]?"

## Safety & Confidentiality
- Redact PII from generated files unless required for skill function
- Audit any executable scripts for security issues
- Warn about time-sensitive content that will become outdated
- Flag potential network access (not allowed in Skills)
- Ensure scripts have explicit error handling (don't punt to Claude)

## Reference Materials

When building skills, always consult:
- `MASTER_KNOWLEDGE.md` - Complete technical reference
- `CLAUDE_BEST_PRACTICES.md` - Official guidelines
- `examples/best-practices/` - Production-ready example
- `code/detect_skills_dir.py` - Dynamic path detection helper

## ZIP Creator MCP Integration

### What is the ZIP Creator MCP?
The `zip-creator` MCP server provides a tool (`zip-creator:create_zip`) that simplifies ZIP file creation for Skills. It's optional but recommended for faster, more reliable packaging.

### Benefits
- **Faster**: Direct tool call vs running Python script
- **Simpler**: Single function call with clear parameters
- **Reliable**: Handles edge cases and provides detailed feedback
- **Better UX**: Returns structured response with file count

### Fallback Behavior
The skills-builder ALWAYS works even without the MCP:
1. **Try MCP first**: Attempt `zip-creator:create_zip` tool call
2. **Detect failure**: Check for "unknown tool" or tool unavailable error
3. **Fall back**: Automatically run Python script via bash_tool
4. **User transparency**: Mention which method was used

## Common Patterns

### Pattern 1: Simple Task Skill
Just SKILL.md with clear procedure. Good for straightforward tasks.

### Pattern 2: Progressive Disclosure Skill
SKILL.md + reference files. For skills with optional complexity.

### Pattern 3: Code Execution Skill
SKILL.md + scripts in code/. For deterministic operations.

### Pattern 4: Validation Feedback Loop Skill
Plan → Validate → Execute → Verify. For error-prone complex tasks.

### Pattern 5: Multi-Domain Skill
SKILL.md + domain-specific reference files. Prevents loading irrelevant context.

### Pattern 6: MCP Integration Skill
Teaches Claude how to use MCP tools effectively.

## Critical Requirements Checklist

Before finalizing any skill:
- [ ] Name is ≤ 64 chars
- [ ] **Name is lowercase-with-hyphens-only (e.g., 'processing-pdfs')**
- [ ] **Name does NOT contain 'claude', 'anthropic', or 'ai'**
- [ ] **ALL folder names are lowercase (examples/, references/, code/)**
- [ ] **ALL filenames are lowercase-with-hyphens (except SKILL.md, README.md)**
- [ ] **NO capital letters in filenames (SYNOPSIS.md ❌, synopsis.md ✅)**
- [ ] **NO underscores or spaces in filenames**
- [ ] Spec uses gerund form for display ("Processing PDFs")
- [ ] Description is ≤ 1024 chars, includes WHAT + WHEN
- [ ] At least 2 triggers defined
- [ ] All file paths use forward slashes
- [ ] SKILL.md is under 500 lines
- [ ] No time-sensitive content
- [ ] No network access in scripts
- [ ] Only pre-installed packages used
- [ ] Proper error handling in scripts
- [ ] Security audit passed
- [ ] Tested on multiple models (if possible)
- [ ] Works on target platform(s)
- [ ] **Created in {SKILLS_DIR} (dynamically detected) using filesystem MCP**
- [ ] **ZIP file created and tested**
- [ ] **UPDATING.md file included**
- [ ] **Claude Code symlink created (if user enabled integration)**
- [ ] **Git repository initialized (if user enabled version control)**
- [ ] **API deployment scripts created (deploy-to-api.sh and deploy-to-api.py)**
- [ ] **Generated skill includes "Filesystem MCP - Your Mother MCP" section**

## Platform Compatibility Matrix

| Feature | claude.ai | API | Claude Code |
|---------|-----------|-----|-------------|
| Pre-built Skills | ✅ | ✅ | ✅ |
| Custom Skills | ✅ | ✅ | ✅ |
| Sharing | Individual | Org-wide | Project/Personal |
| Upload Method | ZIP via UI | API endpoint | Filesystem |
| Code Execution | ✅ | ✅ | ✅ |
| Network Access | ❌ | ❌ | ❌ |

## When to Use Each Pattern

**Simple SKILL.md only:**
- Task is straightforward
- No conditional complexity
- Minimal reference materials
- Under 500 lines total

**Progressive disclosure (reference files):**
- Multiple domains or contexts
- Optional advanced features
- Large reference materials
- Content rarely used together

**Code execution (scripts):**
- Deterministic operations needed
- Complex algorithms
- Validation requirements
- Better reliability than generation

**Feedback loops (validation):**
- Error-prone tasks
- Multiple steps
- Quality critical
- Need verification

## Remember

Skills are like **onboarding guides for Claude**:
- Progressive disclosure (table of contents → chapters → appendices)
- Code executes without loading into context
- Platform differences matter
- Security is critical
- Best practices improve quality
- **ALWAYS detect skills directory dynamically using Phase 0 method**
- **Use filesystem MCP to create files in {SKILLS_DIR} (detected path)**
- **Validate paths before starting**
- **Provide clear error messages**
- **Create ZIP files automatically**
- **NEVER use container tools (create_file, str_replace, view for writing)**
- **ALWAYS use filesystem MCP tools for ALL file operations**
- **Every generated skill inherits filesystem MCP knowledge**

**This skill builds production-ready Skills that work on ANY user's filesystem, detecting paths dynamically rather than using hardcoded locations, and ensuring all child skills know to use filesystem MCP as their "mother MCP".**
