# Claude Skills Best Practices Reference

This document summarizes Anthropic's official best practices for skill authoring. The Skills Builder incorporates these principles automatically.

## Core Principles

### 1. Concise is Key
- Skills share the context window with system prompt, conversation history, and other skills
- Always ask: "Does Claude really need this explanation?"
- Keep SKILL.md body under 500 lines for optimal performance
- Use progressive disclosure: reference detailed files only when needed

### 2. Set Appropriate Degrees of Freedom
**High freedom (text-based instructions)** - Use when:
- Multiple approaches are valid
- Decisions depend on context
- Heuristics guide the approach

**Medium freedom (templates/examples)** - Use when:
- A preferred pattern exists
- Some variation is acceptable
- Configuration affects behavior

**Low freedom (strict specifications)** - Use when:
- Operations are fragile and error-prone
- Consistency is critical
- A specific sequence must be followed

### 3. Test with All Models
- Test with Haiku (fast, economical): Does the Skill provide enough guidance?
- Test with Sonnet (balanced): Is the Skill clear and efficient?
- Test with Opus (powerful reasoning): Does the Skill avoid over-explaining?

## Skill Structure Requirements

### YAML Frontmatter
```yaml
---
name: Your Skill Name  # Max 64 characters, use gerund form (e.g., "Processing PDFs")
description: One-line description of what it does and when to use it  # Max 1024 characters
---
```

### Naming Conventions
**Good** (gerund form):
- "Processing PDFs"
- "Analyzing spreadsheets"
- "Managing databases"
- "Testing code"

**Avoid**:
- Noun phrases: "PDF Processing"
- Action-oriented: "Process PDFs"
- Vague: "Helper", "Utils", "Tools"
- Generic: "Documents", "Data"

### Description Best Practices
- Include BOTH what it does AND when to use it
- Use active voice: "Processes Excel files and generates reports"
- Avoid first/second person: NOT "I can help you" or "You can use this"
- Include key terms for discoverability

## Progressive Disclosure Patterns

### Pattern 1: High-level Guide with References
```markdown
# SKILL.md (overview)
For detailed API schemas, see `reference/api-docs.md`
For common query patterns, see `reference/patterns.md`
```

### Pattern 2: Domain-specific Organization
```
SKILL.md (overview)
├── sales/schemas.md
├── finance/schemas.md
└── marketing/schemas.md
```

### Pattern 3: Conditional Details
```markdown
Basic workflow here...

For advanced options, see `reference/advanced-config.md`
```

**Important**: Keep references ONE level deep from SKILL.md. Avoid deeply nested references.

### Structure Longer Reference Files
For files >100 lines, include a table of contents at the top:
```markdown
# Contents
- [Basic Usage](#basic-usage)
- [Advanced Features](#advanced-features)
- [Troubleshooting](#troubleshooting)
```

## Workflows and Feedback Loops

### Complex Task Workflows
Break into clear, sequential steps. For particularly complex workflows, provide a checklist:

```markdown
## Workflow
- [ ] Step 1: Validate input
- [ ] Step 2: Process data
- [ ] Step 3: Generate output
- [ ] Step 4: Verify results
```

### Feedback Loops
Common pattern: Run validator → fix errors → repeat

```markdown
1. Generate output
2. Run `validate_output.py`
3. If validation fails, fix identified issues and repeat step 2
4. Proceed only after validation passes
```

## Content Guidelines

### Avoid Time-Sensitive Information
**Bad**: "As of 2024, the API uses version 2.3"
**Good**: Put in separate "Current Configuration" section you can update

### Use Consistent Terminology
**Good**: Always use "API endpoint", "field", "extract"
**Bad**: Mix "endpoint/URL/route", "field/box/element", "extract/pull/get"

## Common Patterns

### Template Pattern
For strict requirements (API responses, data formats):
```markdown
## Required Output Format
\`\`\`json
{
  "field1": "value",
  "field2": 123
}
\`\`\`
DO NOT deviate from this structure.
```

### Examples Pattern
Provide input/output pairs:
```markdown
## Examples
**Input**: [sample input]
**Output**: [expected output]
```

### Conditional Workflow Pattern
```markdown
1. If condition A:
   - Do X
   - Then Y
2. If condition B:
   - Do Z
```

## Evaluation and Iteration

### Build Evaluations First
1. Identify gaps: Run Claude without Skill, document failures
2. Create evaluations: Build 3 scenarios testing these gaps
3. Establish baseline: Measure performance without Skill
4. Write minimal instructions: Address gaps to pass evaluations
5. Iterate: Execute evaluations, compare, refine

### Develop Skills Iteratively with Claude
1. Complete a task without a Skill first
2. Identify reusable patterns
3. Ask Claude to create a Skill from the pattern
4. Review for conciseness
5. Improve information architecture
6. Test on similar tasks
7. Iterate based on observation

## Anti-patterns to Avoid

### File Paths
- ✓ Good: `scripts/helper.py`, `reference/guide.md`
- ✗ Bad: `scripts\helper.py`, `reference\guide.md` (Windows-style)

### Don't Offer Too Many Options
**Bad**:
```markdown
You can either:
- Approach 1...
- Approach 2...
- Approach 3...
```
**Good**: Choose the best approach and document it clearly.

## Advanced: Skills with Executable Code

### Solve, Don't Punt
Handle errors in scripts, don't punt to Claude:
```python
# Good
try:
    result = process_data()
except ValueError as e:
    print(f"Error: Invalid data format - {e}")
    sys.exit(1)

# Bad
try:
    result = process_data()
except Exception:
    print("Something went wrong")  # Punts to Claude
```

### Provide Utility Scripts
Benefits:
- More reliable than generated code
- Save tokens (no code in context)
- Save time (no generation needed)
- Ensure consistency

### Create Verifiable Intermediate Outputs
Plan-validate-execute pattern:
```markdown
1. Analyze input and create plan.json
2. Run validate_plan.py
3. If validation fails, revise plan.json and repeat
4. Execute plan
5. Verify results
```

### Package Dependencies
- claude.ai: Can install npm/PyPI packages, pull from GitHub
- Anthropic API: No network access, no runtime package installation

### MCP Tool References
Always use fully qualified names: `ServerName:tool_name`
```markdown
Use `BigQuery:bigquery_schema` to fetch table structure
Use `GitHub:create_issue` to file bugs
```

## Runtime Environment

Skills run in code execution environment:
- Metadata (name/description) pre-loaded in system prompt
- Files read on-demand via bash tools
- Scripts executed efficiently (only output consumes tokens)
- No context penalty for large files until accessed

**Implications**:
- File paths matter (use forward slashes)
- Name files descriptively: `form_validation_rules.md` not `doc2.md`
- Organize for discovery: `reference/finance.md` not `docs/file1.md`
- Bundle comprehensive resources (no penalty until accessed)
- Prefer scripts for deterministic operations
- Make execution intent clear: "Run X" vs "See X for algorithm"

## Checklist for Effective Skills

### Core Quality
- [ ] Name max 64 chars, uses gerund form
- [ ] Description includes what + when, max 1024 chars
- [ ] SKILL.md body under 500 lines
- [ ] Additional details in separate files (if needed)
- [ ] No time-sensitive information
- [ ] Consistent terminology throughout
- [ ] Examples are concrete, not abstract
- [ ] File references one level deep
- [ ] Progressive disclosure used appropriately
- [ ] Workflows have clear steps

### Code and Scripts (if applicable)
- [ ] Scripts solve problems, don't punt
- [ ] Error handling is explicit
- [ ] No unexplained constants
- [ ] Required packages listed and verified
- [ ] Scripts have clear documentation
- [ ] No Windows-style paths
- [ ] Validation/verification for critical operations
- [ ] Feedback loops for quality-critical tasks

### Testing
- [ ] At least 3 evaluations created
- [ ] Tested with Haiku, Sonnet, and Opus
- [ ] Tested with real usage scenarios
- [ ] Team feedback incorporated (if applicable)

---

**Source**: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices
