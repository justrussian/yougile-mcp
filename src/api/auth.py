"""
YouGile Authentication API client.
Handles login, API keys, and company access (4 endpoints).
"""

from typing import Dict, Any, List, Optional
from ..core.client import YouGileClient
from ..utils.validation import validate_required_fields, validate_email, validate_uuid


async def get_companies(
    client: YouGileClient,
    login: str,
    password: str, 
    limit: int = 50,
    offset: int = 0
) -> List[Dict[str, Any]]:
    """Get list of companies for user credentials."""
    credentials = {
        "login": validate_email(login),
        "password": password,
    }
    
    params = {"limit": limit, "offset": offset}
    
    response = await client.post("/auth/companies", json=credentials, params=params)
    return response.get("content", [])


async def get_api_keys(client: YouGileClient, login: str, password: str, company_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get list of API keys for user."""
    credentials = {
        "login": validate_email(login),
        "password": password,
    }
    
    if company_id:
        credentials["companyId"] = validate_uuid(company_id, "companyId")
    
    response = await client.post("/auth/keys/get", json=credentials)
    return response if isinstance(response, list) else []


async def create_api_key(client: YouGileClient, login: str, password: str, company_id: str) -> str:
    """Create new API key for company access."""
    credentials = {
        "login": validate_email(login),
        "password": password,
        "companyId": validate_uuid(company_id, "companyId"),
    }
    
    response = await client.post("/auth/keys", json=credentials)
    return response.get("key", "")


async def delete_api_key(client: YouGileClient, key: str) -> Dict[str, Any]:
    """Delete an API key."""
    if not key or not key.strip():
        raise ValueError("API key is required")
    
    return await client.delete(f"/auth/keys/{key.strip()}")