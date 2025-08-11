"""
YouGile MCP Server

Main entry point for the YouGile Model Context Protocol server.
Registers all tools, resources, and prompts for YouGile API access.
"""

import asyncio
from mcp.server.fastmcp import FastMCP, Context
from .config import settings
from .core import auth
from .core.client import YouGileClient
from .api import auth as auth_api
from .yougile_mcp.tools.auth_tools import (
    get_companies_tool, 
    create_api_key_tool,
    list_api_keys_tool,
    delete_api_key_tool,
)
from .yougile_mcp.tools.user_tools import (
    list_users_tool,
    invite_user_tool,
    get_user_tool,
    update_user_tool,
    remove_user_tool,
)
from .yougile_mcp.tools.project_tools import (
    list_projects_tool,
    create_project_tool,
    get_project_tool,
    update_project_tool,
)
from .yougile_mcp.tools.board_tools import (
    list_boards_tool,
    create_board_tool,
    get_board_tool,
    update_board_tool,
)
from .yougile_mcp.tools.column_tools import (
    list_columns_tool,
    create_column_tool,
    get_column_tool,
    update_column_tool,
)
from .yougile_mcp.tools.chat_tools import (
    list_group_chats_tool,
    create_group_chat_tool,
    get_group_chat_tool,
    get_chat_messages_tool,
    send_chat_message_tool,
    get_chat_message_tool,
    update_chat_message_tool,
    get_task_comments_tool,
    add_task_comment_tool,
)
from .yougile_mcp.tools.task_tools import (
    list_task_summaries_tool,
    list_tasks_tool,
    create_task_tool,
    get_task_tool,
    get_tasks_by_date_tool,
)
from .yougile_mcp.tools.task_tools_extended import (
    update_task_tool,
    get_task_chat_subscribers_tool,
    update_task_chat_subscribers_tool,
)
from .yougile_mcp.tools.sticker_tools import (
    list_string_stickers_tool,
    get_string_sticker_tool,
    get_string_sticker_state_tool,
    decode_task_stickers_tool,
)
from .yougile_mcp.resources.api_docs import (
    get_api_overview,
    get_project_info,
    get_task_info,
    get_api_endpoints,
)
from .yougile_mcp.prompts.workflow_prompts import (
    setup_new_project_prompt,
    create_task_workflow_prompt,
    sprint_planning_prompt,
    daily_standup_prompt,
    project_health_check_prompt,
    user_productivity_report_prompt,
    weekly_team_report_prompt,
    task_escalation_prompt,
    onboarding_new_team_member_prompt,
    deadline_crunch_management_prompt,
    html_formatting_guide_prompt,
    api_usage_guide_prompt,
    retrospective_analysis_prompt,
)

# Create MCP server instance
mcp = FastMCP(name=settings.server_name)

# Register MCP Tools
@mcp.tool()
async def get_companies(login: str, password: str, ctx: Context) -> list:
    """Get list of companies available to user for API access."""
    return await get_companies_tool(login, password, ctx)

@mcp.tool()
async def create_api_key(login: str, password: str, company_id: str, ctx: Context) -> dict:
    """Create API key for accessing YouGile API.""" 
    return await create_api_key_tool(login, password, company_id, ctx)

@mcp.tool()
async def list_api_keys(login: str, password: str, company_id: str = None, ctx: Context = None) -> list:
    """Get list of existing API keys. Useful for managing keys (max 30 per account)."""
    return await list_api_keys_tool(login, password, company_id, ctx)

@mcp.tool()
async def delete_api_key(api_key: str, ctx: Context) -> dict:
    """Delete an API key. Useful for cleaning up old keys."""
    return await delete_api_key_tool(api_key, ctx)

@mcp.tool()
async def get_user_context(ctx: Context = None) -> str:
    """Get user-configured context and default settings for YouGile operations."""
    try:
        if ctx:
            await ctx.info("Retrieving user context settings...")
        
        if settings.user_context:
            if ctx:
                await ctx.info("✅ User context found")
            return settings.user_context
        else:
            if ctx:
                await ctx.info("ℹ️ No user context configured")
            return "Пользовательские настройки не заданы. Используйте стандартный подход с получением списка проектов и досок."
            
    except Exception as e:
        if ctx:
            await ctx.error(f"Error retrieving user context: {str(e)}")
        return "Ошибка получения пользовательских настроек."


# User Management Tools
@mcp.tool()
async def list_users(ctx: Context) -> list:
    """Get list of all users in the company."""
    return await list_users_tool(ctx)

@mcp.tool()
async def invite_user(email: str, first_name: str, last_name: str, role: str = "user", departments: list = None, ctx: Context = None) -> dict:
    """Invite a new user to the company."""
    return await invite_user_tool(email, first_name, last_name, role, departments or [], ctx)

@mcp.tool()
async def get_user(user_id: str, ctx: Context) -> dict:
    """Get detailed information about a specific user."""
    return await get_user_tool(user_id, ctx)

@mcp.tool()
async def update_user(user_id: str, first_name: str = None, last_name: str = None, role: str = None, departments: list = None, ctx: Context = None) -> dict:
    """Update user information."""
    return await update_user_tool(user_id, first_name, last_name, role, departments, ctx)

@mcp.tool()
async def remove_user(user_id: str, ctx: Context) -> dict:
    """Remove user from the company."""
    return await remove_user_tool(user_id, ctx)

# Project Management Tools
@mcp.tool()
async def list_projects(ctx: Context) -> list:
    """Get list of all projects in the company."""
    return await list_projects_tool(ctx)

@mcp.tool()
async def create_project(title: str, users: dict = None, workflow_id: str = None, ctx: Context = None) -> dict:
    """Create a new project."""
    return await create_project_tool(title, users, workflow_id, ctx)

@mcp.tool()
async def get_project(project_id: str, ctx: Context) -> dict:
    """Get detailed information about a specific project."""
    return await get_project_tool(project_id, ctx)

@mcp.tool()
async def update_project(project_id: str, title: str = None, users: dict = None, workflow_id: str = None, ctx: Context = None) -> dict:
    """Update project information."""
    return await update_project_tool(project_id, title, users, workflow_id, ctx)

# Board Management Tools
@mcp.tool()
async def list_boards(project_id: str = None, title: str = None, limit: int = 50, offset: int = 0, include_deleted: bool = False, ctx: Context = None) -> list:
    """Get list of boards with optional filtering."""
    return await list_boards_tool(project_id, title, limit, offset, include_deleted, ctx)

@mcp.tool()
async def create_board(title: str, project_id: str, workflow_id: str = None, ctx: Context = None) -> dict:
    """Create a new board in a project."""
    return await create_board_tool(title, project_id, workflow_id, ctx)

@mcp.tool()
async def get_board(board_id: str, ctx: Context) -> dict:
    """Get detailed information about a specific board."""
    return await get_board_tool(board_id, ctx)

@mcp.tool()
async def update_board(board_id: str, title: str = None, workflow_id: str = None, ctx: Context = None) -> dict:
    """Update board information."""
    return await update_board_tool(board_id, title, workflow_id, ctx)

# Column Management Tools
@mcp.tool()
async def list_columns(board_id: str = None, ctx: Context = None) -> list:
    """Get list of columns with optional filtering by board."""
    return await list_columns_tool(board_id, ctx)

@mcp.tool()
async def create_column(title: str, board_id: str, color: int = None, ctx: Context = None) -> dict:
    """Create a new column in a board. Color must be between 1-16."""
    return await create_column_tool(title, board_id, color, ctx)

@mcp.tool()
async def get_column(column_id: str, ctx: Context) -> dict:
    """Get detailed information about a specific column."""
    return await get_column_tool(column_id, ctx)

@mcp.tool()
async def update_column(column_id: str, title: str = None, color: int = None, ctx: Context = None) -> dict:
    """Update column information. Color must be between 1-16."""
    return await update_column_tool(column_id, title, color, ctx)

# Task Management Tools
@mcp.tool()
async def list_task_summaries(limit: int = 50, offset: int = 0, ctx: Context = None) -> list:
    """Get list of task summaries with pagination."""
    return await list_task_summaries_tool(limit, offset, ctx)

@mcp.tool()
async def list_tasks(column_id: str = None, assigned_to: str = None, title: str = None, limit: int = 50, offset: int = 0, include_deleted: bool = False, ctx: Context = None) -> list:
    """Get detailed list of tasks with optional filtering."""
    return await list_tasks_tool(column_id, assigned_to, title, limit, offset, include_deleted, ctx)

@mcp.tool()
async def create_task(title: str, column_id: str, description: str = None, assigned_users: list = None, deadline: dict = None, time_tracking: dict = None, stickers: dict = None, subtasks: list = None, checklists: list = None, completed: bool = None, archived: bool = None, ctx: Context = None) -> dict:
    """Create a new task. 
    
    🚨 CRITICAL: description parameter MUST be in HTML format!
    - Use <br> for line breaks (NOT \\n)
    - Use <b>text</b> for bold, <i>text</i> for italic
    - Example: "Fix bug<br><br><b>Steps:</b><br>1. Check login<br>2. Fix error"
    - Plain text will display incorrectly in YouGile interface!
    """
    return await create_task_tool(title, column_id, description, assigned_users, deadline, time_tracking, stickers, subtasks, checklists, completed, archived, ctx)

@mcp.tool()
async def get_task(task_id: str, ctx: Context) -> dict:
    """Get detailed information about a specific task."""
    return await get_task_tool(task_id, ctx)

@mcp.tool()
async def get_tasks_by_date(assigned_to: str = None, created_by: str = None, target_date: str = None, completed_only: bool = False, limit: int = 5000, ctx: Context = None) -> list:
    """Get tasks filtered by date and completion status.
    
    Examples:
    - get_tasks_by_date(assigned_to="user-id") - all tasks assigned to user for today
    - get_tasks_by_date(created_by="user-id") - all tasks created by user for today  
    - get_tasks_by_date(target_date="2024-01-15", completed_only=True) - completed tasks for specific date
    - get_tasks_by_date(assigned_to="user-id", completed_only=True) - completed tasks by user for today
    - get_tasks_by_date(created_by="user-id", target_date="2024-01-15") - tasks created by user on specific date
    """
    return await get_tasks_by_date_tool(assigned_to, created_by, target_date, completed_only, limit, ctx)

@mcp.tool()
async def update_task(task_id: str, title: str = None, description: str = None, column_id: str = None, assigned_users: list = None, deadline: dict = None, time_tracking: dict = None, stickers: dict = None, subtasks: list = None, checklists: list = None, completed: bool = None, archived: bool = None, deleted: bool = None, ctx: Context = None) -> dict:
    """Update task information.
    
    🚨 CRITICAL: description parameter MUST be in HTML format!
    - Use <br> for line breaks (NOT \\n)
    - Use <b>text</b> for bold, <i>text</i> for italic
    - Example: "Updated requirements<br><br><b>Changes:</b><br>• Added validation<br>• Fixed bugs"
    - Plain text will display incorrectly in YouGile interface!
    """
    return await update_task_tool(task_id, title, description, column_id, assigned_users, deadline, time_tracking, stickers, subtasks, checklists, completed, archived, deleted, ctx)

@mcp.tool()  
async def delete_task(task_id: str, ctx: Context = None) -> dict:
    """Delete a task (soft delete)."""
    return await update_task_tool(task_id, deleted=True, ctx=ctx)

@mcp.tool()
async def set_task_deadline(task_id: str, deadline_timestamp: int, start_date_timestamp: int = None, with_time: bool = True, ctx: Context = None) -> dict:
    """Set task deadline sticker.
    
    Args:
        task_id: ID of the task to set deadline for
        deadline_timestamp: Deadline timestamp in MILLISECONDS (13 digits, e.g. 1653029146646)
        start_date_timestamp: Optional start date timestamp in MILLISECONDS
        with_time: Whether to display time on the sticker, or only date
    """
    # Auto-convert seconds to milliseconds if needed
    if deadline_timestamp < 10000000000:  # Less than 10 digits = seconds
        deadline_timestamp *= 1000
        if ctx:
            await ctx.info(f"Auto-converted deadline timestamp to milliseconds: {deadline_timestamp}")
    
    deadline_data = {
        "deadline": deadline_timestamp,
        "withTime": with_time,
        "blockedPoints": [],  # Required field
        "links": []  # Required field
    }
    
    if start_date_timestamp:
        # Auto-convert start date if needed
        if start_date_timestamp < 10000000000:
            start_date_timestamp *= 1000
            if ctx:
                await ctx.info(f"Auto-converted start date timestamp to milliseconds: {start_date_timestamp}")
        deadline_data["startDate"] = start_date_timestamp
        
    return await update_task_tool(task_id, deadline=deadline_data, ctx=ctx)

@mcp.tool()
async def set_task_time_tracking(task_id: str, planned_hours: int = None, actual_hours: int = None, ctx: Context = None) -> dict:
    """Set task time tracking sticker."""
    time_tracking_data = {}
    if planned_hours is not None:
        time_tracking_data["plan"] = planned_hours
    if actual_hours is not None:
        time_tracking_data["work"] = actual_hours
    return await update_task_tool(task_id, time_tracking=time_tracking_data, ctx=ctx)

@mcp.tool()
async def set_task_custom_stickers(task_id: str, sticker_values: dict, ctx: Context = None) -> dict:
    """Set custom stickers on task (sticker_id -> state_id mapping)."""
    return await update_task_tool(task_id, stickers=sticker_values, ctx=ctx)

@mcp.tool()  
async def remove_task_sticker(task_id: str, sticker_type: str, ctx: Context = None) -> dict:
    """Remove sticker from task by setting it to deleted/removed state."""
    if sticker_type == "deadline":
        return await update_task_tool(task_id, deadline={"deleted": True}, ctx=ctx)
    elif sticker_type == "timeTracking":
        return await update_task_tool(task_id, time_tracking={"deleted": True}, ctx=ctx)
    else:
        # For custom stickers, use "-" to detach
        sticker_data = {sticker_type: "-"}
        return await update_task_tool(task_id, stickers=sticker_data, ctx=ctx)

@mcp.tool()
async def get_task_chat_subscribers(task_id: str, ctx: Context) -> list:
    """Get list of users subscribed to task chat."""
    return await get_task_chat_subscribers_tool(task_id, ctx)

@mcp.tool()
async def update_task_chat_subscribers(task_id: str, subscribers: list, ctx: Context) -> dict:
    """Update task chat subscribers list."""
    return await update_task_chat_subscribers_tool(task_id, subscribers, ctx)

# String Stickers Management Tools
@mcp.tool()
async def list_string_stickers(limit: int = 50, offset: int = 0, include_deleted: bool = False, ctx: Context = None) -> list:
    """Get list of custom string stickers available in the company."""
    return await list_string_stickers_tool(limit, offset, include_deleted, ctx)

@mcp.tool()
async def get_string_sticker(sticker_id: str, ctx: Context) -> dict:
    """Get detailed information about a specific string sticker including its states."""
    return await get_string_sticker_tool(sticker_id, ctx)

@mcp.tool()  
async def get_string_sticker_state(sticker_id: str, state_id: str, ctx: Context) -> dict:
    """Get information about a specific state of a string sticker."""
    return await get_string_sticker_state_tool(sticker_id, state_id, ctx)

@mcp.tool()
async def decode_task_stickers(stickers_dict: dict, ctx: Context = None) -> dict:
    """Decode task stickers dictionary into readable sticker and state information.
    
    Takes a dictionary of sticker_id -> state_id (like from task.stickers) and returns
    readable names, colors, and icons for each sticker and its current state.
    """
    return await decode_task_stickers_tool(stickers_dict, ctx)

# Chat and Communication Tools
@mcp.tool()
async def list_group_chats(ctx: Context) -> list:
    """Get list of all group chats."""
    return await list_group_chats_tool(ctx)

@mcp.tool()
async def create_group_chat(title: str, participants: list = None, ctx: Context = None) -> dict:
    """Create a new group chat."""
    return await create_group_chat_tool(title, participants, ctx)

@mcp.tool()
async def get_group_chat(chat_id: str, ctx: Context) -> dict:
    """Get detailed information about a specific group chat."""
    return await get_group_chat_tool(chat_id, ctx)

@mcp.tool()
async def get_chat_messages(chat_id: str, limit: int = 50, ctx: Context = None) -> list:
    """Get messages from a chat (task comments or group chat messages)."""
    return await get_chat_messages_tool(chat_id, limit, ctx)

@mcp.tool()
async def send_chat_message(chat_id: str, message: str, ctx: Context = None) -> dict:
    """Send a message to a chat (add comment to task or send group chat message)."""
    return await send_chat_message_tool(chat_id, message, ctx)

@mcp.tool()
async def get_chat_message(chat_id: str, message_id: str, ctx: Context = None) -> dict:
    """Get a specific message from a chat."""
    return await get_chat_message_tool(chat_id, message_id, ctx)

@mcp.tool()
async def update_chat_message(chat_id: str, message_id: str, message: str, ctx: Context = None) -> dict:
    """Update/edit a message in a chat."""
    return await update_chat_message_tool(chat_id, message_id, message, ctx)

# Task Comment Tools (convenient aliases)
@mcp.tool()
async def get_task_comments(task_id: str, limit: int = 50, ctx: Context = None) -> list:
    """Get comments for a specific task."""
    return await get_task_comments_tool(task_id, limit, ctx)

@mcp.tool()
async def add_task_comment(task_id: str, comment: str, ctx: Context = None) -> dict:
    """Add a comment to a specific task.
    
    🚨 CRITICAL: comment parameter MUST be in HTML format!
    - Use <br> for line breaks (NOT \\n)
    - Use <b>text</b> for bold, <i>text</i> for italic
    - Example: "Status update<br><br><b>Progress:</b><br>• Completed testing<br>• Ready for review"
    - Plain text will display incorrectly in YouGile interface!
    """
    return await add_task_comment_tool(task_id, comment, ctx)

# Register MCP Resources
@mcp.resource("yougile://api/overview")
def api_overview() -> str:
    """YouGile API v2.0 comprehensive overview and getting started guide."""
    return get_api_overview()

@mcp.resource("yougile://api/endpoints")
def api_endpoints() -> str:
    """Complete list of all 65 YouGile API endpoints organized by category."""
    return get_api_endpoints()

@mcp.resource("yougile://projects/{project_id}")
def project_info(project_id: str) -> str:
    """Detailed information about a specific project including schema and examples."""
    return get_project_info(project_id)

@mcp.resource("yougile://tasks/{task_id}")
def task_info(task_id: str) -> str:
    """Detailed information about a specific task including schema and operations."""
    return get_task_info(task_id)


# Register MCP Prompts
@mcp.prompt(title="Setup New Project")
def setup_project(project_name: str, project_type: str = "kanban"):
    """Step-by-step guide for creating and configuring a new project in YouGile."""
    return setup_new_project_prompt(project_name, project_type)

@mcp.prompt(title="Create Task")
def create_task_prompt(task_title: str, priority: str = "medium") -> str:
    """Template for creating well-structured tasks with all necessary details."""
    return create_task_workflow_prompt(task_title, priority)

@mcp.prompt(title="Sprint Planning")
def plan_sprint(sprint_name: str, duration_weeks: int = 2):
    """Complete sprint planning workflow with backlog refinement and capacity planning."""
    return sprint_planning_prompt(sprint_name, duration_weeks)

@mcp.prompt(title="Daily Standup Report")
def daily_standup(team_user_ids: str = "team-user-ids-here"):
    """Generate daily standup report for team meetings."""
    user_list = team_user_ids.split(",") if team_user_ids != "team-user-ids-here" else None
    return daily_standup_prompt(user_list)

@mcp.prompt(title="Project Health Check")
def project_health_check(project_id: str):
    """Comprehensive project health analysis with task flow, team performance, and timeline metrics."""
    return project_health_check_prompt(project_id)

@mcp.prompt(title="User Productivity Report")
def user_productivity_report(user_id: str, target_date: str = None):
    """Individual user productivity analysis with task completion, creation, and collaboration metrics."""
    return user_productivity_report_prompt(user_id, target_date)

@mcp.prompt(title="Weekly Team Report")
def weekly_team_report(team_user_ids: str, start_date: str):
    """Weekly team performance report with productivity trends and collaboration metrics."""
    user_list = team_user_ids.split(",")
    return weekly_team_report_prompt(user_list, start_date)

@mcp.prompt(title="Task Escalation")
def task_escalation(task_id: str):
    """Task escalation workflow when something is blocked or needs urgent attention."""
    return task_escalation_prompt(task_id)

@mcp.prompt(title="Onboard Team Member")
def onboard_team_member(new_member_name: str, role: str):
    """Team member onboarding workflow with project access and task assignment."""
    return onboarding_new_team_member_prompt(new_member_name, role)

@mcp.prompt(title="Deadline Crunch Management")
def deadline_crunch_management(deadline_date: str):
    """Managing tasks when approaching critical deadlines with priority triage and resource allocation."""
    return deadline_crunch_management_prompt(deadline_date)

@mcp.prompt(title="Sprint Retrospective")
def sprint_retrospective(sprint_end_date: str, team_user_ids: str):
    """Sprint/project retrospective analysis with performance patterns and improvement insights."""
    user_list = team_user_ids.split(",")
    return retrospective_analysis_prompt(sprint_end_date, user_list)

@mcp.prompt(title="HTML Formatting Guide")
def html_formatting_guide():
    """Essential guide for HTML formatting in YouGile tasks and comments - CRITICAL for proper display."""
    return html_formatting_guide_prompt()

@mcp.prompt(title="API Usage Guide") 
def api_usage_guide():
    """Quick reference for using YouGile MCP tools with correct parameters and formats."""
    return api_usage_guide_prompt()


async def initialize_auth():
    """Initialize authentication automatically from environment variables."""
    if not all([settings.yougile_email, settings.yougile_password, settings.yougile_company_id]):
        print("⚠️  YouGile credentials not configured in .env file")
        print("Add YOUGILE_EMAIL, YOUGILE_PASSWORD, YOUGILE_COMPANY_ID to .env")
        return False
    
    try:
        print("🔑 Initializing YouGile authentication...")
        
        # Check if we already have a valid API key
        if settings.yougile_api_key:
            print("📝 Found existing API key, testing...")
            try:
                # Test existing key
                auth.auth_manager.set_credentials(settings.yougile_api_key, settings.yougile_company_id)
                async with YouGileClient(auth.auth_manager) as client:
                    # Test key with a simple API call (get users)
                    await client.get("/users")
                
                print("✅ Existing API key is valid, using it")
                return True
                
            except Exception as e:
                print(f"⚠️  Existing API key invalid ({e}), creating new one...")
        
        # Create new API key
        print("🔄 Creating new API key...")
        temp_auth = auth.auth_manager.__class__()
        async with YouGileClient(temp_auth) as client:
            api_key = await auth_api.create_api_key(
                client, 
                settings.yougile_email, 
                settings.yougile_password, 
                settings.yougile_company_id
            )
            
            # Save to global auth manager
            auth.auth_manager.set_credentials(api_key, settings.yougile_company_id)
            
            # Save API key to .env file for future use
            await save_api_key_to_env(api_key)
            
        print("✅ New API key created and saved successfully")
        return True
        
    except Exception as e:
        print(f"❌ Failed to initialize authentication: {e}")
        return False

async def save_api_key_to_env(api_key: str):
    """Save API key to .env file for future reuse."""
    import os
    from pathlib import Path
    
    env_file = Path(".env")
    if not env_file.exists():
        return
    
    try:
        # Read current .env content
        with open(env_file, 'r') as f:
            lines = f.readlines()
        
        # Update or add API key line
        updated = False
        for i, line in enumerate(lines):
            if line.startswith('YOUGILE_API_KEY=') or line.startswith('# YOUGILE_API_KEY='):
                lines[i] = f"YOUGILE_API_KEY={api_key}\n"
                updated = True
                break
        
        if not updated:
            lines.append(f"\nYOUGILE_API_KEY={api_key}\n")
        
        # Write back to .env
        with open(env_file, 'w') as f:
            f.writelines(lines)
            
        print("💾 API key saved to .env file for future use")
        
    except Exception as e:
        print(f"⚠️  Could not save API key to .env: {e}")

def main():
    """Main entry point for the server."""
    # Initialize authentication if credentials are provided
    if settings.yougile_email and settings.yougile_password and settings.yougile_company_id:
        asyncio.run(initialize_auth())
    
    mcp.run()


if __name__ == "__main__":
    main()