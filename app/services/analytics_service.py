from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List

from app.models.task import Task, TaskStatus, TaskPriority
from app.models.user import User
from app.schemas.analytics import (
    TaskStatistics,
    ProductivityMetrics,
    UserPerformance,
    Forecast,
)

class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db
        
    def get_summary(self, user_id: int):
        tasks = self.db.query(Task).filter(Task.owner_id == user_id).all()
        total_tasks = len(tasks)
        completed_tasks = len([t for t in tasks if t.status == TaskStatus.COMPLETED])
        pending_tasks = len([t for t in tasks if t.status == TaskStatus.PENDING])
        in_progress_tasks = len([t for t in tasks if t.status == TaskStatus.IN_PROGRESS])

        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "in_progress_tasks": in_progress_tasks
        }

    def get_task_analytics(self, user_id: int):
        tasks = self.db.query(Task).filter(Task.owner_id == user_id).all()
        by_priority = {}
        for task in tasks:
            priority = task.priority.value if isinstance(task.priority, TaskPriority) else task.priority
            by_priority[priority] = by_priority.get(priority, 0) + 1
        return by_priority

    def get_metrics(self, user_id: int):
        tasks = self.db.query(Task).filter(Task.owner_id == user_id).all()
        total = len(tasks)
        completed = len([t for t in tasks if t.status == TaskStatus.COMPLETED])
        completion_rate = (completed / total * 100) if total > 0 else 0

        return {
            "total_tasks": total,
            "completed_tasks": completed,
            "completion_rate": completion_rate
        }

    def get_task_statistics(self, user_id: int = None) -> TaskStatistics:
        import numpy as np
        import pandas as pd

        query = self.db.query(Task)
        if user_id:
            query = query.filter(Task.owner_id == user_id)
            
        tasks = query.all()
        if not tasks:
            return TaskStatistics()

        df = pd.DataFrame([{
            "status": t.status.value if isinstance(t.status, TaskStatus) else t.status,
            "priority": t.priority.value if isinstance(t.priority, TaskPriority) else t.priority,
            "created_at": t.created_at,
            "completed_at": t.completed_at,
            "estimated_hours": t.estimated_hours,
            "actual_hours": t.actual_hours
        } for t in tasks])

        status_counts = df["status"].value_counts().to_dict()
        priority_counts = df["priority"].value_counts().to_dict()

        completed_tasks = df[df["status"] == TaskStatus.COMPLETED.value]
        completion_rate = len(completed_tasks) / len(df) if len(df) > 0 else 0

        avg_completion_time = None
        if len(completed_tasks) > 0:
            completed_tasks["completion_time"] = (
                completed_tasks["completed_at"] - completed_tasks["created_at"]
            ).dt.total_seconds() / 3600
            avg_completion_time = completed_tasks["completion_time"].mean()

        df["accuracy"] = np.where(
            df["estimated_hours"] > 0,
            (df["actual_hours"] - df["estimated_hours"]) / df["estimated_hours"] * 100,
            0
        )
        avg_accuracy = df["accuracy"].mean()

        return TaskStatistics(
            total_tasks=len(tasks),
            completed_tasks=len(completed_tasks),
            pending_tasks=len(df[df["status"] == TaskStatus.PENDING.value]),
            in_progress_tasks=len(df[df["status"] == TaskStatus.IN_PROGRESS.value]),
            completion_rate=completion_rate,
            avg_completion_time_hours=avg_completion_time,
            avg_estimation_accuracy_percent=avg_accuracy,
            status_distribution=status_counts,
            priority_distribution=priority_counts,
        )

    def get_productivity_metrics(self, user_id: int = None, days: int = 30) -> ProductivityMetrics:
        import pandas as pd

        start_date = datetime.now() - timedelta(days=days)
        query = self.db.query(Task).filter(Task.created_at >= start_date)
        if user_id:
            query = query.filter(Task.owner_id == user_id)
        tasks = query.all()
        if not tasks:
            return ProductivityMetrics()

        df = pd.DataFrame([{
            "date": t.created_at.date(),
            "completed": 1 if t.status == TaskStatus.COMPLETED else 0,
            "hours": t.actual_hours,
            "priority_weight": {
                TaskPriority.LOW: 1,
                TaskPriority.MEDIUM: 2,
                TaskPriority.HIGH: 3,
                TaskPriority.URGENT: 4,
            }[t.priority]
        } for t in tasks])

        daily_metrics = df.groupby("date").agg({
            "completed": "sum",
            "hours": "sum",
            "priority_weight": "sum"
        }).reset_index()

        daily_metrics["completion_ma7"] = daily_metrics["completed"].rolling(window=7, min_periods=1).mean()
        daily_metrics["hours_ma7"] = daily_metrics["hours"].rolling(window=7, min_periods=1).mean()
        daily_metrics["productivity_score"] = (
            daily_metrics["completed"] * daily_metrics["priority_weight"]
        ) / (daily_metrics["hours"] + 1)

        df["week"] = pd.to_datetime(df["date"]).dt.isocalendar().week
        weekly_metrics = df.groupby("week").agg({
            "completed": "sum",
            "hours": "sum",
            "priority_weight": "sum"
        }).reset_index()

        return ProductivityMetrics(
            daily_metrics=daily_metrics.to_dict("records"),
            weekly_metrics=weekly_metrics.to_dict("records"),
            avg_daily_completion=daily_metrics["completed"].mean(),
            total_hours=df["hours"].sum(),
            productivity_trend=list(daily_metrics["productivity_score"].values),
        )

    def get_user_performance_ranking(self) -> List[UserPerformance]:
        users = self.db.query(User).all()
        rankings: List[UserPerformance] = []
        for user in users:
            tasks = self.db.query(Task).filter(Task.owner_id == user.id).all()
            if not tasks:
                continue
            completed = [t for t in tasks if t.status == TaskStatus.COMPLETED]
            completion_rate = len(completed) / len(tasks) if tasks else 0

            efficiency = 0
            if completed:
                total_estimated = sum(t.estimated_hours for t in completed)
                total_actual = sum(t.actual_hours for t in completed)
                efficiency = (total_estimated / total_actual) if total_actual > 0 else 0

            score = (completion_rate * 0.5 + efficiency * 0.5) * 100
            rankings.append(UserPerformance(
                user_id=user.id,
                username=user.username,
                full_name=user.full_name,
                completion_rate=completion_rate,
                efficiency=efficiency,
                total_tasks=len(tasks),
                completed_tasks=len(completed),
                performance_score=score,
            ))

        rankings.sort(key=lambda x: x.performance_score, reverse=True)
        return rankings

    def forecast_workload(self, user_id: int = None) -> Forecast:
        import numpy as np
        import pandas as pd

        query = self.db.query(Task)
        if user_id:
            query = query.filter(Task.owner_id == user_id)
        tasks = query.filter(Task.status != TaskStatus.COMPLETED).all()

        if len(tasks) < 5:
            return Forecast(predicted_completion_days=0, confidence_interval=[0, 0], risk_level="low")

        df = pd.DataFrame([{
            "created_at": t.created_at,
            "estimated_hours": t.estimated_hours,
            "priority_weight": {
                TaskPriority.LOW: 1,
                TaskPriority.MEDIUM: 2,
                TaskPriority.HIGH: 3,
                TaskPriority.URGENT: 4,
            }[t.priority],
        } for t in tasks])

        df["workload"] = df["estimated_hours"] * df["priority_weight"]
        df = df.sort_values("created_at")

        x = np.arange(len(df))
        y = df["workload"].cumsum().values
        if len(x) > 1:
            z = np.polyfit(x, y, 1)
            p = np.poly1d(z)
            predicted = p(len(x) + 5) - p(len(x) - 1)
        else:
            predicted = y[-1] if len(y) > 0 else 0

        return Forecast(
            predicted_completion_days=max(1, int(predicted / 8)),
            confidence_interval=[max(0, predicted - 10), predicted + 10],
            risk_level="high" if predicted > 40 else "medium" if predicted > 20 else "low",
        )
