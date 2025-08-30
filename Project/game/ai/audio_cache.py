"""Audio caching system for TTS with content-based hashing."""

import os
import hashlib
import logging
from typing import Optional, Tuple
from pathlib import Path

from config import get_config
from api import APIClient


logger = logging.getLogger(__name__)


class AudioCache:
    """Manages TTS audio caching with SHA256-based keys."""
    
    def __init__(self, cache_dir: Optional[str] = None):
        """Initialize audio cache manager.
        
        Args:
            cache_dir: Directory for cached audio files.
                      Defaults to game/assets/audio/tts/
        """
        self.config = get_config()
        
        # Set cache directory
        if cache_dir:
            self.cache_dir = Path(cache_dir)
        else:
            # Default to game/assets/audio/tts/
            try:
                import renpy
                game_dir = Path(renpy.config.gamedir)
                self.cache_dir = game_dir / "assets" / "audio" / "tts"
            except (ImportError, AttributeError):
                # Fallback for testing outside Ren'Py
                self.cache_dir = Path(__file__).parent.parent / "assets" / "audio" / "tts"
        
        # Ensure cache directory exists
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # API client for TTS generation
        self.api_client = APIClient(self.config)
        
        # Supported audio formats
        self.supported_formats = ['mp3', 'wav', 'ogg']
        self.default_format = 'mp3'
        
        logger.info(f"Audio cache initialized at: {self.cache_dir}")
    
    def _generate_cache_key(self, text: str, voice: str) -> str:
        """Generate cache key from text and voice.
        
        Args:
            text: Text content to speak
            voice: Voice ID/name
            
        Returns:
            SHA256 hash of voice + text
        """
        content = f"{voice}:{text}"
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def _get_cache_path(self, cache_key: str, format: str = None) -> Path:
        """Get full path for cached audio file.
        
        Args:
            cache_key: SHA256 cache key
            format: Audio format (mp3, wav, ogg)
            
        Returns:
            Path to cached file
        """
        format = format or self.default_format
        return self.cache_dir / f"{cache_key}.{format}"
    
    def get_tts_cached(self, text: str, voice: Optional[str] = None,
                      format: str = None) -> Optional[str]:
        """Get cached TTS audio or generate if missing.
        
        Args:
            text: Text to speak
            voice: Voice to use (defaults to config)
            format: Audio format
            
        Returns:
            Path to audio file or None if failed
        """
        # Use default voice if not specified
        voice = voice or self.config.tts_voice
        format = format or self.default_format
        
        # Generate cache key
        cache_key = self._generate_cache_key(text, voice)
        cache_path = self._get_cache_path(cache_key, format)
        
        # Check if cached file exists
        if cache_path.exists():
            logger.debug(f"Cache hit for TTS: {cache_key[:8]}...")
            return str(cache_path)
        
        # Generate new TTS audio
        logger.info(f"Cache miss, generating TTS for: {text[:50]}...")
        audio_data = self._generate_tts(text, voice)
        
        if audio_data:
            # Cache the audio data
            if self.cache_tts(audio_data, cache_key, format):
                return str(cache_path)
        
        return None
    
    def cache_tts(self, audio_data: bytes, cache_key: str, 
                  format: str = None) -> bool:
        """Save audio data to cache.
        
        Args:
            audio_data: Raw audio bytes
            cache_key: Cache key for the file
            format: Audio format
            
        Returns:
            True if cached successfully
        """
        try:
            format = format or self.default_format
            cache_path = self._get_cache_path(cache_key, format)
            
            # Write audio data to file
            with open(cache_path, 'wb') as f:
                f.write(audio_data)
            
            logger.info(f"Cached TTS audio: {cache_key[:8]}... ({len(audio_data)} bytes)")
            return True
            
        except Exception as e:
            logger.error(f"Failed to cache TTS audio: {e}")
            return False
    
    def _generate_tts(self, text: str, voice: str) -> Optional[bytes]:
        """Generate TTS audio using API.
        
        Args:
            text: Text to speak
            voice: Voice to use
            
        Returns:
            Audio data bytes or None if failed
        """
        try:
            audio_data = self.api_client.generate_speech(text, voice)
            if audio_data:
                logger.info(f"Generated TTS audio: {len(audio_data)} bytes")
                return audio_data
            else:
                logger.error("TTS generation returned no data")
                return None
                
        except Exception as e:
            logger.error(f"TTS generation error: {e}")
            return None
    
    def prefetch_tts(self, text: str, voice: Optional[str] = None) -> bool:
        """Prefetch TTS audio without blocking.
        
        Args:
            text: Text to prefetch
            voice: Voice to use
            
        Returns:
            True if already cached or generation started
        """
        voice = voice or self.config.tts_voice
        cache_key = self._generate_cache_key(text, voice)
        cache_path = self._get_cache_path(cache_key)
        
        # Already cached
        if cache_path.exists():
            return True
        
        # In a real implementation, this would start async generation
        # For now, we'll just note it for future implementation
        logger.debug(f"Prefetch requested for: {text[:50]}...")
        return True
    
    def get_cache_stats(self) -> dict:
        """Get cache statistics.
        
        Returns:
            Dict with cache stats
        """
        try:
            # Count cached files
            cached_files = list(self.cache_dir.glob("*.mp3")) + \
                          list(self.cache_dir.glob("*.wav")) + \
                          list(self.cache_dir.glob("*.ogg"))
            
            # Calculate total size
            total_size = sum(f.stat().st_size for f in cached_files)
            
            return {
                "cache_dir": str(self.cache_dir),
                "total_files": len(cached_files),
                "total_size": total_size,
                "total_size_mb": round(total_size / (1024 * 1024), 2)
            }
            
        except Exception as e:
            logger.error(f"Failed to get cache stats: {e}")
            return {
                "cache_dir": str(self.cache_dir),
                "total_files": 0,
                "total_size": 0,
                "total_size_mb": 0
            }
    
    def clear_cache(self) -> int:
        """Clear all cached audio files.
        
        Returns:
            Number of files removed
        """
        try:
            files_removed = 0
            for format in self.supported_formats:
                for file in self.cache_dir.glob(f"*.{format}"):
                    file.unlink()
                    files_removed += 1
            
            logger.info(f"Cleared {files_removed} cached audio files")
            return files_removed
            
        except Exception as e:
            logger.error(f"Failed to clear cache: {e}")
            return 0
    
    def verify_cache(self, text: str, voice: Optional[str] = None) -> bool:
        """Check if TTS audio is cached without generating.
        
        Args:
            text: Text to check
            voice: Voice to check
            
        Returns:
            True if cached, False otherwise
        """
        voice = voice or self.config.tts_voice
        cache_key = self._generate_cache_key(text, voice)
        cache_path = self._get_cache_path(cache_key)
        
        return cache_path.exists()


# Global audio cache instance
_audio_cache_instance = None


def get_audio_cache() -> AudioCache:
    """Get or create global audio cache instance.
    
    Returns:
        Global AudioCache instance
    """
    global _audio_cache_instance
    if _audio_cache_instance is None:
        _audio_cache_instance = AudioCache()
    return _audio_cache_instance


# Convenience functions for direct use
def get_or_generate_tts(text: str, voice: Optional[str] = None) -> Optional[str]:
    """Get cached TTS or generate new.
    
    Args:
        text: Text to speak
        voice: Voice to use
        
    Returns:
        Path to audio file or None
    """
    cache = get_audio_cache()
    return cache.get_tts_cached(text, voice)


def prefetch_tts(text: str, voice: Optional[str] = None) -> bool:
    """Prefetch TTS audio for later use.
    
    Args:
        text: Text to prefetch
        voice: Voice to use
        
    Returns:
        True if cached or prefetch started
    """
    cache = get_audio_cache()
    return cache.prefetch_tts(text, voice)


def clear_tts_cache() -> int:
    """Clear all cached TTS audio.
    
    Returns:
        Number of files removed
    """
    cache = get_audio_cache()
    return cache.clear_cache()