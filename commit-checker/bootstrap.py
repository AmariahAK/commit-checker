import subprocess
import sys

def ensure_package(package):
    try:
        __import__(package)
    except ImportError:
        print(f"📦 Installing missing dependency: {package}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def bootstrap():
    for pkg in ["requests", "colorama"]:
        ensure_package(pkg)
