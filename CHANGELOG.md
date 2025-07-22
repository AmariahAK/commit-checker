# Changelog

All notable changes to this project will be documented in this file.

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
