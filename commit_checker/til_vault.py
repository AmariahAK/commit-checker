import os
import json
import subprocess
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple


DEFAULT_VAULT_PATH = os.path.expanduser("~/.commit-checker/tils/")
TEMPLATES_PATH = os.path.expanduser("~/.commit-checker/templates/")


def ensure_vault_directories():
    """Ensure TIL vault and templates directories exist"""
    os.makedirs(DEFAULT_VAULT_PATH, exist_ok=True)
    os.makedirs(TEMPLATES_PATH, exist_ok=True)


def get_vault_path(config=None):
    """Get TIL vault path from config or use default"""
    if config and config.get('vault_path'):
        return os.path.expanduser(config['vault_path'])
    return DEFAULT_VAULT_PATH


def create_til_from_template(title: str, template_name: str, config=None) -> Tuple[bool, str]:
    """Create a new TIL entry from a template"""
    ensure_vault_directories()
    
    template_path = os.path.join(TEMPLATES_PATH, f"{template_name}.md")
    if not os.path.exists(template_path):
        return False, f"Template '{template_name}' not found. Available templates: {list_templates()}"
    
    # Read template
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
    except Exception as e:
        return False, f"Failed to read template: {e}"
    
    # Generate filename
    date_str = datetime.now().strftime("%Y-%m-%d")
    safe_title = re.sub(r'[^\w\-_\.]', '-', title.lower())
    filename = f"{date_str}-{safe_title}.md"
    
    vault_path = get_vault_path(config)
    file_path = os.path.join(vault_path, filename)
    
    # Replace template variables
    content = template_content.replace("{{title}}", title)
    content = content.replace("{{date}}", datetime.now().strftime("%B %d, %Y"))
    content = content.replace("{{timestamp}}", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, f"TIL created: {file_path}"
    except Exception as e:
        return False, f"Failed to create TIL: {e}"


def add_til_to_vault(title: str, content: str, tags: List[str] = None, config=None) -> Tuple[bool, str]:
    """Add a new TIL entry to the vault"""
    ensure_vault_directories()
    
    # Generate filename
    date_str = datetime.now().strftime("%Y-%m-%d")
    safe_title = re.sub(r'[^\w\-_\.]', '-', title.lower())
    filename = f"{date_str}-{safe_title}.md"
    
    vault_path = get_vault_path(config)
    file_path = os.path.join(vault_path, filename)
    
    # Build markdown content
    md_content = f"# {title}\n\n"
    md_content += f"**Date:** {datetime.now().strftime('%B %d, %Y')}\n\n"
    
    if tags:
        tag_string = " ".join([f"#{tag}" for tag in tags])
        md_content += f"**Tags:** {tag_string}\n\n"
    
    md_content += "## Content\n\n"
    md_content += content + "\n"
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        return True, f"TIL added to vault: {file_path}"
    except Exception as e:
        return False, f"Failed to add TIL to vault: {e}"


def list_templates() -> List[str]:
    """List available TIL templates"""
    ensure_vault_directories()
    
    templates = []
    if os.path.exists(TEMPLATES_PATH):
        for file in os.listdir(TEMPLATES_PATH):
            if file.endswith('.md'):
                templates.append(file[:-3])  # Remove .md extension
    
    return sorted(templates)


def search_til_vault(query: str, config=None) -> List[Dict]:
    """Fuzzy search TIL vault entries"""
    vault_path = get_vault_path(config)
    
    if not os.path.exists(vault_path):
        return []
    
    results = []
    query_lower = query.lower()
    
    for filename in os.listdir(vault_path):
        if not filename.endswith('.md'):
            continue
        
        file_path = os.path.join(vault_path, filename)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Score based on matches in title, tags, and content
            score = 0
            matching_lines = []
            
            lines = content.split('\n')
            for i, line in enumerate(lines):
                line_lower = line.lower()
                if query_lower in line_lower:
                    # Higher score for title matches
                    if line.startswith('# '):
                        score += 10
                    # Medium score for tag matches
                    elif 'tags:' in line_lower or line.strip().startswith('#'):
                        score += 5
                    # Lower score for content matches
                    else:
                        score += 1
                    
                    # Highlight the matching part
                    highlighted_line = highlight_match(line, query)
                    matching_lines.append((i + 1, highlighted_line))
            
            if score > 0:
                # Extract title
                title = "Unknown"
                for line in lines:
                    if line.startswith('# '):
                        title = line[2:].strip()
                        break
                
                # Extract date from filename
                date_match = re.match(r'(\d{4}-\d{2}-\d{2})', filename)
                date = date_match.group(1) if date_match else "Unknown"
                
                results.append({
                    'filename': filename,
                    'title': title,
                    'date': date,
                    'score': score,
                    'matching_lines': matching_lines[:5]  # Limit to 5 matches
                })
        
        except Exception:
            continue
    
    # Sort by score (descending)
    results.sort(key=lambda x: x['score'], reverse=True)
    return results


def highlight_match(text: str, query: str) -> str:
    """Highlight matching text with ANSI colors"""
    # Simple highlighting - replace with colored text
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    return pattern.sub(f"\033[93m{query}\033[0m", text)


def display_search_results(results: List[Dict]) -> str:
    """Display TIL search results"""
    if not results:
        return "🔍 No TIL entries found matching your query."
    
    output = []
    output.append(f"🔍 Found {len(results)} TIL entries:")
    output.append("=" * 50)
    output.append("")
    
    for i, result in enumerate(results[:10], 1):  # Show top 10
        output.append(f"{i}. 📝 {result['title']}")
        output.append(f"   📅 {result['date']} | Score: {result['score']}")
        
        # Show matching lines
        for line_num, line in result['matching_lines']:
            output.append(f"   L{line_num}: {line.strip()}")
        
        output.append("")
    
    return "\n".join(output)


def generate_til_from_diff(repo_path: str, commit_hash: str = None) -> Tuple[bool, str]:
    """Generate TIL entry from git diff (no AI, just structured info)"""
    try:
        # If no commit hash provided, use the latest commit
        if not commit_hash:
            commit_hash = subprocess.check_output([
                "git", "--git-dir", os.path.join(repo_path, ".git"),
                "--work-tree", repo_path,
                "rev-parse", "HEAD"
            ], stderr=subprocess.DEVNULL).decode("utf-8").strip()
        
        # Get commit info
        commit_info = subprocess.check_output([
            "git", "--git-dir", os.path.join(repo_path, ".git"),
            "--work-tree", repo_path,
            "show", "--format=%s%n%b", "--no-patch", commit_hash
        ], stderr=subprocess.DEVNULL).decode("utf-8").strip()
        
        # Get diff stats
        diff_stats = subprocess.check_output([
            "git", "--git-dir", os.path.join(repo_path, ".git"),
            "--work-tree", repo_path,
            "show", "--stat", "--format=", commit_hash
        ], stderr=subprocess.DEVNULL).decode("utf-8").strip()
        
        # Get modified files
        modified_files = subprocess.check_output([
            "git", "--git-dir", os.path.join(repo_path, ".git"),
            "--work-tree", repo_path,
            "show", "--name-only", "--format=", commit_hash
        ], stderr=subprocess.DEVNULL).decode("utf-8").strip().split('\n')
        
        # Parse diff for function names and changes
        diff_output = subprocess.check_output([
            "git", "--git-dir", os.path.join(repo_path, ".git"),
            "--work-tree", repo_path,
            "show", "--format=", commit_hash
        ], stderr=subprocess.DEVNULL).decode("utf-8")
        
        # Extract function names (basic parsing)
        functions_added = []
        functions_modified = []
        
        for line in diff_output.split('\n'):
            if line.startswith('+++'):
                continue
            elif line.startswith('+') and ('def ' in line or 'function ' in line or 'const ' in line):
                # Extract function name (basic)
                func_match = re.search(r'(def|function|const)\s+([a-zA-Z_][a-zA-Z0-9_]*)', line)
                if func_match:
                    functions_added.append(func_match.group(2))
        
        # Build TIL content
        repo_name = os.path.basename(repo_path)
        commit_lines = commit_info.split('\n')
        commit_title = commit_lines[0] if commit_lines else "Unknown commit"
        
        til_content = f"""# Code Changes: {commit_title}

**Repository:** {repo_name}
**Commit:** {commit_hash[:8]}
**Date:** {datetime.now().strftime('%B %d, %Y')}

## Summary
{commit_title}

## Files Modified
"""
        
        for file in modified_files:
            if file.strip():
                til_content += f"- `{file}`\n"
        
        if diff_stats:
            til_content += f"\n## Statistics\n```\n{diff_stats}\n```\n"
        
        if functions_added:
            til_content += f"\n## Functions Added/Modified\n"
            for func in functions_added:
                til_content += f"- `{func}()`\n"
        
        til_content += f"\n## What I Learned\n_TODO: Add your insights about this change_\n"
        
        return True, til_content
        
    except Exception as e:
        return False, f"Failed to generate TIL from diff: {e}"


def create_til_from_latest_commit(repo_paths: List[str], config=None) -> Tuple[bool, str]:
    """Create TIL from the latest commit in any of the repos"""
    if not repo_paths:
        return False, "No repository paths provided"
    
    latest_commit = None
    latest_repo = None
    latest_timestamp = 0
    
    # Find the most recent commit across all repos
    for path in repo_paths:
        if not path or not os.path.exists(path):
            continue
            
        for root, dirs, files in os.walk(path):
            if '.git' in dirs:
                try:
                    # Get latest commit timestamp
                    timestamp_output = subprocess.check_output([
                        "git", "--git-dir", os.path.join(root, ".git"),
                        "--work-tree", root,
                        "log", "-1", "--format=%ct"
                    ], stderr=subprocess.DEVNULL).decode("utf-8").strip()
                    
                    if timestamp_output:
                        timestamp = int(timestamp_output)
                        if timestamp > latest_timestamp:
                            latest_timestamp = timestamp
                            latest_repo = root
                            
                            # Get commit hash
                            latest_commit = subprocess.check_output([
                                "git", "--git-dir", os.path.join(root, ".git"),
                                "--work-tree", root,
                                "rev-parse", "HEAD"
                            ], stderr=subprocess.DEVNULL).decode("utf-8").strip()
                
                except Exception:
                    continue
                dirs.clear()
    
    if not latest_commit or not latest_repo:
        return False, "No recent commits found"
    
    # Generate TIL from the latest commit
    success, til_content = generate_til_from_diff(latest_repo, latest_commit)
    
    if success:
        # Save to vault
        repo_name = os.path.basename(latest_repo)
        title = f"Latest changes in {repo_name}"
        return add_til_to_vault(title, til_content, ["git", "code"], config)
    
    return False, til_content


def list_vault_entries(config=None, limit=20) -> List[Dict]:
    """List TIL vault entries"""
    vault_path = get_vault_path(config)
    
    if not os.path.exists(vault_path):
        return []
    
    entries = []
    
    for filename in os.listdir(vault_path):
        if not filename.endswith('.md'):
            continue
        
        file_path = os.path.join(vault_path, filename)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract title
            title = "Unknown"
            tags = []
            
            lines = content.split('\n')
            for line in lines:
                if line.startswith('# '):
                    title = line[2:].strip()
                elif 'tags:' in line.lower():
                    # Extract tags
                    tag_line = line.split(':', 1)[1] if ':' in line else line
                    tags = re.findall(r'#(\w+)', tag_line)
                
                if title != "Unknown" and tags:
                    break
            
            # Extract date from filename
            date_match = re.match(r'(\d{4}-\d{2}-\d{2})', filename)
            date = date_match.group(1) if date_match else "Unknown"
            
            entries.append({
                'filename': filename,
                'title': title,
                'date': date,
                'tags': tags,
                'file_path': file_path
            })
        
        except Exception:
            continue
    
    # Sort by date (newest first)
    entries.sort(key=lambda x: x['date'], reverse=True)
    return entries[:limit]


def display_vault_summary(config=None) -> str:
    """Display TIL vault summary"""
    vault_path = get_vault_path(config)
    
    if not os.path.exists(vault_path):
        return "📚 TIL Vault is empty. Add your first entry!"
    
    entries = list_vault_entries(config)
    
    if not entries:
        return "📚 TIL Vault is empty. Add your first entry!"
    
    output = []
    output.append("📚 TIL Vault Summary")
    output.append("=" * 50)
    output.append(f"📁 Location: {vault_path}")
    output.append(f"📄 Total entries: {len(entries)}")
    output.append("")
    
    # Show recent entries
    output.append("📝 Recent entries:")
    for entry in entries[:5]:
        tag_str = " ".join([f"#{tag}" for tag in entry['tags']]) if entry['tags'] else ""
        output.append(f"  • {entry['date']}: {entry['title']} {tag_str}")
    
    if len(entries) > 5:
        output.append(f"  ... and {len(entries) - 5} more")
    
    # Tag statistics
    all_tags = []
    for entry in entries:
        all_tags.extend(entry['tags'])
    
    if all_tags:
        from collections import Counter
        tag_counts = Counter(all_tags)
        output.append("")
        output.append("🏷️  Popular tags:")
        for tag, count in tag_counts.most_common(5):
            output.append(f"  #{tag} ({count})")
    
    return "\n".join(output)


def add_custom_template(name, structure):
    """Add a custom TIL template"""
    ensure_vault_directories()
    
    # Sanitize template name
    safe_name = re.sub(r'[^\w\-_]', '', name.lower())
    if not safe_name:
        return False, "Invalid template name. Use only letters, numbers, hyphens, and underscores."
    
    template_path = os.path.join(TEMPLATES_PATH, f"{safe_name}.md")
    
    # Replace placeholders in structure with proper template variables
    template_content = structure.replace('{title}', '{{title}}')
    template_content = template_content.replace('{date}', '{{date}}')
    template_content = template_content.replace('{timestamp}', '{{timestamp}}')
    
    # Add basic template structure if none provided
    if not template_content.startswith('#'):
        template_content = f"# {{{{title}}}}\n\n**Date:** {{{{date}}}}\n**Tags:** #{safe_name}\n\n{template_content}"
    
    try:
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(template_content)
        return True, f"Custom template '{safe_name}' added successfully"
    except Exception as e:
        return False, f"Failed to create template: {e}"


def create_default_templates():
    """Create default TIL templates"""
    ensure_vault_directories()
    
    templates = {
        "bugfix": """# {{title}}

**Date:** {{date}}
**Tags:** #bugfix #troubleshooting

## The Problem
Describe what wasn't working...

## The Solution
Explain how you fixed it...

## What I Learned
Key insights and takeaways...

## Code Changes
```
// Add relevant code snippets
```

## Resources
- [Link to documentation](url)
- [Stack Overflow post](url)
""",
        
        "feature": """# {{title}}

**Date:** {{date}}
**Tags:** #feature #development

## Overview
Brief description of the new feature...

## Implementation Details
How you built it...

## Challenges
What problems did you encounter...

## Learning Outcomes
What new skills or knowledge did you gain...

## Code Highlights
```
// Show the most interesting parts
```
""",
        
        "concept": """# {{title}}

**Date:** {{date}}
**Tags:** #concept #learning

## What is it?
Explain the concept in simple terms...

## Why is it important?
Context and relevance...

## How does it work?
Technical details...

## Example
```
// Practical example
```

## Further Reading
- [Resource 1](url)
- [Resource 2](url)
""",
        
        "tool": """# {{title}}

**Date:** {{date}}
**Tags:** #tool #productivity

## What is it?
Brief description of the tool...

## How to use it
Step-by-step instructions...

## Why it's useful
Benefits and use cases...

## Configuration
```bash
# Setup commands
```

## Tips and Tricks
- Tip 1
- Tip 2
- Tip 3
""",
        
        "algorithm": """# {{title}}

**Date:** {{date}}
**Tags:** #algorithm #datastructures

## Problem
What problem does this algorithm solve...

## Approach
High-level strategy...

## Implementation
```python
# Code implementation
def algorithm_name():
    pass
```

## Time Complexity
O(?)

## Space Complexity
O(?)

## When to use
Practical applications...
"""
    }
    
    created_count = 0
    for name, content in templates.items():
        template_path = os.path.join(TEMPLATES_PATH, f"{name}.md")
        if not os.path.exists(template_path):
            try:
                with open(template_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                created_count += 1
            except Exception:
                continue
    
    return created_count
