"""YouGile Chats API client (Group Chats + Messages: 8 endpoints)."""

from typing import Dict, Any, List
from ..core.client import YouGileClient
from ..utils.validation import validate_uuid

# Group Chats (4 endpoints)
async def get_group_chats(client: YouGileClient) -> List[Dict[str, Any]]:
    return await client.get("/group-chats")

async def create_group_chat(client: YouGileClient, chat_data: Dict[str, Any]) -> Dict[str, Any]:
    return await client.post("/group-chats", json=chat_data)

async def get_group_chat(client: YouGileClient, chat_id: str) -> Dict[str, Any]:
    return await client.get(f"/group-chats/{validate_uuid(chat_id, 'chat_id')}")

async def update_group_chat(client: YouGileClient, chat_id: str, chat_data: Dict[str, Any]) -> Dict[str, Any]:
    return await client.put(f"/group-chats/{validate_uuid(chat_id, 'chat_id')}", json=chat_data)

# Chat Messages (4 endpoints)
async def get_chat_messages(client: YouGileClient, chat_id: str) -> List[Dict[str, Any]]:
    return await client.get(f"/chats/{validate_uuid(chat_id, 'chat_id')}/messages")

async def send_chat_message(client: YouGileClient, chat_id: str, message_data: Dict[str, Any]) -> Dict[str, Any]:
    return await client.post(f"/chats/{validate_uuid(chat_id, 'chat_id')}/messages", json=message_data)

async def get_chat_message(client: YouGileClient, chat_id: str, message_id: str) -> Dict[str, Any]:
    return await client.get(f"/chats/{validate_uuid(chat_id, 'chat_id')}/messages/{validate_uuid(message_id, 'message_id')}")

async def update_chat_message(client: YouGileClient, chat_id: str, message_id: str, message_data: Dict[str, Any]) -> Dict[str, Any]:
    return await client.put(f"/chats/{validate_uuid(chat_id, 'chat_id')}/messages/{validate_uuid(message_id, 'message_id')}", json=message_data)