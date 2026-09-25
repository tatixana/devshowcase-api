from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/api/projects", tags=["Projects"])


@router.post("", response_model=schemas.ProjectResponse, status_code=201)
def criar_project(dados: schemas.ProjectCreate, db: Session = Depends(get_db)):
    # 1. O perfil informado precisa existir.
    profile = db.get(models.Profile, dados.profile_id)
    if profile is None:
        raise HTTPException(
            status_code=404, detail=f"Perfil com id {dados.profile_id} não encontrado."
        )

    # 2. Todas as tecnologias informadas precisam existir.
    ids_pedidos = set(dados.technology_ids)
    technologies = (
        db.query(models.Technology).filter(models.Technology.id.in_(ids_pedidos)).all()
    )
    ids_encontrados = {technology.id for technology in technologies}
    ids_faltando = sorted(ids_pedidos - ids_encontrados)
    if ids_faltando:
        raise HTTPException(
            status_code=404,
            detail=f"Tecnologia(s) com id {ids_faltando} não encontrada(s).",
        )

    # 3. Salva o projeto ligado ao perfil e às tecnologias.
    project = models.Project(
        title=dados.title,
        description=dados.description,
        repository_url=dados.repository_url,
        demo_url=dados.demo_url,
        profile=profile,
        technologies=technologies,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.get("", response_model=list[schemas.ProjectResponse])
def listar_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).order_by(models.Project.id).all()
