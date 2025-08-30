"""Content-based caching utilities for AI-generated assets."""

import os
import json
import hashlib
import shutil
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Union, Any

from config import get_config


logger = logging.getLogger(__name__)


class CacheManager:
    """Manages content-based caching for generated assets."""
    
    def __init__(self, cache_dir: Optional[Path] = None):
        """Initialize cache manager."""
        config = get_config()
        self.cache_dir = cache_dir or config.cache_dir
        self.max_age_days = config.max_cache_age_days
        
        # Ensure cache directory exists
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_hash(self, content: Union[str, bytes, dict]) -> str:
        """Generate SHA256 hash for content."""
        hasher = hashlib.sha256()
        
        if isinstance(content, str):
            hasher.update(content.encode('utf-8'))
        elif isinstance(content, bytes):
            hasher.update(content)
        elif isinstance(content, dict):
            # Sort keys for consistent hashing
            hasher.update(json.dumps(content, sort_keys=True).encode('utf-8'))
        else:
            raise TypeError(f"Unsupported content type: {type(content)}")
        
        return hasher.hexdigest()
    
    def _get_cache_path(self, cache_type: str, content_hash: str, 
                       extension: str = "") -> Path:
        """Get cache file path based on type and hash.
        
        Structure: cache_dir/type/hash[:2]/hash.ext
        """
        # Create subdirectory structure
        type_dir = self.cache_dir / cache_type
        hash_dir = type_dir / content_hash[:2]
        hash_dir.mkdir(parents=True, exist_ok=True)
        
        # Build filename
        filename = content_hash
        if extension:
            if not extension.startswith('.'):
                extension = '.' + extension
            filename += extension
        
        return hash_dir / filename
    
    def cache_exists(self, cache_type: str, content: Union[str, bytes, dict],
                    extension: str = "") -> bool:
        """Check if cached version exists."""
        content_hash = self._get_hash(content)
        cache_path = self._get_cache_path(cache_type, content_hash, extension)
        return cache_path.exists()
    
    def get_cached(self, cache_type: str, content: Union[str, bytes, dict],
                  extension: str = "", as_path: bool = False) -> Optional[Union[bytes, str, Path]]:
        """Get cached content if it exists.
        
        Args:
            cache_type: Type of cache (e.g., 'image', 'audio', 'text')
            content: Content to hash for cache key
            extension: File extension for cache file
            as_path: If True, return Path object instead of content
        
        Returns:
            Cached content as bytes/string, or Path if as_path=True, or None if not cached
        """
        content_hash = self._get_hash(content)
        cache_path = self._get_cache_path(cache_type, content_hash, extension)
        
        if not cache_path.exists():
            logger.debug(f"Cache miss: {cache_path}")
            return None
        
        logger.debug(f"Cache hit: {cache_path}")
        
        if as_path:
            return cache_path
        
        # Read and return content
        try:
            if cache_type in ['text', 'json']:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                with open(cache_path, 'rb') as f:
                    return f.read()
        except Exception as e:
            logger.error(f"Error reading cache file {cache_path}: {e}")
            return None
    
    def save_to_cache(self, cache_type: str, content: Union[str, bytes, dict],
                     data: Union[str, bytes], extension: str = "") -> Path:
        """Save data to cache.
        
        Args:
            cache_type: Type of cache (e.g., 'image', 'audio', 'text')
            content: Content to hash for cache key
            data: Data to save
            extension: File extension for cache file
        
        Returns:
            Path to cached file
        """
        content_hash = self._get_hash(content)
        cache_path = self._get_cache_path(cache_type, content_hash, extension)
        
        try:
            if isinstance(data, str):
                with open(cache_path, 'w', encoding='utf-8') as f:
                    f.write(data)
            else:
                with open(cache_path, 'wb') as f:
                    f.write(data)
            
            logger.debug(f"Saved to cache: {cache_path}")
            
            # Also save metadata
            self._save_metadata(cache_path, {
                'cache_type': cache_type,
                'content_hash': content_hash,
                'created': datetime.now().isoformat(),
                'size': len(data)
            })
            
            return cache_path
            
        except Exception as e:
            logger.error(f"Error saving to cache {cache_path}: {e}")
            raise
    
    def _save_metadata(self, cache_path: Path, metadata: dict):
        """Save metadata for cached file."""
        meta_path = cache_path.with_suffix(cache_path.suffix + '.meta')
        try:
            with open(meta_path, 'w') as f:
                json.dump(metadata, f, indent=2)
        except Exception as e:
            logger.warning(f"Failed to save metadata: {e}")
    
    def _load_metadata(self, cache_path: Path) -> Optional[dict]:
        """Load metadata for cached file."""
        meta_path = cache_path.with_suffix(cache_path.suffix + '.meta')
        if not meta_path.exists():
            return None
        
        try:
            with open(meta_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load metadata: {e}")
            return None
    
    def cleanup_old_entries(self, dry_run: bool = False) -> int:
        """Remove cache entries older than max_age_days.
        
        Args:
            dry_run: If True, only report what would be deleted
        
        Returns:
            Number of files deleted/would be deleted
        """
        cutoff_date = datetime.now() - timedelta(days=self.max_age_days)
        deleted_count = 0
        
        for cache_type_dir in self.cache_dir.iterdir():
            if not cache_type_dir.is_dir():
                continue
            
            for hash_dir in cache_type_dir.iterdir():
                if not hash_dir.is_dir():
                    continue
                
                for cache_file in hash_dir.iterdir():
                    if cache_file.suffix == '.meta':
                        continue
                    
                    # Check file age
                    try:
                        # Try to load metadata first
                        metadata = self._load_metadata(cache_file)
                        if metadata and 'created' in metadata:
                            created = datetime.fromisoformat(metadata['created'])
                        else:
                            # Fall back to file modification time
                            created = datetime.fromtimestamp(cache_file.stat().st_mtime)
                        
                        if created < cutoff_date:
                            if dry_run:
                                logger.info(f"Would delete: {cache_file}")
                            else:
                                cache_file.unlink()
                                # Also delete metadata
                                meta_file = cache_file.with_suffix(cache_file.suffix + '.meta')
                                if meta_file.exists():
                                    meta_file.unlink()
                                logger.info(f"Deleted old cache: {cache_file}")
                            deleted_count += 1
                            
                    except Exception as e:
                        logger.error(f"Error processing cache file {cache_file}: {e}")
        
        # Clean up empty directories
        if not dry_run:
            self._cleanup_empty_dirs()
        
        return deleted_count
    
    def _cleanup_empty_dirs(self):
        """Remove empty cache directories."""
        for cache_type_dir in self.cache_dir.iterdir():
            if not cache_type_dir.is_dir():
                continue
            
            for hash_dir in cache_type_dir.iterdir():
                if hash_dir.is_dir() and not any(hash_dir.iterdir()):
                    hash_dir.rmdir()
                    logger.debug(f"Removed empty directory: {hash_dir}")
            
            # Remove type directory if empty
            if not any(cache_type_dir.iterdir()):
                cache_type_dir.rmdir()
                logger.debug(f"Removed empty directory: {cache_type_dir}")
    
    def get_cache_stats(self) -> dict:
        """Get statistics about cache usage."""
        stats = {
            'total_files': 0,
            'total_size': 0,
            'by_type': {}
        }
        
        for cache_type_dir in self.cache_dir.iterdir():
            if not cache_type_dir.is_dir():
                continue
            
            type_name = cache_type_dir.name
            type_stats = {
                'files': 0,
                'size': 0
            }
            
            for hash_dir in cache_type_dir.iterdir():
                if not hash_dir.is_dir():
                    continue
                
                for cache_file in hash_dir.iterdir():
                    if cache_file.suffix == '.meta':
                        continue
                    
                    type_stats['files'] += 1
                    type_stats['size'] += cache_file.stat().st_size
            
            stats['by_type'][type_name] = type_stats
            stats['total_files'] += type_stats['files']
            stats['total_size'] += type_stats['size']
        
        return stats
    
    def clear_cache(self, cache_type: Optional[str] = None) -> int:
        """Clear all or specific type of cache.
        
        Args:
            cache_type: If specified, only clear this cache type
        
        Returns:
            Number of files deleted
        """
        deleted_count = 0
        
        if cache_type:
            cache_dir = self.cache_dir / cache_type
            if cache_dir.exists():
                shutil.rmtree(cache_dir)
                deleted_count = sum(1 for _ in cache_dir.rglob('*') if _.is_file())
                logger.info(f"Cleared {cache_type} cache: {deleted_count} files")
        else:
            for cache_type_dir in self.cache_dir.iterdir():
                if cache_type_dir.is_dir():
                    count = sum(1 for _ in cache_type_dir.rglob('*') if _.is_file())
                    shutil.rmtree(cache_type_dir)
                    deleted_count += count
            logger.info(f"Cleared all cache: {deleted_count} files")
        
        return deleted_count


# Global cache manager instance
_cache_manager: Optional[CacheManager] = None


def get_cache_manager() -> CacheManager:
    """Get or create the global cache manager instance."""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager()
    return _cache_manager


# Convenience functions
def cache_exists(cache_type: str, content: Union[str, bytes, dict],
                extension: str = "") -> bool:
    """Check if cached version exists."""
    return get_cache_manager().cache_exists(cache_type, content, extension)


def get_cached(cache_type: str, content: Union[str, bytes, dict],
              extension: str = "", as_path: bool = False) -> Optional[Union[bytes, str, Path]]:
    """Get cached content if it exists."""
    return get_cache_manager().get_cached(cache_type, content, extension, as_path)


def save_to_cache(cache_type: str, content: Union[str, bytes, dict],
                 data: Union[str, bytes], extension: str = "") -> Path:
    """Save data to cache."""
    return get_cache_manager().save_to_cache(cache_type, content, data, extension)