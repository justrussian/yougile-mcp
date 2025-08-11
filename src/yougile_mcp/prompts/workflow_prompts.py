"""
MCP prompts for common YouGile workflows.
Provides templates and conversation flows for typical project management tasks.
"""

from typing import List
from mcp.server.fastmcp.prompts import base


def setup_new_project_prompt(project_name: str, project_type: str = "kanban") -> List[base.Message]:
    """
    Guide for setting up a new project in YouGile.
    """
    return [
        base.UserMessage(f"I want to create a new {project_type} project called '{project_name}' in YouGile."),
        base.AssistantMessage(f"""I'll help you set up your new {project_type} project '{project_name}' step by step.

Let me start by creating the project and then we'll configure the team and workflow structure.

First, I'll use create_project() to set up the basic project structure. Do you have specific team members you want to assign to this project?"""),
        base.UserMessage("Yes, I want to add my development team to this project."),
        base.AssistantMessage("""Perfect! I'll help you:

1. Create the project with create_project() - returns only project ID
2. Add team members using the users parameter  
3. Set up boards with create_board() - returns only board ID
4. Create initial columns with create_column() (requires title, board_id, optional color 1-16)
5. Configure project roles if needed

Let's start - what are the user IDs of your team members, and what roles should they have (admin, developer, viewer)?""")
    ]


def create_task_workflow_prompt(task_title: str, priority: str = "medium") -> str:
    """
    Template for creating well-structured tasks.
    """
    return f"""Help me create a comprehensive task in YouGile: "{task_title}" with {priority} priority.

Please guide me through:

1. First, use get_user_context() to check for any default project/board settings
2. Use list_columns() to find the right column for this task
3. Use create_task() with proper details including:
   - Descriptive title and acceptance criteria in task description (MANDATORY HTML format: use <br> for line breaks, NOT \\n)
   - Assign to appropriate team members (use list_users() to find user IDs)  
   - Set deadline if needed using the deadline parameter
   - Add time tracking estimates if applicable
   - Include any custom stickers for priority/category

4. After creating, set up communication:
   - Use update_task_chat_subscribers() to add relevant people
   - Add initial comment with add_task_comment() explaining the context (MANDATORY HTML format: use <br> for line breaks)

5. For tracking, show me how to use get_tasks_by_date() to monitor progress

What specific work needs to be done for "{task_title}" and who should be involved?"""


def sprint_planning_prompt(sprint_name: str, duration_weeks: int = 2) -> List[base.Message]:
    """
    Complete sprint planning workflow.
    """
    return [
        base.UserMessage(f"I need to plan '{sprint_name}' sprint for {duration_weeks} weeks in YouGile."),
        base.AssistantMessage(f"""Great! Let's plan your {duration_weeks}-week sprint '{sprint_name}'. I'll guide you through the complete process.

First, let me gather some information about your current setup. I'll use list_projects() and list_boards() to see your project structure.

What's your main goal for this sprint?"""),
        base.UserMessage("The main goal is to complete the user authentication system."),
        base.AssistantMessage("""Perfect goal! User authentication is critical. Let me help you plan this systematically:

1. **Sprint Setup**: I'll create a dedicated board for this sprint using create_board() - returns board ID only
2. **Backlog Review**: Use list_tasks() to find existing auth-related tasks
3. **Capacity Planning**: Use get_tasks_by_date() to check team workload
4. **Task Assignment**: Break down auth features and assign using create_task()
5. **Sprint Kickoff**: Set up task communication and tracking

Let's start by creating the sprint board and identifying all authentication features needed. What auth components do you need: login, registration, password reset, session management?""")
    ]


def daily_standup_prompt(team_user_ids: List[str] = None) -> str:
    """
    Generate daily standup report for the team.
    """
    user_list = team_user_ids or ["your-team-user-ids-here"]
    return f"""Help me generate a daily standup report for our team meeting.

Please gather this information for each team member:

For each user ID {user_list}:
1. Use get_tasks_by_date(assigned_to="user-id", completed_only=True) - what they completed yesterday
2. Use get_tasks_by_date(assigned_to="user-id") - what they're working on today  
3. Use list_tasks(assigned_to="user-id", column_id="blocked-column-id") - any blockers

Then create a summary showing:
- Team velocity (total completed tasks)
- Current sprint progress
- Any blockers or overdue items needing attention
- Workload distribution across team members

Format this as a clear standup report for our team meeting."""


def project_health_check_prompt(project_id: str) -> str:
    """
    Comprehensive project health analysis.
    """
    return f"""Perform a comprehensive health check for project {project_id} in YouGile.

Please analyze:

1. **Task Flow Analysis**:
   - Use list_boards(project_id="{project_id}") to get all boards
   - For each board, use list_columns() to see workflow stages
   - Use list_tasks() with column filters to check task distribution
   - Identify bottlenecks where tasks are piling up

2. **Team Performance**: 
   - Use get_tasks_by_date() to check daily productivity for each team member
   - Compare assigned vs completed tasks to find workload imbalances
   - Check for overloaded or underutilized team members

3. **Timeline Health**:
   - Use list_tasks() to find tasks with deadlines 
   - Identify overdue tasks that need immediate attention
   - Check sprint/milestone progress using date filtering

4. **Communication Health**:
   - Use list_group_chats() to check if team communication is active
   - Look for tasks without recent comments that might be stalled

Generate a comprehensive report with specific metrics, identified risks, and actionable recommendations for improving project health."""


def user_productivity_report_prompt(user_id: str, target_date: str = None) -> str:
    """
    Individual user productivity analysis.
    """
    date_clause = f"for {target_date}" if target_date else "for today"
    return f"""Generate a detailed productivity report for user {user_id} {date_clause}.

Please analyze:

1. **Task Completion**:
   - Use get_tasks_by_date(assigned_to="{user_id}", completed_only=True, target_date="{target_date or 'today'}")
   - Show what they accomplished and task complexity

2. **Task Creation**: 
   - Use get_tasks_by_date(created_by="{user_id}", target_date="{target_date or 'today'}")
   - See what new work they initiated

3. **Current Workload**:
   - Use get_tasks_by_date(assigned_to="{user_id}", target_date="{target_date or 'today'}")
   - Check active vs completed ratio

4. **Collaboration**:
   - Use get_task_chat_subscribers() on their tasks to see collaboration level
   - Check recent task comments for communication activity

5. **Time Tracking** (if available):
   - Look for tasks with time tracking data
   - Compare planned vs actual time spent

Create a comprehensive productivity summary with insights about their work patterns, efficiency, and areas for improvement."""


def weekly_team_report_prompt(team_user_ids: List[str], start_date: str) -> str:
    """
    Weekly team performance report.
    """
    return f"""Generate a comprehensive weekly team report starting from {start_date}.

For team members {team_user_ids}, please analyze:

1. **Weekly Productivity Trends**:
   - Use get_tasks_by_date() for each day of the week
   - Track daily completion rates for each team member
   - Identify productivity patterns and peak performance days

2. **Task Creation vs Completion**:
   - Compare tasks created vs completed for the week
   - Check if backlog is growing or shrinking
   - Identify who's contributing most to task creation

3. **Collaboration Metrics**:
   - Check task assignments and cross-team collaboration
   - Use task chat subscribers to measure team communication
   - Identify isolated vs collaborative work patterns

4. **Sprint/Project Progress**:
   - If using sprints, measure sprint goal achievement
   - Check milestone progress using deadline tracking
   - Identify any projects falling behind schedule

5. **Quality Indicators**:
   - Look for tasks that were reopened or moved backward
   - Check for tasks with many revisions or long completion times

Provide actionable insights for improving team performance next week."""


def task_escalation_prompt(task_id: str) -> List[base.Message]:
    """
    Task escalation workflow when something is blocked.
    """
    return [
        base.UserMessage(f"Task {task_id} is blocked and needs escalation. What should I do?"),
        base.AssistantMessage("""I'll help you properly escalate this blocked task. Let me gather context first.

First, let me check the task details using get_task() to understand the current status, assignees, and any existing comments about the blocker."""),
        base.UserMessage("The task has been stuck for 3 days with no progress."),
        base.AssistantMessage(f"""Got it - a 3-day blocked task needs immediate attention. Here's my escalation plan:

1. **Document the Issue**: Use add_task_comment(task_id="{task_id}", comment="🚨 ESCALATION: Task blocked for 3 days...")

2. **Update Stakeholders**: Use update_task_chat_subscribers() to add managers/leads who need visibility

3. **Change Task Status**: Use update_task() to move to a "Blocked" column if you have one

4. **Create Follow-up Actions**: Use create_task() to create specific unblocking tasks

5. **Set Urgency**: Use task stickers or priority fields to mark as high priority

What specific blocker is preventing progress? Is it technical, waiting for approval, missing requirements, or external dependency?""")
    ]


def onboarding_new_team_member_prompt(new_member_name: str, role: str) -> List[base.Message]:
    """
    Team member onboarding workflow.
    """
    return [
        base.UserMessage(f"I need to onboard {new_member_name} as a {role} to our YouGile projects."),
        base.AssistantMessage(f"""Perfect! I'll help you onboard {new_member_name} as a {role}. Let me set up a comprehensive onboarding plan.

First, I'll use list_projects() to see which projects they should have access to, then use list_users() to understand our current team structure."""),
        base.UserMessage(f"They should have access to all development projects and work closely with the backend team."),
        base.AssistantMessage(f"""Excellent! Here's my onboarding plan for {new_member_name}:

1. **Project Access Setup**:
   - Use update_project() to add them to all development projects with {role} permissions
   - Use list_boards() to identify key boards they'll work with

2. **Team Integration**:
   - Use create_group_chat() or add to existing team chats
   - Use list_group_chats() to find backend team communications

3. **Initial Task Assignment**:
   - Use create_task() to create onboarding tasks (setup, introductions, first small project)
   - Use update_task_chat_subscribers() to connect them with mentors

4. **Monitoring Setup**:
   - Use get_tasks_by_date() to track their first week progress
   - Set up regular check-ins with get_tasks_by_date(assigned_to="new-member-user-id")

What's their email address so I can help you send them project invitations and setup their first tasks?""")
    ]


def deadline_crunch_management_prompt(deadline_date: str) -> str:
    """
    Managing tasks when approaching a critical deadline.
    """
    return f"""Help me manage our team's work as we approach the critical deadline on {deadline_date}.

Please help me:

1. **Deadline Assessment**:
   - Use list_tasks() to find all tasks with deadlines around {deadline_date}
   - Use get_tasks_by_date(target_date="{deadline_date}", completed_only=False) to see scope

2. **Priority Triage**:
   - Identify which tasks are truly critical vs nice-to-have
   - Use task stickers or priorities to mark must-have items
   - Consider using update_task() to move non-critical items to future sprints

3. **Resource Allocation**:
   - Use get_tasks_by_date() to check current team workload
   - Identify who has capacity to take on additional critical tasks
   - Redistribute work using update_task() with new assignees

4. **Communication Plan**:
   - Use update_task_chat_subscribers() to ensure all critical tasks have proper oversight
   - Use add_task_comment() to add urgency markers and daily check-in requirements

5. **Progress Tracking**:
   - Set up daily monitoring using get_tasks_by_date() for deadline-related tasks
   - Create escalation plan for any tasks that fall behind

Help me execute this crunch-time management plan efficiently."""


def html_formatting_guide_prompt() -> str:
    """
    Essential guide for HTML formatting in YouGile tasks and comments.
    """
    return """🚨 CRITICAL: YouGile requires HTML format for ALL task descriptions and comments

**Why HTML is MANDATORY:**
- Plain text doesn't display properly in YouGile interface
- Line breaks \\n are ignored - you MUST use <br> tags
- Without HTML, descriptions appear as single unreadable lines

**Required HTML formatting:**
```
✅ CORRECT:
"Fix login bug<br><br><b>Steps to reproduce:</b><br>1. Go to login page<br>2. Enter credentials<br>3. Click submit<br><br><b>Expected:</b> User logged in<br><b>Actual:</b> Error message appears"

❌ WRONG:
"Fix login bug\\n\\nSteps to reproduce:\\n1. Go to login page\\n2. Enter credentials\\n3. Click submit\\n\\nExpected: User logged in\\nActual: Error message appears"
```

**Essential HTML tags:**
- Line breaks: `<br>` (NEVER use \\n)
- Bold text: `<b>text</b>`
- Italic text: `<i>text</i>`
- Underline: `<u>text</u>`
- Links: `<a href="https://example.com">link text</a>`
- Lists: `<ul><li>item 1</li><li>item 2</li></ul>`

**Examples for common scenarios:**
```
Bug report:
"<b>Bug:</b> Login fails<br><br><b>Steps:</b><br>1. Open app<br>2. Enter email<br>3. Click login<br><br><b>Error:</b> <i>Invalid credentials</i>"

Feature request:
"<b>Feature:</b> Dark mode toggle<br><br><b>Requirements:</b><br>• System preference detection<br>• Manual toggle button<br>• Persist user choice<br><br><a href='https://design.com/mockup'>Design mockup</a>"

Task with checklist:
"<b>Implement user authentication</b><br><br><b>Backend tasks:</b><br>• Database schema<br>• API endpoints<br>• JWT tokens<br><br><b>Frontend tasks:</b><br>• Login form<br>• User dashboard"
```

**Remember:** Always use HTML format or your text will be unreadable!"""


def api_usage_guide_prompt() -> str:
    """
    Guide for using YouGile MCP tools with correct parameters.
    """
    return """Here's a quick reference for using YouGile MCP tools correctly:

**Project Creation:**
- `create_project(title="My Project", users={"user-uuid": "admin"})` 
- Returns: `{"id": "project-uuid"}` only
- Use `get_project(project_id="project-uuid")` to get full details after creation

**Board Creation:**
- `create_board(title="Sprint Board", project_id="project-uuid")`
- Returns: `{"id": "board-uuid"}` only
- Use `get_board(board_id="board-uuid")` to get full details after creation

**Column Creation:** 
- `create_column(title="To Do", board_id="board-uuid")` - basic column
- `create_column(title="In Progress", board_id="board-uuid", color=5)` - with color (1-16)
- Returns: `{"id": "column-uuid"}` only
- Colors: 1=gray, 2=red, 3=orange, 4=yellow, 5=green, 6=teal, 7=blue, 8=purple, etc.

**Important Notes:**
- Creation tools return only IDs, not full objects
- Always use `get_*` tools after creation if you need full object details
- Column colors: 1-16 (1=gray, 2=red, 3=orange, 4=yellow, 5=green, 6=teal, 7=blue, 8=purple)
- All UUIDs must be valid format: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
- **🚨 CRITICAL - HTML FORMAT REQUIRED**: Task descriptions and comments MUST use HTML format
  - Line breaks: use `<br>` tag (NEVER use \\n - it won't display!)
  - Formatting: `<b>bold</b>`, `<i>italic</i>`, `<u>underline</u>`
  - Links: `<a href="https://example.com">text</a>`
  - Lists: `<ul><li>item</li></ul>` or `<ol><li>item</li></ol>`
  - ⚠️ Plain text breaks YouGile interface - use HTML_FORMATTING_GUIDE prompt for examples

**Checklists Support**: Tasks can have checklists for detailed tracking
  - Format: `[{"title": "Checklist Name", "items": [{"title": "Item 1", "isCompleted": false}]}]`
  - Multiple checklists per task: `[{"title": "Backend", "items": [...]}, {"title": "Frontend", "items": [...]}]`
  - Use for: acceptance criteria, testing steps, deployment checklist

**Workflow Example:**
```
1. project = create_project(title="Website", users={"user-id": "admin"})
2. board = create_board(title="Development", project_id=project.id) 
3. col1 = create_column(title="Backlog", board_id=board.id, color=1)
4. col2 = create_column(title="In Progress", board_id=board.id, color=5)
5. col3 = create_column(title="Done", board_id=board.id, color=13)
```"""


def retrospective_analysis_prompt(sprint_end_date: str, team_user_ids: List[str]) -> str:
    """
    Sprint/project retrospective analysis.
    """
    return f"""Help me conduct a thorough retrospective analysis for the sprint that ended on {sprint_end_date}.

For team {team_user_ids}, please analyze:

1. **Sprint Goal Achievement**:
   - Use get_tasks_by_date(target_date="{sprint_end_date}", completed_only=True) 
   - Compare planned vs completed tasks
   - Identify which features/goals were fully delivered

2. **Team Performance Patterns**:
   - Use get_tasks_by_date() for each team member across the sprint period
   - Identify productivity trends, peak performance days
   - Check collaboration patterns through task assignments

3. **Process Bottlenecks**:
   - Use list_tasks() with column filters to see where tasks got stuck
   - Identify workflow stages that consistently slow down delivery
   - Look for tasks that took longer than expected

4. **Quality Metrics**:
   - Find tasks that were reopened or required significant rework
   - Check for patterns in task comments about issues or blockers

5. **Communication Effectiveness**:
   - Analyze task chat activity and team collaboration
   - Identify gaps in communication that led to delays

Generate insights for what went well, what needs improvement, and specific action items for the next sprint to increase team effectiveness."""