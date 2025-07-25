import argparse
import os
import sys
import importlib.util

# Handle imports for both standalone and package modes
try:
    from .checker import check_github_commits, check_local_commits, scan_repos, get_most_active_repo
    from .config import config_exists, load_config, prompt_config, get_auto_config, save_config, delete_config
    from .updater import check_for_updates, check_pending_update_on_startup, manual_update_check
    from .bootstrap import bootstrap
    from .til import add_til_entry, view_til, edit_til, reset_til, delete_til, get_til_stats, filter_til_by_tag, export_til
    from .wizard import interactive_setup_wizard, show_commit_stats, run_diagnostics
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
        til = load_module("til", os.path.join(current_dir, "til.py"))
        wizard = load_module("wizard", os.path.join(current_dir, "wizard.py"))
        
        check_github_commits = checker.check_github_commits
        check_local_commits = checker.check_local_commits
        scan_repos = checker.scan_repos
        get_most_active_repo = checker.get_most_active_repo
        config_exists = config.config_exists
        load_config = config.load_config
        prompt_config = config.prompt_config
        get_auto_config = config.get_auto_config
        save_config = config.save_config
        delete_config = config.delete_config
        check_for_updates = updater.check_for_updates
        check_pending_update_on_startup = updater.check_pending_update_on_startup
        manual_update_check = updater.manual_update_check
        add_til_entry = til.add_til_entry
        view_til = til.view_til
        edit_til = til.edit_til
        reset_til = til.reset_til
        delete_til = til.delete_til
        get_til_stats = til.get_til_stats
        filter_til_by_tag = til.filter_til_by_tag
        export_til = til.export_til
        interactive_setup_wizard = wizard.interactive_setup_wizard
        show_commit_stats = wizard.show_commit_stats
        run_diagnostics = wizard.run_diagnostics
        
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

def detect_install_method():
    """Detect how commit-checker was installed"""
    import subprocess
    try:
        # Check if installed via pipx
        pipx_result = subprocess.run([sys.executable, "-m", "pipx", "list"], 
                                   capture_output=True, text=True)
        if pipx_result.returncode == 0 and "commit-checker" in pipx_result.stdout:
            return "pipx"
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    try:
        # Check if installed as regular pip package
        import pkg_resources
        pkg_resources.get_distribution("commit-checker")
        return "pip"
    except (pkg_resources.DistributionNotFound, ImportError):
        pass
    
    # Check if running as standalone script
    if os.path.exists(os.path.expanduser("~/.local/bin/commit-checker")):
        return "standalone"
    
    return "unknown"

def uninstall_package():
    """Remove the commit-checker package via appropriate method and clean up config"""
    import subprocess
    import shutil
    
    install_method = detect_install_method()
    print(f"🔍 Detected installation method: {install_method}")
    
    try:
        if install_method == "pipx":
            print("🗑️  Uninstalling commit-checker via pipx...")
            subprocess.check_call([sys.executable, "-m", "pipx", "uninstall", "commit-checker"])
            print("✅ Package uninstalled successfully via pipx")
            
        elif install_method == "standalone":
            print("🗑️  Removing standalone installation...")
            binary_path = os.path.expanduser("~/.local/bin/commit-checker")
            if os.path.exists(binary_path):
                os.remove(binary_path)
                print(f"🗑️  Removed {binary_path}")
            
            # Remove standalone cache directory
            standalone_dir = os.path.expanduser("~/.commit-checker-standalone")
            if os.path.exists(standalone_dir):
                shutil.rmtree(standalone_dir)
                print(f"🗑️  Removed {standalone_dir}")
            print("✅ Standalone installation removed successfully")
            
        else:
            # Try standard pip uninstall with fallbacks for PEP 668
            print("🗑️  Uninstalling commit-checker package...")
            uninstall_commands = [
                [sys.executable, "-m", "pip", "uninstall", "commit-checker", "-y"],
                [sys.executable, "-m", "pip", "uninstall", "commit-checker", "-y", "--break-system-packages"],
                ["pipx", "uninstall", "commit-checker"]
            ]
            
            success = False
            for cmd in uninstall_commands:
                try:
                    subprocess.check_call(cmd, stderr=subprocess.DEVNULL)
                    print("✅ Package uninstalled successfully")
                    success = True
                    break
                except (subprocess.CalledProcessError, FileNotFoundError):
                    continue
            
            if not success:
                print("⚠️  Could not uninstall via pip. This might be due to PEP 668 (externally managed environment).")
                print("💡 Try one of these alternatives:")
                print("   - If installed with pipx: pipx uninstall commit-checker")
                print("   - If system-managed: python3 -m pip uninstall commit-checker --break-system-packages")
                print("   - Manual removal: Delete ~/.local/bin/commit-checker if it exists")
                print("\n🗑️  Proceeding to clean up configuration files...")
        
        # Remove config directory and files
        print("🗑️  Removing configuration files...")
        
        # Ask about TIL log deletion
        try:
            til_stats = get_til_stats()
            if til_stats and til_stats['entries'] > 0:
                til_confirm = input(f"📝 You have {til_stats['entries']} TIL entries. Delete your TIL log as well? [y/N]: ").lower()
                if til_confirm in ["y", "yes"]:
                    delete_til()
                else:
                    print(f"📝 TIL log preserved at: {til_stats['path']}")
        except:
            pass  # Continue if TIL check fails
        
        delete_config()
        
        # Try to remove binary from common locations
        binary_paths = [
            "/usr/local/bin/commit-checker",
            os.path.expanduser("~/.local/bin/commit-checker")
        ]
        
        for binary_path in binary_paths:
            if os.path.exists(binary_path):
                try:
                    os.remove(binary_path)
                    print(f"🗑️  Removed {binary_path}")
                except Exception:
                    pass
        
        print("✅ Commit Checker has been fully removed.")
        return True
        
    except Exception as e:
        print(f"⚠️  Error during uninstall: {e}")
        print("🗑️  Proceeding to clean up configuration files...")
        delete_config()
        return False

def main():
    # Parse early to check for --check-only flag
    early_parser = argparse.ArgumentParser(add_help=False)
    early_parser.add_argument("--check-only", action="store_true")
    early_args, _ = early_parser.parse_known_args()

    if not early_args.check_only:
        try:
            bootstrap()
            check_pending_update_on_startup()  # Check for pending updates first
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
    parser.add_argument("--init", action="store_true", help="Interactive setup wizard")
    parser.add_argument("--uninstall", action="store_true", help="Completely remove commit-checker from your system")
    parser.add_argument("--support", action="store_true", help="Show donation link to support dev")
    parser.add_argument("--silent", action="store_true", help="Minimal output (clean log mode)")
    parser.add_argument("--nocolor", action="store_true", help="Disable emojis and colors in output")
    parser.add_argument("--check-only", action="store_true", help="Run check without startup actions")
    parser.add_argument("--update", action="store_true", help="Manually check for new GitHub version")
    parser.add_argument("--stats", action="store_true", help="Show ASCII commit trend charts")
    parser.add_argument("--diagnose", action="store_true", help="Run system diagnostics")
    
    # TIL (Today I Learned) functionality
    parser.add_argument("til", nargs="?", help="Add a 'Today I Learned' entry")
    parser.add_argument("--view-til", action="store_true", help="View your TIL log")
    parser.add_argument("--edit-til", action="store_true", help="Edit your TIL log in default editor")
    parser.add_argument("--reset-til", action="store_true", help="Clear your TIL log")
    parser.add_argument("--no-date", action="store_true", help="Add TIL entry without date header")
    parser.add_argument("--tag", type=str, help="Add tag to TIL entry")
    parser.add_argument("--export", choices=["md", "json"], help="Export TIL entries to format")
    parser.add_argument("--filter-tag", type=str, help="Filter TIL entries by tag")
    
    # New feature flags
    parser.add_argument("--scan", action="store_true", help="Scan repo folder for all git repositories")
    parser.add_argument("--repos-summary", action="store_true", help="Show full summary of all local repos")
    parser.add_argument("--most-active", action="store_true", help="Show most active repository")
    parser.add_argument("--day", action="store_true", help="Use with --most-active for daily timeframe")
    parser.add_argument("--week", action="store_true", help="Use with --most-active for weekly timeframe")  
    parser.add_argument("--month", action="store_true", help="Use with --most-active for monthly timeframe")
    parser.add_argument("--force", action="store_true", help="Use with --uninstall to bypass confirmation")
    args = parser.parse_args()

    if args.uninstall:
        if args.force:
            uninstall_package()
        else:
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
            manual_update_check()
        except:
            print("⚠️  Update check failed")
        sys.exit(0)

    if args.setup:
        config = prompt_config()
    
    if args.init:
        if interactive_setup_wizard():
            config = load_config()  # Reload config after wizard
        sys.exit(0)
    
    if args.diagnose:
        run_diagnostics()
        sys.exit(0)
    
    if args.stats:
        local_paths = config.get('local_paths', [])
        if not local_paths:
            print("❌ No local paths configured. Run --init or --setup first.")
            sys.exit(1)
        show_commit_stats(local_paths)
        sys.exit(0)
    
    # Handle TIL commands
    if args.view_til:
        if args.filter_tag:
            success, result = filter_til_by_tag(config, args.filter_tag)
        else:
            success, result = view_til(config)
        
        if success:
            print(result)
        else:
            print(result)
        sys.exit(0)
    
    if args.export:
        success, result = export_til(config, args.export)
        print(result)
        sys.exit(0)
    
    if args.edit_til:
        success, result = edit_til(config)
        print(result)
        sys.exit(0)
    
    if args.reset_til:
        confirm = input("⚠️  This will clear all your TIL entries. Continue? [y/N]: ").lower()
        if confirm in ["y", "yes"]:
            success, result = reset_til(config)
            print(result)
        else:
            print("❌ Reset cancelled.")
        sys.exit(0)
    
    if args.til:
        include_date = not args.no_date
        success, result = add_til_entry(args.til, config, include_date, args.tag)
        print(result)
        sys.exit(0)

    # Handle output formatting based on flags and config
    def format_output(text, emoji="", color=True):
        # Check if user wants plain output or emoji output is disabled
        if args.nocolor or config.get('output') == 'plain':
            # Strip emojis and simplify output
            text = text.replace("🌐", "").replace("🟢", "").replace("🟩", "")
            text = text.replace("✅", "").replace("😢", "").replace("📁", "")
            text = text.replace("🗂️", "").replace(" — ", " - ").replace("→", "->")
            text = text.replace("🧮", "").replace("🕒", "").replace("🔥", "")
            text = text.replace("📅", "").replace("❌", "").replace("🔍", "")
            return text.strip()
        return text

    def output(text, emoji=""):
        if not args.silent:
            print(format_output(text, emoji))

    def silent_output(text):
        if args.silent:
            print(format_output(text))

    # Handle new feature flags first
    if args.scan:
        repo_folder = config.get('repo_folder')
        if not repo_folder:
            print("❌ No repo folder configured. Run --setup first.")
            sys.exit(1)
        
        output(f"🔍 Scanning {repo_folder} for git repositories...")
        repos = scan_repos(repo_folder)
        
        if repos:
            output(f"\n📁 Scanned {len(repos)} repos:\n")
            for repo in repos:
                status_emoji = "✅" if repo['today_commits'] > 0 else "❌"
                if config.get('output') == 'emoji':
                    output(f"{repo['name']} → {status_emoji} {repo['today_commits']} today | 🧮 {repo['total_commits']} total | 🕒 {repo['last_commit_date']}")
                else:
                    output(f"{repo['name']} -> {repo['today_commits']} today | {repo['total_commits']} total | {repo['last_commit_date']}")
        else:
            output("❌ No git repositories found.")
        sys.exit(0)
    
    if args.repos_summary:
        repo_folder = config.get('repo_folder')
        if not repo_folder:
            print("❌ No repo folder configured. Run --setup first.")
            sys.exit(1)
            
        repos = scan_repos(repo_folder)
        if repos:
            if config.get('output') == 'emoji':
                output("🧾 Repo Summary:")
            else:
                output("Repo Summary:")
            for repo in repos:
                status_emoji = "✅" if repo['today_commits'] > 0 else "❌"
                if config.get('output') == 'emoji':
                    output(f"📁 {repo['name']} → {status_emoji} {repo['today_commits']} today | 🧮 {repo['total_commits']} total | 🕒 {repo['last_commit_date']}")
                else:
                    output(f"{repo['name']} -> {repo['today_commits']} today | {repo['total_commits']} total | {repo['last_commit_date']}")
        else:
            output("❌ No git repositories found.")
        sys.exit(0)
    
    if args.most_active:
        repo_folder = config.get('repo_folder')
        if not repo_folder:
            print("❌ No repo folder configured. Run --setup first.")
            sys.exit(1)
            
        # Determine timeframe
        timeframe = "day"  # default
        if args.week:
            timeframe = "week"
        elif args.month:
            timeframe = "month"
        
        most_active = get_most_active_repo(repo_folder, timeframe)
        if most_active and most_active['commits'] > 0:
            if config.get('output') == 'emoji':
                output(f"🔥 Most active repo this {timeframe}:")
                output(f"📁 {most_active['name']} → {most_active['commits']} commits")
                output(f"📅 Last activity: {most_active['last_activity']}")
            else:
                output(f"Most active repo this {timeframe}:")
                output(f"{most_active['name']} -> {most_active['commits']} commits")
                output(f"Last activity: {most_active['last_activity']}")
        else:
            output(f"❌ No active repositories found this {timeframe}.")
        sys.exit(0)

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
