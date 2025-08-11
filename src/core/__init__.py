"""Core utilities for YouGile MCP server."""

from .auth import AuthManager
from .client import YouGileClient
from .exceptions import (
    YouGileError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
)
from . import models

# Global authentication manager for MCP session
auth_manager = AuthManager()

__all__ = [
    "AuthManager",
    "YouGileClient", 
    "YouGileError",
    "AuthenticationError",
    "RateLimitError",
    "ValidationError",
    "models",
    "auth_manager",
]