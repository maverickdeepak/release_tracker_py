from typing import Annotated, Sequence
from fastapi import FastAPI, HTTPException, status, Depends
from sqlmodel import Session, select

from release_tracker.database import get_session
from release_tracker.models import Project, ProjectRead, ProjectCreate, ProjectUpdate
from release_tracker.utils import slugify

app = FastAPI(
    title="Release Tracker",
    description="API for tracking project milestones",
    version="1.0.0",
)

SessionDep = Annotated[Session, Depends(get_session)]


# get a list of all projects, optionally filtered by name
@app.get("/projects", response_model=list[ProjectRead], status_code=status.HTTP_200_OK)
def list_projects(session: SessionDep):
    statement = select(Project).order_by(Project.name)
    projects = session.exec(statement).all()
    return list(projects)


# get a specific project by ID
@app.get(
    "/projects/{project_id}", response_model=ProjectRead, status_code=status.HTTP_200_OK
)
def get_project(project_id: int, session: SessionDep) -> Project:
    # project = mock_database.get(project_id)
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    return project


# get a specific project by slug
@app.get(
    "/projects/slug/{project_slug}",
    response_model=list[ProjectRead],
    status_code=status.HTTP_200_OK,
)
def get_project_by_slug(project_slug: str, session: SessionDep) -> Sequence[Project]:
    # projects = [project for project in mock_database.values() if project.slug == project_slug]
    statement = select(Project).where(Project.slug == project_slug)
    projects = session.exec(statement).all()
    if not projects:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    return projects

# create new project
@app.post("/projects", response_model=ProjectRead, status_code= status.HTTP_201_CREATED)
def create_project(payload: ProjectCreate, session: SessionDep) -> Project:
    project = Project.model_validate(payload, update={
        "slug": slugify(payload.name)
    })
    session.add(project)
    session.commit()
    session.refresh(project)
    return project

# delete a project
@app.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, session: SessionDep) -> None:
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    session.delete(project)
    session.commit()