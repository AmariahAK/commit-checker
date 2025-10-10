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
download_if_needed "profile.py" "$REPO_URL/commit_checker/profile.py"
download_if_needed "path_detector.py" "$REPO_URL/commit_checker/path_detector.py"
download_if_needed "updater.py" "$REPO_URL/commit_checker/updater.py"
download_if_needed "til.py" "$REPO_URL/commit_checker/til.py"
download_if_needed "wizard.py" "$REPO_URL/commit_checker/wizard.py"
download_if_needed "gamification.py" "$REPO_URL/commit_checker/gamification.py"
download_if_needed "analytics.py" "$REPO_URL/commit_checker/analytics.py"
download_if_needed "til_vault.py" "$REPO_URL/commit_checker/til_vault.py"
download_if_needed "bootstrap.py" "$REPO_URL/commit_checker/bootstrap.py"
download_if_needed "wisdom.py" "$REPO_URL/commit_checker/wisdom.py"
download_if_needed "context.py" "$REPO_URL/commit_checker/context.py"
download_if_needed "ai_handler.py" "$REPO_URL/commit_checker/ai_handler.py"

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

# Import our modules with absolute imports
import importlib.util
import importlib

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Load modules
    checker = load_module("checker", os.path.join(script_dir, "checker.py"))
    config = load_module("config", os.path.join(script_dir, "config.py"))
    profile = load_module("profile", os.path.join(script_dir, "profile.py"))
    path_detector = load_module("path_detector", os.path.join(script_dir, "path_detector.py"))
    til = load_module("til", os.path.join(script_dir, "til.py"))
    wizard = load_module("wizard", os.path.join(script_dir, "wizard.py"))
    gamification = load_module("gamification", os.path.join(script_dir, "gamification.py"))
    analytics = load_module("analytics", os.path.join(script_dir, "analytics.py"))
    til_vault = load_module("til_vault", os.path.join(script_dir, "til_vault.py"))
    updater = load_module("updater", os.path.join(script_dir, "updater.py"))
    
    # Get functions from modules
    check_github_commits = checker.check_github_commits
    check_local_commits = checker.check_local_commits
    scan_repos = checker.scan_repos
    get_most_active_repo = checker.get_most_active_repo
    config_exists = config.config_exists
    load_config = config.load_config
    prompt_config = config.prompt_config
    get_auto_config = config.get_auto_config
    save_config = config.save_config
    try:
        load_profile = config.load_profile
        save_profile = config.save_profile
        is_profile_enabled = config.is_profile_enabled
        needs_profile_rebuild = config.needs_profile_rebuild
        enable_profile = config.enable_profile
    except AttributeError:
        # Fallback if profile functions don't exist in older version
        def load_profile(): return None
        def save_profile(p): return True
        def is_profile_enabled(): return False
        def needs_profile_rebuild(): return True
        def enable_profile(e): return True
    
    try:
        build_profile = profile.build_profile
        suggest_commit_message = profile.suggest_commit_message
        get_stack_suggestions = profile.get_stack_suggestions
        get_structure_suggestions = profile.get_structure_suggestions
        get_commit_size_suggestions = profile.get_commit_size_suggestions
        get_til_tag_suggestions = profile.get_til_tag_suggestions
        update_freeform_feedback = profile.update_freeform_feedback
        play_sound = profile.play_sound
    except AttributeError as e:
        # Fallback if profile module doesn't exist - print debug info
        print(f"⚠️  Profile functions not available: {e}")
        def build_profile(p): 
            print("❌ Profile building not available in standalone mode")
            return {}
        def suggest_commit_message(r, p, m): return []
        def get_stack_suggestions(r, p): return []
        def get_structure_suggestions(r, p): return []
        def get_commit_size_suggestions(r): return []
        def get_til_tag_suggestions(r, p, t): return []
        def update_freeform_feedback(p, r, f): return p
        def play_sound(s): pass
    
    get_current_git_repo = path_detector.get_current_git_repo
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
    
    # Gamification functions
    display_achievements = gamification.display_achievements
    display_xp_status = gamification.display_xp_status
    process_commits_for_gamification = gamification.process_commits_for_gamification
    ensure_gamification_files = gamification.ensure_gamification_files
    
    # Analytics functions
    get_commit_heatmap_data = analytics.get_commit_heatmap_data
    render_ascii_heatmap = analytics.render_ascii_heatmap
    get_language_stats = analytics.get_language_stats
    render_language_pie_chart = analytics.render_language_pie_chart
    get_mood_commit_line = analytics.get_mood_commit_line
    export_heatmap_svg = analytics.export_heatmap_svg
    
    # TIL Vault functions
    create_til_from_template = til_vault.create_til_from_template
    search_til_vault = til_vault.search_til_vault
    display_search_results = til_vault.display_search_results
    create_til_from_latest_commit = til_vault.create_til_from_latest_commit
    display_vault_summary = til_vault.display_vault_summary
    list_templates = til_vault.list_templates
    create_default_templates = til_vault.create_default_templates
    
    # Updater functions  
    manual_update_check = updater.manual_update_check
    detect_installation_type = updater.detect_installation_type
    
except Exception as e:
    print(f"❌ Error importing modules: {e}")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Check today's GitHub + local commits.")
    parser.add_argument("--setup", action="store_true", help="Reset your config")
    parser.add_argument("--init", action="store_true", help="Interactive setup wizard")
    parser.add_argument("--uninstall", action="store_true", help="Remove commit-checker")
    parser.add_argument("--support", action="store_true", help="Show donation link")
    parser.add_argument("--silent", action="store_true", help="Minimal output")
    parser.add_argument("--nocolor", action="store_true", help="Disable emojis and colors")
    parser.add_argument("--stats", action="store_true", help="Show ASCII commit trend charts")
    parser.add_argument("--diagnose", action="store_true", help="Run system diagnostics")
    parser.add_argument("--update", action="store_true", help="Check for updates")
    parser.add_argument("--version", action="store_true", help="Show version information")
    
    # Smart Profile System flags (v0.7.1)
    parser.add_argument("--build-profile", action="store_true", help="Build or rebuild your coding profile")
    parser.add_argument("--coach", type=str, nargs='?', const='', help="Get commit message coaching suggestions")
    parser.add_argument("--insights", action="store_true", help="Show personalized coding insights")
    parser.add_argument("--no-profile", action="store_true", help="Skip profile-based suggestions")
    parser.add_argument("--feedback", choices=["good", "bad"], help="Give feedback on coaching suggestions")
    
    # Repository management
    parser.add_argument("--scan", action="store_true", help="Scan repo folder for git repositories")
    parser.add_argument("--repos-summary", action="store_true", help="Show repository summary")
    parser.add_argument("--most-active", action="store_true", help="Show most active repository")
    parser.add_argument("--week", action="store_true", help="Use week timeframe (with --most-active)")
    parser.add_argument("--month", action="store_true", help="Use month timeframe (with --most-active)")
    
    # Gamification
    parser.add_argument("--achievements", action="store_true", help="Display achievement gallery")
    parser.add_argument("--xp", action="store_true", help="Show XP status and level progress")
    
    # Analytics
    parser.add_argument("--heatmap", action="store_true", help="Display commit heatmap")
    parser.add_argument("--days", type=int, default=365, help="Number of days for heatmap")
    parser.add_argument("--heatmap-export", choices=["svg"], help="Export heatmap format")
    parser.add_argument("--stats-lang", action="store_true", help="Show programming language statistics")
    
    # TIL functionality
    parser.add_argument("til", nargs="*", help="Add a 'Today I Learned' entry")
    parser.add_argument("--view-til", action="store_true", help="View your TIL log")
    parser.add_argument("--edit-til", action="store_true", help="Edit your TIL log in default editor")
    parser.add_argument("--reset-til", action="store_true", help="Clear your TIL log")
    parser.add_argument("--no-date", action="store_true", help="Add TIL entry without date header")
    parser.add_argument("--tag", type=str, help="Add tag to TIL entry")
    parser.add_argument("--export", choices=["md", "json"], help="Export TIL entries to format")
    parser.add_argument("--filter-tag", type=str, help="Filter TIL entries by tag")
    
    # TIL Vault
    parser.add_argument("--template", type=str, help="Use template for TIL entry")
    parser.add_argument("--search-til", type=str, help="Search TIL vault entries")
    parser.add_argument("--til-vault", action="store_true", help="Show TIL vault summary")
    parser.add_argument("--til-from-diff", action="store_true", help="Create TIL from latest commit")
    parser.add_argument("--list-templates", action="store_true", help="List available TIL templates")
    
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
        print("☕ Buy Me A Coffee: https://buymeacoffee.com/amariahak")
        print("🌐 GitHub: https://github.com/AmariahAK")
        sys.exit(0)
    
    if args.version:
        print("🚀 commit-checker v0.7.6")
        print("💡 AI Commit Mentor with Wisdom Drop Integration")
        print("🔗 https://github.com/AmariahAK/commit-checker")
        sys.exit(0)
    
    if args.update:
        manual_update_check()
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
            # Use the imported build_profile function
            profile = build_profile(local_paths)
            
            # Save profile using config functions
            if save_profile(profile):
                repo_count = len(profile.get("repos", {}))
                print(f"\n✅ Profile built successfully!")
                print(f"   📈 Analyzed {repo_count} repositories")
                print(f"   💡 Smart suggestions now enabled")
                
                # Enable profile if not already enabled
                config['enable_profile'] = True
                save_config(config)
            else:
                print("❌ Failed to save profile. Check file permissions.")
        except Exception as e:
            print(f"❌ Profile building failed: {e}")
        
        sys.exit(0)
    
    if args.insights:
        if not config.get('enable_profile', False):
            print("🧙 Smart profile system is disabled.")
            print("💡 Run --build-profile to enable insights.")
            sys.exit(1)
        
        # Load profile from config
        profile = config.get('profile', {})
        if not profile:
            print("🧙 No profile found. Run --build-profile first.")
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
        
        last_scan = profile.get("last_scan", "")
        if last_scan:
            print(f"\n🕒 Profile last updated: {last_scan[:19].replace('T', ' ')}")
        
        print("\n💡 Run --build-profile to refresh your profile data")
        sys.exit(0)
    
    # Gamification commands
    if args.achievements:
        print(display_achievements())
        sys.exit(0)
    
    if args.xp:
        print(display_xp_status())
        sys.exit(0)
    
    # Analytics commands
    if args.heatmap:
        local_paths = config.get('local_paths', [])
        if not local_paths:
            print("❌ No local paths configured. Run --init or --setup first.")
            sys.exit(1)
        
        heatmap_data = get_commit_heatmap_data(local_paths, args.days)
        if args.heatmap_export == "svg":
            success, message = export_heatmap_svg(heatmap_data, f"commit-heatmap-{args.days}days.svg", args.days)
            print(message)
        else:
            print(render_ascii_heatmap(heatmap_data, args.days))
        sys.exit(0)
    
    if args.stats_lang:
        local_paths = config.get('local_paths', [])
        if not local_paths:
            print("❌ No local paths configured. Run --init or --setup first.")
            sys.exit(1)
        
        language_stats = get_language_stats(local_paths)
        print(render_language_pie_chart(language_stats))
        sys.exit(0)
    
    # Repository management commands
    if args.scan:
        repo_folder = config.get('repo_folder')
        if not repo_folder:
            print("❌ No repo folder configured. Run --setup first.")
            sys.exit(1)
        
        print(f"🔍 Scanning {repo_folder} for git repositories...")
        repos = scan_repos(repo_folder)
        
        if repos:
            print(f"\n📁 Scanned {len(repos)} repos:\n")
            for repo in repos:
                status_emoji = "✅" if repo['today_commits'] > 0 else "❌"
                print(f"{repo['name']} → {status_emoji} {repo['today_commits']} today | 🧮 {repo['total_commits']} total | 🕒 {repo['last_commit_date']}")
        else:
            print("❌ No git repositories found.")
        sys.exit(0)
    
    if args.repos_summary:
        repo_folder = config.get('repo_folder')
        if not repo_folder:
            print("❌ No repo folder configured. Run --setup first.")
            sys.exit(1)
            
        repos = scan_repos(repo_folder)
        if repos:
            print("🧾 Repo Summary:")
            for repo in repos:
                status_emoji = "✅" if repo['today_commits'] > 0 else "❌"
                print(f"📁 {repo['name']} → {status_emoji} {repo['today_commits']} today | 🧮 {repo['total_commits']} total | 🕒 {repo['last_commit_date']}")
        else:
            print("❌ No git repositories found.")
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
            print(f"🔥 Most active repo this {timeframe}:")
            print(f"📁 {most_active['name']} → {most_active['commits']} commits")
            print(f"📅 Last activity: {most_active['last_activity']}")
        else:
            print(f"❌ No active repositories found this {timeframe}.")
        sys.exit(0)
    
    # Enhanced TIL commands
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

    # Handle local paths
    local_paths = config.get('local_paths', [])
    
    # Process commits for gamification
    gamification_data = process_commits_for_gamification(local_paths, config)
    
    # Check local commits FIRST
    local_commits_found = False
    if local_paths:
        output(f"🗂️  Scanning {len(local_paths)} local path(s):")
        for path in local_paths:
            if path:
                output(f"   📁 {path}")
    
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
    
    # Check GitHub commits (after local)
    if config.get('github_username'):
        output(f"\n🌐 GitHub: @{config['github_username']}")
        error, commits = check_github_commits(config["github_username"], config.get("github_token"))
        if error:
            output(error)
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
                # Simple achievement display without import dependencies
                output(f"   🏆 {achievement_id}")
        
        if gamification_data["current_streak"] > 0:
            output(f"🔥 Current streak: {gamification_data['current_streak']} days")
    
    # Display Wisdom Drop quote at end
    try:
        if config.get('inspire', True):
            wisdom = load_module("wisdom", os.path.join(script_dir, "wisdom.py"))
            quote = wisdom.get_latest_wisdom_quote()
            if quote:
                emoji_mode = config.get('output', 'emoji') != 'plain'
                formatted = wisdom.format_wisdom_quote(quote, emoji_mode=emoji_mode)
                output("\n" + formatted)
    except Exception:
        pass

if __name__ == "__main__":
    main()
EOF

# Make it executable
chmod +x "$SCRIPT_DIR/run_commit_checker.py"

# Run the Python script
python3 "$SCRIPT_DIR/run_commit_checker.py" "$@"
