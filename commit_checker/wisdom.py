"""Wisdom Drop integration module for fetching and displaying daily wisdom quotes.

This module handles:
- Fetching quotes from the wisdom-drop GitHub repository
- Parsing quotes with category, date, and author information
- Intelligent caching with date-based and commit-based invalidation
- Formatting quotes for display in the terminal
"""
import requests
import json
import os
import re
from datetime import datetime

WISDOM_DROP_URL = "https://raw.githubusercontent.com/AmariahAK/wisdom-drop/main/README.md"
GITHUB_API_URL = "https://api.github.com/repos/AmariahAK/wisdom-drop/commits"
CACHE_DIR = os.path.expanduser("~/.commit_checker_cache")
QUOTE_CACHE_FILE = os.path.join(CACHE_DIR, "quote.json")
CACHE_DURATION = 86400

def get_cache_dir():
    cache_dir = os.path.expanduser("~/.commit_checker_cache")
    os.makedirs(cache_dir, exist_ok=True)
    return cache_dir

def get_latest_wisdom_commit_sha():
    """Get the latest commit SHA for wisdom-drop README.md"""
    try:
        response = requests.get(WISDOM_DROP_API_URL, timeout=5)
        response.raise_for_status()
        commits = response.json()
        if commits and len(commits) > 0:
            return commits[0]['sha']
    except Exception:
        pass
    return None

def is_cache_valid():
    """Check if the cached wisdom quote is still valid.
    
    Validates cache based on:
    1. Date change - invalidates if cached on a different day
    2. Repository updates - invalidates if wisdom-drop has new commits
    3. Time-based fallback - invalidates after 24 hours
    
    Returns:
        bool: True if cache is valid and can be used, False otherwise
    """
    if not os.path.exists(QUOTE_CACHE_FILE):
        return False
    try:
        with open(QUOTE_CACHE_FILE, 'r', encoding='utf-8') as f:
            cache = json.load(f)
        
        # Check if we're on a different day than when cached
        cached_date = cache.get('cached_day')
        today_date = datetime.now().strftime('%Y-%m-%d')
        if cached_date and cached_date != today_date:
            return False  # New day, invalidate cache to check for new quote
        
        # Check if wisdom-drop repo has been updated
        cached_commit = cache.get('commit_sha')
        if cached_commit:
            latest_commit = get_latest_wisdom_commit_sha()
            if latest_commit and latest_commit != cached_commit:
                return False  # New commit available, cache invalid
        
        # Fallback to time-based cache (24hr)
        cache_time = cache.get('timestamp', 0)
        return (datetime.now().timestamp() - cache_time) < CACHE_DURATION
    except Exception:
        return False

def load_cached_quote():
    try:
        with open(QUOTE_CACHE_FILE, 'r', encoding='utf-8') as f:
            cache = json.load(f)
        return {
            'quote': cache.get('quote', ''),
            'author': cache.get('author', ''),
            'category': cache.get('category', ''),
            'date_display': cache.get('date_display', '')
        }
    except Exception:
        return None

def save_quote_to_cache(quote, author, category, date_display='', commit_sha=None):
    try:
        get_cache_dir()
        cache_data = {
            'quote': quote,
            'author': author,
            'category': category,
            'date_display': date_display,
            'timestamp': datetime.now().timestamp(),
            'cached_day': datetime.now().strftime('%Y-%m-%d'),
            'commit_sha': commit_sha
        }
        with open(QUOTE_CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, indent=2)
    except Exception:
        pass

def parse_date_from_header(header_text):
    month_map = {
        'january': 1, 'february': 2, 'march': 3, 'april': 4,
        'may': 5, 'june': 6, 'july': 7, 'august': 8,
        'september': 9, 'october': 10, 'november': 11, 'december': 12
    }
    
    pattern = r'\(([A-Za-z]+)\s+(\d+)\s+(\d+)\)'
    match = re.search(pattern, header_text)
    if match:
        month_str, day_str, year_str = match.groups()
        month_lower = month_str.lower()
        if month_lower in month_map:
            try:
                month = month_map[month_lower]
                day = int(day_str)
                year = int(year_str)
                return datetime(year, month, day)
            except (ValueError, OverflowError):
                return None
    return None

def parse_wisdom_drop_readme(readme_content):
    """Parse wisdom quotes from the wisdom-drop README content.
    
    Extracts quotes with metadata including:
    - Category (e.g., 'Developer', 'Samurai Discipline / Modern Focus')
    - Date (parsed from header)
    - Quote text
    - Author attribution
    
    Handles multiple format variations:
    - Authors with em-dashes: > — Author Name
    - Authors without dashes: > Author Name
    - Multi-line quotes
    - Case variations ("day" vs "Day")
    
    Args:
        readme_content (str): The raw README.md content from wisdom-drop repo
        
    Returns:
        list: List of dicts containing quote, author, category, date, and date_display
    """
    quotes = []
    lines = readme_content.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith('# ') and 'wisdom of the' in line.lower():
            # Extract category from format like: # Developer Wisdom of the day (July 29 2025)
            # or # Life Wisdom of the day (July 31 2025)
            category = ''
            
            # Try to extract category before 'Wisdom of the day'
            category_pattern = r'^#\s*([^W]+?)\s*Wisdom of the day'
            category_match = re.match(category_pattern, line, re.IGNORECASE)
            if category_match:
                category = category_match.group(1).strip()
            
            # Parse date from header
            date = parse_date_from_header(line)
            
            # Extract formatted date string for display (e.g., "July 29 2025")
            date_str_pattern = r'\(([A-Za-z]+\s+\d+\s+\d+)\)'
            date_str_match = re.search(date_str_pattern, line)
            date_display = date_str_match.group(1) if date_str_match else ''
            
            quote_text = ''
            author = ''
            
            # Collect all lines for this quote entry
            quote_lines = []
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith('# '):
                content_line = lines[j].strip()
                if content_line.startswith('>'):
                    quote_lines.append(content_line[1:].strip())
                j += 1
            
            # Now parse the collected lines
            # Logic: First line(s) are quote, last line is usually author
            if not quote_lines:
                i = j
                continue
            
            quote_text = ''
            author = ''
            
            # If there's only one line, it's the quote with no author
            if len(quote_lines) == 1:
                quote_text = quote_lines[0]
            else:
                # Check if last line is author (starts with dash OR looks like a name/attribution)
                last_line = quote_lines[-1]
                
                # Is it clearly an author line (starts with dash)?
                if last_line.startswith('—') or last_line.startswith('–') or last_line.startswith('-'):
                    author = re.sub(r'^[—–-]\s*', '', last_line)
                    quote_text = ' '.join(quote_lines[:-1])
                # Does it look like an attribution? (short, no ending punctuation, or has names/sources)
                elif (len(last_line) < 100 and 
                      not last_line.strip('"').endswith(('.', '!', '?'))):
                    # Likely an author without dash
                    author = last_line
                    quote_text = ' '.join(quote_lines[:-1])
                # Otherwise, all lines are part of the quote
                else:
                    quote_text = ' '.join(quote_lines)
            
            # Clean up quote text (remove quotes if present)
            quote_text = quote_text.strip()
            
            # Extract category from author if needed (some entries have "Author, Category: XYZ")
            if author:
                category_in_author = re.search(r',?\s*Category:\s*([^,]+)', author, re.IGNORECASE)
                if category_in_author:
                    if not category:
                        category = category_in_author.group(1).strip()
                    author = re.sub(r',?\s*Category:.*', '', author).strip()
            
            if quote_text and date:
                quotes.append({
                    'quote': quote_text.strip(),
                    'author': author.strip() if author else 'Unknown',
                    'category': category.strip() if category else 'Wisdom',
                    'date': date,
                    'date_display': date_display
                })
            
            i = j
        else:
            i += 1
    
    return quotes

def get_latest_wisdom_quote():
    """Get the latest wisdom quote, using cache when valid.
    
    Fetches from wisdom-drop repository if cache is invalid or missing.
    Automatically handles caching and commit SHA tracking.
    
    Returns:
        dict: Quote data with keys: quote, author, category, date_display
        None: If quote cannot be fetched and no cache available
    """
    if is_cache_valid():
        cached = load_cached_quote()
        if cached:
            return cached
    
    try:
        response = requests.get(WISDOM_DROP_URL, timeout=10)
        response.raise_for_status()
        readme_content = response.text
        
        quotes = parse_wisdom_drop_readme(readme_content)
        
        if not quotes:
            import sys
            if '--debug' in sys.argv:
                print("⚠️ Warning: No quotes parsed from wisdom-drop", file=sys.stderr)
            return None
        
        today = datetime.now()
        valid_quotes = [q for q in quotes if q['date'] <= today]
        
        if not valid_quotes:
            import sys
            if '--debug' in sys.argv:
                print(f"⚠️ Warning: No valid quotes for today ({today.strftime('%Y-%m-%d')})", file=sys.stderr)
            return None
        
        latest = max(valid_quotes, key=lambda q: q['date'])
        
        commit_sha = get_latest_wisdom_commit_sha()
        save_quote_to_cache(
            latest['quote'], 
            latest['author'], 
            latest['category'],
            latest.get('date_display', ''),
            commit_sha
        )
        
        return {
            'quote': latest['quote'],
            'author': latest['author'],
            'category': latest['category'],
            'date_display': latest.get('date_display', '')
        }
    
    except requests.RequestException as e:
        import sys
        if '--debug' in sys.argv:
            print(f"⚠️ Network error fetching wisdom quote: {e}", file=sys.stderr)
    except Exception as e:
        import sys
        if '--debug' in sys.argv:
            print(f"⚠️ Error getting wisdom quote: {e}", file=sys.stderr)
        cached = load_cached_quote()
        if cached:
            return cached
        return None

def format_wisdom_quote(quote_data, emoji_mode=True):
    if not quote_data:
        return ""
    
    icon = "💡" if emoji_mode else ">"
    quote = quote_data['quote'].strip('"').strip("'")
    author = quote_data['author']
    category = quote_data.get('category', 'Wisdom')
    date_display = quote_data.get('date_display', '')
    
    # Format: 💡 [Category] Wisdom of the day (Date): "Quote" — Author
    if date_display:
        return f"{icon} [{category}] Wisdom of the day ({date_display}): \"{quote}\" — {author}"
    else:
        return f"{icon} [{category}] Wisdom of the day: \"{quote}\" — {author}"

def refresh_wisdom_quote():
    try:
        if os.path.exists(QUOTE_CACHE_FILE):
            os.remove(QUOTE_CACHE_FILE)
        
        quote_data = get_latest_wisdom_quote()
        if quote_data:
            print("✅ Wisdom Drop quote refreshed!")
            print(format_wisdom_quote(quote_data))
            return True
        else:
            print("⚠️  Could not fetch Wisdom Drop quote")
            return False
    except Exception as e:
        print(f"❌ Error refreshing quote: {e}")
        return False
