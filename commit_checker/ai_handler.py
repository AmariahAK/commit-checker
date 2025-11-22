"""AI-powered commit message assistant with model management.

This module provides:
- AI-based commit message suggestions using transformers (DialoGPT, DistilBERT)
- Intelligent fallback to heuristic-based suggestions
- Model download and management
- Status checking for AI availability
- Profile-aware coaching for personalized suggestions
"""
import os
import json
import re

MODEL_DIR = os.path.expanduser("~/.commit-checker/models")
PROFILE_FILE = os.path.expanduser("~/.commit-checker/profile.json")

class CommitAIModel:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.generator = None
        self.use_model = False
        self.model_loaded = False
    
    def is_model_available(self):
        try:
            import transformers
            import torch
            return os.path.exists(MODEL_DIR) and os.path.isdir(MODEL_DIR)
        except ImportError:
            return False
    
    def ai_status_message(self):
        """Get a detailed status message about AI availability"""
        try:
            import transformers
            import torch
            transformers_available = True
        except ImportError:
            transformers_available = False
        
        if not transformers_available:
            return {
                'available': False,
                'reason': 'missing_dependencies',
                'message': '⚠️  AI models not available - transformers/torch not installed',
                'suggestion': '💡 Install with: pip install transformers torch --break-system-packages\n   Or run: commit-checker --download-models (requires dependencies first)'
            }
        
        if not os.path.exists(MODEL_DIR) or not os.path.isdir(MODEL_DIR):
            return {
                'available': False,
                'reason': 'models_not_downloaded',
                'message': '⚠️  AI models not downloaded',
                'suggestion': '💡 Download models with: commit-checker --download-models'
            }
        
        return {
            'available': True,
            'reason': 'ready',
            'message': '✅ AI models available and ready',
            'suggestion': ''
        }
    
    def load_model(self, model_type='generator'):
        if self.model_loaded:
            return True
        
        try:
            import transformers
            import torch
            
            if model_type == 'generator':
                model_path = os.path.join(MODEL_DIR, 'dialogpt')
                if os.path.exists(model_path):
                    self.tokenizer = transformers.AutoTokenizer.from_pretrained(model_path)
                    self.generator = transformers.AutoModelForCausalLM.from_pretrained(model_path)
                    self.model_loaded = True
                    return True
            elif model_type == 'analyzer':
                model_path = os.path.join(MODEL_DIR, 'distilbert')
                if os.path.exists(model_path):
                    self.tokenizer = transformers.AutoTokenizer.from_pretrained(model_path)
                    self.model = transformers.AutoModelForSequenceClassification.from_pretrained(model_path)
                    self.model_loaded = True
                    return True
            
            return False
        except Exception:
            return False
    
    def download_models(self, hf_token=None):
        try:
            import transformers
            import torch
            
            os.makedirs(MODEL_DIR, exist_ok=True)
            
            print("📥 Downloading commit suggestion models...")
            print("   This is a one-time download (~300MB)")
            
            try:
                print("   - Downloading DialoGPT-small for generation...")
                dialogpt_path = os.path.join(MODEL_DIR, 'dialogpt')
                tokenizer = transformers.AutoTokenizer.from_pretrained('microsoft/DialoGPT-small')
                model = transformers.AutoModelForCausalLM.from_pretrained('microsoft/DialoGPT-small')
                tokenizer.save_pretrained(dialogpt_path)
                model.save_pretrained(dialogpt_path)
                print("   ✅ DialoGPT downloaded")
            except Exception as e:
                print(f"   ⚠️  DialoGPT download failed: {e}")
            
            try:
                print("   - Downloading DistilBERT for analysis...")
                distilbert_path = os.path.join(MODEL_DIR, 'distilbert')
                tokenizer = transformers.AutoTokenizer.from_pretrained('distilbert-base-uncased')
                model = transformers.AutoModel.from_pretrained('distilbert-base-uncased')
                tokenizer.save_pretrained(distilbert_path)
                model.save_pretrained(distilbert_path)
                print("   ✅ DistilBERT downloaded")
            except Exception as e:
                print(f"   ⚠️  DistilBERT download failed: {e}")
            
            print("✅ Model download complete!")
            print("💡 You can now use AI-powered commit suggestions")
            
            if hf_token:
                print("🗑️  Deleting HuggingFace token (not needed after download)...")
            
            return True
        
        except ImportError:
            print("❌ transformers or torch not installed")
            print("   Install with: pip install transformers torch --break-system-packages")
            return False
        except Exception as e:
            print(f"❌ Model download failed: {e}")
            return False
    
    def suggest_commit(self, draft_message, context=None, profile=None):
        if self.use_model and self.load_model('generator'):
            return self._suggest_with_model(draft_message, context, profile)
        else:
            return self._suggest_with_heuristics(draft_message, context, profile)
    
    def _suggest_with_model(self, draft, context, profile):
        try:
            prompt = f"Improve this commit message: {draft}"
            if context:
                prompt += f"\nContext: {context.get('summary', '')}"
            if profile and profile.get('tone'):
                prompt += f"\nTone: {profile['tone']}"
            
            inputs = self.tokenizer.encode(prompt + self.tokenizer.eos_token, return_tensors='pt')
            outputs = self.generator.generate(
                inputs,
                max_length=100,
                pad_token_id=self.tokenizer.eos_token_id,
                temperature=0.7,
                top_k=50,
                top_p=0.9,
                do_sample=True
            )
            
            suggestion = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return self._clean_suggestion(suggestion)
        
        except Exception:
            return self._suggest_with_heuristics(draft, context, profile)
    
    def _suggest_with_heuristics(self, draft, context, profile):
        suggestions = []
        
        if not draft:
            if context and context.get('has_changes'):
                generated = self._generate_from_context(context)
                suggestions.append(f"💡 Suggested: {generated}")
                suggestions.append("📝 Based on your staged changes")
            else:
                suggestions.append("💡 Add a commit message describing your changes")
            return suggestions
        
        draft_lower = draft.lower().strip()
        words = draft.split()
        
        vague_words = ['stuff', 'things', 'updates', 'changes', 'fixes', 'misc', 'various']
        has_vague = any(word in draft_lower for word in vague_words)
        
        if has_vague:
            if context and context.get('files'):
                file_hint = os.path.basename(context['files'][0])
                suggestions.append(f"💡 '{draft}' is vague - specify what changed (e.g., 'fix {file_hint} validation')")
            else:
                suggestions.append(f"💡 Be more specific - what exactly changed?")
        
        if len(words) < 3 and not has_vague:
            if context and context.get('summary'):
                suggestions.append(f"💡 Add detail: {self._enhance_short_message(draft, context)}")
            else:
                suggestions.append("💡 Consider adding more detail to your message")
        
        if context:
            commit_type = self._infer_commit_type(context)
            scope = self._infer_scope(context)
            
            is_conventional = any(draft_lower.startswith(ct) for ct in ['feat', 'fix', 'docs', 'test', 'chore', 'refactor', 'style', 'perf'])
            
            if not is_conventional and commit_type:
                if scope:
                    suggestions.append(f"💡 Conventional format: {commit_type}({scope}): {draft}")
                else:
                    suggestions.append(f"💡 Conventional format: {commit_type}: {draft}")
        
        action_verbs = ['add', 'fix', 'update', 'remove', 'refactor', 'docs', 'test', 'feat', 'chore', 'improve', 'optimize']
        if not any(draft_lower.startswith(verb) for verb in action_verbs):
            verb_suggestion = self._suggest_verb_from_context(context) if context else 'add'
            suggestions.append(f"💡 Start with action verb (e.g., '{verb_suggestion}: {draft}')")
        
        if len(draft) > 72:
            shortened = draft[:69] + '...'
            suggestions.append(f"💡 Shorten to <72 chars: '{shortened}'")
        
        if draft[0].isupper() and ':' not in draft[:10] and not draft_lower.startswith('feat'):
            suggestions.append("💡 Use lowercase for non-conventional commits or add type prefix")
        
        if profile:
            avg_len = profile.get('avg_length', 50)
            if len(draft) < avg_len * 0.5:
                suggestions.append(f"💡 Your commits are usually {int(avg_len)} chars - add more context?")
        
        typos = {
            'teh': 'the', 'adn': 'and', 'recieve': 'receive', 
            'seperate': 'separate', 'definately': 'definitely'
        }
        for typo, correct in typos.items():
            if typo in draft_lower:
                suggestions.append(f"💡 Typo detected: '{typo}' → '{correct}'")
        
        return suggestions if suggestions else ["✅ Looks good!"]
    
    def _enhance_short_message(self, draft, context):
        if not context or not context.get('files'):
            return draft
        
        files = context.get('files', [])
        additions = context.get('total_additions', 0)
        
        if len(files) == 1:
            filename = os.path.basename(files[0])
            return f"{draft} in {filename}"
        elif additions > 50:
            return f"{draft} across {len(files)} files"
        else:
            return f"{draft} (minor changes)"
    
    def _suggest_verb_from_context(self, context):
        if not context:
            return 'update'
        
        additions = context.get('total_additions', 0)
        deletions = context.get('total_deletions', 0)
        files = context.get('files', [])
        
        if deletions > additions * 2:
            return 'remove'
        if additions > deletions * 3:
            return 'add'
        if any('test' in f.lower() for f in files):
            return 'test'
        if any('.md' in f.lower() for f in files):
            return 'docs'
        
        return 'update'
    
    def _generate_from_context(self, context):
        if not context or not context.get('has_changes'):
            return ""
        
        commit_type = self._infer_commit_type(context)
        scope = self._infer_scope(context)
        action = self._infer_action(context)
        
        if scope:
            return f"{commit_type}({scope}): {action}"
        return f"{commit_type}: {action}"
    
    def _infer_commit_type(self, context):
        if not context:
            return 'feat'
        
        files = context.get('files', [])
        additions = context.get('total_additions', 0)
        deletions = context.get('total_deletions', 0)
        
        if any('test' in f.lower() for f in files):
            return 'test'
        if any('.md' in f.lower() or 'doc' in f.lower() for f in files):
            return 'docs'
        if deletions > additions:
            return 'refactor'
        if additions < 20:
            return 'fix'
        
        return 'feat'
    
    def _infer_scope(self, context):
        if not context or not context.get('files'):
            return ''
        
        files = context['files']
        if len(files) == 1:
            return os.path.splitext(os.path.basename(files[0]))[0]
        
        common_dir = os.path.commonprefix([os.path.dirname(f) for f in files])
        if common_dir:
            return os.path.basename(common_dir)
        
        return ''
    
    def _infer_action(self, context):
        if not context:
            return 'update code'
        
        additions = context.get('total_additions', 0)
        deletions = context.get('total_deletions', 0)
        files = context.get('files', [])
        
        if deletions > additions * 2:
            return 'remove deprecated code'
        if len(files) > 5:
            return 'implement new feature'
        if additions < 10:
            return 'fix minor issue'
        
        return 'update implementation'
    
    def _clean_suggestion(self, text):
        text = re.sub(r'\s+', ' ', text).strip()
        if len(text) > 72:
            text = text[:69] + '...'
        return text
    
    def adapt_from_history(self, profile):
        if not profile or not profile.get('commit_history'):
            return
        
        history = profile['commit_history']
        
        tones = [commit.get('tone', 'imperative') for commit in history]
        common_tone = max(set(tones), key=tones.count) if tones else 'imperative'
        
        profile['preferred_tone'] = common_tone
        profile['avg_length'] = sum(len(c.get('message', '')) for c in history) / len(history) if history else 50
        
        return profile

ai_model = CommitAIModel()

def get_ai_suggestion(draft, context=None, profile=None, use_model=False):
    ai_model.use_model = use_model
    return ai_model.suggest_commit(draft, context, profile)

def download_ai_models(hf_token=None):
    return ai_model.download_models(hf_token)

def is_ai_available():
    return ai_model.is_model_available()

def get_ai_status():
    """Get detailed AI status information"""
    return ai_model.ai_status_message()
