import os
import subprocess
import sys
from .config import CONFIG_PATH

def remove_from_shell_startup():
    """Remove commit-checker from shell startup files"""
    shell_files = [
        os.path.expanduser("~/.bashrc"),
        os.path.expanduser("~/.zshrc"),
        os.path.expanduser("~/.profile")
    ]
    
    removed_count = 0
    for shell_file in shell_files:
        if os.path.exists(shell_file):
            try:
                with open(shell_file, 'r') as f:
                    lines = f.readlines()
                
                # Remove lines containing commit-checker
                original_count = len(lines)
                lines = [line for line in lines if 'commit-checker' not in line]
                
                if len(lines) < original_count:
                    with open(shell_file, 'w') as f:
                        f.writelines(lines)
                    removed_count += 1
                    print(f"🗑️  Removed auto-run from {shell_file}")
                    
            except Exception as e:
                print(f"⚠️  Could not modify {shell_file}: {e}")
    
    if removed_count == 0:
        print("ℹ️  No shell startup modifications found")
    
    return removed_count > 0

def remove_config():
    """Remove configuration files"""
    if os.path.exists(CONFIG_PATH):
        os.remove(CONFIG_PATH)
        config_dir = os.path.dirname(CONFIG_PATH)
        if os.path.exists(config_dir) and not os.listdir(config_dir):
            os.rmdir(config_dir)
        print("🗑️  Configuration files removed")
        return True
    else:
        print("ℹ️  No configuration files found")
        return False

def uninstall_package():
    """Remove the commit-checker package via pip"""
    try:
        print("🗑️  Uninstalling commit-checker package...")
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "commit-checker", "-y"])
        print("✅ Package uninstalled successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Could not uninstall package: {e}")
        return False

def full_uninstall():
    """Complete uninstall process"""
    print("🗑️  Starting complete uninstall of commit-checker...\n")
    
    # Step 1: Remove from shell startup
    print("1️⃣  Removing from shell startup files...")
    remove_from_shell_startup()
    
    # Step 2: Remove configuration
    print("\n2️⃣  Removing configuration files...")
    remove_config()
    
    # Step 3: Uninstall package
    print("\n3️⃣  Uninstalling Python package...")
    package_removed = uninstall_package()
    
    if package_removed:
        print("\n✅ commit-checker has been completely removed from your system!")
        print("💡 You may need to restart your terminal or run 'source ~/.bashrc' (or ~/.zshrc)")
        return True
    else:
        print("\n⚠️  Uninstall partially completed. You may need to manually remove the package.")
        return False
