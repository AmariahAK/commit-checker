# 🟢 commit-checker

Keep your GitHub streak green with a lightweight, cross-platform tool.  
Automatically checks your daily commits — both **public (GitHub)** and **local (git)** — with smart path detection 🧠⚙️

---

## ✨ Features

### 🔧 Core Functionality

- ✅ **Smart auto-detection** of git repositories
- ✅ **Cross-platform** support (macOS, Linux, Windows)
- ✅ **Multiple development folders** monitoring
- ✅ **GitHub public & private** commits tracking
- ✅ **Repository scanning** and commit analysis
- ✅ **Most active repo detection** (daily, weekly, monthly)

### 🧙‍♂️ Interactive Setup & Configuration

- ✅ **Interactive Setup Wizard** (`--init`) with guided configuration
- ✅ **Smart Path Detection** - automatically finds your dev folders
- ✅ **Theme Selection** - tech, kawaii, anime, horror, or default themes
- ✅ **Custom Commit Rules** - regex patterns for commit message validation
- ✅ **Pre-commit Hook Installation** - optional Git hook setup

### 📊 Statistics & Analytics

- ✅ **ASCII Commit Charts** (`--stats`) showing 30-day trends
- ✅ **Visual Repository Analysis** with Unicode bar charts (▁▂▃▄▅▆▇█)
- ✅ **Multi-Repository Stats** across all local repositories
- ✅ **Recent Activity Summary** with detailed commit breakdowns

### 📚 Enhanced TIL (Today I Learned) System

- ✅ **Tag Support** - organize entries with `#tags`
- ✅ **Smart Filtering** - filter by tag with `--filter-tag`
- ✅ **Export Functionality** - export to Markdown or JSON
- ✅ **Enhanced Statistics** - tag counting and comprehensive analytics
- ✅ **Integrated Editor Support** for TIL log management

### 🔍 System Diagnostics & Health

- ✅ **System Diagnostics** (`--diagnose`) for troubleshooting
- ✅ **Installation Method Detection** (pip, pipx, standalone)
- ✅ **Dependency Verification** and environment analysis
- ✅ **Configuration Validation** with automatic migration

### 🛠️ Installation & Updates

- ✅ **No pip installation issues** - works with any Python setup
- ✅ **One-line installation** with curl/bash
- ✅ **Intelligent Update System** with version caching
- ✅ **PEP 668 Compliance** - handles externally managed environments
- ✅ **Complete uninstall** functionality with smart cleanup

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

**Setup & Configuration:**
- `commit-checker --init` - Interactive setup wizard (recommended for first-time users)
- `commit-checker --setup` - Quick reconfigure settings
- `commit-checker --diagnose` - Run system diagnostics

**Core functionality:**
- `commit-checker` - Check today's commits
- `commit-checker --scan` - Scan repo folder for all git repositories  
- `commit-checker --repos-summary` - Show full summary of all repos
- `commit-checker --most-active` - Show most active repository today
- `commit-checker --most-active --week` - Show most active repo this week
- `commit-checker --most-active --month` - Show most active repo this month
- `commit-checker --stats` - Show ASCII commit trend charts (30 days)

**Enhanced TIL (Today I Learned) commands:**
- `commit-checker til "Your learning today"` - Add a TIL entry
- `commit-checker til "Python async" --tag python` - Add TIL entry with tag
- `commit-checker --view-til` - View your complete TIL log
- `commit-checker --view-til --filter-tag python` - View TIL entries by tag
- `commit-checker --edit-til` - Edit TIL log in your default editor
- `commit-checker --export md` - Export TIL to Markdown file
- `commit-checker --export json` - Export TIL to JSON file
- `commit-checker --reset-til` - Clear all TIL entries (with confirmation)
- `commit-checker til "Entry" --no-date` - Add entry without date header

**System commands:**
- `commit-checker --update` - Manually check for updates
- `commit-checker --uninstall` - Remove completely (with PEP 668 support)
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

## ☕ Support

If this tool helps you stay consistent, focused, or productive — consider supporting development!

[![Buy Me A Coffee](https://img.shields.io/badge/☕-Support%20me%20on%20Buy%20Me%20A%20Coffee-orange)](https://www.buymeacoffee.com/amariahak)

Or visit: https://buymeacoffee.com/amariahak

---

## 👨🏽‍💻 Built By

**Amariah Kamau**  
📂 GitHub: [@AmariahAK](https://github.com/AmariahAK)  
🌐 Portfolio: https://portfolio-pied-five-61.vercel.app

---

## 📄 License

Licensed under the [MIT License](LICENSE.md).

---

## 📝 TIL (Today I Learned) Feature

Track your daily learnings with commit-checker's built-in TIL functionality:

### Basic Usage
```bash
# Add a learning entry
commit-checker til "Learned how to use async/await in Python"

# View your TIL log
commit-checker --view-til

# Edit in your preferred editor
commit-checker --edit-til
```

### Example TIL Log
```markdown
# Today I Learned

## July 22, 2025
- Learned how to use async/await in Python
- Discovered that Git hooks can automate code quality checks
- Found out about the --no-ff flag in Git merge

## July 21, 2025
- Learned about CSS Grid layout properties
- Discovered Docker multi-stage builds for smaller images
```

### Advanced Options
```bash
# Add entry without date grouping
commit-checker til "Quick tip" --no-date

# Reset all entries (with confirmation)
commit-checker --reset-til
```

**TIL Storage:** Entries are saved to `~/.commit-checker/til.md` and persist between sessions unless manually deleted.

---

## 🔥 New Features in Action

### Interactive Setup Wizard
```bash
$ commit-checker --init
🧙‍♂️ Welcome to commit-checker Interactive Setup Wizard!
🌐 GitHub Configuration
   👤 GitHub username: AmariahAK
📁 Development Folder Configuration
   🔍 Found these potential development folders:
      1. /Users/you/Documents/GitHub (15 git repos found)
      2. /Users/you/Developer (8 git repos found)
🎨 Output Style Configuration
   1. 🎉 Emoji mode (colorful with emojis)
   2. 📝 Plain mode (simple text only)
📚 TIL Configuration...
🎉 Configuration saved!
```

### ASCII Commit Statistics
```bash
$ commit-checker --stats
📊 Commit Statistics (Last 30 Days)
==================================================

📁 commit-checker
   Total commits: 18
   Trend: ▁▂▃█▇▆▅▃▂▁▃▄▅▇█▇▅▃▂▁▂▄▅▆▇█▇▅▃▂▁
   Recent: 2025-07-23: 2, 2025-07-24: 3, 2025-07-25: 5

📁 my-website
   Total commits: 12
   Trend: ▁▁▂▃▄▅▆▇█▇▆▅▄▃▂▁▁▂▃▄▅▆▇█▇▆▅▄▃▂▁
   Recent: 2025-07-23: 1, 2025-07-24: 2, 2025-07-25: 4
```

### Enhanced TIL with Tags
```bash
$ commit-checker til "Learned about async/await in Python" --tag python
✅ TIL entry added (tagged: python)

$ commit-checker --view-til --filter-tag python
# Today I Learned

## July 25, 2025
- Learned about async/await in Python `#python`
- Python decorators can modify function behavior `#python`

$ commit-checker --export json
📊 TIL exported to ~/til_export_20250725_143022.json
```

### System Diagnostics
```bash
$ commit-checker --diagnose
🔍 System Diagnostics
==============================
🐍 Python version: 3.11.5
📦 Git: git version 2.39.0
📦 Package: Installed via pip (v0.5.0)
⚙️  Config: Found at ~/.commit-checker/config.json
   GitHub user: AmariahAK
   Local paths: 2 configured
   Output mode: emoji
📚 Dependencies:
   ✅ requests: Available
   ✅ packaging: Available
   ✅ colorama: Available
🐍 Environment: Virtual environment
📦 pipx: Available but commit-checker not installed via pipx
✅ Diagnostics complete!
```

### Repository Scanning
```bash
$ commit-checker --scan
🔍 Scanning /Users/you/Documents/GitHub for git repositories...

📁 Scanned 6 repos:

commit-checker → ✅ 2 today | 🧮 41 total | 🕒 Today
blog-api → ❌ 0 today | 🧮 89 total | 🕒 Jul 17
my-website → ✅ 1 today | 🧮 156 total | 🕒 Today
```

---

## 🎉 Recent Updates

### v0.5.0 - Interactive Wizards & Enhanced Analytics (Latest)
- 🧙‍♂️ **Interactive Setup Wizard** - Complete guided configuration with `--init`
- 📊 **ASCII Statistics** - Visual commit trends and repository analytics
- 📚 **Enhanced TIL System** - Tags, filtering, and export functionality
- 🔍 **System Diagnostics** - Comprehensive health checks and troubleshooting
- 🔧 **Critical Bug Fixes** - Fixed update loops and PEP 668 uninstall issues

### v0.4.3 - TIL (Today I Learned) Feature
- 📝 **New TIL Command** - Log daily learnings with `commit-checker til "message"`
- 📁 **Local Storage** - Entries saved to `~/.commit-checker/til.md` with smart date organization
- 🖊️ **Editor Integration** - `--edit-til` opens your TIL log in default editor
- 👀 **View & Reset** - `--view-til` and `--reset-til` for easy management
- 🔧 **Customizable** - Configure TIL path via config.json

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
