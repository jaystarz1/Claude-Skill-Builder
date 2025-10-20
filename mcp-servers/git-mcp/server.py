#!/usr/bin/env python3
"""
Git MCP Server for Skills-Builder
Provides git operations that work with absolute filesystem paths
"""

import os
import subprocess
from pathlib import Path
from typing import Optional
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("git-mcp")


def run_git_command(path: str, *args) -> tuple[bool, str, str]:
    """
    Run a git command in the specified directory.
    Returns (success, stdout, stderr)
    """
    try:
        result = subprocess.run(
            ["git", "-C", path, *args],
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


@mcp.tool()
def git_init(path: str) -> str:
    """
    Initialize a git repository at the specified path.
    
    Args:
        path: Absolute path to the directory to initialize
    
    Returns:
        Success message or error details
    """
    path_obj = Path(path).expanduser().resolve()
    
    if not path_obj.exists():
        return f"❌ Error: Directory does not exist: {path}"
    
    success, stdout, stderr = run_git_command(str(path_obj), "init")
    
    if success:
        return f"✅ Initialized git repository at {path}"
    else:
        return f"❌ Failed to initialize git repository\nError: {stderr}"


@mcp.tool()
def git_remote_add(path: str, name: str, url: str) -> str:
    """
    Add a remote repository.
    
    Args:
        path: Absolute path to the git repository
        name: Name of the remote (e.g., "origin")
        url: URL of the remote repository
    
    Returns:
        Success message or error details
    """
    path_obj = Path(path).expanduser().resolve()
    
    if not path_obj.exists():
        return f"❌ Error: Directory does not exist: {path}"
    
    success, stdout, stderr = run_git_command(str(path_obj), "remote", "add", name, url)
    
    if success:
        return f"✅ Added remote '{name}': {url}"
    else:
        # Check if remote already exists
        if "already exists" in stderr:
            return f"ℹ️  Remote '{name}' already exists"
        return f"❌ Failed to add remote\nError: {stderr}"


@mcp.tool()
def git_add(path: str, files: str = ".") -> str:
    """
    Stage files for commit.
    
    Args:
        path: Absolute path to the git repository
        files: Files to stage (default: "." for all files)
    
    Returns:
        Success message or error details
    """
    path_obj = Path(path).expanduser().resolve()
    
    if not path_obj.exists():
        return f"❌ Error: Directory does not exist: {path}"
    
    success, stdout, stderr = run_git_command(str(path_obj), "add", files)
    
    if success:
        return f"✅ Staged files: {files}"
    else:
        return f"❌ Failed to stage files\nError: {stderr}"


@mcp.tool()
def git_commit(path: str, message: str) -> str:
    """
    Commit staged changes.
    
    Args:
        path: Absolute path to the git repository
        message: Commit message
    
    Returns:
        Success message with commit details or error details
    """
    path_obj = Path(path).expanduser().resolve()
    
    if not path_obj.exists():
        return f"❌ Error: Directory does not exist: {path}"
    
    success, stdout, stderr = run_git_command(str(path_obj), "commit", "-m", message)
    
    if success:
        return f"✅ Committed changes\n{stdout}"
    else:
        # Check if there's nothing to commit
        if "nothing to commit" in stdout or "nothing to commit" in stderr:
            return "ℹ️  Nothing to commit (working tree clean)"
        return f"❌ Failed to commit\nError: {stderr}"


@mcp.tool()
def git_push(path: str, remote: str = "origin", branch: str = "main", set_upstream: bool = False) -> str:
    """
    Push commits to remote repository.
    
    Args:
        path: Absolute path to the git repository
        remote: Name of the remote (default: "origin")
        branch: Name of the branch (default: "main")
        set_upstream: Whether to set upstream tracking (default: False)
    
    Returns:
        Success message or error details
    """
    path_obj = Path(path).expanduser().resolve()
    
    if not path_obj.exists():
        return f"❌ Error: Directory does not exist: {path}"
    
    args = ["push"]
    if set_upstream:
        args.extend(["-u", remote, branch])
    else:
        args.extend([remote, branch])
    
    success, stdout, stderr = run_git_command(str(path_obj), *args)
    
    if success:
        return f"✅ Pushed to {remote}/{branch}\n{stderr}"  # Git outputs progress to stderr
    else:
        return f"❌ Failed to push\nError: {stderr}"


@mcp.tool()
def git_pull(path: str, remote: str = "origin", branch: str = "main") -> str:
    """
    Pull changes from remote repository.
    
    Args:
        path: Absolute path to the git repository
        remote: Name of the remote (default: "origin")
        branch: Name of the branch (default: "main")
    
    Returns:
        Success message or error details
    """
    path_obj = Path(path).expanduser().resolve()
    
    if not path_obj.exists():
        return f"❌ Error: Directory does not exist: {path}"
    
    success, stdout, stderr = run_git_command(str(path_obj), "pull", remote, branch)
    
    if success:
        return f"✅ Pulled from {remote}/{branch}\n{stdout}"
    else:
        return f"❌ Failed to pull\nError: {stderr}"


@mcp.tool()
def git_status(path: str) -> str:
    """
    Get the status of the git repository.
    
    Args:
        path: Absolute path to the git repository
    
    Returns:
        Git status output or error details
    """
    path_obj = Path(path).expanduser().resolve()
    
    if not path_obj.exists():
        return f"❌ Error: Directory does not exist: {path}"
    
    success, stdout, stderr = run_git_command(str(path_obj), "status")
    
    if success:
        return stdout
    else:
        return f"❌ Failed to get status\nError: {stderr}"


@mcp.tool()
def git_log(path: str, limit: int = 10) -> str:
    """
    Get the commit history.
    
    Args:
        path: Absolute path to the git repository
        limit: Number of commits to show (default: 10)
    
    Returns:
        Commit history or error details
    """
    path_obj = Path(path).expanduser().resolve()
    
    if not path_obj.exists():
        return f"❌ Error: Directory does not exist: {path}"
    
    success, stdout, stderr = run_git_command(
        str(path_obj), "log", f"--max-count={limit}", "--oneline", "--decorate"
    )
    
    if success:
        return stdout if stdout else "No commits yet"
    else:
        return f"❌ Failed to get log\nError: {stderr}"


@mcp.tool()
def git_branch_set_upstream(path: str, remote: str = "origin", branch: str = "main") -> str:
    """
    Set the upstream tracking branch.
    
    Args:
        path: Absolute path to the git repository
        remote: Name of the remote (default: "origin")
        branch: Name of the branch (default: "main")
    
    Returns:
        Success message or error details
    """
    path_obj = Path(path).expanduser().resolve()
    
    if not path_obj.exists():
        return f"❌ Error: Directory does not exist: {path}"
    
    success, stdout, stderr = run_git_command(
        str(path_obj), "branch", "-u", f"{remote}/{branch}"
    )
    
    if success:
        return f"✅ Set upstream to {remote}/{branch}"
    else:
        return f"❌ Failed to set upstream\nError: {stderr}"


@mcp.tool()
def chmod_executable(path: str, file: str) -> str:
    """
    Make a file executable (chmod +x).
    
    Args:
        path: Absolute path to the directory containing the file
        file: Relative path to the file (from path)
    
    Returns:
        Success message or error details
    """
    path_obj = Path(path).expanduser().resolve()
    file_path = path_obj / file
    
    if not file_path.exists():
        return f"❌ Error: File does not exist: {file_path}"
    
    try:
        # Make file executable (owner, group, others can execute)
        current_mode = file_path.stat().st_mode
        file_path.chmod(current_mode | 0o111)
        return f"✅ Made executable: {file_path}"
    except Exception as e:
        return f"❌ Failed to make file executable\nError: {str(e)}"


@mcp.tool()
def git_fetch(path: str, remote: str = "origin") -> str:
    """
    Fetch changes from remote repository.
    
    Args:
        path: Absolute path to the git repository
        remote: Name of the remote (default: "origin")
    
    Returns:
        Success message or error details
    """
    path_obj = Path(path).expanduser().resolve()
    
    if not path_obj.exists():
        return f"❌ Error: Directory does not exist: {path}"
    
    success, stdout, stderr = run_git_command(str(path_obj), "fetch", remote)
    
    if success:
        return f"✅ Fetched from {remote}\n{stderr}"  # Git outputs to stderr
    else:
        return f"❌ Failed to fetch\nError: {stderr}"


if __name__ == "__main__":
    mcp.run()
