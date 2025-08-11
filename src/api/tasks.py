"""YouGile Tasks API client (7 endpoints)."""

from typing import Dict, Any, List, Optional
from ..core.client import YouGileClient
from ..utils.validation import validate_uuid


async def get_task_list(
    client: YouGileClient,
    limit: int = 50,
    offset: int = 0
) -> List[Dict[str, Any]]:
    """Get list of task summaries."""
    params = {
        "limit": limit,
        "offset": offset
    }
    response = await client.get("/task-list", params=params)
    return response.get("content", [])

async def get_tasks(
    client: YouGileClient,
    column_id: Optional[str] = None,
    assigned_to: Optional[str] = None,
    title: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    include_deleted: bool = False
) -> List[Dict[str, Any]]:
    """Get detailed list of tasks with optional filtering."""
    params = {
        "limit": limit,
        "offset": offset,
        "includeDeleted": include_deleted
    }
    
    if column_id:
        params["columnId"] = validate_uuid(column_id, "column_id")
    
    if assigned_to:
        params["assignedTo"] = assigned_to
    
    if title:
        params["title"] = title
    
    response = await client.get("/tasks", params=params)
    return response.get("content", [])

async def create_task(client: YouGileClient, task_data: Dict[str, Any]) -> Dict[str, Any]:
    return await client.post("/tasks", json=task_data)

async def get_task(client: YouGileClient, task_id: str) -> Dict[str, Any]:
    return await client.get(f"/tasks/{validate_uuid(task_id, 'task_id')}")

async def update_task(client: YouGileClient, task_id: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
    return await client.put(f"/tasks/{validate_uuid(task_id, 'task_id')}", json=task_data)

async def get_task_chat_subscribers(client: YouGileClient, task_id: str) -> List[Dict[str, Any]]:
    return await client.get(f"/tasks/{validate_uuid(task_id, 'task_id')}/chat-subscribers")

async def update_task_chat_subscribers(client: YouGileClient, task_id: str, subscribers: List[str]) -> Dict[str, Any]:
    return await client.put(f"/tasks/{validate_uuid(task_id, 'task_id')}/chat-subscribers", json={"subscribers": subscribers})

