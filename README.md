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
- 📦 Installable globally with `pip install` or `curl | bash`  
- 🔔 **Self-updating** from GitHub  
- 💖 Built-in `--support` option to tip the creator  

---

## 🧪 Quick Install

### 🌀 One-liner install:
```bash
curl -s https://raw.githubusercontent.com/AmariahAK/commit-checker/main/install.sh | bash
or using wget:

bash
Copy
Edit
wget -qO- https://raw.githubusercontent.com/AmariahAK/commit-checker/main/install.sh | bash
🧠 First-Time Setup
On your first run, the tool will ask:

👤 GitHub username

🔑 GitHub token (optional – for private repos)

📁 Local dev folder (e.g. ~/Documents/Github)

Then it remembers forever (until you run --setup again).
And yep — it’ll automatically run each time you launch a terminal 💻

🖥️ Usage
Just type:

bash
Copy
Edit
commit-checker
You’ll get a daily summary:

bash
Copy
Edit
🌐 GitHub: @AmariahAK
✅ AmariahAK/commit-checker — 2 commit(s)

🗂️ Scanning local path: /Users/amariah/Documents/Github
📁 project-1/
✅ 8a3c12 Initial commit
✅ 9b4e23 Added support flag
🎛️ CLI Flags
Flag	Description
--setup	Re-run onboarding config
--support	Show donation link to support dev
--silent	Minimal output (clean log mode)
--nocolor	Disable emojis and colors in output
--check-only	Run check without startup actions
--update	Manually check for new GitHub version

💖 Support This Project
If this tool helps you stay on track, show some love 💚

Donate via PayPal:
📬 amariah.abish@gmail.com

Even small support helps keep the streak alive for devs worldwide 🌍

👨🏽‍💻 Built By
Amariah Kamau
📂 GitHub: @AmariahAK
🌐 Portfolio: https://portfolio-pied-five-61.vercel.app

📄 License
Licensed under the MIT License(LICENSE).

Please give visible credit if you fork or remix:

Built by Amariah – https://github.com/AmariahAK

Suggestions and PRs are always welcome 💬