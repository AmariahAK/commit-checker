import os
import subprocess
import json
import re
import collections
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple, Any

def run_git(cmd: List[str], cwd: str) -> Optional[str]:
    """
    Run git command safely with fallbacks
    Returns None if command fails (e.g., not a git repo, git not available)
    """
    try:
        result = subprocess.check_output(
            ["git"] + cmd,
            cwd=cwd,
            stderr=subprocess.DEVNULL,
            text=True
        )
        return result.strip()
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        # Fallback for various errors: not a git repo, git not installed, permission issues
        return None

def detect_tech_stack(repo_path: str) -> List[str]:
    """
    Detect tech stack based on project files (shallow scan, top 2 levels only)
    Returns list of 1-3 tech stack identifiers
    Supports 30+ programming languages and frameworks
    """
    # Massively expanded tech stack detection map
    TECH_STACKS = {
        # Existing languages
        "python": ["requirements.txt", "pyproject.toml", "setup.py", "Pipfile"],
        "django": ["manage.py", "settings.py"],
        "flask": ["app.py", "run.py"],
        "javascript": ["package.json", "package-lock.json"],
        "react": ["src/App.js", "src/App.jsx"],
        "typescript": ["tsconfig.json"],
        "rust": ["Cargo.toml", "Cargo.lock"],
        "java": ["pom.xml", "build.gradle"],
        "go": ["go.mod", "go.sum"],
        "csharp": [".csproj", "packages.config", "Directory.Packages.props"],
        "ruby": ["Gemfile", "Gemfile.lock"],
        "php": ["composer.json", "composer.lock"],
        "swift": ["Package.swift", "Podfile"],
        "kotlin": ["build.gradle.kts"],
        "elixir": ["mix.exs"],
        "scala": ["build.sbt"],
        "haskell": ["cabal.project", "package.yaml", "stack.yaml"],
        
        # NEW: C/C++ and related
        "c": ["Makefile", "CMakeLists.txt", "configure.ac"],
        "cpp": ["CMakeLists.txt", "meson.build"],
        "objectivec": ["Podfile", "*.xcodeproj"],
        
        # NEW: Mobile and cross-platform
        "dart": ["pubspec.yaml", "pubspec.lock"],  # Flutter/Dart
        "flutter": ["pubspec.yaml"],
        "reactnative": ["app.json", "metro.config.js"],
        
        # NEW: Data science and scientific computing
        "r": ["DESCRIPTION", "NAMESPACE", ".Rproj"],
        "julia": ["Project.toml", "Manifest.toml"],
        "matlab": ["*.mlx", "*.mlapp"],
        
        # NEW: Scripting languages
        "perl": ["cpanfile", "Makefile.PL"],
        "lua": ["rockspec", "*.rockspec"],
        "bash": ["*.sh", "configure"],
        "powershell": ["*.ps1", "*.psm1"],
        
        # NEW: Systems and low-level
        "zig": ["build.zig", "build.zig.zon"],
        "nim": ["*.nimble", "config.nims"],
        "crystal": ["shard.yml", "shard.lock"],
        "v": ["v.mod"],
        "fortran": ["*.f90", "*.f95", "Makefile"],
        "assembly": ["*.asm", "*.s"],
        
        # NEW: Hardware description
        "vhdl": ["*.vhdl", "*.vhd"],
        "verilog": ["*.v", "*.sv"],
        
        # NEW: Blockchain and smart contracts
        "solidity": ["hardhat.config.js", "truffle-config.js", "foundry.toml"],
        "move": ["Move.toml"],  # Sui/Aptos
        "cairo": ["Scarb.toml"],  # Starknet
        
        # NEW: Emerging languages
        "gren": ["gren.json"],
        "roc": ["*.roc"],
        
        # NEW: Markup and config
        "latex": ["*.tex", "*.bib"],
        "markdown": ["*.md", "*.markdown"],
    }
    
    stack = []
    key_files = []
    file_extensions = collections.defaultdict(int)
    
    try:
        # Shallow walk - only top 2 levels to avoid performance issues
        for root, dirs, files in os.walk(repo_path):
            # Limit depth to 2 levels from repo root
            level = root[len(repo_path):].count(os.sep)
            if level >= 2:
                dirs[:] = []  # Don't go deeper
                continue
                
            for file in files:
                key_files.append(file)
                _, ext = os.path.splitext(file)
                if ext:
                    file_extensions[ext.lower()] += 1
                    
    except (OSError, PermissionError):
        # Fallback if directory access fails
        return ["unknown"]
    
    # Primary stack detection based on manifest files
    for tech, manifest_files in TECH_STACKS.items():
        if tech in ["django", "flask", "react", "typescript"]:
            continue  # Handle these as sub-frameworks below
            
        if any(f in key_files for f in manifest_files):
            stack.append(tech)
            
            # Handle sub-frameworks
            if tech == "python":
                if any(f in key_files for f in TECH_STACKS["django"]):
                    stack.append("django")
                elif any(f in key_files for f in TECH_STACKS["flask"]):
                    stack.append("flask")
                    
            elif tech == "javascript":
                # Check for React in package.json
                try:
                    package_json_path = os.path.join(repo_path, "package.json")
                    if os.path.exists(package_json_path):
                        with open(package_json_path, 'r', encoding='utf-8') as f:
                            package_data = json.load(f)
                            package_str = str(package_data).lower()
                            if 'react' in package_str:
                                stack.append("react")
                            if ('typescript' in package_str or '"type": "module"' in package_str or 
                                any(f in key_files for f in TECH_STACKS["typescript"])):
                                stack.append("typescript")
                except (json.JSONDecodeError, OSError, UnicodeDecodeError):
                    # Fallback if package.json parsing fails
                    pass
                    
            elif tech == "java":
                # Check for Kotlin in build.gradle
                if "build.gradle.kts" in key_files:
                    stack.append("kotlin")
    
    # Fallback: detect by file extensions if no manifest files found
    if not stack:
        ext_map = {
            # Existing
            ".py": "python", ".js": "javascript", ".ts": "typescript",
            ".rs": "rust", ".java": "java", ".go": "go", ".cs": "csharp",
            ".rb": "ruby", ".php": "php", ".swift": "swift", ".kt": "kotlin",
            ".ex": "elixir", ".exs": "elixir", ".scala": "scala", ".hs": "haskell",
            
            # NEW: C/C++ family
            ".c": "c", ".h": "c",
            ".cpp": "cpp", ".cc": "cpp", ".cxx": "cpp", ".hpp": "cpp",
            ".m": "objectivec", ".mm": "objectivec",
            
            # NEW: Mobile/cross-platform
            ".dart": "dart",
            ".jsx": "react",
            
            # NEW: Data science
            ".r": "r", ".R": "r",
            ".jl": "julia",
            ".m": "matlab",  # Conflicts with objc, check context
            
            # NEW: Scripting
            ".pl": "perl", ".pm": "perl",
            ".lua": "lua",
            ".sh": "bash", ".bash": "bash", ".zsh": "bash",
            ".ps1": "powershell", ".psm1": "powershell",
            
            # NEW: Systems/low-level
            ".zig": "zig",
            ".nim": "nim",
            ".cr": "crystal",
            ".v": "v",
            ".f90": "fortran", ".f95": "fortran", ".f03": "fortran",
            ".asm": "assembly", ".s": "assembly",
            
            # NEW: Hardware
            ".vhd": "vhdl", ".vhdl": "vhdl",
            ".v": "verilog", ".sv": "verilog",  # System Verilog
            
            # NEW: Blockchain
            ".sol": "solidity",
            ".move": "move",
            ".cairo": "cairo",
            
            # NEW: Other
            ".tex": "latex",
            ".md": "markdown", ".markdown": "markdown",
        }
        
        for ext, count in file_extensions.items():
            if count > 5 and ext in ext_map:
                tech = ext_map[ext]
                if tech not in stack:
                    stack.append(tech)
        
    # CLI/Tool detection
    if any(f in key_files for f in ["cli.py", "main.py", "__main__.py"]) or "bin/" in key_files:
        if "cli" not in stack:
            stack.append("cli")
        
    return stack[:3]  # Limit to top 3 stack items

def analyze_project_structure(repo_path: str) -> Dict[str, Any]:
    """
    Analyze project structure (shallow scan for performance)
    Returns summary of directories and key files
    """
    top_dirs = []
    key_files = []
    has_tests_dir = False
    
    try:
        for item in os.listdir(repo_path):
            item_path = os.path.join(repo_path, item)
            if os.path.isdir(item_path):
                top_dirs.append(item)
                if item.lower() in ["tests", "test", "spec", "__tests__"]:
                    has_tests_dir = True
            else:
                # Track important files
                if item.lower() in ["readme.md", "readme.txt", "readme.rst", "package.json", 
                                   "setup.py", "cargo.toml", "pom.xml", "makefile", "dockerfile"]:
                    key_files.append(item)
                    
    except (OSError, PermissionError):
        # Fallback for directory access issues
        return {"top_dirs": [], "key_files": [], "has_tests_dir": False}
    
    return {
        "top_dirs": sorted(top_dirs)[:10],  # Limit to top 10 dirs
        "key_files": key_files,
        "has_tests_dir": has_tests_dir
    }

def analyze_commit_style(repo_path: str, limit: int = 50) -> Dict[str, Any]:
    """
    Analyze commit message patterns from recent history
    Returns style analysis with fallbacks for empty repos
    """
    log_output = run_git(["log", f"-{limit}", "--oneline"], repo_path)
    
    if not log_output:
        # Fallback for empty repos or git issues
        return {
            "avg_length": 5.0,
            "common_prefixes": [],
            "case_style": "imperative",
            "uses_emoji": False,
            "freeform_ratio": 1.0  # Default to freeform for empty repos
        }
    
    messages = []
    prefixes = []
    prefixed_commits = 0
    total_commits = 0
    emoji_count = 0
    case_patterns = {"sentence": 0, "lowercase": 0, "imperative": 0}
    
    # Regex patterns
    prefix_pattern = re.compile(r'^[a-f0-9]+\s+([a-z]+:)', re.IGNORECASE)
    emoji_pattern = re.compile(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U000024C2-\U0001F251]+')
    imperative_keywords = ['add', 'fix', 'update', 'remove', 'refactor', 'implement', 'create', 'delete']
    
    for line in log_output.split('\n'):
        if not line.strip():
            continue
            
        # Extract commit message (skip hash)
        parts = line.split(' ', 1)
        if len(parts) < 2:
            continue
            
        message = parts[1].strip()
        messages.append(message)
        total_commits += 1
        
        # Check for emoji
        if emoji_pattern.search(message):
            emoji_count += 1
            
        # Extract prefix for freeform calculation
        prefix_match = prefix_pattern.match(line)
        if prefix_match:
            prefixes.append(prefix_match.group(1).lower())
            prefixed_commits += 1
        
        # Analyze case style
        first_word = message.split()[0] if message.split() else ""
        if first_word:
            if first_word.lower() in imperative_keywords:
                case_patterns["imperative"] += 1
            elif first_word[0].isupper() and message.endswith('.'):
                case_patterns["sentence"] += 1
            elif first_word.islower():
                case_patterns["lowercase"] += 1
    
    # Calculate averages and patterns
    avg_length = sum(len(msg.split()) for msg in messages) / len(messages) if messages else 5.0
    prefix_counter = collections.Counter(prefixes)
    common_prefixes = [prefix + ":" for prefix, count in prefix_counter.most_common(3)]
    uses_emoji = (emoji_count / len(messages)) > 0.2 if messages else False
    
    # Calculate freeform ratio (1.0 = fully freeform, 0.0 = fully prefixed)
    freeform_ratio = 1.0 - (prefixed_commits / total_commits) if total_commits > 0 else 1.0
    
    # Determine dominant case style
    dominant_case = max(case_patterns, key=case_patterns.get) if any(case_patterns.values()) else "imperative"
    
    return {
        "avg_length": round(avg_length, 1),
        "common_prefixes": common_prefixes,
        "case_style": dominant_case,
        "uses_emoji": uses_emoji,
        "freeform_ratio": round(freeform_ratio, 2)
    }

def get_repo_habits(repo_path: str) -> Dict[str, str]:
    """
    Analyze repository habits (default branch, etc.)
    """
    default_branch = run_git(["symbolic-ref", "--short", "HEAD"], repo_path)
    if not default_branch:
        # Fallback: try to get main branch name
        default_branch = run_git(["rev-parse", "--abbrev-ref", "HEAD"], repo_path)
        if not default_branch:
            default_branch = "main"  # Ultimate fallback
    
    return {
        "default_branch": default_branch
    }

def build_profile(dev_paths: List[str]) -> Dict[str, Any]:
    """
    Build user profile by scanning repositories in dev paths
    Returns complete profile dict ready for caching
    """
    repos = {}
    global_stats = {
        "total_length": 0,
        "total_messages": 0,
        "all_prefixes": [],
        "emoji_repos": 0,
        "case_counts": collections.defaultdict(int)
    }
    
    scanned_repos = []
    
    # Find repos using existing path detector logic
    for base_path in dev_paths:
        if not base_path or not os.path.exists(base_path):
            continue
            
        for root, dirs, files in os.walk(base_path):
            if '.git' in dirs:
                try:
                    # Get repo name (prefer remote name)
                    repo_name = os.path.basename(root)
                    remote_url = run_git(["config", "--get", "remote.origin.url"], root)
                    
                    if remote_url:
                        if remote_url.endswith('.git'):
                            remote_url = remote_url[:-4]
                        repo_name = remote_url.split('/')[-1]
                    
                    # Skip if we already processed this repo (by name)
                    if repo_name in repos:
                        dirs.clear()
                        continue
                    
                    # Analyze repo
                    commit_style = analyze_commit_style(root)
                    tech_stack = detect_tech_stack(root)
                    structure = analyze_project_structure(root)
                    habits = get_repo_habits(root)
                    
                    # Store repo profile
                    repos[repo_name] = {
                        "path": root,
                        "tech_stack": tech_stack,
                        "structure": structure,
                        "commit_style": commit_style,
                        "habits": habits
                    }
                    
                    # Aggregate global stats
                    global_stats["total_length"] += commit_style["avg_length"]
                    global_stats["total_messages"] += 1
                    global_stats["all_prefixes"].extend(commit_style["common_prefixes"])
                    if commit_style["uses_emoji"]:
                        global_stats["emoji_repos"] += 1
                    global_stats["case_counts"][commit_style["case_style"]] += 1
                    
                    scanned_repos.append(repo_name)
                    
                    # Limit to prevent performance issues
                    if len(scanned_repos) >= 10:
                        break
                        
                except (OSError, subprocess.SubprocessError):
                    # Skip repos that cause issues
                    continue
                    
                dirs.clear()  # Don't scan nested repos
            
            if len(scanned_repos) >= 10:
                break
    
    # Calculate global aggregates
    if global_stats["total_messages"] > 0:
        global_avg_length = global_stats["total_length"] / global_stats["total_messages"]
        global_mood = max(global_stats["case_counts"], key=global_stats["case_counts"].get) if global_stats["case_counts"] else "imperative"
        global_uses_emoji = (global_stats["emoji_repos"] / global_stats["total_messages"]) > 0.3
    else:
        # Fallback for no repos found
        global_avg_length = 5.0
        global_mood = "imperative"
        global_uses_emoji = False
    
    # Build final profile
    profile = {
        "global": {
            "avg_length": round(global_avg_length, 1),
            "mood": global_mood,
            "uses_emoji": global_uses_emoji
        },
        "repos": repos,
        "last_scan": datetime.now(timezone.utc).isoformat()
    }
    
    return profile

def suggest_commit_message(repo_path: str, profile: Dict[str, Any], current_message: str = "") -> List[str]:
    """
    Generate adaptive commit message coaching suggestions based on profile
    Returns list of non-blocking suggestions
    """
    suggestions = []
    
    # Get repo name for profile lookup
    repo_name = os.path.basename(repo_path)
    remote_url = run_git(["config", "--get", "remote.origin.url"], repo_path)
    if remote_url:
        if remote_url.endswith('.git'):
            remote_url = remote_url[:-4]
        repo_name = remote_url.split('/')[-1]
    
    repo_profile = profile.get("repos", {}).get(repo_name, {})
    global_profile = profile.get("global", {})
    
    if not current_message:
        return suggestions
    
    words = current_message.split()
    repo_style = repo_profile.get("commit_style", {})
    
    # Check if user has freeform style (>80% unprefixed commits)
    freeform_ratio = repo_style.get("freeform_ratio", 0.5)
    is_freeform_style = freeform_ratio > 0.8
    
    if is_freeform_style:
        # Freeform style: suggest length/clarity only
        if len(words) < 5:
            # Suggest more detail for short messages
            example_expansion = current_message.lower()
            if "fix" in example_expansion:
                example = f"{current_message} → {current_message.replace('fix', 'fixed login crash')}"
            elif "update" in example_expansion:
                example = f"{current_message} → {current_message.replace('update', 'updated user dashboard')}"
            elif "add" in example_expansion:
                example = f"{current_message} → {current_message.replace('add', 'added search filter')}"
            else:
                example = f"'{current_message}' → add specific details"
            
            suggestions.append(f"💡 Casual style detected—add detail? E.g., {example}")
        
        # Check for vague words that could be more specific
        vague_words = ["stuff", "things", "issues", "problems", "code"]
        for vague in vague_words:
            if vague in current_message.lower():
                suggestions.append(f"💡 '{vague}' is vague—what specifically? E.g., 'fixed login {vague}' → 'fixed login validation'")
                break
                
    else:
        # Traditional style: keep existing prefix/mood/case/emoji suggestions
        
        # Prefix suggestions
        common_prefixes = repo_style.get("common_prefixes", [])
        if common_prefixes and not any(current_message.lower().startswith(prefix.lower()) for prefix in common_prefixes):
            top_prefix = common_prefixes[0]
            suggestions.append(f"💡 Your '{repo_name}' uses '{top_prefix}'—try '{top_prefix} {current_message}'?")
        
        # Case style suggestions
        mood = repo_style.get("case_style", global_profile.get("mood", "imperative"))
        first_word = words[0] if words else ""
        
        if mood == "imperative" and first_word.lower() in ["added", "fixed", "updated", "removed"]:
            imperative_word = first_word.lower().replace("added", "add").replace("fixed", "fix").replace("updated", "update").replace("removed", "remove")
            suggestions.append(f"💡 Try imperative: '{imperative_word.capitalize()} {' '.join(words[1:])}' vs '{current_message}'")
        
        if mood == "lowercase" and first_word and first_word[0].isupper():
            suggestions.append(f"💡 Try lowercase: '{current_message.lower()}'")
        
        # Emoji suggestions
        uses_emoji = repo_style.get("uses_emoji", global_profile.get("uses_emoji", False))
        emoji_pattern = re.compile(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U000024C2-\U0001F251]+')
        
        if uses_emoji and not emoji_pattern.search(current_message):
            suggestions.append("💡 Add an emoji? 😎")
    
    # Length suggestions (apply to both styles)
    repo_avg = repo_style.get("avg_length", global_profile.get("avg_length", 5))
    if len(words) < 0.7 * repo_avg:
        suggestions.append(f"💡 Your messages avg {repo_avg} words—expand? E.g., '{current_message} (add details)'")
    
    return suggestions

def get_stack_suggestions(repo_path: str, profile: Dict[str, Any]) -> List[str]:
    """
    Generate stack-aware suggestions based on recent changes
    Returns list of helpful suggestions
    """
    suggestions = []
    
    # Get repo name and profile
    repo_name = os.path.basename(repo_path)
    remote_url = run_git(["config", "--get", "remote.origin.url"], repo_path)
    if remote_url:
        if remote_url.endswith('.git'):
            remote_url = remote_url[:-4]
        repo_name = remote_url.split('/')[-1]
    
    repo_profile = profile.get("repos", {}).get(repo_name, {})
    tech_stack = repo_profile.get("tech_stack", [])
    
    # Check recent changes
    changed_files = run_git(["diff", "--name-only", "HEAD~1"], repo_path)
    if not changed_files:
        changed_files = run_git(["diff", "--name-only", "--cached"], repo_path)  # Check staged changes
    
    if not changed_files:
        return suggestions
    
    changed_list = changed_files.split('\n')
    
    # Stack-specific suggestions
    if "javascript" in tech_stack or "react" in tech_stack:
        if "package.json" in changed_list and "package-lock.json" not in changed_list:
            suggestions.append("💡 JavaScript/React: Run 'npm install' to update lockfile?")
    
    if "typescript" in tech_stack:
        if any(f.endswith('.ts') for f in changed_list):
            suggestions.append("💡 TypeScript: Run 'tsc' to compile?")
    
    if "python" in tech_stack:
        if "django" in tech_stack:
            if any("models.py" in f for f in changed_list) and not any("migrations/" in f for f in changed_list):
                suggestions.append("💡 Django: Run 'python manage.py makemigrations'?")
        
        if "requirements.txt" in changed_list or "setup.py" in changed_list:
            suggestions.append("💡 Python: Update virtual environment with new dependencies?")
    
    if "rust" in tech_stack:
        if "Cargo.toml" in changed_list and "Cargo.lock" not in changed_list:
            suggestions.append("💡 Rust: Run 'cargo check' to update Cargo.lock?")
    
    if "php" in tech_stack:
        if "composer.json" in changed_list and "composer.lock" not in changed_list:
            suggestions.append("💡 PHP: Run 'composer install' for lockfile?")
    
    if "swift" in tech_stack:
        if "Podfile" in changed_list:
            suggestions.append("💡 Swift: Update pods?")
    
    if "kotlin" in tech_stack:
        if "build.gradle" in changed_list or "build.gradle.kts" in changed_list:
            suggestions.append("💡 Kotlin: Gradle sync?")
    
    if "elixir" in tech_stack:
        if "mix.exs" in changed_list:
            suggestions.append("💡 Elixir: Run 'mix deps.get'?")
    
    if "scala" in tech_stack:
        if "build.sbt" in changed_list:
            suggestions.append("💡 Scala: SBT reload?")
    
    if "haskell" in tech_stack:
        if "cabal.project" in changed_list or "package.yaml" in changed_list:
            suggestions.append("💡 Haskell: Cabal update?")
    
    return suggestions

def get_structure_suggestions(repo_path: str, profile: Dict[str, Any]) -> List[str]:
    """
    Generate structure-based suggestions
    Returns list of maintenance suggestions
    """
    suggestions = []
    
    # Get repo name and profile
    repo_name = os.path.basename(repo_path)
    remote_url = run_git(["config", "--get", "remote.origin.url"], repo_path)
    if remote_url:
        if remote_url.endswith('.git'):
            remote_url = remote_url[:-4]
        repo_name = remote_url.split('/')[-1]
    
    repo_profile = profile.get("repos", {}).get(repo_name, {})
    structure = repo_profile.get("structure", {})
    
    # Check last 5 commits for patterns
    changed_files_output = run_git(["log", "--name-only", "-5", "--pretty=format:"], repo_path)
    if not changed_files_output:
        return suggestions
    
    changed_files = [f.strip() for f in changed_files_output.split('\n') if f.strip()]
    
    # Source code vs tests analysis
    source_changes = any(any(dir_name in f for dir_name in ["src", "app", "lib"]) for f in changed_files)
    test_changes = any(any(test_dir in f for test_dir in ["test", "tests", "spec", "__tests__"]) for f in changed_files)
    has_tests_dir = structure.get("has_tests_dir", False)
    
    if source_changes and not test_changes and not has_tests_dir:
        suggestions.append("💡 No tests updated—add one for your changes?")
    
    # Documentation checks
    readme_changed = any("readme" in f.lower() for f in changed_files)
    significant_changes = len([f for f in changed_files if f.endswith(('.py', '.js', '.ts', '.rs', '.java', '.go'))]) > 3
    
    if significant_changes and not readme_changed:
        suggestions.append("📝 README might be stale—update with new features?")
    
    return suggestions

def get_commit_size_suggestions(repo_path: str) -> List[str]:
    """
    Generate commit size nudge suggestions based on git diff stats
    Returns list of suggestions for commit granularity
    """
    suggestions = []
    
    try:
        # Get diff stats for staged changes or last commit
        diff_stat = run_git(["diff", "--stat", "--cached"], repo_path)
        if not diff_stat:
            diff_stat = run_git(["diff", "--stat", "HEAD~1"], repo_path)
        
        if not diff_stat:
            return suggestions
            
        lines = diff_stat.strip().split('\n')
        if len(lines) < 2:
            return suggestions
            
        # Parse the summary line (e.g., "5 files changed, 123 insertions(+), 45 deletions(-)")
        summary_line = lines[-1]
        files_changed = 0
        lines_changed = 0
        
        # Extract number of files changed
        if "file" in summary_line:
            files_match = re.search(r'(\d+)\s+file', summary_line)
            if files_match:
                files_changed = int(files_match.group(1))
        
        # Extract lines changed (insertions + deletions)
        insertions_match = re.search(r'(\d+)\s+insertion', summary_line)
        deletions_match = re.search(r'(\d+)\s+deletion', summary_line)
        
        if insertions_match:
            lines_changed += int(insertions_match.group(1))
        if deletions_match:
            lines_changed += int(deletions_match.group(1))
        
        # Generate suggestions based on size
        if lines_changed > 100 or files_changed > 10:
            suggestions.append(f"💡 Large commit ({lines_changed}+ lines, {files_changed} files)—split into smaller commits?")
        elif lines_changed < 5 and files_changed == 1:
            # Check if it's not a doc file
            non_doc_extensions = ['.py', '.js', '.ts', '.rs', '.java', '.go', '.cs', '.rb', '.php', '.swift', '.kt', '.ex', '.scala', '.hs']
            changed_files = [line.split()[0] for line in lines[:-1] if '|' in line]
            
            if changed_files and any(any(f.endswith(ext) for ext in non_doc_extensions) for f in changed_files):
                suggestions.append("💡 Tiny commit—bundle with related changes?")
    
    except Exception:
        # Don't break on git errors
        pass
    
    return suggestions

def get_til_tag_suggestions(repo_path: str, profile: Dict[str, Any], til_title: str = "") -> List[str]:
    """
    Generate TIL tag suggestions based on repo context and commit keywords
    Returns list of tag suggestions
    """
    suggestions = []
    
    try:
        # Get repo name and profile
        repo_name = os.path.basename(repo_path)
        remote_url = run_git(["config", "--get", "remote.origin.url"], repo_path)
        if remote_url:
            if remote_url.endswith('.git'):
                remote_url = remote_url[:-4]
            repo_name = remote_url.split('/')[-1]
        
        repo_profile = profile.get("repos", {}).get(repo_name, {})
        tech_stack = repo_profile.get("tech_stack", [])
        
        # Suggest tags from tech stack
        if tech_stack:
            primary_tech = tech_stack[0]  # Most relevant tech
            suggestions.append(f"💡 Add --tag {primary_tech}? (detected {primary_tech.title()} repo)")
        
        # Get recent commit keywords for contextual suggestions
        if til_title:
            recent_commit = run_git(["log", "-1", "--format=%s"], repo_path)
            if recent_commit:
                commit_lower = recent_commit.lower()
                keyword_tags = {
                    "async": "async",
                    "test": "testing",
                    "debug": "debugging",
                    "performance": "optimization",
                    "security": "security",
                    "database": "database",
                    "api": "api",
                    "frontend": "frontend",
                    "backend": "backend",
                    "deployment": "deployment",
                    "docker": "docker",
                    "git": "git"
                }
                
                for keyword, tag in keyword_tags.items():
                    if keyword in commit_lower or keyword in til_title.lower():
                        suggestions.append(f"💡 Add --tag {tag}? (detected '{keyword}' context)")
                        break  # Only suggest one contextual tag
    
    except Exception:
        # Don't break on git errors
        pass
    
    return suggestions

def update_freeform_feedback(profile: Dict[str, Any], repo_path: str, feedback: str) -> Dict[str, Any]:
    """
    Update freeform ratio based on user feedback
    Returns updated profile
    """
    # Get repo name
    repo_name = os.path.basename(repo_path)
    remote_url = run_git(["config", "--get", "remote.origin.url"], repo_path)
    if remote_url:
        if remote_url.endswith('.git'):
            remote_url = remote_url[:-4]
        repo_name = remote_url.split('/')[-1]
    
    # Update freeform ratio based on feedback
    if repo_name in profile.get("repos", {}):
        repo_profile = profile["repos"][repo_name]
        commit_style = repo_profile.get("commit_style", {})
        current_ratio = commit_style.get("freeform_ratio", 0.5)
        
        if feedback.lower() == "bad":
            # User doesn't like prefix suggestions, increase freeform ratio
            new_ratio = min(1.0, current_ratio + 0.1)
        elif feedback.lower() == "good":
            # User likes prefix suggestions, decrease freeform ratio
            new_ratio = max(0.0, current_ratio - 0.1)
        else:
            return profile
        
        commit_style["freeform_ratio"] = round(new_ratio, 2)
        profile["repos"][repo_name]["commit_style"] = commit_style
    
    return profile

def play_sound(sound_file: str) -> None:
    """
    Play notification sound (non-blocking)
    """
    try:
        import sys
        sound_path = os.path.join(os.path.dirname(__file__), '..', 'sounds', sound_file)
        if os.path.exists(sound_path):
            if os.name == 'nt':  # Windows
                import winsound
                winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
            elif os.name == 'posix':  # macOS/Linux
                subprocess.Popen(['afplay' if sys.platform == 'darwin' else 'aplay', sound_path],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        # Fallback: don't break if sound fails
        pass
