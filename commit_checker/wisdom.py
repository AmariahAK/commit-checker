import requests
import json
import os
import re
from datetime import datetime, timedelta

WISDOM_DROP_URL = "https://raw.githubusercontent.com/AmariahAK/wisdom-drop/main/README.md"
QUOTE_CACHE_FILE = os.path.expanduser("~/.commit_checker_cache/quote.json")
CACHE_DURATION = 86400

def get_cache_dir():
    cache_dir = os.path.expanduser("~/.commit_checker_cache")
    os.makedirs(cache_dir, exist_ok=True)
    return cache_dir

def is_cache_valid():
    if not os.path.exists(QUOTE_CACHE_FILE):
        return False
    try:
        with open(QUOTE_CACHE_FILE, 'r', encoding='utf-8') as f:
            cache = json.load(f)
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
            'category': cache.get('category', '')
        }
    except Exception:
        return None

def save_quote_to_cache(quote, author, category):
    try:
        get_cache_dir()
        cache_data = {
            'quote': quote,
            'author': author,
            'category': category,
            'timestamp': datetime.now().timestamp()
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
    quotes = []
    lines = readme_content.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith('# ') and 'Wisdom of the day' in line:
            category = ''
            category_match = re.match(r'#\s*\[([^\]]+)\]', line)
            if category_match:
                category = category_match.group(1)
            
            date = parse_date_from_header(line)
            
            quote_text = ''
            author = ''
            
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith('# '):
                content_line = lines[j].strip()
                
                if content_line.startswith('>'):
                    quote_line = content_line[1:].strip()
                    
                    if quote_line.startswith('—') or quote_line.startswith('–'):
                        author_text = re.sub(r'^[—–]\s*', '', quote_line)
                        category_in_author = re.search(r',?\s*Category:\s*([^,]+)', author_text, re.IGNORECASE)
                        if category_in_author:
                            if not category:
                                category = category_in_author.group(1).strip()
                            author = re.sub(r',?\s*Category:.*', '', author_text).strip()
                        else:
                            author = author_text.strip()
                    else:
                        if quote_text:
                            quote_text += ' '
                        quote_text += quote_line
                
                j += 1
            
            if quote_text and date:
                quotes.append({
                    'quote': quote_text.strip(),
                    'author': author.strip() if author else 'Unknown',
                    'category': category.strip() if category else 'Wisdom',
                    'date': date
                })
            
            i = j
        else:
            i += 1
    
    return quotes

def get_latest_wisdom_quote():
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
            return None
        
        today = datetime.now()
        valid_quotes = [q for q in quotes if q['date'] <= today]
        
        if not valid_quotes:
            return None
        
        latest = max(valid_quotes, key=lambda q: q['date'])
        
        save_quote_to_cache(latest['quote'], latest['author'], latest['category'])
        
        return {
            'quote': latest['quote'],
            'author': latest['author'],
            'category': latest['category']
        }
    
    except Exception as e:
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
    category = quote_data['category']
    
    return f"{icon} Wisdom Drop: \"{quote}\" — {author}, {category}"

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
