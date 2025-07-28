import os
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta

# Handle imports for both standalone and package modes
try:
    from .config import save_config, CONFIG_PATH
    from .path_detector import get_suggested_paths, get_best_default_path
except ImportError:
    # Standalone mode - load modules directly
    import importlib.util
    
    def load_module(name, path):
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config = load_module("config", os.path.join(current_dir, "config.py"))
    path_detector = load_module("path_detector", os.path.join(current_dir, "path_detector.py"))
    
    save_config = config.save_config
    CONFIG_PATH = config.CONFIG_PATH
    get_suggested_paths = path_detector.get_suggested_paths
    get_best_default_path = path_detector.get_best_default_path


def interactive_setup_wizard():
    """Interactive setup wizard for first-time users"""
    print("🧙‍♂️ Welcome to commit-checker Interactive Setup Wizard!")
    print("Let's configure your perfect development environment.\n")
    
    config = {}
    
    # GitHub Configuration
    print("🌐 GitHub Configuration")
    github_username = input("   👤 GitHub username (optional): ").strip()
    config['github_username'] = github_username if github_username else None
    
    if github_username:
        github_token = input("   🔑 GitHub personal token (optional, for private repos): ").strip()
        config['github_token'] = github_token if github_token else None
    else:
        config['github_token'] = None
    
    # Development Paths
    print("\n📁 Development Folder Configuration")
    suggestions = get_suggested_paths()
    default_path = get_best_default_path()
    
    if suggestions:
        print("   🔍 Found these potential development folders:")
        for i, suggestion in enumerate(suggestions[:5], 1):
            print(f"      {i}. {suggestion}")
        print("      Or enter a custom path")
        print(f"      (Default: {default_path})")
        
        while True:
            choice = input("\n   📂 Enter number (1-5), custom path, or press Enter for default: ").strip()
            
            if choice == "":
                local_path = default_path
                break
            elif choice.isdigit() and 1 <= int(choice) <= min(5, len(suggestions)):
                local_path = suggestions[int(choice) - 1].split(':')[1].strip() if ':' in suggestions[int(choice) - 1] else suggestions[int(choice) - 1].split('(')[0].strip()
                break
            elif not choice.isdigit():
                # Custom path entered
                local_path = choice
                break
            else:
                print(f"   ❌ Invalid choice. Please enter 1-{min(5, len(suggestions))}, a custom path, or press Enter for default.")
                continue
    else:
        local_path = input(f"   📁 Local dev folder path (default: {default_path}): ").strip()
        if not local_path:
            local_path = default_path
    
    # Support multiple paths
    if ',' in local_path:
        paths = [os.path.expanduser(p.strip()) for p in local_path.split(',')]
    else:
        paths = [os.path.expanduser(local_path)]
    
    config['local_paths'] = paths
    
    # Repository Scanning Folder
    print(f"\n🔍 Repository Scanning Configuration")
    print(f"   Default: {paths[0] if paths else default_path}")
    repo_folder = input("   📁 Repo folder for scanning (or press Enter for default): ").strip()
    if not repo_folder:
        repo_folder = paths[0] if paths else default_path
    config['repo_folder'] = os.path.expanduser(repo_folder)
    
    # Output Style
    print("\n🎨 Output Style Configuration")
    print("   1. 🎉 Emoji mode (colorful with emojis)")
    print("   2. 📝 Plain mode (simple text only)")
    while True:
        output_choice = input("   📝 Enter 1 or 2 (default: 1): ").strip()
        if output_choice in ["", "1", "2"]:
            config['output'] = "plain" if output_choice == "2" else "emoji"
            break
        else:
            print("   ❌ Invalid choice. Please enter 1 or 2.")
            continue
    
    # TIL Configuration
    print("\n📚 TIL (Today I Learned) Configuration")
    print("   1. 📝 Use default path (~/.commit-checker/til.md)")
    print("   2. 📁 Custom path")
    while True:
        til_choice = input("   📝 Enter 1 or 2 (default: 1): ").strip()
        if til_choice in ["", "1", "2"]:
            if til_choice == "2":
                til_path = input("   📁 Custom TIL file path: ").strip()
                config['til_path'] = os.path.expanduser(til_path) if til_path else None
            else:
                config['til_path'] = None
            break
        else:
            print("   ❌ Invalid choice. Please enter 1 or 2.")
            continue
    
    # Commit Rules Configuration
    print("\n📝 Commit Message Rules (Optional)")
    rules_choice = input("   ✅ Enable custom commit message validation? [y/N]: ").strip().lower()
    
    commit_rules = []
    if rules_choice in ["y", "yes"]:
        print("   📝 Add regex patterns for commit message validation:")
        print("   💡 Examples:")
        print("      - ^feat: (must start with 'feat:')")
        print("      - \\[JIRA-\\d+\\] (must include JIRA ticket)")
        print("      - .{10,} (minimum 10 characters)")
        print("   (Enter empty line to finish)")
        
        while True:
            pattern = input("   🔍 Regex pattern (or Enter to finish): ").strip()
            if not pattern:
                break
            
            error_msg = input(f"   💬 Error message for '{pattern}': ").strip()
            if error_msg:
                commit_rules.append({
                    "pattern": pattern,
                    "error": error_msg
                })
    
    config['commit_rules'] = commit_rules
    
    # Interactive Mode
    print("\n🖥️  Interactive Mode Configuration")
    interactive_choice = input("   🎯 Enable interactive TUI mode? [y/N]: ").strip().lower()
    config['interactive_mode'] = interactive_choice in ["y", "yes"]
    
    if config['interactive_mode']:
        print("   🎨 Choose theme:")
        print("      1. 🤖 tech (green-on-black hacker vibes)")
        print("      2. 🌸 kawaii (pastel colors, emoji-heavy)")
        print("      3. 🎭 anime (bold colors)")
        print("      4. 🧛 horror (dark red, unsettling)")
        print("      5. 🎨 default (balanced colors)")
        
        themes = {"1": "tech", "2": "kawaii", "3": "anime", "4": "horror", "5": "default"}
        while True:
            theme_choice = input("   🎨 Enter 1-5 (default: 5): ").strip()
            if theme_choice in ["", "1", "2", "3", "4", "5"]:
                config['theme'] = themes.get(theme_choice, "default")
                print(f"   ✨ Theme set to: {config['theme']}")
                break
            else:
                print("   ❌ Invalid choice. Please enter 1, 2, 3, 4, or 5.")
                continue
    else:
        config['theme'] = "default"
    
    # Pre-commit Hooks
    print("\n🔗 Git Hook Configuration")
    hooks_choice = input("   ⚡ Install pre-commit hooks for this repo? [y/N]: ").strip().lower()
    config['install_hooks'] = hooks_choice in ["y", "yes"]
    
    # Summary
    print("\n📋 Configuration Summary:")
    print(f"   👤 GitHub: {config['github_username'] or 'Not configured'}")
    print(f"   📁 Local paths: {len(config['local_paths'])} path(s)")
    print(f"   🔍 Repo folder: {config['repo_folder']}")
    print(f"   🎨 Output style: {config['output']}")
    print(f"   📚 TIL path: {config['til_path'] or 'Default'}")
    print(f"   📝 Commit rules: {len(config['commit_rules'])} rule(s)")
    print(f"   🖥️  Interactive mode: {'Enabled' if config['interactive_mode'] else 'Disabled'}")
    print(f"   🎨 Theme: {config['theme']}")
    print(f"   🔗 Pre-commit hooks: {'Enabled' if config['install_hooks'] else 'Disabled'}")
    
    while True:
        confirm = input("\n✅ Save this configuration? [Y/n]: ").strip().lower()
        if confirm in ["", "y", "yes", "n", "no"]:
            if confirm not in ["n", "no"]:
                save_config(config)
                print(f"\n🎉 Configuration saved to {CONFIG_PATH}")
                
                # Install hooks if requested
                if config['install_hooks']:
                    install_git_hooks()
                
                return True
            else:
                print("❌ Configuration cancelled.")
                return False
        else:
            print("❌ Invalid choice. Please enter 'y' for yes or 'n' for no.")
            continue


def get_commit_stats(repo_path, days=30):
    """Get commit statistics for a repository"""
    try:
        since_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        # Get commits per day
        log_output = subprocess.check_output([
            "git", "--git-dir", os.path.join(repo_path, ".git"), "--work-tree", repo_path,
            "log", f"--since={since_date}", "--pretty=format:%cd", "--date=short"
        ], stderr=subprocess.DEVNULL).decode("utf-8").strip()
        
        if not log_output:
            return {}
        
        # Count commits per day
        commits_by_date = {}
        for date in log_output.split('\n'):
            if date:
                commits_by_date[date] = commits_by_date.get(date, 0) + 1
        
        return commits_by_date
    except Exception:
        return {}


def generate_ascii_chart(data, width=30):
    """Generate ASCII chart from commit data"""
    if not data:
        return "No data available"
    
    max_commits = max(data.values()) if data else 1
    chart_chars = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"]
    
    # Get last 'width' days
    today = datetime.now().date()
    chart_data = []
    
    for i in range(width):
        date = today - timedelta(days=width - 1 - i)
        date_str = date.strftime('%Y-%m-%d')
        commits = data.get(date_str, 0)
        
        # Calculate bar height (0-7 index for chart_chars)
        if max_commits == 0:
            bar_height = 0
        else:
            bar_height = min(7, int((commits / max_commits) * 7))
        
        chart_data.append(chart_chars[bar_height])
    
    return ''.join(chart_data)


def show_commit_stats(repo_paths):
    """Show ASCII commit trend charts for repositories"""
    print("📊 Commit Statistics (Last 30 Days)")
    print("=" * 50)
    
    for repo_path in repo_paths:
        if not os.path.exists(repo_path):
            continue
            
        # Find git repositories in the path
        for root, dirs, files in os.walk(repo_path):
            if '.git' in dirs:
                try:
                    repo_name = os.path.basename(root)
                    stats = get_commit_stats(root)
                    
                    if stats:
                        total_commits = sum(stats.values())
                        chart = generate_ascii_chart(stats)
                        print(f"\n📁 {repo_name}")
                        print(f"   Total commits: {total_commits}")
                        print(f"   Trend: {chart}")
                        
                        # Show recent activity
                        recent_dates = sorted(stats.keys())[-7:]  # Last 7 days with activity
                        if recent_dates:
                            print(f"   Recent: {', '.join(f'{d}: {stats[d]}' for d in recent_dates[-3:])}")
                    
                except Exception:
                    continue
                    
                dirs.clear()  # Don't search nested repos


def install_git_hooks():
    """Install pre-commit hooks in current git repository"""
    try:
        # Check if we're in a git repo
        result = subprocess.run(['git', 'rev-parse', '--git-dir'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print("⚠️  Not in a git repository. Hooks not installed.")
            return False
        
        git_dir = result.stdout.strip()
        hooks_dir = os.path.join(git_dir, 'hooks')
        os.makedirs(hooks_dir, exist_ok=True)
        
        # Create pre-commit hook
        hook_content = '''#!/bin/bash
# commit-checker pre-commit hook

echo "🔍 Running commit-checker validation..."

# Run commit message validation
if command -v commit-checker &> /dev/null; then
    commit-checker --validate-commit "$1"
    if [ $? -ne 0 ]; then
        echo "❌ Commit message validation failed"
        exit 1
    fi
fi

# Optional: Prompt for TIL entry
if [ -t 1 ]; then  # Only if interactive terminal
    read -p "📝 Add a TIL entry for this commit? [y/N]: " til_choice
    if [[ $til_choice =~ ^[Yy]$ ]]; then
        read -p "📚 What did you learn? " til_entry
        if [ ! -z "$til_entry" ]; then
            commit-checker til "$til_entry"
        fi
    fi
fi

exit 0
'''
        
        hook_path = os.path.join(hooks_dir, 'pre-commit')
        with open(hook_path, 'w') as f:
            f.write(hook_content)
        
        # Make executable
        os.chmod(hook_path, 0o755)
        
        print(f"✅ Pre-commit hook installed at {hook_path}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to install hooks: {e}")
        return False


def run_diagnostics():
    """Run system diagnostics"""
    print("🔍 System Diagnostics")
    print("=" * 30)
    
    # Check Python version
    python_version = sys.version.split()[0]
    print(f"🐍 Python version: {python_version}")
    
    # Check Git availability
    try:
        git_result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if git_result.returncode == 0:
            git_version = git_result.stdout.strip()
            print(f"📦 Git: {git_version}")
        else:
            print("❌ Git: Not available")
    except FileNotFoundError:
        print("❌ Git: Not found")
    
    # Check package installation method
    try:
        import pkg_resources
        try:
            dist = pkg_resources.get_distribution("commit-checker")
            print(f"📦 Package: Installed via pip (v{dist.version})")
            print(f"   Location: {dist.location}")
        except pkg_resources.DistributionNotFound:
            print("📦 Package: Standalone installation")
    except ImportError:
        print("📦 Package: Cannot determine installation method")
    
    # Check config file
    if os.path.exists(CONFIG_PATH):
        print(f"⚙️  Config: Found at {CONFIG_PATH}")
        try:
            with open(CONFIG_PATH, 'r') as f:
                config = json.load(f)
            print(f"   GitHub user: {config.get('github_username', 'Not set')}")
            print(f"   Local paths: {len(config.get('local_paths', []))} configured")
            print(f"   Output mode: {config.get('output', 'emoji')}")
        except Exception as e:
            print(f"   ❌ Error reading config: {e}")
    else:
        print("⚙️  Config: Not found (run --init or --setup)")
    
    # Check dependencies
    deps = ['requests', 'packaging', 'colorama']
    print("📚 Dependencies:")
    for dep in deps:
        try:
            __import__(dep)
            print(f"   ✅ {dep}: Available")
        except ImportError:
            print(f"   ❌ {dep}: Missing")
    
    # Check virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("🐍 Environment: Virtual environment detected")
    else:
        print("🐍 Environment: System Python")
    
    # Check pipx
    try:
        pipx_result = subprocess.run([sys.executable, "-m", "pipx", "list"], 
                                   capture_output=True, text=True)
        if pipx_result.returncode == 0:
            if "commit-checker" in pipx_result.stdout:
                print("📦 pipx: commit-checker installed via pipx")
            else:
                print("📦 pipx: Available but commit-checker not installed via pipx")
        else:
            print("📦 pipx: Not available")
    except FileNotFoundError:
        print("📦 pipx: Not found")
    
    print("\n✅ Diagnostics complete!")
