import pytest

def test_get_analytics_summary(client):
    response = client.get("/api/v1/analytics/summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_tasks" in data
    assert "completed_tasks" in data

def test_get_task_analytics(client):
    response = client.get("/api/v1/analytics/tasks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)

def test_get_metrics(client):
    response = client.get("/api/v1/analytics/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "total_tasks" in data
    assert "completion_rate" in data
