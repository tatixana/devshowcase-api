from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app import models  # importar os models registra as tabelas no Base
from app.database import Base, engine
from app.routers import profiles, projects, technologies

# Cria as tabelas no devshowcase.db (se ainda não existirem) quando a API inicia.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DevShowcase API",
    description="API para cadastrar perfis de desenvolvedores, projetos, tecnologias e feedbacks.",
    version="1.0.0",
)

app.include_router(profiles.router)
app.include_router(technologies.router)
app.include_router(projects.router)


# Deixa os erros de validação (422) mais simples de ler, em português.
@app.exception_handler(RequestValidationError)
async def erro_de_validacao(request: Request, erro: RequestValidationError):
    traducoes = {
        "missing": "Este campo é obrigatório.",
        "int_parsing": "Informe um número inteiro.",
        "int_type": "Informe um número inteiro.",
        "string_type": "Informe um texto.",
        "list_type": "Informe uma lista, por exemplo [1, 2].",
        "json_invalid": "O JSON enviado está com erro de digitação.",
    }
    erros = []
    for item in erro.errors():
        campo = ".".join(str(parte) for parte in item["loc"] if parte != "body")
        mensagem = traducoes.get(item["type"], item["msg"].replace("Value error, ", ""))

        if item["type"] == "json_invalid":
            campo = "JSON"
        elif campo == "":
            # O Body inteiro está faltando ou não foi enviado como JSON.
            campo = "Body"
            mensagem = "Envie os dados em JSON pela aba Body (raw → JSON)."
        erros.append({"campo": campo, "mensagem": mensagem})

    return JSONResponse(
        status_code=422,
        content={"detail": "Os dados enviados são inválidos.", "erros": erros},
    )


@app.get("/", tags=["Início"])
def inicio():
    return {"message": "DevShowcase API está funcionando"}
