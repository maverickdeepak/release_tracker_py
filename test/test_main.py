from fastapi.testclient import TestClient
from release_tracker.main import app

client = TestClient(app)

def test_list_projects():
    response = client.get("/projects")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3  # We have 3 projects in the mock database

def test_list_projects_with_name_filter():
    response = client.get("/projects?name=API")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1  # Only one project matches the name filter
    assert data[0]["name"] == "API Version 2"
    
def test_get_project_by_id():
    response = client.get("/projects/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Frontend Redesign"
    assert data["slug"] == "frontend-redesign"
    
def test_get_project_by_id_not_found():
    response = client.get("/projects/999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Project not found"
    
def test_get_project_by_slug():
    response = client.get("/projects/slug/frontend-redesign")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["slug"] == "frontend-redesign"

def test_get_project_by_slug_not_found():
    response = client.get("/projects/slug/non-existent-slug")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Project not found"