"""YouGile Project Roles API client (5 endpoints)."""

from typing import Dict, Any, List
from ..core.client import YouGileClient
from ..utils.validation import validate_uuid


async def get_project_roles(client: YouGileClient, project_id: str) -> List[Dict[str, Any]]:
    """Get project roles."""
    return await client.get(f"/projects/{validate_uuid(project_id, 'project_id')}/roles")


async def create_project_role(client: YouGileClient, project_id: str, role_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create project role."""
    return await client.post(f"/projects/{validate_uuid(project_id, 'project_id')}/roles", json=role_data)


async def get_project_role(client: YouGileClient, project_id: str, role_id: str) -> Dict[str, Any]:
    """Get project role by ID."""
    return await client.get(f"/projects/{validate_uuid(project_id, 'project_id')}/roles/{validate_uuid(role_id, 'role_id')}")


async def update_project_role(client: YouGileClient, project_id: str, role_id: str, role_data: Dict[str, Any]) -> Dict[str, Any]:
    """Update project role."""
    return await client.put(f"/projects/{validate_uuid(project_id, 'project_id')}/roles/{validate_uuid(role_id, 'role_id')}", json=role_data)


async def delete_project_role(client: YouGileClient, project_id: str, role_id: str) -> Dict[str, Any]:
    """Delete project role."""
    return await client.delete(f"/projects/{validate_uuid(project_id, 'project_id')}/roles/{validate_uuid(role_id, 'role_id')}")