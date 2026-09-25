# DevShowcase API

API REST para cadastrar **perfis de desenvolvedores**, seus **projetos**, as **tecnologias** usadas em cada projeto e os **feedbacks** recebidos.

Trabalho acadêmico: **Modelagem de domínio, persistência e endpoints básicos.**

Repositório: https://github.com/tatixana/devshowcase-api

> 👉 **Só quer ligar e testar? Leia o [COMECE_AQUI.md](COMECE_AQUI.md)** — uma página só.

## Objetivo

Iniciar o backend da plataforma DevShowcase com:

- entidades relacionais;
- persistência em banco de dados relacional (SQLite);
- DTOs/Schemas de entrada e de saída;
- validações dos dados recebidos;
- endpoints REST;
- demonstração prática pelo Postman.

## Integrantes

- LUSIMAR DAS SILVA DOS SANTOS
- LUCILENE COELHO DE SOUSA
- RAIMUNDA MARIA RIBEIRO DOS SANTOS
- TATILANE RIBEIRO DE ASSIS

## Tecnologias utilizadas

| Tecnologia | Para que serve no projeto |
|---|---|
| Python 3.13 | Linguagem de programação |
| FastAPI | Criação dos endpoints da API |
| SQLAlchemy | Comunicação com o banco (models e relacionamentos) |
| Pydantic | Schemas/DTOs e validações |
| SQLite | Banco de dados relacional (arquivo `devshowcase.db`) |
| Uvicorn | Servidor que executa a API |
| Git e GitHub | Versionamento e publicação do código |

## Entidades

| Entidade | O que representa | Campos |
|---|---|---|
| **Profile** | Perfil do desenvolvedor | id, name, bio, github_url, linkedin_url |
| **Project** | Um projeto do desenvolvedor | id, title, description, repository_url, demo_url, profile_id |
| **Technology** | Uma tecnologia usada nos projetos | id, name |
| **Feedback** | Uma opinião sobre um projeto | id, author_name, comment, project_id |

## Relacionamentos

**Profile 1:N Project**
Um perfil pode possuir vários projetos. Cada projeto pertence a um perfil (campo `profile_id`).

**Project N:N Technology**
Um projeto pode utilizar várias tecnologias e uma tecnologia pode ser utilizada por vários projetos.
Essa ligação fica guardada na tabela associativa `project_technologies`.

**Project 1:N Feedback**
Um projeto pode possuir vários feedbacks. Cada feedback pertence a um projeto (campo `project_id`).

```
Profile 1 ──── N Project N ──── N Technology
                    │        (project_technologies)
                    1
                    │
                    N
                 Feedback
```

> Nesta etapa o enunciado não pede endpoints de Feedback. A tabela e o relacionamento já estão prontos no banco.

## Endpoints

| Método | URL | O que faz | Sucesso |
|---|---|---|---|
| GET | `/` | Confirma que a API está funcionando | 200 |
| POST | `/api/profiles` | Cadastra um perfil | 201 |
| GET | `/api/profiles/{id}` | Busca um perfil pelo ID | 200 |
| POST | `/api/technologies` | Cadastra uma tecnologia | 201 |
| GET | `/api/technologies` | Lista todas as tecnologias | 200 |
| POST | `/api/projects` | Cadastra um projeto (com `profile_id` e `technology_ids`) | 201 |
| GET | `/api/projects` | Lista os projetos com o perfil e as tecnologias relacionadas | 200 |

### Validações e códigos de erro

| Situação | Código |
|---|---|
| `name` (Profile/Technology) ou `title` (Project) ausente ou vazio | 422 |
| URL inválida (`github_url`, `linkedin_url`, `repository_url`, `demo_url`) | 422 |
| Tipo errado (ex.: texto em `profile_id`) ou JSON mal escrito | 422 |
| Perfil não encontrado (GET por ID ou `profile_id` do projeto) | 404 |
| Tecnologia de `technology_ids` não encontrada | 404 |
| Tecnologia com nome já cadastrado | 400 |

Os campos de URL são opcionais, mas quando informados precisam ser endereços completos (ex.: `https://github.com/usuario`).

## Instalação (Windows)

Pré-requisito: Python 3.10 ou mais recente instalado.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Execução

```bash
uvicorn app.main:app --reload
```

- API: http://127.0.0.1:8000
- Swagger (documentação interativa): http://127.0.0.1:8000/docs

O banco `devshowcase.db` e todas as tabelas são criados automaticamente quando a API inicia.
Os dados continuam salvos mesmo depois de parar e iniciar a API novamente.

O passo a passo completo para iniciantes está em [PASSO_A_PASSO.md](PASSO_A_PASSO.md).

## Testando no Postman

Veja o guia [GUIA_POSTMAN.md](GUIA_POSTMAN.md), com os 8 testes na ordem da apresentação.

Exemplo — cadastrar um projeto (`POST /api/projects`):

```json
{
  "title": "Sistema de Biblioteca",
  "description": "API para gerenciamento de uma biblioteca.",
  "repository_url": "https://github.com/exemplo/sistema-biblioteca",
  "demo_url": "https://exemplo.com",
  "profile_id": 1,
  "technology_ids": [1, 2]
}
```

## Swagger

Com a API rodando, acesse http://127.0.0.1:8000/docs.
Lá aparecem todos os endpoints. Para testar: clique no endpoint → **Try it out** → preencha → **Execute**.

## Estrutura do projeto

```
devshowcase-api/
├── app/
│   ├── __init__.py
│   ├── main.py            # cria a API, as tabelas e junta os routers
│   ├── database.py        # conexão com o SQLite
│   ├── models.py          # entidades e relacionamentos (SQLAlchemy)
│   ├── schemas.py         # DTOs de entrada e saída + validações (Pydantic)
│   └── routers/
│       ├── __init__.py
│       ├── profiles.py      # endpoints de Profile
│       ├── technologies.py  # endpoints de Technology
│       └── projects.py      # endpoints de Project
├── requirements.txt
├── .gitignore
├── README.md
├── GUIA_POSTMAN.md
├── PASSO_A_PASSO.md
└── ROTEIRO_APRESENTACAO.md
```
