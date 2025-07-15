import requests
from datetime import datetime, timezone
import argparse

def get_today_push_events(username):
    url = f"https://api.github.com/users/{username}/events"
    headers = {"Accept": "application/vnd.github.v3+json"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        events = response.json()
    except requests.RequestException as e:
        print("❌ Failed to fetch events:", e)
        return

    today_str = datetime.now(timezone.utc).date().isoformat()
    push_events = [
        e for e in events
        if e["type"] == "PushEvent" and e["created_at"].startswith(today_str)
    ]

    if not push_events:
        print(f"😞 No public commits found for @{username} today ({today_str}).")
        return

    print(f"✅ Public commits for @{username} today ({today_str}):\n")
    for event in push_events:
        repo_name = event["repo"]["name"]
        commit_count = len(event["payload"]["commits"])
        print(f"📁 {repo_name} — {commit_count} commit(s)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check if you've committed to GitHub today.")
    parser.add_argument("username", help="Your GitHub username")
    args = parser.parse_args()

    get_today_push_events(args.username)
