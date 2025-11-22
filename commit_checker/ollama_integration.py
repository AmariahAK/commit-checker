"""Ollama integration for commit-checker.

Provides local AI-powered commit suggestions using Ollama.
User can use ANY Ollama model - automatically detects installed models.
"""
import subprocess
import json
import requests
from typing import Dict, List, Optional, Any


# Ollama API endpoint (local)
OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_LIST_URL = "http://localhost:11434/api/tags"


def is_ollama_installed() -> bool:
    """Check if Ollama is installed and running."""
    try:
        # Check if ollama command exists
        result = subprocess.run(
            ['which', 'ollama'],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except Exception:
        return False


def is_ollama_running() -> bool:
    """Check if Ollama service is running."""
    try:
        response = requests.get(OLLAMA_LIST_URL, timeout=2)
        return response.status_code == 200
    except requests.RequestException:
        return False


def get_installed_models() -> List[str]:
    """Get list of installed Ollama models.
    
    Returns:
        List of model names (e.g., ['llama3', 'mistral', 'codellama'])
    """
    try:
        response = requests.get(OLLAMA_LIST_URL, timeout=5)
        if response.status_code != 200:
            return []
        
        data = response.json()
        models = data.get('models', [])
        
        # Extract model names
        model_names = [model['name'] for model in models if 'name' in model]
        return model_names
    
    except Exception:
        return []


def select_default_model(models: List[str]) -> Optional[str]:
    """Auto-select best model from available models.
    
    Priority:
    1. Code-focused models (codellama, deepseek-coder)
    2. Chat models (llama3, mistral)
    3. First available model
    """
    if not models:
        return None
    
    # Priority models for commit messages
    priority_patterns = [
        'codellama',
        'deepseek-coder',
        'llama3',
        'mistral',
        'qwen'
    ]
    
    # Try to find priority model
    for pattern in priority_patterns:
        for model in models:
            if pattern in model.lower():
                return model
    
    # Fallback: return first model
    return models[0]


def generate_commit_message(
    diff_summary: str,
    user_profile: Optional[Dict[str, Any]] = None,
    model_name: Optional[str] = None
) -> Dict[str, Any]:
    """Generate commit message suggestions using Ollama.
    
    Args:
        diff_summary: Summary from diff_analyzer
        user_profile: User's commit style from history_learner
        model_name: Specific model to use (auto-selects if None)
        
    Returns:
        Dict with 'suggestions' list and optional 'error'
    """
    # Check if Ollama is available
    if not is_ollama_running():
        return {
            'error': 'Ollama is not running. Start it with: ollama serve',
            'suggestions': []
        }
    
    # Get model to use
    if not model_name:
        from .config_manager import get_preference
        model_name = get_preference('ollama_model')
    
    if not model_name:
        # Auto-select
        models = get_installed_models()
        model_name = select_default_model(models)
    
    if not model_name:
        return {
            'error': 'No Ollama models found. Install one with: ollama pull llama3',
            'suggestions': []
        }
    
    # Build prompt
    prompt = build_commit_prompt(diff_summary, user_profile)
    
    try:
        # Call Ollama API
        payload = {
            'model': model_name,
            'prompt': prompt,
            'stream': False,
            'options': {
                'temperature': 0.7,
                'num_predict': 200
            }
        }
        
        response = requests.post(
            OLLAMA_API_URL,
            json=payload,
            timeout=30
        )
        
        if response.status_code != 200:
            return {
                'error': f'Ollama API error: {response.status_code}',
                'suggestions': []
            }
        
        result = response.json()
        ai_response = result.get('response', '').strip()
        
        # Parse suggestions
        suggestions = parse_ollama_response(ai_response)
        
        return {
            'suggestions': suggestions,
            'model': model_name
        }
    
    except requests.RequestException as e:
        return {
            'error': f'Network error: {str(e)}',
            'suggestions': []
        }
    except Exception as e:
        return {
            'error': f'Unexpected error: {str(e)}',
            'suggestions': []
        }


def build_commit_prompt(
    diff_summary: str,
    user_profile: Optional[Dict[str, Any]] = None
) -> str:
    """Build optimized prompt for Ollama."""
    prompt_parts = [
        "You are a helpful commit message assistant.",
        "Generate 3 concise commit message suggestions for these changes:",
        "",
        diff_summary,
        ""
    ]
    
    # Add style guidance if available
    if user_profile:
        prompt_parts.append("User's commit style:")
        
        # Conventional commits
        if user_profile.get("prefixes", {}).get("uses_conventional"):
            prefixes = user_profile["prefixes"].get("common_prefixes", [])
            if prefixes:
                top_prefix = prefixes[0]["prefix"]
                prompt_parts.append(f"- Uses conventional commits (e.g., {top_prefix}:)")
        
        # Average length
        avg_words = user_profile.get("structure", {}).get("avg_words", 7)
        prompt_parts.append(f"- Typically ~{avg_words} words")
        
        prompt_parts.append("")
    
    prompt_parts.extend([
        "Provide exactly 3 commit message suggestions:",
        "1. Concise (1 line)",
        "2. Detailed (with context)",
        "3. Conventional commit format (type: description)",
        "",
        "Keep each suggestion under 72 characters.",
        "Format as: 1. <message>\\n2. <message>\\n3. <message>"
    ])
    
    return "\\n".join(prompt_parts)


def parse_ollama_response(response: str) -> List[str]:
    """Parse Ollama response into suggestions list."""
    suggestions = []
    
    # Split by newlines and look for numbered items
    lines = [line.strip() for line in response.split('\\n') if line.strip()]
    
    for line in lines:
        # Remove numbering (1., 2., etc.)
        cleaned = line.lstrip('123456789.*-) ').strip()
        
        # Filter valid suggestions
        if cleaned and 5 < len(cleaned) < 150:
            suggestions.append(cleaned)
        
        # Stop at 3 suggestions
        if len(suggestions) >= 3:
            break
    
    return suggestions[:3]


def print_status():
    """Print Ollama status."""
    print("\\n🦙 Ollama Status")
    print("=" * 60)
    
    installed = is_ollama_installed()
    running = is_ollama_running()
    
    if not installed:
        print("❌ Ollama not installed")
        print("   Install: https://ollama.com/download")
        return
    
    print("✅ Ollama installed")
    
    if not running:
        print("❌ Ollama not running")
        print("   Start: ollama serve")
        return
    
    print("✅ Ollama running")
    
    models = get_installed_models()
    if not models:
        print("⚠️  No models installed")
        print("   Install: ollama pull llama3")
        return
    
    print(f"✅ {len(models)} model(s) available:")
    for model in models:
        print(f"   • {model}")
    
    # Show recommended model
    recommended = select_default_model(models)
    if recommended:
        print(f"\\n🎯 Recommended: {recommended}")


def print_setup_instructions():
    """Print setup instructions for Ollama."""
    print("\\n🦙 Ollama Setup")
    print("=" * 60)
    print("1. Install Ollama:")
    print("   • Visit: https://ollama.com/download")
    print("   • Download for your OS (Mac/Linux/Windows)")
    print("   • Install and start Ollama")
    print()
    print("2. Install a model:")
    print("   • Recommended: ollama pull llama3")
    print("   • Or browse: https://ollama.com/library")
    print("   • For code: ollama pull codellama")
    print()
    print("3. Start using:")
    print("   • commit-checker will auto-detect your models")
    print("   • Or set preference: commit-checker --setup-ai")
    print()


if __name__ == "__main__":
    # Test
    print("🧪 Testing Ollama integration...")
    print()
    
    print_status()
    print()
    print_setup_instructions()
    
    # Test with sample diff
    if is_ollama_running():
        print("\\n📝 Testing generation...")
        sample_diff = "Changes: 2 files, +45/-3 lines | Modified: auth.py, config.py"
        
        result = generate_commit_message(sample_diff)
        
        if result.get('error'):
            print(f"⚠️  {result['error']}")
        else:
            print(f"Model: {result.get('model', 'unknown')}")
            print("Suggestions:")
            for i, suggestion in enumerate(result['suggestions'], 1):
                print(f"  {i}. {suggestion}")
