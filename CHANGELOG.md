# Changelog

All notable changes to this project will be documented in this file.

## [0.6.0] - 2025-07-28

### 🎮 Gamification & Developer Progress
- **NEW: Achievement System**: Unlock badges with ASCII art based on commit streaks and milestones
  - 🟩 Common (3-day streak): Getting Started, Week Warrior
  - 🟦 Rare (14 days): Fortnight Fighter, Century Club  
  - 🟨 Epic (30 days): Monthly Master, Code Tsunami
  - 🟥 Legendary (90+ days): Legendary Coder, Commit Overlord
  - 🟪 Mythic (365 days): Code Deity
- **NEW: XP & Level System**: Earn XP based on lines changed, project weight, and commit complexity
  - 10 levels from Novice Coder to Programming Deity
  - Visual progress bars and level-up celebrations
  - Configurable XP weights per project

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
- **NEW: TIL Vault Mode**: Individual markdown files instead of single log
- **NEW: Fuzzy Search**: Search TIL entries with highlighted matches (`--search-til`)
- **NEW: TIL from Diff**: Auto-generate TIL entries from git commits (`--til-from-diff`)
- **Enhanced TIL Commands**: `--til-vault`, `--list-templates`, template support

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
- **New Dependencies**: Added textual, plotext, pydub for enhanced features
- **Modular Architecture**: Separated gamification, analytics, and TIL vault into dedicated modules
- **Enhanced CLI**: 15+ new command-line options for comprehensive functionality
- **Automatic Setup**: Default templates and gamification files created on first run

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
