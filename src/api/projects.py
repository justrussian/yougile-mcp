"""YouGile Projects API client (4 endpoints)."""

from typing import Dict, Any, List
from ..core.client import YouGileClient
from ..utils.validation import validate_uuid


async def get_projects(client: YouGileClient) -> List[Dict[str, Any]]:
    """Get list of projects."""
    response = await client.get("/projects")
    return response.get("content", [])


async def create_project(client: YouGileClient, project_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create new project."""
    return await client.post("/projects", json=project_data)


async def get_project(client: YouGileClient, project_id: str) -> Dict[str, Any]:
    """Get project by ID."""
    return await client.get(f"/projects/{validate_uuid(project_id, 'project_id')}")


async def update_project(client: YouGileClient, project_id: str, project_data: Dict[str, Any]) -> Dict[str, Any]:
    """Update project."""
    return await client.put(f"/projects/{validate_uuid(project_id, 'project_id')}", json=project_data)