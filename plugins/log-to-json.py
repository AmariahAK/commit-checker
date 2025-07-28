#!/usr/bin/env python3
"""
Sample commit-checker plugin: JSON Logger

This plugin demonstrates the plugin system by logging all commit events to a JSON file.
It shows how to hook into different events and process data.

Plugin Hooks Available:
- on_commit_check: Called when commits are checked
- on_til_add: Called when a TIL entry is added
- on_theme_change: Called when theme is changed
- on_level_up: Called when user levels up
- on_achievement_unlock: Called when achievement is unlocked
"""

import json
import os
from datetime import datetime
from pathlib import Path


# Plugin configuration
PLUGIN_NAME = "JSON Logger"
PLUGIN_VERSION = "1.0.0"
LOG_FILE = os.path.expanduser("~/.commit-checker/logs/commit-log.json")


def ensure_log_directory():
    """Ensure log directory exists"""
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)


def load_log_data():
    """Load existing log data"""
    ensure_log_directory()
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            return {"events": []}
    return {"events": []}


def save_log_data(data):
    """Save log data"""
    ensure_log_directory()
    try:
        with open(LOG_FILE, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    except Exception as e:
        print(f"Plugin error: Failed to save log data: {e}")


def log_event(event_type, data):
    """Log an event to the JSON file"""
    log_data = load_log_data()
    
    event = {
        "timestamp": datetime.now().isoformat(),
        "event_type": event_type,
        "data": data
    }
    
    log_data["events"].append(event)
    
    # Keep only last 1000 events to prevent file from growing too large
    if len(log_data["events"]) > 1000:
        log_data["events"] = log_data["events"][-1000:]
    
    save_log_data(log_data)


# Plugin Hook Functions
def on_commit_check(commit_data):
    """Called when commits are checked"""
    log_event("commit_check", {
        "repos_checked": len(commit_data.get("local_commits", [])),
        "total_commits_today": commit_data.get("total_commits", 0),
        "xp_gained": commit_data.get("xp_gained", 0),
        "current_streak": commit_data.get("current_streak", 0)
    })


def on_til_add(til_data):
    """Called when a TIL entry is added"""
    log_event("til_add", {
        "title": til_data.get("title", "Unknown"),
        "tags": til_data.get("tags", []),
        "type": til_data.get("type", "manual"),  # manual, template, diff-generated
        "template_used": til_data.get("template")
    })


def on_theme_change(theme_data):
    """Called when theme is changed"""
    log_event("theme_change", {
        "old_theme": theme_data.get("old_theme"),
        "new_theme": theme_data.get("new_theme")
    })


def on_level_up(level_data):
    """Called when user levels up"""
    log_event("level_up", {
        "old_level": level_data.get("old_level"),
        "new_level": level_data.get("new_level"),
        "total_xp": level_data.get("total_xp"),
        "level_title": level_data.get("level_title")
    })


def on_achievement_unlock(achievement_data):
    """Called when achievement is unlocked"""
    log_event("achievement_unlock", {
        "achievement_id": achievement_data.get("achievement_id"),
        "achievement_name": achievement_data.get("name"),
        "rarity": achievement_data.get("rarity"),
        "description": achievement_data.get("description")
    })


# Plugin utility functions
def get_log_stats():
    """Get statistics about logged events"""
    log_data = load_log_data()
    events = log_data.get("events", [])
    
    if not events:
        return "No events logged yet."
    
    # Count events by type
    event_counts = {}
    for event in events:
        event_type = event.get("event_type", "unknown")
        event_counts[event_type] = event_counts.get(event_type, 0) + 1
    
    # Get date range
    first_event = events[0].get("timestamp", "Unknown")
    last_event = events[-1].get("timestamp", "Unknown")
    
    stats = [
        f"📊 JSON Logger Statistics",
        f"Total events: {len(events)}",
        f"Date range: {first_event[:10]} to {last_event[:10]}",
        "",
        "Event types:"
    ]
    
    for event_type, count in sorted(event_counts.items()):
        stats.append(f"  {event_type}: {count}")
    
    return "\n".join(stats)


def export_log_csv(output_path=None):
    """Export log data to CSV format"""
    if not output_path:
        output_path = os.path.expanduser("~/commit-checker-log.csv")
    
    log_data = load_log_data()
    events = log_data.get("events", [])
    
    if not events:
        return False, "No events to export"
    
    try:
        import csv
        
        with open(output_path, 'w', newline='') as csvfile:
            fieldnames = ['timestamp', 'event_type', 'data']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for event in events:
                writer.writerow({
                    'timestamp': event.get('timestamp'),
                    'event_type': event.get('event_type'),
                    'data': json.dumps(event.get('data', {}))
                })
        
        return True, f"Log exported to {output_path}"
    
    except Exception as e:
        return False, f"Export failed: {e}"


# Plugin main function (called when plugin is loaded)
def main():
    """Main plugin function - called when plugin is loaded"""
    print(f"🔌 {PLUGIN_NAME} v{PLUGIN_VERSION} loaded")
    ensure_log_directory()


if __name__ == "__main__":
    # Allow plugin to be run standalone for testing
    main()
    print(get_log_stats())
