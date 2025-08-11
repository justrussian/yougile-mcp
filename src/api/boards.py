"""YouGile Boards API client (4 endpoints)."""

from typing import Dict, Any, List, Optional
from ..core.client import YouGileClient
from ..utils.validation import validate_uuid


async def get_boards(
    client: YouGileClient,
    project_id: Optional[str] = None,
    title: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    include_deleted: bool = False
) -> List[Dict[str, Any]]:
    """Get list of boards with optional filtering."""
    params = {
        "limit": limit,
        "offset": offset,
        "includeDeleted": include_deleted
    }
    
    if project_id:
        params["projectId"] = validate_uuid(project_id, "project_id")
    
    if title:
        params["title"] = title
    
    response = await client.get("/boards", params=params)
    return response.get("content", [])

async def create_board(client: YouGileClient, board_data: Dict[str, Any]) -> Dict[str, Any]:
    return await client.post("/boards", json=board_data)

async def get_board(client: YouGileClient, board_id: str) -> Dict[str, Any]:
    return await client.get(f"/boards/{validate_uuid(board_id, 'board_id')}")

async def update_board(client: YouGileClient, board_id: str, board_data: Dict[str, Any]) -> Dict[str, Any]:
    return await client.put(f"/boards/{validate_uuid(board_id, 'board_id')}", json=board_data)