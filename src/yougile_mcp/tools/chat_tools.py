"""
YouGile Chat MCP tools.
Communication features: group chats and task messages (8 endpoints).
"""

from typing import List, Dict, Any, Optional
from mcp.server.fastmcp import Context
from ...core import models
from ...core import auth
from ...core.client import YouGileClient
from ...core.exceptions import YouGileError, ValidationError
from ...api import chats
from ...utils.validation import validate_uuid, validate_non_empty_string


# Group Chat Management
async def list_group_chats_tool(ctx: Context) -> List[Dict[str, Any]]:
    """Get list of all group chats."""
    try:
        await ctx.info("Fetching group chats from YouGile...")
        
        async with YouGileClient(auth.auth_manager) as client:
            result = await chats.get_group_chats(client)
            
        await ctx.info(f" Successfully retrieved {len(result)} group chats")
        return result
        
    except YouGileError as e:
        await ctx.error(f"API error while fetching group chats: {e.message}")
        raise
    except Exception as e:
        await ctx.error(f"Unexpected error: {str(e)}")
        raise


async def create_group_chat_tool(
    title: str,
    participants: List[str] = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """Create a new group chat."""
    try:
        await ctx.info(f"Creating group chat: {title}")
        
        # Validate inputs
        title = validate_non_empty_string(title, "title")
        
        chat_data = {
            "title": title
        }
        
        if participants is not None:
            participants = [validate_uuid(user_id, "user_id") for user_id in participants]
            chat_data["participants"] = participants
        
        async with YouGileClient(auth.auth_manager) as client:
            result = await chats.create_group_chat(client, chat_data)
            
        await ctx.info(f" Successfully created group chat with ID: {result.get('id')}")
        return result
        
    except ValidationError as e:
        await ctx.error(f"Validation failed: {e.message}")
        raise
    except YouGileError as e:
        await ctx.error(f"API error while creating group chat: {e.message}")
        raise
    except Exception as e:
        await ctx.error(f"Unexpected error: {str(e)}")
        raise


async def get_group_chat_tool(chat_id: str, ctx: Context) -> Dict[str, Any]:
    """Get detailed information about a specific group chat."""
    try:
        await ctx.info(f"Fetching group chat details: {chat_id}")
        
        chat_id = validate_uuid(chat_id, "chat_id")
        
        async with YouGileClient(auth.auth_manager) as client:
            result = await chats.get_group_chat(client, chat_id)
            
        await ctx.info(f" Successfully retrieved group chat: {result.get('title', chat_id)}")
        return result
        
    except ValidationError as e:
        await ctx.error(f"Validation failed: {e.message}")
        raise
    except YouGileError as e:
        await ctx.error(f"API error while fetching group chat: {e.message}")
        raise
    except Exception as e:
        await ctx.error(f"Unexpected error: {str(e)}")
        raise


# Chat Messages (Comments)
async def get_chat_messages_tool(
    chat_id: str,
    limit: int = 50,
    ctx: Context = None
) -> List[Dict[str, Any]]:
    """Get messages from a chat (task comments or group chat messages).
    
    Args:
        chat_id: ID of the chat (can be task ID for task comments)
        limit: Maximum number of messages to return
    """
    try:
        await ctx.info(f"Fetching messages from chat: {chat_id}")
        
        chat_id = validate_uuid(chat_id, "chat_id")
        
        async with YouGileClient(auth.auth_manager) as client:
            result = await chats.get_chat_messages(client, chat_id)
            
        # Apply limit if needed
        if limit and len(result) > limit:
            result = result[-limit:]  # Get latest messages
            
        await ctx.info(f" Successfully retrieved {len(result)} messages")
        return result
        
    except ValidationError as e:
        await ctx.error(f"Validation failed: {e.message}")
        raise
    except YouGileError as e:
        await ctx.error(f"API error while fetching messages: {e.message}")
        raise
    except Exception as e:
        await ctx.error(f"Unexpected error: {str(e)}")
        raise


async def send_chat_message_tool(
    chat_id: str,
    message: str,
    ctx: Context = None
) -> Dict[str, Any]:
    """Send a message to a chat (add comment to task or send group chat message).
    
    Args:
        chat_id: ID of the chat (can be task ID for task comments)
        message: Message text to send
    """
    try:
        await ctx.info(f"Sending message to chat: {chat_id}")
        
        # Validate inputs
        chat_id = validate_uuid(chat_id, "chat_id")
        message = validate_non_empty_string(message, "message")
        
        message_data = {
            "text": message,
            "textHtml": f"<p>{message}</p>",  # HTML version
            "label": "Comment"  # Default label for task comments
        }
        
        async with YouGileClient(auth.auth_manager) as client:
            result = await chats.send_chat_message(client, chat_id, message_data)
            
        await ctx.info(f" Successfully sent message with ID: {result.get('id')}")
        return result
        
    except ValidationError as e:
        await ctx.error(f"Validation failed: {e.message}")
        raise
    except YouGileError as e:
        await ctx.error(f"API error while sending message: {e.message}")
        raise
    except Exception as e:
        await ctx.error(f"Unexpected error: {str(e)}")
        raise


async def get_chat_message_tool(
    chat_id: str,
    message_id: str,
    ctx: Context = None
) -> Dict[str, Any]:
    """Get a specific message from a chat."""
    try:
        await ctx.info(f"Fetching message {message_id} from chat: {chat_id}")
        
        chat_id = validate_uuid(chat_id, "chat_id")
        message_id = validate_uuid(message_id, "message_id")
        
        async with YouGileClient(auth.auth_manager) as client:
            result = await chats.get_chat_message(client, chat_id, message_id)
            
        await ctx.info(f" Successfully retrieved message")
        return result
        
    except ValidationError as e:
        await ctx.error(f"Validation failed: {e.message}")
        raise
    except YouGileError as e:
        await ctx.error(f"API error while fetching message: {e.message}")
        raise
    except Exception as e:
        await ctx.error(f"Unexpected error: {str(e)}")
        raise


async def update_chat_message_tool(
    chat_id: str,
    message_id: str,
    message: str,
    ctx: Context = None
) -> Dict[str, Any]:
    """Update/edit a message in a chat."""
    try:
        await ctx.info(f"Updating message {message_id} in chat: {chat_id}")
        
        # Validate inputs
        chat_id = validate_uuid(chat_id, "chat_id")
        message_id = validate_uuid(message_id, "message_id")
        message = validate_non_empty_string(message, "message")
        
        message_data = {
            "text": message,
            "textHtml": f"<p>{message}</p>",  # HTML version
            "label": "Comment"  # Default label for task comments
        }
        
        async with YouGileClient(auth.auth_manager) as client:
            result = await chats.update_chat_message(client, chat_id, message_id, message_data)
            
        await ctx.info(f" Successfully updated message")
        return result
        
    except ValidationError as e:
        await ctx.error(f"Validation failed: {e.message}")
        raise
    except YouGileError as e:
        await ctx.error(f"API error while updating message: {e.message}")
        raise
    except Exception as e:
        await ctx.error(f"Unexpected error: {str(e)}")
        raise


# Task-specific comment helpers
async def get_task_comments_tool(
    task_id: str,
    limit: int = 50,
    ctx: Context = None
) -> List[Dict[str, Any]]:
    """Get comments for a specific task (alias for get_chat_messages with task ID)."""
    await ctx.info(f"Fetching comments for task: {task_id}")
    return await get_chat_messages_tool(task_id, limit, ctx)


async def add_task_comment_tool(
    task_id: str,
    comment: str,
    ctx: Context = None
) -> Dict[str, Any]:
    """Add a comment to a specific task (alias for send_chat_message with task ID)."""
    await ctx.info(f"Adding comment to task: {task_id}")
    return await send_chat_message_tool(task_id, comment, ctx)