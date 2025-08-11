"""
Helper for authentication in MCP tools.
Ensures authentication is initialized for each tool call.
"""

from mcp.server.fastmcp import Context
from ...core import auth


async def ensure_authenticated(ctx: Context) -> None:
    """Ensure authentication is initialized for YouGile API access."""
    if not auth.auth_manager.is_authenticated():
        await ctx.info("Initializing YouGile authentication...")
        
        # Debug: Show what credentials we have
        from ...config import settings
        await ctx.info(f"Email configured: {bool(settings.yougile_email)}")
        await ctx.info(f"Password configured: {bool(settings.yougile_password)}")
        await ctx.info(f"Company ID configured: {bool(settings.yougile_company_id)}")
        await ctx.info(f"API Key configured: {bool(settings.yougile_api_key)}")
        
        # Check if all required credentials are present
        if not settings.yougile_email:
            await ctx.error("YOUGILE_EMAIL not found in environment")
        if not settings.yougile_password:
            await ctx.error("YOUGILE_PASSWORD not found in environment")
        if not settings.yougile_company_id:
            await ctx.error("YOUGILE_COMPANY_ID not found in environment")
        
        from ...server import initialize_auth
        success = await initialize_auth()
        if not success:
            raise Exception("Failed to initialize YouGile authentication. Check credentials.")
        await ctx.info("Authentication initialized successfully")