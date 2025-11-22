# Release Notes - commit-checker v0.8.5

**Release Date**: November 21, 2025
**Major Feature Expansion**: Advanced AI Integration & 30+ Languages

---

## 🎉 What's New in v0.8.5

This is a **major feature release** adding comprehensive AI capabilities, expanded language support, and enhanced developer insights.

### 🤖 Advanced AI Integration (3 Model Support)

**Flexible AI Model System**:
- ✅ **TogetherAI API** - Use ANY model from together.ai
  - Just paste model ID (e.g., `deepseek-ai/deepseek-coder-33b-instruct`, `Qwen/Qwen2-72B-Instruct`)
  - No hardcoded list - complete freedom!
- ✅ **TensorFlow** (Local, Fast)
- ✅ **Local Large Model** (High Quality)
- ✅ Intelligent fallback system

**New CLI Commands**:
```bash
# Setup TogetherAI with any model
commit-checker --setup-ai

# Get AI commit suggestions from your staged changes
commit-checker --ai-suggest

# Check AI model status
commit-checker --ai-status
```

### 📊 Enhanced Diff Analysis

**Smart Git Diff Parser**:
- Detailed breakdown of changes (added/modified/deleted)
- Function and class-level context extraction
- Human-friendly explanations
- Conventional commit type suggestions
- AI-optimized summaries for better suggestions

**New Command**:
```bash
# Analyze current git diff
commit-checker --analyze-diff
```

### 🧠 User Commit Style Learning

**Personalized Insights**:
- Analyzes your commit history to learn your style
- Detects conventional commit usage
- Identifies common keywords and tone
- Emoji pattern recognition
- Per-repository caching for speed

**New Command**:
```bash
# Learn from your commit history
commit-checker --learn-style
```

### 🌍 Expanded Language Support (30+ Languages)

Now detects and analyzes:
- **Systems**: C/C++, Objective-C, Zig, Nim, Crystal, V, Fortran, Assembly
- **Mobile**: Dart/Flutter, React Native
- **Data Science**: R, Julia, MATLAB
- **Scripting**: Perl, Lua, Bash/Zsh, PowerShell
- **Hardware**: VHDL, Verilog
- **Blockchain**: Solidity, Move (Sui/Aptos), Cairo (Starknet)
- **Other**: LaTeX, Markdown
- Plus all existing languages!

### 🔐 Secure Configuration System

**Centralized Config at `~/.commit-checker/config.json`**:
- Encrypted API key storage (XOR + Base64)
- CLI and VS Code extension sync-ready
- Automatic migration from legacy config
- Clean uninstall (secure deletion)

**Configuration Features**:
- Model preference saving
- Per-repo settings
- User preferences
- Safe credential management

---

## 🛠️ Technical Improvements

### New Core Modules

1. **`config_manager.py`** (~320 lines)
   - Centralized configuration
   - Encrypted API key management
   - Migration and sync support

2. **`diff_analyzer.py`** (~380 lines)
   - Git diff parsing
   - Context extraction
   - Change categorization

3. **`history_learner.py`** (~350 lines)
   - Commit history analysis
   - Style pattern recognition
   - Personalized recommendations

4. **`together_ai.py`** (~320 lines)
   - TogetherAI API client
   - Flexible model selection
   - Cost tracking

5. **`ai_models.py`** (~345 lines)
   - Unified AI model manager
   - Intelligent fallback logic
   - Performance optimization

**Total New Code**: ~1,700+ lines across 5 modules

### Performance Enhancements

- ✅ Lazy loading for AI models
- ✅ Diff analysis caching
- ✅ Optimized language detection
- ✅ Async git operations
- ✅ Reduced startup time

---

## 📚 New Documentation

- ✅ Comprehensive [CONTRIBUTING.md](CONTRIBUTING.md)
- ✅ Updated contributor-friendly [LICENSE.md](LICENSE.md)
- ✅ TogetherAI setup guides
- ✅ AI model selection documentation

---

## 🚀 Usage Examples

### Setup TogetherAI (Super Easy!)

```bash
# Run setup
commit-checker --setup-ai

# Follow prompts:
# 1. Get API key from: https://api.together.xyz/
# 2. Browse models at: https://api.together.xyz/models
# 3. Paste API key when prompted
# 4. Paste model ID (e.g., "Qwen/Qwen2-72B-Instruct")
# Done!
```

### Get AI-Powered Suggestions

```bash
# Stage your changes first
git add .

# Get AI suggestions
commit-checker --ai-suggest

# Output:
# 🤖 AI Suggestions (using TogetherAI):
# 1. feat: add user authentication module
# 2. feat(auth): implement JWT-based user login
# 3. Add user authentication with JWT tokens
```

### Analyze Your Changes

```bash
commit-checker --analyze-diff

# Output:
# **3 file(s) changed**
#   +156 additions, -12 deletions
#
# 📄 New files:
#   • auth.py (+89 lines)
#
# ✏️  Modified files:
#   • config.py (+67 / -12)
#
# 💡 Suggested type: `feat:`
```

### Learn Your Style

```bash
commit-checker --learn-style

# Output:
# 📊 Your Commit Style (from 50 commits):
#
# ✅ Uses conventional commits
# • Most common: feat (42%), fix (28%)
#
# 📝 Message Structure:
# • Average: ~8 words (52 chars)
# • Capitalization: First letter capitalized
# • Punctuation: Rarely uses periods
#
# 🎯 Tone: Imperative ("Add feature")
# 🏷️  Top keywords: add, fix, update, improve
```

---

## 🔄 Migration from v0.8.0

**Automatic**: Existing configs migrate automatically!

- Old cache preserved
- API keys secure
- Settings retained
- Zero manual steps

---

## 📦 Installation / Upgrade

```bash
# Upgrade existing installation
pip install --upgrade commit-checker

# Or fresh install
pip install commit-checker

# Verify version
commit-checker --version
# Should show: v0.8.5
```

---

## 🎯 Complete Feature List

### Commit Analysis
- ✅ GitHub & local commit tracking
- ✅ Streak monitoring
- ✅ Repository scanning
- ✅ 30+ language detection
- ✅ Git diff analysis
- ✅ Commit style learning

### AI Features
- ✅ 3 AI model support (TensorFlow, Local, TogetherAI)
- ✅ Flexible model selection (any TogetherAI model)
- ✅ Diff-based suggestions
- ✅ Personalized recommendations
- ✅ Cost tracking & warnings
- ✅ Intelligent fallback

### Gamification
- ✅ XP & leveling system
- ✅ Achievement unlocks
- ✅ Milestone celebrations
- ✅ Progress tracking

### Analytics
- ✅ Commit heatmaps
- ✅ Language breakdowns
- ✅ Time distribution charts
- ✅ Dashboard views
- ✅ SVG export

### TIL (Today I Learned)
- ✅ Entry management
- ✅ Template system
- ✅ Fuzzy search
- ✅ Tag filtering
- ✅ Export (MD/JSON)
- ✅ Diff-based TIL creation

### Integration
- ✅ VS Code extension (ready)
- ✅ CLI interface
- ✅ Wisdom Drop quotes
- ✅ Auto-updates

---

## 🐛 Bug Fixes

- Fixed wisdom quote parsing (case-insensitive)
- Improved date handling in wisdom quotes
- Enhanced error messages
- Better API key validation
- Optimized cache invalidation

---

## ⚡ Performance Stats

| Metric | v0.8.0 | v0.8.5 |
|--------|--------|--------|
| Languages Supported | ~15 | 30+ |
| AI Models | 2 | 3 (+ infinite via API) |
| Startup Time | ~0.5s | ~0.3s |
| Diff Analysis | Basic | Advanced |
| Personalization | None | Full history learning |
| Code Modules | 15 | 20 |

---

## 🙏 Credits

- **Lead Developer**: Amariah Aderonke Kyeremaa
- **Wisdom Drop**: Integrated from the wisdom-drop project
- **Contributors**: All contributors recognized in LICENSE.md
- **Community**: Thank you for your support and feedback!

---

## 🔗 Links

- **GitHub**: https://github.com/AmariahAK/commit-checker
- **TogetherAI**: https://api.together.xyz/
- **Wisdom Drop**: https://github.com/AmariahAK/wisdom-drop
- **Documentation**: See README.md

---

## 📝 Notes

- API keys are encrypted and stored securely
- TogetherAI usage costs apply (user's own API key)
- Spending limits recommended on TogetherAI account
- All local models run offline
- VS Code extension works without separate login

---

**Enjoy v0.8.5! 🎉**

Questions? Open an issue on GitHub!
