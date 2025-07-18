# 🟢 commit-checker

Keep your GitHub streak green with a lightweight, cross-platform tool.  
Automatically checks your daily commits — both **public (GitHub)** and **local (git)** — with smart path detection 🧠⚙️

---

## ✨ Features

- ✅ **Smart auto-detection** of git repositories
- ✅ **Cross-platform** support (macOS, Linux, Windows)
- ✅ **Multiple development folders** monitoring
- ✅ **GitHub public & private** commits tracking
- ✅ **Repository scanning** and commit analysis
- ✅ **Most active repo detection** (daily, weekly, monthly)
- ✅ **Configurable output modes** (emoji or plain text)
- ✅ **Complete repo summaries** with commit stats
- ✅ **No pip installation issues** - works with any Python setup
- ✅ **One-line installation** with curl/bash
- ✅ **Auto-updates** files from GitHub
- ✅ **Complete uninstall** functionality

---

## 🚀 Quick Install (Recommended)

### **Method 1: Safe Installation** (Recommended - avoids encoding issues)
```bash
curl -s https://raw.githubusercontent.com/AmariahAK/commit-checker/main/scripts/install-safe.sh | bash
```

### **Method 2: Manual Download** (Most reliable)
```bash
curl -s https://raw.githubusercontent.com/AmariahAK/commit-checker/main/scripts/install-standalone.sh -o /tmp/install.sh
chmod +x /tmp/install.sh
/tmp/install.sh
```

### **Method 3: Direct Pipe** (May have encoding issues on some systems)
```bash
curl -s https://raw.githubusercontent.com/AmariahAK/commit-checker/main/scripts/install-standalone.sh | bash
```

### **Method 4: Run Without Installation**
```bash
curl -s https://raw.githubusercontent.com/AmariahAK/commit-checker/main/scripts/commit-checker-standalone.sh -o /tmp/commit-checker.sh
chmod +x /tmp/commit-checker.sh
/tmp/commit-checker.sh
```

### **Method 5: Traditional pip Install**
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
- `commit-checker --scan` - Scan repo folder for all git repositories  
- `commit-checker --repos-summary` - Show full summary of all repos
- `commit-checker --most-active` - Show most active repository today
- `commit-checker --most-active --week` - Show most active repo this week
- `commit-checker --most-active --month` - Show most active repo this month
- `commit-checker --uninstall` - Remove completely
- `commit-checker --uninstall --force` - Remove without confirmation
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

## 🔥 New Features in Action

### Repository Scanning
```bash
$ commit-checker --scan
🔍 Scanning /Users/you/Documents/GitHub for git repositories...

📁 Scanned 6 repos:

commit-checker → ✅ 2 today | 🧮 41 total | 🕒 Today
blog-api → ❌ 0 today | 🧮 89 total | 🕒 Jul 17
my-website → ✅ 1 today | 🧮 156 total | 🕒 Today
```

### Most Active Repository
```bash
$ commit-checker --most-active --week
🔥 Most active repo this week:
📁 my-website → 12 commits
📅 Last activity: Today
```

### Repository Summary
```bash
$ commit-checker --repos-summary
🧾 Repo Summary:
📁 commit-checker → ✅ 2 today | 🧮 41 total | 🕒 Today
📁 my-website → ✅ 4 today | 🧮 163 total | 🕒 Today
📁 old-project → ❌ 0 today | 🧮 12 total | 🕒 Jul 10
```

---

## 🎉 Recent Updates

### v0.4.2 - Enhanced Update System
- 🔄 **Intelligent Update Scheduling** - Install updates now or on next terminal restart
- 📋 **Release Notes Preview** - See what's new before updating
- 🔧 **Robust Update Methods** - Multiple fallback installation approaches
- 📅 **Pending Update Management** - Automatic installation of scheduled updates

### v0.4.1 - Advanced Repository Analytics
- 🔍 **Repository scanning** with `--scan` flag
- 📊 **Complete repo summaries** with commit statistics  
- 🔥 **Most active repo detection** (daily, weekly, monthly)
- 🎨 **Configurable output modes** (emoji or plain text)
- 🗑️ **Enhanced uninstall** with `--force` option
- ⚙️ **Persistent configuration** with repo folder settings

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
