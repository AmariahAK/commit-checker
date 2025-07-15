# 🟢 commit-checker

Keep your GitHub streak green with a lightweight, cross-platform CLI tool.  
Automatically checks your daily commits — both **public (GitHub)** and **local (SSH/git)** — and reminds you to stay consistent 🧠⚙️

---

## ✨ Features

- ✅ Tracks **GitHub public & private** commits  
- 🗂️ Checks **local git repos** for daily activity  
- 💾 One-time setup (GitHub + dev folder)  
- 🛠️ Auto-installs dependencies  
- ⚙️ Auto-runs in terminal on startup  
- 🌍 Cross-platform (macOS, Linux, Windows PowerShell)  
- 📦 Installable globally with one-liner script  
- 🔔 **Self-updating** from GitHub  
- 💖 Built-in `--support` option to tip the creator  

---

## 🧪 Quick Install

### 🌀 One-liner install:
```bash
curl -s https://raw.githubusercontent.com/AmariahAK/commit-checker/main/install.sh | bash
```
or using wget:

```bash
wget -qO- https://raw.githubusercontent.com/AmariahAK/commit-checker/main/install.sh | bash
```

> **📦 pip install:** Coming soon! We're working on PyPI package distribution for easier installation.

---

## 🧠 First-Time Setup
On your first run, the tool will ask:

👤 GitHub username

🔑 GitHub token (optional – for private repos)

📁 Local dev folder (e.g. ~/Documents/Github)

Then it remembers forever (until you run --setup again).
And yep — it'll automatically run each time you launch a terminal 💻

---

## 🖥️ Usage
Just type:

```bash
commit-checker
```
You'll get a daily summary:

```bash
🌐 GitHub: @AmariahAK
✅ AmariahAK/commit-checker — 2 commit(s)

🗂️ Scanning local path: /Users/amariah/Documents/Github
📁 project-1/
✅ 8a3c12 Initial commit
✅ 9b4e23 Added support flag
```

---

## 🗑️ Uninstalling

To completely remove commit-checker from your system:

```bash
commit-checker --uninstall
```

This will:
- ✅ Remove the Python package via pip
- ✅ Delete all configuration files (`~/.commit-checker/`)
- ✅ Remove auto-run entries from shell startup files (`.bashrc`, `.zshrc`, etc.)
- ✅ Clean up all traces of the extension

You'll be prompted to confirm before proceeding. After uninstalling, you may need to restart your terminal or run `source ~/.bashrc` (or `~/.zshrc`) to fully remove the auto-run behavior.

---

## 🎛️ CLI Flags
| Flag | Description |
|------|-------------|
| `--setup` | Re-run onboarding config |
| `--uninstall` | Completely remove commit-checker from your system |
| `--support` | Show donation link to support dev |
| `--silent` | Minimal output (clean log mode) |
| `--nocolor` | Disable emojis and colors in output |
| `--check-only` | Run check without startup actions |
| `--update` | Manually check for new GitHub version |

---

## 🏗️ Project Structure

```
commit-checker/
├── 📄 LICENSE.md                 # MIT License
├── 📖 README.md                  # This file
├── 📦 setup.py                   # Python package setup
├── 📋 requirements.txt           # Python dependencies
├── 🚀 install.sh                 # One-liner installation script
└── commit_checker/               # Main package directory
    ├── 🔧 __init__.py            # Package initialization
    ├── 🎯 cli.py                 # Command-line interface
    ├── ✅ checker.py             # Core commit checking logic
    ├── ⚙️ config.py              # Configuration management
    ├── 🔄 updater.py             # Auto-update functionality
    ├── 🗑️ uninstaller.py         # Complete uninstall functionality
    └── 🚀 bootstrap.py           # Initial setup and bootstrapping
```

---

## 💖 Support This Project
If this tool helps you stay on track, show some love 💚

**Donate via PayPal:**  
📬 amariah.abish@gmail.com

Even small support helps keep the streak alive for devs worldwide 🌍

---

## 👨🏽‍💻 Built By
**Amariah Kamau**  
📂 GitHub: [@AmariahAK](https://github.com/AmariahAK)  
🌐 Portfolio: https://portfolio-pied-five-61.vercel.app

---

## 📄 License
Licensed under the [MIT License](LICENSE.md).

Please give visible credit if you fork or remix:
> Built by Amariah – https://github.com/AmariahAK

Suggestions and PRs are always welcome 💬

---

## 📚 Quick Navigation
- 📖 [README.md](README.md) - You are here
- 📄 [LICENSE.md](LICENSE.md) - MIT License details
- 📦 [setup.py](setup.py) - Python package configuration
- 📋 [requirements.txt](requirements.txt) - Dependencies list
- 🚀 [install.sh](install.sh) - Installation script
- 🎯 [commit_checker/cli.py](commit_checker/cli.py) - CLI interface
- ✅ [commit_checker/checker.py](commit_checker/checker.py) - Core logic
- ⚙️ [commit_checker/config.py](commit_checker/config.py) - Configuration
- 🔄 [commit_checker/updater.py](commit_checker/updater.py) - Auto-updater
- 🗑️ [commit_checker/uninstaller.py](commit_checker/uninstaller.py) - Uninstall functionality
- 🚀 [commit_checker/bootstrap.py](commit_checker/bootstrap.py) - Setup logic