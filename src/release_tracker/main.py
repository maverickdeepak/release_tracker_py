from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Release Tracker", description="API for tracking software releases", version="1.0.0")

class ProjectRead(BaseModel):
    id: int
    name: str
    slug: str

# mock database for demonstration purposes
mock_database: dict[int, ProjectRead] = {
    1: ProjectRead(id=1, name="Frontend Redesign", slug="frontend-redesign"),
    2: ProjectRead(id=2, name="API Version 2", slug="api-v2"),
    3: ProjectRead(id=3, name="Database Migration", slug="database-migration"),
}


# get a list of all projects, optionally filtered by name
@app.get("/projects")
def list_projects(name: str | None = None):
    projects = list(mock_database.values())
    if name:
        projects = [project for project in projects if name in project.name]
    return projects

# get a specific project by ID
@app.get("/projects/{project_id}", response_model=ProjectRead)
def get_project(project_id: int) -> ProjectRead:
    project = mock_database.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
