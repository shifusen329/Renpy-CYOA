"""Configuration module for AI integration.

Loads environment variables and provides configuration management.
"""

import os
from dataclasses import dataclass
from typing import Optional
from pathlib import Path


@dataclass
class Config:
    """Configuration for AI backend integration."""
    
    # API Configuration
    api_base_url: str
    api_key: str
    
    # Model Configuration
    default_chat_model: str = "Dolphin-Mistral-24B-Venice-Edition"
    tts_model: str = "kokoro"
    tts_voice: str = "af_bella"  # Kokoro voice: American female, friendly
    
    # SD WebUI Configuration
    sd_webui_url: Optional[str] = None
    
    # Timeout Configuration (in seconds)
    connect_timeout: float = 5.0
    read_timeout: float = 30.0
    
    # Retry Configuration
    max_retries: int = 3
    retry_backoff: float = 1.0
    
    # Cache Configuration
    cache_dir: Path = Path("game/assets/cache")
    max_cache_age_days: int = 30
    
    # Performance Configuration
    enable_prefetch: bool = True
    prefetch_delay: float = 0.5
    
    def validate(self) -> None:
        """Validate configuration values."""
        if not self.api_base_url:
            raise ValueError("API_BASE_URL is required")
        if not self.api_key:
            raise ValueError("API_KEY is required")
        
        # Ensure URLs don't have trailing slashes
        self.api_base_url = self.api_base_url.rstrip('/')
        if self.sd_webui_url:
            self.sd_webui_url = self.sd_webui_url.rstrip('/')
        
        # Ensure cache directory exists
        self.cache_dir.mkdir(parents=True, exist_ok=True)


_config: Optional[Config] = None


def load_env() -> dict:
    """Load environment variables from .env file if it exists."""
    env_vars = {}
    env_file = Path(".env")
    
    if env_file.exists():
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        env_vars[key.strip()] = value.strip()
    
    # Override with actual environment variables
    for key in env_vars:
        if key in os.environ:
            env_vars[key] = os.environ[key]
    
    return env_vars


def get_config() -> Config:
    """Get or create the configuration singleton."""
    global _config
    
    if _config is None:
        env = load_env()
        
        # Create config from environment
        _config = Config(
            api_base_url=env.get('API_BASE_URL', ''),
            api_key=env.get('API_KEY', ''),
            default_chat_model=env.get('DEFAULT_CHAT_MODEL', 'Dolphin-Mistral-24B-Venice-Edition'),
            tts_model=env.get('TTS_MODEL', 'kokoro'),
            tts_voice=env.get('TTS_VOICE', 'af_heart'),
            sd_webui_url=env.get('SD_WEBUI_URL'),
            connect_timeout=float(env.get('CONNECT_TIMEOUT', '5.0')),
            read_timeout=float(env.get('READ_TIMEOUT', '30.0')),
            max_retries=int(env.get('MAX_RETRIES', '3')),
            retry_backoff=float(env.get('RETRY_BACKOFF', '1.0')),
            cache_dir=Path(env.get('CACHE_DIR', 'game/assets/cache')),
            max_cache_age_days=int(env.get('MAX_CACHE_AGE_DAYS', '30')),
            enable_prefetch=env.get('ENABLE_PREFETCH', 'true').lower() == 'true',
            prefetch_delay=float(env.get('PREFETCH_DELAY', '0.5'))
        )
        
        # Validate configuration
        _config.validate()
    
    return _config


def reset_config() -> None:
    """Reset the configuration singleton (useful for testing)."""
    global _config
    _config = None