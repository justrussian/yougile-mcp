"""
Input validation utilities.
Pure functions for validating various input types.
"""

import re
import uuid
from typing import Dict, Any, List
from ..core.exceptions import ValidationError


def validate_uuid(value: str, field_name: str = "id") -> str:
    """Validate UUID format."""
    if not value or not isinstance(value, str):
        raise ValidationError(f"{field_name} is required", field=field_name)
    
    try:
        uuid.UUID(value)
        return value.strip()
    except ValueError:
        raise ValidationError(f"{field_name} must be a valid UUID", field=field_name)


def validate_email(email: str) -> str:
    """Validate email format."""
    if not email or not isinstance(email, str):
        raise ValidationError("Email is required", field="email")
    
    email = email.strip().lower()
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        raise ValidationError("Invalid email format", field="email")
    
    return email


def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> None:
    """Validate that all required fields are present and not empty."""
    for field in required_fields:
        if field not in data:
            raise ValidationError(f"Field '{field}' is required", field=field)
        
        value = data[field]
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ValidationError(f"Field '{field}' cannot be empty", field=field)


def validate_pagination(limit: int = None, offset: int = None) -> Dict[str, int]:
    """Validate and normalize pagination parameters."""
    if limit is not None:
        if not isinstance(limit, int) or limit < 1 or limit > 1000:
            raise ValidationError("Limit must be between 1 and 1000", field="limit")
    else:
        limit = 50  # Default limit
    
    if offset is not None:
        if not isinstance(offset, int) or offset < 0:
            raise ValidationError("Offset must be non-negative", field="offset")
    else:
        offset = 0  # Default offset
    
    return {"limit": limit, "offset": offset}


def validate_non_empty_string(value: str, field_name: str, max_length: int = None) -> str:
    """Validate non-empty string with optional max length."""
    if not value or not isinstance(value, str):
        raise ValidationError(f"{field_name} is required", field=field_name)
    
    value = value.strip()
    if not value:
        raise ValidationError(f"{field_name} cannot be empty", field=field_name)
    
    if max_length and len(value) > max_length:
        raise ValidationError(
            f"{field_name} cannot exceed {max_length} characters",
            field=field_name
        )
    
    return value