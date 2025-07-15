import argparse
import os
from .checker import check_github_commits, check_local_commits
from .config import config_exists, load_config, prompt_config

from .bootstrap import bootstrap
bootstrap()

from .updater import check_for_updates
check_for_updates()

def main():
    if not config_exists():
        config = prompt_config()
    else:
        config = load_config()

    parser = argparse.ArgumentParser(description="Check today's GitHub + local commits.")
    parser.add_argument("--setup", action="store_true", help="Reset your config")
    args = parser.parse_args()

    if args.setup:
        config = prompt_config()

    print(f"🌐 GitHub: @{config['github_username']}")
    error, commits = check_github_commits(config["github_username"], config["github_token"])
    if error:
        print(error)
    elif not commits:
        print("😢 No public commits found today.")
    else:
        print("\n🟢 GitHub Commits:")
        for repo, count in commits:
            print(f"✅ {repo} — {count} commit(s)")

    print(f"\n🗂️  Scanning local path: {config['local_path']}")
    local = check_local_commits(config["local_path"])
    if not local:
        print("😢 No local commits found today.")
    else:
        print("\n🟩 Local Commits:")
        for path, log in local:
            print(f"📁 {path}:\n{log}\n")
