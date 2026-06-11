import pytest

def test_get_task_statistics(client, auth_headers):
    response = client.get("/api/v1/analytics/tasks/statistics", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "total_tasks" in data
    assert "completed_tasks" in data
    assert "completion_rate" in data

def test_get_productivity(client, auth_headers):
    response = client.get("/api/v1/analytics/productivity", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "avg_daily_completion" in data
    assert "productivity_trend" in data

def test_get_forecast(client, auth_headers):
    response = client.get("/api/v1/analytics/forecast", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_completion_days" in data
    assert "risk_level" in data

def test_export_report(client, auth_headers):
    response = client.get("/api/v1/analytics/export?format=json", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "statistics" in data
    assert "productivity" in data

