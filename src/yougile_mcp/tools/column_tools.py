"""
YouGile Columns MCP tools.
Column operations and board structure management (4 endpoints).
"""

from typing import List, Dict, Any, Optional
from mcp.server.fastmcp import Context
from ...core import models
from ...core import auth
from ...core.client import YouGileClient
from ...core.exceptions import YouGileError, ValidationError
from ...api import columns
from ...utils.validation import validate_uuid, validate_non_empty_string


async def list_columns_tool(
    board_id: Optional[str] = None,
    ctx: Context = None
) -> List[Dict[str, Any]]:
    """Get list of columns with optional filtering by board.
    
    Args:
        board_id: Filter columns by specific board ID
    """
    try:
        if board_id:
            board_id = validate_uuid(board_id, "board_id")
            await ctx.info(f"Fetching columns from board: {board_id}")
        else:
            await ctx.info("Fetching all columns from YouGile...")
        
        async with YouGileClient(auth.auth_manager) as client:
            result = await columns.get_columns(client, board_id=board_id)
            
        await ctx.info(f"✅ Successfully retrieved {len(result)} columns")
        return result
        
    except ValidationError as e:
        await ctx.error(f"Validation failed: {e.message}")
        raise
    except YouGileError as e:
        await ctx.error(f"API error while fetching columns: {e.message}")
        raise
    except Exception as e:
        await ctx.error(f"Unexpected error: {str(e)}")
        raise


async def create_column_tool(
    title: str,
    board_id: str,
    color: int = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """Create a new column in a board."""
    try:
        await ctx.info(f"Creating column: {title}")
        
        # Validate inputs
        title = validate_non_empty_string(title, "title")
        board_id = validate_uuid(board_id, "board_id")
        
        column_data = {
            "title": title,
            "boardId": board_id
        }
        
        if color is not None:
            if not (1 <= color <= 16):
                raise ValidationError("Color must be between 1 and 16")
            column_data["color"] = color
        
        async with YouGileClient(auth.auth_manager) as client:
            result = await columns.create_column(client, column_data)
            
        await ctx.info(f"✅ Successfully created column: {title}")
        return result
        
    except ValidationError as e:
        await ctx.error(f"Validation failed: {e.message}")
        raise
    except YouGileError as e:
        await ctx.error(f"API error while creating column: {e.message}")
        raise
    except Exception as e:
        await ctx.error(f"Unexpected error: {str(e)}")
        raise


async def get_column_tool(column_id: str, ctx: Context) -> Dict[str, Any]:
    """Get detailed information about a specific column."""
    try:
        await ctx.info(f"Fetching column details: {column_id}")
        
        column_id = validate_uuid(column_id, "column_id")
        
        async with YouGileClient(auth.auth_manager) as client:
            result = await columns.get_column(client, column_id)
            
        await ctx.info(f"✅ Successfully retrieved column: {result.get('title', column_id)}")
        return result
        
    except ValidationError as e:
        await ctx.error(f"Validation failed: {e.message}")
        raise
    except YouGileError as e:
        await ctx.error(f"API error while fetching column: {e.message}")
        raise
    except Exception as e:
        await ctx.error(f"Unexpected error: {str(e)}")
        raise


async def update_column_tool(
    column_id: str,
    title: str = None,
    color: int = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """Update column information."""
    try:
        await ctx.info(f"Updating column: {column_id}")
        
        column_id = validate_uuid(column_id, "column_id")
        
        # Build update data with only provided fields
        column_data = {}
        
        if title is not None:
            title = validate_non_empty_string(title, "title")
            column_data["title"] = title
            
        if color is not None:
            if not (1 <= color <= 16):
                raise ValidationError("Color must be between 1 and 16")
            column_data["color"] = color
            
        if not column_data:
            raise ValidationError("At least one field must be provided for update")
        
        async with YouGileClient(auth.auth_manager) as client:
            result = await columns.update_column(client, column_id, column_data)
            
        await ctx.info(f"✅ Successfully updated column: {result.get('title', column_id)}")
        return result
        
    except ValidationError as e:
        await ctx.error(f"Validation failed: {e.message}")
        raise
    except YouGileError as e:
        await ctx.error(f"API error while updating column: {e.message}")
        raise
    except Exception as e:
        await ctx.error(f"Unexpected error: {str(e)}")
        raise