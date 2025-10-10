import subprocess
import sys
import warnings

# Suppress urllib3 OpenSSL warnings
warnings.filterwarnings('ignore', message='.*urllib3.*OpenSSL.*')

def ensure_package(package):
    try:
        __import__(package)
        return True
    except ImportError:
        print(f"📦 Installing missing dependency: {package}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            return True
        except subprocess.CalledProcessError:
            # Try with --break-system-packages for externally managed environments
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--break-system-packages"])
                return True
            except subprocess.CalledProcessError:
                # Try with --user flag as last resort
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--user"])
                    return True
                except subprocess.CalledProcessError:
                    print(f"⚠️  Could not install {package}. Please install manually: pip install {package}")
                    return False

def bootstrap():
    for pkg in ["requests", "colorama", "packaging"]:
        ensure_package(pkg)
