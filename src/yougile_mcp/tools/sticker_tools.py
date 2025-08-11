"""
YouGile Stickers MCP tools.
String and Sprint sticker operations.
"""

from typing import List, Dict, Any, Optional
from mcp.server.fastmcp import Context
from ...core import auth
from ...core.client import YouGileClient
from ...core.exceptions import YouGileError, ValidationError
from ...api import stickers
from ...utils.validation import validate_uuid


async def list_string_stickers_tool(
    limit: int = 50,
    offset: int = 0,
    include_deleted: bool = False,
    ctx: Context = None
) -> List[Dict[str, Any]]:
    """Get list of string (custom) stickers with their basic information."""
    try:
        if ctx:
            await ctx.info(f"Fetching string stickers (limit: {limit}, offset: {offset})...")
        
        async with YouGileClient(auth.auth_manager) as client:
            result = await stickers.get_string_stickers(client, limit, offset, include_deleted)
            
        # Extract content from paginated response
        sticker_list = result.get("content", [])
        
        if ctx:
            await ctx.info(f" Successfully retrieved {len(sticker_list)} string stickers")
        return sticker_list
        
    except YouGileError as e:
        if ctx:
            await ctx.error(f"API error while fetching string stickers: {e.message}")
        raise
    except Exception as e:
        if ctx:
            await ctx.error(f"Unexpected error: {str(e)}")
        raise


async def get_string_sticker_tool(sticker_id: str, ctx: Context = None) -> Dict[str, Any]:
    """Get detailed information about a specific string sticker including its states."""
    try:
        if ctx:
            await ctx.info(f"Fetching string sticker details: {sticker_id}")
        
        sticker_id = validate_uuid(sticker_id, "sticker_id")
        
        async with YouGileClient(auth.auth_manager) as client:
            result = await stickers.get_string_sticker(client, sticker_id)
            
        if ctx:
            await ctx.info(f" Successfully retrieved sticker: {result.get('name', sticker_id)}")
        return result
        
    except ValidationError as e:
        if ctx:
            await ctx.error(f"Validation failed: {e.message}")
        raise
    except YouGileError as e:
        if ctx:
            await ctx.error(f"API error while fetching string sticker: {e.message}")
        raise
    except Exception as e:
        if ctx:
            await ctx.error(f"Unexpected error: {str(e)}")
        raise


async def get_string_sticker_state_tool(
    sticker_id: str, 
    state_id: str, 
    ctx: Context = None
) -> Dict[str, Any]:
    """Get information about a specific state of a string sticker."""
    try:
        if ctx:
            await ctx.info(f"Fetching sticker state: {sticker_id}/{state_id}")
        
        sticker_id = validate_uuid(sticker_id, "sticker_id")
        # state_id can be short hex format, no strict validation needed
        if not state_id or not isinstance(state_id, str):
            raise ValidationError("state_id is required", field="state_id")
        state_id = state_id.strip()
        
        async with YouGileClient(auth.auth_manager) as client:
            result = await stickers.get_string_sticker_state(client, sticker_id, state_id)
            
        if ctx:
            await ctx.info(f" Successfully retrieved sticker state: {result.get('name', state_id)}")
        return result
        
    except ValidationError as e:
        if ctx:
            await ctx.error(f"Validation failed: {e.message}")
        raise
    except YouGileError as e:
        if ctx:
            await ctx.error(f"API error while fetching sticker state: {e.message}")
        raise
    except Exception as e:
        if ctx:
            await ctx.error(f"Unexpected error: {str(e)}")
        raise


async def decode_task_stickers_tool(
    stickers_dict: Dict[str, str], 
    ctx: Context = None
) -> Dict[str, Dict[str, Any]]:
    """Decode task stickers dictionary into readable sticker and state information."""
    try:
        if ctx:
            await ctx.info(f"Decoding {len(stickers_dict)} task stickers...")
        
        decoded_stickers = {}
        
        async with YouGileClient(auth.auth_manager) as client:
            for sticker_id, state_id in stickers_dict.items():
                try:
                    # Get sticker information
                    sticker_info = await stickers.get_string_sticker(client, sticker_id)
                    
                    # Get state information
                    state_info = await stickers.get_string_sticker_state(client, sticker_id, state_id)
                    
                    decoded_stickers[sticker_id] = {
                        "sticker": {
                            "id": sticker_id,
                            "name": sticker_info.get("name", "Unknown"),
                            "icon": sticker_info.get("icon", ""),
                        },
                        "state": {
                            "id": state_id,
                            "name": state_info.get("name", "Unknown"),
                            "color": state_info.get("color", "#000000")
                        }
                    }
                    
                except Exception as e:
                    # If we can't decode a specific sticker, include error info
                    decoded_stickers[sticker_id] = {
                        "sticker": {"id": sticker_id, "name": "Error loading sticker"},
                        "state": {"id": state_id, "name": "Error loading state"},
                        "error": str(e)
                    }
        
        if ctx:
            await ctx.info(f" Successfully decoded {len(decoded_stickers)} stickers")
        return decoded_stickers
        
    except Exception as e:
        if ctx:
            await ctx.error(f"Unexpected error while decoding stickers: {str(e)}")
        raise