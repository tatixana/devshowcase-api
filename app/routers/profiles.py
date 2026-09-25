from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/api/profiles", tags=["Profiles"])


@router.post("", response_model=schemas.ProfileResponse, status_code=201)
def criar_profile(dados: schemas.ProfileCreate, db: Session = Depends(get_db)):
    profile = models.Profile(**dados.model_dump())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.get("/{profile_id}", response_model=schemas.ProfileResponse)
def buscar_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = db.get(models.Profile, profile_id)
    if profile is None:
        raise HTTPException(status_code=404, detail=f"Perfil com id {profile_id} não encontrado.")
    return profile
