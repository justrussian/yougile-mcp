"""YouGile Columns API client (4 endpoints)."""

from typing import Dict, Any, List, Optional
from ..core.client import YouGileClient
from ..utils.validation import validate_uuid


async def get_columns(
    client: YouGileClient,
    board_id: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Get list of columns with optional filtering by board."""
    params = {}
    
    if board_id:
        from ..utils.validation import validate_uuid
        params["boardId"] = validate_uuid(board_id, "board_id")
    
    response = await client.get("/columns", params=params)
    return response.get("content", [])

async def create_column(client: YouGileClient, column_data: Dict[str, Any]) -> Dict[str, Any]:
    return await client.post("/columns", json=column_data)

async def get_column(client: YouGileClient, column_id: str) -> Dict[str, Any]:
    return await client.get(f"/columns/{validate_uuid(column_id, 'column_id')}")

async def update_column(client: YouGileClient, column_id: str, column_data: Dict[str, Any]) -> Dict[str, Any]:
    return await client.put(f"/columns/{validate_uuid(column_id, 'column_id')}", json=column_data)