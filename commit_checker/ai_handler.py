"""AI-powered commit message assistant - Heuristic coaching only.

This module provides intelligent commit message coaching without requiring
heavy ML models. For AI-powered suggestions, see ai_models.py.
"""
import os
import re
from typing import Dict, List, Optional, Any


class CommitCoach:
    """Heuristic-based commit message coaching."""
    
    def suggest_commit(self, draft_message, context=None, profile=None):
        """Generate suggestions using rule-based heuristics."""
        return self._suggest_with_heuristics(draft_message, context, profile)
    
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
        
        # Check for vague words
        vague_words = ['stuff', 'things', 'updates', 'changes', 'fixes', 'misc', 'various']
        has_vague = any(word in draft_lower for word in vague_words)
        
        if has_vague:
            if context and context.get('files'):
                file_hint = os.path.basename(context['files'][0])
                suggestions.append(f"💡 '{draft}' is vague - specify what changed (e.g., 'fix {file_hint} validation')")
            else:
                suggestions.append(f"💡 Be more specific - what exactly changed?")
        
        # Check length
        if len(words) < 3 and not has_vague:
            if context and context.get('summary'):
                suggestions.append(f"💡 Add detail: {self._enhance_short_message(draft, context)}")
            else:
                suggestions.append("💡 Consider adding more detail to your message")
        
        # Conventional commits
        if context:
            commit_type = self._infer_commit_type(context)
            scope = self._infer_scope(context)
            
            is_conventional = any(draft_lower.startswith(ct) for ct in ['feat', 'fix', 'docs', 'test', 'chore', 'refactor', 'style', 'perf'])
            
            if not is_conventional and commit_type:
                if scope:
                    suggestions.append(f"💡 Conventional format: {commit_type}({scope}): {draft}")
                else:
                    suggestions.append(f"💡 Conventional format: {commit_type}: {draft}")
        
        # Action verb check
        action_verbs = ['add', 'fix', 'update', 'remove', 'refactor', 'docs', 'test', 'feat', 'chore', 'improve', 'optimize']
        if not any(draft_lower.startswith(verb) for verb in action_verbs):
            verb_suggestion = self._suggest_verb_from_context(context) if context else 'add'
            suggestions.append(f"💡 Start with action verb (e.g., '{verb_suggestion}: {draft}')")
        
        # Length check
        if len(draft) > 72:
            shortened = draft[:69] + '...'
            suggestions.append(f"💡 Shorten to <72 chars: '{shortened}'")
        
        # Capitalization
        if draft[0].isupper() and ':' not in draft[:10] and not draft_lower.startswith('feat'):
            suggestions.append("💡 Use lowercase for non-conventional commits or add type prefix")
        
        # Profile comparison
        if profile:
            avg_len = profile.get('avg_length', 50)
            if len(draft) < avg_len * 0.5:
                suggestions.append(f"💡 Your commits are usually {int(avg_len)} chars - add more context?")
        
        # Typo detection
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
    
    def adapt_from_history(self, profile):
        """Adapt suggestions based on user's commit history."""
        if not profile or not profile.get('commit_history'):
            return
        
        history = profile['commit_history']
        
        tones = [commit.get('tone', 'imperative') for commit in history]
        common_tone = max(set(tones), key=tones.count) if tones else 'imperative'
        
        profile['preferred_tone'] = common_tone
        profile['avg_length'] = sum(len(c.get('message', '')) for c in history) / len(history) if history else 50
        
        return profile


# Global instance
coach = CommitCoach()


# Convenience functions for CLI compatibility
def get_ai_suggestion(draft, context=None, profile=None, **kwargs):
    """Get commit message suggestions (heuristic-based)."""
    return coach.suggest_commit(draft, context, profile)


def is_ai_available():
    """Heuristic coach is always available."""
    return True


def get_ai_status():
    """Get AI status information."""
    return {
        'available': True,
        'reason': 'heuristic',
        'message': '✅ Heuristic coach available',
        'suggestion': '💡 For AI-powered suggestions, use: commit-checker --setup-ai'
    }
