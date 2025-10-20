# Skills-Builder Setup Guide

Welcome! This guide will help you set up the skills-builder so you can create professional Claude Skills on your own machine.

---

## 🎯 What You're Setting Up

The skills-builder creates Claude Skills that work on **your filesystem** (not temporary containers). To do this, you need two MCP servers:

1. **Filesystem MCP** - Lets Claude read/write files on your computer
2. **Zip Creator MCP** - Lets Claude automatically package skills into ZIP files

**Without these:** Skills-builder will still work, but files will be created in temporary locations that disappear when you close Claude.

**With these:** Skills-builder creates skills directly in your `~/skills/` directory and automatically packages them for upload!

---

## ⚡ Quick Start (Experienced Users)

If you already have MCP servers set up:

1. Install filesystem MCP with access to your home directory
2. Install zip-creator MCP (optional but recommended)
3. Upload `skills-builder.zip` to Claude Desktop
4. You're ready!

---

## 📚 Detailed Setup (Step-by-Step)

### Prerequisites

- **Node.js 18+** installed ([Download](https://nodejs.org/))
- **Claude Desktop** installed ([Download](https://claude.ai/download))
- **Basic terminal/command line** familiarity

---

### Step 1: Install Filesystem MCP

The filesystem MCP allows Claude to create skills in your `~/skills/` directory.

**📖 Full Installation Guide:**
https://docs.google.com/document/d/1UrH2zf0W_PABbaIJXUftcGF07zSM7bij_3wPlF_A6yY/edit?usp=sharing

**Quick Summary:**

1. Create MCP directory:
   ```bash
   mkdir ~/mcp-servers/filesystem-mcp
   cd ~/mcp-servers/filesystem-mcp
   ```

2. Follow the complete setup instructions in the Google Doc above

3. Add to `claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "filesystem": {
         "command": "node",
         "args": [
           "/absolute/path/to/filesystem-mcp/dist/index.js",
           "/Users/yourname"
         ]
       }
     }
   }
   ```

**⚠️ Important:** Give filesystem MCP access to your **home directory** (`/Users/yourname` on Mac, `/home/yourname` on Linux, `C:\Users\yourname` on Windows) so it can create the `~/skills/` directory.

---

### Step 2: Install Zip Creator MCP (Optional but Recommended)

The zip-creator MCP automatically packages your skills into ZIP files ready for upload.

**📖 Full Setup Instructions:** See `reference/zip-creator-mcp-setup.md`

**Quick Summary:**

1. Create MCP directory:
   ```bash
   mkdir ~/mcp-servers/zip-creator
   cd ~/mcp-servers/zip-creator
   ```

2. Create `server.py`:
   ```python
   # See reference/zip-creator-mcp-setup.md for full code
   ```

3. Add to `claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "filesystem": {
         "command": "node",
         "args": [
           "/absolute/path/to/filesystem-mcp/dist/index.js",
           "/Users/yourname"
         ]
       },
       "zip-creator": {
         "command": "python3",
         "args": [
           "/absolute/path/to/zip-creator/server.py"
         ]
       }
     }
   }
   ```

**Without zip-creator:** Skills-builder will use a Python fallback to create ZIPs (still works fine!)

---

### Step 3: Upload Skills-Builder to Claude Desktop

1. **Locate the ZIP file:**
   - In this repository: `skills-builder.zip`

2. **Upload to Claude:**
   - Open Claude Desktop
   - Go to **Settings → Capabilities**
   - Click **"Upload skill"**
   - Select `skills-builder.zip`

3. **Verify it worked:**
   - Start a new chat
   - Ask: "Can you list your available skills?"
   - You should see `skills-builder` in the list

---

### Step 4: Verify Everything Works

**Test the filesystem MCP:**
```
Ask Claude: "Can you list the allowed directories?"
Expected: Should show your home directory
```

**Test the skills-builder:**
```
Ask Claude: "Create a test skill that says hello"
Expected: Skill created in ~/skills/test-skill/ with automatic ZIP
```

**Check the files:**
```bash
ls ~/skills/
# Should show: test-skill/

ls ~/skills/test-skill/
# Should show: SKILL.md, test-skill.zip, etc.
```

---

## 🔍 Troubleshooting

### "Skills directory not found"

**Problem:** Skills-builder can't find or create `~/skills/`

**Solution:**
1. Make sure filesystem MCP has access to your home directory
2. Check `claude_desktop_config.json` paths are correct
3. Try creating the directory manually: `mkdir ~/skills`

### "ZIP creation failed"

**Problem:** Zip-creator MCP not working or not installed

**Solution:**
- Skills-builder will automatically fall back to Python script
- This is fine! ZIP will still be created
- If you want the MCP: Follow Step 2 above

### "Access denied" errors

**Problem:** Filesystem MCP doesn't have permission

**Solution:**
1. Check `claude_desktop_config.json` includes your home directory
2. Verify paths are absolute, not relative
3. Restart Claude Desktop after config changes

### MCP servers not showing up

**Solution:**
1. Check JSON syntax in `claude_desktop_config.json`
2. Verify all paths are absolute
3. Completely quit and restart Claude Desktop
4. Check terminal logs when starting Claude Desktop

---

## 📁 Expected Directory Structure

After setup, you should have:

```
~/
├── skills/                          # Created by skills-builder
│   ├── test-skill/                  # Example skill you create
│   │   ├── SKILL.md
│   │   ├── test-skill.zip
│   │   └── ...
│   └── another-skill/
│       └── ...
│
├── mcp-servers/                     # MCP servers location
│   ├── filesystem-mcp/
│   │   ├── dist/index.js
│   │   └── ...
│   └── zip-creator/                 # Optional
│       ├── server.py
│       └── ...
│
└── Library/Application Support/Claude/
    └── claude_desktop_config.json   # Config file
```

---

## 🎉 Success!

Once everything is set up, you can:

✅ Create skills that persist on your filesystem  
✅ Have skills automatically packaged into ZIPs  
✅ Immediately upload and use new skills  
✅ Update existing skills with automatic ZIP recreation  

**Try it out:**
```
"Create a skill that helps me write meeting notes"
```

Skills-builder will:
1. Detect your `~/skills/` directory
2. Create the skill with all files
3. Automatically create a ZIP file
4. Tell you where to upload it

---

## 📖 Additional Resources

- **Filesystem MCP Full Guide:** https://docs.google.com/document/d/1UrH2zf0W_PABbaIJXUftcGF07zSM7bij_3wPlF_A6yY/edit?usp=sharing
- **Zip Creator Setup:** `reference/zip-creator-mcp-setup.md`
- **Skills-Builder Documentation:** `SKILL.md`
- **Update Guide:** `UPDATES.md`
- **MCP SDK Documentation:** https://github.com/modelcontextprotocol/sdk

---

## 💡 Tips for Best Results

1. **Start Simple:** Create a basic "hello world" skill first to test everything
2. **Use Projects:** Create Claude Projects with skills-builder in the knowledge
3. **Check Paths:** Always verify paths in config are absolute
4. **Restart Claude:** After config changes, fully quit and restart Claude Desktop
5. **Read Error Messages:** Skills-builder gives detailed error messages to help debug

---

## 🤝 Contributing

Found a bug or want to improve the setup process?

1. Fork this repository
2. Make your changes
3. Submit a pull request

We welcome contributions that make setup easier!

---

## ❓ Still Having Issues?

1. **Check the Google Doc:** The filesystem MCP guide has detailed troubleshooting
2. **Read the error messages:** Skills-builder tries to give helpful error messages
3. **Open an issue:** Describe what's not working and include error messages
4. **Join the discussion:** Check existing issues for similar problems

---

**Happy skill building! 🚀**
