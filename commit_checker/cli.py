import argparse
import os
import sys
import importlib.util
from datetime import datetime

# Handle imports for both standalone and package modes
try:
    from .checker import check_github_commits, check_local_commits, scan_repos, get_most_active_repo, get_latest_commit_message
    from .config import (config_exists, load_config, prompt_config, get_auto_config, save_config, delete_config,
                        load_profile, save_profile, is_profile_enabled, needs_profile_rebuild, enable_profile)
    from .profile import (build_profile, suggest_commit_message, get_stack_suggestions, get_structure_suggestions, 
                         play_sound, run_git, get_commit_size_suggestions, get_til_tag_suggestions, update_freeform_feedback)
    from .updater import check_for_updates, check_pending_update_on_startup, manual_update_check
    from .bootstrap import bootstrap
    from .til import add_til_entry, view_til, edit_til, reset_til, delete_til, get_til_stats, filter_til_by_tag, export_til
    from .wizard import interactive_setup_wizard, show_commit_stats, run_diagnostics
    from .gamification import (display_achievements, display_xp_status, process_commits_for_gamification, 
                              create_default_templates, ensure_gamification_files, check_streak_milestone)
    from .analytics import (get_commit_heatmap_data, render_ascii_heatmap, get_language_stats, 
                           render_language_pie_chart, get_mood_commit_line, export_heatmap_svg,
                           analyze_commit_message, get_commit_time_stats, render_time_stats,
                           get_dashboard_stats, render_dashboard)
    from .til_vault import (create_til_from_template, search_til_vault, display_search_results,
                           create_til_from_latest_commit, display_vault_summary, list_templates,
                           add_custom_template)
    from .wisdom import get_latest_wisdom_quote, format_wisdom_quote, refresh_wisdom_quote
    from .context import extract_commit_context, format_context_summary, suggest_conventional_commit_type
    from .ai_handler import get_ai_suggestion, download_ai_models, is_ai_available
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
        profile = load_module("profile", os.path.join(current_dir, "profile.py"))
        updater = load_module("updater", os.path.join(current_dir, "updater.py"))
        til = load_module("til", os.path.join(current_dir, "til.py"))
        wizard = load_module("wizard", os.path.join(current_dir, "wizard.py"))
        gamification = load_module("gamification", os.path.join(current_dir, "gamification.py"))
        analytics = load_module("analytics", os.path.join(current_dir, "analytics.py"))
        til_vault = load_module("til_vault", os.path.join(current_dir, "til_vault.py"))
        
        check_github_commits = checker.check_github_commits
        check_local_commits = checker.check_local_commits
        scan_repos = checker.scan_repos
        get_most_active_repo = checker.get_most_active_repo
        get_latest_commit_message = checker.get_latest_commit_message
        config_exists = config.config_exists
        load_config = config.load_config
        prompt_config = config.prompt_config
        get_auto_config = config.get_auto_config
        save_config = config.save_config
        delete_config = config.delete_config
        load_profile = config.load_profile
        save_profile = config.save_profile
        is_profile_enabled = config.is_profile_enabled
        needs_profile_rebuild = config.needs_profile_rebuild
        enable_profile = config.enable_profile
        build_profile = profile.build_profile
        suggest_commit_message = profile.suggest_commit_message
        get_stack_suggestions = profile.get_stack_suggestions
        get_structure_suggestions = profile.get_structure_suggestions
        get_commit_size_suggestions = profile.get_commit_size_suggestions
        get_til_tag_suggestions = profile.get_til_tag_suggestions
        update_freeform_feedback = profile.update_freeform_feedback
        play_sound = profile.play_sound
        run_git = profile.run_git
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
        
        # Gamification imports
        display_achievements = gamification.display_achievements
        display_xp_status = gamification.display_xp_status
        process_commits_for_gamification = gamification.process_commits_for_gamification
        ensure_gamification_files = gamification.ensure_gamification_files
        check_streak_milestone = gamification.check_streak_milestone
        
        # Analytics imports
        get_commit_heatmap_data = analytics.get_commit_heatmap_data
        render_ascii_heatmap = analytics.render_ascii_heatmap
        get_language_stats = analytics.get_language_stats
        render_language_pie_chart = analytics.render_language_pie_chart
        get_mood_commit_line = analytics.get_mood_commit_line
        export_heatmap_svg = analytics.export_heatmap_svg
        analyze_commit_message = analytics.analyze_commit_message
        get_commit_time_stats = analytics.get_commit_time_stats
        render_time_stats = analytics.render_time_stats
        get_dashboard_stats = analytics.get_dashboard_stats
        render_dashboard = analytics.render_dashboard
        
        # TIL Vault imports
        create_til_from_template = til_vault.create_til_from_template
        search_til_vault = til_vault.search_til_vault
        display_search_results = til_vault.display_search_results
        create_til_from_latest_commit = til_vault.create_til_from_latest_commit
        display_vault_summary = til_vault.display_vault_summary
        list_templates = til_vault.list_templates
        create_default_templates = til_vault.create_default_templates
        add_custom_template = til_vault.add_custom_template
        
        # Wisdom imports
        wisdom = load_module("wisdom", os.path.join(current_dir, "wisdom.py"))
        get_latest_wisdom_quote = wisdom.get_latest_wisdom_quote
        format_wisdom_quote = wisdom.format_wisdom_quote
        refresh_wisdom_quote = wisdom.refresh_wisdom_quote
        
        # Context imports
        context_module = load_module("context", os.path.join(current_dir, "context.py"))
        extract_commit_context = context_module.extract_commit_context
        format_context_summary = context_module.format_context_summary
        suggest_conventional_commit_type = context_module.suggest_conventional_commit_type
        
        # AI handler imports
        ai_handler = load_module("ai_handler", os.path.join(current_dir, "ai_handler.py"))
        get_ai_suggestion = ai_handler.get_ai_suggestion
        download_ai_models = ai_handler.download_ai_models
        is_ai_available = ai_handler.is_ai_available
        
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
            
            for pkg in ["requests", "colorama", "packaging", "markdown"]:
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

def force_uninstall_everything():
    """Nuclear option: Remove ALL traces of commit-checker from system"""
    import subprocess
    import shutil
    
    print("🚨 FORCE UNINSTALL: Removing ALL traces of commit-checker...")
    print("This will completely remove commit-checker from your system.")
    
    confirm = input("⚠️  Continue with complete removal? [y/N]: ").lower()
    if confirm not in ["y", "yes"]:
        print("❌ Uninstall cancelled.")
        return
    
    removed_items = []
    
    try:
        # 1. Remove binary/script files from all possible locations
        binary_paths = [
            os.path.expanduser("~/.local/bin/commit-checker"),
            "/usr/local/bin/commit-checker", 
            "/usr/bin/commit-checker"
        ]
        
        for binary_path in binary_paths:
            if os.path.exists(binary_path):
                try:
                    os.remove(binary_path)
                    removed_items.append(f"Binary: {binary_path}")
                except Exception as e:
                    print(f"⚠️  Could not remove {binary_path}: {e}")
        
        # 2. Remove ALL directories
        directories_to_remove = [
            os.path.expanduser("~/.commit-checker"),
            os.path.expanduser("~/.commit-checker-standalone"),
            os.path.expanduser("~/.cache/commit-checker"),
            os.path.expanduser("~/.local/share/commit-checker")
        ]
        
        for directory in directories_to_remove:
            if os.path.exists(directory):
                try:
                    shutil.rmtree(directory)
                    removed_items.append(f"Directory: {directory}")
                except Exception as e:
                    print(f"⚠️  Could not remove {directory}: {e}")
        
        # 3. Try ALL pip uninstall methods
        pip_commands = [
            [sys.executable, "-m", "pip", "uninstall", "commit-checker", "-y"],
            [sys.executable, "-m", "pip", "uninstall", "commit-checker", "-y", "--break-system-packages"],
            [sys.executable, "-m", "pip", "uninstall", "commit-checker", "-y", "--user"],
            ["pipx", "uninstall", "commit-checker"]
        ]
        
        for cmd in pip_commands:
            try:
                subprocess.check_call(cmd, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
                removed_items.append(f"Package: pip/pipx")
                break  
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
        
        # 4. Clean ALL shell files thoroughly - this was the main issue
        shell_files = [
            os.path.expanduser("~/.bashrc"),
            os.path.expanduser("~/.zshrc"),
            os.path.expanduser("~/.bash_profile"), 
            os.path.expanduser("~/.profile"),
            os.path.expanduser("~/.config/fish/config.fish"),
            os.path.expanduser("~/.zprofile"),
            os.path.expanduser("~/.bash_login"),
            os.path.expanduser("~/.zshenv")
        ]
        
        for shell_file in shell_files:
            if os.path.exists(shell_file):
                try:
                    with open(shell_file, 'r') as f:
                        content = f.read()
                    
                    # Remove commit-checker lines
                    lines = content.split('\n')
                    cleaned_lines = []
                    
                    for line in lines:
                        # Skip lines mentioning commit-checker
                        if 'commit-checker' in line.lower():
                            continue
                        # Skip auto-run comments  
                        if line.strip().startswith('#') and ('auto-run' in line.lower() or 'commit-checker' in line.lower()):
                            continue
                        cleaned_lines.append(line)
                    
                    # Write back if changed
                    cleaned_content = '\n'.join(cleaned_lines)
                    if cleaned_content != content:
                        with open(shell_file, 'w') as f:
                            f.write(cleaned_content)
                        removed_items.append(f"Shell: {shell_file}")
                        
                except Exception as e:
                    print(f"⚠️  Could not clean {shell_file}: {e}")
        
        # Show what was removed
        if removed_items:
            print("\n✅ ENHANCED UNINSTALL COMPLETE!")
            print("🗑️  Removed:")
            for item in removed_items:
                print(f"   • {item}")
        
        print("\n💡 Restart your terminal to complete removal")
        print("🔄 Fresh install: curl -s https://raw.githubusercontent.com/AmariahAK/commit-checker/main/scripts/install-standalone.sh | bash")
        
        # Legacy code below - keeping for compatibility but won't execute
        if False and install_method == "pipx":
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
        
        # Remove shell startup commands
        print("🗑️  Removing shell startup commands...")
        shell_files = [
            os.path.expanduser("~/.bashrc"),
            os.path.expanduser("~/.zshrc"),
            os.path.expanduser("~/.bash_profile"),
            os.path.expanduser("~/.profile"),
            os.path.expanduser("~/.config/fish/config.fish")
        ]
        
        for shell_file in shell_files:
            if os.path.exists(shell_file):
                try:
                    with open(shell_file, 'r') as f:
                        content = f.read()
                    
                    # Remove commit-checker auto-run lines
                    lines = content.split('\n')
                    cleaned_lines = []
                    skip_next = False
                    
                    for i, line in enumerate(lines):
                        # Skip lines containing commit-checker
                        if 'commit-checker' in line:
                            continue
                        # Skip comment lines that mention commit-checker
                        if line.strip().startswith('#') and 'commit-checker' in line.lower():
                            continue
                        # Skip empty lines that come after commit-checker blocks
                        if line.strip() == '' and i > 0 and 'commit-checker' in lines[i-1]:
                            continue
                        cleaned_lines.append(line)
                    
                    # Write back cleaned content
                    cleaned_content = '\n'.join(cleaned_lines)
                    if cleaned_content != content:
                        with open(shell_file, 'w') as f:
                            f.write(cleaned_content)
                        print(f"🗑️  Cleaned startup commands from {shell_file}")
                
                except Exception as e:
                    print(f"⚠️  Could not clean {shell_file}: {e}")
        
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
            # Skip update checks for profile commands to avoid interruption
            if '--build-profile' not in ' '.join(sys.argv) and '--coach' not in ' '.join(sys.argv) and '--insights' not in ' '.join(sys.argv):
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
    parser.add_argument("--refresh-quote", action="store_true", help="Force refresh Wisdom Drop quote")
    parser.add_argument("--stats", action="store_true", help="Show ASCII commit trend charts")
    parser.add_argument("--diagnose", action="store_true", help="Run system diagnostics")
    parser.add_argument("--version", action="store_true", help="Show version information")
    
    # Smart Profile System flags
    parser.add_argument("--build-profile", action="store_true", help="Build or rebuild your coding profile")
    parser.add_argument("--coach", type=str, nargs='?', const='', help="Get commit message coaching suggestions")
    parser.add_argument("--insights", action="store_true", help="Show personalized coding insights")
    parser.add_argument("--no-profile", action="store_true", help="Skip profile-based suggestions")
    parser.add_argument("--feedback", choices=["good", "bad"], help="Give feedback on coaching suggestions")
    
    # Gamification features
    parser.add_argument("--achievements", action="store_true", help="Display achievement gallery")
    parser.add_argument("--xp", action="store_true", help="Show current XP and level status")
    
    # Analytics features
    parser.add_argument("--heatmap", action="store_true", help="Display ASCII commit heatmap")
    parser.add_argument("--heatmap-days", type=int, default=365, help="Days to include in heatmap (default: 365)")
    parser.add_argument("--heatmap-export", choices=["svg"], help="Export heatmap to SVG file")
    parser.add_argument("--stats-lang", action="store_true", help="Show programming language breakdown")
    parser.add_argument("--time-stats", action="store_true", help="Show commit time analysis")
    parser.add_argument("--dashboard", action="store_true", help="Show quick stats dashboard")
    parser.add_argument("--suggest", type=str, nargs='?', const='', help="Suggest a better commit message (optional draft message)")
    
    # Wisdom Drop & AI features
    parser.add_argument("--download-models", action="store_true", help="Download AI models for commit suggestions")
    parser.add_argument("--repair", action="store_true", help="Attempt to auto-repair local assets/config")
    parser.add_argument("--debug", action="store_true", help="Show debug information for troubleshooting")
    
    # Enhanced TIL features
    parser.add_argument("--search-til", type=str, help="Fuzzy search TIL entries")
    parser.add_argument("--til-vault", action="store_true", help="Show TIL vault summary")
    parser.add_argument("--til-from-diff", action="store_true", help="Create TIL from latest commit diff")
    parser.add_argument("--template", type=str, help="Use template for TIL entry")
    parser.add_argument("--list-templates", action="store_true", help="List available TIL templates")
    parser.add_argument("--add-template", type=str, nargs=2, metavar=('NAME', 'STRUCTURE'), help="Add custom TIL template")
    
    # TIL (Today I Learned) functionality
    parser.add_argument("til", nargs="*", help="Add a 'Today I Learned' entry")
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
            force_uninstall_everything()
        else:
            confirm = input("⚠️  This will completely remove commit-checker from your system. Continue? [y/N]: ").lower()
            if confirm in ["y", "yes"]:
                force_uninstall_everything()
            else:
                print("❌ Uninstall cancelled.")
        sys.exit(0)

    if args.support:
        print("💖 Support commit-checker development!")
        print("☕ Buy Me A Coffee: https://buymeacoffee.com/amariahak")
        print("🌐 GitHub: https://github.com/AmariahAK")
        print("📱 Portfolio: https://portfolio-pied-five-61.vercel.app")
        print("\nEven small support helps keep the streak alive for devs worldwide 🌍")
        sys.exit(0)

    if args.version:
        print("🚀 commit-checker v0.7.8")
        print("💡 AI Commit Mentor with Wisdom Drop Integration")
        print("🔗 https://github.com/AmariahAK/commit-checker")
        sys.exit(0)

    if args.update:
        try:
            manual_update_check()
        except:
            print("⚠️  Update check failed")
        sys.exit(0)
    
    if args.download_models:
        try:
            download_ai_models()
            print("✅ AI models downloaded.")
        except Exception as e:
            print(f"⚠️  Could not download AI models: {e}")
        sys.exit(0)
    
    if args.refresh_quote:
        try:
            refresh_wisdom_quote()
        except Exception as e:
            print(f"⚠️  Could not refresh Wisdom Drop: {e}")
        sys.exit(0)
    
    if args.repair:
        try:
            print("🛠️  Repairing commit-checker assets...")
            ensure_gamification_files()
            create_default_templates()
            if needs_profile_rebuild():
                local_paths = load_config().get('local_paths', [])
                if local_paths:
                    print("🔁 Rebuilding profile...")
                    prof = build_profile(local_paths)
                    save_profile(prof)
            print("✅ Repair completed.")
        except Exception as e:
            print(f"⚠️  Repair encountered issues: {e}")
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
    
    # Handle Smart Profile System commands
    if args.build_profile:
        local_paths = config.get('local_paths', [])
        if not local_paths:
            print("❌ No local paths configured. Run --init or --setup first.")
            sys.exit(1)
        
        print("🧙 Building your smart coding profile...")
        print("   📊 Analyzing commit history patterns...")
        print("   🔍 Detecting project tech stacks...")
        print("   📁 Scanning project structures...")
        
        try:
            profile = build_profile(local_paths)
            if save_profile(profile):
                repo_count = len(profile.get("repos", {}))
                print(f"\n✅ Profile built successfully!")
                print(f"   📈 Analyzed {repo_count} repositories")
                print(f"   💡 Smart suggestions now enabled")
                
                # Ask to enable profile if not already enabled
                if not is_profile_enabled():
                    enable_choice = input("\n🧙 Enable profile-based suggestions? [Y/n]: ").strip().lower()
                    if enable_choice != 'n':
                        enable_profile(True)
                        print("✅ Smart profile system activated!")
                        play_sound("notify.wav")
                    else:
                        print("💡 You can enable suggestions later with --build-profile")
                else:
                    play_sound("notify.wav")
            else:
                print("❌ Failed to save profile. Check file permissions.")
        except Exception as e:
            print(f"❌ Profile building failed: {e}")
        
        sys.exit(0)
    
    if args.coach:
        if not is_profile_enabled():
            print("🧙 Smart profile system is disabled.")
            print("💡 Run --build-profile to enable coaching suggestions.")
            sys.exit(1)
        
        profile = load_profile()
        if not profile:
            print("🧙 No profile found. Run --build-profile first.")
            sys.exit(1)
        
        # Get commit message to analyze
        commit_message = args.coach.strip()
        if not commit_message:
            # Try to get from stdin or prompt
            try:
                if not sys.stdin.isatty():
                    commit_message = sys.stdin.read().strip()
            except:
                pass
            
            if not commit_message:
                commit_message = input("💬 Enter commit message to analyze: ").strip()
        
        if not commit_message:
            print("❌ No commit message provided.")
            sys.exit(1)
        
        # Find current repo
        import os
        current_dir = os.getcwd()
        repo_path = current_dir
        
        # Walk up to find .git directory
        while repo_path and repo_path != '/':
            if os.path.exists(os.path.join(repo_path, '.git')):
                break
            repo_path = os.path.dirname(repo_path)
        else:
            repo_path = current_dir  # Fallback to current directory
        
        print(f"🔍 Analyzing: \"{commit_message}\"")
        suggestions = suggest_commit_message(repo_path, profile, commit_message)
        
        # Add commit size suggestions
        size_suggestions = get_commit_size_suggestions(repo_path)
        suggestions.extend(size_suggestions)
        
        if suggestions:
            print("\n💡 Suggestions:")
            for suggestion in suggestions:
                print(f"  {suggestion}")
            play_sound("suggest.wav")
        else:
            print("\n✅ Commit message looks great!")
        
        # Handle feedback
        if args.feedback:
            updated_profile = update_freeform_feedback(profile, repo_path, args.feedback)
            if save_profile(updated_profile):
                feedback_msg = "Thanks! Tuned your preferences." if args.feedback == "good" else "Got it! Less prefix suggestions."
                print(f"\n👍 {feedback_msg}")
                play_sound("notify.wav")
        
        sys.exit(0)
    
    if args.insights:
        if not is_profile_enabled():
            print("🧙 Smart profile system is disabled.")
            print("💡 Run --build-profile to enable insights.")
            sys.exit(1)
        
        profile = load_profile()
        if not profile:
            print("🧙 No profile found. Run --build-profile first.")
            sys.exit(1)
        
        local_paths = config.get('local_paths', [])
        if not local_paths:
            print("❌ No local paths configured.")
            sys.exit(1)
        
        print("🧠 Personal Coding Insights")
        print("=" * 50)
        
        global_profile = profile.get("global", {})
        repos = profile.get("repos", {})
        
        # Global insights
        print(f"📊 Overall Style:")
        print(f"   • Average commit length: {global_profile.get('avg_length', 0)} words")
        print(f"   • Preferred mood: {global_profile.get('mood', 'unknown').title()}")
        print(f"   • Uses emojis: {'Yes' if global_profile.get('uses_emoji', False) else 'No'}")
        
        # Repository insights
        if repos:
            print(f"\n📁 Repository Analysis ({len(repos)} repos):")
            
            # Count tech stacks
            tech_stacks = {}
            for repo_data in repos.values():
                for tech in repo_data.get("tech_stack", []):
                    tech_stacks[tech] = tech_stacks.get(tech, 0) + 1
            
            if tech_stacks:
                print("   🔧 Tech Stack Distribution:")
                for tech, count in sorted(tech_stacks.items(), key=lambda x: x[1], reverse=True):
                    percentage = (count / len(repos)) * 100
                    print(f"     • {tech.title()}: {count} repos ({percentage:.0f}%)")
            
            # Commit style breakdown
            style_counts = {}
            for repo_data in repos.values():
                style = repo_data.get("commit_style", {}).get("case_style", "unknown")
                style_counts[style] = style_counts.get(style, 0) + 1
            
            if style_counts:
                print("   📝 Commit Style Breakdown:")
                for style, count in sorted(style_counts.items(), key=lambda x: x[1], reverse=True):
                    percentage = (count / len(repos)) * 100
                    print(f"     • {style.title()}: {count} repos ({percentage:.0f}%)")
        
        last_scan = profile.get("last_scan", "")
        if last_scan:
            from datetime import datetime
            try:
                scan_date = datetime.fromisoformat(last_scan.replace('Z', '+00:00'))
                print(f"\n🕒 Profile last updated: {scan_date.strftime('%Y-%m-%d %H:%M')}")
            except:
                pass
        
        print("\n💡 Run --build-profile to refresh your profile data")
        play_sound("notify.wav")
        sys.exit(0)
    
    # Initialize gamification on first run
    ensure_gamification_files()
    create_default_templates()
    
    # Handle new gamification commands
    if args.achievements:
        print(display_achievements())
        sys.exit(0)
    
    if args.xp:
        print(display_xp_status())
        sys.exit(0)
    
    # Handle analytics commands
    if args.heatmap:
        local_paths = config.get('local_paths', [])
        if not local_paths:
            print("❌ No local paths configured. Run --init or --setup first.")
            sys.exit(1)
        
        commit_data = get_commit_heatmap_data(local_paths, args.heatmap_days)
        print(render_ascii_heatmap(commit_data, args.heatmap_days))
        
        if args.heatmap_export == "svg":
            output_path = os.path.expanduser(f"~/commit-heatmap-{datetime.now().strftime('%Y%m%d')}.svg")
            success, message = export_heatmap_svg(commit_data, output_path, args.heatmap_days)
            print(message)
        
        sys.exit(0)
    
    if args.stats_lang:
        local_paths = config.get('local_paths', [])
        if not local_paths:
            print("❌ No local paths configured. Run --init or --setup first.")
            sys.exit(1)
        
        language_stats = get_language_stats(local_paths)
        print(render_language_pie_chart(language_stats))
        sys.exit(0)
    
    # Handle new v0.6.2 analytics commands
    if args.time_stats:
        local_paths = config.get('local_paths', [])
        if not local_paths:
            print("❌ No local paths configured. Run --init or --setup first.")
            sys.exit(1)
        
        time_buckets = get_commit_time_stats(local_paths)
        print(render_time_stats(time_buckets))
        sys.exit(0)
    
    if args.dashboard:
        local_paths = config.get('local_paths', [])
        if not local_paths:
            print("❌ No local paths configured. Run --init or --setup first.")
            sys.exit(1)
        
        stats = get_dashboard_stats(local_paths, config)
        print(render_dashboard(stats, config))
        sys.exit(0)
    
    # AI-powered commit message suggestion
    if args.suggest is not None:
        current_dir = os.getcwd()
        repo_path = current_dir
        while repo_path and repo_path != '/':
            if os.path.exists(os.path.join(repo_path, '.git')):
                break
            repo_path = os.path.dirname(repo_path)
        else:
            repo_path = current_dir
        
        draft_message = (args.suggest or "").strip()
        if not draft_message:
            try:
                local_paths = config.get('local_paths', [])
                if local_paths:
                    latest = get_latest_commit_message(local_paths)
                    if latest:
                        draft_message = latest.get('message', '')
            except Exception:
                pass
        
        context_info = None
        conventional_type = None
        try:
            context_info = extract_commit_context(repo_path)
            conventional_type = suggest_conventional_commit_type(context_info)
        except Exception:
            pass
        
        emoji_mode = config.get('output', 'emoji') != 'plain'
        if context_info and context_info.get('has_changes'):
            print("\n🧠 Context summary:" if emoji_mode else "\nContext summary:")
            print(format_context_summary(context_info, emoji_mode))
        
        if conventional_type:
            print(f"\n🔖 Conventional type suggestion: {conventional_type}")
        
        suggestions = []
        try:
            use_ai = is_ai_available()
            profile_obj = None
            
            if use_ai:
                if is_profile_enabled():
                    try:
                        profile_obj = load_profile()
                    except Exception:
                        pass
                
                suggestions_list = get_ai_suggestion(
                    draft_message or "",
                    context=context_info,
                    profile=profile_obj,
                    use_model=use_ai
                )
                if isinstance(suggestions_list, list):
                    suggestions = suggestions_list
                elif isinstance(suggestions_list, str):
                    suggestions = [suggestions_list]
            elif is_profile_enabled() and draft_message:
                try:
                    profile_obj = load_profile()
                    suggestions = suggest_commit_message(repo_path, profile_obj, draft_message)
                except Exception:
                    pass
            
            if not suggestions and draft_message:
                analysis_result = analyze_commit_message(draft_message)
                if isinstance(analysis_result, list):
                    suggestions = analysis_result
        except Exception as e:
            print(f"⚠️  Suggestion engine issue: {e}")
        
        print("\n✨ Suggested commit message:")
        if suggestions:
            for suggestion in suggestions[:3]:
                print(f"  {suggestion}")
        else:
            print("  No strong suggestion available. Try providing a draft or download AI models with --download-models")
        
        try:
            play_sound("suggest.wav")
        except:
            pass
        
        try:
            quote = get_latest_wisdom_quote()
            if quote:
                print()
                print(format_wisdom_quote(quote, emoji_mode=emoji_mode))
        except:
            pass
        
        sys.exit(0)
    
    # Handle enhanced TIL commands
    if args.search_til:
        results = search_til_vault(args.search_til, config)
        print(display_search_results(results))
        sys.exit(0)
    
    if args.til_vault:
        print(display_vault_summary(config))
        sys.exit(0)
    
    if args.til_from_diff:
        local_paths = config.get('local_paths', [])
        if not local_paths:
            print("❌ No local paths configured. Run --init or --setup first.")
            sys.exit(1)
        
        success, result = create_til_from_latest_commit(local_paths, config)
        print(result)
        sys.exit(0)
    
    if args.list_templates:
        templates = list_templates()
        if templates:
            print("📚 Available TIL templates:")
            for template in templates:
                print(f"  • {template}")
            print(f"\nUsage: commit-checker til \"Title\" --template {templates[0]}")
        else:
            print("📚 No templates found. Creating default templates...")
            create_default_templates()
            print("✅ Default templates created!")
        sys.exit(0)
    
    if args.add_template:
        name, structure = args.add_template
        success, result = add_custom_template(name, structure)
        print(result)
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
        # Join the list of words to form the complete TIL title
        til_title = " ".join(args.til)
        
        # Add TIL tag suggestions if profile is enabled and no tag specified
        if not args.tag and is_profile_enabled():
            try:
                profile = load_profile()
                if profile:
                    current_dir = os.getcwd()
                    repo_path = current_dir
                    
                    # Walk up to find .git directory
                    while repo_path and repo_path != '/':
                        if os.path.exists(os.path.join(repo_path, '.git')):
                            break
                        repo_path = os.path.dirname(repo_path)
                    
                    if os.path.exists(os.path.join(repo_path, '.git')):
                        tag_suggestions = get_til_tag_suggestions(repo_path, profile, til_title)
                        if tag_suggestions:
                            print("💡 TIL Tag Suggestions:")
                            for suggestion in tag_suggestions:
                                print(f"  {suggestion}")
                            play_sound("suggest.wav")
                            print()  # Add space before TIL result
            except Exception:
                pass  # Don't break TIL creation if suggestions fail
        
        if args.template:
            # Use template for TIL vault
            success, result = create_til_from_template(til_title, args.template, config)
            print(result)
        else:
            # Use original TIL system
            include_date = not args.no_date
            success, result = add_til_entry(til_title, config, include_date, args.tag)
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

    # Handle both old and new config formats
    local_paths = config.get('local_paths', [config.get('local_path', '')]) if config.get('local_path') else config.get('local_paths', [])
    
    # Process commits for gamification
    gamification_data = process_commits_for_gamification(local_paths, config)
    
    # Check local commits FIRST
    local_commits_found = False
    if local_paths:
        output(f"🗂️  Scanning {len(local_paths)} local path(s):")
        for path in local_paths:
            if path:
                output(f"   📁 {path}")
    
    try:
        local = check_local_commits(local_paths)
        if not local:
            output("\n😢 No local commits found today.")
            silent_output("No local commits today")
        else:
            local_commits_found = True
            output("\n🟩 Local Commits:")
            for repo_name, repo_path, commits, count in local:
                output(f"📁 Repository: {repo_name}")
                output(f"   📍 Path: {repo_path}")
                output(f"   📊 {count} commit(s) today:")
                output(f"   {commits}\n")
                silent_output(f"{repo_name}: {count} commit(s)")
    except Exception as e:
        output(f"⚠️  Local check failed: {e}")
    
    # Check GitHub commits (show after local, with contextual message)
    if config.get('github_username') and not config.get('skip_github', False):
        output(f"\n🌐 GitHub: @{config['github_username']}")
        try:
            error, commits = check_github_commits(config["github_username"], config.get("github_token"))
            if error:
                output(error)
                # If it's an auth error and no token, suggest skipping GitHub checks
                if "requires authentication" in error and not config.get("github_token"):
                    output("💡 Run --setup and choose 'Skip GitHub checks' to disable this warning")
            elif not commits:
                if local_commits_found:
                    output("ℹ️  No commits pushed to GitHub yet (local commits not yet pushed)")
                else:
                    output("😢 No public commits found today.")
                silent_output("No GitHub commits today")
            else:
                output("🟢 GitHub Commits:")
                for repo, count in commits:
                    output(f"✅ {repo} — {count} commit(s)")
                    silent_output(f"{repo}: {count} commit(s)")
        except Exception as e:
            output(f"⚠️  GitHub check failed: {e}")
    elif config.get('skip_github', False):
        output("\n🌐 GitHub checks disabled (run --setup to re-enable)")
    
    # Display gamification results
    if gamification_data["xp_gained"] > 0 or gamification_data["commits_today"] > 0:
        mood_line = get_mood_commit_line(
            gamification_data["xp_gained"],
            gamification_data["commits_today"],
            gamification_data["current_streak"]
        )
        output(f"\n{mood_line}")
        
        if gamification_data["xp_gained"] > 0:
            output(f"💫 +{gamification_data['xp_gained']} XP earned today!")
        
        if gamification_data["level_up"]:
            output(f"🎉 LEVEL UP! You're now level {gamification_data['new_level']}!")
        
        if gamification_data["achievements"]:
            output("🏆 New achievements unlocked:")
            for achievement_id in gamification_data["achievements"]:
                from .gamification import ACHIEVEMENTS
                achievement = ACHIEVEMENTS.get(achievement_id, {})
                output(f"   {achievement.get('emoji', '🏆')} {achievement.get('name', achievement_id)}")
        
        if gamification_data["current_streak"] > 0:
            output(f"🔥 Current streak: {gamification_data['current_streak']} days")
            
            # Check for streak milestone
            milestone_message = check_streak_milestone(gamification_data["current_streak"], config)
            if milestone_message:
                output(f"\n{milestone_message}")
    
    # Smart Profile System suggestions (non-disruptive)
    if not args.no_profile and is_profile_enabled() and local_paths:
        try:
            profile = load_profile()
            if profile:
                # Get current working directory to find active repo
                current_dir = os.getcwd()
                repo_path = current_dir
                
                # Walk up to find .git directory
                while repo_path and repo_path != '/':
                    if os.path.exists(os.path.join(repo_path, '.git')):
                        break
                    repo_path = os.path.dirname(repo_path)
                
                if os.path.exists(os.path.join(repo_path, '.git')):
                    # Generate stack and structure suggestions
                    stack_suggestions = get_stack_suggestions(repo_path, profile)
                    structure_suggestions = get_structure_suggestions(repo_path, profile)
                    
                    all_suggestions = stack_suggestions + structure_suggestions
                    if all_suggestions:
                        output("\n🧙 Smart Suggestions:")
                        for suggestion in all_suggestions[:3]:  # Limit to 3 suggestions
                            output(f"  {suggestion}")
                        play_sound("suggest.wav")
                        
        except Exception:
            # Don't break the main flow if profile suggestions fail
            pass
    
    # Profile system onboarding (suggest building profile if enabled but missing)
    if not args.no_profile and is_profile_enabled() and needs_profile_rebuild():
        if local_paths:
            output("\n🧙 Smart Profile: No profile found!")
            output("💡 Run --build-profile to enable personalized suggestions")
            play_sound("suggest.wav")
    
    # Display Wisdom Drop quote at end of every commit check
    try:
        if config.get('inspire', True):
            quote = get_latest_wisdom_quote()
            if quote:
                emoji_mode = config.get('output', 'emoji') != 'plain'
                formatted = format_wisdom_quote(quote, emoji_mode=emoji_mode)
                output("\n" + formatted)
            elif args.debug:
                print("⚠️  Wisdom Drop: No quote retrieved")
    except Exception as e:
        # Silently log but don't break the flow
        if args.debug:
            import traceback
            print(f"⚠️  Wisdom Drop error: {e}")
            traceback.print_exc()
        pass

if __name__ == "__main__":
    main()
