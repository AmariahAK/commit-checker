# Release Notes - Commit-Checker v0.8.0

## 🚀 What's New in v0.8.0

This release brings major improvements to commit-checker with enhanced wisdom quotes, better AI assistant communication, and the debut of our VS Code extension!

---

## ✨ New Features

### 🔮 VS Code Extension (NEW!)
Track your commits, streak, and XP directly in VS Code!

- **Status Bar Integration** - See streak, commits, and level at a glance
- **Interactive Dashboard** - Beautiful webview with stats and progress bars
- **TIL Quick Access** - Add and search TIL entries from the editor
- **Achievements Gallery** - View unlocked badges within VS Code
- **Local & Secure** - Uses your existing CLI installation, no separate login
- **Auto-refresh** - Configurable stats updates (default: 5 minutes)

**Installation**: Search for "Commit Checker" in VS Code Extensions Marketplace

### 💡 Enhanced Wisdom Quotes
Daily inspirational quotes now show **category** and **date**!

**Before**: `💡 [Wisdom] Wisdom of the day: "quote" — Author`  
**After**: `💡 [Faith / Purpose] Wisdom of the day (October 21 2025): "quote" — Tony Gaskins`

- Shows wisdom category (Developer, Life, Samurai, Faith, etc.)
- Displays the specific date of the quote
- **Date-based cache invalidation** - Quotes refresh daily, even without new wisdom-drop commits
- Improved parsing for multi-word categories (e.g., "Samurai Discipline / Modern Focus")

### 🤖 AI Assistant Improvements
Better communication about AI model availability!

- **New `--ai-status` command** - Check if AI models are available
- Clear error messages with actionable guidance:
  - Missing dependencies? → Install command provided
  - Models not downloaded? → Download command provided
  - Ready to use? → Confirmation message
- Falls back gracefully to heuristics when models unavailable
- Improved suggestions quality in heuristic mode

---

## 🐛 Bug Fixes

### Wisdom Quote System
- ✅ **Fixed**: Quotes not updating daily when wisdom-drop repo had no new commits
- ✅ **Fixed**: Category extraction for complex category names with slashes and multiple words
- ✅ **Fixed**: Cache validation now checks both commit SHA and current date

### AI Assistant
- ✅ **Fixed**: Silent fallback to heuristics - now shows status messages
- ✅ **Fixed**: No indication when transformers/torch not installed - now provides clear guidance
- ✅ **Fixed**: `--download-models` command not well-documented - now mentioned in `--ai-status`

### Performance
- ✅ **Optimized**: Startup time by improving bootstrap sequence
- ✅ **Optimized**: Update checks now have better caching
- ✅ **Optimized**: Profile loading is more efficient

---

## 🎨 Improvements

### User Experience
- Updated version display to v0.8.0
- Better error messages throughout the tool
- Clearer command help text
- Improved guidance for new users

### Code Quality
- Refactored wisdom quote parsing for better reliability
- Enhanced AI handler with status messaging
- Better separation of concerns in CLI module
- Improved type safety in extension code

---

## 📦 Technical Changes

- **Version**: Bumped to 0.8.0 in `setup.py` and CLI
- **Dependencies**: No new required dependencies
- **Optional**: VS Code Extension requires vscode ^1.75.0
- **Python**: Still requires Python >=3.13 (or 3.7+ for basic features)

---

## 🗑️ Deprecated/Removed

- Removed `DEVELOPMENT.md` (content integrated into main README)
- Removed `roadmap.md` (tracked in GitHub Issues instead)

---

## 📚 Documentation Updates

- Updated README with v0.8 features
- Added VS Code extension documentation
- Improved troubleshooting section
- Added development guide inline

---

## 🔄 Migration Guide

### From v0.7.x to v0.8.0

**No breaking changes!** This is a fully backward-compatible release.

#### Recommended Actions:
1. **Clear wisdom quote cache** for immediate category/date display:
   ```bash
   rm ~/.commit_checker_cache/quote.json
   ```

2. **Check AI status** to see if you can use AI features:
   ```bash
   commit-checker --ai-status
   ```

3. **Install VS Code extension**:
   - Open VS Code
   - Go to Extensions (Cmd+Shift+X / Ctrl+Shift+X)
   - Search for "Commit Checker"
   - Click Install

#### Configuration:
No config changes needed. All existing configurations work as-is.

---

## 🎯 What's Next?

Coming in future releases:
- Browser extension for GitHub streak tracking
- Mobile app for on-the-go commits
- Team leaderboards and challenges
- Integration with more git platforms (GitLab, Bitbucket)

---

## 💖 Credits

**Developed by**: Amariah Kamau ([@AmariahAK](https://github.com/AmariahAK))

**Special Thanks**: 
- All users who provided feedback on v0.7.x
- wisdom-drop contributors for daily inspiration
- VS Code extension API documentation

---

## 🐛 Known Issues

- VS Code extension: Initial stats load may take 2-3 seconds
- Wisdom quote categories with emojis may not display correctly in plain mode
- AI model download requires ~300MB disk space

---

## 📝 Changelog Summary

```
v0.8.0 (2025-11-21)
  • NEW: VS Code extension with status bar and dashboard
  • NEW: Wisdom quotes show category and date
  • NEW: --ai-status command for AI availability check
  • IMPROVED: Daily quote refresh without requiring new commits
  • IMPROVED: Better AI assistant error messages and guidance
  • FIXED: Quote cache validation logic
  • FIXED: Category extraction for complex names
  • OPTIMIZED: Startup performance
```

---

## 🚀 Installation/Update

### New Installation:
```bash
curl -s https://raw.githubusercontent.com/AmariahAK/commit-checker/main/scripts/install-standalone.sh | bash
```

### Update from Previous Version:
```bash
commit-checker --update
```

Or reinstall:
```bash
curl -s https://raw.githubusercontent.com/AmariahAK/commit-checker/main/scripts/install-standalone.sh | bash
```

---

**Full Changelog**: https://github.com/AmariahAK/commit-checker/compare/v0.7.8...v0.8.0
**Documentation**: https://github.com/AmariahAK/commit-checker#readme
**Issues**: https://github.com/AmariahAK/commit-checker/issues

---

**Enjoy v0.8.0! Keep that streak alive! 🔥**
