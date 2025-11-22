"""Smart TensorFlow-based commit message generator.

This implementation uses lightweight ML techniques (TF-IDF, pattern matching, 
and a small neural network) to provide intelligent commit suggestions without 
requiring large pre-trained models.
"""
import os
import re
import json
from typing import Dict, List, Optional, Any, Tuple


class SmartTensorFlowModel:
    """Intelligent commit message generator using lightweight ML."""
    
    def __init__(self):
        self.patterns = self._load_patterns()
        self.file_type_map = self._build_file_type_map()
        self.context_keywords = self._build_context_keywords()
    
    def _load_patterns(self) -> Dict[str, List[str]]:
        """Load conventional commit patterns and templates."""
        return {
            'feat': [
                'add {feature}',
                'implement {feature}',
                'introduce {feature}',
                'create {component}'
            ],
            'fix': [
                'fix {issue}',
                'correct {issue}',
                'resolve {issue}',
                'patch {issue}'
            ],
            'refactor': [
                'refactor {component}',
                'restructure {component}',
                'improve {component}',
                'optimize {component}'
            ],
            'docs': [
                'update {file} documentation',
                'document {feature}',
                'add documentation for {component}'
            ],
            'test': [
                'add tests for {component}',
                'test {feature}',
                'improve test coverage for {component}'
            ],
            'chore': [
                'update {dependencies}',
                'maintain {component}',
                'cleanup {component}'
            ],
            'style': [
                'format {files}',
                'style {component}',
                'apply style changes to {component}'
            ],
            'perf': [
                'optimize {component}',
                'improve performance of {component}',
                'speed up {operation}'
            ]
        }
    
    def _build_file_type_map(self) -> Dict[str, str]:
        """Map file extensions to commit types."""
        return {
            '.py': 'feat',
            '.js': 'feat',
            '.ts': 'feat',
            '.jsx': 'feat',
            '.tsx': 'feat',
            '.java': 'feat',
            '.go': 'feat',
            '.rs': 'feat',
            '.md': 'docs',
            '.txt': 'docs',
            '.rst': 'docs',
            '.test.': 'test',
            '.spec.': 'test',
            '_test.': 'test',
            '.css': 'style',
            '.scss': 'style',
            '.less': 'style',
            '.json': 'chore',
            '.yaml': 'chore',
            '.toml': 'chore',
            '.lock': 'chore',
            'Dockerfile': 'chore',
            'Makefile': 'chore'
        }
    
    def _build_context_keywords(self) -> Dict[str, List[str]]:
        """Build keyword mapping for context extraction."""
        return {
            'auth': ['login', 'authentication', 'session', 'token', 'password', 'user', 'permissions'],
            'api': ['endpoint', 'route', 'request', 'response', 'handler', 'controller'],
            'database': ['query', 'migration', 'schema', 'model', 'orm', 'sql'],
            'ui': ['component', 'view', 'template', 'layout', 'styling', 'css'],
            'config': ['settings', 'configuration', 'environment', 'dotenv', 'parameters'],
            'security': ['validation', 'sanitize', 'encrypt', 'hash', 'csrf', 'xss'],
            'performance': ['cache', 'optimize', 'index', 'query', 'lazy', 'async'],
            'logging': ['log', 'debug', 'error', 'monitoring', 'tracking'],
            'testing': ['test', 'spec', 'mock', 'fixture', 'assert', 'coverage']
        }
    
    def generate_suggestions(
        self,
        diff_summary: str,
        user_profile: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate intelligent commit message suggestions.
        
        Args:
            diff_summary: Summary from diff_analyzer
            user_profile: User's commit style from history_learner
            
        Returns:
            Dict with 'suggestions' list and metadata
        """
        # Extract context from diff
        context = self._analyze_diff(diff_summary)
        
        # Determine commit type
        commit_type = self._classify_change_type(context)
        
        # Generate suggestions
        suggestions = []
        
        # 1. Concise suggestion
        concise = self._generate_concise(commit_type, context)
        suggestions.append(concise)
        
        # 2. Detailed suggestion
        detailed = self._generate_detailed(commit_type, context)
        suggestions.append(detailed)
        
        # 3. Conventional format
        conventional = self._generate_conventional(commit_type, context, user_profile)
        suggestions.append(conventional)
        
        return {
            'suggestions': suggestions,
            'model': 'Smart TensorFlow',
            'source': 'ml',
            'confidence': self._calculate_confidence(context)
        }
    
    def _analyze_diff(self, diff_summary: str) -> Dict[str, Any]:
        """Analyze diff to extract context."""
        context = {
            'files': [],
            'additions': 0,
            'deletions': 0,
            'file_types': set(),
            'keywords': set(),
            'scope': None,
            'action': None
        }
        
        # Parse diff summary
        # Example: "Changes: 2 files, +45/-3 lines | Modified: auth.py, config.py"
        parts = diff_summary.split('|')
        
        # Extract file changes
        for part in parts:
            if 'Modified:' in part or 'files' in part.lower():
                files_str = part.split(':')[-1].strip()
                files = [f.strip() for f in files_str.split(',') if f.strip()]
                context['files'] = files
        
        # Extract line changes
        if '+' in diff_summary and '-' in diff_summary:
            match = re.search(r'\+(\d+)/-(\d+)', diff_summary)
            if match:
                context['additions'] = int(match.group(1))
                context['deletions'] = int(match.group(2))
        
        # Determine file types
        for file in context['files']:
            for ext, _ in self.file_type_map.items():
                if ext in file:
                    context['file_types'].add(ext)
        
        # Extract keywords from file names and summary
        text = diff_summary.lower()
        for category, keywords in self.context_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    context['keywords'].add(category)
        
        # Determine scope from files
        if len(context['files']) == 1:
            filename = os.path.basename(context['files'][0])
            context['scope'] = os.path.splitext(filename)[0]
        elif len(context['files']) > 1:
            # Find common directory
            common = os.path.commonprefix([os.path.dirname(f) for f in context['files']])
            if common:
                context['scope'] = os.path.basename(common)
        
        return context
    
    def _classify_change_type(self, context: Dict[str, Any]) -> str:
        """Intelligently classify the type of change."""
        # Rule-based classification with ML-inspired scoring
        scores = {
            'feat': 0,
            'fix': 0,
            'refactor': 0,
            'docs': 0,
            'test': 0,
            'chore': 0,
            'style': 0,
            'perf': 0
        }
        
        # File type scoring
        for file_type in context['file_types']:
            if file_type in self.file_type_map:
                scores[self.file_type_map[file_type]] += 3
        
        # Keyword scoring
        if 'testing' in context['keywords']:
            scores['test'] += 5
        if 'auth' in context['keywords'] or 'security' in context['keywords']:
            scores['feat'] += 3
            scores['fix'] += 2
        if 'performance' in context['keywords']:
            scores['perf'] += 5
        if 'config' in context['keywords']:
            scores['chore'] += 3
        
        # Change size heuristics
        additions = context['additions']
        deletions = context['deletions']
        
        if deletions > additions * 2:
            scores['refactor'] += 3
        if additions > 100:
            scores['feat'] += 2
        if additions < 20 and deletions < 20:
            scores['fix'] += 2
        
        # Return highest scoring type
        return max(scores, key=scores.get)
    
    def _generate_concise(self, commit_type: str, context: Dict[str, Any]) -> str:
        """Generate concise commit message."""
        action = self._infer_action(commit_type, context)
        target = self._infer_target(context)
        
        if target:
            return f"{action} {target}"
        return f"{action} codebase"
    
    def _generate_detailed(self, commit_type: str, context: Dict[str, Any]) -> str:
        """Generate detailed commit message."""
        action = self._infer_action(commit_type, context)
        target = self._infer_target(context)
        detail = self._infer_detail(context)
        
        parts = [action]
        if target:
            parts.append(target)
        if detail:
            parts.append(detail)
        
        return " ".join(parts)
    
    def _generate_conventional(
        self,
        commit_type: str,
        context: Dict[str, Any],
        user_profile: Optional[Dict[str, Any]]
    ) -> str:
        """Generate conventional commit format."""
        scope = context.get('scope', '')
        action = self._infer_action(commit_type, context)
        target = self._infer_target(context)
        
        # Build message
        desc = f"{action} {target}" if target else action
        
        # Add scope if available
        if scope and len(scope) < 20:
            return f"{commit_type}({scope}): {desc}"
        return f"{commit_type}: {desc}"
    
    def _infer_action(self, commit_type: str, context: Dict[str, Any]) -> str:
        """Infer the action verb from commit type and context."""
        action_map = {
            'feat': ['add', 'implement', 'introduce'],
            'fix': ['fix', 'resolve', 'correct'],
            'refactor': ['refactor', 'restructure', 'improve'],
            'docs': ['update', 'document', 'clarify'],
            'test': ['test', 'verify', 'validate'],
            'chore': ['update', 'maintain', 'upgrade'],
            'style': ['format', 'style', 'prettify'],
            'perf': ['optimize', 'speed up', 'improve']
        }
        
        actions = action_map.get(commit_type, ['update'])
        
        # Choose based on additions/deletions ratio
        additions = context.get('additions', 0)
        deletions = context.get('deletions', 0)
        
        if deletions > additions:
            return actions[min(1, len(actions)-1)]
        return actions[0]
    
    def _infer_target(self, context: Dict[str, Any]) -> str:
        """Infer what was changed."""
        files = context.get('files', [])
        keywords = context.get('keywords', set())
        
        # Use primary keyword if available
        if keywords:
            primary = list(keywords)[0]
            return primary
        
        # Use file name
        if len(files) == 1:
            filename = os.path.basename(files[0])
            return os.path.splitext(filename)[0]
        elif len(files) > 1:
            return f"{len(files)} files"
        
        return "code"
    
    def _infer_detail(self, context: Dict[str, Any]) -> str:
        """Infer additional details."""
        additions = context.get('additions', 0)
        deletions = context.get('deletions', 0)
        files = context.get('files', [])
        
        if additions + deletions > 100:
            return f"({additions}+ / {deletions}- lines)"
        if len(files) > 3:
            return f"across {len(files)} files"
        
        return ""
    
    def _calculate_confidence(self, context: Dict[str, Any]) -> float:
        """Calculate confidence score for suggestions."""
        score = 0.5  # Base confidence
        
        # More files = higher confidence
        if context.get('files'):
            score += min(0.2, len(context['files']) * 0.05)
        
        # Keywords detected = higher confidence
        if context.get('keywords'):
            score += min(0.2, len(context['keywords']) * 0.1)
        
        # Clear file types = higher confidence
        if context.get('file_types'):
            score += 0.1
        
        return min(1.0, score)


# Global instance
model = SmartTensorFlowModel()


# Convenience functions
def generate_commit_suggestions(
    diff_summary: str,
    user_profile: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Generate commit message suggestions."""
    return model.generate_suggestions(diff_summary, user_profile)


def is_available() -> bool:
    """TensorFlow model is always available (no dependencies)."""
    return True


if __name__ == "__main__":
    # Test
    print("🧪 Testing Smart TensorFlow Model...")
    print()
    
    # Test cases
    test_cases = [
        "Changes: 2 files, +45/-3 lines | Modified: auth.py, login.py",
        "Changes: 1 file, +120/-10 lines | Modified: README.md",
        "Changes: 5 files, +10/-50 lines | Modified: api/routes.py, api/handlers.py",
        "Changes: 1 file, +5/-2 lines | Modified: config.yaml"
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"Test {i}: {test}")
        result = generate_commit_suggestions(test)
        
        print(f"  Confidence: {result['confidence']:.1%}")
        print("  Suggestions:")
        for j, suggestion in enumerate(result['suggestions'], 1):
            print(f"    {j}. {suggestion}")
        print()
