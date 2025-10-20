# Skills-Builder

> Create world-class Claude Skills that work on your actual filesystem!

A comprehensive skill-builder that creates production-ready Claude Skills following all official Anthropic guidelines. Automatically detects your home directory and creates skills in `~/skills/` with dynamic path detection that works for any user.

---

## ✨ Features

- **🎯 Dynamic Path Detection** - Works for any user on any platform (Mac, Linux, Windows)
- **📁 Persistent Files** - Creates skills on your actual filesystem, not temporary containers
- **📦 Automatic ZIP Creation** - Skills are automatically packaged and ready to upload
- **🔄 Git Integration** - Optional pre-commit hooks auto-rebuild ZIPs on every commit
- **✅ Full Validation** - Checks all requirements before creating skills
- **📚 Progressive Disclosure** - Supports reference files, examples, and code helpers
- **🔒 Security First** - Never uses temporary or container directories

---

## 🚀 Quick Start

### 1. Set Up MCP Servers

Before using skills-builder, you need two MCP servers:

**Required:**
- **Filesystem MCP** - Lets Claude create files on your computer

**Recommended:**
- **Zip Creator MCP** - Automatically packages skills (has Python fallback if not installed)

**📖 Complete Setup Guide:** [SETUP.md](SETUP.md)

**Quick links:**
- [Filesystem MCP Guide](reference/filesystem-mcp-setup.md) - Includes link to complete Google Doc
- [Zip Creator MCP Guide](reference/zip-creator-mcp-setup.md) - Step-by-step installation

### 2. Upload to Claude Desktop

1. Download `skills-builder.zip` from this repository
2. Open Claude Desktop
3. Go to **Settings → Capabilities**
4. Click **"Upload skill"**
5. Select `skills-builder.zip`
6. Start a new chat!

### 3. Create Your First Skill

```
User: "Create a skill that helps me write meeting notes"

Claude: 
✅ Detected skills directory: /Users/yourname/skills/
✅ Creating skill at: /Users/yourname/skills/meeting-notes/
✅ Created meeting-notes.zip (ready to upload)

Your skill is ready! Upload meeting-notes.zip to Claude Desktop.
```

---

## 📖 What This Does

The skills-builder creates Claude Skills that:

- ✅ Work on **claude.ai**, **API**, and **Claude Code**
- ✅ Follow all Anthropic specifications and best practices
- ✅ Include comprehensive documentation and examples
- ✅ Auto-generate ZIP files ready for upload
- ✅ Validate naming conventions and structure
- ✅ Support progressive disclosure for complex workflows
- ✅ Include update instructions (UPDATING.md)

---

## 🗂️ Directory Structure

After setup, your files will look like:

```
~/skills/                          # Your skills directory
├── meeting-notes/                 # Example skill
│   ├── SKILL.md                   # Main skill definition
│   ├── meeting-notes.zip          # Auto-generated ZIP
│   ├── UPDATING.md                # Update instructions
│   ├── examples/                  # Optional: example outputs
│   └── references/                # Optional: reference docs
│
└── another-skill/
    └── ...
```

---

## 🎓 How to Use

### Creating a New Skill

```
"Create a skill that [describes what you want]"
```

The skills-builder will:
1. Ask clarifying questions about the skill's purpose
2. Request examples (highly recommended!)
3. Create the skill structure
4. Generate all necessary files
5. Create a ZIP file automatically
6. Tell you where to upload it

### Updating an Existing Skill

```
"Update the [skill-name] skill to [describe changes]"
```

The skills-builder will:
1. Locate the existing skill
2. Make the requested changes
3. Recreate the ZIP file
4. Remind you to upload the new version

### Example Requests

**Simple skill:**
```
"Create a skill that formats JSON nicely"
```

**Complex skill with examples:**
```
"Create a skill for writing legal briefs. I'll provide example briefs to use as templates."
```

**Skill update:**
```
"Update the meeting-notes skill to add a section for action items"
```

---

## 🔧 Requirements

### For Skills-Builder to Work:

1. **Filesystem MCP** installed and configured
   - Gives Claude access to create files on your computer
   - Required for persistent file creation
   - See [setup guide](SETUP.md)

2. **Claude Desktop** (Pro, Team, or Enterprise)
   - Required to upload and use custom skills

### Optional but Recommended:

3. **Zip Creator MCP** installed
   - Faster, more reliable ZIP creation
   - Falls back to Python if not installed
   - See [setup guide](reference/zip-creator-mcp-setup.md)

---

## 📋 Features in Detail

### Dynamic Path Detection

Works for any user on any platform:

- Checks for `$SKILLS_DIR` environment variable
- Falls back to `~/skills/` directory
- Auto-creates the directory if it doesn't exist
- **No hardcoded paths** - works for everyone!

### Automatic ZIP Creation

Every skill is automatically packaged:

- Uses zip-creator MCP if available
- Falls back to Python script if not
- Excludes `.git/`, `__pycache__/`, etc.
- One ZIP file per skill (overwrites previous)

### Git Integration (Optional)

If your skill is in a git repo:

- Auto-sets up pre-commit hook
- Rebuilds ZIP on every commit
- ZIP stays in sync with code
- No manual ZIP recreation needed

### Comprehensive Validation

Before creating any skill:

- ✅ Validates skills directory exists
- ✅ Checks filesystem MCP is available
- ✅ Verifies naming conventions
- ✅ Confirms no reserved words used
- ✅ Checks all requirements met

### Update Tracking

Every skill includes:

- `UPDATING.md` - Instructions for updating
- Clear reminders about ZIP recreation
- Links to tools and documentation

---

## 🎯 Skill Quality

Skills-builder creates professional-quality skills that:

- Follow [Anthropic's best practices](CLAUDE_BEST_PRACTICES.md)
- Use proper naming conventions (lowercase-with-hyphens)
- Include WHAT the skill does AND WHEN to use it
- Have clear, actionable procedures
- Include examples when provided
- Work across all Claude platforms

---

## 📚 Documentation

- **[SETUP.md](SETUP.md)** - Complete setup guide for new users
- **[SKILL.md](SKILL.md)** - Full skills-builder documentation
- **[UPDATES.md](UPDATES.md)** - Recent changes and improvements
- **[reference/](reference/)** - MCP setup guides
  - [filesystem-mcp-setup.md](reference/filesystem-mcp-setup.md)
  - [zip-creator-mcp-setup.md](reference/zip-creator-mcp-setup.md)

---

## 🔒 Security

The skills-builder:

- ✅ Never uses temporary or container directories
- ✅ Only creates files in `~/skills/` (or `$SKILLS_DIR`)
- ✅ Validates all paths before operations
- ✅ Uses filesystem MCP with proper permissions
- ✅ Clear error messages for security issues

---

## 🐛 Troubleshooting

### "Skills directory not found"

**Problem:** Can't find or create `~/skills/`

**Solution:** 
1. Make sure filesystem MCP has access to your home directory
2. Check config paths are absolute
3. Restart Claude Desktop

### "ZIP creation failed"

**Problem:** Zip-creator MCP not working

**Solution:**
- Skills-builder automatically falls back to Python
- Install zip-creator MCP for best experience (see [guide](reference/zip-creator-mcp-setup.md))

### "Access denied" errors

**Problem:** Filesystem MCP doesn't have permission

**Solution:**
1. Add your home directory to filesystem MCP config
2. Verify paths are absolute
3. Restart Claude Desktop after config changes

See [SETUP.md](SETUP.md) for complete troubleshooting guide.

---

## 🤝 Contributing

Contributions welcome! To contribute:

1. Fork this repository
2. Make your changes
3. Test with the skills-builder skill
4. Submit a pull request

Areas for contribution:
- Additional example skills
- Improved documentation
- Better error messages
- Platform-specific fixes

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

---

## 🙏 Acknowledgments

- Built using [Anthropic's MCP SDK](https://github.com/modelcontextprotocol/sdk)
- Follows [Claude Skills specifications](https://docs.anthropic.com/en/docs/build-with-claude/skills)
- Inspired by the Claude developer community

---

## 📞 Support

- **Issues:** Open an issue in this repository
- **Questions:** Check [SETUP.md](SETUP.md) and [SKILL.md](SKILL.md) first
- **Filesystem MCP:** See the [complete guide](https://docs.google.com/document/d/1UrH2zf0W_PABbaIJXUftcGF07zSM7bij_3wPlF_A6yY/edit?usp=sharing)
- **MCP SDK:** https://github.com/modelcontextprotocol/sdk

---

## 🎉 Get Started

Ready to build skills?

1. **Read [SETUP.md](SETUP.md)** - Set up MCP servers
2. **Upload skills-builder.zip** to Claude Desktop
3. **Create your first skill!**

```
"Create a skill that helps me organize my project notes"
```

**Happy skill building! 🚀**
