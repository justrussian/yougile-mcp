"""YouGile API client modules."""

# Import all API modules for easy access
from . import (
    auth,
    company,
    departments,
    users,
    projects,
    project_roles,
    boards,
    columns,
    tasks,
    stickers,
    chats,
    files,
    webhooks,
)

__all__ = [
    "auth",
    "company", 
    "departments",
    "users",
    "projects",
    "project_roles",
    "boards",
    "columns", 
    "tasks",
    "stickers",
    "chats",
    "files",
    "webhooks",
]