# Skills Builder - Complete Master Knowledge Base

This document contains EVERYTHING the skills-builder needs to know to create world-class Claude Skills. This knowledge comes from Anthropic's official documentation, engineering blog, and support materials.

---

## Table of Contents
1. [What Skills Are (Core Concept)](#what-skills-are)
2. [How Skills Work (Technical Architecture)](#how-skills-work)
3. [Progressive Disclosure (The Secret Sauce)](#progressive-disclosure)
4. [Skills Across Platforms](#skills-across-platforms)
5. [The Anatomy of a Skill](#anatomy-of-a-skill)
6. [Security & Trust Model](#security-trust-model)
7. [Development Best Practices](#development-best-practices)
8. [API & Integration](#api-integration)
9. [Limitations & Constraints](#limitations-constraints)
10. [Advanced Patterns](#advanced-patterns)

---

## What Skills Are

### Definition
**Skills are folders of instructions, scripts, and resources that Claude loads dynamically to improve performance on specialized tasks.**

Think of Skills as:
- **Onboarding guides for Claude** - Like training materials for a new hire
- **Composable expertise packages** - Modular capabilities that stack together
- **Reusable workflows** - Create once, use everywhere
- **Domain-specific extensions** - Transform general Claude into a specialist

### Core Philosophy
> "Instead of building fragmented, custom-designed agents for each use case, anyone can now specialize their agents with composable capabilities by capturing and sharing their procedural knowledge."
> 
> — Anthropic Engineering Blog

### Key Characteristics
1. **Composable** - Multiple Skills work together seamlessly. Claude identifies and coordinates them automatically
2. **Portable** - Same format works across Claude apps, Claude Code, and API
3. **Efficient** - Only loads what's needed, when needed
4. **Powerful** - Can include executable code for deterministic operations
5. **Dynamic** - Claude determines relevance and loads information on-demand

### Skills vs Other Features

**Skills vs Projects**
- Projects: Static background knowledge, always loaded
- Skills: Dynamic procedures, activate when needed, work everywhere

**Skills vs MCP (Model Context Protocol)**
- MCP: Connects Claude to external services and data
- Skills: Provides procedural knowledge for how to use tools
- **They work together**: MCP gives tools, Skills teach how to use them

**Skills vs Custom Instructions**
- Custom Instructions: Broad, apply to all conversations
- Skills: Task-specific, load only when relevant

**Skills vs RAG (Retrieval Augmented Generation)**
- RAG: Retrieves documents from vector databases
- Skills: Filesystem-based, unbounded context via progressive disclosure
- Skills can contain WAY more context because they're not pre-loaded

**Skills vs Prompt Engineering**
- Prompts: One-time instructions per conversation
- Skills: Reusable capabilities that persist across conversations

---

## How Skills Work

### The Three-Level Loading Architecture

Skills use **progressive disclosure** - information loads in stages as needed:

#### Level 1: Metadata (Always Loaded - ~100 tokens per Skill)
**When**: At agent startup  
**What**: YAML frontmatter from SKILL.md  
**Content**:
```yaml
---
name: Your Skill Name  # Max 64 chars
description: What it does and when to use it  # Max 1024 chars
---
```

**Purpose**: Discovery. Lets Claude know which Skills exist without loading full content.

#### Level 2: Instructions (Loaded When Triggered - <5k tokens)
**When**: Skill is determined relevant to task  
**What**: Main body of SKILL.md  
**Content**: Procedures, workflows, best practices, guidelines  
**How Claude loads it**: `bash: read skill-name/SKILL.md`

#### Level 3+: Resources & Code (Loaded As Needed - Unlimited)
**When**: Specific files/scripts needed  
**What**: Reference materials, data files, executable scripts  
**Content**: API docs, examples, templates, helper scripts  
**How Claude loads it**: 
- Read: `bash: read skill-name/reference/api-docs.md`
- Execute: `bash: python skill-name/code/validator.py`

### The Runtime Environment

Skills run in Claude's **code execution container** with:
- ✅ Filesystem access (read/write files)
- ✅ Bash commands (navigate, execute scripts)
- ✅ Code execution (Python, JavaScript, etc.)
- ❌ **NO network access** (can't make external API calls)
- ❌ **NO runtime package installation** (only pre-installed packages)

**Critical Insight**: Scripts execute WITHOUT loading their code into context. Only the OUTPUT consumes tokens.

Example:
```python
# This 1000-line script in skills/code/analyze.py
# consumes ZERO tokens when executed
# Only its output ("Analysis complete: 5 issues found") uses tokens
```

### Context Window Management

The context window changes dynamically:

**Initial State**:
```
[System Prompt]
[Skill 1 metadata: name + description]
[Skill 2 metadata: name + description]
[Skill N metadata: name + description]
[User Message]
```

**After Skill Trigger**:
```
[System Prompt]
[All Skill metadata]
[User Message]
[Loaded: SKILL.md body]  ← Only what's needed
[Loaded: reference.md]   ← Only if accessed
[Script output]          ← Only if executed
```

### How Claude Decides What to Load

1. **User makes request** → "Extract form fields from this PDF"
2. **Claude scans metadata** → Reviews all skill names/descriptions
3. **Claude identifies relevance** → "PDF Processing" skill matches
4. **Claude loads Level 2** → Reads pdf-skill/SKILL.md
5. **Claude evaluates needs** → Does task need form-filling?
6. **Claude loads Level 3 (maybe)** → If yes, reads FORMS.md
7. **Claude executes code (maybe)** → Runs extract_fields.py if needed

**Key**: Claude is AUTONOMOUS in navigation. It decides what to read and when.

---

## Progressive Disclosure

### The Core Design Principle

> "Progressive disclosure is the core design principle that makes Agent Skills flexible and scalable. Like a well-organized manual that starts with a table of contents, then specific chapters, and finally a detailed appendix, skills let Claude load information only as needed."

### Why It Matters

Traditional approaches force you to choose:
- **Load everything** → Wastes context, slow, expensive
- **Load nothing** → Missing critical info, poor results

Progressive disclosure gives you both:
- **Minimal overhead** → Only metadata loaded by default
- **Unlimited depth** → Access to comprehensive resources on-demand

### Visual Mental Model

Think of Skills like a book:
```
📖 Book Cover (Level 1: Metadata)
   ├─ Table of Contents (Level 2: SKILL.md)
   │  ├─ Chapter 1: Basic Usage
   │  ├─ Chapter 2: Advanced Features
   │  └─ Chapter 3: Troubleshooting
   └─ Appendices (Level 3+: Reference files)
      ├─ Appendix A: API Reference
      ├─ Appendix B: Examples
      └─ Appendix C: Scripts
```

Claude reads the cover, scans the table of contents, then jumps to the exact chapter/appendix needed.

### Practical Implications

1. **No practical limit on bundled content**: Include comprehensive API docs, large datasets, extensive examples - no penalty until accessed

2. **Keep SKILL.md lean**: Point to detailed files, don't include everything inline

3. **Organize for discovery**: Structure directories by domain/feature with descriptive names

4. **One level deep**: Reference files should link directly from SKILL.md, avoid deep nesting

---

## Skills Across Platforms

Skills work everywhere but have different deployment models:

### Claude.ai (Web/Desktop/Mobile)

**Availability**: Pro, Max, Team, Enterprise plans  
**Setup**: Settings → Capabilities → Skills

**Pre-built Skills** (Anthropic-provided):
- Excel (xlsx) - Spreadsheets with formulas
- PowerPoint (pptx) - Presentations  
- Word (docx) - Documents
- PDF (pdf) - Form filling, merging

**Custom Skills**:
- Upload as ZIP files
- **Individual user only** (not shared org-wide)
- Each team member uploads separately
- Requires Code Execution enabled

**Creating Skills**:
- Use "skill-creator" skill (interactive guide)
- No manual file editing required
- Claude asks about workflow and generates structure

### Claude Code

**Availability**: All Claude Code users  
**Setup**: Automatic via plugins or manual installation

**Installation Methods**:

1. **Marketplace** (Recommended):
```bash
# Register anthropics/skills as plugin
# In Claude Code, run marketplace install command
```

2. **Manual**:
```bash
# Personal: ~/.claude/skills/
# Project-based: .claude/skills/
```

**Usage**:
- Just mention the skill: "use the pdf skill to extract form fields from file.pdf"
- Claude loads automatically when relevant
- Share via version control with team

**Pre-built Skills**: Same document skills as claude.ai

### Claude API (Developer Platform)

**Availability**: All API users  
**Setup**: Via /v1/skills endpoints + code execution tool

**Required Beta Headers**:
```http
anthropic-beta: code-execution-2025-08-25,skills-2025-10-02,files-api-2025-04-14
```

**Pre-built Skills** (Anthropic-managed):
- Use `skill_id` in container parameter
- Available: `pptx`, `xlsx`, `docx`, `pdf`

**Custom Skills**:
- Create via `/v1/skills` POST endpoint
- Manage via `/v1/skills` GET/PUT/DELETE
- Organization-wide (all workspace members access)
- Version control through Console

**Integration Pattern**:
```json
{
  "model": "claude-sonnet-4-5-20250929",
  "max_tokens": 4096,
  "tools": [{
    "type": "code_execution",
    "container": {
      "skills": ["skill_id_here"]
    }
  }],
  "messages": [...]
}
```

### Claude Agent SDK

**Availability**: Custom agent builders  
**Integration**: Same Skills support as other platforms  
**Use case**: Building specialized agents with Skills baked in

---

## Anatomy of a Skill

### Required: SKILL.md File

Every skill MUST have a `SKILL.md` file with this structure:

```markdown
---
name: Skill Name Here
description: What it does and when to use it
---

# Main Instructions

[Your procedural knowledge, workflows, guidelines]

## When to Use
- Trigger phrase 1
- Trigger phrase 2

## Procedure
1. Step one
2. Step two
3. Step three

## Output Format
[Expected output structure]

## Safety & Guidelines
[Constraints and rules]
```

### YAML Frontmatter Requirements

```yaml
---
name: Your Skill Name
description: One-line description
---
```

**Only two fields supported**: `name` and `description`

**Limits**:
- `name`: 64 characters maximum
- `description`: 1024 characters maximum

**Best Practices**:
- **Name**: Use gerund form ("Processing PDFs" not "PDF Processor")
- **Description**: Include BOTH what it does AND when to use it
- **Description**: Active voice, no first/second person
- **Description**: Include key terms for discoverability

**Good Examples**:
```yaml
name: Processing PDFs
description: Extracts text and tables from PDF files, fills forms, merges documents. Use when working with PDF documents that require parsing, editing, or generation.
```

**Bad Examples**:
```yaml
name: PDF Helper  # Vague
description: I can help you with PDFs  # First person, vague
```

### Optional: Additional Files

Skills can bundle anything needed:

#### Reference Files (Progressive Disclosure)
```
skill-name/
├── SKILL.md
├── reference/
│   ├── api-docs.md
│   ├── examples.md
│   └── troubleshooting.md
```

**Pattern in SKILL.md**:
```markdown
For detailed API reference, see `reference/api-docs.md`
For common patterns, see `reference/examples.md`
```

#### Executable Scripts
```
skill-name/
├── SKILL.md
├── code/
│   ├── validator.py
│   ├── formatter.py
│   └── analyzer.py
```

**Pattern in SKILL.md**:
```markdown
## Validation
Run `code/validator.py` to validate output
```

#### Data Files
```
skill-name/
├── SKILL.md
├── data/
│   ├── templates/
│   ├── schemas/
│   └── examples/
```

#### Images (for Visual Analysis)
```
skill-name/
├── SKILL.md
├── images/
│   ├── ui-mockup.png
│   └── workflow-diagram.png
```

**Usage**: Claude can analyze images to understand visual context

### Directory Structure Best Practices

**Good** (organized by domain):
```
analyzing-spreadsheets/
├── SKILL.md
├── reference/
│   ├── excel-functions.md
│   ├── data-patterns.md
│   └── visualization-guide.md
├── code/
│   ├── parse_excel.py
│   └── validate_data.py
└── examples/
    └── sample-reports/
```

**Bad** (flat, unclear):
```
spreadsheet-skill/
├── SKILL.md
├── doc1.md
├── doc2.md
├── script.py
├── other-script.py
```

### File Naming Conventions

**Good**:
- `api-reference.md` (descriptive)
- `parse_excel.py` (clear purpose)
- `validation-rules.md` (self-explanatory)

**Bad**:
- `doc1.md` (vague)
- `temp.py` (unclear)
- `stuff.md` (useless)

### File Paths

**CRITICAL**: Always use forward slashes, never backslashes

✅ **Good**: `reference/api-docs.md`, `code/helper.py`  
❌ **Bad**: `reference\api-docs.md`, `code\helper.py`

**Why**: Cross-platform compatibility. Windows-style paths break on other systems.

---

## Security & Trust Model

### The Risk Model

Skills grant Claude new capabilities through:
- **Instructions** - What to do
- **Code execution** - Scripts that run in container
- **File access** - Read/write files in container

**This makes them powerful BUT also means malicious skills can**:
- Direct Claude to misuse tools
- Execute harmful code
- Leak data to external systems (if they bypass restrictions)
- Perform unintended operations

### Anthropic's Official Guidance

> "We strongly recommend using Skills only from trusted sources: those you created yourself or obtained from Anthropic."

### Security Audit Checklist

Before using a skill from external sources:

#### 1. **Read ALL Files**
- ✅ SKILL.md - Review instructions for malicious patterns
- ✅ All scripts - Check for suspicious operations
- ✅ All reference files - Look for hidden instructions
- ✅ All data files - Verify contents are legitimate

#### 2. **Look For Red Flags**
- ❌ Unexpected network calls (shouldn't be possible but check)
- ❌ File access patterns that don't match stated purpose
- ❌ Instructions to fetch data from external URLs
- ❌ Obfuscated or encoded content
- ❌ Operations that don't match skill description

#### 3. **External Dependencies Are High-Risk**
- Skills that fetch data from URLs can be compromised
- Even trustworthy skills can become unsafe if dependencies change
- Prefer skills that bundle all necessary resources

#### 4. **Verify Tool Usage**
- Check that tool invocations match stated purpose
- Look for attempts to access sensitive data
- Verify file operations are appropriate

### Runtime Protections

Claude provides some built-in protection:

**Sandboxing**:
- Skills run in isolated container
- No access to host system
- No network access (by design)
- Limited to pre-installed packages

**No Persistence**:
- Data doesn't persist between sessions
- Skills can't leave artifacts
- Each session starts clean

**Workspace Isolation**:
- Skills in API are workspace-scoped
- Skills in claude.ai are user-scoped
- No cross-contamination

### Best Practices

1. **Trusted Sources Only**
   - Your own skills
   - Anthropic official skills
   - Well-audited open-source skills

2. **Audit Before Use**
   - Read all files
   - Understand what code does
   - Verify external dependencies

3. **Treat Like Installing Software**
   - Would you install this app on your computer?
   - Do you trust the source?
   - Does it have access to sensitive data?

4. **Be Extra Careful In Production**
   - Double audit skills used in production systems
   - Test thoroughly in isolated environment first
   - Monitor for unexpected behavior

---

## Development Best Practices

### Start with Evaluation (Test-Driven Development)

**DON'T**: Write extensive documentation first  
**DO**: Build evaluations before writing skills

**Process**:
1. **Identify gaps** - Run Claude on tasks, document specific failures
2. **Create evaluations** - Build 3 scenarios testing these gaps
3. **Establish baseline** - Measure Claude's performance without skill
4. **Write minimal instructions** - Just enough to pass evaluations
5. **Iterate** - Execute evaluations, compare, refine

### Develop Iteratively with Claude

**Most effective pattern**: Use Claude to help build skills for Claude

**Two-Claude Method**:
1. **Claude A** (Helper): Helps design and refine the skill
2. **Claude B** (User): Tests the skill in real tasks

**Workflow**:
```
1. Complete task with Claude A (without skill)
   → Notice what context you repeatedly provide

2. Ask Claude A to create a skill
   → "Create a skill that captures this BigQuery analysis pattern"

3. Review for conciseness
   → "Remove the explanation about what win rate means"

4. Improve information architecture
   → "Organize so table schema is in separate reference file"

5. Test with Claude B (fresh instance with skill loaded)
   → Give Claude B actual tasks using the skill

6. Observe Claude B's behavior
   → Note struggles, successes, unexpected choices

7. Return to Claude A with feedback
   → "Claude B forgot to filter test accounts - should we make it more prominent?"

8. Repeat
   → Continue iterate-observe-refine cycle
```

### Structure for Scale

**When SKILL.md gets unwieldy**:
- Split content into separate files
- Reference them from SKILL.md
- Keep mutually exclusive contexts separate
- Add table of contents to long files (>100 lines)

**Pattern 1: Domain-specific organization**
```
SKILL.md → Overview
├── sales/schemas.md → Only for sales queries
├── finance/schemas.md → Only for finance queries
└── marketing/schemas.md → Only for marketing queries
```

**Pattern 2: Conditional details**
```
SKILL.md → Basic workflow
└── reference/advanced-config.md → For advanced users
```

**Pattern 3: High-level guide**
```
SKILL.md → Table of contents
├── getting-started.md
├── api-reference.md
└── troubleshooting.md
```

### Code Over Generation

**Prefer executable scripts for**:
- Deterministic operations
- Complex algorithms
- Repeated computations
- Validation logic

**Why**:
- More reliable than generated code
- Saves tokens (no code in context)
- Saves time (no generation needed)
- Ensures consistency

**Pattern**:
```python
# Good: Solve, don't punt
try:
    result = process_data(input)
except ValueError as e:
    print(f"Error: Invalid format - {e}")
    print("Expected format: [specific format]")
    sys.exit(1)

# Bad: Punt to Claude
try:
    result = process_data(input)
except Exception:
    print("Something went wrong")  # Claude has to figure it out
```

### Feedback Loops for Quality

**Pattern: Plan → Validate → Execute → Verify**

Example for complex tasks:
```markdown
## Workflow
1. Analyze input and create plan.json
2. Run validate_plan.py
3. If validation fails, revise plan.json and repeat step 2
4. Once valid, execute plan
5. Verify results with verify_output.py
```

**Why this works**:
- Catches errors early
- Machine-verifiable validation
- Reversible planning (can iterate without touching originals)
- Clear debugging (error messages point to specific problems)

### Visual Analysis When Possible

For inputs that can be rendered as images:
```markdown
## Analyzing Forms
1. Convert PDF to images using pdf_to_images.py
2. Analyze each page image to understand structure
3. Identify form fields visually
4. Extract field metadata
5. Fill forms based on visual layout
```

**Why**: Claude can "see" the document structure, improving accuracy

### Think from Claude's Perspective

**Monitor how Claude uses your skill**:
- Unexpected exploration paths? → Structure not intuitive
- Missed connections? → Links need to be more prominent
- Overreliance on certain sections? → Move to SKILL.md
- Ignored content? → Unnecessary or poorly signaled

**Iterate based on observation**:
- Don't assume - watch actual usage
- Real agent behavior > theoretical design
- Claude shows you what it needs

### Content Quality

**Avoid time-sensitive information**:
```markdown
# Bad
As of 2024, the API uses version 2.3

# Good
See `reference/current-config.md` for API version
# (Update current-config.md separately as needed)
```

**Use consistent terminology**:
```markdown
# Good
Always: "API endpoint", "field", "extract"

# Bad
Mix: "endpoint/URL/route", "field/box/element", "extract/pull/get"
```

**Provide concrete examples**:
```markdown
# Good
Input: {user: "john", score: 95}
Output: "John scored 95 points"

# Bad
Process the input and generate appropriate output
```

### Template Pattern for Strict Requirements

When output must match exact format:
```markdown
## Required Output Format
\`\`\`json
{
  "field1": "value",
  "field2": 123,
  "field3": ["item1", "item2"]
}
\`\`\`

**CRITICAL**: Output MUST match this structure exactly. Do not add extra fields or change data types.
```

### Testing Guidelines

**Test with all models**:
- **Haiku**: Does skill provide enough guidance? (May need more detail)
- **Sonnet**: Is skill clear and efficient? (Should be well-balanced)
- **Opus**: Does skill avoid over-explaining? (Can be more concise)

**Test with real scenarios**:
- Not toy examples
- Actual tasks from production
- Edge cases and error conditions

**Team feedback**:
- Share with teammates
- Observe their usage patterns
- Incorporate blind spots you missed

---

## API & Integration

### Skills API Endpoints

**Base URL**: `https://api.anthropic.com/v1/skills`

#### Create Skill
```http
POST /v1/skills
Content-Type: multipart/form-data

skill_files: [ZIP file containing skill directory]
```

**Response**:
```json
{
  "id": "skill_abc123",
  "name": "Analyzing Spreadsheets",
  "description": "...",
  "created_at": "2025-01-15T10:30:00Z",
  "version": 1
}
```

#### List Skills
```http
GET /v1/skills
```

**Response**:
```json
{
  "skills": [
    {
      "id": "skill_abc123",
      "name": "Analyzing Spreadsheets",
      "version": 1
    }
  ]
}
```

#### Get Skill
```http
GET /v1/skills/{skill_id}
```

#### Update Skill
```http
PUT /v1/skills/{skill_id}
Content-Type: multipart/form-data

skill_files: [Updated ZIP file]
```

**Result**: Creates new version, old version preserved

#### Delete Skill
```http
DELETE /v1/skills/{skill_id}
```

### Using Skills in Messages API

```json
{
  "model": "claude-sonnet-4-5-20250929",
  "max_tokens": 4096,
  "tools": [
    {
      "type": "code_execution",
      "container": {
        "skills": [
          "pptx",           // Anthropic skill (skill_id)
          "skill_abc123"    // Custom skill (skill_id)
        ]
      }
    }
  ],
  "messages": [
    {
      "role": "user",
      "content": "Create a PowerPoint about Q4 results using our data"
    }
  ]
}
```

### Required Beta Headers

```http
anthropic-beta: code-execution-2025-08-25,skills-2025-10-02,files-api-2025-04-14
```

**Why three headers**:
- `code-execution-2025-08-25`: Skills run in code execution container
- `skills-2025-10-02`: Enables Skills functionality
- `files-api-2025-04-14`: Required for file uploads/downloads

### Anthropic-Managed Skills

Pre-built skills available via `skill_id`:
- `pptx` - PowerPoint
- `xlsx` - Excel
- `docx` - Word
- `pdf` - PDF

**Usage**: Just include the skill_id in the skills array

### Version Management

- Skills are versioned automatically
- Updates create new version
- Old versions preserved
- Can specify version in requests (future feature)

### Workspace Scope

**API Skills**:
- Shared organization-wide
- All workspace members can access
- Managed centrally through Console

**Claude.ai Skills**:
- Individual user only
- Not shared organization-wide
- Each user uploads separately

---

## Limitations & Constraints

### Cross-Surface Availability

**Skills DO NOT sync across platforms**:
- Claude.ai upload ≠ API upload
- API upload ≠ Claude.ai
- Claude Code ≠ both

**To use everywhere**: Upload/install separately on each platform

### Sharing Scope

| Platform | Sharing |
|----------|---------|
| Claude.ai | Individual user only |
| API | Workspace-wide |
| Claude Code | Personal (~/.claude/skills) or project (.claude/skills) |

### Runtime Environment Constraints

**Network Access**:
- ❌ **NO network access**
- Can't make external API calls
- Can't fetch data from URLs
- Can't connect to databases

**Package Installation**:
- ❌ **NO runtime installation**
- Only pre-installed packages available
- Can't pip install or npm install during execution
- Check available packages in code execution tool docs

**Pre-configured Dependencies Only**:
- Python packages: Limited to what's pre-installed
- JavaScript/Node: Limited to what's pre-installed
- See: [Code Execution Tool Documentation](https://docs.claude.com/en/docs/agents-and-tools/tool-use/code-execution-tool)

### Size & Performance

**SKILL.md Body**:
- Recommended: Under 500 lines
- If exceeded: Split into reference files
- Why: Optimal performance, faster loading

**Total Skill Size**:
- Technically: No hard limit
- Practically: Keep reasonable
- Progressive disclosure means big skills OK if organized well

### Platform-Specific Limitations

**Claude.ai**:
- Requires Pro/Max/Team/Enterprise plan
- Requires Code Execution enabled
- Individual user only (no org-wide deployment)
- Upload as ZIP only

**API**:
- Requires beta headers
- Workspace-level only (no individual)
- Version management available

**Claude Code**:
- Filesystem-based (no API upload)
- Plugin system or manual installation
- Project or personal scope

---

## Advanced Patterns

### Multi-Domain Skills

When skill covers multiple domains, organize to avoid loading irrelevant context:

```
skill-name/
├── SKILL.md (overview + routing)
├── sales/
│   ├── metrics.md
│   └── reports.md
├── finance/
│   ├── metrics.md
│   └── reports.md
└── marketing/
    ├── metrics.md
    └── reports.md
```

**In SKILL.md**:
```markdown
## Domain-Specific Details

- For sales queries: see `sales/metrics.md`
- For finance queries: see `finance/metrics.md`
- For marketing queries: see `marketing/metrics.md`
```

**Result**: Claude only loads the domain it needs

### Conditional Complexity

**Pattern**: Show basic content, link to advanced

```markdown
## Basic Usage
[Simple instructions here]

## Advanced Usage
For advanced configuration options, see `reference/advanced-config.md`
```

**When to use**: 
- Most users need basic
- Power users need advanced
- Don't force everyone to load advanced content

### MCP Integration

Skills can teach Claude how to use MCP tools effectively:

```markdown
## Using BigQuery MCP Tool

Always use fully qualified names: `BigQuery:tool_name`

### Available Tools
- `BigQuery:bigquery_schema` - Get table structure
- `BigQuery:run_query` - Execute SQL query

### Workflow
1. Use `BigQuery:bigquery_schema` to understand table structure
2. Construct query based on schema
3. Use `BigQuery:run_query` to execute
4. Parse and format results
```

**Why this works**:
- MCP provides the tools
- Skill teaches how to use them
- Together = powerful workflow

### Plan-Validate-Execute Pattern

For complex, error-prone tasks:

```markdown
## Workflow

### 1. Planning Phase
Create `plan.json` with proposed changes:
\`\`\`json
{
  "changes": [
    {"field": "name", "old": "...", "new": "..."},
    {"field": "email", "old": "...", "new": "..."}
  ]
}
\`\`\`

### 2. Validation Phase
Run `code/validate_plan.py`:
- Checks all fields exist
- Validates data types
- Verifies no conflicts

If validation fails:
- Review errors
- Revise plan.json
- Re-run validation
- Only proceed after pass

### 3. Execution Phase
Run `code/apply_changes.py`:
- Applies validated changes
- Generates audit log

### 4. Verification Phase
Run `code/verify_results.py`:
- Confirms changes applied correctly
- Reports any discrepancies
```

**Why this works**:
- Catches errors before applying
- Machine-verifiable validation
- Iterative planning without risk
- Clear audit trail

### Checklist Pattern

For complex multi-step workflows:

```markdown
## Compliance Review Workflow

- [ ] Step 1: Load policy documents from `policies/`
- [ ] Step 2: Parse content for required sections
- [ ] Step 3: Run `code/compliance_check.py` on each section
- [ ] Step 4: Document all findings in findings.json
- [ ] Step 5: Generate report using output template
- [ ] Step 6: Verify report completeness

**Only mark step complete after validation passes**
```

**Why this works**:
- Clear progress tracking
- Forces sequential execution
- Prevents skipping critical steps
- Visual confirmation of completion

### Skill Composition

Multiple skills can work together automatically:

**Example**: Quarterly Investor Deck
- Skill 1: Brand Guidelines (colors, fonts, logo)
- Skill 2: Financial Reporting (data format, calculations)
- Skill 3: Presentation Formatting (layout, structure)

**Claude automatically**:
- Identifies all three are relevant
- Loads all three
- Coordinates between them
- Produces deck following all guidelines

**No manual orchestration required**

### Reference File Organization

For large reference files (>100 lines), include table of contents:

```markdown
# API Reference

## Contents
- [Authentication](#authentication)
- [Endpoints](#endpoints)
  - [Users](#users)
  - [Orders](#orders)
  - [Products](#products)
- [Error Codes](#error-codes)
- [Rate Limits](#rate-limits)

## Authentication
[Details...]

## Endpoints
### Users
[Details...]
```

**Why**: Claude sees full scope even in partial reads

### Execution Intent Clarity

Make it clear whether to execute or reference code:

```markdown
# Execute
Run `code/validator.py` to validate the output

# Reference
See `code/validator.py` for the validation algorithm logic
```

**Why**: Prevents confusion about how to use scripts

---

## Summary: The Skills-Builder's Mission

The skills-builder must create Skills that are:

1. **Properly Structured**
   - Valid YAML frontmatter (64/1024 char limits)
   - Gerund naming convention
   - Descriptive, discoverable descriptions
   - Forward slashes in paths

2. **Progressively Disclosed**
   - Lean SKILL.md (<500 lines)
   - Reference files for details
   - One level deep from SKILL.md
   - Table of contents for long files

3. **Platform-Aware**
   - Works on claude.ai, API, and Claude Code
   - Respects platform limitations
   - Portable across surfaces

4. **Secure**
   - No external network calls
   - Clear audit trail
   - Validates inputs
   - Handles errors explicitly

5. **Well-Tested**
   - Evaluations drive development
   - Tested on Haiku, Sonnet, Opus
   - Real scenarios, not toy examples
   - Iterated based on observation

6. **Intelligently Organized**
   - Domain-specific separation
   - Conditional complexity
   - Feedback loops for quality
   - Executable scripts for determinism

7. **Following Best Practices**
   - No time-sensitive content
   - Consistent terminology
   - Concrete examples
   - Visual analysis when possible

The skills-builder is the MASTER tool for creating world-class Claude Skills that kick ass across all platforms.

---

**Sources**:
- https://support.claude.com/en/articles/12512176-what-are-skills
- https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview
- https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices
- https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- GitHub: anthropics/skills
- Claude Developer Platform Documentation
