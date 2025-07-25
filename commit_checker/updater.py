import requests
from packaging import version
import subprocess
import os
import sys
import json
import time

LOCAL_VERSION = "0.5.0"
REPO = "AmariahAK/commit-checker"
UPDATE_MARKER_FILE = os.path.expanduser("~/.commit-checker/pending_update")
VERSION_CACHE_FILE = os.path.expanduser("~/.commit-checker/version_cache.json")
UPDATE_CHECK_INTERVAL = 86400  # 24 hours in seconds

def get_installed_version():
    """Get the actual installed version of commit-checker"""
    try:
        # Try to get version from installed package
        import pkg_resources
        try:
            installed_version = pkg_resources.get_distribution("commit-checker").version
            return installed_version
        except pkg_resources.DistributionNotFound:
            pass
    except ImportError:
        pass
    
    # Fallback to LOCAL_VERSION constant
    return LOCAL_VERSION

def get_version_cache():
    """Get cached version check data"""
    if not os.path.exists(VERSION_CACHE_FILE):
        return None
    
    try:
        with open(VERSION_CACHE_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return None

def save_version_cache(data):
    """Save version check data to cache"""
    try:
        os.makedirs(os.path.dirname(VERSION_CACHE_FILE), exist_ok=True)
        with open(VERSION_CACHE_FILE, 'w') as f:
            json.dump(data, f)
    except Exception:
        pass

def should_check_for_updates():
    """Check if we should perform an update check based on interval"""
    cache = get_version_cache()
    if not cache:
        return True
    
    last_check = cache.get('last_check_time', 0)
    return (time.time() - last_check) > UPDATE_CHECK_INTERVAL

def get_latest_version():
    """Get the latest version from GitHub releases"""
    try:
        response = requests.get(f"https://api.github.com/repos/{REPO}/releases/latest")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        latest_version = response.json()["tag_name"].lstrip("v")
        
        # Cache the result
        cache_data = {
            'latest_version': latest_version,
            'last_check_time': time.time(),
            'current_version': get_installed_version()
        }
        save_version_cache(cache_data)
        
        return latest_version
    except Exception:
        # Try to use cached version if network fails
        cache = get_version_cache()
        if cache:
            return cache.get('latest_version')
        return None

def mark_pending_update(version_str):
    """Mark that an update is pending for next startup"""
    os.makedirs(os.path.dirname(UPDATE_MARKER_FILE), exist_ok=True)
    with open(UPDATE_MARKER_FILE, "w") as f:
        f.write(version_str)

def get_pending_update():
    """Check if there's a pending update"""
    if os.path.exists(UPDATE_MARKER_FILE):
        try:
            with open(UPDATE_MARKER_FILE, "r") as f:
                return f.read().strip()
        except Exception:
            pass
    return None

def clear_pending_update():
    """Clear the pending update marker"""
    if os.path.exists(UPDATE_MARKER_FILE):
        try:
            os.remove(UPDATE_MARKER_FILE)
        except Exception:
            pass

def perform_update(target_version):
    """Perform the actual update"""
    try:
        print(f"⬆️  Updating commit-checker to v{target_version}...")
        
        # Try different update methods
        update_commands = [
            f"pip install --upgrade git+https://github.com/{REPO}.git@v{target_version}",
            f"pip install --upgrade git+https://github.com/{REPO}.git@v{target_version} --break-system-packages",
            f"pip install --upgrade git+https://github.com/{REPO}.git@v{target_version} --user"
        ]
        
        for cmd in update_commands:
            try:
                print(f"🔄 Running: {cmd}")
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ Successfully updated to v{target_version}!")
                    return True
            except Exception:
                continue
                
        print("❌ Update failed. Please try manually:")
        print(f"   pip install --upgrade git+https://github.com/{REPO}.git@v{target_version}")
        return False
        
    except Exception as e:
        print(f"❌ Update failed: {e}")
        return False

def check_pending_update_on_startup():
    """Check for pending updates on startup and install if requested"""
    pending_version = get_pending_update()
    if pending_version:
        print(f"🔔 Installing pending update to v{pending_version}...")
        if perform_update(pending_version):
            clear_pending_update()
            print("🎉 Update completed! Please restart commit-checker to use the new version.")
            sys.exit(0)
        else:
            clear_pending_update()  # Clear failed update

def check_for_updates(force_check=False):
    """Check for updates with user interaction"""
    try:
        # Skip update check if not forced and within interval
        if not force_check and not should_check_for_updates():
            return False
            
        current_version = get_installed_version()
        latest = get_latest_version()
        
        if not latest:
            if force_check:
                print("⚠️  Could not check for updates (no releases found)")
            return False
            
        if version.parse(latest) > version.parse(current_version):
            print(f"\n🔔 New version available: v{latest} (you have v{current_version})")
            
            # Show changelog if available
            try:
                changelog_url = f"https://api.github.com/repos/{REPO}/releases/latest"
                response = requests.get(changelog_url)
                if response.status_code == 200:
                    release_info = response.json()
                    if release_info.get("body"):
                        # Show first few lines of release notes
                        body_lines = release_info["body"].split('\n')[:5]
                        print("📋 What's new:")
                        for line in body_lines:
                            if line.strip():
                                print(f"   {line.strip()}")
                        print("   ...")
            except Exception:
                pass
            
            print("\n📦 Update options:")
            print("   1. Install now")
            print("   2. Install on next terminal restart")
            print("   3. Skip this update")
            
            choice = input("❓ Choose option (1/2/3) [1]: ").strip()
            
            if choice in ["", "1"]:
                success = perform_update(latest)
                if success:
                    # Update cache to reflect new version
                    cache_data = {
                        'latest_version': latest,
                        'last_check_time': time.time(),
                        'current_version': latest
                    }
                    save_version_cache(cache_data)
                return success
            elif choice == "2":
                mark_pending_update(latest)
                print(f"📅 Update to v{latest} scheduled for next terminal restart")
                return True
            else:
                print("⏭️  Update skipped")
                return False
        else:
            if force_check:
                print(f"✅ You're running the latest version (v{current_version})")
            return False
            
    except Exception as e:
        if force_check:
            print(f"⚠️  Update check failed: {e}")
    return False

def manual_update_check():
    """Manual update check triggered by --update flag"""
    print("🔍 Checking for updates...")
    return check_for_updates(force_check=True)
