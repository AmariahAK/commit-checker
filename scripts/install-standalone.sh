#!/bin/bash

echo "🚀 Installing commit-checker (standalone version)..."

# Create local bin directory if it doesn't exist
mkdir -p "$HOME/.local/bin"

# Download the standalone script
if curl -s https://raw.githubusercontent.com/AmariahAK/commit-checker/main/scripts/commit-checker-standalone.sh -o "$HOME/.local/bin/commit-checker"; then
    echo "✅ Downloaded successfully"
else
    echo "❌ Download failed"
    exit 1
fi

# Make it executable
chmod +x "$HOME/.local/bin/commit-checker"

# Add ~/.local/bin to PATH if not already there
SHELL_RC="$HOME/.bashrc"
[[ "$SHELL" == *zsh ]] && SHELL_RC="$HOME/.zshrc"

if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
    echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$SHELL_RC"
    echo "✅ Added ~/.local/bin to PATH in $SHELL_RC"
    export PATH="$HOME/.local/bin:$PATH"
fi

# Add to shell startup (optional)
echo ""
read -p "Add commit-checker to startup? [Y/n]: " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
    if ! grep -q "commit-checker" "$SHELL_RC"; then
        echo -e "\n# Auto-run commit-checker\ncommit-checker\n" >> "$SHELL_RC"
        echo "✅ Added to startup in $SHELL_RC"
    else
        echo "✅ Already in startup"
    fi
fi

echo ""
echo "✅ commit-checker installed! Run: commit-checker"
echo "💡 You may need to restart your terminal or run: source $SHELL_RC"
