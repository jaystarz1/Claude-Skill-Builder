# Zip Creator MCP Setup Guide

This guide walks you through setting up the zip-creator MCP server, which allows Claude to automatically create ZIP files for your skills.

---

## Why Install This?

**Without zip-creator MCP:**
- Skills-builder uses Python fallback to create ZIPs
- Works fine, just slightly slower

**With zip-creator MCP:**
- Faster ZIP creation
- More reliable
- Better error messages
- Cleaner implementation

**Recommendation:** Install it for the best experience, but skills-builder works fine without it!

---

## Prerequisites

- **Python 3.8+** installed
- **Filesystem MCP** already set up (see SETUP.md)
- Basic terminal familiarity

---

## Installation Steps

### Step 1: Create MCP Directory

```bash
mkdir -p ~/mcp-servers/zip-creator
cd ~/mcp-servers/zip-creator
```

### Step 2: Create the MCP Server Script

Create a file called `server.py`:

```python
#!/usr/bin/env python3
"""
Zip Creator MCP Server
Creates ZIP files from directories, excluding git and other unnecessary files.
"""

import asyncio
import json
import zipfile
from pathlib import Path
from typing import Any

# MCP server imports
try:
    from mcp.server.models import InitializationOptions
    from mcp.server import NotificationOptions, Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
    from pydantic import AnyUrl
except ImportError:
    print("Error: MCP SDK not installed. Run: pip install mcp", file=sys.stderr)
    sys.exit(1)


# Create server instance
server = Server("zip-creator")


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="create_zip",
            description=(
                "Create a ZIP file from a directory. Excludes .git folders and existing .zip files. "
                "Useful for packaging Claude Skills and other projects."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "directory_path": {
                        "type": "string",
                        "description": "Absolute path to the directory to zip"
                    },
                    "zip_name": {
                        "type": "string",
                        "description": "Name for the ZIP file (e.g., 'my-skill.zip')"
                    }
                },
                "required": ["directory_path", "zip_name"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls."""
    if name != "create_zip":
        raise ValueError(f"Unknown tool: {name}")
    
    # Get arguments
    directory_path = arguments.get("directory_path")
    zip_name = arguments.get("zip_name")
    
    if not directory_path or not zip_name:
        raise ValueError("Both directory_path and zip_name are required")
    
    # Convert to Path objects
    dir_path = Path(directory_path).resolve()
    
    # Validate directory exists
    if not dir_path.exists():
        raise ValueError(f"Directory does not exist: {directory_path}")
    
    if not dir_path.is_dir():
        raise ValueError(f"Path is not a directory: {directory_path}")
    
    # Determine output path (in the same directory being zipped)
    zip_path = dir_path / zip_name
    
    # Create the ZIP file
    try:
        files_added = 0
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in dir_path.rglob('*'):
                # Skip if it's a directory
                if file_path.is_dir():
                    continue
                
                # Skip .git folders
                if '.git' in file_path.parts:
                    continue
                
                # Skip existing .zip files
                if file_path.suffix == '.zip':
                    continue
                
                # Skip __pycache__ and .pyc files
                if '__pycache__' in file_path.parts or file_path.suffix == '.pyc':
                    continue
                
                # Skip .DS_Store
                if file_path.name == '.DS_Store':
                    continue
                
                # Add file to ZIP
                arcname = file_path.relative_to(dir_path)
                zipf.write(file_path, arcname)
                files_added += 1
        
        result_message = f"✅ Created {zip_name} with {files_added} files"
        
        return [
            TextContent(
                type="text",
                text=json.dumps({
                    "success": True,
                    "zip_file": str(zip_path),
                    "files_added": files_added,
                    "message": result_message
                }, indent=2)
            )
        ]
    
    except Exception as e:
        raise RuntimeError(f"Failed to create ZIP file: {str(e)}")


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="zip-creator",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                )
            )
        )


if __name__ == "__main__":
    asyncio.run(main())
```

### Step 3: Make the Script Executable

**Mac/Linux:**
```bash
chmod +x ~/mcp-servers/zip-creator/server.py
```

**Windows:**
No action needed (Python scripts are executable by default)

### Step 4: Install MCP SDK

The server needs the MCP Python SDK:

```bash
pip install mcp
```

Or if you prefer virtual environments:

```bash
cd ~/mcp-servers/zip-creator
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install mcp
```

### Step 5: Test the Server

Test that it works:

```bash
python3 ~/mcp-servers/zip-creator/server.py
```

You should see it waiting for input (that's good!). Press `Ctrl+C` to exit.

---

## Configuration

### Add to Claude Desktop Config

**Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Add the zip-creator to your existing config:

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

**Important:**
- Replace `/absolute/path/to/zip-creator/server.py` with the actual path
- Use `python3` or `python` depending on your system
- If using a virtual environment, use the full path to the venv Python:
  ```json
  "command": "/absolute/path/to/zip-creator/venv/bin/python3"
  ```

### Platform-Specific Examples

**Mac:**
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "node",
      "args": [
        "/Users/alice/mcp-servers/filesystem-mcp/dist/index.js",
        "/Users/alice"
      ]
    },
    "zip-creator": {
      "command": "python3",
      "args": [
        "/Users/alice/mcp-servers/zip-creator/server.py"
      ]
    }
  }
}
```

**Windows:**
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "node",
      "args": [
        "C:\\Users\\alice\\mcp-servers\\filesystem-mcp\\dist\\index.js",
        "C:\\Users\\alice"
      ]
    },
    "zip-creator": {
      "command": "python",
      "args": [
        "C:\\Users\\alice\\mcp-servers\\zip-creator\\server.py"
      ]
    }
  }
}
```

**Linux:**
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "node",
      "args": [
        "/home/alice/mcp-servers/filesystem-mcp/dist/index.js",
        "/home/alice"
      ]
    },
    "zip-creator": {
      "command": "python3",
      "args": [
        "/home/alice/mcp-servers/zip-creator/server.py"
      ]
    }
  }
}
```

---

## Verification

### Step 1: Restart Claude Desktop

After saving the config, completely quit and restart Claude Desktop.

### Step 2: Check Available Tools

Start a new chat and ask:
```
"Can you list your available MCP tools?"
```

You should see `zip-creator:create_zip` in the list.

### Step 3: Test It

Ask Claude:
```
"Can you test the zip-creator MCP by creating a test ZIP file in a temp directory?"
```

Claude should be able to create a test ZIP and confirm it worked.

---

## Troubleshooting

### "Unknown tool: zip-creator:create_zip"

**Problem:** MCP server not loading

**Solutions:**
1. Check config file syntax (valid JSON)
2. Verify Python path is correct
3. Make sure MCP SDK is installed: `pip list | grep mcp`
4. Restart Claude Desktop completely

### "Module 'mcp' not found"

**Problem:** MCP SDK not installed

**Solution:**
```bash
pip install mcp
```

Or if you installed in a virtual environment, make sure the config points to the venv Python.

### "Permission denied" on Mac/Linux

**Problem:** Script not executable

**Solution:**
```bash
chmod +x ~/mcp-servers/zip-creator/server.py
```

### Server starts but doesn't respond

**Problem:** Stdio communication issue

**Solution:**
1. Test the script directly: `python3 server.py`
2. Check Claude Desktop logs for errors
3. Verify the script path is absolute

---

## How It Works

When Claude calls the tool:

1. **Input:** Directory path + ZIP filename
2. **Process:**
   - Walks through all files in directory
   - Excludes: `.git/`, `__pycache__/`, `.zip` files, `.DS_Store`
   - Adds each file to ZIP with relative paths
3. **Output:** Success message with file count

**Example:**
```python
zip-creator:create_zip(
  directory_path="/Users/alice/skills/my-skill",
  zip_name="my-skill.zip"
)
# Creates: /Users/alice/skills/my-skill/my-skill.zip
```

---

## Benefits Over Python Fallback

| Feature | With MCP | Without MCP (Fallback) |
|---------|----------|------------------------|
| Speed | Fast (direct tool call) | Slower (bash + Python) |
| Error Messages | Detailed, structured | Basic |
| File Count | Returned in response | Not available |
| Integration | Native MCP tool | Shell script |
| Reliability | More reliable | Works but less robust |

---

## Uninstalling

To remove the zip-creator MCP:

1. Remove from `claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "filesystem": {
         // Keep this
       }
       // Remove zip-creator section
     }
   }
   ```

2. Restart Claude Desktop

3. (Optional) Delete the directory:
   ```bash
   rm -rf ~/mcp-servers/zip-creator
   ```

Skills-builder will automatically fall back to Python script method.

---

## Advanced: Using Virtual Environments

If you want to keep the MCP SDK isolated:

```bash
# Create virtual environment
cd ~/mcp-servers/zip-creator
python3 -m venv venv

# Activate it
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows

# Install MCP SDK
pip install mcp

# Update config to use venv Python
```

Then in `claude_desktop_config.json`:

```json
"zip-creator": {
  "command": "/absolute/path/to/zip-creator/venv/bin/python3",
  "args": [
    "/absolute/path/to/zip-creator/server.py"
  ]
}
```

---

## Notes

- The ZIP file is created **inside** the directory being zipped
- Existing ZIP files are automatically excluded (prevents zip-in-zip)
- The server is stateless - each ZIP operation is independent
- File paths in the ZIP use relative paths from the source directory

---

## See Also

- **Main Setup Guide:** `../SETUP.md`
- **Filesystem MCP Guide:** https://docs.google.com/document/d/1UrH2zf0W_PABbaIJXUftcGF07zSM7bij_3wPlF_A6yY/edit?usp=sharing
- **Skills-Builder Documentation:** `../SKILL.md`
- **MCP SDK Documentation:** https://github.com/modelcontextprotocol/python-sdk

---

**That's it! The zip-creator MCP is optional but makes the skills-builder experience even smoother. 🚀**
