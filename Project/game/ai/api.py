"""HTTP client with retry logic for AI backend communication."""

import time
import json
import logging
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config import get_config


logger = logging.getLogger(__name__)


@dataclass
class APIResponse:
    """Wrapper for API responses."""
    status_code: int
    data: Optional[Union[dict, bytes]]
    error: Optional[str] = None
    
    @property
    def success(self) -> bool:
        return 200 <= self.status_code < 300 and self.error is None
    
    def json(self) -> dict:
        """Get JSON data from response."""
        if isinstance(self.data, dict):
            return self.data
        elif isinstance(self.data, bytes):
            return json.loads(self.data)
        return {}


class APIClient:
    """HTTP client with retry logic and connection pooling."""
    
    def __init__(self, config=None):
        """Initialize API client with configuration."""
        self.config = config or get_config()
        
        # Create session with connection pooling
        self.session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=self.config.max_retries,
            backoff_factor=self.config.retry_backoff,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST"]
        )
        
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=10,
            pool_maxsize=10
        )
        
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Set default headers
        self.session.headers.update({
            'Authorization': f'Bearer {self.config.api_key}',
            'Content-Type': 'application/json'
        })
    
    def _make_request(self, method: str, url: str, **kwargs) -> APIResponse:
        """Make HTTP request with error handling."""
        try:
            # Set timeouts
            kwargs.setdefault('timeout', (
                self.config.connect_timeout,
                self.config.read_timeout
            ))
            
            # Make request
            response = self.session.request(method, url, **kwargs)
            
            # Parse response
            if response.headers.get('content-type', '').startswith('application/json'):
                data = response.json()
            else:
                data = response.content
            
            return APIResponse(
                status_code=response.status_code,
                data=data
            )
            
        except requests.exceptions.Timeout as e:
            logger.error(f"Request timeout: {e}")
            return APIResponse(
                status_code=408,
                data=None,
                error=f"Request timeout: {str(e)}"
            )
            
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error: {e}")
            return APIResponse(
                status_code=503,
                data=None,
                error=f"Connection error: {str(e)}"
            )
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {e}")
            return APIResponse(
                status_code=500,
                data=None,
                error=f"Request error: {str(e)}"
            )
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            return APIResponse(
                status_code=response.status_code if 'response' in locals() else 500,
                data=response.content if 'response' in locals() else None,
                error=f"JSON decode error: {str(e)}"
            )
            
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return APIResponse(
                status_code=500,
                data=None,
                error=f"Unexpected error: {str(e)}"
            )
    
    def post_json(self, endpoint: str, data: Dict[str, Any], 
                  base_url: Optional[str] = None) -> APIResponse:
        """POST JSON data to endpoint."""
        base = base_url or self.config.api_base_url
        url = f"{base}{endpoint}"
        
        logger.debug(f"POST {url}")
        return self._make_request('POST', url, json=data)
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
            base_url: Optional[str] = None) -> APIResponse:
        """GET from endpoint."""
        base = base_url or self.config.api_base_url
        url = f"{base}{endpoint}"
        
        logger.debug(f"GET {url}")
        return self._make_request('GET', url, params=params)
    
    def post_binary(self, endpoint: str, data: bytes, 
                    content_type: str = 'application/octet-stream',
                    base_url: Optional[str] = None) -> APIResponse:
        """POST binary data to endpoint."""
        base = base_url or self.config.api_base_url
        url = f"{base}{endpoint}"
        
        logger.debug(f"POST (binary) {url}")
        
        # Temporarily override content-type
        old_content_type = self.session.headers.get('Content-Type')
        self.session.headers['Content-Type'] = content_type
        
        try:
            response = self._make_request('POST', url, data=data)
        finally:
            # Restore original content-type
            if old_content_type:
                self.session.headers['Content-Type'] = old_content_type
        
        return response
    
    def generate_text(self, prompt: str, model: Optional[str] = None,
                     temperature: float = 0.7, max_tokens: int = 2000) -> Optional[str]:
        """Generate text using the /api/generate endpoint."""
        data = {
            "prompt": prompt,
            "model": model or self.config.default_chat_model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        
        response = self.post_json("/api/generate", data)
        if response.success:
            result = response.json()
            return result.get("response", result.get("text", ""))
        
        logger.error(f"Text generation failed: {response.error}")
        return None
    
    def chat(self, messages: list, model: Optional[str] = None,
             temperature: float = 0.7, max_tokens: int = 2000) -> Optional[str]:
        """Chat using OpenAI-compatible endpoint."""
        data = {
            "model": model or self.config.default_chat_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        
        response = self.post_json("/v1/chat/completions", data)
        if response.success:
            result = response.json()
            choices = result.get("choices", [])
            if choices:
                return choices[0].get("message", {}).get("content", "")
        
        logger.error(f"Chat failed: {response.error}")
        return None
    
    def generate_image(self, prompt: str, negative_prompt: str = "",
                      width: int = 768, height: int = 512,
                      steps: int = 20, cfg_scale: float = 7.0) -> Optional[bytes]:
        """Generate image using Stable Diffusion WebUI."""
        if not self.config.sd_webui_url:
            logger.error("SD_WEBUI_URL not configured")
            return None
        
        data = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "width": width,
            "height": height,
            "steps": steps,
            "cfg_scale": cfg_scale,
            "sampler_name": "DPM++ 2M Karras",
            "batch_size": 1,
            "n_iter": 1
        }
        
        response = self.post_json("/sdapi/v1/txt2img", data, 
                                 base_url=self.config.sd_webui_url)
        if response.success:
            result = response.json()
            images = result.get("images", [])
            if images:
                import base64
                return base64.b64decode(images[0])
        
        logger.error(f"Image generation failed: {response.error}")
        return None
    
    def generate_speech(self, text: str, voice: Optional[str] = None,
                       model: Optional[str] = None) -> Optional[bytes]:
        """Generate speech using TTS endpoint."""
        data = {
            "input": text,
            "voice": voice or self.config.tts_voice,
            "model": model or self.config.tts_model,
            "response_format": "mp3"
        }
        
        response = self.post_json("/v1/audio/speech", data)
        if response.success:
            if isinstance(response.data, bytes):
                return response.data
            # If JSON response with base64 audio
            result = response.json()
            if "audio" in result:
                import base64
                return base64.b64decode(result["audio"])
        
        logger.error(f"Speech generation failed: {response.error}")
        return None
    
    def close(self):
        """Close the session and free resources."""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()