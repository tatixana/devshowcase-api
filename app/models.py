from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship

from app.database import Base

# Tabela associativa do relacionamento N:N entre Project e Technology.
project_technologies = Table(
    "project_technologies",
    Base.metadata,
    Column("project_id", Integer, ForeignKey("projects.id"), primary_key=True),
    Column("technology_id", Integer, ForeignKey("technologies.id"), primary_key=True),
)


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    bio = Column(Text, nullable=True)
    github_url = Column(String(255), nullable=True)
    linkedin_url = Column(String(255), nullable=True)

    # Profile 1:N Project
    projects = relationship("Project", back_populates="profile")


class Technology(Base):
    __tablename__ = "technologies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)

    # Technology N:N Project
    projects = relationship(
        "Project", secondary=project_technologies, back_populates="technologies"
    )


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    repository_url = Column(String(255), nullable=True)
    demo_url = Column(String(255), nullable=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)

    # Curtidas do projeto (endpoint de upvote).
    upvotes = Column(Integer, nullable=False, default=0, server_default="0")
    # Nota media, recalculada a cada feedback novo.
    rating_average = Column(Float, nullable=False, default=0.0, server_default="0")

    profile = relationship("Profile", back_populates="projects")
    technologies = relationship(
        "Technology", secondary=project_technologies, back_populates="projects"
    )
    # Project 1:N Feedback
    feedbacks = relationship("Feedback", back_populates="project")


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    author_name = Column(String(100), nullable=False)
    comment = Column(Text, nullable=False)
    # Nota de 1 a 5 dada ao projeto.
    rating = Column(Integer, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    project = relationship("Project", back_populates="feedbacks")
