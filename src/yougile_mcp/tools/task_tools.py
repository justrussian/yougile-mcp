"""
YouGile Tasks MCP tools.
Task operations and lifecycle management (7 endpoints).
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, date
from mcp.server.fastmcp import Context
from ...core import models
from ...core import auth
from ...core.client import YouGileClient
from ...core.exceptions import YouGileError, ValidationError
from ...api import tasks
from ...utils.validation import validate_uuid, validate_non_empty_string


async def list_task_summaries_tool(
    limit: int = 50,
    offset: int = 0,
    ctx: Context = None
) -> List[Dict[str, Any]]:
    """Get list of task summaries with pagination.
    
    Args:
        limit: Maximum number of tasks to return (default: 50)
        offset: Number of tasks to skip (default: 0)
    """
    try:
        if ctx:
            await ctx.info(f"Fetching task list from YouGile (limit: {limit}, offset: {offset})...")
        
        async with YouGileClient(auth.auth_manager) as client:
            result = await tasks.get_task_list(client, limit=limit, offset=offset)
            
        if ctx:
            await ctx.info(f"✅ Successfully retrieved {len(result)} task summaries")
        return result
        
    except YouGileError as e:
        if ctx:
            await ctx.error(f"API error while fetching task list: {e.message}")
        raise
    except Exception as e:
        if ctx:
            await ctx.error(f"Unexpected error: {str(e)}")
        raise


async def list_tasks_tool(
    column_id: Optional[str] = None,
    assigned_to: Optional[str] = None,
    title: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    include_deleted: bool = False,
    ctx: Context = None
) -> List[Dict[str, Any]]:
    """Get detailed list of tasks with optional filtering.
    
    Args:
        column_id: Filter tasks by column ID
        assigned_to: Filter tasks by assigned user ID
        title: Filter tasks by title (partial match)
        limit: Maximum number of tasks to return (default: 50)
        offset: Number of tasks to skip (default: 0)
        include_deleted: Include deleted tasks (default: False)
    """
    try:
        if ctx:
            await ctx.info(f"Fetching detailed tasks from YouGile (limit: {limit}, offset: {offset})...")
        
        if column_id:
            column_id = validate_uuid(column_id, "column_id")
            if ctx:
                await ctx.info(f"Filtering by column: {column_id}")
        
        if assigned_to:
            assigned_to = validate_uuid(assigned_to, "assigned_to")
            if ctx:
                await ctx.info(f"Filtering by assignee: {assigned_to}")
        
        if title:
            if ctx:
                await ctx.info(f"Filtering by title: {title}")
        
        async with YouGileClient(auth.auth_manager) as client:
            result = await tasks.get_tasks(
                client,
                column_id=column_id,
                assigned_to=assigned_to,
                title=title,
                limit=limit,
                offset=offset,
                include_deleted=include_deleted
            )
            
        if ctx:
            await ctx.info(f"✅ Successfully retrieved {len(result)} detailed tasks")
        return result
        
    except ValidationError as e:
        if ctx:
            await ctx.error(f"Validation failed: {e.message}")
        raise
    except YouGileError as e:
        if ctx:
            await ctx.error(f"API error while fetching tasks: {e.message}")
        raise
    except Exception as e:
        if ctx:
            await ctx.error(f"Unexpected error: {str(e)}")
        raise


async def create_task_tool(
    title: str,
    column_id: str,
    description: str = None,
    assigned_users: List[str] = None,
    deadline: Dict[str, Any] = None,
    time_tracking: Dict[str, Any] = None,
    stickers: Dict[str, str] = None,
    subtasks: List[str] = None,
    checklists: List[Dict[str, Any]] = None,
    completed: bool = None,
    archived: bool = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """Create a new task. Returns the task ID. Description requires HTML format.
    
    Args:
        title: Task title (required)
        column_id: ID of the column to place task in (required)
        description: Task description in HTML format (use <br> for line breaks, <b>bold</b>, <i>italic</i>, etc)
        assigned_users: List of user IDs to assign task to
        deadline: Deadline sticker data (dict with deadline, startDate, withTime fields)
        time_tracking: Time tracking sticker data (dict with plan, work fields)
        stickers: Custom stickers (dict of sticker_id -> state_id)
        subtasks: List of subtask titles
        checklists: List of checklist groups (dict with title and items: [{"title": "Item", "isCompleted": false}])
        completed: Create task as already completed (True) or active (False)
        archived: Create task as archived (True) or active (False)
    """
    try:
        if ctx:
            await ctx.info(f"Creating task: {title}")
        
        # Validate inputs
        title = validate_non_empty_string(title, "title")
        column_id = validate_uuid(column_id, "column_id")
        
        task_data = {
            "title": title,
            "columnId": column_id
        }
        
        if description is not None:
            # Description accepts HTML format - no validation needed for content
            task_data["description"] = description
            
        if assigned_users is not None:
            assigned_users = [validate_uuid(user_id, "user_id") for user_id in assigned_users]
            task_data["assigned"] = assigned_users
            
        if deadline is not None:
            task_data["deadline"] = deadline
            
        if time_tracking is not None:
            task_data["timeTracking"] = time_tracking
            
        if stickers is not None:
            task_data["stickers"] = stickers
            
        if subtasks is not None:
            subtasks = [validate_non_empty_string(subtask, "subtask") for subtask in subtasks]
            task_data["subtasks"] = subtasks
            
        if checklists is not None:
            # Validate checklist structure
            for checklist in checklists:
                if not isinstance(checklist, dict) or "title" not in checklist or "items" not in checklist:
                    raise ValidationError("Each checklist must have 'title' and 'items' fields")
                validate_non_empty_string(checklist["title"], "checklist title")
                if not isinstance(checklist["items"], list):
                    raise ValidationError("Checklist 'items' must be a list")
                for item in checklist["items"]:
                    if not isinstance(item, dict) or "title" not in item:
                        raise ValidationError("Each checklist item must have a 'title' field")
                    validate_non_empty_string(item["title"], "checklist item title")
            task_data["checklists"] = checklists
            
        if completed is not None:
            task_data["completed"] = completed
            
        if archived is not None:
            task_data["archived"] = archived
        
        async with YouGileClient(auth.auth_manager) as client:
            result = await tasks.create_task(client, task_data)
            
        if ctx:
            await ctx.info(f"✅ Successfully created task with ID: {result.get('id')}")
        return result
        
    except ValidationError as e:
        if ctx:
            await ctx.error(f"Validation failed: {e.message}")
        raise
    except YouGileError as e:
        if ctx:
            await ctx.error(f"API error while creating task: {e.message}")
        raise
    except Exception as e:
        if ctx:
            await ctx.error(f"Unexpected error: {str(e)}")
        raise


async def get_task_tool(task_id: str, ctx: Context) -> Dict[str, Any]:
    """Get detailed information about a specific task."""
    try:
        if ctx:
            await ctx.info(f"Fetching task details: {task_id}")
        
        task_id = validate_uuid(task_id, "task_id")
        
        async with YouGileClient(auth.auth_manager) as client:
            result = await tasks.get_task(client, task_id)
            
        if ctx:
            await ctx.info(f"✅ Successfully retrieved task: {result.get('title', task_id)}")
        return result
        
    except ValidationError as e:
        if ctx:
            await ctx.error(f"Validation failed: {e.message}")
        raise
    except YouGileError as e:
        if ctx:
            await ctx.error(f"API error while fetching task: {e.message}")
        raise
    except Exception as e:
        if ctx:
            await ctx.error(f"Unexpected error: {str(e)}")
        raise


async def get_tasks_by_date_tool(
    assigned_to: Optional[str] = None,
    created_by: Optional[str] = None,
    target_date: Optional[str] = None,
    completed_only: bool = False,
    limit: int = 5000,
    ctx: Context = None
) -> List[Dict[str, Any]]:
    """Get tasks filtered by date and completion status.
    
    Args:
        assigned_to: Filter tasks by assigned user ID (API filter)
        created_by: Filter tasks by creator user ID (client-side filter)
        target_date: Date in YYYY-MM-DD format (default: today)
        completed_only: Only return completed tasks
        limit: Maximum number of tasks to fetch and filter (max 5000)
    """
    try:
        if ctx:
            await ctx.info(f"Fetching tasks with date filtering...")
        
        # Parse target date
        if target_date:
            try:
                filter_date = datetime.strptime(target_date, "%Y-%m-%d").date()
            except ValueError:
                raise ValidationError("target_date must be in YYYY-MM-DD format", field="target_date")
        else:
            filter_date = date.today()
        
        if ctx:
            await ctx.info(f"Filtering tasks for date: {filter_date}")
        
        # Validate user IDs if provided
        if assigned_to:
            assigned_to = validate_uuid(assigned_to, "assigned_to")
        if created_by:
            created_by = validate_uuid(created_by, "created_by")
        
        # Get tasks from API with pagination to handle large datasets
        all_tasks = []
        offset = 0
        batch_size = 1000  # API max per request
        
        # If filtering by created_by, we need to get more tasks since API doesn't support this filter
        fetch_limit = limit if assigned_to else 5000  # Get more tasks if filtering by created_by
        
        async with YouGileClient(auth.auth_manager) as client:
            while len(all_tasks) < fetch_limit:
                current_limit = min(batch_size, fetch_limit - len(all_tasks))
                
                batch = await tasks.get_tasks(
                    client,
                    assigned_to=assigned_to,
                    limit=current_limit,
                    offset=offset,
                    include_deleted=False
                )
                
                if not batch:  # No more tasks
                    break
                    
                all_tasks.extend(batch)
                
                if len(batch) < current_limit:  # Got fewer than requested - no more data
                    break
                    
                offset += len(batch)
        
        if ctx:
            await ctx.info(f"Retrieved {len(all_tasks)} tasks total, filtering by criteria...")
            if created_by:
                await ctx.debug(f"Looking for tasks created by: {created_by}")
            if target_date:
                await ctx.debug(f"Looking for tasks on date: {filter_date}")
        
        # Check if tasks are sorted by date (newest first or oldest first)
        if len(all_tasks) > 1:
            first_timestamp = all_tasks[0].get('timestamp', 0)
            last_timestamp = all_tasks[-1].get('timestamp', 0)
            
            if isinstance(first_timestamp, str):
                first_timestamp = datetime.fromisoformat(first_timestamp.replace('Z', '+00:00')).timestamp()
            if isinstance(last_timestamp, str):
                last_timestamp = datetime.fromisoformat(last_timestamp.replace('Z', '+00:00')).timestamp()
                
            if first_timestamp > last_timestamp:
                sort_order = "newest first"
            elif first_timestamp < last_timestamp:
                sort_order = "oldest first"
            else:
                sort_order = "mixed/same"
                
            if ctx:
                await ctx.debug(f"Tasks appear to be sorted: {sort_order}")
        
        filtered_tasks = []
        
        for task in all_tasks:
            # Filter by completion status if requested
            if completed_only and not task.get('completed', False):
                continue
                
            # Filter by creator if requested
            if created_by and task.get('createdBy') != created_by:
                if ctx:
                    await ctx.debug(f"Task {task.get('id', 'unknown')} created by {task.get('createdBy', 'unknown')}, not {created_by}")
                continue
            
            # Filter by date using timestamp
            timestamp = task.get('timestamp')
            if timestamp:
                try:
                    # Convert timestamp to date
                    if isinstance(timestamp, str):
                        task_datetime = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    else:
                        # Handle both seconds and milliseconds timestamps
                        if timestamp > 1e12:  # Likely milliseconds
                            task_datetime = datetime.fromtimestamp(timestamp / 1000)
                        else:  # Likely seconds
                            task_datetime = datetime.fromtimestamp(timestamp)
                    
                    task_date = task_datetime.date()
                    
                    # Check if task matches target date
                    if task_date == filter_date:
                        if ctx:
                            await ctx.debug(f"✅ Task {task.get('id', 'unknown')} matches date {filter_date}")
                        filtered_tasks.append(task)
                    else:
                        if ctx:
                            await ctx.debug(f"❌ Task {task.get('id', 'unknown')} date {task_date} != {filter_date}")
                        
                except (ValueError, TypeError) as e:
                    if ctx:
                        await ctx.debug(f"Could not parse timestamp for task {task.get('id', 'unknown')}: {e}")
                    continue
        
        # Limit results to requested limit
        final_results = filtered_tasks[:limit]
        
        if ctx:
            await ctx.info(f"✅ Found {len(filtered_tasks)} tasks matching criteria for {filter_date}, returning {len(final_results)}")
        
        return final_results
        
    except ValidationError as e:
        if ctx:
            await ctx.error(f"Validation failed: {e.message}")
        raise
    except YouGileError as e:
        if ctx:
            await ctx.error(f"API error while fetching tasks: {e.message}")
        raise
    except Exception as e:
        if ctx:
            await ctx.error(f"Unexpected error: {str(e)}")
        raise