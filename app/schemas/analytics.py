from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any

class TaskStatistics(BaseModel):
    total_tasks: int = 0
    completed_tasks: int = 0
    pending_tasks: int = 0
    in_progress_tasks: int = 0
    completion_rate: float = 0.0
    avg_completion_time_hours: Optional[float] = None
    avg_estimation_accuracy_percent: Optional[float] = None
    status_distribution: Dict[str, int] = Field(default_factory=dict)
    priority_distribution: Dict[str, int] = Field(default_factory=dict)

class ProductivityMetrics(BaseModel):
    daily_metrics: List[Dict[str, Any]] = Field(default_factory=list)
    weekly_metrics: List[Dict[str, Any]] = Field(default_factory=list)
    avg_daily_completion: Optional[float] = 0.0
    total_hours: Optional[int] = 0
    productivity_trend: List[float] = Field(default_factory=list)

class UserPerformance(BaseModel):
    user_id: int
    username: str
    full_name: Optional[str]
    completion_rate: float
    efficiency: float
    total_tasks: int
    completed_tasks: int
    performance_score: float

class Forecast(BaseModel):
    predicted_completion_days: int
    confidence_interval: List[float]
    risk_level: str

class TimeSeriesData(BaseModel):
    date: datetime
    value: float
    volume: Optional[int] = None

class AnalyticsResponse(BaseModel):
    id: int
    user_id: int
    metric_name: str
    metric_value: float
    recorded_at: datetime

    class Config:
        from_attributes = True
