"""
HTTP client wrapper for YouGile API.
Handles requests, retries, rate limiting, and error handling.
"""

import asyncio
from typing import Optional, Dict, Any, Union
import httpx
from ..config import settings
from .auth import AuthManager
from .exceptions import (
    YouGileError,
    AuthenticationError,
    AuthorizationError,
    RateLimitError,
    NotFoundError,
)


class YouGileClient:
    """HTTP client for YouGile API with built-in error handling and retries."""
    
    def __init__(self, auth_manager: Optional[AuthManager] = None):
        self.auth_manager = auth_manager or AuthManager()
        self.base_url = settings.yougile_base_url
        self._client: Optional[httpx.AsyncClient] = None
    
    async def __aenter__(self):
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=httpx.Timeout(settings.yougile_timeout),
            limits=httpx.Limits(max_keepalive_connections=10, max_connections=100),
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.aclose()
    
    async def request(
        self,
        method: str,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Make an authenticated request to YouGile API."""
        if not self._client:
            raise RuntimeError("Client not initialized. Use 'async with' context manager.")
        
        # Use basic headers for auth endpoints, auth headers for others
        if path.startswith("/auth/") or path.startswith("/api-v2/auth/"):
            headers = self.auth_manager.get_basic_headers()
        else:
            headers = self.auth_manager.get_auth_headers()
            
        full_url = f"/api-v2{path}" if not path.startswith("/api-v2") else path
        
        for attempt in range(settings.yougile_max_retries + 1):
            try:
                response = await self._client.request(
                    method=method,
                    url=full_url,
                    json=json,
                    params=params,
                    headers=headers,
                    **kwargs
                )
                
                return self._handle_response(response)
                
            except httpx.TimeoutException:
                if attempt == settings.yougile_max_retries:
                    raise YouGileError("Request timeout")
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
                
            except httpx.NetworkError as e:
                if attempt == settings.yougile_max_retries:
                    raise YouGileError(f"Network error: {str(e)}")
                await asyncio.sleep(2 ** attempt)
        
        raise YouGileError("Max retries exceeded")
    
    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        """Handle HTTP response and convert errors to exceptions."""
        if response.status_code == 200 or response.status_code == 201:
            try:
                return response.json()
            except ValueError:
                return {"success": True, "data": response.text}
        
        # Handle error responses
        error_data = {}
        try:
            error_data = response.json()
        except ValueError:
            error_data = {"error": response.text or f"HTTP {response.status_code}"}
        
        error_message = error_data.get("error", f"HTTP {response.status_code}")
        
        if response.status_code == 401:
            raise AuthenticationError(error_message)
        elif response.status_code == 403:
            raise AuthorizationError(error_message)
        elif response.status_code == 404:
            raise NotFoundError(error_message)
        elif response.status_code == 429:
            raise RateLimitError(error_message)
        else:
            raise YouGileError(error_message, status_code=response.status_code, details=error_data)
    
    # Convenience methods
    async def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make GET request."""
        return await self.request("GET", path, params=params)
    
    async def post(self, path: str, json: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make POST request.""" 
        return await self.request("POST", path, json=json, params=params)
    
    async def put(self, path: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make PUT request."""
        return await self.request("PUT", path, json=json)
    
    async def delete(self, path: str) -> Dict[str, Any]:
        """Make DELETE request."""
        return await self.request("DELETE", path)