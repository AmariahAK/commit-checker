import subprocess
import os
import requests
from datetime import datetime, timezone

def get_today_date():
    return datetime.now(timezone.utc).date().isoformat()

def check_local_commits(paths):
    """Check local commits in one or more paths"""
    today = get_today_date()
    repos_found = {}  # Use dict to avoid duplicates and group by repo
    
    # Handle both single path (backward compatibility) and multiple paths
    if isinstance(paths, str):
        paths = [paths]
    elif paths is None:
        return []

    for base_path in paths:
        if not base_path or not os.path.exists(base_path):
            continue
            
        for root, dirs, files in os.walk(base_path):
            if '.git' in dirs:
                try:
                    # Get today's commits
                    log = subprocess.check_output(
                        ["git", "--git-dir", os.path.join(root, ".git"), "--work-tree", root,
                         "log", "--since=midnight", "--pretty=format:%h %s"],
                        stderr=subprocess.DEVNULL
                    ).decode("utf-8").strip()
                    
                    if log:
                        # Get repository name
                        repo_name = os.path.basename(root)
                        
                        # Get remote URL to better identify the repo
                        try:
                            remote_url = subprocess.check_output(
                                ["git", "--git-dir", os.path.join(root, ".git"), "--work-tree", root,
                                 "config", "--get", "remote.origin.url"],
                                stderr=subprocess.DEVNULL
                            ).decode("utf-8").strip()
                            
                            # Extract repo name from URL if possible
                            if remote_url:
                                if remote_url.endswith('.git'):
                                    remote_url = remote_url[:-4]
                                repo_name = remote_url.split('/')[-1]
                                
                        except Exception:
                            pass  # Use directory name if can't get remote
                        
                        # Count commits
                        commit_count = len(log.split('\n')) if log else 0
                        
                        # Store unique repos with their info
                        repo_key = f"{repo_name}:{root}"  # Use path to ensure uniqueness
                        if repo_key not in repos_found:
                            repos_found[repo_key] = {
                                'name': repo_name,
                                'path': root,
                                'commits': log,
                                'count': commit_count
                            }
                        
                except Exception:
                    continue
                dirs.clear()  # don't search nested .git repos

    # Convert to list format for compatibility
    return [(repo_info['name'], repo_info['path'], repo_info['commits'], repo_info['count']) 
            for repo_info in repos_found.values()]

def check_github_commits(username, token=None):
    url = f"https://api.github.com/users/{username}/events"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        return f"❌ GitHub API error: {e}", []

    today = get_today_date()
    events = response.json()
    pushes_today = [
        e for e in events if e["type"] == "PushEvent" and e["created_at"].startswith(today)
    ]

    results = []
    for event in pushes_today:
        repo = event["repo"]["name"]
        count = len(event["payload"]["commits"])
        results.append((repo, count))

    return None, results
