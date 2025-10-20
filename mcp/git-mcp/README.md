# Git MCP Integration

## What It Does
Gives skills-builder (and all skills) access to Git version control operations through MCP tools.

## Setup

### 1. Server Code
The Git MCP server should already be installed at:
```
/Users/jaytarzwell/mcp-simple/servers/src/git/
```

### 2. Add to Config
Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "git": {
      "command": "uvx",
      "args": ["mcp-server-git"]
    }
  }
}
```

### 3. Restart Claude
Restart Claude Desktop for changes to take effect.

## Available Tools
- `git:git_init` - Initialize new repo
- `git:git_status` - Check repo status
- `git:git_add` - Stage files
- `git:git_commit` - Commit changes
- `git:git_push` - Push to remote
- `git:git_pull` - Pull from remote
- `git:git_log` - View commit history
- `git:git_create_branch` - Create branches
- `git:git_checkout` - Switch branches

## How Skills-Builder Uses It

When creating or updating skills, skills-builder automatically:
1. Initializes Git repo (`git:git_init`)
2. Stages all files (`git:git_add`)
3. Creates initial commit (`git:git_commit`)
4. Sets up for push (user provides remote URL)
5. Pushes to remote (`git:git_push`)

## Notes
- Remote URL setup requires one bash command: `git remote add origin [url]`
- All other Git operations are handled automatically via MCP
- Works with any Git hosting (GitHub, GitLab, Bitbucket, etc.)
