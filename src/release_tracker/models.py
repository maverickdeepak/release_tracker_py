from datetime import UTC, datetime
from typing import Annotated

from pydantic import StringConstraints
from sqlalchemy import Column, DateTime
from sqlmodel import SQLModel, Field

# Define the Project model for the database
ProjectName = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=100),
]


class ProjectBase(SQLModel):
    name: ProjectName = Field(unique=True, description="The name of the project")
    description: str | None = Field(
        default=None, description="A brief description of the project"
    )


class Project(ProjectBase, table=True):
    __tablename__ = "projects"  # type: ignore
    id: int | None = Field(default=None, primary_key=True)
    slug: str = Field(
        unique=True, description="A URL-friendly identifier for the project"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="The timestamp when the project was created",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="The timestamp when the project was last updated",
    )


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(SQLModel):
    name: ProjectName | None = Field(
        default=None, description="The name of the project"
    )
    description: str | None = Field(
        default=None, description="A brief description of the project"
    )


class ProjectRead(ProjectBase):
    id: int
    slug: str
    created_at: datetime
    updated_at: datetime
