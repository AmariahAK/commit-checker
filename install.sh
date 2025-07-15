#!/bin/bash

echo "🌱 Installing commit-checker..."

# Clone the repo
git clone https://github.com/AmariahAK/commit-checker.git
cd commit-checker || exit

# Install Python package
pip install .

# Add to shell startup
SHELL_RC="$HOME/.bashrc"
[[ "$SHELL" == *zsh ]] && SHELL_RC="$HOME/.zshrc"

if ! grep -q "commit-checker" "$SHELL_RC"; then
    echo '📎 Adding commit-checker to shell startup'
    echo -e "\n# Auto-run commit-checker\ncommit-checker\n" >> "$SHELL_RC"
else
    echo "✅ Already set to auto-run in $SHELL_RC"
fi

echo "✅ Installed! Open a new terminal or run: commit-checker"
