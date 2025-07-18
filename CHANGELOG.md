# Changelog

All notable changes to this project will be documented in this file.

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
