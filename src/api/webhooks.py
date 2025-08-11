"""YouGile Webhooks API client (3 endpoints)."""

from typing import Dict, Any, List
from ..core.client import YouGileClient
from ..utils.validation import validate_uuid


async def create_webhook(client: YouGileClient, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create webhook subscription."""
    return await client.post("/webhooks", json=webhook_data)


async def get_webhooks(client: YouGileClient) -> List[Dict[str, Any]]:
    """Get list of webhook subscriptions."""
    return await client.get("/webhooks")


async def update_webhook(client: YouGileClient, webhook_id: str, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
    """Update webhook subscription."""
    return await client.put(f"/webhooks/{validate_uuid(webhook_id, 'webhook_id')}", json=webhook_data)