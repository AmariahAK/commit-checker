# Changelog

All notable changes to this project will be documented in this file.

## [0.6.2] - 2025-08-26

### 🔍 **Enhanced Commit Message Feedback**
- **NEW: `--suggest` command** - Analyzes latest commit messages with rule-based checks
- **Smart suggestions** for verb usage, vague messages, length, and capitalization
- **Context-aware feedback** respects emoji/plain output mode preference
- **Repository detection** automatically finds and analyzes most recent commit across all monitored repos

### 📊 **Quick Stats Dashboard**
- **NEW: `--dashboard` command** - Concise overview of today's coding activity
- **Real-time metrics**: commits today, current streak, XP progress, most active repo
- **Visual progress bars** for level advancement with Unicode blocks
- **Consistent theming** respects user's emoji/plain text preference
- **Lightweight design** for quick daily status checks

### ⏰ **Lightweight Commit Time Analysis**
- **NEW: `--time-stats` command** - Commit timing patterns over last 30 days
- **Time buckets**: Morning (6AM-12PM), Afternoon (12PM-6PM), Evening (6PM-12AM), Night (12AM-6AM)
- **ASCII bar charts** showing commit distribution by time of day
- **Pattern insights** for optimizing coding schedules and productivity

### 🎉 **Customizable Streak Notifications**
- **Milestone celebrations** with ASCII art for 5, 10, 30, and 100-day streaks
- **Configurable messages** stored in config.json for personalization
- **Contextual display** only shows when streak milestones are reached
- **Motivational messaging** to encourage consistency

### 📝 **TIL Template Customization**
- **NEW: `--add-template` command** - Create custom TIL templates
- **Variable substitution** supports {{title}}, {{date}}, {{timestamp}} placeholders
- **Smart structure** automatically adds proper markdown headers if missing
- **Template validation** with sanitized naming and error handling

### ⚔️ **XP & Leveling System Overhaul**
- **🔧 Fixed XP inflation** - Logarithmic scaling prevents massive XP jumps (was +7569, now capped at ~50)
- **Exponential level curve** - Soulslike progression (easy early levels, very difficult later)
- **Diminishing returns formula** - `final_XP = raw_XP / (1 + (level / 10))`
- **Repo weighting system** - Small repos give proportionally less XP at higher levels
- **Dynamic bonuses**: +10 XP for first commit of day, +5 XP for weekend commits
- **Level-based XP caps** - Maximum XP per commit scales with current level
- **Improved XP calculation** - Better parsing of git diff stats with files changed bonus

### 🏆 **Achievements System Expansion**
- **NEW achievements**: Consistency King (5-day), Double Digits (10 commits), Centennial Coder (100-day streak)
- **Secret achievements**: Midnight Coder (2-4 AM commits), Code Polyglot (5+ languages), Weekend Warrior
- **Enhanced ASCII art** - Multi-line display with full terminal width utilization
- **Rarity system expansion** - Better distribution across Common, Rare, Epic, Legendary, Mythic
- **Special conditions** - Time-based and language-based achievement triggers
- **Improved unlock detection** - More reliable achievement progression tracking

### 🛠️ **Technical Improvements**
- **Anti-inflation architecture** - Logarithmic XP scaling with level-based penalties
- **Smart git parsing** - Enhanced diff analysis with insertions, deletions, and files changed
- **Performance optimization** - Reduced XP calculation overhead
- **Config migration** - Automatic addition of new config fields (streak_milestones, xp_weights)
- **Error handling** - Graceful fallbacks for all new analytics functions

### 🎯 **New CLI Commands**
- `--suggest` - Commit message analysis and improvement suggestions
- `--dashboard` - Quick stats overview (commits, streak, XP, top repo)
- `--time-stats` - Commit timing analysis with visual charts
- `--add-template NAME "STRUCTURE"` - Create custom TIL templates

### 📈 **User Experience Enhancements**
- **Milestone celebrations** appear automatically during normal commit checking
- **Contextual suggestions** provide actionable feedback for commit messages
- **Unified theming** across all new features respects user preferences
- **Progressive disclosure** - Advanced features don't clutter basic usage

## [0.6.1] - 2025-07-28

### 🚨 Critical Fixes
- **Fixed complete uninstallation**: `--uninstall` now properly removes ALL traces including shell startup commands
- **Enhanced wizard validation**: Fixed ability to enter invalid choices (letters, out-of-range numbers) in `--init` wizard
- **Repository detection improvements**: Fixed duplicate path detection and improved repo counting accuracy
- **Standalone script completeness**: Added ALL missing commands (`--achievements`, `--xp`, `--heatmap`, etc.) to standalone version

### 🛠️ Technical Improvements
- **Shell cleanup**: Automatically removes auto-run commands from `~/.zshrc`, `~/.bashrc`, `~/.bash_profile`, `~/.profile`, Fish config
- **Input validation framework**: Consistent validation patterns with clear error messages across all user inputs
- **Path resolution**: Smart handling of symlinks and path variations to eliminate false duplicates
- **Enhanced module loading**: Auto-download missing modules for standalone installations

### 🎯 User Experience
- **Instant theme feedback**: Theme selection now shows immediate confirmation ("✨ Theme set to: tech")
- **Better error messages**: Clear, actionable error messages throughout the wizard
- **Support link update**: Updated from PayPal to Buy Me A Coffee
- **Standalone feature parity**: All v0.6.0 features now available in curl-installed version

### 🐛 Bug Fixes
- Fixed wizard accepting invalid input choices and crashing
- Fixed incomplete cleanup leaving commit-checker auto-run commands after uninstall
- Fixed duplicate repository entries in setup wizard
- Fixed missing gamification and analytics commands in standalone script
- Fixed incorrect repository counting in path detection
- Fixed missing validation on final confirmation prompt

## [0.6.0] - 2025-07-28

### 🎮 Gamification & Developer Progress
- **NEW: Achievement System**: Unlock badges with ASCII art based on commit streaks and milestones
  - 🟩 Common (3-day streak): Getting Started, Week Warrior
  - 🟦 Rare (14 days): Fortnight Fighter, Century Club  
  - 🟨 Epic (30 days): Monthly Master, Code Tsunami
  - 🟥 Legendary (90+ days): Legendary Coder, Commit Overlord
  - 🟪 Mythic (365 days): Code Deity
  - Commands: `--achievements` to display gallery
- **NEW: XP & Level System**: Earn XP based on lines changed, project weight, and commit complexity
  - 10 levels from Novice Coder to Programming Deity
  - Visual progress bars and level-up celebrations
  - Configurable XP weights per project
  - Commands: `--xp` to show current status
- **NEW: Automatic Integration**: Gamification data automatically shown in main commit check
- **NEW: Streak Tracking**: Daily commit streaks with smart detection across repositories

### 📊 Analytics & Visualizations  
- **NEW: ASCII Commit Heatmap**: GitHub-style heatmap with 365-day history (`--heatmap`)
- **NEW: Language Breakdown**: Analyze coding languages across repositories (`--stats-lang`)
- **NEW: SVG Export**: Export heatmaps to SVG format (`--heatmap --export svg`)
- **NEW: Mood Commit Line**: Dynamic status messages based on activity level
- **Enhanced Commit Trends**: Weekly patterns and activity analysis

### 📚 TIL Vault System
- **NEW: TIL Templates**: Markdown templates for structured learning entries
  - Bugfix, Feature, Concept, Tool, Algorithm templates included
  - Custom template creation with variable substitution
  - Command: `--list-templates` to show available templates
  - Usage: `commit-checker til "Title" --template bugfix`
- **NEW: TIL Vault Mode**: Individual markdown files instead of single log
  - Each entry saved as separate file in `~/.commit-checker/tils/`
  - Automatic date-based naming and organization
- **NEW: Fuzzy Search**: Search TIL entries with highlighted matches (`--search-til`)
  - Score-based ranking with highlighted matches
  - Search across titles, content, and tags
- **NEW: TIL from Diff**: Auto-generate TIL entries from git commits (`--til-from-diff`)
  - Parses git diffs for files changed, function names, statistics
  - No AI required - pure git analysis
- **Enhanced TIL Commands**: `--til-vault` (summary), `--list-templates`, template support

### 🔧 Performance & Usability
- **Offline-First Architecture**: Zero dependencies on external APIs or AI services
- **Enhanced Error Handling**: Better fallbacks and graceful degradation
- **Improved Startup Performance**: Lazy loading and optimized initialization
- **Cross-Platform Compatibility**: Enhanced support for macOS, Linux, Windows

### 🎨 Foundation for Customization
- **Theme System Structure**: JSON-based theme configuration (cyberpunk theme included)
- **Sound System Framework**: Audio notification system with placeholder files
- **Plugin System Base**: Hooks for extending functionality (JSON logger plugin included)

### 🛠️ Technical Improvements
- **New Dependencies**: Added textual, plotext for enhanced features (pydub deferred)
- **Modular Architecture**: Separated gamification, analytics, and TIL vault into dedicated modules
- **Enhanced CLI**: 15+ new command-line options for comprehensive functionality
- **Automatic Setup**: Default templates and gamification files created on first run

### 🎯 New CLI Commands (15+ Added)
- **Gamification**: `--achievements`, `--xp`
- **Analytics**: `--heatmap`, `--heatmap-days N`, `--heatmap-export svg`, `--stats-lang`
- **TIL Vault**: `--search-til "query"`, `--til-vault`, `--til-from-diff`, `--template NAME`, `--list-templates`
- **Enhanced Integration**: All features automatically integrate with main `commit-checker` command
- **Backwards Compatibility**: All existing commands continue to work unchanged

### 💰 Support Updates
- **Updated Support Links**: Moved from PayPal to Buy Me A Coffee
- **Enhanced Documentation**: Comprehensive roadmap and feature documentation

## [0.5.0] - 2025-07-25

### 🔧 Critical Bug Fixes
- **Fixed Update Loop**: Resolved infinite update prompt issue by implementing proper version detection and caching
- **Fixed PEP 668 Uninstall**: Enhanced `--uninstall` to handle externally managed environments with intelligent fallbacks
- **Smart Install Detection**: Added automatic detection of pip, pipx, and standalone installation methods

### 🧙‍♂️ Interactive Setup Wizard
- **New `--init` Command**: Complete interactive setup wizard for first-time configuration
- **Smart Path Detection**: Automatically detects and suggests development folders
- **Theme Selection**: Choose from tech, kawaii, anime, horror, or default themes
- **Commit Rules Configuration**: Setup custom regex patterns for commit message validation
- **Pre-commit Hook Setup**: Optional Git hook installation during setup

### 📊 ASCII Statistics & Analytics
- **New `--stats` Command**: ASCII commit trend charts showing 30-day activity patterns
- **Visual Repository Analysis**: Bar charts using Unicode blocks (▁▂▃▄▅▆▇█)
- **Multi-Repository Stats**: Analyze commit patterns across all local repositories
- **Recent Activity Summary**: Quick view of last 7 days with commit counts

### 📚 Enhanced TIL (Today I Learned) System
- **Tag Support**: Add tags to TIL entries with `--tag` flag (e.g., `#python`, `#react`)
- **Smart Filtering**: Filter TIL entries by tag using `--filter-tag` command
- **Export Functionality**: Export TIL data to Markdown or JSON format with `--export`
- **Enhanced Statistics**: Tag counting and comprehensive TIL analytics
- **Improved Entry Format**: Better markdown structure with tag integration

### 🔍 System Diagnostics
- **New `--diagnose` Command**: Comprehensive system health check
- **Installation Method Detection**: Identifies pip, pipx, venv, or standalone installation
- **Dependency Verification**: Checks for required packages and their availability
- **Configuration Validation**: Verifies config file integrity and settings
- **Environment Analysis**: Detects virtual environments and Python context

### 🛠️ Technical Improvements
- **Version Caching**: Intelligent update checking with 24-hour intervals
- **Enhanced Error Handling**: Better fallback mechanisms for failed operations
- **Cross-Platform Compatibility**: Improved support for macOS, Linux, and Windows
- **Memory Optimization**: Reduced startup time with lazy loading
- **Config Migration**: Automatic migration of old configuration formats

### 📁 Repository Management
- **Intelligent Scanning**: Enhanced repository detection with better performance
- **Commit Statistics**: Detailed analysis of commit patterns and trends
- **Activity Monitoring**: Track repository activity across different timeframes
- **Smart Grouping**: Better organization of multi-repository environments

### 🔄 Update System Improvements
- **Pending Update Management**: Schedule updates for next terminal restart
- **Release Notes Preview**: See what's new before updating
- **Multiple Install Methods**: Robust update handling for different installation types
- **Update Verification**: Confirm successful updates with version validation

## [0.4.3] - 2025-07-22

### 📝 New TIL (Today I Learned) Feature
- **TIL Command**: Added `commit-checker til "message"` to log daily learnings
- **Local Storage**: TIL entries saved to `~/.commit-checker/til.md` with markdown formatting
- **Date Organization**: Entries automatically grouped by date with smart date headers
- **View TIL Log**: Added `--view-til` flag to display current TIL entries
- **Edit TIL Log**: Added `--edit-til` flag to open TIL file in default editor ($EDITOR)
- **Reset TIL Log**: Added `--reset-til` flag to clear all TIL entries with confirmation
- **Minimalist Mode**: Added `--no-date` flag for entries without date headers
- **Custom Path Support**: TIL path configurable via `til_path` in config.json
- **Uninstall Integration**: Prompts to delete TIL log during uninstall process
- **Statistics Tracking**: Internal tracking of TIL entries, dates, and file size

### 🛠️ Technical Improvements
- New `til.py` module with comprehensive TIL management functions
- Enhanced configuration system to support TIL path customization
- Updated both package and standalone versions with TIL functionality
- Improved uninstall process with smart TIL log preservation option
- Added proper error handling and fallback editor detection

### 📁 File Structure Updates
- Enhanced markdown formatting with automatic date grouping
- Smart entry insertion maintaining chronological order
- UTF-8 encoding support for international characters
- Fallback editor chain (EDITOR -> nano -> vim -> vi -> code -> notepad)

## [0.4.2] - 2025-07-18

### 🔄 Enhanced Update System
- **Intelligent Update Scheduling**: Added option to install updates on next terminal restart
- **Enhanced Update Flow**: Three-option update system (now, later, skip)
- **Automatic Pending Updates**: System automatically installs scheduled updates on startup
- **Better Update Feedback**: Shows release notes preview during update check
- **Robust Update Methods**: Multiple fallback installation methods for better compatibility
- **Improved --update Flag**: Enhanced manual update checking with detailed feedback

### 🛠️ Technical Improvements
- Enhanced update marker system with persistent storage
- Better error handling during update processes
- Improved cross-platform update compatibility
- Cleaner startup flow with pending update detection

### 🔧 User Experience
- More informative update prompts with changelog snippets
- Non-intrusive update scheduling for busy workflows
- Better feedback during update installation process
- Simplified update decision making

## [0.4.1] - 2025-07-18

### 🔥 New Features
- **Repository Scanning**: Added `--scan` flag for auto-detection of git repositories with commit analysis
- **Repository Summary**: Added `--repos-summary` flag to show complete statistics of all local repos
- **Most Active Repository**: Added `--most-active` flag with `--day`, `--week`, and `--month` timeframe options
- **Configurable Output**: Added emoji/plain text output modes in configuration
- **Enhanced Uninstall**: Added `--force` flag for unattended removal and complete cleanup

### 🛠️ Improvements
- Enhanced configuration system with `repo_folder` and `output` settings
- Improved output formatting with respect to user preferences
- Better backward compatibility for existing configurations
- More robust error handling for git operations
- Enhanced cleanup during uninstall process

### 📊 Statistics Display
- Today's commits vs total commits for each repository
- Last commit date with smart formatting (Today, Yesterday, Jul 15)
- Visual status indicators (✅/❌) for repository activity
- Repository activity analytics across different timeframes

### 🔧 Technical Changes
- Updated CLI argument parser with new command options
- Enhanced git repository detection and analysis
- Improved cross-platform path handling
- Better exception handling for edge cases

## [0.2.0] - 2025-07-17

### Features
- Smart auto-detection of git repositories
- Enhanced cross-platform support
- Multiple path monitoring
- Standalone bash version
- Improved setup experience

## [0.1.0] - 2025-07-16

### Features
- Basic GitHub and local commit tracking
- CLI interface with multiple flags
- Auto-update functionality
- Cross-platform support
