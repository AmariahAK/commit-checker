# 🛠️ Developer Instructions – Commit Checker Upgrade Plan

This document lists the features to implement as part of the next version of `commit-checker`.

👉 These upgrades **do NOT require GitHub API or SSH keys**. Everything is fully local and CLI-based.

---

## ✅ 1. Repo Auto-Detection + Scan

**Goal:** Detect all Git repositories inside a root folder and scan their commit activity.

### Tasks:
- Add `"repo_folder"` to `config.json`
- On `--scan`:
  - Recursively search for folders with `.git/`
  - Add to list of tracked repos
  - For each repo:
    - Count total commits
    - Count today’s commits
    - Get date of last commit

### Output example:
📁 Scanned 6 repos:

commit-checker → ✅ 2 today | 🧮 41 total | 🕒 Jul 18

blog-api → ❌ 0 today | 🧮 89 total | 🕒 Jul 17

markdown
Copy
Edit

---

## ✅ 2. `--most-active` Flag

**Goal:** Show which local repo had the most commits for a given time frame.

### Supported options:
- `--most-active --day`
- `--most-active --week`
- `--most-active --month`

### Tasks:
- Use `git log` with `--since=...` on all repos from the scan
- Return the one with the highest commit count

### Output example:
🔥 Most active repo this week:
📁 praxia → 12 commits
📅 Last activity: Jul 18

yaml
Copy
Edit

---

## ✅ 3. `--repos-summary` (or auto-run after `--scan`)

**Goal:** Show a full summary of local repo commit stats.

### Tasks:
- Loop through scanned repos
- Display:
  - Commits today
  - Total commits
  - Last commit date

### Output:
🧾 Repo Summary:
📁 commit-checker → ✅ 2 today | 🧮 41 total | 🕒 Jul 18
📁 praxia → ✅ 4 today | 🧮 163 total | 🕒 Jul 18
📁 playground → ❌ 0 today | 🧮 12 total | 🕒 Jul 10

yaml
Copy
Edit

---

## ✅ 4. Emoji Output Mode

**Goal:** Stylize CLI messages using emoji (optional).

### Tasks:
- Add `"output": "emoji"` to `config.json`
- If enabled:
  - Use 🟢/🔴 for commit status
  - Use ✅/❌ for flags

---

## ✅ 5. Config File Support

**Goal:** Store persistent settings like repo folder and output style.

### Config path:
`~/.commit-checker/config.json`

### Sample structure:
```json
{
  "default_username": "AmariahAK",
  "repo_folder": "/Users/amariah/Projects",
  "output": "emoji"
}
✅ 6. Fix --uninstall Flag
Goal: Fully remove all traces of the CLI tool.

Tasks:
Delete binary from /usr/local/bin/commit-checker

Delete config folder ~/.commit-checker

Print:

sql
Copy
Edit
✅ Commit Checker has been fully removed.
Add --force to bypass confirmation prompt

🔄 Future Features (Don’t build yet – just list)
--top-repos: Fetch user's most starred/forked repos (requires token)

--trending: Fetch trending GitHub repos (API or scrape)

VS Code extension integration

Shields.io badge for “Committed Today”

--weekly streak visualization (✅✅❌✅...)

📅 Priority Order for Implementation
--scan + auto repo detection

Config file support

--repos-summary

--most-active

Emoji output

Fix --uninstall

📌 All work must remain offline-capable and zero-dependency for now (no API, no pip/brew).
CLI should remain globally executable after install via curl | bash.

Built by Amariah – powered by vibes and streaks 💚

yaml
Copy
Edit
