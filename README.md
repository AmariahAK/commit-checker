# 🟢 commit-checker

Keep your GitHub streak green with a lightweight, cross-platform tool.  
Automatically checks your daily commits — both **public (GitHub)** and **local (git)** — with smart path detection 🧠⚙️

---

## ✨ Features

### 🚀 **NEW: Performance & Stability (v0.8.0)**

- ✅ **Optimized Git Operations** - Faster repository scanning and commit analysis
- ✅ **Reduced Memory Footprint** - More efficient resource usage
- ✅ **Improved Error Handling** - More robust and user-friendly error messages
- ✅ **Enhanced Cross-Platform Compatibility** - Better support for various shell environments
- ✅ **Refactored Core Logic** - Cleaner, more maintainable codebase

### 🧠 **NEW: Smart Profile System (v0.7.0)**

- ✅ **AI-like Personalization** - Learns your coding patterns without ML dependencies
- ✅ **Commit Message Coaching** (`--coach`) - Suggests improvements based on your style
- ✅ **Tech Stack Detection** - Auto-detects Python, JS/React, Rust, Java, etc.
- ✅ **Project Structure Analysis** - Suggests tests, documentation updates
- ✅ **Stack-aware Suggestions** - Django migrations, npm installs, cargo checks
- ✅ **Personal Insights** (`--insights`) - Analyze your coding habits and trends
- ✅ **Non-disruptive** - Suggestions only, never blocks your workflow
- ✅ **Sound Notifications** - Audio feedback for completion and suggestions

### 🎮 **Gamification & Developer Progress (v0.6.0)**

- ✅ **Achievement System** - Unlock badges with ASCII art (Common to Mythic rarity)
- ✅ **AI-powered commits** (`--suggest`) - Optional ML-based suggestions (DialoGPT, DistilBERT)
- ✅ **GitHub streak tracker** - Never miss a day with automated checks
- ✅ **Wisdom Drop Integration** - Daily coding wisdom from AmariahAK/wisdom-drop

### 📱 **NEW: VS Code Extension (v0.8.0)**

- ✅ **Status Bar Widget** - Shows streak, daily commits, and level at a glance
- ✅ **Interactive Dashboard** - Beautiful webview with XP progress and achievements
- ✅ **TIL Integration** - Add and search TIL entries from the editor
- ✅ **Achievements Gallery** - View unlocked badges within VS Code
- ✅ **Local & Secure** - Uses existing CLI installation, no separate login
- ✅ **Auto-refresh** - Configurable stats updates (default: 5 minutes)

### 💡 **Enhanced Wisdom Drop (v0.8.0)**

- ✅ **Category Display** - Shows wisdom category (Developer, Samurai, Faith, etc.)
- ✅ **Date Information** - Displays the specific date of each quote
- ✅ **Daily Refresh** - Automatically updates quotes daily
- ✅ **Smart Caching** - Efficient fetching with commit-based invalidation
- ✅ **Example**: `💡 [Samurai Discipline / Modern Focus] Wisdom of the day (November 21 2025): "A samurai does not wait for the perfect wind..." — Inspired by the Way of the Samurai`
- ✅ **XP & Level System** - Earn XP from commits, progress through 10 levels
- ✅ **Streak Tracking** - Daily commit streaks with automatic achievement unlocking
- ✅ **Visual Progress** - Unicode progress bars and level-up celebrations
- ✅ **Smart XP Calculation** - Based on lines changed, deletions, and project weights
- ✅ **Configurable Weights** - Set different XP multipliers per project

### 📊 **NEW: Advanced Analytics & Visualizations (v0.6.0)**

- ✅ **ASCII Commit Heatmap** - GitHub-style activity visualization (365 days)
- ✅ **Language Breakdown** - Analyze coding languages across repositories
- ✅ **SVG Export** - Export heatmaps for sharing and documentation
- ✅ **Dynamic Mood System** - Smart status messages based on activity
- ✅ **Visual Charts** - Unicode bar charts and activity indicators

### 📚 **NEW: TIL Vault System (v0.6.0)**

- ✅ **Template System** - 5 built-in templates (bugfix, feature, concept, tool, algorithm)
- ✅ **Individual Files** - Each TIL entry as separate markdown file
- ✅ **Fuzzy Search** - Search entries with highlighted matches and scoring
- ✅ **Auto-generation** - Generate TIL entries from git commit diffs
- ✅ **Tag Organization** - Automatic tag extraction and filtering
- ✅ **Vault Management** - Comprehensive statistics and organization

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

### 📊 Enhanced Statistics & Repository Analysis

- ✅ **ASCII Commit Charts** (`--stats`) showing 30-day trends
- ✅ **Visual Repository Analysis** with Unicode bar charts (▁▂▃▄▅▆▇█)
- ✅ **Multi-Repository Stats** across all local repositories
- ✅ **Recent Activity Summary** with detailed commit breakdowns
- ✅ **Repository Scanning** (`--scan`) with commit analysis

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

> **v0.6.1 Update**: If you're experiencing uninstall issues or missing commands from v0.6.0, the latest version fixes all known issues including complete cleanup and standalone feature parity.

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

**🧠 Smart Profile System (v0.7.0):**
- `commit-checker --build-profile` - Build/rebuild your personalized coding profile
- `commit-checker --coach "fix user auth"` - Get commit message coaching suggestions
- `commit-checker --feedback good/bad` - Give feedback on coaching suggestions to tune preferences
- `commit-checker --insights` - Show personalized coding insights and habits
- `commit-checker --no-profile` - Skip profile-based suggestions for this run

**Core functionality:**
- `commit-checker` - Check today's commits with gamification
- `commit-checker --scan` - Scan repo folder for all git repositories  
- `commit-checker --repos-summary` - Show full summary of all repos
- `commit-checker --most-active` - Show most active repository today
- `commit-checker --most-active --week` - Show most active repo this week
- `commit-checker --most-active --month` - Show most active repo this month
- `commit-checker --stats` - Show ASCII commit trend charts (30 days)

**🎮 Gamification & Progress:**
- `commit-checker --achievements` - Display achievement gallery with ASCII art
- `commit-checker --xp` - Show current XP, level, and progress to next level
- Automatic streak tracking and achievement unlocking
- XP earned from commits based on lines changed and project weights

**📊 Analytics & Visualizations:**
- `commit-checker --heatmap` - Display ASCII commit heatmap (365 days)
- `commit-checker --heatmap --days 90` - Custom timeframe heatmap
- `commit-checker --heatmap-export svg` - Export heatmap to SVG file
- `commit-checker --stats-lang` - Programming language breakdown with charts
- `commit-checker --time-stats` - Commit timing analysis (morning/afternoon/evening/night)
- `commit-checker --dashboard` - Quick stats overview (commits today, streak, XP, top repo)
- `commit-checker --suggest` - Analyze latest commit message and suggest improvements

**📚 Enhanced TIL (Today I Learned) Vault System:**
- `commit-checker til "Your learning today"` - Add a TIL entry to log
- `commit-checker til "Fixed bug" --template bugfix` - Use template for vault entry
- `commit-checker --list-templates` - Show available TIL templates
- `commit-checker --add-template NAME "STRUCTURE"` - Create custom TIL templates
- `commit-checker --til-vault` - Show TIL vault summary with stats
- `commit-checker --search-til "async"` - Fuzzy search TIL entries
- `commit-checker --til-from-diff` - Generate TIL from latest commit changes
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

### 🎮 Gamification System
```bash
$ commit-checker
🌐 GitHub: @AmariahAK
😢 No public commits found today.

🗂️  Scanning 1 local path(s):
   📁 /Users/you/Documents/GitHub

🟩 Local Commits:
📁 Repository: commit-checker
   📍 Path: /Users/you/Documents/GitHub/commit-checker
   📊 3 commit(s) today:
   e05feb7 feat: implement v0.6.1 - Critical Fixes & Enhanced Reliability

⚡ 3 commits today | +2305 XP | 1🔥 streak | 🚀 Coding machine!
💫 +2305 XP earned today!
🎉 LEVEL UP! You're now level 7!
🏆 New achievements unlocked:
   🟩 Hello World
   🟨 Code Tsunami
🔥 Current streak: 1 days

$ commit-checker --xp
⚡ Level 7: Framework Knight
💫 Total XP: 4,499
📊 Progress: [██░░░░░░░░░░░░░░░░░░] 12.5%
🎯 Next Level: 3,501 XP needed
📈 Commits Tracked: 2

$ commit-checker --achievements
🏆 Achievement Gallery
==================================================

🟩 COMMON BADGES
   🟩 Hello World
   Made your first tracked commit

🟨 EPIC BADGES
   🟨 Code Tsunami
   Single commit with 500+ line changes
```

### 📊 Advanced Analytics
```bash
$ commit-checker --heatmap
📅 Commit Heatmap (Last 365 days)
==================================================

01/28: ░ ░ ░ ░ ░ ░ ░
02/04: ░ ░ ░ ░ ░ ░ ░
...
07/20: ░ ▓ ▒ ▒ ▒ ▒ ░
07/27: ▓ █ ▓ ▒ ░ ░ ░

Legend: ░ None  ▒ Low  ▓ Medium  █ High
Max commits in a day: 5
Last 7 days: 12 commits

$ commit-checker --stats-lang
📊 Programming Language Breakdown
==================================================

Python          [████████████████░░░░░░░░░░░░░░]  54.1% (3,274 lines, 47 files)
JavaScript      [███████░░░░░░░░░░░░░░░░░░░░░░░]  23.2% (1,405 lines, 23 files)
TypeScript      [████░░░░░░░░░░░░░░░░░░░░░░░░░░]  13.1% (793 lines, 12 files)
CSS             [██░░░░░░░░░░░░░░░░░░░░░░░░░░░░]   6.8% (412 lines, 8 files)
Markdown        [█░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]   2.8% (169 lines, 5 files)

📈 Total: 6,053 lines across 95 files
```

### 📚 TIL Vault System
```bash
$ commit-checker --list-templates
📚 Available TIL templates:
  • algorithm
  • bugfix
  • concept
  • feature
  • tool

Usage: commit-checker til "Title" --template algorithm

$ commit-checker til "Fixed async race condition" --template bugfix
TIL created: /Users/you/.commit-checker/tils/2025-07-28-fixed-async-race-condition.md

$ commit-checker --til-vault
📚 TIL Vault Summary
==================================================
📁 Location: /Users/you/.commit-checker/tils/
📄 Total entries: 5

📝 Recent entries:
  • 2025-07-28: Fixed async race condition #bugfix #async
  • 2025-07-27: Implemented new caching layer #feature #performance
  • 2025-07-26: Understanding Docker volumes #concept #docker

🏷️  Popular tags:
  #bugfix (2)
  #feature (1)
  #concept (1)

$ commit-checker --search-til "async"
🔍 Found 2 TIL entries:
==================================================

1. 📝 Fixed async race condition
   📅 2025-07-28 | Score: 10
   L1: # Fixed async race condition
   L15: - Used asyncio.Lock() to prevent race conditions

2. 📝 Understanding async patterns
   📅 2025-07-26 | Score: 5
   L8: - async/await syntax in Python
```

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

### Smart Profile System (v0.7.0)
```bash
$ commit-checker --build-profile
🧙 Building your smart coding profile...
   📊 Analyzing commit history patterns...
   🔍 Detecting project tech stacks...
   📁 Scanning project structures...

✅ Profile built successfully!
   📈 Analyzed 6 repositories
   💡 Smart suggestions now enabled

$ commit-checker --coach "fixed stuff"
🔍 Analyzing: "fixed stuff"

💡 Suggestions:
  💡 Casual style detected—add detail? E.g., fixed stuff → fixed login crash
  💡 'stuff' is vague—what specifically? E.g., 'fixed login stuff' → 'fixed login validation'

$ commit-checker --coach "fix auth bug" --feedback good
🔍 Analyzing: "fix auth bug"

💡 Suggestions:
  💡 Your 'blog-api' uses 'feat:'—try 'feat: fix auth bug'?

👍 Thanks! Tuned your preferences.

$ commit-checker --insights
🧠 Personal Coding Insights
==================================================
📊 Overall Style:
   • Average commit length: 7.5 words
   • Preferred mood: Imperative
   • Uses emojis: No

📁 Repository Analysis (6 repos):
   🔧 Tech Stack Distribution:
     • Python: 4 repos (67%)
     • Javascript: 2 repos (33%)
     • Cli: 1 repos (17%)
   📝 Commit Style Breakdown:
     • Imperative: 4 repos (67%)
     • Lowercase: 2 repos (33%)

🕒 Profile last updated: 2025-09-18 12:10

$ commit-checker til "Learned async patterns"
💡 TIL Tag Suggestions:
  💡 Add --tag python? (detected Python repo)
  💡 Add --tag async? (detected 'async' context)

✅ TIL entry added

$ commit-checker --coach "refactor everything"
🔍 Analyzing: "refactor everything"

💡 Suggestions:
  💡 Large commit (150+ lines, 12 files)—split into smaller commits?
  💡 Casual style detected—add detail? E.g., refactor everything → refactored user auth module
```

---

## 🎉 Recent Updates

### v0.7.2 - Standalone Script Fixes (Latest)
- 🔧 **Fixed Standalone Profile Commands** - `--build-profile`, `--insights`, `--coach` now work in standalone mode
- 📱 **Added `--version` Flag** - Show version information and project details  
- 🛡️ **Enhanced Standalone Compatibility** - Profile functions now work for curl/bash installations
- 🔄 **Fixed Update System** - Resolved infinite update loops in standalone mode
- 📦 **Improved Command Routing** - All Smart Profile System commands now properly execute

### v0.7.1 - Smart Profile System  
- 🐛 **Critical Bug Fixes** - Fixed sys import error causing command failures
- ⚡ **Enhanced Stability** - All commands now exit cleanly without errors
- 🛡️ **Improved Install Script** - Better error handling during installation
- 🔧 **Refined Coaching** - More accurate freeform style detection
- 📊 **Performance Optimizations** - Faster profile building and analysis

### v0.7.0 - Smart Profile System
- 🧠 **Adaptive Coaching** - Suggests clarity for freeform styles (e.g., "fixed stuff → fixed login crash")
- 📚 **Expanded Tech Detection** - Added PHP, Swift, Kotlin, Elixir, Scala, Haskell, TypeScript
- 💡 **New Suggestions** - Commit size nudges, TIL tag recommendations
- 👍 **--feedback good/bad** - Tune coaching preferences
- 🔧 **Stack-aware Suggestions** - Django migrations, npm installs, cargo checks, etc.
- 📊 **Personal Coding Insights** - Analyze your habits, tech stack distribution, and style evolution
- 📁 **Project Structure Analysis** - Suggests tests, documentation, and maintenance tasks
- 🎵 **Sound Notifications** - Audio feedback for completions and suggestions
- 🧙 **New Commands**: `--build-profile`, `--coach`, `--insights`, `--no-profile`, `--feedback`

### v0.6.2 - Enhanced Feedback & Advanced Analytics
- 🔍 **Commit Message Analysis** - New `--suggest` command analyzes and improves commit messages
- 📊 **Quick Dashboard** - New `--dashboard` command for instant daily overview
- ⏰ **Time Analytics** - New `--time-stats` command shows coding patterns by time of day
- 🎉 **Streak Milestones** - Customizable celebrations for 5, 10, 30, 100+ day streaks
- 📝 **Custom TIL Templates** - Create personalized templates with `--add-template`
- ⚔️ **XP System Rebalanced** - Fixed inflation with logarithmic scaling and level-based caps
- 🏆 **New Achievements** - Secret achievements, polyglot badges, and midnight coder rewards

### v0.6.1 - Critical Fixes & Enhanced Reliability
- 🚨 **Complete Uninstallation** - Fixed `--uninstall` leaving shell startup commands, now removes ALL traces
- 🛡️ **Bulletproof Wizard** - Enhanced `--init` validation prevents invalid input choices with clear error messages
- 🔍 **Improved Detection** - Fixed duplicate repository paths and enhanced counting accuracy in setup
- ⚡ **Standalone Completeness** - Added ALL missing commands (`--achievements`, `--xp`, `--heatmap`, etc.) to curl version
- ✨ **Better UX** - Instant theme feedback, robust input validation, and enhanced error handling

### New v0.6.2 Features in Action
```bash
$ commit-checker --dashboard
📊 Today's Dashboard
==============================
🟩 Commits Today: 3
🔥 Streak: 12 days
⚡ Level 5: [████████░░░░░░░] 650/700 XP
📁 Top Repo: commit-checker (2 commits)

$ commit-checker --suggest
🔍 Latest commit in my-website: "updated code"

💡 Suggestions:
  • Consider starting with an action verb (Add/Fix/Update/etc.)
  • Message is too vague. Be more specific about what changed

$ commit-checker --time-stats
⏰ Commit Time Stats (Last 30 Days)
========================================
Morning (6 AM–12 PM):   [███░░░░░░░░░░░░░░░░░] 15 commits
Afternoon (12 PM–6 PM): [████████████░░░░░░░░] 32 commits  
Evening (6 PM–12 AM):   [████████░░░░░░░░░░░░] 21 commits
Night (12 AM–6 AM):     [█░░░░░░░░░░░░░░░░░░░] 3 commits

$ commit-checker --add-template learning "What I learned: {description}\nWhy it matters: {impact}"
Custom template 'learning' added successfully
```

### v0.6.0 - Offline Gamified Power Mode
- 🎮 **Complete Gamification** - Achievement system with ASCII art, XP levels, streak tracking
- 📊 **Advanced Analytics** - ASCII heatmaps, language breakdown, SVG export, mood system
- 📚 **TIL Vault System** - Templates, fuzzy search, auto-generation from diffs, individual files
- ⚡ **Offline-First Architecture** - Zero external dependencies, pure git-powered analytics
- 🔧 **Developer-Friendly Hooks** - Non-blocking git hooks for seamless integration
- 🛠️ **15+ New Commands** - Comprehensive CLI with gamification, analytics, and vault features

### v0.5.0 - Interactive Wizards & Enhanced Analytics
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
