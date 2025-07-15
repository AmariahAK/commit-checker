import subprocess
import os
import requests
from datetime import datetime, timezone

def get_today_date():
    return datetime.now(timezone.utc).date().isoformat()

def check_local_commits(paths):
    """Check local commits in one or more paths"""
    today = get_today_date()
    repos_checked = []
    
    # Handle both single path (backward compatibility) and multiple paths
    if isinstance(paths, str):
        paths = [paths]
    elif paths is None:
        return repos_checked

    for base_path in paths:
        if not base_path or not os.path.exists(base_path):
            continue
            
        for root, dirs, files in os.walk(base_path):
            if '.git' in dirs:
                try:
                    log = subprocess.check_output(
                        ["git", "--git-dir", os.path.join(root, ".git"), "--work-tree", root,
                         "log", "--since=midnight", "--pretty=format:%h %s"],
                        stderr=subprocess.DEVNULL
                    ).decode("utf-8").strip()
                    if log:
                        # Make path relative to base_path for cleaner display
                        display_path = os.path.relpath(root, base_path) if root != base_path else os.path.basename(root)
                        repos_checked.append((display_path, log))
                except Exception:
                    continue
                dirs.clear()  # don't search nested .git repos

    return repos_checked

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
