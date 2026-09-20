from fastapi import FastAPI, HTTPException, status
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
@app.get("/projects/{project_id}", response_model=ProjectRead, status_code=status.HTTP_200_OK)
def get_project(project_id: int) -> ProjectRead:
    project = mock_database.get(project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project

#get a specific project by slug
@app.get("/projects/slug/{project_slug}", response_model=list[ProjectRead], status_code=status.HTTP_200_OK)
def get_project_by_slug(project_slug: str) -> list[ProjectRead]:
    projects = [project for project in mock_database.values() if project.slug == project_slug]
    if not projects:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return projects