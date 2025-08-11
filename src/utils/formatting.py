"""
Response formatting utilities.
Pure functions for formatting API responses for MCP tools.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime


def format_task_response(task: Dict[str, Any]) -> str:
    """Format task data for human-readable display."""
    title = task.get("title", "Untitled Task")
    task_id = task.get("id", "")
    description = task.get("description", "")
    
    # Format assigned users
    assignees = task.get("assignedUsers", [])
    assignee_names = [user.get("name", "Unknown") for user in assignees] if assignees else []
    
    # Format deadline
    deadline = task.get("deadline")
    deadline_str = ""
    if deadline:
        deadline_str = f"\n📅 Deadline: {deadline.get('date', 'Not set')}"
    
    # Format status
    column = task.get("column", {})
    status = column.get("title", "No Status")
    
    result = f"📋 **{title}**"
    if task_id:
        result += f" (ID: {task_id[:8]}...)"
    
    result += f"\n🏷️ Status: {status}"
    
    if assignee_names:
        result += f"\n👥 Assigned: {', '.join(assignee_names)}"
    
    if description:
        desc_preview = description[:100] + "..." if len(description) > 100 else description
        result += f"\n📝 Description: {desc_preview}"
    
    result += deadline_str
    
    return result


def format_project_response(project: Dict[str, Any]) -> str:
    """Format project data for human-readable display."""
    title = project.get("title", "Untitled Project")
    project_id = project.get("id", "")
    description = project.get("description", "")
    
    # Format users
    users = project.get("users", {})
    user_count = len(users) if users else 0
    
    result = f"📁 **{title}**"
    if project_id:
        result += f" (ID: {project_id[:8]}...)"
    
    result += f"\n👥 Members: {user_count}"
    
    if description:
        desc_preview = description[:150] + "..." if len(description) > 150 else description
        result += f"\n📝 Description: {desc_preview}"
    
    return result


def format_board_response(board: Dict[str, Any]) -> str:
    """Format board data for human-readable display."""
    title = board.get("title", "Untitled Board")
    board_id = board.get("id", "")
    project_id = board.get("projectId", "")
    
    result = f"📊 **{title}**"
    if board_id:
        result += f" (ID: {board_id[:8]}...)"
    
    if project_id:
        result += f"\n📁 Project: {project_id[:8]}..."
    
    return result


def format_user_response(user: Dict[str, Any]) -> str:
    """Format user data for human-readable display."""
    name = user.get("realName") or user.get("name", "Unknown User")
    email = user.get("email", "")
    user_id = user.get("id", "")
    role = user.get("role", "")
    
    result = f"👤 **{name}**"
    if user_id:
        result += f" (ID: {user_id[:8]}...)"
    
    if email:
        result += f"\n📧 Email: {email}"
    
    if role:
        result += f"\n🎭 Role: {role}"
    
    return result


def format_error_message(error: Exception) -> str:
    """Format error for user-friendly display."""
    error_type = type(error).__name__
    message = str(error)
    
    if hasattr(error, 'status_code') and error.status_code:
        return f"❌ {error_type} (HTTP {error.status_code}): {message}"
    
    return f"❌ {error_type}: {message}"


def format_list_response(items: List[Dict[str, Any]], item_type: str, formatter_func) -> str:
    """Format a list of items with a specific formatter."""
    if not items:
        return f"No {item_type} found."
    
    count = len(items)
    result = f"Found {count} {item_type}(s):\n\n"
    
    for i, item in enumerate(items[:10], 1):  # Limit to first 10 items
        result += f"{i}. {formatter_func(item)}\n\n"
    
    if count > 10:
        result += f"... and {count - 10} more {item_type}(s)"
    
    return result.strip()


def format_success_message(action: str, item_type: str, item_name: str = None) -> str:
    """Format success message."""
    if item_name:
        return f"✅ Successfully {action} {item_type}: {item_name}"
    return f"✅ Successfully {action} {item_type}"