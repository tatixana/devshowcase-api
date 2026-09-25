from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/api/projects", tags=["Projects"])


def buscar_projeto_ou_404(project_id: int, db: Session) -> models.Project:
    """Busca o projeto pelo id. Se não existir, responde 404."""
    project = db.get(models.Project, project_id)
    if project is None:
        raise HTTPException(
            status_code=404, detail=f"Projeto com id {project_id} não encontrado."
        )
    return project


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


@router.get("", response_model=schemas.ProjectsPage | list[schemas.ProjectResponse])
def listar_projects(
    db: Session = Depends(get_db),
    tecnologia: str | None = Query(
        default=None, description="Filtra pelo nome da tecnologia. Ex.: Python"
    ),
    pagina: int = Query(default=1, ge=1, description="Número da página"),
    por_pagina: int | None = Query(
        default=None, ge=1, le=100, description="Quantos projetos por página"
    ),
):
    """Lista os projetos.

    Sem nenhum parâmetro devolve a lista completa.
    Informando `tecnologia`, `pagina` ou `por_pagina` devolve o resultado em páginas.
    """
    consulta = db.query(models.Project)

    # Filtro por tecnologia: junta com a tabela de tecnologias e compara o nome.
    if tecnologia is not None:
        consulta = consulta.join(models.Project.technologies).filter(
            func.lower(models.Technology.name) == tecnologia.strip().lower()
        )

    consulta = consulta.order_by(models.Project.id)

    # Sem filtro e sem paginação: devolve a lista simples.
    if tecnologia is None and por_pagina is None and pagina == 1:
        return consulta.all()

    total = consulta.count()
    tamanho = por_pagina or 10
    total_paginas = max(1, (total + tamanho - 1) // tamanho)
    projetos = consulta.offset((pagina - 1) * tamanho).limit(tamanho).all()

    return schemas.ProjectsPage(
        total=total,
        pagina=pagina,
        por_pagina=tamanho,
        total_paginas=total_paginas,
        projetos=projetos,
    )


@router.post(
    "/{project_id}/feedbacks",
    response_model=schemas.FeedbackCriadoResponse,
    status_code=201,
)
def criar_feedback(
    project_id: int, dados: schemas.FeedbackCreate, db: Session = Depends(get_db)
):
    """Cadastra um feedback (nota de 1 a 5 e comentário) e atualiza a nota média."""
    project = buscar_projeto_ou_404(project_id, db)

    feedback = models.Feedback(
        author_name=dados.author_name,
        comment=dados.comment,
        rating=dados.rating,
        project=project,
    )
    db.add(feedback)
    db.flush()  # grava o feedback antes de recalcular a média

    # Recalcula a nota média do projeto com todos os feedbacks dele.
    notas = [f.rating for f in project.feedbacks]
    project.rating_average = round(sum(notas) / len(notas), 2)

    db.commit()
    db.refresh(feedback)
    db.refresh(project)

    return schemas.FeedbackCriadoResponse(
        feedback=feedback,
        rating_average=project.rating_average,
        total_feedbacks=len(notas),
    )


@router.get("/{project_id}/feedbacks", response_model=list[schemas.FeedbackResponse])
def listar_feedbacks(project_id: int, db: Session = Depends(get_db)):
    """Lista os feedbacks de um projeto."""
    project = buscar_projeto_ou_404(project_id, db)
    return sorted(project.feedbacks, key=lambda f: f.id)


@router.put("/{project_id}/upvote", response_model=schemas.ProjectResponse)
def dar_upvote(project_id: int, db: Session = Depends(get_db)):
    """Soma uma curtida no projeto."""
    project = buscar_projeto_ou_404(project_id, db)
    project.upvotes += 1
    db.commit()
    db.refresh(project)
    return project
