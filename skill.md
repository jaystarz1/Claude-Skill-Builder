---
name: skills-builder
description: Creates world-class agent Skills following Anthropic's official specifications and best practices. Use when building custom Skills for web, desktop, or API - handles validation, generation, and packaging.
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
- ✅ Using filesystem MCP tools as primary method
- ✅ After validating directory exists and is accessible

**Before starting ANY skill creation:**
1. **DETECT SKILLS DIRECTORY** using method above - store as `{SKILLS_DIR}`
2. Call `filesystem:list_directory` on `{SKILLS_DIR}`
3. If this fails, STOP and report error to user
4. If this succeeds, proceed with skill creation IN THIS DIRECTORY

### Tool Selection Priority

**PRIMARY (Always try first):**
- `filesystem:create_directory` - Create skill folder structure
- `filesystem:write_file` - Create SKILL.md, skill.spec.json, examples, etc.
- `filesystem:list_directory` - Verify structure and check existing files
- `filesystem:directory_tree` - Display final structure
- `filesystem:read_text_file` - Read existing skill files when updating

**FALLBACK (Only if filesystem MCP unavailable):**
- `create_file` / `bash_tool` - Create in `/home/claude/`
- **MUST** display clear instructions to user on how to move files to actual filesystem

**Detection Strategy:**
1. Try filesystem MCP tool first
2. If error contains "unknown tool" or "not found", filesystem MCP is unavailable
3. Automatically fall back with clear warning to user

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

**Before creating or updating any skill, ALWAYS run these checks:**

1. **DETECT SKILLS DIRECTORY (NEW - MOST CRITICAL STEP):**
   ```python
   import os
   from pathlib import Path
   
   # Try environment variable
   env_skills_dir = os.getenv('SKILLS_DIR')
   if env_skills_dir:
       SKILLS_DIR = Path(env_skills_dir).expanduser().resolve()
   else:
       # Use ~/skills/
       SKILLS_DIR = Path.home() / 'skills'
   
   # Create if doesn't exist
   if not SKILLS_DIR.exists():
       SKILLS_DIR.mkdir(parents=True, exist_ok=True)
       # Inform user: "Created skills directory at {SKILLS_DIR}"
   ```
   
   **Store the detected path in `SKILLS_DIR` variable and use it for ALL subsequent operations.**

2. **Validate skills directory is accessible:**
   ```
   filesystem:list_directory(path="{SKILLS_DIR}")
   ```
   - If this succeeds: ✅ Proceed to next step
   - If this fails: ❌ STOP - Show error to user (see Error Handling section)

3. **Check if filesystem MCP is available:**
   - Try the `filesystem:list_directory` call above
   - If successful: ✅ Use filesystem MCP for all file operations
   - If error contains "unknown tool": ⚠️ Fall back to bash tools with warning

4. **Determine skill slug:**
   - Convert user's skill name to lowercase-with-hyphens
   - Remove any forbidden words ('claude', 'anthropic', 'ai')
   - Validate name is ≤ 64 characters

5. **Check if skill already exists (for new skills):**
   ```
   filesystem:list_directory(path="{SKILLS_DIR}")
   ```
   - Look for directory matching skill slug
   - If exists: Ask user if they want to update or create new version
   - If not exists: ✅ Proceed with creation

6. **Confirm target path:**
   - Display to user: "Creating skill at: `{SKILLS_DIR}/{skill-slug}/`"
   - Get user confirmation before proceeding

**Only after ALL checks pass, proceed to Phase 1.**

**Example Path Detection Output:**
```
✅ Detected skills directory: /Users/alice/skills/
✅ Creating skill at: /Users/alice/skills/weather-forecast/
```

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

**CRITICAL: Use filesystem MCP for all operations with dynamically detected {SKILLS_DIR}**

1. **Create base directory structure** using filesystem MCP:
   ```
   filesystem:create_directory(path="{SKILLS_DIR}/{skill-slug}/")
   ```

2. **If user provided examples: CREATE examples/ folder** and save each example:
   ```
   filesystem:create_directory(path="{SKILLS_DIR}/{skill-slug}/examples/")
   filesystem:write_file(
     path="{SKILLS_DIR}/{skill-slug}/examples/example-1-[name].md",
     content="[example content]"
   )
   ```

3. Determine if progressive disclosure needed (>500 lines?)

4. Organize reference files by domain/purpose:
   ```
   filesystem:create_directory(path="{SKILLS_DIR}/{skill-slug}/references/")
   ```

5. Plan code execution strategy (scripts vs generation):
   ```
   filesystem:create_directory(path="{SKILLS_DIR}/{skill-slug}/code/")
   ```

6. Design validation/feedback loops if needed

7. Reference MASTER_KNOWLEDGE.md - Progressive Disclosure section

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

**CRITICAL: All file operations use filesystem MCP with absolute paths using {SKILLS_DIR}**

1. **Create SKILL.md** using filesystem MCP:
   ```
   filesystem:write_file(
     path="{SKILLS_DIR}/{skill-slug}/SKILL.md",
     content="[skill content with YAML frontmatter]"
   )
   ```

2. **If examples were provided: Save them to examples/ folder:**
   ```
   filesystem:write_file(
     path="{SKILLS_DIR}/{skill-slug}/examples/example-1-[name].md",
     content="[example content]"
   )
   ```

3. **Create UPDATING.md file** - Critical reminder about ZIP recreation:
   ```
   filesystem:write_file(
     path="{SKILLS_DIR}/{skill-slug}/UPDATING.md",
     content="[updating instructions - see template below]"
   )
   ```

4. **Verify all files created correctly:**
   ```
   filesystem:directory_tree(path="{SKILLS_DIR}/{skill-slug}/")
   ```

5. Check SKILL.md length (<500 lines recommended)

6. **Verify examples/ folder exists and contains all provided examples**

7. **AUTOMATICALLY CREATE ZIP FILE** - Package the skill immediately after generation

8. **AUTOMATICALLY SET UP GIT PRE-COMMIT HOOK** (if git repo exists) - Auto-rebuild ZIP on every commit

**ZIP File Creation:**
After creating all skill files, automatically create a ZIP file using one of these methods:

**CRITICAL: ZIP Filename Must Match Folder Name**
The ZIP filename MUST match the skill's folder/directory name + `.zip`
- If folder is `skills-builder/` → ZIP is `skills-builder.zip`
- If folder is `generic-synopsis-skill/` → ZIP is `generic-synopsis-skill.zip`
- NEVER use descriptive names like "skills-builder-v2" or "updated-skill"
- This ensures only ONE ZIP file exists per skill (overwrites previous)

**Method 1: MCP Tool (Preferred)**
If the `zip-creator:create_zip` MCP tool is available, use it:
```
zip-creator:create_zip(
  directory_path='{SKILLS_DIR}/{skill-slug}',
  zip_name='{skill-slug}.zip'
)
```

**Method 2: Python Script (Fallback)**
If the MCP tool is not available, use this Python script via bash_tool:
```python
import zipfile
from pathlib import Path

skill_dir = Path('{SKILLS_DIR}/{skill-slug}')
zip_name = '{skill-slug}.zip'

with zipfile.ZipFile(str(skill_dir / zip_name), 'w', zipfile.ZIP_DEFLATED) as zipf:
    for file_path in skill_dir.rglob('*'):
        if file_path.is_file() and '.git' not in str(file_path) and not str(file_path).endswith('.zip'):
            # CRITICAL: Exclude dist/ folder to avoid multiple SKILL.md files
            if 'dist' not in file_path.parts:
                arcname = file_path.relative_to(skill_dir)
                zipf.write(file_path, arcname)

print(f'✅ Created {zip_name}')
```

**Detection Logic:**
Try Method 1 first. If the tool call fails with "unknown tool" error, automatically fall back to Method 2.

**CRITICAL ZIP RULES:**
- ⚠️ **Exactly ONE SKILL.md file** - Claude will reject ZIPs with multiple SKILL.md files
- ⚠️ **Exclude dist/ folder** - Contains generated skills that would create duplicates
- ⚠️ **Exclude .git/ folder** - Version control not needed in uploaded skills
- ⚠️ **Exclude existing .zip files** - Avoid zip-in-zip situations

**Git Pre-Commit Hook Setup:**
After creating the ZIP file, check if the skill directory is a git repository and set up auto-rebuild:

1. **Check for git repo:**
   ```
   filesystem:list_directory(path="{SKILLS_DIR}/{skill-slug}/.git/")
   ```

2. **If git repo exists, create hooks directory:**
   ```
   filesystem:create_directory(path="{SKILLS_DIR}/{skill-slug}/.git/hooks/")
   ```

3. **Write pre-commit hook:**
   ```
   filesystem:write_file(
     path="{SKILLS_DIR}/{skill-slug}/.git/hooks/pre-commit",
     content="[hook script - see template below]"
   )
   ```

4. **Make executable via bash:**
   ```
   bash_tool: chmod +x {SKILLS_DIR}/{skill-slug}/.git/hooks/pre-commit
   ```

**Hook Template:**
```bash
#!/bin/bash
# Auto-rebuild ZIP file when committing changes to skill files

cd "$(git rev-parse --show-toplevel)"

echo "Rebuilding {skill-slug}.zip..."
zip -r {skill-slug}.zip . -x "*.git*" -x "*.claude*" -x "__MACOSX*" -x "*.DS_Store" -q

# Add the updated ZIP to this commit
git add {skill-slug}.zip

echo "ZIP file updated and staged for commit"
```

**Benefits:**
- ✅ ZIP automatically rebuilds on every `git commit`
- ✅ Always stays in sync with skill files
- ✅ No manual ZIP recreation needed during development
- ✅ ZIP gets committed alongside file changes

**Generated Structure:**
```
skill-name/
├── SKILL.md (with YAML frontmatter)
├── skill-name.zip ⭐ (AUTOMATICALLY CREATED)
├── UPDATING.md ⭐ (CRITICAL REMINDER)
├── .git/hooks/pre-commit ⭐ (AUTO-REBUILD HOOK - if git repo)
├── examples/ (CRITICAL: if user provided examples)
│   ├── README.md (explains what each example shows)
│   ├── example-1-[descriptive-name].md
│   ├── example-2-[descriptive-name].md
│   └── example-N-[descriptive-name].md
├── templates/ (if output contract includes templates)
├── reference/ (if progressive disclosure used)
├── code/ (if code helper enabled)
└── README.md
```

**UPDATING.md File:**
Every skill MUST include an UPDATING.md file with this content:
```markdown
# 🔴 UPDATING THIS SKILL

## CRITICAL: Changes Require New ZIP Upload

If you modify ANY file in this skill, you MUST:

1. **Recreate the ZIP file**
2. **Upload the new ZIP to claude.ai**

### Why?
The skill files on disk ≠ the skill Claude is using.
Claude loads skills from uploaded ZIP files, not from your filesystem.

### When to Create New ZIP?
- ✅ Changed SKILL.md (even typos)
- ✅ Modified examples/
- ✅ Updated references/
- ✅ Fixed code/
- ✅ ANY file change at all

### How to Recreate ZIP

#### Option 1: Git Commit (Automatic - If Git Hook Is Set Up)
If this skill has a git pre-commit hook installed, the ZIP rebuilds automatically:
```bash
git add .
git commit -m "Your commit message"
```
The hook will automatically rebuild the ZIP and add it to your commit. **No manual ZIP creation needed!**

#### Option 2: Ask Claude (Easiest - Uses MCP if Available)
```
"Create a new ZIP for this skill"
```

Claude will automatically use the zip-creator MCP tool if it's installed, or fall back to a Python script.

#### Option 3: MCP Tool Directly (If Installed)
```
zip-creator:create_zip(
  directory_path='/absolute/path/to/skill',
  zip_name='skill-name.zip'
)
```

#### Option 4: Python Script (Always Works)
```bash
python3 << 'EOF'
import zipfile
from pathlib import Path

skill_dir = Path('.')
zip_name = '[skill-name].zip'

with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for file_path in skill_dir.rglob('*'):
        if file_path.is_file() and '.git' not in str(file_path) and not str(file_path).endswith('.zip'):
            # Exclude dist/ folder if it exists (for skills that generate other skills)
            if 'dist' not in file_path.parts:
                arcname = file_path.relative_to(skill_dir)
                zipf.write(file_path, arcname)

print(f'Created: {zip_name}')
EOF
```

### How to Upload

1. Go to Settings → Capabilities in claude.ai
2. Remove old version of this skill
3. Click "Upload skill"
4. Select the NEW ZIP file
5. Test your changes

**Changes take effect immediately after upload.**
```

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

**CRITICAL: Use filesystem MCP for all read/write operations with {SKILLS_DIR}**

1. **Run pre-flight validation** (Phase 0):
   - DETECT SKILLS DIRECTORY → store as `{SKILLS_DIR}`
   - Verify `{SKILLS_DIR}` exists and is accessible
   - Check filesystem MCP availability
   - Locate skill directory

2. **Identify what needs to change** - Ask user for specific changes needed

3. **Read existing skill files:**
   ```
   filesystem:read_text_file(path="{SKILLS_DIR}/{skill-slug}/SKILL.md")
   ```

4. **Make the requested changes** using filesystem MCP:
   ```
   filesystem:write_file(
     path="{SKILLS_DIR}/{skill-slug}/SKILL.md",
     content="[updated content]"
   )
   ```

5. **AUTOMATICALLY RECREATE ZIP FILE** - Always create fresh ZIP after any changes

6. **Remind user to upload new ZIP** - Changes won't take effect until uploaded

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
⚠️ **FILESYSTEM MCP NOT DETECTED**

I'll create the skill in a temporary location, but you'll need to move it manually:

Temporary location: /home/claude/{skill-name}/
Target location: {SKILLS_DIR}/{skill-name}/

After I finish, please:
1. Copy all files from the temporary location
2. Paste them into {SKILLS_DIR}/{skill-name}/
3. Verify the structure is correct

Proceeding with creation...
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

## Generated Files
```
skill-name/
├── SKILL.md
├── skill-name.zip ⭐ (ready to upload)
├── UPDATING.md ⭐ (critical reminder)
├── .git/hooks/pre-commit ⭐ (auto-rebuild hook - if git repo)
├── [other files]
```

**ZIP File**: `skill-name.zip` has been automatically created and is ready to upload to claude.ai

**Git Hook**: Pre-commit hook has been set up (if git repo exists) - ZIP will auto-rebuild on every commit

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
```bash
curl -X POST https://api.anthropic.com/v1/skills \
  -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02,files-api-2025-04-14" \
  -F "skill_files=@skill-name.zip"
```

### For Claude Code
```bash
cp -r {SKILLS_DIR}/skill-name/ ~/.claude/skills/
```

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

### Installation (Optional)
Users can install the zip-creator MCP server to enable automatic ZIP creation:

**Location**: `~/mcp-servers/zip-creator/`

**Files needed**:
- `server.py` - MCP server implementation
- `README.md` - Installation and usage guide
- `INSTALL.md` - Detailed setup instructions

**Config** (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "zip-creator": {
      "command": "/opt/homebrew/bin/python3.11",
      "args": [
        "-m",
        "mcp.server.stdio",
        "~/mcp-servers/zip-creator/server.py"
      ]
    }
  }
}
```

### Fallback Behavior
The skills-builder ALWAYS works even without the MCP:
1. **Try MCP first**: Attempt `zip-creator:create_zip` tool call
2. **Detect failure**: Check for "unknown tool" or tool unavailable error
3. **Fall back**: Automatically run Python script via bash_tool
4. **User transparency**: Mention which method was used

### For Skill Users
- **With MCP**: Just say "Create a ZIP for this skill" - instant, reliable
- **Without MCP**: Same command works, just uses Python fallback
- **No action needed**: The fallback is automatic and transparent

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

**This skill builds production-ready Skills that work on ANY user's filesystem, detecting paths dynamically rather than using hardcoded locations.**
