"""
Authentication utilities for YouGile API.
Handles API key management and company selection.
"""

from typing import Optional, Dict, List
from .exceptions import AuthenticationError, ValidationError


class AuthManager:
    """Manages YouGile authentication and API keys."""
    
    def __init__(self, api_key: Optional[str] = None, company_id: Optional[str] = None):
        self._api_key = api_key
        self._company_id = company_id
    
    @property
    def api_key(self) -> Optional[str]:
        """Get current API key."""
        return self._api_key
    
    @property
    def company_id(self) -> Optional[str]:
        """Get current company ID."""
        return self._company_id
    
    def set_credentials(self, api_key: str, company_id: str) -> None:
        """Set API credentials."""
        if not api_key or not api_key.strip():
            raise ValidationError("API key cannot be empty")
        if not company_id or not company_id.strip():
            raise ValidationError("Company ID cannot be empty")
        
        self._api_key = api_key.strip()
        self._company_id = company_id.strip()
    
    def get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers for API requests."""
        if not self._api_key:
            raise AuthenticationError("No API key configured")
        
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
    
    def get_basic_headers(self) -> Dict[str, str]:
        """Get basic headers without API key (for auth endpoints)."""
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
    
    def is_authenticated(self) -> bool:
        """Check if authentication is configured."""
        return bool(self._api_key and self._company_id)
    
    def clear_credentials(self) -> None:
        """Clear stored credentials."""
        self._api_key = None
        self._company_id = None


# Global auth manager instance
auth_manager = AuthManager()