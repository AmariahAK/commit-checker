# Development Guide

## Git Hooks

This repository includes developer-friendly git hooks that integrate with commit-checker:

- **pre-commit**: Optional TIL entry prompts (never blocks commits)
- **post-commit**: Background XP/achievement updates after successful commits

### What the hooks do

✅ **Never block commits** - Always exit successfully  
✅ **Update your XP/achievements** in the background (post-commit)  
✅ **Optional TIL prompts** with timeout (pre-commit)  
✅ **Auto-detect** commit-checker installation  
✅ **Skip in CI environments**  

### Easy opt-out options:

**Temporary disable:**
```bash
COMMIT_CHECKER_DISABLE=1 git commit -m "your message"
```

**Permanent disable:**
```bash
echo 'export COMMIT_CHECKER_DISABLE=1' >> ~/.bashrc  # or ~/.zshrc
```

**Remove hook entirely:**
```bash
rm .git/hooks/pre-commit
```

### Hook behavior:

1. **Silent operation** - Runs in background, doesn't slow down commits
2. **Interactive TIL** - Only prompts in interactive terminals (not scripts/CI)
3. **Timeout protection** - TIL prompt times out after 10 seconds
4. **Graceful fallbacks** - Works with pip-installed or local commit-checker

### For team repositories:

The hook is designed to be **team-friendly**:
- New developers can commit normally even without commit-checker installed
- No configuration required - works out of the box
- Easy to disable for developers who prefer not to use it
- Never interferes with automated workflows or CI/CD

### Installing the hook in other repositories:

If you want to use this hook in other projects:

```bash
# Copy the hook
curl -o .git/hooks/pre-commit https://raw.githubusercontent.com/AmariahAK/commit-checker/main/.git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

## Testing Changes

When working on commit-checker:

```bash
# Test the CLI
python3 -m commit_checker.cli --help

# Test specific features
python3 -m commit_checker.cli --achievements
python3 -m commit_checker.cli --xp
python3 -m commit_checker.cli --heatmap

# Test TIL vault
python3 -m commit_checker.cli til "Testing new feature" --template feature
python3 -m commit_checker.cli --til-vault

# Test without network calls
python3 -m commit_checker.cli --check-only
```

## Installing Dependencies

For development, install the optional dependencies:

```bash
pip install textual plotext --break-system-packages
# or use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Building and Installing

```bash
# Install in development mode
pip install -e . --break-system-packages

# Or build wheel
python3 setup.py bdist_wheel
```
