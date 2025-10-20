# Filesystem MCP Setup Guide

The filesystem MCP is essential for skills-builder to work properly. It allows Claude to create and manage files on your actual filesystem (not temporary container directories).

---

## 📖 Complete Installation Guide

**Full setup instructions are available in this Google Doc:**

🔗 **https://docs.google.com/document/d/1UrH2zf0W_PABbaIJXUftcGF07zSM7bij_3wPlF_A6yY/edit?usp=sharing**

This comprehensive guide includes:
- ✅ Step-by-step installation instructions
- ✅ Platform-specific examples (Mac, Windows, Linux)
- ✅ Complete TypeScript server code
- ✅ Troubleshooting section
- ✅ Security best practices
- ✅ Configuration examples

---

## Quick Summary

The filesystem MCP provides these capabilities to Claude:

- **read_file** - Read text files
- **write_file** - Create or overwrite files
- **edit_file** - Make line-based edits with diff preview
- **create_directory** - Create directories
- **list_directory** - List directory contents
- **directory_tree** - Get recursive directory structure
- **move_file** - Move or rename files
- **search_files** - Search for files by pattern
- **get_file_info** - Get file metadata
- **list_allowed_directories** - Show accessible directories

---

## Why You Need This

**Without filesystem MCP:**
- ❌ Skills-builder creates files in `/home/claude/` (temporary container)
- ❌ Files disappear when Claude session ends
- ❌ You must manually move files to your filesystem
- ❌ Confusing and frustrating experience

**With filesystem MCP:**
- ✅ Skills-builder creates files in `~/skills/` (your actual filesystem)
- ✅ Files persist permanently
- ✅ Immediately usable without manual steps
- ✅ Smooth, professional workflow

---

## Installation Overview

1. **Install Node.js 18+** (if not already installed)
2. **Create the MCP directory and files**
3. **Build the TypeScript code**
4. **Configure Claude Desktop** to use the MCP
5. **Restart Claude Desktop**
6. **Verify** it's working

**Estimated time:** 15-20 minutes for first-time setup

---

## Key Configuration

You'll need to add this to your `claude_desktop_config.json`:

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

**Critical:** Give the MCP access to your **home directory** so it can create `~/skills/`

---

## Platform-Specific Paths

### Mac
- **Config file:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Home directory:** `/Users/yourname`
- **Skills directory:** `/Users/yourname/skills/`

### Linux
- **Config file:** `~/.config/Claude/claude_desktop_config.json`
- **Home directory:** `/home/yourname`
- **Skills directory:** `/home/yourname/skills/`

### Windows
- **Config file:** `%APPDATA%\Claude\claude_desktop_config.json`
- **Home directory:** `C:\Users\yourname`
- **Skills directory:** `C:\Users\yourname\skills\`

---

## Security Considerations

The filesystem MCP:
- ✅ Only accesses directories you explicitly allow
- ✅ Validates all paths to prevent escaping allowed directories
- ✅ Checks symlink targets for security
- ✅ Requires absolute paths in configuration
- ✅ No default access (you must grant it)

**Best practice:** Give it access to your home directory, which allows:
- Creating `~/skills/` directory
- Access to `~/Documents/`, `~/Desktop/`, etc. as needed
- Full control over your personal projects

**Avoid:** Don't give it access to system directories like `/System/`, `/usr/`, or `C:\Windows\`

---

## Verification Steps

After installation, test it works:

1. **Check tools are available:**
   ```
   Ask Claude: "Can you list your available MCP tools?"
   Expected: Should see filesystem tools listed
   ```

2. **Check directory access:**
   ```
   Ask Claude: "Can you list the allowed directories?"
   Expected: Should show your home directory
   ```

3. **Test file creation:**
   ```
   Ask Claude: "Can you create a test file in ~/test.txt with the content 'Hello World'"
   Expected: File created successfully
   ```

4. **Test with skills-builder:**
   ```
   Ask Claude: "Create a simple hello world skill"
   Expected: Skill created in ~/skills/hello-world/
   ```

---

## Troubleshooting

### "Command not found" errors
- Verify Node.js is installed: `node --version`
- Check paths in config are absolute
- Make sure you ran `npm run build`

### Claude can't see the tools
- Verify JSON syntax in config file
- Restart Claude Desktop completely (quit, not just close window)
- Check paths exist and are correct

### "Access denied" errors
- Verify the directory in config args exists
- Use `list_allowed_directories` to check config
- Ensure you have read/write permissions

### Files created in wrong location
- Check that home directory is in the config args
- Verify skills-builder detects the right path
- Make sure `~/skills/` directory exists

---

## What's in the Google Doc

The complete Google Doc includes:

1. **Full Installation Guide**
   - Prerequisites
   - Step-by-step instructions
   - All necessary code

2. **Complete TypeScript Code**
   - `package.json` configuration
   - `tsconfig.json` setup
   - Full `src/index.ts` server implementation

3. **Configuration Examples**
   - Mac example
   - Windows example
   - Linux example

4. **Troubleshooting Section**
   - Common issues and solutions
   - Debug mode instructions
   - Testing procedures

5. **Security Best Practices**
   - Which directories to allow
   - What to avoid
   - Regular maintenance tips

---

## After Installation

Once the filesystem MCP is installed:

1. **Upload skills-builder.zip to Claude Desktop**
2. **Start creating skills!** They'll automatically go to `~/skills/`
3. **Skills persist permanently** on your filesystem
4. **ZIP files created automatically** (with zip-creator MCP) or via Python fallback

---

## Resources

- **📖 Full Installation Guide:** https://docs.google.com/document/d/1UrH2zf0W_PABbaIJXUftcGF07zSM7bij_3wPlF_A6yY/edit?usp=sharing
- **🏠 Main Setup Guide:** `../SETUP.md`
- **📦 Zip Creator Setup:** `zip-creator-mcp-setup.md`
- **🛠️ MCP SDK Documentation:** https://github.com/modelcontextprotocol/sdk

---

## Quick Start for Experienced Users

If you've set up MCP servers before:

```bash
# 1. Create and navigate
mkdir ~/mcp-servers/filesystem-mcp && cd ~/mcp-servers/filesystem-mcp

# 2. Initialize and install
npm init -y
npm install @modelcontextprotocol/sdk zod zod-to-json-schema diff minimatch
npm install --save-dev typescript @types/node @types/diff

# 3. Create tsconfig.json and src/index.ts from Google Doc

# 4. Build
npm run build

# 5. Add to claude_desktop_config.json with your home directory in args

# 6. Restart Claude Desktop
```

---

**For complete instructions, see the Google Doc linked above. It has everything you need! 📖**
