#!/bin/bash

echo "🌱 Installing commit-checker..."

# Clone the repo
git clone https://github.com/AmariahAK/commit-checker.git
cd commit-checker || exit

# Install Python package with fallback for different environments
echo "📦 Installing Python package..."
if pip install . 2>/dev/null; then
    echo "✅ Installed successfully with pip"
elif pip install . --break-system-packages 2>/dev/null; then
    echo "✅ Installed successfully with --break-system-packages"
elif pip install . --user 2>/dev/null; then
    echo "✅ Installed successfully with --user"
elif pip3 install . 2>/dev/null; then
    echo "✅ Installed successfully with pip3"
elif pip3 install . --break-system-packages 2>/dev/null; then
    echo "✅ Installed successfully with pip3 --break-system-packages"
elif pip3 install . --user 2>/dev/null; then
    echo "✅ Installed successfully with pip3 --user"
else
    echo "❌ Installation failed. Please try manually:"
    echo "   pip install . --break-system-packages"
    echo "   or pip install . --user"
    exit 1
fi

# Add to shell startup
SHELL_RC="$HOME/.bashrc"
[[ "$SHELL" == *zsh ]] && SHELL_RC="$HOME/.zshrc"

if ! grep -q "commit-checker" "$SHELL_RC"; then
    echo '📎 Adding commit-checker to shell startup'
    echo -e "\n# Auto-run commit-checker\ncommit-checker\n" >> "$SHELL_RC"
else
    echo "✅ Already set to auto-run in $SHELL_RC"
fi

# Clean up
cd ..
rm -rf commit-checker

echo "✅ Installed! Open a new terminal or run: commit-checker"
