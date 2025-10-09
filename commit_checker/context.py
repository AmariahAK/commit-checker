import subprocess
import os
import json
import re
from datetime import datetime

CONTEXT_CACHE_FILE = os.path.expanduser("~/.commit_checker_cache/context.json")

def get_cache_dir():
    cache_dir = os.path.expanduser("~/.commit_checker_cache")
    os.makedirs(cache_dir, exist_ok=True)
    return cache_dir

def run_git_command(cmd, cwd=None):
    try:
        if cwd is None:
            cwd = os.getcwd()
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        return None

def get_staged_files(repo_path=None):
    output = run_git_command(['git', 'diff', '--name-only', '--staged'], cwd=repo_path)
    if output:
        return [f for f in output.split('\n') if f.strip()]
    return []

def get_diff_stats(repo_path=None):
    output = run_git_command(['git', 'diff', '--stat', '--staged'], cwd=repo_path)
    return output if output else ""

def get_diff_context(repo_path=None, context_lines=3):
    output = run_git_command(['git', 'diff', f'-U{context_lines}', '--staged'], cwd=repo_path)
    return output if output else ""

def parse_diff_stats(stats_output):
    files_changed = []
    pattern = r'^\s*(.+?)\s+\|\s+(\d+)\s+([+\-]+)'
    
    for line in stats_output.split('\n'):
        match = re.match(pattern, line.strip())
        if match:
            filename = match.group(1).strip()
            changes = match.group(2).strip()
            markers = match.group(3).strip()
            
            additions = markers.count('+')
            deletions = markers.count('-')
            
            files_changed.append({
                'file': filename,
                'changes': int(changes),
                'additions': additions,
                'deletions': deletions
            })
    
    return files_changed

def extract_commit_context(repo_path=None):
    try:
        staged_files = get_staged_files(repo_path)
        
        if not staged_files:
            return {
                'has_changes': False,
                'files': [],
                'summary': 'No staged changes found',
                'diff_preview': ''
            }
        
        diff_stats = get_diff_stats(repo_path)
        diff_context = get_diff_context(repo_path, context_lines=3)
        
        parsed_files = parse_diff_stats(diff_stats)
        
        total_additions = sum(f.get('additions', 0) for f in parsed_files)
        total_deletions = sum(f.get('deletions', 0) for f in parsed_files)
        
        summary_parts = []
        for file_info in parsed_files:
            file_summary = f"{file_info['file']}"
            if file_info.get('additions', 0) > 0 or file_info.get('deletions', 0) > 0:
                file_summary += f" (+{file_info.get('additions', 0)}/-{file_info.get('deletions', 0)})"
            summary_parts.append(file_summary)
        
        summary = f"Files changed: {', '.join(summary_parts[:5])}"
        if len(summary_parts) > 5:
            summary += f" (and {len(summary_parts) - 5} more)"
        
        context_data = {
            'has_changes': True,
            'files': staged_files,
            'file_details': parsed_files,
            'total_files': len(staged_files),
            'total_additions': total_additions,
            'total_deletions': total_deletions,
            'summary': summary,
            'diff_preview': diff_context[:1000],
            'timestamp': datetime.now().isoformat()
        }
        
        save_context_to_cache(context_data)
        
        return context_data
    
    except Exception as e:
        return {
            'has_changes': False,
            'files': [],
            'summary': f'Error extracting context: {str(e)}',
            'diff_preview': ''
        }

def save_context_to_cache(context_data):
    try:
        get_cache_dir()
        with open(CONTEXT_CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(context_data, f, indent=2)
    except Exception:
        pass

def load_cached_context():
    try:
        if os.path.exists(CONTEXT_CACHE_FILE):
            with open(CONTEXT_CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return None

def format_context_summary(context, emoji_mode=True):
    if not context or not context.get('has_changes'):
        return "No staged changes to analyze"
    
    icon = "📝" if emoji_mode else "*"
    files_icon = "📁" if emoji_mode else "-"
    
    lines = []
    lines.append(f"{icon} Commit Context:")
    lines.append(f"  {files_icon} {context['total_files']} file(s) changed")
    lines.append(f"  +{context['total_additions']} additions, -{context['total_deletions']} deletions")
    
    if context.get('file_details'):
        lines.append(f"  Files:")
        for file_info in context['file_details'][:3]:
            lines.append(f"    - {file_info['file']}")
    
    return '\n'.join(lines)

def get_commit_keywords(context):
    if not context or not context.get('has_changes'):
        return []
    
    keywords = []
    
    for file_path in context.get('files', []):
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext in ['.py']:
            keywords.append('python')
        elif ext in ['.js', '.jsx']:
            keywords.append('javascript')
        elif ext in ['.ts', '.tsx']:
            keywords.append('typescript')
        elif ext in ['.go']:
            keywords.append('go')
        elif ext in ['.rs']:
            keywords.append('rust')
        elif ext in ['.java']:
            keywords.append('java')
        elif ext in ['.cpp', '.cc', '.cxx', '.h', '.hpp']:
            keywords.append('cpp')
        
        if 'test' in file_path.lower() or 'spec' in file_path.lower():
            keywords.append('test')
        if 'doc' in file_path.lower() or 'readme' in file_path.lower():
            keywords.append('docs')
    
    return list(set(keywords))

def suggest_conventional_commit_type(context):
    if not context or not context.get('has_changes'):
        return None
    
    files = context.get('files', [])
    additions = context.get('total_additions', 0)
    deletions = context.get('total_deletions', 0)
    
    test_files = any('test' in f.lower() or 'spec' in f.lower() for f in files)
    doc_files = any('doc' in f.lower() or 'readme' in f.lower() or '.md' in f.lower() for f in files)
    config_files = any(f.endswith(('.json', '.yaml', '.yml', '.toml', '.ini', '.config')) for f in files)
    
    if test_files and len(files) <= 2:
        return 'test'
    if doc_files and len(files) <= 2:
        return 'docs'
    if config_files and additions < 10:
        return 'chore'
    if deletions > additions * 2:
        return 'refactor'
    if additions > 50 and len(files) > 3:
        return 'feat'
    if additions < 20 and len(files) <= 2:
        return 'fix'
    
    return 'feat'
