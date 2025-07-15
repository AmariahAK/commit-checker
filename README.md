# 🟢 commit-checker

Keep your GitHub streak green with a lightweight, cross-platform tool.  
Automatically checks your daily commits — both **public (GitHub)** and **local (git)** — with smart path detection 🧠⚙️

---

## ✨ Features

- ✅ **Smart auto-detection** of git repositories
- ✅ **Cross-platform** support (macOS, Linux, Windows)
- ✅ **Multiple development folders** monitoring
- ✅ **GitHub public & private** commits tracking
- ✅ **No pip installation issues** - works with any Python setup
- ✅ **One-line installation** with curl/bash
- ✅ **Auto-updates** files from GitHub
- ✅ **Complete uninstall** functionality

---

## 🚀 Quick Install (Recommended)

### **Standalone Version** (No pip issues!)
```bash
curl -s https://raw.githubusercontent.com/AmariahAK/commit-checker/main/scripts/install-standalone.sh | bash
```

### **Or Run Directly** (No installation)
```bash
curl -s https://raw.githubusercontent.com/AmariahAK/commit-checker/main/scripts/commit-checker-standalone.sh | bash
```

### **Traditional pip Install** (If you prefer)
```bash
curl -s https://raw.githubusercontent.com/AmariahAK/commit-checker/main/install.sh | bash
```

---

## 🔧 Smart Setup Experience

On first run, commit-checker intelligently detects your development setup:

```bash
🔍 Found these potential development folders:
   1. Current directory: /Users/you/project (git repo)
   2. /Users/you/Documents/GitHub (15 git repos found)
   3. /Users/you/Developer (8 git repos found)
   Or enter a custom path
   (Default: /Users/you/Documents/GitHub)

📂 Enter number (1-3), custom path, or press Enter for default:
```

---

## 🎛️ Usage

**Basic usage:**
```bash
commit-checker
```

**All available commands:**
- `commit-checker` - Check today's commits
- `commit-checker --setup` - Reconfigure settings
- `commit-checker --uninstall` - Remove completely
- `commit-checker --support` - Show support info
- `commit-checker --silent` - Minimal output
- `commit-checker --nocolor` - Disable emojis/colors

---

## 🌍 Cross-Platform Path Detection

**macOS**: `~/Documents/GitHub`, `~/Developer`, `~/Desktop/GitHub`  
**Linux**: `~/workspace`, `~/devel`, `/var/www`  
**Windows**: `~/source`, `C:\Projects`, `C:\xampp\htdocs`

---

## 🏗️ Project Structure

```
commit-checker/
├── 📄 LICENSE.md                 # MIT License
├── 📖 README.md                  # This file
├── 📦 setup.py                   # Python package setup (pip version)
├── 📋 requirements.txt           # Python dependencies
├── 🚀 install.sh                 # Traditional pip installation
├── scripts/                      # Standalone versions
│   ├── 🎯 install-standalone.sh  # Standalone installer
│   └── 🚀 commit-checker-standalone.sh  # Standalone script
└── commit_checker/               # Core Python modules
    ├── 🔧 __init__.py            # Package initialization
    ├── ✅ checker.py             # Commit checking logic
    ├── ⚙️ config.py              # Configuration management
    ├── 🔍 path_detector.py       # Smart path detection
    └── 🔄 updater.py             # Auto-update functionality
```

---

## 💖 Support This Project

If this tool helps you stay on track, show some love 💚

**Donate via PayPal:**  
📬 amariah.abish@gmail.com

---

## 👨🏽‍💻 Built By

**Amariah Kamau**  
📂 GitHub: [@AmariahAK](https://github.com/AmariahAK)  
🌐 Portfolio: https://portfolio-pied-five-61.vercel.app

---

## 📄 License

Licensed under the [MIT License](LICENSE.md).

---

## 🎉 Recent Updates

### v0.2.0 - Smart Detection & Standalone Support
- 🔍 **Smart auto-detection** of git repositories
- 🌍 **Enhanced cross-platform** support
- 📁 **Multiple path monitoring**
- 🚀 **Standalone bash version** (no pip issues!)
- 🛠️ **Improved setup experience**

### v0.1.0 - Initial Release
- ✅ Basic GitHub and local commit tracking
- 🎛️ CLI interface with multiple flags
- 🔄 Auto-update functionality
