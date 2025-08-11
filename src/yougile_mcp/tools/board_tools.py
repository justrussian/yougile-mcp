"""
YouGile Boards MCP tools.
Board management and workflows (4 endpoints).
"""

from typing import List, Dict, Any, Optional
from mcp.server.fastmcp import Context
from ...core import models
from ...core import auth
from ...core.client import YouGileClient
from ...core.exceptions import YouGileError, ValidationError
from ...api import boards
from ...utils.validation import validate_uuid, validate_non_empty_string


async def list_boards_tool(
    project_id: Optional[str] = None,
    title: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    include_deleted: bool = False,
    ctx: Context = None
) -> List[models.Board]:
    """Get list of boards with optional filtering.
    
    Args:
        project_id: Filter boards by project ID
        title: Filter boards by title (partial match)
        limit: Maximum number of boards to return (default: 50)
        offset: Number of boards to skip (default: 0)
        include_deleted: Include deleted boards (default: False)
    """
    try:
        await ctx.info(f"Fetching boards from YouGile (limit: {limit}, offset: {offset})...")
        
        if project_id:
            project_id = validate_uuid(project_id, "project_id")
            await ctx.info(f"Filtering by project: {project_id}")
        
        if title:
            await ctx.info(f"Filtering by title: {title}")
        
        async with YouGileClient(auth.auth_manager) as client:
            result = await boards.get_boards(
                client,
                project_id=project_id,
                title=title,
                limit=limit,
                offset=offset,
                include_deleted=include_deleted
            )
            
        board_list = [models.Board(**board) for board in result]
        
        await ctx.info(f" Successfully retrieved {len(board_list)} boards")
        return board_list
        
    except ValidationError as e:
        await ctx.error(f"Validation failed: {e.message}")
        raise
    except YouGileError as e:
        await ctx.error(f"API error while fetching boards: {e.message}")
        raise
    except Exception as e:
        await ctx.error(f"Unexpected error: {str(e)}")
        raise


async def create_board_tool(
    title: str,
    project_id: str,
    workflow_id: str = None,
    ctx: Context = None
) -> models.CreatedEntity:
    """Create a new board in a project."""
    try:
        await ctx.info(f"Creating board: {title}")
        
        # Validate inputs
        title = validate_non_empty_string(title, "title")
        project_id = validate_uuid(project_id, "project_id")
        
        board_data = {
            "title": title,
            "projectId": project_id
        }
        
        if workflow_id is not None:
            workflow_id = validate_uuid(workflow_id, "workflow_id")
            board_data["workflowId"] = workflow_id
        
        async with YouGileClient(auth.auth_manager) as client:
            result = await boards.create_board(client, board_data)
            
        created_entity = models.CreatedEntity(**result)
        
        await ctx.info(f"✅ Successfully created board with ID: {created_entity.id}")
        return created_entity
        
    except ValidationError as e:
        await ctx.error(f"Validation failed: {e.message}")
        raise
    except YouGileError as e:
        await ctx.error(f"API error while creating board: {e.message}")
        raise
    except Exception as e:
        await ctx.error(f"Unexpected error: {str(e)}")
        raise


async def get_board_tool(board_id: str, ctx: Context) -> models.Board:
    """Get detailed information about a specific board."""
    try:
        await ctx.info(f"Fetching board details: {board_id}")
        
        board_id = validate_uuid(board_id, "board_id")
        
        async with YouGileClient(auth.auth_manager) as client:
            result = await boards.get_board(client, board_id)
            
        board = models.Board(**result)
        
        await ctx.info(f" Successfully retrieved board: {board.title}")
        return board
        
    except ValidationError as e:
        await ctx.error(f"Validation failed: {e.message}")
        raise
    except YouGileError as e:
        await ctx.error(f"API error while fetching board: {e.message}")
        raise
    except Exception as e:
        await ctx.error(f"Unexpected error: {str(e)}")
        raise


async def update_board_tool(
    board_id: str,
    title: str = None,
    workflow_id: str = None,
    ctx: Context = None
) -> models.Board:
    """Update board information."""
    try:
        await ctx.info(f"Updating board: {board_id}")
        
        board_id = validate_uuid(board_id, "board_id")
        
        # Build update data with only provided fields
        board_data = {}
        
        if title is not None:
            title = validate_non_empty_string(title, "title")
            board_data["title"] = title
            
        if workflow_id is not None:
            workflow_id = validate_uuid(workflow_id, "workflow_id")
            board_data["workflowId"] = workflow_id
            
        if not board_data:
            raise ValidationError("At least one field must be provided for update")
        
        async with YouGileClient(auth.auth_manager) as client:
            # Update board (returns minimal response with just ID)
            await boards.update_board(client, board_id, board_data)
            
            # Fetch complete board data after update
            result = await boards.get_board(client, board_id)
            
        board = models.Board(**result)
        
        await ctx.info(f" Successfully updated board: {board.title}")
        return board
        
    except ValidationError as e:
        await ctx.error(f"Validation failed: {e.message}")
        raise
    except YouGileError as e:
        await ctx.error(f"API error while updating board: {e.message}")
        raise
    except Exception as e:
        await ctx.error(f"Unexpected error: {str(e)}")
        raise