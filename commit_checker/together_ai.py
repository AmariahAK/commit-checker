"""TogetherAI API integration for commit-checker.

Provides high-quality AI-powered commit suggestions using TogetherAI's API.
User provides their own API key for cost control.
"""
import os
import requests
from typing import Dict, List, Optional, Any
import json


# TogetherAI API endpoint
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"

# Default model (user can specify any model from together.ai)
DEFAULT_MODEL = "meta-llama/Llama-3-70b-chat-hf"

# Example popular models (for reference only - user can use ANY model)
EXAMPLE_MODELS = """
Popular models on TogetherAI:
  • meta-llama/Llama-3-70b-chat-hf (Llama 3 70B)
  • deepseek-ai/deepseek-coder-33b-instruct (DeepSeek Coder)
  • Qwen/Qwen2-72B-Instruct (Qwen 2)
  • mistralai/Mixtral-8x7B-Instruct-v0.1 (Mixtral)
  • codellama/CodeLlama-34b-Instruct-hf (CodeLlama)
  
Find more at: https://api.together.xyz/models
"""


def test_api_key(api_key: str) -> Dict[str, Any]:
    """Test if API key is valid.
    
    Args:
        api_key: TogetherAI API key
        
    Returns:
        Dict with 'valid' boolean and optional 'error' message
    """
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Simple test request with small model
        data = {
            "model": "meta-llama/Llama-3-8b-chat-hf",
            "messages": [{"role": "user", "content": "test"}],
            "max_tokens": 5
        }
        
        response = requests.post(
            TOGETHER_API_URL,
            headers=headers,
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            return {"valid": True}
        elif response.status_code == 401:
            return {"valid": False, "error": "Invalid API key"}
        else:
            return {"valid": False, "error": f"API error: {response.status_code}"}
            
    except requests.RequestException as e:
        return {"valid": False, "error": f"Network error: {str(e)}"}


def generate_commit_message(
    diff_summary: str,
    user_style_profile: Optional[Dict[str, Any]] = None,
    api_key: Optional[str] = None,
    model_id: Optional[str] = None
) -> Dict[str, Any]:
    """Generate commit message suggestion using TogetherAI.
    
    Args:
        diff_summary: Summary of changes from diff_analyzer
        user_style_profile: User's commit style from history_learner
        api_key: TogetherAI API key
        model_id: Model to use (defaults to Llama 3 70B)
        
    Returns:
        Dict with 'suggestions' list and optional 'error'
    """
    if not api_key:
        from .config_manager import get_api_key
        api_key = get_api_key("together_ai")
    
    if not api_key:
        return {
            "error": "No API key found. Set up with: commit-checker --setup-ai",
            "suggestions": []
        }
    
    if not model_id:
        from .config_manager import get_preference
        model_id = get_preference("selected_together_model", DEFAULT_MODEL)
    
    # Build prompt
    prompt = build_commit_prompt(diff_summary, user_style_profile)
    
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model_id,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful commit message assistant. Generate clear, concise commit messages based on code changes."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 200,
            "stop": ["\n\n", "###"]
        }
        
        response = requests.post(
            TOGETHER_API_URL,
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code != 200:
            return {
                "error": f"API error ({response.status_code}): {response.text}",
                "suggestions": []
            }
        
        result = response.json()
        
        # Parse suggestions
        ai_response = result["choices"][0]["message"]["content"].strip()
        suggestions = parse_ai_suggestions(ai_response)
        
        # Track usage for user
        usage = result.get("usage", {})
        
        return {
            "suggestions": suggestions,
            "usage": {
                "tokens": usage.get("total_tokens", 0),
                "estimated_cost": estimate_cost(usage.get("total_tokens", 0), model_id)
            }
        }
        
    except requests.RequestException as e:
        return {
            "error": f"Network error: {str(e)}",
            "suggestions": []
        }
    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}",
            "suggestions": []
        }


def build_commit_prompt(
    diff_summary: str,
    user_style_profile: Optional[Dict[str, Any]] = None
) -> str:
    """Build optimized prompt for commit message generation."""
    prompt_parts = [
        "Generate 3 commit message suggestions for these changes:",
        "",
        diff_summary,
        ""
    ]
    
    # Add style guidance if available
    if user_style_profile:
        prompt_parts.append("User's style preferences:")
        
        # Conventional commits
        if user_style_profile.get("prefixes", {}).get("uses_conventional"):
            prefixes = user_style_profile["prefixes"].get("common_prefixes", [])
            if prefixes:
                top_prefix = prefixes[0]["prefix"]
                prompt_parts.append(f"- Uses conventional commits (common prefix: {top_prefix}:)")
        
        # Tone
        tone = user_style_profile.get("tone", "imperative")
        prompt_parts.append(f"- Style: {tone}")
        
        # Length
        avg_words = user_style_profile.get("structure", {}).get("avg_words", 7)
        prompt_parts.append(f"- Usually ~{avg_words} words")
        
        # Emoji
        if user_style_profile.get("emoji", {}).get("uses_emoji"):
            prompt_parts.append("- Sometimes uses emoji")
        
        prompt_parts.append("")
    
    prompt_parts.extend([
        "Provide 3 variations:",
        "1. Concise version",
        "2. Detailed version",
        "3. Conventional commit format",
        "",
        "Format each as: `suggestion text`"
    ])
    
    return "\n".join(prompt_parts)


def parse_ai_suggestions(ai_response: str) -> List[str]:
    """Parse AI response into suggestion list."""
    suggestions = []
    
    # Try to extract suggestions in backticks
    backtick_pattern = r'`([^`]+)`'
    matches = re.findall(backtick_pattern, ai_response)
    
    if matches:
        suggestions = matches[:3]  # Max 3
    else:
        # Fallback: split by newlines
        lines = [line.strip() for line in ai_response.split('\n') if line.strip()]
        # Remove numbering
        cleaned = []
        for line in lines:
            cleaned_line = re.sub(r'^\d+\.\s*', '', line).strip()
            if cleaned_line and len(cleaned_line) > 5:
                cleaned.append(cleaned_line)
        
        suggestions = cleaned[:3]
    
    return suggestions


def estimate_cost(tokens: int, model_id: str) -> float:
    """Estimate cost for token usage.
    
    Note: Costs vary by model. Check https://api.together.xyz/ for exact pricing.
    This provides a rough estimate based on typical rates (~$0.6-$1.0 per 1M tokens).
    """
    # Generic estimate: $0.80 per 1M tokens (mid-range)
    cost_per_1m = 0.80
    cost = (tokens / 1_000_000) * cost_per_1m
    return round(cost, 6)


def print_available_models():
    """Print examples of popular models."""
    print(EXAMPLE_MODELS)


def print_setup_instructions():
    """Print setup instructions for TogetherAI."""
    print("\n🔑 TogetherAI Setup")
    print("=" * 60)
    print("1. Go to: https://api.together.xyz/signup")
    print("2. Create an account (if you don't have one)")
    print("3. Navigate to API Keys section")
    print("4. Create a new API key")
    print("5. Copy the API key")
    print()
    print("6. Choose your model:")
    print("   • Visit: https://api.together.xyz/models")
    print("   • Find a model you like (e.g., 'meta-llama/Llama-3-70b-chat-hf')")
    print("   • Copy the exact model ID")
    print()
    print("7. Run: commit-checker --setup-ai")
    print("   • Paste your API key when prompted")
    print("   • Paste the model ID when prompted")
    print()


def print_cost_warning():
    """Print cost warning for users."""
    print("\n⚠️  TogetherAI Cost Information")
    print("=" * 60)
    print("• You pay for API usage (token-based pricing)")
    print("• Typical commit suggestion: ~500-1000 tokens")
    print("• Estimated cost: $0.0004 - $0.0008 per suggestion")
    print("• Costs vary by model - check: https://api.together.xyz/")
    print("• Set spending limits in your TogetherAI dashboard")
    print()


if __name__ == "__main__":
    # Test
    import re
    
    print("🧪 Testing TogetherAI integration...")
    print()
    
    # Show example models
    print("📚 Example Models:")
    print_available_models()
    print()
    
    # Show setup instructions
    print_setup_instructions()
    
    # Show cost warning
    print_cost_warning()
    
    # Test with sample diff
    sample_diff = "Changes: 2 files, +45/-3 lines | Modified: auth.py, login.py | Changed: validate_user, check_password"
    
    print("📝 Sample diff summary:")
    print(f"  {sample_diff}")
    print()
    
    print("💡 Quick Start:")
    print("  1. Get API key: https://api.together.xyz/")
    print("  2. Choose model: https://api.together.xyz/models")
    print("  3. Run: commit-checker --setup-ai")
    print("  4. Use: commit-checker --suggest")
