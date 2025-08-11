"""
MCP prompts specifically for teaching users how to use filtering capabilities.
Provides practical examples and best practices for efficient data retrieval.
"""

from typing import List
from mcp.server.fastmcp.prompts import base


def filtering_best_practices_prompt() -> str:
    """
    Guide for using filtering parameters effectively in YouGile MCP tools.
    
    Returns:
        Comprehensive guide for filtering usage
    """
    return """# YouGile MCP Filtering Guide

Learn how to use filtering parameters effectively to get exactly the data you need without overwhelming results.

## Available Filtering Tools

### 1. Board Filtering (`list_boards`)
**Parameters:**
- `project_id`: Get boards from specific project only
- `title`: Search boards by name (partial match)
- `limit`: Maximum boards to return (default: 50)
- `offset`: Skip first N boards for pagination
- `include_deleted`: Include deleted boards (default: false)

**Examples:**
```
# Get all boards from a specific project
list_boards(project_id="proj-123")

# Search for boards with "sprint" in the name
list_boards(title="sprint")

# Get next 50 boards (pagination)
list_boards(limit=50, offset=50)

# Find boards in project containing "mobile"
list_boards(project_id="proj-mobile", title="dev")
```

### 2. Task Filtering (`list_tasks`)
**Parameters:**
- `column_id`: Get tasks from specific column/status
- `assigned_to`: Get tasks assigned to specific user
- `title`: Search tasks by title (partial match)  
- `limit`: Maximum tasks to return (default: 50)
- `offset`: Skip first N tasks for pagination
- `include_deleted`: Include deleted tasks (default: false)

**Examples:**
```
# Get all tasks in "In Progress" column
list_tasks(column_id="col-in-progress")

# Get tasks assigned to specific user
list_tasks(assigned_to="user-john-doe")

# Search for authentication-related tasks
list_tasks(title="auth")

# Get overdue tasks for user (combine filters)
list_tasks(assigned_to="user-123", title="urgent")

# Pagination for large task lists
list_tasks(limit=25, offset=0)  # First 25 tasks
list_tasks(limit=25, offset=25) # Next 25 tasks
```

### 3. Task Summaries (`list_task_summaries`)
**Parameters:**
- `limit`: Maximum summaries to return (default: 50)
- `offset`: Skip first N summaries for pagination

**Examples:**
```
# Get first 10 task summaries
list_task_summaries(limit=10)

# Get summaries 50-100
list_task_summaries(limit=50, offset=50)
```

## Best Practices

### 1. Start Specific, Then Broaden
```
# ✅ Good: Start with specific project
list_boards(project_id="current-project")

# ❌ Avoid: Getting all boards without context
list_boards()
```

### 2. Use Meaningful Limits
```
# ✅ Good: Reasonable limits for exploration
list_tasks(limit=20)

# ❌ Avoid: Excessive limits that may timeout
list_tasks(limit=1000)
```

### 3. Combine Filters Effectively  
```
# ✅ Good: Multiple relevant filters
list_tasks(assigned_to="user-123", column_id="col-review")

# ✅ Good: Search within project scope
list_boards(project_id="proj-web", title="sprint")
```

### 4. Use Pagination for Large Datasets
```
# ✅ Good: Process in chunks
list_tasks(limit=50, offset=0)   # First batch
list_tasks(limit=50, offset=50)  # Second batch
list_tasks(limit=50, offset=100) # Third batch
```

### 5. Leverage Search for Discovery
```
# ✅ Good: Find related items
list_tasks(title="bug")          # All bug-related tasks
list_boards(title="mobile")      # Mobile-related boards
```

## Common Use Cases

### Project Health Check
```python
# 1. Get project boards
boards = list_boards(project_id="proj-123")

# 2. Check each board's task distribution
for board in boards:
    tasks = list_tasks(column_id=f"col-{board.id}-todo")
    in_progress = list_tasks(column_id=f"col-{board.id}-progress")
    done = list_tasks(column_id=f"col-{board.id}-done")
```

### Team Workload Analysis  
```python
# Check workload per team member
team_members = ["user-alice", "user-bob", "user-charlie"]
for member in team_members:
    assigned_tasks = list_tasks(assigned_to=member)
    print(f"{member}: {len(assigned_tasks)} tasks")
```

### Sprint Planning
```python
# Find sprint-related boards
sprint_boards = list_boards(title="sprint")

# Get backlog items (typically in first column)
backlog = list_tasks(column_id="col-backlog", limit=100)

# Check current sprint progress
current_sprint = list_tasks(title="sprint-24")
```

### Debugging and Investigation
```python
# Find tasks with specific keywords
auth_tasks = list_tasks(title="auth")
bug_tasks = list_tasks(title="bug")
urgent_tasks = list_tasks(title="urgent")

# Check specific user's assignments
user_tasks = list_tasks(assigned_to="problematic-user-id")
```

## Performance Tips

1. **Always use reasonable limits** - Start with 20-50 items
2. **Filter by project first** - Reduces search scope significantly  
3. **Use title search for discovery** - More efficient than browsing all items
4. **Paginate large result sets** - Prevents timeouts and memory issues
5. **Combine filters intelligently** - More specific = faster results

## Error Prevention

- **Validate UUIDs**: Ensure project_id, column_id, assigned_to are valid UUIDs
- **Handle empty results**: Always check if returned lists are empty
- **Use appropriate offsets**: Don't skip more items than exist
- **Check permissions**: Some filters may return empty due to access restrictions

Remember: Effective filtering makes YouGile MCP tools much more practical and responsive!"""


def task_management_filtering_prompt() -> List[base.Message]:
    """
    Interactive guide for using task filtering in real scenarios.
    
    Returns:
        Conversation flow teaching task filtering
    """
    return [
        base.UserMessage("I need to manage tasks more efficiently. There are too many tasks and I can't find what I need."),
        base.AssistantMessage("""I'll teach you how to use task filtering to find exactly what you need! YouGile MCP tools have powerful filtering capabilities.

**Common Task Management Scenarios:**

1. **Find Your Assigned Tasks**
   ```
   list_tasks(assigned_to="your-user-id")
   ```

2. **Check Specific Column/Status**
   ```
   list_tasks(column_id="col-in-progress")  # Tasks in progress
   list_tasks(column_id="col-review")       # Tasks waiting for review
   ```

3. **Search by Keywords**
   ```
   list_tasks(title="bug")        # Bug-related tasks
   list_tasks(title="urgent")     # Urgent tasks
   list_tasks(title="api")        # API-related tasks
   ```

4. **Combine Multiple Filters**
   ```
   list_tasks(assigned_to="user-123", column_id="col-todo")  # Your TODO items
   list_tasks(title="auth", assigned_to="your-id")          # Your auth tasks
   ```

What specific task management challenge are you facing? I can show you the exact filtering commands to use."""),
        base.UserMessage("I want to see all tasks assigned to me that are currently in progress."),
        base.AssistantMessage("""Perfect! Here's exactly what you need:

```
list_tasks(assigned_to="your-user-id", column_id="col-in-progress")
```

**To use this effectively:**

1. **First, get your user ID:**
   ```
   list_users()  # Find your user ID in the results
   ```

2. **Find the correct column ID:**
   ```
   list_boards()                      # Get available boards  
   list_columns(board_id="board-id")  # Get columns for specific board
   # Look for column with name like "In Progress", "Doing", "Active"
   ```

3. **Get your in-progress tasks:**
   ```
   list_tasks(assigned_to="your-actual-user-id", column_id="actual-column-id")
   ```

**Pro Tips:**
- If you have many tasks, add `limit=20` to see manageable chunks
- Use `title="keyword"` to further narrow down results
- Check different columns: "col-review", "col-testing", "col-blocked"

Would you like me to help you find your specific user ID and column IDs?"""),
        base.UserMessage("Yes, let's start by finding my user ID."),
        base.AssistantMessage("""Great! Let's find your user ID step by step:

**Step 1: Get all users**
```
list_users()
```

This will show all company users. Look for your entry and note the `id` field.

**Step 2: Once you have your ID, let's find the right column**

First, let's see what projects and boards you have access to:
```
list_projects()                    # See available projects
list_boards(project_id="proj-id")  # Get boards for relevant project
```

**Step 3: Find column IDs for the board**
```
list_columns(board_id="board-id")  # Get all columns for specific board
```

**Step 4: Get your filtered tasks**
```
list_tasks(assigned_to="your-id-from-step1", column_id="column-id-from-step3")
```

**Example workflow:**
```
# 1. Find yourself
users = list_users()
# Look for your name, copy the ID

# 2. Find your main project
projects = list_projects()
# Pick relevant project, copy project ID  

# 3. Get project boards
boards = list_boards(project_id="copied-project-id")
# Pick relevant board, copy board ID

# 4. Get board columns
board_columns = list_columns(board_id="copied-board-id")
# Look for "In Progress", "To Do", "Done" etc. in the results

# 5. Get your tasks
my_tasks = list_tasks(assigned_to="your-user-id", column_id="in-progress-column-id")
```

Ready to start? Run `list_users()` first and tell me what you find!""")
    ]


def board_organization_prompt() -> List[base.Message]:
    """
    Guide for organizing and finding boards efficiently.
    
    Returns:
        Conversation flow for board management
    """
    return [
        base.UserMessage("I have too many boards across multiple projects. How can I organize and find them better?"),
        base.AssistantMessage("""I'll help you master board organization with filtering! Here are the key strategies:

**1. Project-Based Organization**
```
list_boards(project_id="specific-project-id")
```
This is the most effective way to reduce clutter - see only boards from one project.

**2. Search by Naming Patterns**
```
list_boards(title="sprint")     # All sprint boards
list_boards(title="dev")        # Development boards  
list_boards(title="qa")         # QA/Testing boards
list_boards(title="2024")       # Year-specific boards
```

**3. Smart Pagination**
```
list_boards(limit=10)           # See 10 most recent boards
list_boards(limit=20, offset=20) # Next 20 boards
```

**4. Combined Filtering**
```
list_boards(project_id="proj-web", title="sprint")  # Sprint boards in web project
list_boards(project_id="proj-mobile", title="dev")  # Dev boards in mobile project
```

**Best Organization Practices:**

**Naming Conventions:**
- Use prefixes: "SPRINT-2024-Q1", "DEV-Frontend", "QA-Integration"
- Include dates: "Sprint-Dec-2024", "Release-v2.1"  
- Use project codes: "WEB-Sprint-01", "MOB-Testing"

**Project Structure:**
- Group related boards in same project
- Use separate projects for different products/teams
- Archive old boards instead of deleting

What's your current board naming pattern? I can suggest specific filtering strategies based on your setup."""),
        base.UserMessage("We use project codes like WEB, MOB, API, and then add sprint numbers like WEB-Sprint-15."),
        base.AssistantMessage("""Perfect naming convention! Here's how to use filtering effectively with your system:

**Find Boards by Project Code:**
```
list_boards(title="WEB")     # All web-related boards
list_boards(title="MOB")     # All mobile boards  
list_boards(title="API")     # All API boards
```

**Find Current/Recent Sprints:**
```
list_boards(title="Sprint-15")  # Current sprint across all projects
list_boards(title="Sprint-14")  # Previous sprint
list_boards(title="WEB-Sprint") # All web sprints
```

**Project-Specific Sprint Management:**
```
# Get specific project first
web_project = list_projects()  # Find WEB project ID

# Then filter boards within that project
list_boards(project_id="web-project-id", title="Sprint")  # All web sprints
list_boards(project_id="web-project-id", title="Sprint-15") # Current web sprint
```

**Advanced Filtering Strategies:**

**1. Current Sprint Dashboard:**
```python
# Get all current sprint boards
current_sprint_15 = list_boards(title="Sprint-15")
# Shows: WEB-Sprint-15, MOB-Sprint-15, API-Sprint-15
```

**2. Project Health Check:**
```python
# Check each project's boards
web_boards = list_boards(title="WEB")
mobile_boards = list_boards(title="MOB") 
api_boards = list_boards(title="API")
```

**3. Sprint Comparison:**
```python
# Compare sprints
sprint_14 = list_boards(title="Sprint-14")
sprint_15 = list_boards(title="Sprint-15")
# See which projects are on which sprint
```

**Pro Tips for Your Setup:**
- Use `limit=5` to see just recent boards per project
- Search for partial numbers: `title="1"` finds Sprint-10, Sprint-11, etc.
- Combine with project filtering for precise results

Which project are you working on most? I can show you specific commands for that project.""")
    ]