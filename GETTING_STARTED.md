# Getting Started with Skills Builder

## What You'll Build

A custom Claude Skill that automatically activates when you use specific phrases, following your exact specifications.

## Step 1: Understand the Example

Look at `examples/minimal/skill.spec.json` - this is a complete spec for a Document Summarizer skill.

Key parts:
- **name**: "Document Summarizer" 
- **triggers**: Phrases that activate it ("Summarize this document")
- **procedure**: The steps Claude will follow
- **output_contract**: The exact format of the output

## Step 2: Test the Example

```bash
cd /Users/jaytarzwell/Skills/skills-builder

# Validate the example spec
python3 -m code.cli validate --spec examples/minimal/skill.spec.json

# Generate the skill files
python3 -m code.cli new --spec examples/minimal/skill.spec.json --out dist/

# Package it for upload
python3 -m code.cli pack --dir dist/document-summarizer --out dist/document-summarizer.zip
```

## Step 3: Upload to Claude

1. Open Claude (https://claude.ai)
2. Click your profile → Settings → Skills
3. Click "Upload" and select `dist/document-summarizer.zip`
4. The skill is now active!

## Step 4: Test Your Skill

In a new conversation with Claude, say:
> "Summarize this document"

Claude will recognize the trigger and activate your skill.

## Step 5: Build Your Own

### Option A: Interactive (Recommended)

Start a conversation with Claude and say:
> "Help me build a new Claude skill using the Skills Builder"

Claude will interview you and generate the spec.

### Option B: Manual

1. Copy `examples/minimal/skill.spec.json` to a new file
2. Edit all the fields for your use case
3. Run the validation and generation commands
4. Upload and test

## What Makes a Good Skill?

✅ **Clear triggers** - Specific phrases users will naturally say
✅ **Defined inputs** - Exactly what the skill needs (files, data, etc.)
✅ **Step-by-step procedure** - Ordered, logical steps
✅ **Structured output** - Consistent format with clear sections
✅ **Guardrails** - Rules to prevent errors or unwanted behavior

## Common Patterns

### Document Analysis Skill
- Triggers: "analyze", "review", "evaluate"
- Inputs: Document file
- Output: Findings, recommendations, metrics

### Data Processing Skill  
- Triggers: "process", "transform", "clean"
- Inputs: CSV/Excel file
- Output: Cleaned data, statistics, report

### Creative Writing Skill
- Triggers: "write", "draft", "compose"
- Inputs: Topic, style, length
- Output: Formatted document with specific sections

### Research Skill
- Triggers: "research", "investigate", "find"
- Inputs: Topic, sources, constraints
- Output: Summary, key findings, sources

## Tips

1. **Keep triggers unique** - Avoid overlapping with other skills
2. **Test thoroughly** - Try edge cases and unexpected inputs
3. **Iterate** - Update your spec based on real usage
4. **Document well** - Good examples in your spec help Claude understand

## Troubleshooting

**"Skill not activating"** - Make your triggers more specific or add more variations

**"Output doesn't match contract"** - Add more detail to your procedure steps

**"Validation errors"** - Read the error messages - they point to exactly what needs fixing

## Need Help?

- Check the [README.md](README.md) for full documentation
- Look at the example spec in `examples/minimal/`
- Review Claude's Skills documentation: https://docs.anthropic.com/claude/docs/skills

## Next Steps

Once you've built your first skill:
1. Create more skills for different workflows
2. Share specs with your team
3. Add custom validators for your domain
4. Build a library of reusable skills

Happy building! 🚀
