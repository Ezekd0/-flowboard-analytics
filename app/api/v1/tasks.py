from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Annotated, List, Optional
from sqlalchemy.orm import Session

from app.schemas.task import TaskCreate, TaskUpdate, TaskInDB
from app.services.task_service import TaskService
from app.core.security import get_current_user
from app.models.user import User
from app.core.database import get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskInDB, status_code=201)
def create_task(
    task_data: TaskCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """Create a new task"""
    service = TaskService(db)
    return service.create_task(task_data, current_user.id)

@router.get("/", response_model=List[TaskInDB])
def get_tasks(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status: Optional[str] = None,
    priority: Optional[str] = None
):
    """Get user's tasks with pagination and filters"""
    service = TaskService(db)
    return service.get_user_tasks(
        current_user.id,
        skip=skip,
        limit=limit,
        status=status,
        priority=priority
    )

@router.get("/{task_id}", response_model=TaskInDB)
def get_task(
    task_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """Get single task by ID"""
    service = TaskService(db)
    task = service.get_task(task_id, current_user.id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task

@router.put("/{task_id}", response_model=TaskInDB)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """Update existing task"""
    service = TaskService(db)
    task = service.update_task(task_id, task_data, current_user.id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task

@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """Delete task"""
    service = TaskService(db)
    deleted = service.delete_task(task_id, current_user.id)
    
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return None
