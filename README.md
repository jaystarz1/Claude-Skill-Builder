# Claude Skills Builder

An agnostic, config-first framework for creating Claude Skills that follow Anthropic's official best practices.

## What is this?

The Skills Builder helps you create custom Claude Skills that comply with [Anthropic's official best practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices) through:
- **Best practices validation** - Checks your spec against Claude's official guidelines
- **Interactive interview** - Answer questions to define your skill
- **Structural validation** - Ensure your spec is technically sound
- **Scaffolding** - Generate all necessary files automatically
- **Packaging** - Create uploadable .zip files for Claude

## Key Features

✅ **Enforces Claude's official limits**: 64-char names, 1024-char descriptions  
✅ **Validates naming conventions**: Suggests gerund form ("Processing PDFs")  
✅ **Checks best practices**: Time-sensitive content, file paths, MCP tool format  
✅ **Progressive disclosure support**: Reference files, conditional content  
✅ **Feedback loop patterns**: Built-in validation workflows  
✅ **Under 500-line SKILL.md**: Automatic warnings for length

## Two Ways to Use This

### Option 1: Use as a Claude Skill (Interactive - Recommended)

Upload the Skills Builder as a skill to Claude, then ask Claude to help you build skills!

**Requirements:**
- **Claude Code**: ✅ Works out of the box (built-in filesystem access)
- **Claude Desktop**: ✅ Works with [Filesystem MCP](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) enabled
- **Claude Web**: ⚠️ Limited (can provide guidance but can't create files)

**Setup:**
1. Download [`skills-builder-skill.zip`](./skills-builder-skill.zip)
2. Open Claude (Code, Desktop, or Web)
3. Go to Settings → Capabilities → Skills
4. Enable "Code execution and file creation"
5. Click "Upload skill"
6. Select `skills-builder-skill.zip`

**If using Claude Desktop**, you'll also need the Filesystem MCP:
```json
// Add to your claude_desktop_config.json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/your/workspace"]
    }
  }
}
```

**Then use it:**
```
"Help me build a skill for analyzing spreadsheets"
"Create a skill that processes PDFs"
"I want to build a custom skill for my workflow"
```

Claude will guide you through the process, validate your spec, generate files, and package everything for upload.

### Option 2: Use as Command-Line Tools (Automation)

Clone and use the Python CLI directly for automation and CI/CD workflows.

**Requirements:**
- Python 3.9+
- No external dependencies (uses stdlib only)

## Quick Start (CLI)

### 1. Clone the repository

```bash
git clone https://github.com/jaystarz1/Claude-Skill-Builder.git
cd Claude-Skill-Builder
```

### 2. Create a skill spec

See `examples/best-practices/skill.spec.json` for a complete example following all Claude best practices.

### 3. Validate your spec

```bash
python3 -m code.cli validate --spec examples/best-practices/skill.spec.json
```

This checks:
- Required fields and structure ❌ (blocking errors)
- Claude's official limits ❌ (blocking errors)
- Best practices ⚠️ (helpful suggestions)

### 4. Generate the skill

```bash
python3 -m code.cli new --spec examples/best-practices/skill.spec.json --out dist/
```

### 5. Package for upload

```bash
python3 -m code.cli pack --dir dist/analyzing-spreadsheets --out dist/analyzing-spreadsheets.zip
```

### 6. Upload to Claude

1. Open Claude (web, desktop, or mobile)
2. Go to Settings → Capabilities → Skills
3. Click "Upload Skill"
4. Select your .zip file
5. Test with one of your example triggers

## Platform Compatibility

| Platform | Interactive Skill | CLI Tools | Notes |
|----------|-------------------|-----------|-------|
| **Claude Code** | ✅ Full support | ✅ Full support | Best experience - built-in filesystem |
| **Claude Desktop** | ✅ With Filesystem MCP | ✅ Full support | Requires MCP for file creation |
| **Claude Web** | ⚠️ Guidance only | ✅ Full support | Can't create files, copy/paste instead |
| **Claude API** | N/A | ✅ Full support | Use CLI tools |

## Project Structure

```
skills-builder/
├─ skills-builder-skill.zip   # Pre-packaged skill for Claude upload
├─ CLAUDE_BEST_PRACTICES.md   # Anthropic's official guidelines
├─ MASTER_KNOWLEDGE.md         # Complete technical reference
├─ skill.md                    # Meta-skill for builder orchestration
├─ code/
│  ├─ cli.py                   # Command-line interface
│  ├─ scaffold.py              # Skill generation
│  ├─ validate.py              # Spec validation + best practices
│  ├─ pack.py                  # Zip packaging
│  ├─ schema.py                # JSON schemas with Claude limits
│  └─ plugins/                 # Extensible components
├─ templates/                  # Generic templates (Claude-compliant)
├─ examples/
│  ├─ minimal/                 # Simple example
│  └─ best-practices/          # Full-featured example
└─ dist/                       # Generated skills
```

## Skill Spec Format

A skill spec is a JSON file following Claude's requirements:

### Required Fields
- **name** - Short skill name (max 64 chars, use gerund form, lowercase-with-hyphens)
- **description** - What it does + when to use it (max 1024 chars)
- **triggers** - Activation phrases (≥2)
- **inputs** - Expected inputs (files, text, etc.)
- **guardrails** - Rules and constraints
- **procedure** - Step-by-step process
- **output_contract** - Structure of the output

### Optional Fields
- **example_triggers** - Sample activation phrases
- **reference_files** - For progressive disclosure
- **code_helper** - Helper scripts and their usage
- **validation** - Feedback loop configuration
- **mcp_tools** - MCP tool references (format: `ServerName:tool_name`)

See `CLAUDE_BEST_PRACTICES.md` for full details on Claude's official requirements.

## Best Practices Built In

The Skills Builder automatically enforces/suggests:

### Naming & Description
- ✅ Names use gerund form: "Processing PDFs" not "PDF Processor"
- ✅ Names are lowercase-with-hyphens for upload compatibility
- ✅ Descriptions include both WHAT and WHEN
- ✅ Active voice without first/second person
- ✅ Character limits enforced (64 name, 1024 description)

### File Organization
- ✅ Forward slashes for all paths (cross-platform)
- ✅ Progressive disclosure patterns supported
- ✅ Reference files stay one level deep
- ✅ Warns when SKILL.md exceeds 500 lines

### Content Quality
- ⚠️ Detects time-sensitive information
- ⚠️ Suggests feedback loops for validation
- ⚠️ Validates MCP tool format
- ⚠️ Checks for consistent terminology

### Code & Scripts
- ✅ Script execution modes (execute vs reference)
- ✅ Validation feedback loop patterns
- ✅ Helper script organization

## Commands Reference (CLI)

### validate
Check a spec file for errors and best practice issues:
```bash
python3 -m code.cli validate --spec path/to/spec.json
```

Output includes:
- ❌ Blocking errors (must fix)
- ⚠️ Best practice suggestions (optional but recommended)

### new
Generate a new skill from a spec:
```bash
python3 -m code.cli new --spec path/to/spec.json --out output_dir/
```

### pack
Package a skill directory into a .zip:
```bash
python3 -m code.cli pack --dir skill_folder/ --out skill.zip
```

## Design Principles

1. **Claude-compliant** - Follows Anthropic's official guidelines
2. **Agnostic** - No domain assumptions baked in
3. **Config-first** - Everything driven by the spec
4. **Composable** - Templates and validators are pluggable
5. **Deterministic** - Clear structure, predictable output
6. **Portable** - Generates standard Claude Skills packages

## Examples

### Minimal Example
```bash
python3 -m code.cli validate --spec examples/minimal/skill.spec.json
python3 -m code.cli new --spec examples/minimal/skill.spec.json --out dist/
python3 -m code.cli pack --dir dist/summarizing-documents --out dist/summarizing-documents.zip
```

### Best Practices Example (Recommended)
```bash
python3 -m code.cli validate --spec examples/best-practices/skill.spec.json
python3 -m code.cli new --spec examples/best-practices/skill.spec.json --out dist/
python3 -m code.cli pack --dir dist/analyzing-spreadsheets --out dist/analyzing-spreadsheets.zip
```

## Extending the Builder

### Add Custom Validators
```python
# code/plugins/validators/custom.py
from custom import register_validator

def my_validator(spec):
    errors = []
    # Your validation logic
    return errors

register_validator("my_validator", my_validator)
```

### Add Custom Templates
Place new templates in `templates/` and reference them in scaffold.py.

## Troubleshooting

**Import errors**: Make sure you're running from the repository root directory.

**Template rendering issues**: Check that your spec has all required fields.

**Validation failures**: Read the error messages carefully - they tell you exactly what's wrong.

**Best practice warnings**: These are suggestions, not errors. Your skill will work, but following the suggestions improves quality.

**Filesystem MCP not working**: Make sure the path in your config points to a directory where you want skills generated.

## Learn More

- [Claude Skills Documentation](https://docs.anthropic.com/claude/docs/agents-and-tools/agent-skills/overview)
- [Official Best Practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)
- [Filesystem MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)
- [CLAUDE_BEST_PRACTICES.md](./CLAUDE_BEST_PRACTICES.md) - Full reference
- [MASTER_KNOWLEDGE.md](./MASTER_KNOWLEDGE.md) - Complete technical reference
- [Skill Spec Examples](./examples/)
- [Template Reference](./templates/)

## What's Different from Generic Skill Builders?

This builder is specifically designed for Claude Skills with:
- ✅ Official Anthropic best practices baked in
- ✅ Validation against Claude's requirements (64/1024 char limits)
- ✅ Progressive disclosure patterns
- ✅ Feedback loop support
- ✅ MCP tool integration
- ✅ Code execution environment awareness
- ✅ Real best practice warnings during validation
- ✅ **Pre-packaged as a Claude Skill** - Use Claude to build skills!
- ✅ **Works in Claude Code out of the box**

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

Copyright 2025 Jay Tarzwell

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

---

**Ready to build Claude-compliant skills?**

**Interactive (Skill):** Upload `skills-builder-skill.zip` to Claude Code (works instantly) or Claude Desktop (with Filesystem MCP)

**CLI (Automation):**
```bash
# Start with the best practices example
python3 -m code.cli validate --spec examples/best-practices/skill.spec.json
python3 -m code.cli new --spec examples/best-practices/skill.spec.json --out dist/
python3 -m code.cli pack --dir dist/analyzing-spreadsheets --out dist/analyzing-spreadsheets.zip
```
