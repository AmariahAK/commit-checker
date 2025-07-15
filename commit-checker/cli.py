import argparse
from .checker import check_local_commits, check_github_commits

def main():
    parser = argparse.ArgumentParser(description="Check GitHub + local commits for today.")
    parser.add_argument("--github", help="GitHub username")
    parser.add_argument("--token", help="GitHub token (optional)")
    parser.add_argument("--local", help="Local repo base path (e.g. ~/Projects)", default=None)

    args = parser.parse_args()

    if args.github:
        print(f"🌍 Checking GitHub commits for @{args.github}...")
        error, commits = check_github_commits(args.github, args.token)
        if error:
            print(error)
        elif not commits:
            print("😢 No public commits found today.")
        else:
            for repo, count in commits:
                print(f"✅ {repo} — {count} commit(s)")

    if args.local:
        print(f"\n📁 Scanning local repos in: {args.local}")
        results = check_local_commits(os.path.expanduser(args.local))
        if not results:
            print("😢 No local commits found today.")
        else:
            for path, log in results:
                print(f"✅ {path}:\n{log}\n")

if __name__ == "__main__":
    main()
