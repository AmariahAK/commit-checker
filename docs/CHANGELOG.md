# Changelog

All notable changes to commit-checker will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.8.5] - 2025-11-21

### Added

#### AI Features
- **TogetherAI Integration** with flexible model selection - use ANY model from together.ai
- **Unified AI Model Manager** supporting 3 model types (TensorFlow, Local, TogetherAI)
- **--setup-ai** command for easy TogetherAI API configuration
- **--ai-suggest** command for AI-powered commit message suggestions from staged changes
- **--ai-status** command to check AI model availability
- Intelligent fallback system when preferred AI model unavailable
- Cost tracking and warnings for API usage
- Encrypted API key storage

####Language Support
- **30+ new programming languages** detected:
  - Systems: C/C++, Objective-C, Zig, Nim, Crystal, V, Fortran, Assembly
  - Mobile: Dart/Flutter, React Native
  - Data Science: R, Julia, MATLAB
  - Scripting: Perl, Lua, Bash/Zsh, PowerShell
  - Hardware: VHDL, Verilog
  - Blockchain: Solidity, Move (Sui/Aptos), Cairo (Starknet)
  - Other: LaTeX, Markdown

#### Analysis Features
- **Enhanced Diff Analyzer** with detailed breakdown of changes
- **--analyze-diff** command for smart git diff analysis
- **--learn-style** command to analyze commit history and learn user's style
- Function and class-level context extraction from diffs
- Conventional commit type suggestions based on changes
- Human-friendly change explanations

#### Core Modules
- `config_manager.py` - Centralized configuration with encrypted credential storage
- `diff_analyzer.py` - Advanced git diff parsing and analysis
- `history_learner.py` - Commit history analysis and pattern recognition
- `together_ai.py` - TogetherAI API client with flexible model selection
- `ai_models.py` - Unified AI model manager with intelligent fallback

#### Documentation
- Comprehensive CONTRIBUTING.md guide
- Updated LICENSE.md to be contributor-friendly
- TogetherAI setup guides
- AI model selection documentation
- Detailed release notes

### Changed
- **Version updated** to 0.8.5
- Improved startup performance with lazy loading
- Enhanced language detection accuracy
- Optimized diff analysis for large repositories
- Better error messages and user guidance
- Centralized configuration at `~/.commit-checker/config.json`

### Fixed
- Wisdom quote parsing (case-insensitive date matching)
- Date handling in wisdom quotes
- Cache invalidation logic
- API key validation
- Import errors in standalone mode

### Performance
- Reduced startup time from ~0.5s to ~0.3s
- Added caching for diff analysis results
- Lazy loading for AI dependencies
- Optimized language detection
- Async git operations

### Security
- Encrypted API key storage (XOR + Base64)
- Secure credential management
- Clean uninstall with secure deletion
- No API keys in logs or error messages

---

## [0.8.0] - 2025-11-20

### Added
- 🎓 Wisdom Drop integration with daily tech wisdom
- VS Code extension with dashboard and stats
- Enhanced performance with async operations
- Improved wisdom quote display with categories and dates

### Changed
- Updated UI with better formatting
- Improved cache management

### Fixed
- Wisdom quote parsing bugs
- Date display issues
- Performance bottlenecks

---

## [0.7.0] - Previous Release

### Added
- TILVault system
- Template support
- Analytics & Heatmaps
- Gamification features
- Achievement system
- XP & leveling

---

For older changelog entries, see commit history.
