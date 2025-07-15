import argparse
import os
import sys
from .checker import check_github_commits, check_local_commits
from .config import config_exists, load_config, prompt_config
from .uninstaller import full_uninstall

from .bootstrap import bootstrap
from .updater import check_for_updates

# Parse early to check for --check-only flag
import argparse
early_parser = argparse.ArgumentParser(add_help=False)
early_parser.add_argument("--check-only", action="store_true")
early_args, _ = early_parser.parse_known_args()

if not early_args.check_only:
    bootstrap()
    check_for_updates()

def main():
    if not config_exists():
        config = prompt_config()
    else:
        config = load_config()

    parser = argparse.ArgumentParser(description="Check today's GitHub + local commits.")
    parser.add_argument("--setup", action="store_true", help="Reset your config")
    parser.add_argument("--uninstall", action="store_true", help="Completely remove commit-checker from your system")
    parser.add_argument("--support", action="store_true", help="Show donation link to support dev")
    parser.add_argument("--silent", action="store_true", help="Minimal output (clean log mode)")
    parser.add_argument("--nocolor", action="store_true", help="Disable emojis and colors in output")
    parser.add_argument("--check-only", action="store_true", help="Run check without startup actions")
    parser.add_argument("--update", action="store_true", help="Manually check for new GitHub version")
    args = parser.parse_args()

    if args.uninstall:
        confirm = input("⚠️  This will completely remove commit-checker from your system. Continue? [y/N]: ").lower()
        if confirm in ["y", "yes"]:
            full_uninstall()
        else:
            print("❌ Uninstall cancelled.")
        sys.exit(0)

    if args.support:
        print("💖 Support commit-checker development!")
        print("📬 PayPal: amariah.abish@gmail.com")
        print("🌐 GitHub: https://github.com/AmariahAK")
        print("📱 Portfolio: https://portfolio-pied-five-61.vercel.app")
        print("\nEven small support helps keep the streak alive for devs worldwide 🌍")
        sys.exit(0)

    if args.update:
        from .updater import check_for_updates
        check_for_updates()
        sys.exit(0)

    if args.setup:
        config = prompt_config()

    # Handle output formatting based on flags
    def format_output(text, emoji="", color=True):
        if args.nocolor:
            # Strip emojis and simplify output
            text = text.replace("🌐", "").replace("🟢", "").replace("🟩", "")
            text = text.replace("✅", "").replace("😢", "").replace("📁", "")
            text = text.replace("🗂️", "").replace(" — ", " - ")
            return text.strip()
        return text

    def output(text, emoji=""):
        if not args.silent:
            print(format_output(text, emoji))

    def silent_output(text):
        if args.silent:
            print(format_output(text))

    output(f"🌐 GitHub: @{config['github_username']}")
    error, commits = check_github_commits(config["github_username"], config["github_token"])
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

    output(f"\n🗂️  Scanning local path: {config['local_path']}")
    local = check_local_commits(config["local_path"])
    if not local:
        output("😢 No local commits found today.")
        silent_output("No local commits today")
    else:
        output("\n🟩 Local Commits:")
        for path, log in local:
            output(f"📁 {path}:\n{log}\n")
            silent_output(f"{path}: {log.count(chr(10))} commit(s)")
