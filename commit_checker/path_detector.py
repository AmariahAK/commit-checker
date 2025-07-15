import os
import subprocess
import platform
from pathlib import Path

def is_git_repo(path):
    """Check if a directory is a git repository"""
    try:
        subprocess.run(['git', 'rev-parse', '--git-dir'], 
                      cwd=path, capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_current_git_repo():
    """Get current directory if it's a git repo"""
    current_dir = os.getcwd()
    if is_git_repo(current_dir):
        return current_dir
    return None

def get_common_dev_paths():
    """Get common development folder paths based on OS"""
    home = Path.home()
    system = platform.system().lower()
    
    common_paths = []
    
    # Cross-platform common paths
    common_names = [
        'Documents/GitHub', 'Documents/Github', 'Documents/git',
        'github', 'Github', 'git', 'dev', 'Development', 'code', 'Code',
        'projects', 'Projects', 'workspace', 'Workspace', 'src'
    ]
    
    # Add paths relative to home directory
    for name in common_names:
        path = home / name
        if path.exists() and path.is_dir():
            common_paths.append(str(path))
    
    # Platform-specific paths
    if system == 'darwin':  # macOS
        mac_paths = [
            home / 'Developer',
            home / 'Desktop/GitHub',
            home / 'Desktop/Projects',
            '/Applications/XAMPP/htdocs',
            '/usr/local/var/www'
        ]
        for path in mac_paths:
            if path.exists() and path.is_dir():
                common_paths.append(str(path))
                
    elif system == 'linux':
        linux_paths = [
            home / 'workspace',
            home / 'devel',
            '/var/www',
            '/opt/lampp/htdocs',
            '/home/git'
        ]
        for path in linux_paths:
            if path.exists() and path.is_dir():
                common_paths.append(str(path))
                
    elif system == 'windows':
        windows_paths = [
            home / 'source',
            home / 'Source',
            'C:\\inetpub\\wwwroot',
            'C:\\xampp\\htdocs',
            'C:\\wamp\\www',
            'D:\\Projects',
            'C:\\Projects'
        ]
        for path in windows_paths:
            path_obj = Path(path)
            if path_obj.exists() and path_obj.is_dir():
                common_paths.append(str(path_obj))
    
    return common_paths

def find_git_repos_in_path(base_path, max_depth=2):
    """Find git repositories in a given path"""
    git_repos = []
    base_path = Path(base_path)
    
    if not base_path.exists():
        return git_repos
    
    try:
        # Check if base path itself is a git repo
        if is_git_repo(base_path):
            git_repos.append(str(base_path))
            return git_repos
        
        # Search for git repos in subdirectories
        for root, dirs, files in os.walk(base_path):
            # Calculate current depth
            current_depth = len(Path(root).parts) - len(base_path.parts)
            if current_depth > max_depth:
                continue
                
            if '.git' in dirs:
                git_repos.append(root)
                # Don't search within this git repo
                dirs.clear()
                
    except PermissionError:
        # Skip directories we can't access
        pass
        
    return git_repos

def get_suggested_paths():
    """Get suggested paths for the user"""
    suggestions = []
    
    # Current directory if it's a git repo
    current_repo = get_current_git_repo()
    if current_repo:
        suggestions.append(f"Current directory: {current_repo}")
    
    # Common dev paths with git repos
    common_paths = get_common_dev_paths()
    for path in common_paths:
        git_repos = find_git_repos_in_path(path, max_depth=1)
        if git_repos:
            suggestions.append(f"{path} ({len(git_repos)} git repos found)")
    
    return suggestions

def auto_detect_dev_paths():
    """Auto-detect development paths"""
    detected_paths = []
    
    # Add current directory if it's a git repo
    current_repo = get_current_git_repo()
    if current_repo:
        detected_paths.append(current_repo)
    
    # Check common paths for git repos
    common_paths = get_common_dev_paths()
    for path in common_paths:
        git_repos = find_git_repos_in_path(path, max_depth=2)
        if git_repos:
            detected_paths.append(path)
    
    return detected_paths

def get_best_default_path():
    """Get the best default path for the user"""
    # Try current directory first
    current_repo = get_current_git_repo()
    if current_repo:
        return current_repo
    
    # Try common paths
    common_paths = get_common_dev_paths()
    for path in common_paths:
        git_repos = find_git_repos_in_path(path, max_depth=1)
        if git_repos:
            return path
    
    # Fallback to home directory
    return str(Path.home())
