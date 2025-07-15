#!/bin/bash

# Safe installer that downloads first, then executes
# This avoids character encoding issues with direct piping to bash

echo "🚀 Installing commit-checker (safe method)..."

# Create temporary directory
TMP_DIR=$(mktemp -d)
INSTALL_SCRIPT="$TMP_DIR/install-standalone.sh"

# Download the installer
if curl -s https://raw.githubusercontent.com/AmariahAK/commit-checker/main/scripts/install-standalone.sh -o "$INSTALL_SCRIPT"; then
    echo "✅ Downloaded installer successfully"
else
    echo "❌ Failed to download installer"
    rm -rf "$TMP_DIR"
    exit 1
fi

# Make it executable
chmod +x "$INSTALL_SCRIPT"

# Execute the installer
echo "🔧 Running installer..."
"$INSTALL_SCRIPT"

# Clean up
rm -rf "$TMP_DIR"

echo "🎉 Installation complete!"
