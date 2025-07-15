import argparse
import os
import sys
import importlib.util

# Handle imports for both standalone and package modes
try:
    from .checker import check_github_commits, check_local_commits
    from .config import config_exists, load_config, prompt_config, get_auto_config, save_config
    from .updater import check_for_updates
    from .bootstrap import bootstrap
except ImportError:
    # Standalone mode - load modules directly
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    def load_module(name, path):
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    
    try:
        checker = load_module("checker", os.path.join(current_dir, "checker.py"))
        config = load_module("config", os.path.join(current_dir, "config.py"))
        updater = load_module("updater", os.path.join(current_dir, "updater.py"))
        
        check_github_commits = checker.check_github_commits
        check_local_commits = checker.check_local_commits
        config_exists = config.config_exists
        load_config = config.load_config
        prompt_config = config.prompt_config
        get_auto_config = config.get_auto_config
        save_config = config.save_config
        check_for_updates = updater.check_for_updates
        
        # Simple bootstrap function
        def bootstrap():
            import subprocess
            def ensure_package(package):
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
            
            for pkg in ["requests", "colorama", "packaging"]:
                ensure_package(pkg)
        
    except Exception as e:
        print(f"❌ Error loading modules: {e}")
        sys.exit(1)

def uninstall_package():
    """Remove the commit-checker package via pip"""
    import subprocess
    try:
        print("🗑️  Uninstalling commit-checker package...")
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "commit-checker", "-y"])
        print("✅ Package uninstalled successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Could not uninstall package: {e}")
        return False

def main():
    # Parse early to check for --check-only flag
    early_parser = argparse.ArgumentParser(add_help=False)
    early_parser.add_argument("--check-only", action="store_true")
    early_args, _ = early_parser.parse_known_args()

    if not early_args.check_only:
        try:
            bootstrap()
            check_for_updates()
        except:
            pass  # Continue even if bootstrap/update fails

    # Load or create config
    if not config_exists():
        try:
            config = get_auto_config()
            if config and config.get('local_paths'):
                print("🔍 Auto-detected your development setup!")
                if not config.get('github_username'):
                    username = input("👤 GitHub username: ").strip()
                    config['github_username'] = username
                    save_config(config)
            else:
                config = prompt_config()
        except:
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
            uninstall_package()
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
        try:
            check_for_updates()
        except:
            print("⚠️  Update check failed")
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

    # Check GitHub commits
    if config.get('github_username'):
        output(f"🌐 GitHub: @{config['github_username']}")
        try:
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
        except Exception as e:
            output(f"⚠️  GitHub check failed: {e}")

    # Handle both old and new config formats
    local_paths = config.get('local_paths', [config.get('local_path', '')]) if config.get('local_path') else config.get('local_paths', [])
    
    if local_paths:
        output(f"\n🗂️  Scanning {len(local_paths)} local path(s):")
        for path in local_paths:
            if path:
                output(f"   📁 {path}")
    
    try:
        local = check_local_commits(local_paths)
        if not local:
            output("😢 No local commits found today.")
            silent_output("No local commits today")
        else:
            output("\n🟩 Local Commits:")
            for repo_name, repo_path, commits, count in local:
                output(f"📁 Repository: {repo_name}")
                output(f"   📍 Path: {repo_path}")
                output(f"   📊 {count} commit(s) today:")
                output(f"   {commits}\n")
                silent_output(f"{repo_name}: {count} commit(s)")
    except Exception as e:
        output(f"⚠️  Local check failed: {e}")

if __name__ == "__main__":
    main()
