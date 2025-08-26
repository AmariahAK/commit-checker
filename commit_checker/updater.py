import requests
from packaging import version
import subprocess
import os
import sys
import json
import time

LOCAL_VERSION = "0.6.2"
REPO = "AmariahAK/commit-checker"
UPDATE_MARKER_FILE = os.path.expanduser("~/.commit-checker/pending_update")
VERSION_CACHE_FILE = os.path.expanduser("~/.commit-checker/version_cache.json")
UPDATE_CHECK_INTERVAL = 86400  # 24 hours in seconds

def detect_installation_type():
    """Detect how commit-checker is installed"""
    # Check if running as standalone
    if os.path.exists(os.path.expanduser("~/.commit-checker-standalone")):
        return "standalone"
    
    # Check for pip installation
    try:
        import pkg_resources
        try:
            pkg_resources.get_distribution("commit-checker")
            return "pip"
        except pkg_resources.DistributionNotFound:
            pass
    except ImportError:
        pass
    
    return "unknown"


def get_installed_version():
    """Get the actual installed version of commit-checker"""
    # For standalone, always use LOCAL_VERSION
    if detect_installation_type() == "standalone":
        return LOCAL_VERSION
    
    try:
        # Try to get version from installed package (pip installations)
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
        installation_type = detect_installation_type()
        print(f"⬆️  Updating commit-checker to v{target_version}...")
        
        if installation_type == "standalone":
            return update_standalone(target_version)
        else:
            return update_pip_installation(target_version)
        
    except Exception as e:
        print(f"❌ Update failed: {e}")
        return False


def update_standalone(target_version):
    """Update standalone installation"""
    try:
        print("🔄 Updating standalone installation...")
        
        # Download the latest standalone script
        standalone_url = f"https://raw.githubusercontent.com/{REPO}/main/scripts/commit-checker-standalone.sh"
        
        import urllib.request
        binary_path = os.path.expanduser("~/.local/bin/commit-checker")
        temp_path = binary_path + ".tmp"
        
        print(f"📥 Downloading latest standalone script...")
        urllib.request.urlretrieve(standalone_url, temp_path)
        
        # Make it executable and replace old version
        import stat
        os.chmod(temp_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
        
        if os.path.exists(binary_path):
            os.remove(binary_path)
        os.rename(temp_path, binary_path)
        
        print(f"✅ Successfully updated standalone installation!")
        print("🔄 The update will take effect on next run.")
        return True
        
    except Exception as e:
        print(f"❌ Standalone update failed: {e}")
        print("💡 Try reinstalling with:")
        print("   curl -s https://raw.githubusercontent.com/AmariahAK/commit-checker/main/scripts/install-standalone.sh | bash")
        return False


def update_pip_installation(target_version):
    """Update pip installation"""
    try:
        print("🔄 Updating pip installation...")
        
        # Note: For pip installations, we update to main branch since tags might not exist yet
        update_commands = [
            f"pip install --upgrade git+https://github.com/{REPO}.git",
            f"pip install --upgrade git+https://github.com/{REPO}.git --break-system-packages",  
            f"pip install --upgrade git+https://github.com/{REPO}.git --user"
        ]
        
        for cmd in update_commands:
            try:
                print(f"🔄 Running: {cmd}")
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ Successfully updated to latest version!")
                    return True
            except Exception:
                continue
                
        print("❌ Update failed. Please try manually:")
        print(f"   pip install --upgrade git+https://github.com/{REPO}.git")
        return False
        
    except Exception as e:
        print(f"❌ Pip update failed: {e}")
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
        installation_type = detect_installation_type()
        
        if not latest:
            if force_check:
                print("⚠️  Could not check for updates (no releases found)")
            return False
            
        if version.parse(latest) > version.parse(current_version):
            print(f"\n🔔 New version available: v{latest} (you have v{current_version})")
            
            # Show installation type info
            if installation_type == "standalone":
                print(f"📦 Installation: Standalone (curl/bash)")
            elif installation_type == "pip":
                print(f"📦 Installation: pip package")
            
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
            
            # Show VS Code extension teaser for v0.7+
            if version.parse(latest) >= version.parse("0.7.0"):
                print("\n🎉 Coming in v0.7: VS Code Extension!")
                print("   📈 Dashboard panel in VS Code")
                print("   🔄 Auto TIL sync from editor")
                print("   🏆 Achievement notifications")
            
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
                install_msg = f" ({installation_type} installation)" if installation_type != "unknown" else ""
                print(f"✅ You're running the latest version (v{current_version}){install_msg}")
                
                # Show upcoming VS Code extension info
                print("\n💡 Looking forward to v0.7:")
                print("   🔮 VS Code Extension with dashboard panel")
                print("   📊 Real-time stats in your editor")
                print("   🚀 Seamless TIL integration")
            return False
            
    except Exception as e:
        if force_check:
            print(f"⚠️  Update check failed: {e}")
    return False

def manual_update_check():
    """Manual update check triggered by --update flag"""
    print("🔍 Checking for updates...")
    return check_for_updates(force_check=True)
