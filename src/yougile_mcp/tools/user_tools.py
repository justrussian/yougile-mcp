"""
YouGile Users MCP tools.
User management and invitations (5 endpoints).
"""

from typing import List, Dict, Any
from mcp.server.fastmcp import Context
from ...core import models
from ...core import auth
from ...core.client import YouGileClient
from ...core.exceptions import YouGileError, ValidationError
from ...api import users
from ...utils.validation import validate_uuid, validate_email, validate_non_empty_string


async def list_users_tool(ctx: Context) -> List[models.User]:
    """Get list of all users in the company."""
    try:
        await ctx.info("Fetching users from YouGile...")
        
        async with YouGileClient(auth.auth_manager) as client:
            result = await users.get_users(client)
            
        user_list = [models.User(**user) for user in result]
        
        await ctx.info(f" Successfully retrieved {len(user_list)} users")
        return user_list
        
    except YouGileError as e:
        await ctx.error(f"API error while fetching users: {e.message}")
        raise
    except Exception as e:
        await ctx.error(f"Unexpected error: {str(e)}")
        raise


async def invite_user_tool(
    email: str, 
    first_name: str, 
    last_name: str,
    role: str = "user",
    departments: List[str] = None,
    ctx: Context = None
) -> models.User:
    """Invite a new user to the company."""
    try:
        await ctx.info(f"Inviting user: {email}")
        
        # Validate inputs
        email = validate_email(email)
        first_name = validate_non_empty_string(first_name, "first_name")
        last_name = validate_non_empty_string(last_name, "last_name")
        role = validate_non_empty_string(role, "role")
        
        if departments:
            departments = [validate_uuid(dept_id, "department_id") for dept_id in departments]
        
        user_data = {
            "email": email,
            "realName": f"{first_name} {last_name}",
            "firstName": first_name,
            "lastName": last_name,
            "role": role,
            "departments": departments or []
        }
        
        async with YouGileClient(auth.auth_manager) as client:
            result = await users.invite_user(client, user_data)
            
        user = models.User(**result)
        
        await ctx.info(f" Successfully invited user: {email}")
        return user
        
    except ValidationError as e:
        await ctx.error(f"Validation failed: {e.message}")
        raise
    except YouGileError as e:
        await ctx.error(f"API error while inviting user: {e.message}")
        raise
    except Exception as e:
        await ctx.error(f"Unexpected error: {str(e)}")
        raise


async def get_user_tool(user_id: str, ctx: Context) -> models.User:
    """Get detailed information about a specific user."""
    try:
        await ctx.info(f"Fetching user details: {user_id}")
        
        user_id = validate_uuid(user_id, "user_id")
        
        async with YouGileClient(auth.auth_manager) as client:
            result = await users.get_user(client, user_id)
            
        user = models.User(**result)
        
        await ctx.info(f" Successfully retrieved user: {user.real_name}")
        return user
        
    except ValidationError as e:
        await ctx.error(f"Validation failed: {e.message}")
        raise
    except YouGileError as e:
        await ctx.error(f"API error while fetching user: {e.message}")
        raise
    except Exception as e:
        await ctx.error(f"Unexpected error: {str(e)}")
        raise


async def update_user_tool(
    user_id: str,
    first_name: str = None,
    last_name: str = None,
    role: str = None,
    departments: List[str] = None,
    ctx: Context = None
) -> models.User:
    """Update user information."""
    try:
        await ctx.info(f"Updating user: {user_id}")
        
        user_id = validate_uuid(user_id, "user_id")
        
        # Build update data with only provided fields
        user_data = {}
        
        if first_name is not None:
            first_name = validate_non_empty_string(first_name, "first_name")
            user_data["firstName"] = first_name
            
        if last_name is not None:
            last_name = validate_non_empty_string(last_name, "last_name")
            user_data["lastName"] = last_name
            
        if first_name or last_name:
            # Update realName if either name component changed
            real_name_parts = []
            if first_name:
                real_name_parts.append(first_name)
            if last_name:
                real_name_parts.append(last_name)
            user_data["realName"] = " ".join(real_name_parts)
            
        if role is not None:
            role = validate_non_empty_string(role, "role")
            user_data["role"] = role
            
        if departments is not None:
            departments = [validate_uuid(dept_id, "department_id") for dept_id in departments]
            user_data["departments"] = departments
            
        if not user_data:
            raise ValidationError("At least one field must be provided for update")
        
        async with YouGileClient(auth.auth_manager) as client:
            # Update user (returns minimal response with just ID)
            await users.update_user(client, user_id, user_data)
            
            # Fetch complete user data after update
            result = await users.get_user(client, user_id)
            
        user = models.User(**result)
        
        await ctx.info(f" Successfully updated user: {user.real_name}")
        return user
        
    except ValidationError as e:
        await ctx.error(f"Validation failed: {e.message}")
        raise
    except YouGileError as e:
        await ctx.error(f"API error while updating user: {e.message}")
        raise
    except Exception as e:
        await ctx.error(f"Unexpected error: {str(e)}")
        raise


async def remove_user_tool(user_id: str, ctx: Context) -> Dict[str, Any]:
    """Remove user from the company."""
    try:
        await ctx.info(f"Removing user: {user_id}")
        
        user_id = validate_uuid(user_id, "user_id")
        
        async with YouGileClient(auth.auth_manager) as client:
            result = await users.delete_user(client, user_id)
            
        await ctx.info(f" Successfully removed user: {user_id}")
        return {"success": True, "message": "User removed successfully", "user_id": user_id}
        
    except ValidationError as e:
        await ctx.error(f"Validation failed: {e.message}")
        raise
    except YouGileError as e:
        await ctx.error(f"API error while removing user: {e.message}")
        raise
    except Exception as e:
        await ctx.error(f"Unexpected error: {str(e)}")
        raise