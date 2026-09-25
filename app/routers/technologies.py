from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/api/technologies", tags=["Technologies"])


@router.post("", response_model=schemas.TechnologyResponse, status_code=201)
def criar_technology(dados: schemas.TechnologyCreate, db: Session = Depends(get_db)):
    # Não deixa cadastrar a mesma tecnologia duas vezes (ex.: "Python" e "python").
    existente = (
        db.query(models.Technology)
        .filter(func.lower(models.Technology.name) == dados.name.lower())
        .first()
    )
    if existente:
        raise HTTPException(
            status_code=400,
            detail=f"A tecnologia '{existente.name}' já está cadastrada com o id {existente.id}.",
        )

    technology = models.Technology(name=dados.name)
    db.add(technology)
    db.commit()
    db.refresh(technology)
    return technology


@router.get("", response_model=list[schemas.TechnologyResponse])
def listar_technologies(db: Session = Depends(get_db)):
    return db.query(models.Technology).order_by(models.Technology.id).all()
