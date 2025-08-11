"""
YouGile Users API client.
User management and invitations (5 endpoints).
"""

from typing import Dict, Any, List
from ..core.client import YouGileClient
from ..utils.validation import validate_uuid, validate_email


async def get_users(client: YouGileClient) -> List[Dict[str, Any]]:
    """Get list of users."""
    response = await client.get("/users")
    return response.get("content", [])


async def invite_user(client: YouGileClient, user_data: Dict[str, Any]) -> Dict[str, Any]:
    """Invite user to company."""
    return await client.post("/users", json=user_data)


async def get_user(client: YouGileClient, user_id: str) -> Dict[str, Any]:
    """Get user by ID."""
    user_id = validate_uuid(user_id, "user_id")
    return await client.get(f"/users/{user_id}")


async def update_user(client: YouGileClient, user_id: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
    """Update user."""
    user_id = validate_uuid(user_id, "user_id")
    return await client.put(f"/users/{user_id}", json=user_data)


async def delete_user(client: YouGileClient, user_id: str) -> Dict[str, Any]:
    """Remove user from company."""
    user_id = validate_uuid(user_id, "user_id")
    return await client.delete(f"/users/{user_id}")