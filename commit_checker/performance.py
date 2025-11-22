"""Performance optimization utilities for commit-checker.

Provides:
- Async/parallel git operations for faster repository scanning
- Caching utilities for profile and git data
- Optimized commit querying
"""
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache
import hashlib
import json

# Cache for git command results to avoid redundant calls
_git_cache = {}
_cache_enabled = True

def enable_git_cache(enabled=True):
    """Enable or disable git command caching."""
    global _cache_enabled
    _cache_enabled = enabled

def clear_git_cache():
    """Clear the git command cache."""
    global _git_cache
    _git_cache = {}

def cached_git_command(repo_path, command, cache_key=None):
    """Execute git command with caching to avoid redundant calls.
    
    Args:
        repo_path (str): Path to git repository
        command (list): Git command arguments
        cache_key (str): Optional custom cache key
        
    Returns:
        str: Command output
    """
    if not _cache_enabled:
        result = subprocess.run(
            ['git'] + command,
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        return result.stdout.strip() if result.returncode == 0 else ""
    
    # Create cache key from repo path and command
    if cache_key is None:
        cache_key = hashlib.md5(
            f"{repo_path}::{' '.join(command)}".encode()
        ).hexdigest()
    
    if cache_key in _git_cache:
        return _git_cache[cache_key]
    
    result = subprocess.run(
        ['git'] + command,
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    
    output = result.stdout.strip() if result.returncode == 0 else ""
    _git_cache[cache_key] = output
    return output

def parallel_git_operation(repos, operation_func, max_workers=4):
    """Execute git operations in parallel across multiple repositories.
    
    Args:
        repos (list): List of repository paths
        operation_func (callable): Function to execute on each repo
        max_workers (int): Maximum number of parallel workers
        
    Returns:
        dict: Results keyed by repo path
    """
    results = {}
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_repo = {
            executor.submit(operation_func, repo): repo 
            for repo in repos
        }
        
        for future in as_completed(future_to_repo):
            repo = future_to_repo[future]
            try:
                results[repo] = future.result()
            except Exception as e:
                results[repo] = {'error': str(e)}
    
    return results

def get_repo_commits_parallel(repos, since_date=None, max_workers=4):
    """Get commits from multiple repos in parallel.
    
    Args:
        repos (list): List of repository paths
        since_date (str): Optional date filter (e.g., '2025-01-01')
        max_workers (int): Number of parallel workers
        
    Returns:
        dict: Commits by repo path
    """
    def get_commits(repo_path):
        cmd = ['log', '--oneline', '--no-merges']
        if since_date:
            cmd.extend(['--since', since_date])
        
        output = cached_git_command(repo_path, cmd)
        return output.split('\n') if output else []
    
    return parallel_git_operation(repos, get_commits, max_workers)

@lru_cache(maxsize=128)
def get_cached_repo_info(repo_path):
    """Get repository information with LRU caching.
    
    Args:
        repo_path (str): Path to repository
        
    Returns:
        dict: Repo name, branch, etc.
    """
    name = cached_git_command(
        repo_path, 
        ['rev-parse', '--show-toplevel']
    ).split('/')[-1] if os.path.exists(repo_path) else os.path.basename(repo_path)
    
    branch = cached_git_command(repo_path, ['branch', '--show-current'])
    
    return {
        'name': name,
        'branch': branch or 'main',
        'path': repo_path
    }
