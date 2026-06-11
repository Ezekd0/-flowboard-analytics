import pytest

def test_create_task(client, auth_headers):
    response = client.post(
        "/api/v1/tasks/",
        json={
            "title": "Test Task",
            "description": "This is a test task",
            "priority": "high"
        },
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["priority"] == "high"

def test_get_tasks(client, auth_headers):
    response = client.get("/api/v1/tasks/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_update_task(client, auth_headers):
    # Create a task first
    create_response = client.post(
        "/api/v1/tasks/",
        json={
            "title": "Original Task",
            "description": "Original description",
            "priority": "medium"
        },
        headers=auth_headers
    )
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]
    
    # Update the task
    response = client.put(
        f"/api/v1/tasks/{task_id}",
        json={
            "title": "Updated Task",
            "status": "completed"
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Task"

def test_delete_task(client, auth_headers):
    # Create a task first
    create_response = client.post(
        "/api/v1/tasks/",
        json={
            "title": "Task to Delete",
            "description": "This task will be deleted",
            "priority": "low"
        },
        headers=auth_headers
    )
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]
    
    # Delete the task
    response = client.delete(f"/api/v1/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 204

