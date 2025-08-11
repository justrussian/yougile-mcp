"""
Custom exceptions for YouGile MCP server.
Provides specific error types for different failure scenarios.
"""


class YouGileError(Exception):
    """Base exception for all YouGile API related errors."""
    
    def __init__(self, message: str, status_code: int = None, details: dict = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details or {}


class AuthenticationError(YouGileError):
    """Raised when authentication fails."""
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status_code=401)


class AuthorizationError(YouGileError):
    """Raised when user lacks permissions for an operation."""
    
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, status_code=403)


class RateLimitError(YouGileError):
    """Raised when API rate limit is exceeded."""
    
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, status_code=429)


class ValidationError(YouGileError):
    """Raised when input validation fails."""
    
    def __init__(self, message: str, field: str = None):
        super().__init__(message, status_code=400)
        self.field = field


class NotFoundError(YouGileError):
    """Raised when requested resource is not found."""
    
    def __init__(self, message: str, resource_type: str = None, resource_id: str = None):
        super().__init__(message, status_code=404)
        self.resource_type = resource_type
        self.resource_id = resource_id