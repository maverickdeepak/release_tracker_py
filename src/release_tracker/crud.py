from sqlmodel import Session, select

from .models import Project, ProjectCreate, ProjectUpdate


def slugify(value: str) -> str:
    cleaned = "".join(c for c in value.lower() if c.isalnum() or c == " ")
    return "-".join(cleaned.split()) or "project"


def list_projects(session: Session) -> list[Project]:
    # TODO: Build a select statement ordered by Project.name and return the list of all projects.
    pass


def get_project(session: Session, project_id: int) -> Project | None:
    # TODO: Return the Project for `project_id`, or None if it doesn't exist.
    pass


def create_project(session: Session, payload: ProjectCreate) -> Project:
    # TODO: Build a Project from the payload, derive its slug, add/commit/refresh, return it.
    pass


def update_project(
    session: Session, project: Project, payload: ProjectUpdate
) -> Project:
    # TODO: Apply payload to project (use exclude_unset=True so missing fields stay missing),
    # re-slugify if the name was set, then add/commit/refresh.
    pass


def delete_project(session: Session, project: Project) -> None:
    # TODO: Delete the project and commit.
    pass
