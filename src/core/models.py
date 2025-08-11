"""
Pydantic models for structured output in MCP tools.
Provides type-safe data structures for YouGile API responses.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


# Base models
class YouGileBaseModel(BaseModel):
    """Base model for all YouGile entities."""
    id: str = Field(description="Unique identifier")
    timestamp: Optional[datetime] = Field(None, description="Creation/modification timestamp")
    deleted: bool = Field(False, description="Whether the entity is deleted")


class PaginatedResponse(BaseModel):
    """Paginated response wrapper."""
    data: List[Dict[str, Any]] = Field(description="List of entities")
    total: Optional[int] = Field(None, description="Total number of entities")
    limit: Optional[int] = Field(None, description="Page size limit")
    offset: Optional[int] = Field(None, description="Page offset")


# Company models
class Company(YouGileBaseModel):
    """Company entity model."""
    title: str = Field(description="Company name")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "44eccf40-a027-4d06-b5c2-18f4c02bb026",
                "title": "ГосУслуги",
                "timestamp": "2024-01-01T00:00:00Z",
                "deleted": False
            }
        }


# User models
class User(YouGileBaseModel):
    """User entity model."""
    name: Optional[str] = Field(None, description="Display name")
    real_name: Optional[str] = Field(None, alias="realName", description="Real name (Full name)")
    email: Optional[str] = Field(None, description="Email address")
    role: Optional[str] = Field(None, description="User role")
    is_admin: Optional[bool] = Field(None, alias="isAdmin", description="Admin privileges")
    status: Optional[str] = Field(None, description="Online/offline status")
    last_activity: Optional[int] = Field(None, alias="lastActivity", description="Last activity timestamp")
    
    class Config:
        populate_by_name = True  # Allow both field name and alias
        json_schema_extra = {
            "example": {
                "id": "80eed1bd-eda3-4991-ac17-09d28566749d",
                "name": "john_doe",
                "realName": "John Doe",
                "email": "john@example.com",
                "role": "admin",
                "isAdmin": False,
                "status": "online"
            }
        }


# Project models
class Project(YouGileBaseModel):
    """Project entity model."""
    title: str = Field(description="Project name")
    description: Optional[str] = Field(None, description="Project description")
    users: Optional[Dict[str, str]] = Field(None, description="Project users and their roles")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "proj-123",
                "title": "Website Redesign",
                "description": "Complete redesign of company website",
                "users": {"user-1": "admin", "user-2": "developer"}
            }
        }


# Department models
class Department(YouGileBaseModel):
    """Department entity model."""
    title: str = Field(description="Department name")
    parent_id: Optional[str] = Field(None, description="Parent department ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "dept-123",
                "title": "Отдел разработки", 
                "parent_id": "dept-parent-456"
            }
        }


# Board models  
class Board(YouGileBaseModel):
    """Board entity model."""
    title: str = Field(description="Board name")
    project_id: str = Field(alias="projectId", description="Parent project ID")
    stickers: Optional[Dict[str, Any]] = Field(None, description="Board sticker configuration")
    
    class Config:
        populate_by_name = True  # Allow both field name and alias
        json_schema_extra = {
            "example": {
                "id": "board-123",
                "title": "Тестирование",
                "projectId": "proj-123",
                "stickers": {
                    "deadline": True,
                    "timeTracking": True,
                    "assignee": True
                }
            }
        }


# Column models
class Column(YouGileBaseModel):
    """Column entity model."""
    title: str = Field(description="Column name")
    color: Optional[str] = Field(None, description="Column color")
    board_id: str = Field(description="Parent board ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "col-123",
                "title": "To Do",
                "color": "#blue",
                "board_id": "board-123"
            }
        }


# Task models
class TaskDeadline(BaseModel):
    """Task deadline information."""
    deadline: Optional[int] = Field(None, description="Deadline timestamp")
    start_date: Optional[int] = Field(None, alias="startDate", description="Start date timestamp")
    with_time: bool = Field(False, alias="withTime", description="Whether time is included")
    deleted: bool = Field(False, description="Whether deadline is deleted")
    
    class Config:
        populate_by_name = True


class TaskTimeTracking(BaseModel):
    """Task time tracking information."""
    plan: Optional[int] = Field(None, description="Planned time in hours")
    work: Optional[int] = Field(None, description="Actual work time in hours")
    deleted: bool = Field(False, description="Whether time tracking is deleted")


class TaskStopwatch(BaseModel):
    """Task stopwatch information."""
    running: bool = Field(False, description="Whether stopwatch is running")
    seconds: Optional[int] = Field(None, description="Elapsed seconds")
    deleted: bool = Field(False, description="Whether stopwatch is deleted")


class TaskChecklist(BaseModel):
    """Task checklist item."""
    title: str = Field(description="Checklist item title")
    is_completed: bool = Field(False, description="Whether item is completed")


class TaskChecklistGroup(BaseModel):
    """Task checklist group."""
    title: str = Field(description="Checklist group title")
    items: List[TaskChecklist] = Field(description="Checklist items")


class Task(YouGileBaseModel):
    """Task entity model."""
    title: str = Field(description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    column_id: Optional[str] = Field(None, alias="columnId", description="Column ID where task is located")
    assigned_users: Optional[List[str]] = Field(None, alias="assigned", description="Assigned user IDs")
    deadline: Optional[TaskDeadline] = Field(None, description="Task deadline sticker")
    time_tracking: Optional[TaskTimeTracking] = Field(None, alias="timeTracking", description="Time tracking sticker")
    stopwatch: Optional[TaskStopwatch] = Field(None, description="Stopwatch sticker")
    checklists: Optional[List[TaskChecklistGroup]] = Field(None, description="Task checklists")
    stickers: Optional[Dict[str, str]] = Field(None, description="Custom stickers (sticker_id -> state_id)")
    completed: Optional[bool] = Field(None, description="Whether task is completed")
    archived: Optional[bool] = Field(None, description="Whether task is archived")
    
    class Config:
        populate_by_name = True  # Allow both field name and alias
        json_schema_extra = {
            "example": {
                "id": "task-123",
                "title": "Fix login bug",
                "description": "Users cannot login with social auth",
                "columnId": "col-123",
                "deadline": {"deadline": 1653029146646, "withTime": True},
                "timeTracking": {"plan": 5, "work": 3},
                "stickers": {"sticker-1-id": "state-1-id"}
            }
        }


# Sticker models
class StringSticker(YouGileBaseModel):
    """String sticker (custom field) model."""
    title: str = Field(description="Sticker name")
    type: str = Field(description="Sticker type")
    
    
class SprintSticker(YouGileBaseModel):
    """Sprint sticker model."""
    title: str = Field(description="Sprint sticker name")
    type: str = Field(description="Sticker type")


# Chat models
class GroupChat(YouGileBaseModel):
    """Group chat model."""
    title: str = Field(description="Chat title")
    participants: Optional[List[str]] = Field(None, description="Chat participant IDs")


class ChatMessage(BaseModel):
    """Chat message model."""
    id: str = Field(description="Message ID")
    text: str = Field(description="Message text")
    author_id: str = Field(description="Author user ID")
    timestamp: datetime = Field(description="Message timestamp")


# API Key models
class ApiKey(BaseModel):
    """API key model."""
    key: str = Field(description="API key value")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    company_id: str = Field(description="Associated company ID")


# Webhook models
class Webhook(YouGileBaseModel):
    """Webhook subscription model."""
    url: str = Field(description="Webhook URL")
    events: List[str] = Field(description="Subscribed event types")
    active: bool = Field(True, description="Whether webhook is active")


# Creation response models
class CreatedEntity(BaseModel):
    """Response model for entity creation matching WithIdDto schema."""
    id: str = Field(description="ID of created entity")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "086866d2-a230-4a4a-8225-e3a9d847b6d0"
            }
        }


# Success response models
class SuccessResponse(BaseModel):
    """Generic success response."""
    success: bool = Field(True, description="Operation success status")
    message: str = Field(description="Success message")
    data: Optional[Dict[str, Any]] = Field(None, description="Optional response data")


class ErrorResponse(BaseModel):
    """Generic error response."""
    success: bool = Field(False, description="Operation success status")
    error: str = Field(description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")