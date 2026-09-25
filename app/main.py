import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app import models  # importar os models registra as tabelas no Base
from app.database import Base, engine
from app.routers import profiles, projects, technologies

logger = logging.getLogger("devshowcase")

# Cria as tabelas no banco (se ainda não existirem) quando a API inicia.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DevShowcase API",
    description=(
        "API para cadastrar perfis de desenvolvedores, projetos, tecnologias "
        "e feedbacks.\n\n"
        "Os projetos podem receber notas de 1 a 5 e curtidas, e a listagem "
        "aceita filtro por tecnologia e paginação."
    ),
    version="2.0.0",
)

app.include_router(profiles.router)
app.include_router(technologies.router)
app.include_router(projects.router)


# ---------------------------------------------------------------------------
# Tratamento global de erros
#
# Todos os erros da API saem no mesmo formato, em português:
#   { "erro": "...", "detalhe": "...", "codigo": 404 }
# ---------------------------------------------------------------------------

NOMES = {
    400: "Requisição inválida",
    401: "Não autorizado",
    403: "Acesso negado",
    404: "Não encontrado",
    405: "Método não permitido",
    409: "Conflito",
    422: "Dados inválidos",
    500: "Erro interno no servidor",
}

TRADUCOES = {
    "missing": "Este campo é obrigatório.",
    "int_parsing": "Informe um número inteiro.",
    "int_type": "Informe um número inteiro.",
    "float_parsing": "Informe um número.",
    "string_type": "Informe um texto.",
    "list_type": "Informe uma lista, por exemplo [1, 2].",
    "json_invalid": "O JSON enviado está com erro de digitação.",
    "greater_than_equal": "O valor é menor que o mínimo permitido.",
    "less_than_equal": "O valor é maior que o máximo permitido.",
}


def resposta_de_erro(codigo: int, detalhe, erros=None):
    corpo = {
        "erro": NOMES.get(codigo, "Erro"),
        "detalhe": detalhe,
        "codigo": codigo,
    }
    if erros:
        corpo["erros"] = erros
    return JSONResponse(status_code=codigo, content=corpo)


@app.exception_handler(RequestValidationError)
async def erro_de_validacao(request: Request, erro: RequestValidationError):
    """422 - algum campo veio errado ou faltando."""
    erros = []
    for item in erro.errors():
        partes = [p for p in item["loc"] if p not in ("body", "query", "path")]
        campo = ".".join(str(p) for p in partes)
        mensagem = TRADUCOES.get(item["type"], item["msg"].replace("Value error, ", ""))

        if item["type"] == "json_invalid":
            campo = "JSON"
        elif campo == "":
            # O Body inteiro está faltando ou não foi enviado como JSON.
            campo = "Body"
            mensagem = "Envie os dados em JSON pela aba Body (raw → JSON)."
        elif item["type"] in ("greater_than_equal", "less_than_equal"):
            limite = item.get("ctx", {})
            valor = limite.get("ge", limite.get("le"))
            if campo == "rating":
                mensagem = "A nota precisa ser um número de 1 a 5."
            elif valor is not None:
                mensagem = f"{mensagem} (limite: {valor})"

        erros.append({"campo": campo, "mensagem": mensagem})

    return resposta_de_erro(422, "Os dados enviados são inválidos.", erros)


# Mensagens padrão do FastAPI, em inglês, traduzidas.
PADRAO = {
    "Not Found": "Este endereço não existe nesta API. Confira a URL.",
    "Method Not Allowed": "Este endereço não aceita esse método. Confira se é GET, POST ou PUT.",
    "Internal Server Error": "Ocorreu um erro inesperado no servidor.",
}


@app.exception_handler(StarletteHTTPException)
async def erro_http(request: Request, erro: StarletteHTTPException):
    """404, 400, 405 e outros erros que a própria API levanta."""
    detalhe = PADRAO.get(erro.detail, erro.detail)
    return resposta_de_erro(erro.status_code, detalhe)


@app.exception_handler(SQLAlchemyError)
async def erro_de_banco(request: Request, erro: SQLAlchemyError):
    """Problema ao falar com o banco de dados."""
    logger.exception("Erro de banco de dados em %s", request.url.path)
    return resposta_de_erro(
        500, "Não foi possível acessar o banco de dados. Tente novamente."
    )


@app.exception_handler(Exception)
async def erro_inesperado(request: Request, erro: Exception):
    """Qualquer outro erro não previsto. O detalhe técnico fica só no log."""
    logger.exception("Erro inesperado em %s", request.url.path)
    return resposta_de_erro(500, "Ocorreu um erro inesperado no servidor.")


@app.get("/", tags=["Início"])
def inicio():
    return {"message": "DevShowcase API está funcionando"}


@app.get("/health", tags=["Início"])
def health():
    """Usado pelo servidor da nuvem para saber se a API está de pé."""
    return {"status": "ok"}
