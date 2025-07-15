#!/bin/bash

# commit-checker - Standalone bash version
# No pip installation required!

SCRIPT_DIR="$HOME/.commit-checker-standalone"
REPO_URL="https://raw.githubusercontent.com/AmariahAK/commit-checker/main"

# Create directory if it doesn't exist
mkdir -p "$SCRIPT_DIR"

# Function to download a file if it doesn't exist or is older than 1 day
download_if_needed() {
    local file="$1"
    local url="$2"
    local full_path="$SCRIPT_DIR/$file"
    
    if [[ ! -f "$full_path" ]] || [[ $(find "$full_path" -mtime +1 2>/dev/null) ]]; then
        echo "📥 Downloading $file..."
        curl -s "$url" -o "$full_path" || {
            echo "❌ Failed to download $file"
            return 1
        }
    fi
}

# Download required Python files
download_if_needed "checker.py" "$REPO_URL/commit_checker/checker.py"
download_if_needed "config.py" "$REPO_URL/commit_checker/config.py"
download_if_needed "path_detector.py" "$REPO_URL/commit_checker/path_detector.py"
download_if_needed "updater.py" "$REPO_URL/commit_checker/updater.py"

# Create a simple Python runner
cat > "$SCRIPT_DIR/run_commit_checker.py" << 'EOF'
#!/usr/bin/env python3
import sys
import os
import subprocess
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import platform

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def ensure_dependency(package):
    """Ensure a Python package is available"""
    try:
        __import__(package)
        return True
    except ImportError:
        print(f"📦 Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--user", "--quiet"])
            return True
        except subprocess.CalledProcessError:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--break-system-packages", "--quiet"])
                return True
            except subprocess.CalledProcessError:
                print(f"⚠️  Could not install {package}. Some features may not work.")
                return False

# Ensure required packages
ensure_dependency("requests")

# Import our modules
try:
    from checker import check_github_commits, check_local_commits
    from config import config_exists, load_config, prompt_config, get_auto_config, save_config
    from path_detector import get_current_git_repo
except ImportError as e:
    print(f"❌ Error importing modules: {e}")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Check today's GitHub + local commits.")
    parser.add_argument("--setup", action="store_true", help="Reset your config")
    parser.add_argument("--uninstall", action="store_true", help="Remove commit-checker")
    parser.add_argument("--support", action="store_true", help="Show donation link")
    parser.add_argument("--silent", action="store_true", help="Minimal output")
    parser.add_argument("--nocolor", action="store_true", help="Disable emojis and colors")
    args = parser.parse_args()

    if args.uninstall:
        import shutil
        script_dir = os.path.dirname(os.path.abspath(__file__))
        confirm = input("⚠️  Remove commit-checker? [y/N]: ").lower()
        if confirm in ["y", "yes"]:
            shutil.rmtree(script_dir)
            print("🗑️  commit-checker removed!")
        sys.exit(0)

    if args.support:
        print("💖 Support commit-checker development!")
        print("📬 PayPal: amariah.abish@gmail.com")
        print("🌐 GitHub: https://github.com/AmariahAK")
        sys.exit(0)

    # Load or create config
    if not config_exists():
        config = get_auto_config()
        if config and config.get('local_paths'):
            print("🔍 Auto-detected your development setup!")
            if not config.get('github_username'):
                username = input("👤 GitHub username: ").strip()
                config['github_username'] = username
                save_config(config)
        else:
            config = prompt_config()
    else:
        config = load_config()

    if args.setup:
        config = prompt_config()

    # Output functions
    def format_output(text):
        if args.nocolor:
            text = text.replace("🌐", "").replace("🟢", "").replace("🟩", "")
            text = text.replace("✅", "").replace("😢", "").replace("📁", "")
            text = text.replace("🗂️", "").replace(" — ", " - ")
            return text.strip()
        return text

    def output(text):
        if not args.silent:
            print(format_output(text))

    def silent_output(text):
        if args.silent:
            print(format_output(text))

    # Check GitHub commits
    if config.get('github_username'):
        output(f"🌐 GitHub: @{config['github_username']}")
        error, commits = check_github_commits(config["github_username"], config.get("github_token"))
        if error:
            output(error)
        elif not commits:
            output("😢 No public commits found today.")
            silent_output("No GitHub commits today")
        else:
            output("\n🟢 GitHub Commits:")
            for repo, count in commits:
                output(f"✅ {repo} — {count} commit(s)")
                silent_output(f"{repo}: {count} commit(s)")

    # Check local commits
    local_paths = config.get('local_paths', [])
    if local_paths:
        output(f"\n🗂️  Scanning {len(local_paths)} local path(s):")
        for path in local_paths:
            if path:
                output(f"   📁 {path}")
    
    local = check_local_commits(local_paths)
    if not local:
        output("😢 No local commits found today.")
        silent_output("No local commits today")
    else:
        output("\n🟩 Local Commits:")
        for path, log in local:
            output(f"📁 {path}:\n{log}\n")
            silent_output(f"{path}: {log.count(chr(10))} commit(s)")

if __name__ == "__main__":
    main()
EOF

# Make it executable
chmod +x "$SCRIPT_DIR/run_commit_checker.py"

# Run the Python script
python3 "$SCRIPT_DIR/run_commit_checker.py" "$@"
