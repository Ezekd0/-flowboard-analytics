from sqlalchemy.orm import Session
from datetime import datetime
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate

class TaskService:
    def __init__(self, db: Session):
        self.db = db

    def create_task(self, task: TaskCreate, user_id: int):
        db_task = Task(
            title=task.title,
            description=task.description,
            priority=task.priority,
            due_date=task.due_date,
            owner_id=user_id
        )
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def get_user_tasks(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        status: str | None = None,
        priority: str | None = None,
    ):
        query = self.db.query(Task).filter(Task.owner_id == user_id)
        if status:
            query = query.filter(Task.status == status)
        if priority:
            query = query.filter(Task.priority == priority)
        return query.offset(skip).limit(limit).all()

    def get_task(self, task_id: int, user_id: int):
        return (
            self.db.query(Task)
            .filter(Task.id == task_id, Task.owner_id == user_id)
            .first()
        )

    def update_task(self, task_id: int, task: TaskUpdate, user_id: int):
        db_task = self.get_task(task_id, user_id)
        if db_task:
            update_data = task.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_task, field, value)
            if update_data.get("status") == "completed" and not db_task.completed_at:
                db_task.completed_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(db_task)
        return db_task

    def delete_task(self, task_id: int, user_id: int):
        db_task = self.get_task(task_id, user_id)
        if db_task:
            self.db.delete(db_task)
            self.db.commit()
            return True
        return False
