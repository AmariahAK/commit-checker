#!/usr/bin/env python3
"""
Complete commit-checker removal script
Removes all traces of commit-checker from your system
"""

import os
import subprocess
import sys
import shutil
import glob
import platform
from pathlib import Path

def run_command(cmd, ignore_errors=True):
    """Run a command and optionally ignore errors"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0 or ignore_errors:
            return result.stdout.strip()
        return None
    except Exception:
        if not ignore_errors:
            raise
        return None

def safe_remove(path):
    """Safely remove a file or directory"""
    try:
        if os.path.exists(path):
            print(f"🗑️  Removing: {path}")
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            return True
    except Exception as e:
        print(f"⚠️  Could not remove {path}: {e}")
    return False

def main():
    print("🗑️  Complete commit-checker removal script")
    print("=" * 50)
    
    print("\nStep 1: Attempting pip uninstalls...")
    
    # Try various pip uninstall methods
    pip_commands = [
        "pip uninstall commit-checker -y",
        "pip3 uninstall commit-checker -y", 
        "python -m pip uninstall commit-checker -y",
        "python3 -m pip uninstall commit-checker -y",
        "pip uninstall commit-checker -y --break-system-packages",
        "pip3 uninstall commit-checker -y --break-system-packages",
        "python -m pip uninstall commit-checker -y --break-system-packages",
        "python3 -m pip uninstall commit-checker -y --break-system-packages"
    ]
    
    for cmd in pip_commands:
        print(f"📦 Trying: {cmd}")
        run_command(cmd, ignore_errors=True)
    
    print("\nStep 2: Removing binaries...")
    
    # Common binary locations
    binary_paths = [
        "/usr/local/bin/commit-checker",
        "/usr/bin/commit-checker",
        str(Path.home() / ".local/bin/commit-checker"),
        "/opt/homebrew/bin/commit-checker"
    ]
    
    for path in binary_paths:
        safe_remove(path)
    
    print("\nStep 3: Removing configuration...")
    
    # Configuration directories
    config_paths = [
        str(Path.home() / ".commit-checker"),
        str(Path.home() / ".commit-checker-standalone")
    ]
    
    for path in config_paths:
        safe_remove(path)
    
    print("\nStep 4: Removing Python packages...")
    
    # Find and remove Python packages
    python_base_paths = []
    
    # Get Python site-packages directories
    try:
        import site
        python_base_paths.extend(site.getsitepackages())
        python_base_paths.append(site.getusersitepackages())
    except:
        pass
    
    # Add common paths
    home = Path.home()
    system = platform.system().lower()
    
    if system == "darwin":  # macOS
        python_base_paths.extend([
            "/usr/local/lib/python*/site-packages",
            "/opt/homebrew/lib/python*/site-packages",
            str(home / ".local/lib/python*/site-packages"),
            "/Library/Python/*/site-packages"
        ])
    elif system == "linux":
        python_base_paths.extend([
            "/usr/lib/python*/site-packages",
            "/usr/local/lib/python*/site-packages", 
            str(home / ".local/lib/python*/site-packages")
        ])
    elif system == "windows":
        python_base_paths.extend([
            str(Path(sys.executable).parent / "Lib/site-packages"),
            str(home / "AppData/Roaming/Python/Python*/site-packages")
        ])
    
    # Remove commit_checker packages
    for base_path in python_base_paths:
        if "*" in base_path:
            # Handle wildcard patterns
            for expanded_path in glob.glob(base_path):
                pkg_path = os.path.join(expanded_path, "commit_checker")
                safe_remove(pkg_path)
                # Also remove .egg-info directories
                for egg_info in glob.glob(os.path.join(expanded_path, "commit_checker*.egg-info")):
                    safe_remove(egg_info)
        else:
            if os.path.exists(base_path):
                pkg_path = os.path.join(base_path, "commit_checker")
                safe_remove(pkg_path)
                # Also remove .egg-info directories
                for egg_info in glob.glob(os.path.join(base_path, "commit_checker*.egg-info")):
                    safe_remove(egg_info)
    
    print("\nStep 5: Cleaning shell startup files...")
    
    # Shell startup files
    shell_files = [
        home / ".bashrc",
        home / ".zshrc", 
        home / ".bash_profile",
        home / ".profile"
    ]
    
    for shell_file in shell_files:
        if shell_file.exists():
            try:
                with open(shell_file, 'r') as f:
                    lines = f.readlines()
                
                # Filter out commit-checker lines
                filtered_lines = [line for line in lines if 'commit-checker' not in line]
                
                if len(filtered_lines) != len(lines):
                    print(f"🗑️  Removing commit-checker from {shell_file}")
                    # Create backup
                    backup_file = f"{shell_file}.backup.commit-checker-removal"
                    shutil.copy2(shell_file, backup_file)
                    
                    # Write filtered content
                    with open(shell_file, 'w') as f:
                        f.writelines(filtered_lines)
                        
            except Exception as e:
                print(f"⚠️  Could not clean {shell_file}: {e}")
    
    print("\nStep 6: Final verification...")
    
    # Check if command still exists
    which_result = run_command("which commit-checker")
    if which_result:
        print(f"⚠️  commit-checker still found at: {which_result}")
        safe_remove(which_result)
    else:
        print("✅ commit-checker command no longer found")
    
    print("\n" + "=" * 50)
    print("✅ Complete removal finished!")
    print("\n🔄 To verify removal, try:")
    print("   commit-checker --version")
    print("   (should show 'command not found')")
    print("\n📦 To install the latest version (v0.4.2):")
    print("   curl -s https://raw.githubusercontent.com/AmariahAK/commit-checker/main/scripts/install-safe.sh | bash")
    print("\n💡 You may need to restart your terminal for changes to take effect")

if __name__ == "__main__":
    main()
