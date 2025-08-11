"""
YouGile Company API client.
Company details and settings (2 endpoints).
"""

from typing import Dict, Any
from ..core.client import YouGileClient


async def get_company_details(client: YouGileClient) -> Dict[str, Any]:
    """Get company details."""
    return await client.get("/companies")


async def update_company(client: YouGileClient, company_data: Dict[str, Any]) -> Dict[str, Any]:
    """Update company settings."""
    return await client.put("/companies", json=company_data)