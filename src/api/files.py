"""YouGile Files API client (1 endpoint)."""

from typing import Dict, Any
from ..core.client import YouGileClient


async def upload_file(client: YouGileClient, file_data: Dict[str, Any]) -> Dict[str, Any]:
    """Upload file to YouGile."""
    return await client.post("/upload-file", json=file_data)