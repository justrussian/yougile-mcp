# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Model Context Protocol (MCP) server implementation for the YouGile REST API v2.0. The project exposes YouGile's project management functionality through MCP, allowing AI assistants to interact with YouGile's API for managing companies, projects, boards, tasks, and users.

## Core Architecture

### Modular Design Principles

This project follows a **strict modular architecture** with these key principles:

- **Small Files**: Each module file should be under 200 lines of code
- **Single Responsibility**: Each module handles one specific API category or concern
- **Clear Separation**: Business logic, API clients, and MCP handlers are separated
- **Easy Testing**: Each module can be tested independently
- **Maintainable**: New functionality can be added without modifying existing modules

### Project Structure

```
src/
├── __init__.py                 # Package initialization
├── server.py                   # Main MCP server entry point (< 100 lines)
├── config/
│   ├── __init__.py
│   └── settings.py             # Configuration management
├── core/
│   ├── __init__.py
│   ├── auth.py                 # Authentication utilities
│   ├── client.py               # HTTP client wrapper
│   ├── exceptions.py           # Custom exceptions
│   └── models.py               # Pydantic models for structured output
├── api/
│   ├── __init__.py
│   ├── auth.py                 # Authorization endpoints (4)
│   ├── company.py              # Company management (2)
│   ├── departments.py          # Department operations (4)
│   ├── users.py                # User management (5)
│   ├── projects.py             # Project operations (4)
│   ├── project_roles.py        # Project role management (5)
│   ├── boards.py               # Board management (4)
│   ├── columns.py              # Column operations (4)
│   ├── tasks.py                # Task operations (7)
│   ├── stickers.py             # String/Sprint stickers (8+6)
│   ├── chats.py                # Group chats and messages (8)
│   ├── files.py                # File operations (1)
│   └── webhooks.py             # Event subscriptions (3)
├── mcp/
│   ├── __init__.py
│   ├── tools/                  # MCP tool implementations
│   │   ├── __init__.py
│   │   ├── auth_tools.py       # Authentication and setup
│   │   ├── company_tools.py    # Company management
│   │   ├── user_tools.py       # User and department management
│   │   ├── project_tools.py    # Projects and roles
│   │   ├── board_tools.py      # Boards and columns
│   │   ├── task_tools.py       # Task management
│   │   ├── sticker_tools.py    # Custom field stickers
│   │   ├── chat_tools.py       # Communication features
│   │   ├── file_tools.py       # File operations
│   │   └── webhook_tools.py    # Event subscriptions
│   ├── resources/              # MCP resource implementations
│   │   ├── __init__.py
│   │   └── api_docs.py
│   └── prompts/                # MCP prompt implementations
│       ├── __init__.py
│       ├── project_prompts.py
│       └── workflow_prompts.py
└── utils/
    ├── __init__.py
    ├── validation.py           # Input validation helpers
    └── formatting.py           # Response formatting utilities
```

### Complete API Categories (17 categories, 65 endpoints)

**Core Project Management:**
- **Авторизация (Authorization)**: Authentication, API keys, company access (4 endpoints)
- **Компания (Company)**: Company details and settings (2 endpoints)
- **Отделы (Departments)**: Department hierarchy and management (4 endpoints)
- **Сотрудники (Users)**: User management and invitations (5 endpoints)
- **Проекты (Projects)**: Project creation and management (4 endpoints)
- **Роли проекта (Project Roles)**: Custom project roles and permissions (5 endpoints)
- **Доски (Boards)**: Kanban boards and workflows (4 endpoints)
- **Колонки (Columns)**: Board columns and statuses (4 endpoints)
- **Задачи (Tasks)**: Task operations and lifecycle (7 endpoints)

**Advanced Features:**
- **Стикер с набором состояний (String Stickers)**: Custom field stickers with states (4 endpoints)
- **Состояния стикера с набором состояний (String Sticker States)**: Sticker state management (3 endpoints)
- **Стикер спринта (Sprint Stickers)**: Sprint-specific stickers (4 endpoints)
- **Состояния стикера спринта (Sprint Sticker States)**: Sprint sticker states (3 endpoints)
- **Групповые чаты (Group Chats)**: Team communication (4 endpoints)
- **Сообщения чатов (Chat Messages)**: Message management (4 endpoints)
- **Файлы (Files)**: File upload and management (1 endpoint)
- **Подписки на события (Webhooks)**: Event subscriptions and notifications (3 endpoints)

## Key API Concepts

The YouGile API follows these patterns:
- **Authentication**: Bearer token authentication using API keys
- **Rate Limiting**: Maximum 50 requests per minute per company
- **CRUD Operations**: Standard REST operations across all resources
- **Hierarchical Structure**: Companies → Projects → Boards → Tasks
- **Permissions**: API respects user permissions from the YouGile interface

## Development Commands

Based on the MCP Python SDK (as documented in mcp-docs.md):

### Server Development
```bash
# Run server in development mode with MCP Inspector
uv run mcp dev src/server.py

# Add dependencies during development
uv run mcp dev src/server.py --with httpx --with pydantic

# Mount local code for development
uv run mcp dev src/server.py --with-editable .
```

### Installation and Deployment
```bash
# Install server in Claude Desktop
uv run mcp install src/server.py

# Install with custom name
uv run mcp install src/server.py --name "YouGile MCP Server"

# Install with environment variables
uv run mcp install src/server.py -v YOUGILE_API_KEY=your_key -v YOUGILE_BASE_URL=https://yougile.com
uv run mcp install src/server.py -f .env
```

### Direct Execution
```bash
# Run server directly
python src/server.py

# Or using uv
uv run mcp run src/server.py
```

## Implementation Guidelines

### Authentication Flow
1. First obtain company ID using `/api-v2/auth/companies` with login/password
2. Generate API key using `/api-v2/auth/keys` with company ID
3. Use Bearer token authentication for all subsequent requests

### Error Handling
- Success: Status codes 200 or 201
- Errors: Status codes 4xx/5xx with `error` field in response
- Rate limiting: HTTP 429 responses

### Data Models
The API uses consistent patterns across resources:
- All objects have `id`, `timestamp`, `deleted` fields
- Title/name fields for human-readable names
- Parent-child relationships (e.g., projects contain boards, boards contain tasks)

### Module Organization Rules

**File Size Limits:**
- Main server file: < 100 lines (imports and registration only)
- API modules: < 200 lines each
- MCP tool modules: < 150 lines each
- Utility modules: < 100 lines each

**Separation of Concerns:**
- `api/` modules: Pure HTTP API clients, no MCP logic
- `mcp/tools/` modules: MCP tool handlers, call API modules
- `mcp/resources/` modules: Static resources and documentation
- `mcp/prompts/` modules: Workflow templates and guides
- `core/` modules: Shared utilities (auth, HTTP client, exceptions)
- `utils/` modules: Pure functions for validation and formatting

**Import Rules:**
- MCP modules can import from `api/`, `core/`, and `utils/`
- API modules can only import from `core/` and `utils/`
- Core modules should have minimal dependencies
- No circular imports allowed

**MCP Protocol Compliance:**
- **Tools**: Use `@mcp.tool()` with `Context` parameter for progress/logging
  - All tools must be async: `async def tool_name(param: str, ctx: Context)`
  - Use `await ctx.info()`, `await ctx.error()`, `await ctx.debug()` for logging
  - Use `await ctx.report_progress()` for long-running operations
  - Return structured Pydantic models for type safety
- **Resources**: Use URI schemes like `yougile://projects/{id}`
  - Follow pattern: `@mcp.resource("yougile://entity/{param}")`
  - Return documentation, schemas, examples as strings
  - Use consistent URI namespace: `yougile://api/`, `yougile://projects/`, etc.
- **Prompts**: Use `@mcp.prompt()` for workflow templates
  - Return conversation flows as `List[base.Message]` or simple strings
  - Include `title` parameter for user-friendly naming
  - Provide step-by-step guidance for complex workflows
- **Structured Output**: Return Pydantic models for typed responses
  - All models in `src/core/models.py` inherit from `YouGileBaseModel`
  - Use proper Field descriptions for MCP schema generation
  - Include realistic examples in model configs
- **Error Handling**: Comprehensive async error handling
  - Use custom exceptions from `src/core/exceptions.py`
  - Always log errors to Context before re-raising
  - Provide user-friendly error messages

**Naming Conventions:**
- API functions: `get_companies()`, `create_project()`, etc.
- MCP tools: `@mcp.tool() async def tool_name(param: str, ctx: Context) -> Model`
- MCP resources: `@mcp.resource("yougile://entity/{id}")`
- MCP prompts: `@mcp.prompt(title="Task Name")`
- Internal helpers: `_validate_input()`, `_format_response()`

## Common Operations & Examples

### **Authentication Workflow**
```python
# 1. Get available companies for user
companies = await get_companies("user@example.com", "password", ctx)
# Returns: List[Company] with structured output

# 2. Create API key for selected company  
api_key = await create_api_key("user@example.com", "password", company_id, ctx)
# Returns: ApiKey model with key value

# 3. Configure client for subsequent requests
auth_manager.set_credentials(api_key.key, company_id)
```

### **Project Management Workflow**
```python
# 1. List all projects
projects = await list_projects(ctx)  # Returns List[Project]

# 2. Create new project
project = await create_project(
    title="Website Redesign",
    description="Complete website overhaul",
    users={"user-1": "admin", "user-2": "developer"},
    ctx=ctx
)  # Returns Project model

# 3. Set up boards and workflow
board = await create_board(
    title="Development Board", 
    project_id=project.id,
    ctx=ctx
)  # Returns Board model
```

### **Resource Access Examples**
```python
# Get comprehensive API documentation
api_docs = read_resource("yougile://api/overview")

# Get project-specific information
project_info = read_resource(f"yougile://projects/{project_id}")

# Get task schema and examples
task_schema = read_resource(f"yougile://tasks/{task_id}")
```

### **Workflow Prompt Examples**
```python
# Get step-by-step project setup
setup_flow = get_prompt("Setup New Project", {
    "project_name": "Mobile App",
    "project_type": "scrum"
})

# Get task creation template
task_template = get_prompt("Create Task", {
    "task_title": "Implement user authentication",
    "priority": "high"
})
```

### **Error Handling Pattern**
```python
async def example_tool(param: str, ctx: Context) -> Model:
    try:
        await ctx.info(f"Starting operation: {param}")
        
        # Validate input
        validated_param = validate_non_empty_string(param, "param")
        
        # Make API call
        async with YouGileClient(auth_manager) as client:
            result = await api_call(client, validated_param)
            
        # Convert to structured output
        model = ResultModel(**result)
        
        await ctx.info("✅ Operation completed successfully")
        return model
        
    except ValidationError as e:
        await ctx.error(f"Validation failed: {e.message}")
        raise
    except YouGileError as e:
        await ctx.error(f"API error: {e.message}")
        raise
    except Exception as e:
        await ctx.error(f"Unexpected error: {str(e)}")
        raise
```

### **Progress Reporting for Long Operations**
```python
async def bulk_operation(items: List[str], ctx: Context) -> List[Model]:
    results = []
    total = len(items)
    
    await ctx.info(f"Processing {total} items...")
    
    for i, item in enumerate(items):
        # Report progress
        progress = (i + 1) / total
        await ctx.report_progress(
            progress=progress,
            total=1.0,
            message=f"Processing item {i + 1}/{total}: {item}"
        )
        
        # Process item
        result = await process_item(item)
        results.append(result)
        
        await ctx.debug(f"Completed item {i + 1}: {item}")
    
    await ctx.info(f"✅ Successfully processed all {total} items")
    return results
```