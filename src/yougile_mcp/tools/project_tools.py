"""
YouGile Projects MCP tools.
Project management and operations (4 endpoints).
"""

from typing import List, Dict, Any, Optional
from mcp.server.fastmcp import Context
from ...core import models
from ...core import auth
from ...core.client import YouGileClient
from ...core.exceptions import YouGileError, ValidationError
from ...api import projects
from ...utils.validation import validate_uuid, validate_non_empty_string
from ._auth_helper import ensure_authenticated


async def list_projects_tool(ctx: Context) -> List[models.Project]:
    """Get list of all projects in the company."""
    try:
        await ctx.info("Fetching projects from YouGile...")
        
        # Ensure authentication is initialized
        await ensure_authenticated(ctx)
        
        async with YouGileClient(auth.auth_manager) as client:
            result = await projects.get_projects(client)
            
        project_list = [models.Project(**project) for project in result]
        
        await ctx.info(f" Successfully retrieved {len(project_list)} projects")
        return project_list
        
    except YouGileError as e:
        await ctx.error(f"API error while fetching projects: {e.message}")
        raise
    except Exception as e:
        await ctx.error(f"Unexpected error: {str(e)}")
        raise


async def create_project_tool(
    title: str,
    users: Dict[str, str] = None,
    workflow_id: str = None,
    ctx: Context = None
) -> models.CreatedEntity:
    """Create a new project."""
    try:
        await ctx.info(f"Creating project: {title}")
        
        # Validate inputs
        title = validate_non_empty_string(title, "title")
        
        project_data = {
            "title": title
        }
        
        if users is not None:
            # Validate user IDs and roles in the users dict
            validated_users = {}
            for user_id, role in users.items():
                user_id = validate_uuid(user_id, "user_id")
                role = validate_non_empty_string(role, "user_role")
                validated_users[user_id] = role
            project_data["users"] = validated_users
            
        if workflow_id is not None:
            workflow_id = validate_uuid(workflow_id, "workflow_id")
            project_data["workflowId"] = workflow_id
        
        async with YouGileClient(auth.auth_manager) as client:
            result = await projects.create_project(client, project_data)
            
        created_entity = models.CreatedEntity(**result)
        
        await ctx.info(f"✅ Successfully created project with ID: {created_entity.id}")
        return created_entity
        
    except ValidationError as e:
        await ctx.error(f"Validation failed: {e.message}")
        raise
    except YouGileError as e:
        await ctx.error(f"API error while creating project: {e.message}")
        raise
    except Exception as e:
        await ctx.error(f"Unexpected error: {str(e)}")
        raise


async def get_project_tool(project_id: str, ctx: Context) -> models.Project:
    """Get detailed information about a specific project."""
    try:
        await ctx.info(f"Fetching project details: {project_id}")
        
        project_id = validate_uuid(project_id, "project_id")
        
        async with YouGileClient(auth.auth_manager) as client:
            result = await projects.get_project(client, project_id)
            
        project = models.Project(**result)
        
        await ctx.info(f" Successfully retrieved project: {project.title}")
        return project
        
    except ValidationError as e:
        await ctx.error(f"Validation failed: {e.message}")
        raise
    except YouGileError as e:
        await ctx.error(f"API error while fetching project: {e.message}")
        raise
    except Exception as e:
        await ctx.error(f"Unexpected error: {str(e)}")
        raise


async def update_project_tool(
    project_id: str,
    title: str = None,
    users: Dict[str, str] = None,
    workflow_id: str = None,
    ctx: Context = None
) -> models.Project:
    """Update project information."""
    try:
        await ctx.info(f"Updating project: {project_id}")
        
        project_id = validate_uuid(project_id, "project_id")
        
        # Build update data with only provided fields
        project_data = {}
        
        if title is not None:
            title = validate_non_empty_string(title, "title")
            project_data["title"] = title
            
        if users is not None:
            # Validate user IDs and roles in the users dict
            validated_users = {}
            for user_id, role in users.items():
                user_id = validate_uuid(user_id, "user_id")
                role = validate_non_empty_string(role, "user_role")
                validated_users[user_id] = role
            project_data["users"] = validated_users
            
        if workflow_id is not None:
            workflow_id = validate_uuid(workflow_id, "workflow_id")
            project_data["workflowId"] = workflow_id
            
        if not project_data:
            raise ValidationError("At least one field must be provided for update")
        
        async with YouGileClient(auth.auth_manager) as client:
            # Update project (returns minimal response with just ID)
            await projects.update_project(client, project_id, project_data)
            
            # Fetch complete project data after update
            result = await projects.get_project(client, project_id)
            
        project = models.Project(**result)
        
        await ctx.info(f" Successfully updated project: {project.title}")
        return project
        
    except ValidationError as e:
        await ctx.error(f"Validation failed: {e.message}")
        raise
    except YouGileError as e:
        await ctx.error(f"API error while updating project: {e.message}")
        raise
    except Exception as e:
        await ctx.error(f"Unexpected error: {str(e)}")
        raise