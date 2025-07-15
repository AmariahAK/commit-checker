import requests
from packaging import version
import subprocess

LOCAL_VERSION = "0.1.0"
REPO = "AmariahAK/commit-checker"

def check_for_updates():
    try:
        response = requests.get(f"https://api.github.com/repos/{REPO}/releases/latest")
        response.raise_for_status()
        latest = response.json()["tag_name"].lstrip("v")
        
        if version.parse(latest) > version.parse(LOCAL_VERSION):
            print(f"\n🔔 New version available: v{latest} (you have v{LOCAL_VERSION})")
            choice = input("❓ Update now? [Y/n]: ").lower()
            if choice in ["", "y", "yes"]:
                update_command = f"pip install --upgrade git+https://github.com/{REPO}.git"
                print(f"⬆️ Running: {update_command}")
                subprocess.run(update_command, shell=True)
                return True
    except Exception as e:
        print(f"⚠️  Update check failed: {e}")
    return False
