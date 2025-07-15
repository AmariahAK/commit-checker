import os
import json

CONFIG_PATH = os.path.expanduser("~/.commit-checker/config.json")

def config_exists():
    return os.path.exists(CONFIG_PATH)

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def save_config(data):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=4)

def prompt_config():
    print("🛠️  First-time setup: Let’s configure your commit-checker!\n")

    username = input("👤 GitHub username: ").strip()
    token = input("🔑 GitHub personal token (optional - hit Enter to skip): ").strip()
    local_path = input("📁 Local dev folder path (e.g. ~/Documents/Github): ").strip()

    config = {
        "github_username": username,
        "github_token": token if token else None,
        "local_path": os.path.expanduser(local_path)
    }

    save_config(config)
    print("\n✅ Config saved. You’re all set!")
    return config
