import os
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path


ACHIEVEMENTS_PATH = os.path.expanduser("~/.commit-checker/achievements.json")
XP_PATH = os.path.expanduser("~/.commit-checker/xp.json")

# Achievement definitions with ASCII art and rarity
ACHIEVEMENTS = {
    "streak_3": {
        "name": "Getting Started",
        "description": "3-day commit streak",
        "rarity": "common",
        "emoji": "🟩",
        "ascii": [
            " ██████╗ ██████╗ ",
            "██╔═══██╗╚════██╗",
            "██║   ██║ █████╔╝",
            "██║▄▄ ██║ ╚═══██╗",
            "╚██████╔╝██████╔╝",
            " ╚══▀▀═╝ ╚═════╝ "
        ]
    },
    "streak_7": {
        "name": "Week Warrior",
        "description": "7-day commit streak",
        "rarity": "common",
        "emoji": "🟩",
        "ascii": [
            "███████╗",
            "╚════██║",
            "    ██╔╝",
            "   ██╔╝ ",
            "   ██║  ",
            "   ╚═╝  "
        ]
    },
    "streak_14": {
        "name": "Fortnight Fighter",
        "description": "14-day commit streak",
        "rarity": "rare",
        "emoji": "🟦",
        "ascii": [
            "  ██╗██╗  ██╗",
            " ███║██║  ██║",
            " ╚██║███████║",
            "  ██║╚════██║",
            "  ██║     ██║",
            "  ╚═╝     ╚═╝"
        ]
    },
    "streak_30": {
        "name": "Monthly Master",
        "description": "30-day commit streak",
        "rarity": "epic",
        "emoji": "🟨",
        "ascii": [
            "██████╗  ██████╗ ",
            "╚════██╗██╔═████╗",
            " █████╔╝██║██╔██║",
            " ╚═══██╗████╔╝██║",
            "██████╔╝╚██████╔╝",
            "╚═════╝  ╚═════╝ "
        ]
    },
    "streak_90": {
        "name": "Legendary Coder",
        "description": "90-day commit streak",
        "rarity": "legendary",
        "emoji": "🟥",
        "ascii": [
            "██████╗  ██████╗ ",
            "██╔══██╗██╔═████╗",
            "██████╔╝██║██╔██║",
            "██╔═══╝ ████╔╝██║",
            "██║     ╚██████╔╝",
            "╚═╝      ╚═════╝ "
        ]
    },
    "streak_365": {
        "name": "Code Deity",
        "description": "365-day commit streak",
        "rarity": "mythic",
        "emoji": "🟪",
        "ascii": [
            "██████╗  ██████╗ ███████╗",
            "╚════██╗██╔════╝ ██╔════╝",
            " █████╔╝███████╗ ███████╗",
            " ╚═══██╗██╔═══██╗╚════██║",
            "██████╔╝╚██████╔╝███████║",
            "╚═════╝  ╚═════╝ ╚══════╝"
        ]
    },
    "first_commit": {
        "name": "Hello World",
        "description": "Made your first tracked commit",
        "rarity": "common",
        "emoji": "🟩",
        "ascii": [
            "██╗  ██╗██╗",
            "██║  ██║██║",
            "███████║██║",
            "██╔══██║██║",
            "██║  ██║██║",
            "╚═╝  ╚═╝╚═╝"
        ]
    },
    "hundred_commits": {
        "name": "Century Club",
        "description": "Made 100 total commits",
        "rarity": "rare",
        "emoji": "🟦",
        "ascii": [
            "  ██╗ ██████╗  ██████╗ ",
            " ███║██╔═████╗██╔═████╗",
            " ╚██║██║██╔██║██║██╔██║",
            "  ██║████╔╝██║████╔╝██║",
            "  ██║╚██████╔╝╚██████╔╝",
            "  ╚═╝ ╚═════╝  ╚═════╝ "
        ]
    },
    "thousand_commits": {
        "name": "Commit Overlord",
        "description": "Made 1000 total commits",
        "rarity": "legendary",
        "emoji": "🟥",
        "ascii": [
            "  ██╗ ██████╗  ██████╗  ██████╗ ",
            " ███║██╔═████╗██╔═████╗██╔═████╗",
            " ╚██║██║██╔██║██║██╔██║██║██╔██║",
            "  ██║████╔╝██║████╔╝██║████╔╝██║",
            "  ██║╚██████╔╝╚██████╔╝╚██████╔╝",
            "  ╚═╝ ╚═════╝  ╚═════╝  ╚═════╝ "
        ]
    },
    "big_diff": {
        "name": "Code Tsunami",
        "description": "Single commit with 500+ line changes",
        "rarity": "epic",
        "emoji": "🟨",
        "ascii": [
            "████████╗███████╗██╗   ██╗",
            "╚══██╔══╝██╔════╝██║   ██║",
            "   ██║   ███████╗██║   ██║",
            "   ██║   ╚════██║██║   ██║",
            "   ██║   ███████║╚██████╔╝",
            "   ╚═╝   ╚══════╝ ╚═════╝ "
        ]
    }
}

# XP Level thresholds
XP_LEVELS = [
    {"level": 1, "threshold": 0, "title": "Novice Coder"},
    {"level": 2, "threshold": 100, "title": "Code Apprentice"},
    {"level": 3, "threshold": 250, "title": "Script Warrior"},
    {"level": 4, "threshold": 500, "title": "Function Master"},
    {"level": 5, "threshold": 1000, "title": "Class Hero"},
    {"level": 6, "threshold": 2000, "title": "Module Sage"},
    {"level": 7, "threshold": 4000, "title": "Framework Knight"},
    {"level": 8, "threshold": 8000, "title": "Architecture Lord"},
    {"level": 9, "threshold": 15000, "title": "Code Overlord"},
    {"level": 10, "threshold": 30000, "title": "Programming Deity"}
]


def ensure_gamification_files():
    """Ensure gamification files exist"""
    os.makedirs(os.path.dirname(ACHIEVEMENTS_PATH), exist_ok=True)
    
    if not os.path.exists(ACHIEVEMENTS_PATH):
        with open(ACHIEVEMENTS_PATH, 'w') as f:
            json.dump({"unlocked": [], "progress": {}}, f, indent=2)
    
    if not os.path.exists(XP_PATH):
        with open(XP_PATH, 'w') as f:
            json.dump({"total_xp": 0, "level": 1, "commits_tracked": 0}, f, indent=2)


def load_achievements():
    """Load achievements data"""
    ensure_gamification_files()
    with open(ACHIEVEMENTS_PATH, 'r') as f:
        return json.load(f)


def save_achievements(data):
    """Save achievements data"""
    ensure_gamification_files()
    with open(ACHIEVEMENTS_PATH, 'w') as f:
        json.dump(data, f, indent=2)


def load_xp_data():
    """Load XP data"""
    ensure_gamification_files()
    with open(XP_PATH, 'r') as f:
        return json.load(f)


def save_xp_data(data):
    """Save XP data"""
    ensure_gamification_files()
    with open(XP_PATH, 'w') as f:
        json.dump(data, f, indent=2)


def calculate_commit_xp(repo_path, commit_hash, config):
    """Calculate XP for a specific commit based on diff stats"""
    try:
        # Get diff stats for the commit
        diff_output = subprocess.check_output([
            "git", "--git-dir", os.path.join(repo_path, ".git"), 
            "--work-tree", repo_path,
            "show", "--stat", "--format=", commit_hash
        ], stderr=subprocess.DEVNULL).decode("utf-8").strip()
        
        if not diff_output:
            return 0
        
        # Parse insertions and deletions
        insertions = deletions = 0
        for line in diff_output.split('\n'):
            if 'insertion' in line or 'deletion' in line:
                parts = line.split()
                for i, part in enumerate(parts):
                    if 'insertion' in part:
                        insertions = int(parts[i-1]) if parts[i-1].isdigit() else 0
                    elif 'deletion' in part:
                        deletions = int(parts[i-1]) if parts[i-1].isdigit() else 0
        
        # Get repo name
        repo_name = os.path.basename(repo_path)
        
        # Load XP weights from config
        xp_weights = config.get('xp_weights', {
            'insertions': 1,
            'deletions': 0.5,
            'projects': {}
        })
        
        # Calculate base XP
        base_xp = (insertions * xp_weights.get('insertions', 1) + 
                   deletions * xp_weights.get('deletions', 0.5))
        
        # Apply project multiplier
        project_multiplier = xp_weights.get('projects', {}).get(repo_name, 1.0)
        
        total_xp = int(base_xp * project_multiplier)
        
        # Check for big diff achievement
        if insertions + deletions >= 500:
            unlock_achievement("big_diff")
        
        return total_xp
        
    except Exception:
        return 0


def add_xp(amount, commit_info=None):
    """Add XP and check for level up"""
    xp_data = load_xp_data()
    old_level = xp_data['level']
    
    xp_data['total_xp'] += amount
    xp_data['commits_tracked'] += 1
    
    # Check for level up
    new_level = get_level_from_xp(xp_data['total_xp'])
    if new_level > old_level:
        xp_data['level'] = new_level
        save_xp_data(xp_data)
        return True, new_level  # Level up occurred
    
    save_xp_data(xp_data)
    return False, new_level  # No level up


def get_level_from_xp(total_xp):
    """Get level from total XP"""
    for i in range(len(XP_LEVELS) - 1, -1, -1):
        if total_xp >= XP_LEVELS[i]['threshold']:
            return XP_LEVELS[i]['level']
    return 1


def get_xp_for_next_level(current_xp, current_level):
    """Get XP needed for next level"""
    if current_level >= len(XP_LEVELS):
        return 0  # Max level
    
    next_threshold = XP_LEVELS[current_level]['threshold']
    return max(0, next_threshold - current_xp)


def unlock_achievement(achievement_id):
    """Unlock an achievement"""
    achievements = load_achievements()
    
    if achievement_id not in achievements['unlocked'] and achievement_id in ACHIEVEMENTS:
        achievements['unlocked'].append(achievement_id)
        achievements['unlocked'].sort()  # Keep sorted
        save_achievements(achievements)
        return True
    return False


def check_streak_achievements(streak_days):
    """Check and unlock streak-based achievements"""
    achievements_unlocked = []
    
    milestones = [3, 7, 14, 30, 90, 365]
    for milestone in milestones:
        if streak_days >= milestone:
            achievement_id = f"streak_{milestone}"
            if unlock_achievement(achievement_id):
                achievements_unlocked.append(achievement_id)
    
    return achievements_unlocked


def check_total_commits_achievements(total_commits):
    """Check achievements based on total commits"""
    achievements_unlocked = []
    
    if total_commits >= 1:
        if unlock_achievement("first_commit"):
            achievements_unlocked.append("first_commit")
    
    if total_commits >= 100:
        if unlock_achievement("hundred_commits"):
            achievements_unlocked.append("hundred_commits")
    
    if total_commits >= 1000:
        if unlock_achievement("thousand_commits"):
            achievements_unlocked.append("thousand_commits")
    
    return achievements_unlocked


def get_current_streak(local_paths):
    """Calculate current commit streak"""
    if not local_paths:
        return 0
    
    streak = 0
    current_date = datetime.now().date()
    
    for path in local_paths:
        if not path or not os.path.exists(path):
            continue
            
        for root, dirs, files in os.walk(path):
            if '.git' in dirs:
                try:
                    # Get all commit dates
                    log_output = subprocess.check_output([
                        "git", "--git-dir", os.path.join(root, ".git"),
                        "--work-tree", root,
                        "log", "--since=90 days ago", "--format=%cd", "--date=short"
                    ], stderr=subprocess.DEVNULL).decode("utf-8").strip()
                    
                    if log_output:
                        commit_dates = set()
                        for line in log_output.split('\n'):
                            if line.strip():
                                commit_dates.add(datetime.strptime(line.strip(), "%Y-%m-%d").date())
                        
                        # Calculate streak
                        temp_streak = 0
                        check_date = current_date
                        
                        while check_date in commit_dates:
                            temp_streak += 1
                            check_date -= timedelta(days=1)
                        
                        streak = max(streak, temp_streak)
                        
                except Exception:
                    continue
                dirs.clear()
    
    return streak


def display_achievements():
    """Display all unlocked achievements with ASCII art"""
    achievements = load_achievements()
    unlocked = achievements['unlocked']
    
    if not unlocked:
        return "🏆 No achievements unlocked yet. Start committing to earn your first badge!"
    
    output = ["🏆 Achievement Gallery", "=" * 50, ""]
    
    # Group by rarity
    rarities = ["common", "rare", "epic", "legendary", "mythic"]
    rarity_colors = {"common": "🟩", "rare": "🟦", "epic": "🟨", "legendary": "🟥", "mythic": "🟪"}
    
    for rarity in rarities:
        rarity_achievements = [aid for aid in unlocked if ACHIEVEMENTS.get(aid, {}).get('rarity') == rarity]
        
        if rarity_achievements:
            output.append(f"{rarity_colors[rarity]} {rarity.upper()} BADGES")
            output.append("")
            
            for achievement_id in rarity_achievements:
                achievement = ACHIEVEMENTS[achievement_id]
                output.append(f"   {achievement['emoji']} {achievement['name']}")
                output.append(f"   {achievement['description']}")
                
                # Add ASCII art (compact version)
                for line in achievement['ascii'][:3]:  # Show only first 3 lines for compactness
                    output.append(f"   {line}")
                output.append("")
    
    return "\n".join(output)


def display_xp_status():
    """Display current XP and level status"""
    xp_data = load_xp_data()
    current_level = xp_data['level']
    current_xp = xp_data['total_xp']
    
    # Get level info
    level_info = None
    for level in XP_LEVELS:
        if level['level'] == current_level:
            level_info = level
            break
    
    if not level_info:
        level_info = XP_LEVELS[-1]  # Max level
    
    # Calculate progress to next level
    if current_level < len(XP_LEVELS):
        next_level_info = next((l for l in XP_LEVELS if l['level'] == current_level + 1), None)
        if next_level_info:
            xp_needed = next_level_info['threshold'] - current_xp
            progress = max(0, min(100, (current_xp - level_info['threshold']) / 
                                  (next_level_info['threshold'] - level_info['threshold']) * 100))
        else:
            xp_needed = 0
            progress = 100
    else:
        xp_needed = 0
        progress = 100
    
    # Create progress bar
    bar_length = 20
    filled = int(progress / 100 * bar_length)
    progress_bar = "█" * filled + "░" * (bar_length - filled)
    
    output = [
        f"⚡ Level {current_level}: {level_info['title']}",
        f"💫 Total XP: {current_xp:,}",
        f"📊 Progress: [{progress_bar}] {progress:.1f}%"
    ]
    
    if xp_needed > 0:
        output.append(f"🎯 Next Level: {xp_needed:,} XP needed")
    else:
        output.append("🏆 MAX LEVEL REACHED!")
    
    output.append(f"📈 Commits Tracked: {xp_data['commits_tracked']:,}")
    
    return "\n".join(output)


def process_commits_for_gamification(local_paths, config):
    """Process today's commits for XP and achievements"""
    if not local_paths:
        return {"xp_gained": 0, "achievements": [], "level_up": False}
    
    total_xp_gained = 0
    all_achievements = []
    level_up_occurred = False
    total_commits_today = 0
    
    for path in local_paths:
        if not path or not os.path.exists(path):
            continue
            
        for root, dirs, files in os.walk(path):
            if '.git' in dirs:
                try:
                    # Get today's commits
                    log_output = subprocess.check_output([
                        "git", "--git-dir", os.path.join(root, ".git"),
                        "--work-tree", root,
                        "log", "--since=midnight", "--pretty=format:%H"
                    ], stderr=subprocess.DEVNULL).decode("utf-8").strip()
                    
                    if log_output:
                        commit_hashes = log_output.split('\n')
                        total_commits_today += len(commit_hashes)
                        
                        for commit_hash in commit_hashes:
                            xp = calculate_commit_xp(root, commit_hash, config)
                            total_xp_gained += xp
                    
                except Exception:
                    continue
                dirs.clear()
    
    # Add XP and check for level up
    if total_xp_gained > 0:
        level_up_occurred, new_level = add_xp(total_xp_gained)
    
    # Check streak achievements
    current_streak = get_current_streak(local_paths)
    streak_achievements = check_streak_achievements(current_streak)
    all_achievements.extend(streak_achievements)
    
    # Check total commits achievements
    xp_data = load_xp_data()
    commit_achievements = check_total_commits_achievements(xp_data['commits_tracked'])
    all_achievements.extend(commit_achievements)
    
    return {
        "xp_gained": total_xp_gained,
        "achievements": all_achievements,
        "level_up": level_up_occurred,
        "new_level": new_level if level_up_occurred else None,
        "current_streak": current_streak,
        "commits_today": total_commits_today
    }
