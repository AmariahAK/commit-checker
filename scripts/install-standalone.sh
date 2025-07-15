#!/bin/bash

echo "🚀 Installing commit-checker (standalone version)..."

# Download the standalone script
curl -s https://raw.githubusercontent.com/AmariahAK/commit-checker/main/commit-checker-standalone.sh -o /usr/local/bin/commit-checker

# Make it executable
chmod +x /usr/local/bin/commit-checker

# Add to shell startup (optional)
SHELL_RC="$HOME/.bashrc"
[[ "$SHELL" == *zsh ]] && SHELL_RC="$HOME/.zshrc"

read -p "Add commit-checker to startup? [Y/n]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
    if ! grep -q "commit-checker" "$SHELL_RC"; then
        echo -e "\n# Auto-run commit-checker\ncommit-checker\n" >> "$SHELL_RC"
        echo "✅ Added to $SHELL_RC"
    else
        echo "✅ Already in $SHELL_RC"
    fi
fi

echo "✅ commit-checker installed! Run: commit-checker"
