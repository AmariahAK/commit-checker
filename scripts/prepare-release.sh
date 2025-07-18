#!/bin/bash

# commit-checker Release Preparation Script
# Version 0.4.1

set -e

VERSION="0.4.1"
REPO_URL="https://github.com/AmariahAK/commit-checker"

echo "🚀 Preparing commit-checker v$VERSION for release..."

# Verify we're in the right directory
if [ ! -f "setup.py" ] || [ ! -d "commit_checker" ]; then
    echo "❌ Error: Run this script from the project root directory"
    exit 1
fi

# Check if git working directory is clean
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  Warning: Working directory is not clean. Uncommitted changes detected."
    read -p "Continue anyway? [y/N]: " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Release preparation cancelled."
        exit 1
    fi
fi

# Verify version consistency across files
echo "🔍 Verifying version consistency..."

# Check setup.py
SETUP_VERSION=$(grep -o 'version="[^"]*"' setup.py | cut -d'"' -f2)
if [ "$SETUP_VERSION" != "$VERSION" ]; then
    echo "❌ Version mismatch in setup.py: expected $VERSION, found $SETUP_VERSION"
    exit 1
fi

# Check updater.py
UPDATER_VERSION=$(grep -o 'LOCAL_VERSION = "[^"]*"' commit_checker/updater.py | cut -d'"' -f2)
if [ "$UPDATER_VERSION" != "$VERSION" ]; then
    echo "❌ Version mismatch in updater.py: expected $VERSION, found $UPDATER_VERSION"
    exit 1
fi

echo "✅ Version consistency verified"

# Run basic functionality tests
echo "🧪 Running basic functionality tests..."

# Test help command
if ! python3 -m commit_checker.cli --help >/dev/null 2>&1; then
    echo "❌ Help command test failed"
    exit 1
fi

# Test new features
echo "  Testing --scan functionality..."
if ! python3 -m commit_checker.cli --check-only --scan >/dev/null 2>&1; then
    echo "❌ Scan command test failed"
    exit 1
fi

echo "  Testing --repos-summary functionality..."
if ! python3 -m commit_checker.cli --check-only --repos-summary >/dev/null 2>&1; then
    echo "❌ Repos summary command test failed"
    exit 1
fi

echo "  Testing --most-active functionality..."
if ! python3 -m commit_checker.cli --check-only --most-active --week >/dev/null 2>&1; then
    echo "❌ Most active command test failed"
    exit 1
fi

echo "✅ All functionality tests passed"

# Create distribution files
echo "📦 Creating distribution files..."
rm -rf dist/ build/ *.egg-info/
python3 setup.py sdist bdist_wheel >/dev/null 2>&1
echo "✅ Distribution files created"

# Create release assets
echo "📋 Creating release assets..."
RELEASE_DIR="release-v$VERSION"
mkdir -p "$RELEASE_DIR"

# Copy main files
cp README.md "$RELEASE_DIR/"
cp LICENSE.md "$RELEASE_DIR/"
cp CHANGELOG.md "$RELEASE_DIR/"
cp requirements.txt "$RELEASE_DIR/"
cp setup.py "$RELEASE_DIR/"
cp -r commit_checker/ "$RELEASE_DIR/"
cp -r scripts/ "$RELEASE_DIR/"

# Create tarball
tar -czf "commit-checker-v$VERSION.tar.gz" "$RELEASE_DIR"
echo "✅ Release tarball created: commit-checker-v$VERSION.tar.gz"

# Generate release notes
echo "📝 Generating release notes..."
cat > "RELEASE_NOTES_v$VERSION.md" << EOF
# 🚀 commit-checker v$VERSION Release

## 🔥 Major New Features

### Repository Analytics
- **\`--scan\`** - Automatically detect and analyze all git repositories in your development folder
- **\`--repos-summary\`** - Get a complete overview of all your repositories with commit statistics  
- **\`--most-active\`** - Find your most productive repository with daily, weekly, or monthly views

### Enhanced User Experience
- **Configurable Output** - Choose between emoji-rich or plain text output modes
- **Smart Configuration** - Persistent settings for repository scanning and display preferences
- **Improved Uninstall** - Complete cleanup with \`--force\` option for unattended removal

## 📊 What's New

\`\`\`bash
# Scan all your repositories
commit-checker --scan

# See complete repository statistics
commit-checker --repos-summary

# Find your most active repo this week
commit-checker --most-active --week
\`\`\`

## 🛠️ Technical Improvements

- Enhanced git repository detection and analysis
- Better error handling and cross-platform compatibility
- Backward-compatible configuration updates
- Improved output formatting system

## 📦 Installation

### Quick Install (Recommended)
\`\`\`bash
curl -s https://raw.githubusercontent.com/AmariahAK/commit-checker/main/scripts/install-safe.sh | bash
\`\`\`

### Traditional pip Install
\`\`\`bash
pip install git+https://github.com/AmariahAK/commit-checker.git@v$VERSION
\`\`\`

## 🔄 Upgrading from Previous Versions

Existing configurations will be automatically upgraded. No manual intervention required!

## 🐛 Bug Reports & Feature Requests

Please report issues at: $REPO_URL/issues

---

Built with ❤️ by [Amariah Kamau](https://github.com/AmariahAK)
EOF

echo "✅ Release notes generated: RELEASE_NOTES_v$VERSION.md"

echo ""
echo "🎉 Release v$VERSION preparation complete!"
echo ""
echo "📋 Next steps:"
echo "1. Review the generated files:"
echo "   - RELEASE_NOTES_v$VERSION.md"
echo "   - commit-checker-v$VERSION.tar.gz"
echo "   - dist/ directory with wheel and source distribution"
echo ""
echo "2. Commit and tag the release:"
echo "   git add ."
echo "   git commit -m \"Release v$VERSION\""
echo "   git tag -a v$VERSION -m \"Release v$VERSION\""
echo "   git push origin main --tags"
echo ""
echo "3. Create GitHub release:"
echo "   - Go to $REPO_URL/releases/new"
echo "   - Tag: v$VERSION"
echo "   - Title: commit-checker v$VERSION"
echo "   - Description: Use content from RELEASE_NOTES_v$VERSION.md"
echo "   - Attach: commit-checker-v$VERSION.tar.gz"
echo ""
echo "4. Optional: Publish to PyPI:"
echo "   twine upload dist/*"
