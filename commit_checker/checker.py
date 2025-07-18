import subprocess
import os
import requests
from datetime import datetime, timezone, timedelta

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

def scan_repos(repo_folder):
    """Scan a folder for git repositories and gather commit stats"""
    if not repo_folder or not os.path.exists(repo_folder):
        return []
    
    repos_found = []
    today = get_today_date()
    
    for root, dirs, files in os.walk(repo_folder):
        if '.git' in dirs:
            try:
                repo_name = os.path.basename(root)
                
                # Get remote URL for better repo identification
                try:
                    remote_url = subprocess.check_output(
                        ["git", "--git-dir", os.path.join(root, ".git"), "--work-tree", root,
                         "config", "--get", "remote.origin.url"],
                        stderr=subprocess.DEVNULL
                    ).decode("utf-8").strip()
                    
                    if remote_url:
                        if remote_url.endswith('.git'):
                            remote_url = remote_url[:-4]
                        repo_name = remote_url.split('/')[-1]
                except Exception:
                    pass  # Use directory name if can't get remote
                
                # Count today's commits
                today_log = subprocess.check_output(
                    ["git", "--git-dir", os.path.join(root, ".git"), "--work-tree", root,
                     "log", "--since=midnight", "--oneline"],
                    stderr=subprocess.DEVNULL
                ).decode("utf-8").strip()
                today_count = len(today_log.split('\n')) if today_log else 0
                
                # Count total commits
                total_log = subprocess.check_output(
                    ["git", "--git-dir", os.path.join(root, ".git"), "--work-tree", root,
                     "rev-list", "--all", "--count"],
                    stderr=subprocess.DEVNULL
                ).decode("utf-8").strip()
                total_count = int(total_log) if total_log.isdigit() else 0
                
                # Get date of last commit
                try:
                    last_commit_date = subprocess.check_output(
                        ["git", "--git-dir", os.path.join(root, ".git"), "--work-tree", root,
                         "log", "-1", "--format=%cd", "--date=short"],
                        stderr=subprocess.DEVNULL
                    ).decode("utf-8").strip()
                    
                    # Convert to a more readable format
                    if last_commit_date:
                        commit_date = datetime.strptime(last_commit_date, "%Y-%m-%d")
                        if commit_date.date() == datetime.now().date():
                            last_commit_display = "Today"
                        elif commit_date.date() == (datetime.now() - timedelta(days=1)).date():
                            last_commit_display = "Yesterday"
                        else:
                            last_commit_display = commit_date.strftime("%b %d")
                    else:
                        last_commit_display = "No commits"
                except Exception:
                    last_commit_display = "Unknown"
                
                repos_found.append({
                    'name': repo_name,
                    'path': root,
                    'today_commits': today_count,
                    'total_commits': total_count,
                    'last_commit_date': last_commit_display
                })
                
            except Exception:
                continue
            dirs.clear()  # Don't search nested .git repos
    
    return repos_found

def get_most_active_repo(repo_folder, timeframe="day"):
    """Find the most active repository in a given timeframe"""
    if not repo_folder or not os.path.exists(repo_folder):
        return None
    
    # Set the git log since parameter based on timeframe
    if timeframe == "day":
        since_param = "midnight"
    elif timeframe == "week":
        since_param = "1 week ago"
    elif timeframe == "month":
        since_param = "1 month ago"
    else:
        since_param = "midnight"
    
    most_active = None
    max_commits = 0
    
    for root, dirs, files in os.walk(repo_folder):
        if '.git' in dirs:
            try:
                repo_name = os.path.basename(root)
                
                # Get remote URL for better repo identification
                try:
                    remote_url = subprocess.check_output(
                        ["git", "--git-dir", os.path.join(root, ".git"), "--work-tree", root,
                         "config", "--get", "remote.origin.url"],
                        stderr=subprocess.DEVNULL
                    ).decode("utf-8").strip()
                    
                    if remote_url:
                        if remote_url.endswith('.git'):
                            remote_url = remote_url[:-4]
                        repo_name = remote_url.split('/')[-1]
                except Exception:
                    pass
                
                # Count commits in timeframe
                log = subprocess.check_output(
                    ["git", "--git-dir", os.path.join(root, ".git"), "--work-tree", root,
                     "log", f"--since={since_param}", "--oneline"],
                    stderr=subprocess.DEVNULL
                ).decode("utf-8").strip()
                commit_count = len(log.split('\n')) if log else 0
                
                if commit_count > max_commits:
                    max_commits = commit_count
                    
                    # Get last commit date
                    try:
                        last_commit_date = subprocess.check_output(
                            ["git", "--git-dir", os.path.join(root, ".git"), "--work-tree", root,
                             "log", "-1", "--format=%cd", "--date=short"],
                            stderr=subprocess.DEVNULL
                        ).decode("utf-8").strip()
                        
                        if last_commit_date:
                            commit_date = datetime.strptime(last_commit_date, "%Y-%m-%d")
                            if commit_date.date() == datetime.now().date():
                                last_activity = "Today"
                            elif commit_date.date() == (datetime.now() - timedelta(days=1)).date():
                                last_activity = "Yesterday"
                            else:
                                last_activity = commit_date.strftime("%b %d")
                        else:
                            last_activity = "No recent commits"
                    except Exception:
                        last_activity = "Unknown"
                    
                    most_active = {
                        'name': repo_name,
                        'path': root,
                        'commits': max_commits,
                        'last_activity': last_activity
                    }
                
            except Exception:
                continue
            dirs.clear()  # Don't search nested .git repos
    
    return most_active
