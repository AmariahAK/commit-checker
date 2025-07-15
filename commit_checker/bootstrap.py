import subprocess
import sys

def ensure_package(package):
    try:
        __import__(package)
    except ImportError:
        print(f"📦 Installing missing dependency: {package}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except subprocess.CalledProcessError:
            # Try with --break-system-packages for externally managed environments
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--break-system-packages"])
            except subprocess.CalledProcessError:
                # Try with --user flag as last resort
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--user"])
                except subprocess.CalledProcessError:
                    print(f"⚠️  Could not install {package}. Please install manually: pip install {package}")
                    return False
    return True

def bootstrap():
    for pkg in ["requests", "colorama"]:
        ensure_package(pkg)
