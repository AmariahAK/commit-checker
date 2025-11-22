"""Shared configuration management for commit-checker.

Handles:
- Centralized config storage (~/.commit-checker/config.json)
- API key encryption and secure storage
- Sync between CLI and VS Code extension
- User preferences and settings
- Migration from old config format
"""
import os
import json
import hashlib
from typing import Dict, Any, Optional
from datetime import datetime
import base64

# Config location
CONFIG_DIR = os.path.expanduser("~/.commit-checker")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
LEGACY_CONFIG_FILE = os.path.expanduser("~/.commit_checker_cache/config.json")

# Default configuration schema
DEFAULT_CONFIG = {
    "version": "1.0",
    "api_keys": {
        "together_ai": None,
        "openai": None,  # Future
    },
    "preferences": {
        "default_ai_model": "local",  # local, tensorflow, together_ai
        "ai_enabled": True,
        "selected_together_model": "meta-llama/Llama-3-70b-chat-hf",
        "theme": "pilgrimstack",
        "auto_suggest": False,
    },
    "user_profile": {
        "commit_style": {},
        "language_preferences": [],
        "last_profile_update": None,
    },
    "sync": {
        "last_sync": None,
        "sync_source": None,  # "cli" or "vscode"
    },
    "created_at": None,
    "last_updated": None,
}


def get_config_dir() -> str:
    """Get config directory, create if it doesn't exist."""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    return CONFIG_DIR


def _simple_encrypt(text: str, key: str = "commit-checker-key") -> str:
    """Simple XOR-based encryption for API keys.
    
    Note: This is NOT military-grade encryption, just basic obfuscation
    to prevent accidental exposure in config files.
    """
    if not text:
        return ""
    
    # Create key hash
    key_hash = hashlib.sha256(key.encode()).digest()
    
    # XOR encrypt
    encrypted = bytearray()
    for i, char in enumerate(text.encode()):
        encrypted.append(char ^ key_hash[i % len(key_hash)])
    
    # Base64 encode
    return base64.b64encode(bytes(encrypted)).decode()


def _simple_decrypt(encrypted_text: str, key: str = "commit-checker-key") -> str:
    """Decrypt API key."""
    if not encrypted_text:
        return ""
    
    try:
        # Base64 decode
        encrypted = base64.b64decode(encrypted_text.encode())
        
        # Create key hash
        key_hash = hashlib.sha256(key.encode()).digest()
        
        # XOR decrypt
        decrypted = bytearray()
        for i, byte in enumerate(encrypted):
            decrypted.append(byte ^ key_hash[i % len(key_hash)])
        
        return bytes(decrypted).decode()
    except Exception:
        return ""


def load_config() -> Dict[str, Any]:
    """Load configuration from file, create default if missing."""
    get_config_dir()  # Ensure directory exists
    
    # Try loading existing config
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Ensure all required keys exist (migration/safety)
            for key in DEFAULT_CONFIG:
                if key not in config:
                    config[key] = DEFAULT_CONFIG[key]
            
            return config
        except (json.JSONDecodeError, OSError):
            pass  # Fall through to create new
    
    # Check for legacy config and migrate
    if os.path.exists(LEGACY_CONFIG_FILE):
        migrated = migrate_from_legacy()
        if migrated:
            return migrated
    
    # Create new default config
    config = DEFAULT_CONFIG.copy()
    config["created_at"] = datetime.now().isoformat()
    config["last_updated"] = datetime.now().isoformat()
    save_config(config)
    return config


def save_config(config: Dict[str, Any]) -> bool:
    """Save configuration to file."""
    try:
        get_config_dir()
        config["last_updated"] = datetime.now().isoformat()
        
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        return True
    except (OSError, IOError) as e:
        print(f"⚠️  Could not save config: {e}")
        return False


def set_api_key(provider: str, api_key: str) -> bool:
    """Securely store an API key with encryption."""
    config = load_config()
    
    # Encrypt the key
    encrypted_key = _simple_encrypt(api_key)
    
    # Store
    config["api_keys"][provider] = encrypted_key
    config["sync"]["last_sync"] = datetime.now().isoformat()
    
    return save_config(config)


def get_api_key(provider: str) -> Optional[str]:
    """Retrieve and decrypt an API key."""
    config = load_config()
    encrypted_key = config.get("api_keys", {}).get(provider)
    
    if not encrypted_key:
        return None
    
    return _simple_decrypt(encrypted_key)


def delete_api_key(provider: str) -> bool:
    """Delete an API key from config."""
    config = load_config()
    
    if provider in config.get("api_keys", {}):
        config["api_keys"][provider] = None
        return save_config(config)
    
    return False


def clear_all_api_keys() -> bool:
    """Clear all API keys (for uninstall)."""
    config = load_config()
    for provider in config.get("api_keys", {}):
        config["api_keys"][provider] = None
    return save_config(config)


def update_preference(key: str, value: Any) -> bool:
    """Update a user preference."""
    config = load_config()
    config["preferences"][key] = value
    config["sync"]["last_sync"] = datetime.now().isoformat()
    return save_config(config)


def get_preference(key: str, default: Any = None) -> Any:
    """Get a user preference."""
    config = load_config()
    return config.get("preferences", {}).get(key, default)


def update_user_profile(profile_data: Dict[str, Any]) -> bool:
    """Update user profile data."""
    config = load_config()
    config["user_profile"].update(profile_data)
    config["user_profile"]["last_profile_update"] = datetime.now().isoformat()
    return save_config(config)


def get_user_profile() -> Dict[str, Any]:
    """Get user profile data."""
    config = load_config()
    return config.get("user_profile", {})


def mark_sync(source: str = "cli") -> bool:
    """Mark that a sync occurred from CLI or VS Code."""
    config = load_config()
    config["sync"]["last_sync"] = datetime.now().isoformat()
    config["sync"]["sync_source"] = source
    return save_config(config)


def migrate_from_legacy() -> Optional[Dict[str, Any]]:
    """Migrate from old config format if exists."""
    try:
        with open(LEGACY_CONFIG_FILE, 'r', encoding='utf-8') as f:
            old_config = json.load(f)
        
        # Create new config with old data
        new_config = DEFAULT_CONFIG.copy()
        new_config["created_at"] = datetime.now().isoformat()
        new_config["last_updated"] = datetime.now().isoformat()
        
        # Migrate what we can
        # (Old config might not have much, but preserve what exists)
        if "github_token" in old_config:
            # Encrypt and store
            token = old_config["github_token"]
            new_config["api_keys"]["github"] = _simple_encrypt(token)
        
        save_config(new_config)
        return new_config
        
    except (json.JSONDecodeError, OSError, IOError):
        return None


def get_config_file_path() -> str:
    """Get the full path to the config file."""
    return CONFIG_FILE


def delete_all_config() -> bool:
    """Delete all configuration (for complete uninstall)."""
    try:
        if os.path.exists(CONFIG_FILE):
            os.remove(CONFIG_FILE)
        # Optionally remove the directory if empty
        if os.path.exists(CONFIG_DIR) and not os.listdir(CONFIG_DIR):
            os.rmdir(CONFIG_DIR)
        return True
    except OSError:
        return False


# CLI helper functions
def print_config_status():
    """Print current configuration status."""
    config = load_config()
    
    print("\n🔧 Commit-Checker Configuration")
    print("=" * 50)
    print(f"📍 Location: {CONFIG_FILE}")
    print(f"📅 Last Updated: {config.get('last_updated', 'Unknown')}")
    print()
    
    print("🤖 AI Settings:")
    prefs = config.get("preferences", {})
    print(f"  • AI Enabled: {prefs.get('ai_enabled', False)}")
    print(f"  • Default Model: {prefs.get('default_ai_model', 'local')}")
    if prefs.get('default_ai_model') == 'together_ai':
        print(f"  • TogetherAI Model: {prefs.get('selected_together_model', 'N/A')}")
    print()
    
    print("🔑 API Keys:")
    api_keys = config.get("api_keys", {})
    for provider, encrypted_key in api_keys.items():
        if encrypted_key:
            # Show partial key for verification
            decrypted = _simple_decrypt(encrypted_key)
            masked = decrypted[:8] + "..." if len(decrypted) > 8 else "***"
            print(f"  • {provider.replace('_', ' ').title()}: {masked} ✓")
        else:
            print(f"  • {provider.replace('_', ' ').title()}: Not set")
    print()
    
    sync_info = config.get("sync", {})
    if sync_info.get("last_sync"):
        print(f"🔄 Last Sync: {sync_info['last_sync']} (from {sync_info.get('sync_source', '?')})")


if __name__ == "__main__":
    # Test the config system
    print("Testing config manager...")
    config = load_config()
    print("✓ Config loaded")
    print_config_status()
