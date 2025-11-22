"""User commit history learning module for commit-checker.

Analyzes user's past commits to learn their style and preferences.
Provides personalized recommendations based on historical patterns.
"""
import os
import re
import subprocess
from typing import Dict, List, Any, Optional
from collections import Counter, defaultdict
from datetime import datetime


def run_git(command: List[str], cwd: str) -> Optional[str]:
    """Run git command safely."""
    try:
        result = subprocess.check_output(
            ["git"] + command,
            cwd=cwd,
            stderr=subprocess.DEVNULL,
            text=True
        )
        return result.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def analyze_commit_history(repo_path: str, limit: int = 100) -> Dict[str, Any]:
    """Analyze user's commit history to learn their style.
    
    Extracts patterns like:
    - Message structure (prefixes, length, etc.)
    - Common phrases and keywords
    - Tone (formal vs casual)
    - Emoji usage
    - Conventional commit adoption
    
    Args:
        repo_path: Path to git repository
        limit: Number of recent commits to analyze
        
    Returns:
        Dict containing style profile
    """
    # Get commit messages
    log = run_git(
        ["log", f"-{limit}", "--pretty=format:%s"],
        repo_path
    )
    
    if not log:
        return get_default_profile()
    
    messages = [m.strip() for m in log.split('\n') if m.strip()]
    
    if not messages:
        return get_default_profile()
    
    # Analyze patterns
    prefixes = analyze_prefixes(messages)
    structure = analyze_structure(messages)
    keywords = analyze_keywords(messages)
    tone = analyze_tone(messages)
    emoji_usage = analyze_emoji_usage(messages)
    
    return {
        "total_commits": len(messages),
        "prefixes": prefixes,
        "structure": structure,
        "keywords": keywords,
        "tone": tone,
        "emoji": emoji_usage,
        "analyzed_at": datetime.now().isoformat()
    }


def get_default_profile() -> Dict[str, Any]:
    """Return default profile for repos with no history."""
    return {
        "total_commits": 0,
        "prefixes": {
            "uses_conventional": False,
            "common_prefixes": [],
            "prefix_ratio": 0.0
        },
        "structure": {
            "avg_length": 50,
            "avg_words": 7,
            "uses_capitalization": True
        },
        "keywords": {
            "top_keywords": [],
            "action_words": []
        },
        "tone": "imperative",
        "emoji": {
            "uses_emoji": False,
            "emoji_ratio": 0.0
        },
        "analyzed_at": datetime.now().isoformat()
    }


def analyze_prefixes(messages: List[str]) -> Dict[str, Any]:
    """Analyze commit message prefixes (e.g., feat:, fix:, etc.)."""
    conventional_pattern = re.compile(r'^([a-z]+)(\([^)]+\))?:\s+', re.IGNORECASE)
    
    prefixes = []
    conventional_count = 0
    
    for msg in messages:
        match = conventional_pattern.match(msg)
        if match:
            prefix = match.group(1).lower()
            prefixes.append(prefix)
            conventional_count += 1
    
    prefix_counter = Counter(prefixes)
    common_prefixes = [
        {"prefix": prefix, "count": count}
        for prefix, count in prefix_counter.most_common(5)
    ]
    
    return {
        "uses_conventional": conventional_count / len(messages) > 0.3,
        "common_prefixes": common_prefixes,
        "prefix_ratio": conventional_count / len(messages)
    }


def analyze_structure(messages: List[str]) -> Dict[str, Any]:
    """Analyze structural patterns in commit messages."""
    lengths = [len(msg) for msg in messages]
    word_counts = [len(msg.split()) for msg in messages]
    
    # Check capitalization
    capitalized = sum(1 for msg in messages if msg[0].isupper()) if messages else 0
    
    # Check for ending punctuation
    ends_with_period = sum(1 for msg in messages if msg.endswith('.'))
    
    return {
        "avg_length": int(sum(lengths) / len(lengths)),
        "avg_words": int(sum(word_counts) / len(word_counts)),
        "uses_capitalization": capitalized / len(messages) > 0.7,
        "uses_periods": ends_with_period / len(messages) > 0.3
    }


def analyze_keywords(messages: List[str]) -> Dict[str, Any]:
    """Extract common keywords and action words."""
    # Common action words
    action_words = ['add', 'fix', 'update', 'remove', 'refactor', 'implement',
                    'create', 'delete', 'modify', 'improve', 'enhance', 'optimize']
    
    # Extract all words (lowercase)
    all_words = []
    found_actions = []
    
    for msg in messages:
        words = re.findall(r'\b\w+\b', msg.lower())
        all_words.extend(words)
        
        # Check for action words
        for action in action_words:
            if action in words:
                found_actions.append(action)
    
    # Count frequencies
    word_counter = Counter(all_words)
    action_counter = Counter(found_actions)
    
    # Filter out common stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with'}
    meaningful_words = {w: c for w, c in word_counter.items() if w not in stop_words and len(w) > 3}
    
    top_keywords = [
        {"word": word, "count": count}
        for word, count in Counter(meaningful_words).most_common(10)
    ]
    
    top_actions = [
        {"word": action, "count": count}
        for action, count in action_counter.most_common(5)
    ]
    
    return {
        "top_keywords": top_keywords,
        "action_words": top_actions
    }


def analyze_tone(messages: List[str]) -> str:
    """Determine the dominant tone/style of commit messages."""
    # Imperative: "Add feature", "Fix bug"
    imperative_count = sum(
        1 for msg in messages
        if msg.split()[0].lower() in ['add', 'fix', 'update', 'remove', 'refactor', 
                                       'implement', 'create', 'delete', 'improve']
    )
    
    # Past tense: "Added feature", "Fixed bug"
    past_tense_count = sum(
        1 for msg in messages
        if msg.split()[0].lower() in ['added', 'fixed', 'updated', 'removed', 
                                       'refactored', 'implemented', 'created', 'deleted']
    )
    
    # Present continuous: "Adding feature", "Fixing bug"
    continuous_count = sum(
        1 for msg in messages
        if msg.split()[0].lower().endswith('ing')
    )
    
    # Determine dominant style
    if imperative_count > past_tense_count and imperative_count > continuous_count:
        return "imperative"
    elif past_tense_count > continuous_count:
        return "past_tense"
    elif continuous_count > 0:
        return "continuous"
    else:
        return "casual"


def analyze_emoji_usage(messages: List[str]) -> Dict[str, Any]:
    """Analyze emoji usage in commit messages."""
    emoji_pattern = re.compile(
        r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF'
        r'\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U000024C2-\U0001F251]+'
    )
    
    messages_with_emoji = sum(1 for msg in messages if emoji_pattern.search(msg))
    
    # Extract all emoji
    all_emoji = []
    for msg in messages:
        found = emoji_pattern.findall(msg)
        all_emoji.extend(found)
    
    emoji_counter = Counter(all_emoji)
    common_emoji = [
        {"emoji": emoji, "count": count}
        for emoji, count in emoji_counter.most_common(5)
    ]
    
    return {
        "uses_emoji": messages_with_emoji / len(messages) > 0.1,
        "emoji_ratio": messages_with_emoji / len(messages),
        "common_emoji": common_emoji
    }


def generate_style_summary(profile: Dict[str, Any]) -> str:
    """Generate human-readable summary of commit style."""
    if profile["total_commits"] == 0:
        return "No commit history found. Recommendations will use defaults."
    
    parts = []
    
    # Conventional commits
    if profile["prefixes"]["uses_conventional"]:
        top_prefix = profile["prefixes"]["common_prefixes"][0]["prefix"] if profile["prefixes"]["common_prefixes"] else "feat"
        parts.append(f"✓ Uses conventional commits (mostly `{top_prefix}:`)")
    else:
        parts.append("• Freeform style (no prefixes)")
    
    # Length
    avg_len = profile["structure"]["avg_length"]
    avg_words = profile["structure"]["avg_words"]
    parts.append(f"• Average: ~{avg_words} words ({avg_len} chars)")
    
    # Tone
    tone = profile["tone"]
    tone_desc = {
        "imperative": "Imperative mood (\"Add feature\")",
        "past_tense": "Past tense (\"Added feature\")",
        "continuous": "Present continuous (\"Adding feature\")",
        "casual": "Casual style"
    }
    parts.append(f"• {tone_desc.get(tone, tone)}")
    
    # Emoji
    if profile["emoji"]["uses_emoji"]:
        parts.append("• Uses emoji ✨")
    
    return "\n".join(parts)


def get_recommendations_from_profile(
    profile: Dict[str, Any],
    current_message: str
) -> List[str]:
    """Generate recommendations based on learned profile.
    
    Args:
        profile: User's commit style profile
        current_message: The message user is currently writing
        
    Returns:
        List of helpful suggestions
    """
    suggestions = []
    
    if not current_message:
        return suggestions
    
    # Prefix recommendation
    if profile["prefixes"]["uses_conventional"] and ':' not in current_message:
        top_prefix = "feat"
        if profile["prefixes"]["common_prefixes"]:
            top_prefix = profile["prefixes"]["common_prefixes"][0]["prefix"]
        suggestions.append(f"💡 Try adding `{top_prefix}:` prefix (you use it often)")
    
    # Length recommendation
    words = len(current_message.split())
    if words < profile["structure"]["avg_words"] * 0.6:
        suggestions.append(f"💡 Your messages usually have ~{profile['structure']['avg_words']} words. Add more detail?")
    
    # Capitalization
    if profile["structure"]["uses_capitalization"] and current_message and not current_message[0].isupper():
        suggestions.append("💡 Consider capitalizing first letter (matches your style)")
    
    # Emoji
    if profile["emoji"]["uses_emoji"] and not re.search(r'[\U0001F600-\U0001F64F]', current_message):
        if profile["emoji"]["common_emoji"]:
            emoji = profile["emoji"]["common_emoji"][0]["emoji"]
            suggestions.append(f"💡 Add an emoji? (you often use {emoji})")
    
    return suggestions


def save_profile_to_cache(repo_path: str, profile: Dict[str, Any]) -> bool:
    """Save learned profile to cache for faster future use."""
    try:
        from .config_manager import update_user_profile
        
        # Get repo name
        repo_name = os.path.basename(repo_path)
        
        # Update in config
        return update_user_profile({
            "repos": {
                repo_name: profile
            }
        })
    except Exception:
        return False


def load_profile_from_cache(repo_path: str) -> Optional[Dict[str, Any]]:
    """Load previously learned profile from cache."""
    try:
        from .config_manager import get_user_profile
        
        repo_name = os.path.basename(repo_path)
        profile_data = get_user_profile()
        
        return profile_data.get("repos", {}).get(repo_name)
    except Exception:
        return None


if __name__ == "__main__":
    # Test with commit-checker itself
    repo = "/Users/amariah/Documents/GitHub/commit-checker"
    
    print("🧠 Learning from your commit history...")
    print()
    
    profile = analyze_commit_history(repo, limit=50)
    
    print("📊 Your Commit Style Profile:")
    print("=" * 50)
    print(generate_style_summary(profile))
    print()
    
    print("📝 Detailed Analysis:")
    print(f"  Total commits analyzed: {profile['total_commits']}")
    
    if profile['prefixes']['common_prefixes']:
        print(f"  Most used prefixes:")
        for p in profile['prefixes']['common_prefixes'][:3]:
            print(f"    • {p['prefix']}: {p['count']} times")
    
    if profile['keywords']['action_words']:
        print(f"  Favorite action words:")
        for a in profile['keywords']['action_words'][:3]:
            print(f"    • {a['word']}: {a['count']} times")
    
    print()
    print("💡 Testing recommendations...")
    test_msg = "add new feature"
    recs = get_recommendations_from_profile(profile, test_msg)
    if recs:
        print(f"  For message: \"{test_msg}\"")
        for rec in recs:
            print(f"  {rec}")
