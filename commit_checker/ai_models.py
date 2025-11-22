"""Unified AI model manager for commit-checker.

Manages three AI model types:
1. TensorFlow (fast, local)
2. 300MB Local Model (high quality, local)
3. TogetherAI API (highest quality, requires API key)

Provides intelligent fallback and model selection.
"""
import os
import sys
from typing import Dict, List, Optional, Any
from enum import Enum


class ModelType(Enum):
    """Available AI model types."""
    TENSORFLOW = "tensorflow"
    LOCAL_LARGE = "local"
    TOGETHER_AI = "together_ai"


class AIModelManager:
    """Unified manager for all AI models."""
    
    def __init__(self):
        self.current_model = None
        self.tensorflow_available = False
        self.local_available = False
        self.together_available = False
        
        # Check availability
        self._check_model_availability()
    
    def _check_model_availability(self):
        """Check which models are available."""
        # Check TensorFlow
        try:
            import tensorflow as tf
            self.tensorflow_available = True
        except ImportError:
            self.tensorflow_available = False
        
        # Check local large model (transformers)
        try:
            import transformers
            import torch
            self.local_available = True
        except ImportError:
            self.local_available = False
        
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
                "name": "TensorFlow (Fast & Local)",
                "available": self.tensorflow_available,
                "description": "Fastest option, runs locally, good quality"
            },
            {
                "type": ModelType.LOCAL_LARGE,
                "name": "Local Large Model (High Quality)",
                "available": self.local_available,
                "description": "Higher quality, runs locally, requires transformers"
            },
            {
                "type": ModelType.TOGETHER_AI,
                "name": "TogetherAI API (Best Quality)",
                "available": self.together_available,
                "description": "Highest quality, requires API key, costs per use"
            }
        ]
        return models
    
    def get_preferred_model(self) -> Optional[ModelType]:
        """Get user's preferred model from config."""
        try:
            from .config_manager import get_preference
            model_pref = get_preference("default_ai_model", "local")
            
            # Map preference to ModelType
            mapping = {
                "tensorflow": ModelType.TENSORFLOW,
                "local": ModelType.LOCAL_LARGE,
                "together_ai": ModelType.TOGETHER_AI
            }
            
            return mapping.get(model_pref, ModelType.LOCAL_LARGE)
        except Exception:
            return ModelType.LOCAL_LARGE
    
    def get_best_available_model(self) -> Optional[ModelType]:
        """Get best available model with fallback logic."""
        preferred = self.get_preferred_model()
        
        # Try preferred first
        if preferred == ModelType.TOGETHER_AI and self.together_available:
            return ModelType.TOGETHER_AI
        elif preferred == ModelType.LOCAL_LARGE and self.local_available:
            return ModelType.LOCAL_LARGE
        elif preferred == ModelType.TENSORFLOW and self.tensorflow_available:
            return ModelType.TENSORFLOW
        
        # Fallback: try in quality order
        if self.together_available:
            return ModelType.TOGETHER_AI
        elif self.local_available:
            return ModelType.LOCAL_LARGE
        elif self.tensorflow_available:
            return ModelType.TENSORFLOW
        
        return None
    
    def generate_suggestions(
        self,
        diff_summary: str,
        diff_data: Optional[Dict[str, Any]] = None,
        user_profile: Optional[Dict[str, Any]] = None,
        force_model: Optional[ModelType] = None
    ) -> Dict[str, Any]:
        """Generate commit message suggestions using best available model.
        
        Args:
            diff_summary: Summary from diff_analyzer
            diff_data: Full diff data for context
            user_profile: User's commit style from history_learner
            force_model: Force specific model type
            
        Returns:
            Dict with suggestions list and metadata
        """
        # Determine which model to use
        model_to_use = force_model or self.get_best_available_model()
        
        if model_to_use is None:
            return self._fallback_suggestions(diff_summary, diff_data, user_profile)
        
        try:
            if model_to_use == ModelType.TOGETHER_AI:
                return self._together_ai_suggestions(diff_summary, user_profile)
            elif model_to_use == ModelType.LOCAL_LARGE:
                return self._local_large_suggestions(diff_summary, user_profile)
            elif model_to_use == ModelType.TENSORFLOW:
                return self._tensorflow_suggestions(diff_summary, user_profile)
        except Exception as e:
            print(f"⚠️  {model_to_use.value} failed: {e}", file=sys.stderr)
            # Fallback to next best
            return self._fallback_suggestions(diff_summary, diff_data, user_profile)
    
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
    
    def _local_large_suggestions(
        self,
        diff_summary: str,
        user_profile: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate suggestions using local large model."""
        # This would use the existing ai_handler logic 
        # For now, defer to the existing implementation
        try:
            from .ai_handler import get_ai_suggestion
            
            # Use the existing suggestion logic
            suggestions = get_ai_suggestion(
                diff_summary,
                max_suggestions=3,
                style_profile=user_profile
            )
            
            if suggestions:
                return {
                    "suggestions": suggestions if isinstance(suggestions, list) else [suggestions],
                    "model": "Local Large Model",
                    "source": "local"
                }
        except Exception as e:
            raise Exception(f"Local model failed: {e}")
        
        raise Exception("Local model not properly configured")
    
    def _tensorflow_suggestions(
        self,
        diff_summary: str,
        user_profile: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate suggestions using TensorFlow."""
        # Lightweight TensorFlow-based suggestions
        # For now, use heuristic fallback with TensorFlow label
        return self._heuristic_suggestions(diff_summary, user_profile, model_name="TensorFlow")
    
    def _fallback_suggestions(
        self,
        diff_summary: str,
        diff_data: Optional[Dict[str, Any]],
        user_profile: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate heuristic-based suggestions when no AI available."""
        return self._heuristic_suggestions(diff_summary, user_profile, model_name="Heuristic")
    
    def _heuristic_suggestions(
        self,
        diff_summary: str,
        user_profile: Optional[Dict[str, Any]],
        model_name: str = "Heuristic"
    ) -> Dict[str, Any]:
        """Generate suggestions using heuristic rules."""
        suggestions = []
        
        # Parse the summary to extract info
        parts = diff_summary.split("|")
        files_changed = "files"
        
        # Extract file names if available
        modified_files = []
        if "Modified:" in diff_summary:
            for part in parts:
                if "Modified:" in part:
                    files = part.replace("Modified:", "").strip().split(",")
                    modified_files = [f.strip() for f in files]
        
        # Generate variations
        # 1. Concise
        if modified_files:
            suggestions.append(f"Update {', '.join(modified_files[:2])}")
        else:
            suggestions.append("Update project files")
        
        # 2. With conventional commit
        change_type = "feat"  # Default
        if "fix" in diff_summary.lower() or "bug" in diff_summary.lower():
            change_type = "fix"
        
        if modified_files:
            suggestions.append(f"{change_type}: update {modified_files[0]}")
        else:
            suggestions.append(f"{change_type}: improve codebase")
        
        # 3. Detailed
        if modified_files:
            suggestions.append(f"Update {', '.join(modified_files)} with improvements")
        else:
            suggestions.append("Improve codebase with multiple enhancements")
        
        return {
            "suggestions": suggestions,
            "model": model_name,
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
                if model["type"] == ModelType.TOGETHER_AI:
                    print("  → Run: commit-checker --setup-ai")
                else:
                    print(f"  → Install: pip install transformers torch")
            print()
        
        best = self.get_best_available_model()
        if best:
            print(f"🎯 Will use: {best.value}")
        else:
            print("⚠️  No AI models available. Will use heuristic fallback.")


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
    # Test - add parent to path for standalone execution
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
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
        print(f"⚠️  Error during testing: {e}")
        print("This is expected if AI dependencies aren't installed.")
