"""
MCP resources for YouGile API documentation and schemas.
Provides access to API documentation, schemas, and examples.
"""

from typing import Dict, Any
import json
from pathlib import Path


def get_api_overview() -> str:
    """
    Get YouGile API overview documentation.
    
    Returns comprehensive overview of YouGile REST API v2.0.
    """
    return """
# YouGile REST API v2.0 Overview

YouGile provides a comprehensive REST API for project management and team collaboration.

## Authentication
- Use Bearer token authentication with API keys
- Rate limit: 50 requests per minute per company
- Base URL: https://yougile.com/api-v2/

## Core Entities
- **Companies**: Organizations and settings
- **Users**: Team members and roles  
- **Projects**: Project containers
- **Boards**: Kanban boards within projects
- **Tasks**: Work items with assignments and deadlines
- **Stickers**: Custom fields for tasks and sprints
- **Chats**: Team communication
- **Webhooks**: Event notifications

## API Categories (17 total, 65 endpoints)
1. Authorization (4 endpoints) - Authentication and API keys
2. Company (2 endpoints) - Company management
3. Users (5 endpoints) - User management
4. Projects (4 endpoints) - Project operations
5. Boards (4 endpoints) - Board management
6. Tasks (7 endpoints) - Task lifecycle
7. And 11 more specialized categories...

## Getting Started
1. Get company ID with your login/password
2. Create API key for the company
3. Use API key in Authorization header for all requests
4. Start managing your projects programmatically!
"""


def get_project_info(project_id: str) -> str:
    """
    Get project information resource.
    
    Args:
        project_id: Project identifier
        
    Returns:
        Project documentation and schema information
    """
    return f"""
# Project Information: {project_id}

## Project Schema
```json
{{
  "id": "string (UUID)",
  "title": "string",
  "description": "string (optional)",
  "users": {{
    "user_id": "role (admin|developer|viewer)"
  }},
  "timestamp": "datetime",
  "deleted": "boolean"
}}
```

## Available Operations
- GET /api-v2/projects - List all projects
- POST /api-v2/projects - Create new project
- GET /api-v2/projects/{project_id} - Get specific project
- PUT /api-v2/projects/{project_id} - Update project

## Example Usage
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \\
     -H "Content-Type: application/json" \\
     https://yougile.com/api-v2/projects/{project_id}
```

## Related Resources
- yougile://boards?project_id={project_id} - Project boards
- yougile://users?project_id={project_id} - Project members
- yougile://roles/{project_id} - Project roles
"""


def get_task_info(task_id: str) -> str:
    """
    Get task information resource.
    
    Args:
        task_id: Task identifier
        
    Returns:
        Task documentation and schema information
    """
    return f"""
# Task Information: {task_id}

## Task Schema
```json
{{
  "id": "string (UUID)",
  "title": "string",
  "description": "string (optional)",
  "column_id": "string (UUID)",
  "assigned_users": [
    {{
      "id": "string",
      "name": "string",
      "email": "string"
    }}
  ],
  "deadline": {{
    "date": "string (YYYY-MM-DD)",
    "is_expired": "boolean"
  }},
  "checklists": [
    {{
      "title": "string",
      "items": [
        {{
          "title": "string",
          "is_completed": "boolean"
        }}
      ]
    }}
  ],
  "timestamp": "datetime",
  "deleted": "boolean"
}}
```

## Available Operations
- GET /api-v2/tasks - List tasks (newest first)
- GET /api-v2/task-list - List tasks (standard order)
- POST /api-v2/tasks - Create new task
- GET /api-v2/tasks/{task_id} - Get specific task
- PUT /api-v2/tasks/{task_id} - Update task
- GET /api-v2/tasks/{task_id}/chat-subscribers - Get task chat participants
- PUT /api-v2/tasks/{task_id}/chat-subscribers - Update chat participants

## Example Usage
```bash
# Get task details
curl -H "Authorization: Bearer YOUR_API_KEY" \\
     https://yougile.com/api-v2/tasks/{task_id}

# Update task
curl -X PUT \\
     -H "Authorization: Bearer YOUR_API_KEY" \\
     -H "Content-Type: application/json" \\
     -d '{{"title": "Updated Task Title"}}' \\
     https://yougile.com/api-v2/tasks/{task_id}
```
"""


def get_api_endpoints() -> str:
    """
    Get complete list of API endpoints.
    
    Returns:
        Comprehensive list of all 65 YouGile API endpoints organized by category
    """
    return """
# YouGile API v2.0 Complete Endpoints Reference

## Authorization (4 endpoints)
- POST /api-v2/auth/companies - Get list of companies
- POST /api-v2/auth/keys/get - Get list of API keys  
- POST /api-v2/auth/keys - Create API key
- DELETE /api-v2/auth/keys/{key} - Delete API key

## Company (2 endpoints)
- GET /api-v2/companies - Get company details
- PUT /api-v2/companies - Update company

## Users (5 endpoints)
- GET /api-v2/users - Get list of users
- POST /api-v2/users - Invite user to company
- GET /api-v2/users/{id} - Get user by ID
- PUT /api-v2/users/{id} - Update user
- DELETE /api-v2/users/{id} - Remove user from company

## Projects (4 endpoints)
- GET /api-v2/projects - Get list of projects
- POST /api-v2/projects - Create project
- GET /api-v2/projects/{id} - Get project by ID
- PUT /api-v2/projects/{id} - Update project

## Project Roles (5 endpoints)
- GET /api-v2/projects/{projectId}/roles - Get project roles
- POST /api-v2/projects/{projectId}/roles - Create project role
- GET /api-v2/projects/{projectId}/roles/{id} - Get role by ID
- PUT /api-v2/projects/{projectId}/roles/{id} - Update role
- DELETE /api-v2/projects/{projectId}/roles/{id} - Delete role

## Departments (4 endpoints)
- GET /api-v2/departments - Get list of departments
- POST /api-v2/departments - Create department
- GET /api-v2/departments/{id} - Get department by ID
- PUT /api-v2/departments/{id} - Update department

## Boards (4 endpoints)
- GET /api-v2/boards - Get list of boards
- POST /api-v2/boards - Create board
- GET /api-v2/boards/{id} - Get board by ID
- PUT /api-v2/boards/{id} - Update board

## Columns (4 endpoints)
- GET /api-v2/columns - Get list of columns
- POST /api-v2/columns - Create column
- GET /api-v2/columns/{id} - Get column by ID
- PUT /api-v2/columns/{id} - Update column

## Tasks (7 endpoints)
- GET /api-v2/task-list - Get task list (standard order)
- GET /api-v2/tasks - Get tasks (newest first)
- POST /api-v2/tasks - Create task
- GET /api-v2/tasks/{id} - Get task by ID
- PUT /api-v2/tasks/{id} - Update task
- GET /api-v2/tasks/{id}/chat-subscribers - Get task chat participants
- PUT /api-v2/tasks/{id}/chat-subscribers - Update chat participants

## String Stickers (4 endpoints)
- GET /api-v2/string-stickers - Get string stickers
- POST /api-v2/string-stickers - Create string sticker
- GET /api-v2/string-stickers/{id} - Get sticker by ID
- PUT /api-v2/string-stickers/{id} - Update sticker

## String Sticker States (3 endpoints)
- GET /api-v2/string-stickers/{stickerId}/states/{stateId} - Get state
- PUT /api-v2/string-stickers/{stickerId}/states/{stateId} - Update state
- POST /api-v2/string-stickers/{stickerId}/states - Create state

## Sprint Stickers (4 endpoints)
- GET /api-v2/sprint-stickers - Get sprint stickers
- POST /api-v2/sprint-stickers - Create sprint sticker
- GET /api-v2/sprint-stickers/{id} - Get sticker by ID
- PUT /api-v2/sprint-stickers/{id} - Update sticker

## Sprint Sticker States (3 endpoints)
- GET /api-v2/sprint-stickers/{stickerId}/states/{stateId} - Get state
- PUT /api-v2/sprint-stickers/{stickerId}/states/{stateId} - Update state
- POST /api-v2/sprint-stickers/{stickerId}/states - Create state

## Group Chats (4 endpoints)
- GET /api-v2/group-chats - Get list of chats
- POST /api-v2/group-chats - Create chat
- GET /api-v2/group-chats/{id} - Get chat by ID
- PUT /api-v2/group-chats/{id} - Update chat

## Chat Messages (4 endpoints)
- GET /api-v2/chats/{chatId}/messages - Get message history
- POST /api-v2/chats/{chatId}/messages - Send message
- GET /api-v2/chats/{chatId}/messages/{id} - Get message by ID
- PUT /api-v2/chats/{chatId}/messages/{id} - Update message

## Files (1 endpoint)
- POST /api-v2/upload-file - Upload file

## Webhooks (3 endpoints)
- POST /api-v2/webhooks - Create webhook subscription
- GET /api-v2/webhooks - Get webhook subscriptions
- PUT /api-v2/webhooks/{id} - Update webhook subscription

---
**Total: 65 endpoints across 17 categories**
"""