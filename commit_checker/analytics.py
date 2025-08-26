import os
import subprocess
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import re


def get_commit_heatmap_data(local_paths, days=365):
    """Get commit data for heatmap generation"""
    if not local_paths:
        return {}
    
    commit_data = defaultdict(int)
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    
    for path in local_paths:
        if not path or not os.path.exists(path):
            continue
            
        for root, dirs, files in os.walk(path):
            if '.git' in dirs:
                try:
                    # Get commits in date range
                    log_output = subprocess.check_output([
                        "git", "--git-dir", os.path.join(root, ".git"),
                        "--work-tree", root,
                        "log", f"--since={start_date}", "--format=%cd", "--date=short"
                    ], stderr=subprocess.DEVNULL).decode("utf-8").strip()
                    
                    if log_output:
                        for line in log_output.split('\n'):
                            if line.strip():
                                commit_data[line.strip()] += 1
                    
                except Exception:
                    continue
                dirs.clear()
    
    return dict(commit_data)


def render_ascii_heatmap(commit_data, days=365):
    """Render ASCII heatmap of commits"""
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    
    # Create date range
    date_range = []
    current_date = start_date
    while current_date <= end_date:
        date_range.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)
    
    # Get commit counts for each date
    daily_commits = [commit_data.get(date, 0) for date in date_range]
    
    if not any(daily_commits):
        return "📅 No commits found in the specified period."
    
    # Determine intensity levels
    max_commits = max(daily_commits) if daily_commits else 1
    
    def get_intensity_char(count):
        if count == 0:
            return "░"
        elif count <= max_commits * 0.25:
            return "▒"
        elif count <= max_commits * 0.5:
            return "▓"
        elif count <= max_commits * 0.75:
            return "█"
        else:
            return "█"
    
    # Build heatmap
    output = []
    output.append(f"📅 Commit Heatmap (Last {days} days)")
    output.append("=" * 50)
    output.append("")
    
    # Group by weeks (7 days per row)
    weeks = []
    for i in range(0, len(daily_commits), 7):
        week = daily_commits[i:i+7]
        weeks.append(week)
    
    # Render weeks
    for week_idx, week in enumerate(weeks):
        week_chars = [get_intensity_char(count) for count in week]
        week_str = " ".join(week_chars)
        
        # Add week label
        week_start_date = start_date + timedelta(weeks=week_idx)
        week_label = week_start_date.strftime("%m/%d")
        
        output.append(f"{week_label}: {week_str}")
    
    # Add legend
    output.append("")
    output.append("Legend: ░ None  ▒ Low  ▓ Medium  █ High")
    output.append(f"Max commits in a day: {max_commits}")
    
    # Add recent activity summary
    recent_7_days = daily_commits[-7:]
    recent_total = sum(recent_7_days)
    output.append(f"Last 7 days: {recent_total} commits")
    
    return "\n".join(output)


def get_language_stats(local_paths):
    """Get programming language statistics from repositories"""
    if not local_paths:
        return {}
    
    language_stats = defaultdict(lambda: {"files": 0, "lines": 0})
    
    # File extension to language mapping
    lang_map = {
        ".py": "Python",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".jsx": "React",
        ".tsx": "React TypeScript",
        ".java": "Java",
        ".cpp": "C++",
        ".c": "C",
        ".h": "C/C++ Headers",
        ".cs": "C#",
        ".php": "PHP",
        ".rb": "Ruby",
        ".go": "Go",
        ".rs": "Rust",
        ".swift": "Swift",
        ".kt": "Kotlin",
        ".scala": "Scala",
        ".html": "HTML",
        ".css": "CSS",
        ".scss": "SCSS",
        ".sass": "Sass",
        ".less": "Less",
        ".vue": "Vue",
        ".svelte": "Svelte",
        ".sql": "SQL",
        ".sh": "Shell",
        ".bash": "Bash",
        ".zsh": "Zsh",
        ".fish": "Fish",
        ".ps1": "PowerShell",
        ".yaml": "YAML",
        ".yml": "YAML",
        ".json": "JSON",
        ".xml": "XML",
        ".md": "Markdown",
        ".tex": "LaTeX",
        ".r": "R",
        ".R": "R",
        ".m": "MATLAB",
        ".pl": "Perl",
        ".lua": "Lua",
        ".dart": "Dart",
        ".elm": "Elm",
        ".ex": "Elixir",
        ".exs": "Elixir",
        ".clj": "Clojure",
        ".hs": "Haskell",
        ".ml": "OCaml",
        ".fs": "F#",
        ".vim": "Vim Script",
        ".dockerfile": "Dockerfile",
        ".tf": "Terraform",
    }
    
    for path in local_paths:
        if not path or not os.path.exists(path):
            continue
            
        for root, dirs, files in os.walk(path):
            # Skip hidden directories and common non-code directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and 
                      d not in ['node_modules', '__pycache__', 'dist', 'build', 'target']]
            
            for file in files:
                if file.startswith('.'):
                    continue
                
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1].lower()
                
                # Special cases
                if file.lower() == "dockerfile":
                    file_ext = ".dockerfile"
                elif file.endswith(".tf"):
                    file_ext = ".tf"
                
                if file_ext in lang_map:
                    language = lang_map[file_ext]
                    language_stats[language]["files"] += 1
                    
                    # Count lines (basic count, skip binary files)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            lines = sum(1 for line in f if line.strip())
                            language_stats[language]["lines"] += lines
                    except (UnicodeDecodeError, OSError):
                        # Skip binary files or files we can't read
                        continue
    
    return dict(language_stats)


def render_language_pie_chart(language_stats):
    """Render ASCII pie chart of language usage"""
    if not language_stats:
        return "📊 No language statistics available."
    
    # Sort by lines of code
    sorted_langs = sorted(language_stats.items(), 
                         key=lambda x: x[1]["lines"], reverse=True)
    
    total_lines = sum(stats["lines"] for stats in language_stats.values())
    
    if total_lines == 0:
        return "📊 No code lines found."
    
    output = []
    output.append("📊 Programming Language Breakdown")
    output.append("=" * 50)
    output.append("")
    
    # Show top languages with percentages
    for i, (language, stats) in enumerate(sorted_langs[:10]):  # Top 10
        percentage = (stats["lines"] / total_lines) * 100
        
        # Create visual bar
        bar_length = 30
        filled = int(percentage / 100 * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        output.append(f"{language:15} [{bar}] {percentage:5.1f}% ({stats['lines']:,} lines, {stats['files']} files)")
    
    output.append("")
    output.append(f"📈 Total: {total_lines:,} lines across {sum(s['files'] for s in language_stats.values())} files")
    
    return "\n".join(output)


def get_mood_commit_line(xp_gained, commits_today, current_streak):
    """Generate mood-based commit status line"""
    mood_messages = {
        "fire": ["🔥 You're in the zone!", "🚀 Coding machine!", "⚡ On fire today!"],
        "good": ["💪 Great work!", "👍 Solid progress!", "✨ Nice commits!"],
        "okay": ["📝 Making progress", "⚙️ Steady coding", "📈 Building momentum"],
        "low": ["🌱 Every commit counts", "📚 Learning and growing", "🎯 Keep going!"],
        "none": ["💤 Time to code?", "🎪 Ready to commit?", "🌟 Start your streak!"]
    }
    
    # Determine mood based on activity
    if commits_today >= 5 or xp_gained >= 200:
        mood = "fire"
    elif commits_today >= 3 or xp_gained >= 100:
        mood = "good"
    elif commits_today >= 1 or xp_gained > 0:
        mood = "okay"
    elif current_streak > 0:
        mood = "low"
    else:
        mood = "none"
    
    import random
    message = random.choice(mood_messages[mood])
    
    # Build status line
    status_parts = []
    if commits_today > 0:
        status_parts.append(f"{commits_today} commits today")
    if xp_gained > 0:
        status_parts.append(f"+{xp_gained} XP")
    if current_streak > 0:
        status_parts.append(f"{current_streak}🔥 streak")
    
    if status_parts:
        return f"⚡ {' | '.join(status_parts)} | {message}"
    else:
        return f"⚡ {message}"


def export_heatmap_svg(commit_data, output_path, days=365):
    """Export heatmap as SVG (basic implementation)"""
    try:
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        # Create SVG content
        svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="800" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect width="800" height="200" fill="#f6f8fa"/>
  <text x="10" y="20" font-family="Arial" font-size="14" fill="#333">Commit Activity</text>
'''
        
        # Add heatmap squares
        current_date = start_date
        x, y = 10, 40
        max_commits = max(commit_data.values()) if commit_data else 1
        
        for week in range(53):  # Approximate weeks in a year
            for day in range(7):
                date_str = current_date.strftime("%Y-%m-%d")
                commits = commit_data.get(date_str, 0)
                
                # Calculate color intensity
                if commits == 0:
                    color = "#ebedf0"
                elif commits <= max_commits * 0.25:
                    color = "#9be9a8"
                elif commits <= max_commits * 0.5:
                    color = "#40c463"
                elif commits <= max_commits * 0.75:
                    color = "#30a14e"
                else:
                    color = "#216e39"
                
                svg_content += f'  <rect x="{x + week * 12}" y="{y + day * 12}" width="10" height="10" fill="{color}" rx="2"/>\n'
                
                current_date += timedelta(days=1)
                if current_date > end_date:
                    break
            if current_date > end_date:
                break
        
        svg_content += '</svg>'
        
        with open(output_path, 'w') as f:
            f.write(svg_content)
        
        return True, f"Heatmap exported to {output_path}"
    
    except Exception as e:
        return False, f"Failed to export heatmap: {e}"


def get_weekly_commit_stats(local_paths, weeks=4):
    """Get weekly commit statistics"""
    if not local_paths:
        return []
    
    weekly_stats = []
    end_date = datetime.now().date()
    
    for week_num in range(weeks):
        week_end = end_date - timedelta(days=week_num * 7)
        week_start = week_end - timedelta(days=6)
        
        week_commits = 0
        
        for path in local_paths:
            if not path or not os.path.exists(path):
                continue
                
            for root, dirs, files in os.walk(path):
                if '.git' in dirs:
                    try:
                        log_output = subprocess.check_output([
                            "git", "--git-dir", os.path.join(root, ".git"),
                            "--work-tree", root,
                            "log", f"--since={week_start}", f"--until={week_end}", 
                            "--oneline"
                        ], stderr=subprocess.DEVNULL).decode("utf-8").strip()
                        
                        if log_output:
                            week_commits += len(log_output.split('\n'))
                        
                    except Exception:
                        continue
                    dirs.clear()
        
        weekly_stats.append({
            "week_start": week_start,
            "week_end": week_end,
            "commits": week_commits
        })
    
    return list(reversed(weekly_stats))  # Most recent first


def render_commit_trend(weekly_stats):
    """Render ASCII trend chart of commits"""
    if not weekly_stats:
        return "📈 No trend data available."
    
    output = []
    output.append("📈 Commit Trend (Last 4 Weeks)")
    output.append("=" * 40)
    output.append("")
    
    max_commits = max(week["commits"] for week in weekly_stats) if weekly_stats else 1
    
    for week in weekly_stats:
        # Create bar
        bar_length = 20
        if max_commits > 0:
            filled = int((week["commits"] / max_commits) * bar_length)
        else:
            filled = 0
        
        bar = "█" * filled + "░" * (bar_length - filled)
        week_label = week["week_start"].strftime("%m/%d")
        
        output.append(f"{week_label}: [{bar}] {week['commits']} commits")
    
    return "\n".join(output)


def analyze_commit_message(message):
    """Analyze commit message and provide feedback"""
    suggestions = []
    
    # Rule 1: Should start with a verb
    verbs = ['add', 'fix', 'update', 'remove', 'refactor', 'improve', 'create', 'delete', 
            'implement', 'enhance', 'optimize', 'clean', 'merge', 'bump', 'revert']
    
    if not any(message.lower().startswith(verb) for verb in verbs):
        suggestions.append("Consider starting with an action verb (Add/Fix/Update/etc.)")
    
    # Rule 2: Check for vague messages
    vague_patterns = ['update code', 'fix stuff', 'changes', 'misc', 'wip', 'temp', 'test']
    if any(pattern in message.lower() for pattern in vague_patterns):
        suggestions.append("Message is too vague. Be more specific about what changed")
    
    # Rule 3: Check length
    if len(message) < 10:
        suggestions.append("Message is too short. Add more detail about the change")
    elif len(message) > 72:
        suggestions.append("Message is quite long. Consider keeping first line under 72 characters")
    
    # Rule 4: Check for proper capitalization
    if message and not message[0].isupper():
        suggestions.append("Consider starting with a capital letter")
    
    # Rule 5: Check for ending period
    if message.endswith('.'):
        suggestions.append("Avoid ending commit messages with a period")
    
    return suggestions


def get_commit_time_stats(local_paths, days=30):
    """Analyze commit timing patterns"""
    if not local_paths:
        return {}
    
    time_buckets = {
        "morning": 0,    # 6 AM - 12 PM
        "afternoon": 0,  # 12 PM - 6 PM  
        "evening": 0,    # 6 PM - 12 AM
        "night": 0       # 12 AM - 6 AM
    }
    
    since_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    
    for path in local_paths:
        if not path or not os.path.exists(path):
            continue
            
        for root, dirs, files in os.walk(path):
            if '.git' in dirs:
                try:
                    # Get commit timestamps
                    log_output = subprocess.check_output([
                        "git", "--git-dir", os.path.join(root, ".git"),
                        "--work-tree", root,
                        "log", f"--since={since_date}", "--format=%at"
                    ], stderr=subprocess.DEVNULL).decode("utf-8").strip()
                    
                    if log_output:
                        for timestamp in log_output.split('\n'):
                            if timestamp.strip():
                                # Convert timestamp to hour
                                dt = datetime.fromtimestamp(int(timestamp))
                                hour = dt.hour
                                
                                if 6 <= hour < 12:
                                    time_buckets["morning"] += 1
                                elif 12 <= hour < 18:
                                    time_buckets["afternoon"] += 1
                                elif 18 <= hour < 24:
                                    time_buckets["evening"] += 1
                                else:  # 0 <= hour < 6
                                    time_buckets["night"] += 1
                    
                except Exception:
                    continue
                dirs.clear()
    
    return time_buckets


def render_time_stats(time_buckets):
    """Render ASCII chart of commit time statistics"""
    if not time_buckets or not any(time_buckets.values()):
        return "⏰ No commit time data available."
    
    output = []
    output.append("⏰ Commit Time Stats (Last 30 Days)")
    output.append("=" * 40)
    output.append("")
    
    # Calculate max for scaling
    max_commits = max(time_buckets.values()) if time_buckets.values() else 1
    
    time_labels = {
        "morning": "Morning (6 AM–12 PM)",
        "afternoon": "Afternoon (12 PM–6 PM)", 
        "evening": "Evening (6 PM–12 AM)",
        "night": "Night (12 AM–6 AM)"
    }
    
    for time_period, count in time_buckets.items():
        # Create bar
        bar_length = 20
        if max_commits > 0:
            filled = int((count / max_commits) * bar_length)
        else:
            filled = 0
        
        bar = "█" * filled + "░" * (bar_length - filled)
        label = time_labels.get(time_period, time_period)
        
        output.append(f"{label}: [{bar}] {count} commits")
    
    return "\n".join(output)


def get_dashboard_stats(local_paths, config):
    """Get quick dashboard statistics"""
    from .gamification import process_commits_for_gamification, load_xp_data, get_current_streak
    from .checker import check_local_commits, get_most_active_repo
    
    stats = {}
    
    # Get today's commits
    local_commits = check_local_commits(local_paths)
    stats['commits_today'] = sum(commit[3] for commit in local_commits) if local_commits else 0
    
    # Get streak
    stats['current_streak'] = get_current_streak(local_paths)
    
    # Get XP and level data
    xp_data = load_xp_data()
    stats['level'] = xp_data.get('level', 1)
    stats['total_xp'] = xp_data.get('total_xp', 0)
    
    # Calculate XP for next level
    from .gamification import XP_LEVELS
    if stats['level'] < len(XP_LEVELS):
        next_level_info = next((l for l in XP_LEVELS if l['level'] == stats['level'] + 1), None)
        if next_level_info:
            stats['xp_needed'] = next_level_info['threshold'] - stats['total_xp']
            current_level_threshold = next((l for l in XP_LEVELS if l['level'] == stats['level']), {})['threshold']
            stats['xp_progress'] = stats['total_xp'] - current_level_threshold
            stats['xp_total_needed'] = next_level_info['threshold'] - current_level_threshold
        else:
            stats['xp_needed'] = 0
    else:
        stats['xp_needed'] = 0
        
    # Get most active repo
    repo_folder = config.get('repo_folder')
    if repo_folder:
        most_active = get_most_active_repo(repo_folder, "day")
        stats['top_repo'] = most_active['name'] if most_active and most_active['commits'] > 0 else None
        stats['top_repo_commits'] = most_active['commits'] if most_active else 0
    else:
        stats['top_repo'] = None
        stats['top_repo_commits'] = 0
    
    return stats


def render_dashboard(stats, config):
    """Render quick stats dashboard"""
    output = []
    output.append("📊 Today's Dashboard")
    output.append("=" * 30)
    output.append("")
    
    # Format based on output mode
    is_emoji = config.get('output', 'emoji') == 'emoji'
    
    if is_emoji:
        output.append(f"🟩 Commits Today: {stats['commits_today']}")
        output.append(f"🔥 Streak: {stats['current_streak']} days")
        
        # XP Progress bar
        if stats.get('xp_needed', 0) > 0:
            progress_pct = int((stats.get('xp_progress', 0) / stats.get('xp_total_needed', 1)) * 100)
            bar_length = 15
            filled = int((progress_pct / 100) * bar_length)
            progress_bar = "█" * filled + "░" * (bar_length - filled)
            output.append(f"⚡ Level {stats['level']}: [{progress_bar}] {stats['total_xp']}/{stats['total_xp'] + stats['xp_needed']} XP")
        else:
            output.append(f"⚡ Level {stats['level']}: MAX LEVEL")
        
        if stats.get('top_repo'):
            output.append(f"📁 Top Repo: {stats['top_repo']} ({stats['top_repo_commits']} commits)")
        else:
            output.append("📁 Top Repo: None today")
    else:
        output.append(f"Commits Today: {stats['commits_today']}")
        output.append(f"Streak: {stats['current_streak']} days")
        
        if stats.get('xp_needed', 0) > 0:
            output.append(f"Level {stats['level']}: {stats['total_xp']}/{stats['total_xp'] + stats['xp_needed']} XP")
        else:
            output.append(f"Level {stats['level']}: MAX LEVEL")
        
        if stats.get('top_repo'):
            output.append(f"Top Repo: {stats['top_repo']} ({stats['top_repo_commits']} commits)")
        else:
            output.append("Top Repo: None today")
    
    return "\n".join(output)
