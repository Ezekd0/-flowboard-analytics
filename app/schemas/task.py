from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List
from enum import Enum

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    COMPLETED = "completed"
    ARCHIVED = "archived"

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=5000)
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None
    estimated_hours: int = Field(0, ge=0, le=1000)
    tags: Optional[List[str]] = []

    @validator("due_date")
    def validate_due_date(cls, v):
        if v and v < datetime.now():
            raise ValueError("Due date cannot be in the past")
        return v

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    estimated_hours: Optional[int] = Field(None, ge=0, le=1000)
    actual_hours: Optional[int] = Field(None, ge=0)
    tags: Optional[List[str]] = None

class TaskResponse(TaskBase):
    id: int
    owner_id: int
    assigned_to_id: Optional[int]
    actual_hours: int = 0
    created_at: datetime
    updated_at: Optional[datetime]
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True

TaskInDB = TaskResponse
