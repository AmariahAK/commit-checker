# Commit Checker VS Code Extension

Track your GitHub streak, commits, XP, and achievements directly in VS Code!

## Features

- **Status Bar Widget**: Shows current streak, commits today, and level at a glance
- **Interactive Dashboard**: View detailed stats including XP progress, achievements, and top repos
- **TIL Integration**: Quickly add and search Today I Learned entries from within VS Code
- **Commit Message Coaching**: Get smart suggestions for better commit messages (if profile enabled)
- **Local & Secure**: Uses your existing commit-checker CLI installation - no separate login required

## Requirements

commit-checker CLI must be installed. Install with:

```bash
curl -s https://raw.githubusercontent.com/AmariahAK/commit-checker/main/scripts/install-standalone.sh | bash
```

Or via pip:

```bash
pip install commit-checker
```

## Extension Settings

This extension contributes the following settings:

* `commit-checker.cliPath`: Path to commit-checker CLI command (default: `commit-checker`)
* `commit-checker.refreshInterval`: Dashboard refresh interval in seconds (default: 300)
* `commit-checker.showStatusBar`: Show commit streak and XP in status bar (default: true)
* `commit-checker.enableCoaching`: Enable commit message coaching suggestions (default: true)

## Usage

### Status Bar

The status bar shows:
- 🔥 Your current streak
- Daily commits
- Current level

Click the status bar to open the full dashboard.

### Commands

- `Commit Checker: Show Dashboard` - Open the stats dashboard
- `Commit Checker: Refresh Stats` - Manually refresh stats
- `Commit Checker: Add TIL Entry` - Add a Today I Learned entry
- `Commit Checker: Search TIL` - Search your TIL vault
- `Commit Checker: View Achievements` - View unlocked achievements

### Dashboard

The dashboard displays:
- Commits today
- Current streak (with fire emoji!)
- XP progress bar with level
- Top repository
- Quick access to full CLI features

## How It Works

This extension integrates with your local commit-checker CLI installation. It:
1. Reads your GitHub username from git config (same as CLI)
2. Uses local git repositories for commit tracking
3. No separate authentication needed - uses your existing setup

All data stays local and secure, just like the CLI tool.

## Publishing to VS Code Marketplace

To publish this extension:

1. Install vsce: `npm install -g @vscode/vsce`
2. Create a publisher account at https://marketplace.visualstudio.com/manage
3. Get a Personal Access Token from Azure DevOps
4. Login: `vsce login <publisher-name>`
5. Package: `vsce package`
6. Publish: `vsce publish`

For detailed instructions, see: https://code.visualstudio.com/api/working-with-extensions/publishing-extension

## Known Issues

- Initial stats load may take a few seconds on first activation
- Some TIL search results may not format perfectly in webview

## Release Notes

### 0.8.0

Initial release! 🎉

Features:
- Status bar integration showing streak and XP
- Interactive dashboard with stats
- TIL integration for quick logging
- Achievements gallery
- Local-only, secure by design

---

**Enjoy tracking your commits in VS Code!** 🚀

For bugs or feature requests, visit: https://github.com/AmariahAK/commit-checker/issues
