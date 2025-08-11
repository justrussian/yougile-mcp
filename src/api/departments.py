"""
YouGile Departments API client.
Department hierarchy and management (4 endpoints).
"""

from typing import Dict, Any, List, Optional
from ..core.client import YouGileClient
from ..utils.validation import validate_uuid, validate_non_empty_string


async def get_departments(client: YouGileClient) -> List[Dict[str, Any]]:
    """Get list of departments."""
    response = await client.get("/departments")
    return response.get("content", [])


async def create_department(client: YouGileClient, department_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create new department."""
    return await client.post("/departments", json=department_data)


async def get_department(client: YouGileClient, department_id: str) -> Dict[str, Any]:
    """Get department by ID."""
    department_id = validate_uuid(department_id, "department_id")
    return await client.get(f"/departments/{department_id}")


async def update_department(client: YouGileClient, department_id: str, department_data: Dict[str, Any]) -> Dict[str, Any]:
    """Update department."""
    department_id = validate_uuid(department_id, "department_id")
    return await client.put(f"/departments/{department_id}", json=department_data)