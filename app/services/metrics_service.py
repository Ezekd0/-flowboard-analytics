from sqlalchemy.orm import Session

class MetricsService:
    def __init__(self, db: Session):
        self.db = db

    def record_metric(self, user_id: int, metric_name: str, metric_value: float):
        # TODO: Implement metric recording
        pass
