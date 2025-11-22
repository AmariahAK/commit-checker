"""Diff analysis and explanation module for commit-checker.

Provides:
- Git diff parsing and categorization
- Human-friendly explanations of changes
- Context extraction (functions, classes changed)
- Simple summaries for AI models
"""
import os
import re
import subprocess
from typing import Dict, List, Tuple, Optional, Any


def run_git(command: List[str], cwd: str) -> Optional[str]:
    """Run git command safely."""
    try:
        result = subprocess.check_output(
            ["git"] + command,
            cwd=cwd,
            stderr=subprocess.DEVNULL,
            text=True
        )
        return result.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def parse_diff(repo_path: str, staged_only: bool = True) -> Dict[str, Any]:
    """Parse git diff and categorize changes.
    
    Args:
        repo_path: Path to git repository
        staged_only: If True, only parse staged changes (default)
        
    Returns:
        Dict containing added, modified, deleted files and summary stats
    """
    # Get the diff
    if staged_only:
        diff_output = run_git(["diff", "--cached", "--numstat"], repo_path)
        diff_text = run_git(["diff", "--cached"], repo_path)
    else:
        diff_output = run_git(["diff", "--numstat"], repo_path)
        diff_text = run_git(["diff"], repo_path)

    
    if not diff_output:
        return {
            "added": [],
            "modified": [],
            "deleted": [],
            "summary": {
                "files_changed": 0,
                "insertions": 0,
                "deletions": 0,
                "total_changes": 0
            },
            "context": [],
            "diff_text": ""
        }
    
    added_files = []
    modified_files = []
    deleted_files = []
    total_insertions = 0
    total_deletions = 0
    
    # Parse numstat output
    for line in diff_output.split('\n'):
        if not line.strip():
            continue
        
        parts = line.split('\t')
        if len(parts) < 3:
            continue
        
        insertions, deletions, filename = parts[0], parts[1], parts[2]
        
        # Check if file is binary
        if insertions == '-' or deletions == '-':
            # Binary file
            insertions = 0
            deletions = 0
        else:
            insertions = int(insertions)
            deletions = int(deletions)
            total_insertions += insertions
            total_deletions += deletions
        
        # Categorize change type
        if insertions > 0 and deletions == 0:
            # Likely a new file
            added_files.append({
                "file": filename,
                "insertions": insertions
            })
        elif insertions == 0 and deletions > 0:
            # Likely deleted file
            deleted_files.append({
                "file": filename,
                "deletions": deletions
            })
        else:
            # Modified file
            modified_files.append({
                "file": filename,
                "insertions": insertions,
                "deletions": deletions
            })
    
    # Extract context from diff
    context = extract_context_from_diff(diff_text or "")
    
    return {
        "added": added_files,
        "modified": modified_files,
        "deleted": deleted_files,
        "summary": {
            "files_changed": len(added_files) + len(modified_files) + len(deleted_files),
            "insertions": total_insertions,
            "deletions": total_deletions,
            "total_changes": total_insertions + total_deletions
        },
        "context": context,
        "diff_text": diff_text or ""
    }


def extract_context_from_diff(diff_text: str) -> List[Dict[str, str]]:
    """Extract context like function/class names from diff.
    
    Args:
        diff_text: Raw git diff output
        
    Returns:
        List of context items with type and name
    """
    context = []
    current_file = None
    
    # Patterns to match functions and classes
    patterns = {
        "python_function": r"def\s+(\w+)\s*\(",
        "python_class": r"class\s+(\w+)",
        "js_function": r"function\s+(\w+)\s*\(",
        "js_class": r"class\s+(\w+)",
        "js_arrow": r"const\s+(\w+)\s*=\s*\(",
        "java_method": r"(public|private|protected).*\s+(\w+)\s*\(",
        "c_function": r"\w+\s+(\w+)\s*\([^)]*\)\s*\{",
    }
    
    lines = diff_text.split('\n')
    for line in lines:
        # Track current file
        if line.startswith('+++'):
            current_file = line.split('+++')[1].strip().lstrip('b/')
            continue
        
        # Look for added/modified lines with function/class definitions
        if line.startswith('+') and current_file:
            line_content = line[1:].strip()
            
            for pattern_name, pattern in patterns.items():
                match = re.search(pattern, line_content)
                if match:
                    name = match.group(1) if len(match.groups()) == 1 else match.group(2)
                    context.append({
                        "file": current_file,
                        "type": pattern_name.split('_')[1],  # function, class, etc.
                        "name": name,
                        "language": pattern_name.split('_')[0]
                    })
                    break
    
    return context


def explain_diff_simple(diff_data: Dict[str, Any]) -> str:
    """Generate simple, human-friendly explanation of changes.
    
    Args:
        diff_data: Output from parse_diff()
        
    Returns:
        Human-readable explanation string
    """
    explanations = []
    summary = diff_data["summary"]
    
    # Overall summary
    if summary["files_changed"] == 0:
        return "No changes detected"
    
    explanations.append(f"**{summary['files_changed']} file(s) changed**")
    explanations.append(f"  +{summary['insertions']} additions, -{summary['deletions']} deletions")
    explanations.append("")
    
    # Added files
    if diff_data["added"]:
        explanations.append("📄 **New files:**")
        for item in diff_data["added"][:5]:  # Limit to 5
            explanations.append(f"  • {item['file']} (+{item['insertions']} lines)")
        if len(diff_data["added"]) > 5:
            explanations.append(f"  ... and {len(diff_data['added']) - 5} more")
        explanations.append("")
    
    # Modified files
    if diff_data["modified"]:
        explanations.append("✏️  **Modified files:**")
        for item in diff_data["modified"][:5]:
            explanations.append(
                f"  • {item['file']} "
                f"(+{item['insertions']} / -{item['deletions']})"
            )
        if len(diff_data["modified"]) > 5:
            explanations.append(f"  ... and {len(diff_data['modified']) - 5} more")
        explanations.append("")
    
    # Deleted files
    if diff_data["deleted"]:
        explanations.append("🗑️  **Deleted files:**")
        for item in diff_data["deleted"][:5]:
            explanations.append(f"  • {item['file']} (-{item['deletions']} lines)")
        if len(diff_data["deleted"]) > 5:
            explanations.append(f"  ... and {len(diff_data['deleted']) - 5} more")
        explanations.append("")
    
    # Context (functions/classes changed)
    if diff_data["context"]:
        explanations.append("🔧 **Changes in:**")
        seen = set()
        for item in diff_data["context"][:10]:  # Limit to 10
            key = f"{item['file']}:{item['name']}"
            if key not in seen:
                explanations.append(
                    f"  • {item['type']} `{item['name']}` in {item['file']}"
                )
                seen.add(key)
        if len(diff_data["context"]) > 10:
            explanations.append(f"  ... and more")
    
    return '\n'.join(explanations)


def get_diff_for_ai(diff_data: Dict[str, Any]) -> str:
    """Format diff data for AI model consumption.
    
    Provides concise summary optimized for token efficiency.
    
    Args:
        diff_data: Output from parse_diff()
        
    Returns:
        AI-optimized diff summary
    """
    parts = []
    
    # Summary
    s = diff_data["summary"]
    parts.append(
        f"Changes: {s['files_changed']} files, "
        f"+{s['insertions']}/-{s['deletions']} lines"
    )
    
    # Files
    if diff_data["added"]:
        files = [f['file'] for f in diff_data["added"][:3]]
        parts.append(f"Added: {', '.join(files)}")
    
    if diff_data["modified"]:
        files = [f['file'] for f in diff_data["modified"][:3]]
        parts.append(f"Modified: {', '.join(files)}")
    
    if diff_data["deleted"]:
        files = [f['file'] for f in diff_data["deleted"][:3]]
        parts.append(f"Deleted: {', '.join(files)}")
    
    # Context
    if diff_data["context"]:
        contexts = [f"{c['name']}" for c in diff_data["context"][:5]]
        parts.append(f"Changed: {', '.join(contexts)}")
    
    return " | ".join(parts)


def analyze_change_type(diff_data: Dict[str, Any]) -> str:
    """Determine the type of change (feat, fix, refactor, etc.).
    
    Args:
        diff_data: Output from parse_diff()
        
    Returns:
        Conventional commit type
    """
    summary = diff_data["summary"]
    
    # If only new files, likely a feature
    if diff_data["added"] and not diff_data["modified"] and not diff_data["deleted"]:
        return "feat"
    
    # If only deletions, likely a cleanup/chore
    if diff_data["deleted"] and not diff_data["added"] and not diff_data["modified"]:
        return "chore"
    
    # If test files changed
    test_patterns = ["test", "spec", "__tests__"]
    has_tests = any(
        any(pattern in f["file"].lower() for pattern in test_patterns)
        for f in diff_data["added"] + diff_data["modified"]
    )
    if has_tests:
        return "test"
    
    # If docs changed
    doc_patterns = ["readme", "doc", ".md", "contributing"]
    has_docs = any(
        any(pattern in f["file"].lower() for pattern in doc_patterns)
        for f in diff_data["added"] + diff_data["modified"]
    )
    if has_docs:
        return "docs"
    
    # If mostly modifications with few additions, likely a fix
    if diff_data["modified"] and summary["deletions"] > summary["insertions"]:
        return "fix"
    
    # If major additions, likely a feature
    if summary["insertions"] > summary["deletions"] * 2:
        return "feat"
    
    # Default to refactor
    return "refactor"


if __name__ == "__main__":
    # Test with commit-checker itself
    import sys
    
    repo_path = "/Users/amariah/Documents/GitHub/commit-checker"
    
    print("🔍 Analyzing staged changes...")
    print()
    
    diff_data = parse_diff(repo_path, staged_only=True)
    
    if diff_data["summary"]["files_changed"] == 0:
        print("No staged changes found.")
        sys.exit(0)
    
    # Show simple explanation
    print(explain_diff_simple(diff_data))
    print()
    
    # Show AI summary
    print("📝 AI Summary:")
    print(get_diff_for_ai(diff_data))
    print()
    
    # Show suggested type
    change_type = analyze_change_type(diff_data)
    print(f"💡 Suggested type: `{change_type}:`")
