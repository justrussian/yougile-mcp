"""YouGile Stickers API client (String + Sprint Stickers: 14 endpoints)."""

from typing import Dict, Any, List
from ..core.client import YouGileClient
from ..utils.validation import validate_uuid

# String Stickers (4 endpoints)
async def get_string_stickers(
    client: YouGileClient, 
    limit: int = 50, 
    offset: int = 0, 
    include_deleted: bool = False
) -> Dict[str, Any]:
    params = {
        "limit": limit,
        "offset": offset,
        "includeDeleted": include_deleted
    }
    return await client.get("/string-stickers", params=params)

async def create_string_sticker(client: YouGileClient, sticker_data: Dict[str, Any]) -> Dict[str, Any]:
    return await client.post("/string-stickers", json=sticker_data)

async def get_string_sticker(client: YouGileClient, sticker_id: str) -> Dict[str, Any]:
    return await client.get(f"/string-stickers/{validate_uuid(sticker_id, 'sticker_id')}")

async def update_string_sticker(client: YouGileClient, sticker_id: str, sticker_data: Dict[str, Any]) -> Dict[str, Any]:
    return await client.put(f"/string-stickers/{validate_uuid(sticker_id, 'sticker_id')}", json=sticker_data)

# String Sticker States (3 endpoints)
async def get_string_sticker_state(client: YouGileClient, sticker_id: str, state_id: str) -> Dict[str, Any]:
    return await client.get(f"/string-stickers/{validate_uuid(sticker_id, 'sticker_id')}/states/{state_id}")

async def update_string_sticker_state(client: YouGileClient, sticker_id: str, state_id: str, state_data: Dict[str, Any]) -> Dict[str, Any]:
    return await client.put(f"/string-stickers/{validate_uuid(sticker_id, 'sticker_id')}/states/{state_id}", json=state_data)

async def create_string_sticker_state(client: YouGileClient, sticker_id: str, state_data: Dict[str, Any]) -> Dict[str, Any]:
    return await client.post(f"/string-stickers/{validate_uuid(sticker_id, 'sticker_id')}/states", json=state_data)

# Sprint Stickers (4 endpoints) 
async def get_sprint_stickers(client: YouGileClient) -> List[Dict[str, Any]]:
    return await client.get("/sprint-stickers")

async def create_sprint_sticker(client: YouGileClient, sticker_data: Dict[str, Any]) -> Dict[str, Any]:
    return await client.post("/sprint-stickers", json=sticker_data)

async def get_sprint_sticker(client: YouGileClient, sticker_id: str) -> Dict[str, Any]:
    return await client.get(f"/sprint-stickers/{validate_uuid(sticker_id, 'sticker_id')}")

async def update_sprint_sticker(client: YouGileClient, sticker_id: str, sticker_data: Dict[str, Any]) -> Dict[str, Any]:
    return await client.put(f"/sprint-stickers/{validate_uuid(sticker_id, 'sticker_id')}", json=sticker_data)

# Sprint Sticker States (3 endpoints)
async def get_sprint_sticker_state(client: YouGileClient, sticker_id: str, state_id: str) -> Dict[str, Any]:
    return await client.get(f"/sprint-stickers/{validate_uuid(sticker_id, 'sticker_id')}/states/{validate_uuid(state_id, 'state_id')}")

async def update_sprint_sticker_state(client: YouGileClient, sticker_id: str, state_id: str, state_data: Dict[str, Any]) -> Dict[str, Any]:
    return await client.put(f"/sprint-stickers/{validate_uuid(sticker_id, 'sticker_id')}/states/{validate_uuid(state_id, 'state_id')}", json=state_data)

async def create_sprint_sticker_state(client: YouGileClient, sticker_id: str, state_data: Dict[str, Any]) -> Dict[str, Any]:
    return await client.post(f"/sprint-stickers/{validate_uuid(sticker_id, 'sticker_id')}/states", json=state_data)