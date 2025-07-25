import os
import subprocess
import sys
from datetime import datetime


DEFAULT_TIL_PATH = os.path.expanduser("~/.commit-checker/til.md")


def get_til_path(config=None):
    """Get the TIL file path from config or use default"""
    if config and config.get('til_path'):
        return os.path.expanduser(config['til_path'])
    return DEFAULT_TIL_PATH


def ensure_til_file_exists(til_path):
    """Ensure the TIL file and its directory exist"""
    os.makedirs(os.path.dirname(til_path), exist_ok=True)
    if not os.path.exists(til_path):
        with open(til_path, 'w', encoding='utf-8') as f:
            f.write("# Today I Learned\n\n")


def get_today_header():
    """Get today's date header"""
    return datetime.now().strftime("## %B %d, %Y")


def add_til_entry(message, config=None, include_date=True, tag=None):
    """Add a new TIL entry to the file"""
    til_path = get_til_path(config)
    ensure_til_file_exists(til_path)
    
    try:
        # Read existing content
        with open(til_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Get today's header
        today_header = get_today_header()
        
        # Format the entry with optional tag
        if tag:
            entry_text = f"- {message} `#{tag}`"
        else:
            entry_text = f"- {message}"
        
        # Prepare the new entry
        if include_date:
            # Check if today's header already exists
            if today_header in content:
                # Add to existing date section
                lines = content.split('\n')
                header_index = -1
                for i, line in enumerate(lines):
                    if line.strip() == today_header:
                        header_index = i
                        break
                
                if header_index != -1:
                    # Find the next header or end of file
                    insert_index = len(lines)
                    for i in range(header_index + 1, len(lines)):
                        if lines[i].strip().startswith('## '):
                            insert_index = i
                            break
                    
                    # Insert the new entry
                    lines.insert(insert_index, entry_text)
                    if insert_index < len(lines) - 1:
                        lines.insert(insert_index + 1, "")
                    content = '\n'.join(lines)
                else:
                    # Fallback: append at the end
                    content += f"\n{today_header}\n{entry_text}\n"
            else:
                # Add new date section
                content += f"\n{today_header}\n{entry_text}\n"
        else:
            # No date mode - just append the entry
            content += f"{entry_text}\n"
        
        # Write back to file
        with open(til_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        tag_text = f" (tagged: {tag})" if tag else ""
        return True, f"✅ TIL entry added to {til_path}{tag_text}"
        
    except Exception as e:
        return False, f"❌ Failed to add TIL entry: {e}"


def view_til(config=None):
    """View the current TIL file"""
    til_path = get_til_path(config)
    
    if not os.path.exists(til_path):
        return False, "📝 No TIL entries found. Add your first entry with: commit-checker til \"Your learning\""
    
    try:
        with open(til_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if content.strip() == "# Today I Learned":
            return False, "📝 TIL file exists but is empty. Add your first entry with: commit-checker til \"Your learning\""
        
        return True, content
        
    except Exception as e:
        return False, f"❌ Failed to read TIL file: {e}"


def edit_til(config=None):
    """Open the TIL file in the default editor"""
    til_path = get_til_path(config)
    ensure_til_file_exists(til_path)
    
    # Get editor from environment or use fallback
    editor = os.environ.get('EDITOR', 'nano')
    
    try:
        subprocess.run([editor, til_path])
        return True, f"📝 Opened {til_path} in {editor}"
    except FileNotFoundError:
        # Try common editors as fallback
        fallback_editors = ['nano', 'vim', 'vi', 'code', 'notepad']
        for fallback in fallback_editors:
            try:
                subprocess.run([fallback, til_path])
                return True, f"📝 Opened {til_path} in {fallback}"
            except FileNotFoundError:
                continue
        
        return False, f"❌ No suitable editor found. Please set the EDITOR environment variable or install nano/vim"
    except Exception as e:
        return False, f"❌ Failed to open editor: {e}"


def reset_til(config=None):
    """Clear the contents of the TIL file"""
    til_path = get_til_path(config)
    
    try:
        with open(til_path, 'w', encoding='utf-8') as f:
            f.write("# Today I Learned\n\n")
        
        return True, f"🗑️  TIL file reset: {til_path}"
        
    except Exception as e:
        return False, f"❌ Failed to reset TIL file: {e}"


def delete_til(config=None):
    """Delete the TIL file completely"""
    til_path = get_til_path(config)
    
    if not os.path.exists(til_path):
        return True, "📝 No TIL file to delete"
    
    try:
        os.remove(til_path)
        return True, f"🗑️  TIL file deleted: {til_path}"
    except Exception as e:
        return False, f"❌ Failed to delete TIL file: {e}"


def filter_til_by_tag(config=None, tag=None):
    """Filter TIL entries by tag"""
    til_path = get_til_path(config)
    
    if not os.path.exists(til_path):
        return False, "📝 No TIL file found"
    
    try:
        with open(til_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not tag:
            return True, content
        
        # Filter content by tag
        filtered_lines = []
        current_header = None
        
        for line in content.split('\n'):
            if line.strip().startswith('## '):
                current_header = line
                header_added = False
            elif line.strip().startswith('- ') and f"`#{tag}`" in line:
                if current_header and not header_added:
                    filtered_lines.append(current_header)
                    header_added = True
                filtered_lines.append(line)
            elif line.strip().startswith('# '):
                filtered_lines.append(line)
        
        if not filtered_lines:
            return False, f"📝 No entries found with tag '{tag}'"
        
        return True, '\n'.join(filtered_lines)
        
    except Exception as e:
        return False, f"❌ Failed to filter TIL entries: {e}"


def export_til(config=None, format="md"):
    """Export TIL entries to specified format"""
    til_path = get_til_path(config)
    
    if not os.path.exists(til_path):
        return False, "📝 No TIL file found to export"
    
    try:
        with open(til_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format == "md":
            export_path = os.path.expanduser(f"~/til_export_{timestamp}.md")
            with open(export_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, f"📄 TIL exported to {export_path}"
            
        elif format == "json":
            import json
            
            # Parse markdown content into JSON structure
            lines = content.split('\n')
            data = {
                'export_date': datetime.now().isoformat(),
                'entries': []
            }
            
            current_date = None
            for line in lines:
                line = line.strip()
                if line.startswith('## '):
                    current_date = line[3:].strip()
                elif line.startswith('- '):
                    entry_text = line[2:].strip()
                    
                    # Extract tag if present
                    tag = None
                    if '`#' in entry_text and '`' in entry_text:
                        tag_start = entry_text.rfind('`#') + 2
                        tag_end = entry_text.rfind('`')
                        if tag_start < tag_end:
                            tag = entry_text[tag_start:tag_end]
                            entry_text = entry_text[:entry_text.rfind('`#')].strip()
                    
                    data['entries'].append({
                        'date': current_date,
                        'text': entry_text,
                        'tag': tag
                    })
            
            export_path = os.path.expanduser(f"~/til_export_{timestamp}.json")
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True, f"📊 TIL exported to {export_path}"
        
    except Exception as e:
        return False, f"❌ Failed to export TIL: {e}"


def get_til_stats(config=None):
    """Get statistics about the TIL file"""
    til_path = get_til_path(config)
    
    if not os.path.exists(til_path):
        return None
    
    try:
        with open(til_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        
        # Count entries (lines starting with -)
        entry_count = sum(1 for line in lines if line.strip().startswith('- '))
        
        # Count date headers (lines starting with ##)
        date_count = sum(1 for line in lines if line.strip().startswith('## '))
        
        # Count tags
        tags = set()
        for line in lines:
            if '`#' in line and '`' in line:
                tag_start = line.rfind('`#') + 2
                tag_end = line.rfind('`')
                if tag_start < tag_end:
                    tags.add(line[tag_start:tag_end])
        
        # Get file size
        file_size = len(content.encode('utf-8'))
        
        return {
            'entries': entry_count,
            'dates': date_count,
            'tags': len(tags),
            'size_bytes': file_size,
            'path': til_path,
            'tag_list': sorted(tags)
        }
        
    except Exception:
        return None
