import os
import json
import sys
import importlib.util

# Handle imports for both standalone and package modes
try:
    from .path_detector import get_suggested_paths, get_best_default_path, auto_detect_dev_paths
except ImportError:
    # Standalone mode - load path_detector directly
    current_dir = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location("path_detector", os.path.join(current_dir, "path_detector.py"))
    path_detector = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(path_detector)
    get_suggested_paths = path_detector.get_suggested_paths
    get_best_default_path = path_detector.get_best_default_path
    auto_detect_dev_paths = path_detector.auto_detect_dev_paths

CONFIG_PATH = os.path.expanduser("~/.commit-checker/config.json")

def config_exists():
    return os.path.exists(CONFIG_PATH)

def load_config():
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
    
    # Handle backward compatibility
    if "local_path" in config and "local_paths" not in config:
        config["local_paths"] = [config["local_path"]]
    
    # Add missing new config fields with defaults
    if "repo_folder" not in config:
        config["repo_folder"] = config.get("local_paths", [None])[0]
    
    if "output" not in config:
        config["output"] = "emoji"
    
    if "til_path" not in config:
        config["til_path"] = None  # Will use default path
    
    # Save updated config if any changes were made
    save_config(config)
    
    return config

def save_config(data):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=4)

def prompt_config():
    print("🛠️  First-time setup: Let's configure your commit-checker!\n")

    username = input("👤 GitHub username: ").strip()
    token = input("🔑 GitHub personal token (optional - hit Enter to skip): ").strip()
    
    # Smart path detection
    print("\n📁 Setting up local development folder...")
    suggestions = get_suggested_paths()
    default_path = get_best_default_path()
    
    if suggestions:
        print("🔍 Found these potential development folders:")
        for i, suggestion in enumerate(suggestions[:5], 1):
            print(f"   {i}. {suggestion}")
        print(f"   Or enter a custom path")
        print(f"   (Default: {default_path})")
        
        choice = input("\n📂 Enter number (1-5), custom path, or press Enter for default: ").strip()
        
        if choice == "":
            local_path = default_path
        elif choice.isdigit() and 1 <= int(choice) <= len(suggestions):
            # Extract just the path from the suggestion
            local_path = suggestions[int(choice) - 1].split(':')[1].strip() if ':' in suggestions[int(choice) - 1] else suggestions[int(choice) - 1].split('(')[0].strip()
        else:
            local_path = choice
    else:
        local_path = input(f"📁 Local dev folder path (default: {default_path}): ").strip()
        if not local_path:
            local_path = default_path

    # Support multiple paths separated by commas
    if ',' in local_path:
        paths = [os.path.expanduser(p.strip()) for p in local_path.split(',')]
    else:
        paths = [os.path.expanduser(local_path)]

    # Ask about output mode
    print("\n🎨 Choose output style:")
    print("   1. Emoji mode (default - colorful with emojis)")
    print("   2. Plain mode (simple text only)")
    output_choice = input("📝 Enter 1 or 2 (default: 1): ").strip()
    output_mode = "plain" if output_choice == "2" else "emoji"
    
    # Ask about repo folder for scanning
    print(f"\n🔍 Set repo scanning folder (where to look for git repos):")
    print(f"   Default: {paths[0] if paths else default_path}")
    repo_folder = input("📁 Repo folder (or press Enter for default): ").strip()
    if not repo_folder:
        repo_folder = paths[0] if paths else default_path
    repo_folder = os.path.expanduser(repo_folder)

    config = {
        "github_username": username,
        "github_token": token if token else None,
        "local_paths": paths,
        "repo_folder": repo_folder,
        "output": output_mode,
        "til_path": None  # Use default path
    }

    save_config(config)
    print(f"\n✅ Config saved! Monitoring {len(paths)} path(s).")
    return config

def delete_config():
    """Delete the configuration file and directory"""
    if os.path.exists(CONFIG_PATH):
        os.remove(CONFIG_PATH)
        config_dir = os.path.dirname(CONFIG_PATH)
        if os.path.exists(config_dir) and not os.listdir(config_dir):
            os.rmdir(config_dir)
        print("🗑️  Configuration deleted successfully!")
        return True
    else:
        print("❌ No configuration found to delete.")
        return False

def get_auto_config():
    """Get config with auto-detected paths if no config exists"""
    if config_exists():
        return load_config()
    
    # Auto-detect without prompting
    detected_paths = auto_detect_dev_paths()
    
    if detected_paths:
        print(f"🔍 Auto-detected {len(detected_paths)} development folder(s)")
        for path in detected_paths:
            print(f"   📁 {path}")
        
        config = {
            "github_username": None,
            "github_token": None,
            "local_paths": detected_paths,
            "repo_folder": detected_paths[0] if detected_paths else None,
            "output": "emoji",
            "til_path": None  # Use default path
        }
        
        return config
    
    return None
