from fastapi import APIRouter, Depends, Query, HTTPException, Response
from typing import Annotated, Optional
from datetime import datetime

from app.services.analytics_service import AnalyticsService
from app.core.security import get_current_user, require_role
from app.models.user import User, UserRole
from app.core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/tasks/statistics")
def get_task_statistics(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
    user_id: Optional[int] = Query(None, description="User ID (admin only)")
):
    """Get task statistics for current user or specific user (admin)"""
    if user_id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    target_user_id = user_id if user_id else current_user.id
    analytics = AnalyticsService(db)
    
    return analytics.get_task_statistics(target_user_id)

@router.get("/productivity")
def get_productivity_metrics(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
    days: int = Query(30, ge=1, le=365),
    user_id: Optional[int] = Query(None)
):
    """Get productivity metrics and trends"""
    if user_id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    target_user_id = user_id if user_id else current_user.id
    analytics = AnalyticsService(db)
    
    return analytics.get_productivity_metrics(target_user_id, days)

@router.get("/performance/ranking")
def get_performance_ranking(
    current_user: Annotated[User, Depends(require_role([UserRole.ADMIN, UserRole.ANALYST]))],
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=100)
):
    """Get user performance ranking (admin/analyst only)"""
    analytics = AnalyticsService(db)
    rankings = analytics.get_user_performance_ranking()
    
    return {
        "ranking": rankings[:limit],
        "total_users": len(rankings)
    }

@router.get("/forecast")
def get_workload_forecast(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
    user_id: Optional[int] = None
):
    """Get workload forecast for planning"""
    if user_id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    target_user_id = user_id if user_id else current_user.id
    analytics = AnalyticsService(db)
    
    return analytics.forecast_workload(target_user_id)

@router.get("/export")
def export_analytics_report(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
    format: str = Query("json", pattern="^(json|csv)$")
):
    """Export analytics report (JSON or CSV)"""
    analytics = AnalyticsService(db)
    stats = analytics.get_task_statistics(current_user.id)
    metrics = analytics.get_productivity_metrics(current_user.id)
    
    report = {
        "generated_at": datetime.now().isoformat(),
        "user_id": current_user.id,
        "statistics": stats.dict(),
        "productivity": metrics.dict()
    }
    
    if format == "csv":
        import pandas as pd

        df = pd.DataFrame([report])
        return Response(
            content=df.to_csv(index=False),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=analytics_report.csv"}
        )
    
    return report
