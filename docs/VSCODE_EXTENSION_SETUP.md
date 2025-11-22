# VS Code Extension Setup Guide

## Publishing Your Commit-Checker VS Code Extension

You have 2 options: **Local installation** (testing) or **Publish to Marketplace** (public).

---

## Option 1: Local Installation (Quick Test)

This is for testing the extension without publishing.

```bash
cd vscode-extension

# Install dependencies
npm install

# Compile TypeScript
npm run compile

# Package extension
npx vsce package

# This creates: commit-checker-0.8.5.vsix
```

**Install in VS Code**:
1. Open VS Code
2. Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
3. Type: `Extensions: Install from VSIX`
4. Select the `.vsix` file you just created
5. Reload VS Code

**Done!** You'll see commit-checker in your status bar.

---

## Option 2: Publish to Marketplace (Public)

This makes your extension available to everyone via the VS Code Marketplace.

### Step 1: Prepare Your Extension

```bash
cd vscode-extension

# Make sure you have a publisher account first (see Step 2)
# Then update package.json with your publisher name:
# "publisher": "your-publisher-name"
```

### Step 2: Create Publisher Account

1. Go to https://marketplace.visualstudio.com/manage
2. Sign in with Microsoft account
3. Click "Create Publisher"
4. Choose a unique publisher ID (e.g., `amariah-ak`)
5. Fill in details

### Step 3: Get Personal Access Token

1. Go to https://dev.azure.com
2. Click User Settings (top right) → Personal Access Tokens
3. Click "+ New Token"
4. Name: "VS Code Extension Publishing"
5. Organization: "All accessible organizations"
6. Scopes: Select "Marketplace" → Check "Manage"
7. Click "Create"
8. **Copy the token!** (You won't see it again)

### Step 4: Login with vsce

```bash
# Install vsce if you haven't
npm install -g vsce

# Login with your publisher name
vsce login your-publisher-name

# Paste the token when prompted
```

### Step 5: Update Extension Metadata

Edit `vscode-extension/package.json`:

```json
{
  "name": "commit-checker",
  "displayName": "Commit Checker",
  "description": "AI-powered commit mentor with streaks, analytics, and wisdom",
  "version": "0.8.5",
  "publisher": "your-publisher-name",
  "icon": "media/logo.png",  // Make sure logo.png exists!
  "repository": {
    "type": "git",
    "url": "https://github.com/AmariahAK/commit-checker"
  },
  // ... rest of config
}
```

### Step 6: Publish!

```bash
cd vscode-extension

# First time publish
vsce publish

# Or specify version
vsce publish 0.8.5

# Or just patch/minor/major
vsce publish patch
```

**Publishing takes 5-10 minutes to appear in marketplace.**

### Step 7: Find Your Extension

Visit: https://marketplace.visualstudio.com/items?itemName=your-publisher-name.commit-checker

Users can now install via:
- VS Code UI (search "Commit Checker")
- Command line: `code --install-extension your-publisher-name.commit-checker`

---

## Recommended Flow

1. **First**: Test locally (Option 1)
2. **Then**: Push to GitHub
3. **Finally**: Publish to marketplace (Option 2)

**Why this order?**
- Test locally to fix bugs
- Push to GitHub for version control
- Publish when everything works perfectly

---

## Updating Your Extension

```bash
# Make changes to your code
# Update version in package.json

# Then republish
vsce publish
```

---

## Important Files Checklist

Before publishing, make sure you have:

- ✅ `media/logo.png` - Extension icon (128x128px recommended)
- ✅ `README.md` - Extension description
- ✅ `CHANGELOG.md` - Version history
- ✅ `LICENSE` - License file
- ✅ `.vscodeignore` - Files to exclude from package

---

## Logo Info

**Your logo locations**:
- CLI: `image/logo.png`
- VS Code: `vscode-extension/media/logo.png`

**Both exist!** The VS Code extension uses the one in `vscode-extension/media/`.

To use in extension, make sure `package.json` has:
```json
"icon": "media/logo.png"
```

---

## Troubleshooting

### "Publisher not found"
→ Create publisher account first (Step 2)

### "Icon not found"
→ Make sure `vscode-extension/media/logo.png` exists
→ Update path in `package.json` under `"icon"`

### "vsce: command not found"
→ Install: `npm install -g vsce`

### "Invalid token"
→ Regenerate token at dev.azure.com
→ Make sure "Marketplace: Manage" scope is selected

---

## Best Practices

1. **Test locally first** - Always test `.vsix` before publishing
2. **Semantic versioning** - Use 0.8.5, 0.8.6, 0.9.0, etc.
3. **Good README** - Clear description, screenshots, features
4. **Changelog** - Document changes between versions
5. **Keywords** - Add to package.json for discoverability:
   ```json
   "keywords": ["git", "commit", "productivity", "ai", "streak"]
   ```

---

## Quick Reference

```bash
# Package locally
npx vsce package

# Install locally
code --install-extension commit-checker-0.8.5.vsix

# Publish
vsce publish

# Update version and publish
vsce publish minor  # 0.8.5 → 0.9.0
vsce publish patch  # 0.8.5 → 0.8.6
vsce publish major  # 0.8.5 → 1.0.0
```

---

**Ready to publish!** 🚀

Your extension will appear at:
`https://marketplace.visualstudio.com/items?itemName=YOUR-PUBLISHER.commit-checker`
