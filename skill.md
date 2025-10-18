---
name: Building Claude Skills
description: Creates world-class Claude Skills following Anthropic's official specifications and best practices. Use when building custom Skills for claude.ai, Claude Code, or the API - handles validation, generation, and packaging.
---

# Building Claude Skills

A comprehensive skill-builder that creates production-ready Claude Skills following all official Anthropic guidelines.

## When to Use
- User wants to create a new Claude Skill
- User says "build a skill", "create a skill", "make a skill"
- User wants to validate or improve an existing skill
- User needs to package a skill for upload
- User asks about Skills best practices or architecture

## Inputs
- User's description of what the skill should do
- Workflow/procedures the skill should follow
- Optional: existing skill.spec.json file
- Optional: reference materials to include
- Optional: scripts or code to bundle

## Ground Rules
- Follow ALL Anthropic specifications (64-char names, 1024-char descriptions)
- Use gerund form for skill names ("Processing PDFs" not "PDF Processor")
- Descriptions must include WHAT it does AND WHEN to use it
- Always use forward slashes in paths (never backslashes)
- Keep SKILL.md under 500 lines (use progressive disclosure for more)
- No network access in scripts (Skills run in sandboxed environment)
- Only use pre-installed packages (no runtime installation)
- Validate against security best practices
- Generate skills that work on claude.ai, API, AND Claude Code

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

## Procedure

### Phase 1: Discovery & Specification
1. Ask user what the skill should do (be specific)
2. Identify the workflow/procedure the skill follows
3. Determine inputs the skill needs
4. Establish guardrails and constraints
5. Define expected output format
6. Identify any reference materials or scripts needed

**Key Questions:**
- What specific task does this skill perform?
- When should Claude use this skill? (triggers)
- What inputs does it need? (files, parameters, context)
- What rules must it follow? (guardrails)
- What's the step-by-step procedure?
- What should the output look like?
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
- Name ≤ 64 characters, uses gerund form?
- Description ≤ 1024 characters, includes WHAT + WHEN?
- At least 2 triggers defined?
- All required fields present?
- File paths use forward slashes?
- No time-sensitive content?
- MCP tools properly formatted (ServerName:tool_name)?

### Phase 3: Structure & Organization
1. Determine if progressive disclosure needed (>500 lines?)
2. Organize reference files by domain/purpose
3. Plan code execution strategy (scripts vs generation)
4. Design validation/feedback loops if needed
5. Reference MASTER_KNOWLEDGE.md - Progressive Disclosure section

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

### Phase 5: Generation
1. Use `python -m code.cli new` to generate skill
2. Verify all files created correctly
3. Check SKILL.md length (<500 lines recommended)
4. Validate generated content

**Generated Structure:**
```
skill-name/
├── SKILL.md (with YAML frontmatter)
├── templates/ (if output contract includes templates)
├── reference/ (if progressive disclosure used)
├── code/ (if code helper enabled)
└── README.md
```

### Phase 6: Packaging & Deployment
1. Use `python -m code.cli pack` to create ZIP
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

## Output Format

# Skill Creation Report

## Skill Specification
**Name**: [Skill name]  
**Description**: [Full description]  
**Platform**: claude.ai | API | Claude Code | All

## Generated Files
```
skill-name/
├── SKILL.md
├── [other files]
```

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
4. Select the generated ZIP file

### For API
```bash
curl -X POST https://api.anthropic.com/v1/skills \
  -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02,files-api-2025-04-14" \
  -F "skill_files=@skill-name.zip"
```

### For Claude Code
```bash
cp -r skill-name/ ~/.claude/skills/
```

## Testing
Try these example triggers:
- [Trigger 1]
- [Trigger 2]
- [Trigger 3]

## Next Steps
1. Test with real tasks
2. Observe Claude's usage
3. Iterate based on feedback
4. Share with team (if applicable)

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
- [ ] Name is ≤ 64 chars, gerund form
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

**This skill builds production-ready Skills that kick ass across all platforms.**
