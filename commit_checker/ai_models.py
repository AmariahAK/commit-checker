"""Unified AI model manager for commit-checker.

Manages four AI options:
1. TensorFlow (smart, lightweight, local - no dependencies)
2. Ollama (flexible, any model, local - requires Ollama)
3. TogetherAI (cloud API - requires API key)
4. Heuristic (fallback - always available)
"""
import os
import sys
from typing import Dict, List, Optional, Any
from enum import Enum


class ModelType(Enum):
    """Available AI model types."""
    TENSORFLOW = "tensorflow"
    OLLAMA = "ollama"
    TOGETHER_AI = "together_ai"
    HEURISTIC = "heuristic"


class AIModelManager:
    """Unified manager for all AI models."""
    
    def __init__(self):
        self.current_model = None
        self.tensorflow_available = True  # Always available (no dependencies)
        self.ollama_available = False
        self.together_available = False
        
        # Check availability
        self._check_model_availability()
    
    def _check_model_availability(self):
        """Check which models are available."""
        # TensorFlow is always available (built-in)
        self.tensorflow_available = True
        
        # Check Ollama
        try:
            from .ollama_integration import is_ollama_running
            self.ollama_available = is_ollama_running()
        except Exception:
            self.ollama_available = False
        
        # Check TogetherAI (requires API key)
        try:
            from .config_manager import get_api_key
            api_key = get_api_key("together_ai")
            self.together_available = api_key is not None
        except Exception:
            self.together_available = False
    
    def get_available_models(self) -> List[Dict[str, Any]]:
        """Get list of available models with their status."""
        models = [
            {
                "type": ModelType.TENSORFLOW,
                "name": "TensorFlow (Smart & Lightweight)",
                "available": self.tensorflow_available,
                "description": "Pattern-based ML, no dependencies, always available"
            },
            {
                "type": ModelType.OLLAMA,
                "name": "Ollama (Flexible Local AI)",
                "available": self.ollama_available,
                "description": "Any Ollama model, runs locally, requires Ollama"
            },
            {
                "type": ModelType.TOGETHER_AI,
                "name": "TogetherAI (Cloud API)",
                "available": self.together_available,
                "description": "Highest quality, requires API key"
            },
            {
                "type": ModelType.HEURISTIC,
                "name": "Heuristic Coach",
                "available": True,
                "description": "Rule-based coaching, always available"
            }
        ]
        return models
    
    def get_preferred_model(self) -> Optional[ModelType]:
        """Get user's preferred model from config."""
        try:
            from .config_manager import get_preference
            model_pref = get_preference("default_ai_model", "tensorflow")
            
            # Map preference to ModelType
            mapping = {
                "tensorflow": ModelType.TENSORFLOW,
                "ollama": ModelType.OLLAMA,
                "together_ai": ModelType.TOGETHER_AI,
                "heuristic": ModelType.HEURISTIC
            }
            
            return mapping.get(model_pref, ModelType.TENSORFLOW)
        except Exception:
            return ModelType.TENSORFLOW
    
    def get_best_available_model(self) -> ModelType:
        """Get best available model with fallback logic."""
        preferred = self.get_preferred_model()
        
        # Try preferred first
        if preferred == ModelType.TOGETHER_AI and self.together_available:
            return ModelType.TOGETHER_AI
        elif preferred == ModelType.OLLAMA and self.ollama_available:
            return ModelType.OLLAMA
        elif preferred == ModelType.TENSORFLOW and self.tensorflow_available:
            return ModelType.TENSORFLOW
        elif preferred == ModelType.HEURISTIC:
            return ModelType.HEURISTIC
        
        # Smart fallback: try in quality order
        if self.ollama_available:
            return ModelType.OLLAMA
        elif self.together_available:
            return ModelType.TOGETHER_AI
        elif self.tensorflow_available:
            return ModelType.TENSORFLOW
        
        # Ultimate fallback
        return ModelType.HEURISTIC
    
    def generate_suggestions(
        self,
        diff_summary: str,
        diff_data: Optional[Dict[str, Any]] = None,
        user_profile: Optional[Dict[str, Any]] = None,
        force_model: Optional[ModelType] = None
    ) -> Dict[str, Any]:
        """Generate commit message suggestions using best available model.
        
        Args:
            diff_summary: Summary from diff_analyzer or direct input
            diff_data: Full diff data for context (optional)
            user_profile: User's commit style from history_learner
            force_model: Force specific model type
            
        Returns:
            Dict with suggestions list and metadata
        """
        # Determine which model to use
        model_to_use = force_model or self.get_best_available_model()
        
        try:
            if model_to_use == ModelType.TOGETHER_AI:
                return self._together_ai_suggestions(diff_summary, user_profile)
            elif model_to_use == ModelType.OLLAMA:
                return self._ollama_suggestions(diff_summary, user_profile)
            elif model_to_use == ModelType.TENSORFLOW:
                return self._tensorflow_suggestions(diff_summary, user_profile)
            elif model_to_use == ModelType.HEURISTIC:
                return self._heuristic_suggestions(diff_summary, user_profile)
        except Exception as e:
            print(f"⚠️  {model_to_use.value} failed: {e}", file=sys.stderr)
            # Fallback to heuristic
            return self._heuristic_suggestions(diff_summary, user_profile)
    
    def _together_ai_suggestions(
        self,
        diff_summary: str,
        user_profile: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate suggestions using TogetherAI."""
        from .together_ai import generate_commit_message
        
        result = generate_commit_message(diff_summary, user_profile)
        
        if result.get("error"):
            raise Exception(result["error"])
        
        return {
            "suggestions": result["suggestions"],
            "model": "TogetherAI",
            "usage": result.get("usage"),
            "source": "api"
        }
    
    def _ollama_suggestions(
        self,
        diff_summary: str,
        user_profile: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate suggestions using Ollama."""
        from .ollama_integration import generate_commit_message
        
        result = generate_commit_message(diff_summary, user_profile)
        
        if result.get("error"):
            raise Exception(result["error"])
        
        return {
            "suggestions": result["suggestions"],
            "model": f"Ollama ({result.get('model', 'unknown')})",
            "source": "local"
        }
    
    def _tensorflow_suggestions(
        self,
        diff_summary: str,
        user_profile: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate suggestions using smart TensorFlow model."""
        from .tensorflow_model import generate_commit_suggestions
        
        result = generate_commit_suggestions(diff_summary, user_profile)
        
        return {
            "suggestions": result["suggestions"],
            "model": "Smart TensorFlow",
            "confidence": result.get("confidence", 0.8),
            "source": "local"
        }
    
    def _heuristic_suggestions(
        self,
        diff_summary: str,
        user_profile: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate suggestions using heuristic rules."""
        from .ai_handler import get_ai_suggestion
        
        # ai_handler expects (draft, context, profile)
        # We'll pass diff_summary as context
        context = {'summary': diff_summary, 'has_changes': True}
        
        suggestions = get_ai_suggestion("", context, user_profile)
        
        return {
            "suggestions": suggestions if isinstance(suggestions, list) else [suggestions],
            "model": "Heuristic Coach",
            "source": "heuristic"
        }
    
    def print_status(self):
        """Print current model status."""
        print("\n🤖 AI Model Status")
        print("=" * 60)
        
        models = self.get_available_models()
        for model in models:
            status = "✓" if model["available"] else "✗"
            print(f"{status} {model['name']}")
            print(f"  {model['description']}")
            if not model["available"]:
                if model["type"] == ModelType.OLLAMA:
                    print("  → Install: https://ollama.com/download")
                    print("  → Start: ollama serve")
                elif model["type"] == ModelType.TOGETHER_AI:
                    print("  → Setup: commit-checker --setup-ai")
            print()
        
        best = self.get_best_available_model()
        print(f"🎯 Will use: {best.value}")


# Convenience functions for CLI
def get_commit_suggestions(
    diff_summary: str,
    diff_data: Optional[Dict[str, Any]] = None,
    user_profile: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Get commit message suggestions (main entry point)."""
    manager = AIModelManager()
    return manager.generate_suggestions(diff_summary, diff_data, user_profile)


def print_model_status():
    """Print AI model status."""
    manager = AIModelManager()
    manager.print_status()


if __name__ == "__main__":
    # Test
    print("🧪 Testing AI Model Manager...")
    print()
    
    manager = AIModelManager()
    manager.print_status()
    
    # Test with sample diff
    sample_diff = "Changes: 2 files, +45/-3 lines | Modified: auth.py, config.py"
    
    print("\n📝 Testing suggestion generation...")
    print(f"Diff: {sample_diff}")
    print()
    
    try:
        result = manager.generate_suggestions(sample_diff)
        
        print(f"Model used: {result['model']}")
        print("Suggestions:")
        for i, suggestion in enumerate(result['suggestions'], 1):
            print(f"  {i}. {suggestion}")
    except Exception as e:
        print(f"⚠️  Error: {e}")
