#!/bin/bash

# Complete commit-checker removal script
# This will remove all traces of commit-checker from your system

echo "🗑️  Complete commit-checker removal script"
echo "=========================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to remove file/directory if it exists
safe_remove() {
    if [ -e "$1" ]; then
        echo "🗑️  Removing: $1"
        rm -rf "$1"
    fi
}

# Function to remove binary if it exists
remove_binary() {
    if [ -f "$1" ]; then
        echo "🗑️  Removing binary: $1"
        sudo rm -f "$1" 2>/dev/null || rm -f "$1" 2>/dev/null
    fi
}

echo ""
echo "Step 1: Removing pip installations..."

# Try to uninstall via pip (multiple methods)
if command_exists pip; then
    echo "📦 Attempting pip uninstall..."
    pip uninstall commit-checker -y 2>/dev/null || true
    pip uninstall commit-checker --break-system-packages -y 2>/dev/null || true
fi

if command_exists pip3; then
    echo "📦 Attempting pip3 uninstall..."
    pip3 uninstall commit-checker -y 2>/dev/null || true
    pip3 uninstall commit-checker --break-system-packages -y 2>/dev/null || true
fi

if command_exists python -m pip; then
    echo "📦 Attempting python -m pip uninstall..."
    python -m pip uninstall commit-checker -y 2>/dev/null || true
    python -m pip uninstall commit-checker --break-system-packages -y 2>/dev/null || true
fi

if command_exists python3 -m pip; then
    echo "📦 Attempting python3 -m pip uninstall..."
    python3 -m pip uninstall commit-checker -y 2>/dev/null || true
    python3 -m pip uninstall commit-checker --break-system-packages -y 2>/dev/null || true
fi

echo ""
echo "Step 2: Removing binaries from common locations..."

# Remove binaries from common locations
remove_binary "/usr/local/bin/commit-checker"
remove_binary "/usr/bin/commit-checker"
remove_binary "$HOME/.local/bin/commit-checker"
remove_binary "/opt/homebrew/bin/commit-checker"
remove_binary "/usr/local/Cellar/commit-checker"

echo ""
echo "Step 3: Removing configuration and data..."

# Remove configuration directories
safe_remove "$HOME/.commit-checker"
safe_remove "$HOME/.commit-checker-standalone"

echo ""
echo "Step 4: Checking for package installations..."

# Check for Python package installations
PYTHON_PATHS=(
    "/usr/local/lib/python*/site-packages/commit_checker*"
    "/usr/lib/python*/site-packages/commit_checker*"
    "$HOME/.local/lib/python*/site-packages/commit_checker*"
    "/opt/homebrew/lib/python*/site-packages/commit_checker*"
    "/Library/Python/*/site-packages/commit_checker*"
)

for path_pattern in "${PYTHON_PATHS[@]}"; do
    for path in $path_pattern; do
        if [ -e "$path" ]; then
            echo "🗑️  Removing Python package: $path"
            rm -rf "$path" 2>/dev/null || sudo rm -rf "$path" 2>/dev/null || true
        fi
    done
done

echo ""
echo "Step 5: Removing from shell startup files..."

# Remove from shell startup files
SHELL_FILES=(
    "$HOME/.bashrc"
    "$HOME/.zshrc"
    "$HOME/.bash_profile"
    "$HOME/.profile"
)

for shell_file in "${SHELL_FILES[@]}"; do
    if [ -f "$shell_file" ]; then
        if grep -q "commit-checker" "$shell_file"; then
            echo "🗑️  Removing commit-checker from $shell_file"
            # Create backup
            cp "$shell_file" "$shell_file.backup.$(date +%s)"
            # Remove lines containing commit-checker
            grep -v "commit-checker" "$shell_file.backup.$(date +%s)" > "$shell_file"
        fi
    fi
done

echo ""
echo "Step 6: Clearing PATH references..."

# Remove from current PATH (temporary)
export PATH=$(echo "$PATH" | tr ':' '\n' | grep -v commit-checker | tr '\n' ':' | sed 's/:$//')

echo ""
echo "Step 7: Final cleanup check..."

# Check if any commit-checker processes are running
if pgrep -f "commit-checker" >/dev/null; then
    echo "🛑 Stopping running commit-checker processes..."
    pkill -f "commit-checker" 2>/dev/null || true
fi

# Check if command still exists
if command_exists commit-checker; then
    echo "⚠️  commit-checker command still found in PATH"
    echo "📍 Location: $(which commit-checker)"
    echo "🗑️  Attempting manual removal..."
    MANUAL_PATH=$(which commit-checker)
    rm -f "$MANUAL_PATH" 2>/dev/null || sudo rm -f "$MANUAL_PATH" 2>/dev/null || true
else
    echo "✅ commit-checker command no longer found in PATH"
fi

echo ""
echo "=========================================="
echo "✅ Complete removal finished!"
echo ""
echo "🔄 To verify removal, try:"
echo "   commit-checker --version"
echo "   (should show 'command not found')"
echo ""
echo "📦 To install the latest version:"
echo "   curl -s https://raw.githubusercontent.com/AmariahAK/commit-checker/main/scripts/install-safe.sh | bash"
echo ""
echo "💡 You may need to restart your terminal or run:"
echo "   source ~/.bashrc   # or ~/.zshrc"
echo ""
