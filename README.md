# DevShowcase API

API REST para cadastrar **perfis de desenvolvedores**, seus **projetos**, as **tecnologias** usadas em cada projeto e os **feedbacks** recebidos.

Trabalho acadêmico: **Modelagem de domínio, persistência e endpoints básicos.**

Repositório: https://github.com/tatixana/devshowcase-api

> 👉 **Só quer ligar e testar?** Dois cliques no arquivo **`INICIAR`** e pronto.
> Detalhes em [COMECE_AQUI.md](COMECE_AQUI.md) — uma página só.

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
| SQLite | Banco de dados no computador (arquivo `devshowcase.db`) |
| PostgreSQL | Banco de dados em produção, na nuvem (Supabase) |
| Render | Serviço que publica a API, com deploy contínuo do GitHub |
| Uvicorn | Servidor que executa a API |
| Git e GitHub | Versionamento e publicação do código |

## Entidades

| Entidade | O que representa | Campos |
|---|---|---|
| **Profile** | Perfil do desenvolvedor | id, name, bio, github_url, linkedin_url |
| **Project** | Um projeto do desenvolvedor | id, title, description, repository_url, demo_url, profile_id |
| **Technology** | Uma tecnologia usada nos projetos | id, name |
| **Feedback** | Uma opinião sobre um projeto | id, author_name, comment, rating, project_id |

O projeto guarda ainda dois campos calculados: `upvotes` (curtidas) e `rating_average` (nota média, recalculada a cada feedback novo).

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
| GET | `/health` | Usado pela nuvem para saber se a API está de pé | 200 |
| POST | `/api/profiles` | Cadastra um perfil | 201 |
| GET | `/api/profiles/{id}` | Busca um perfil pelo ID | 200 |
| POST | `/api/technologies` | Cadastra uma tecnologia | 201 |
| GET | `/api/technologies` | Lista todas as tecnologias | 200 |
| POST | `/api/projects` | Cadastra um projeto (com `profile_id` e `technology_ids`) | 201 |
| GET | `/api/projects` | Lista os projetos, com filtro por tecnologia e paginação | 200 |
| POST | `/api/projects/{id}/feedbacks` | Cadastra nota de 1 a 5 e comentário, e recalcula a nota média | 201 |
| GET | `/api/projects/{id}/feedbacks` | Lista os feedbacks de um projeto | 200 |
| PUT | `/api/projects/{id}/upvote` | Soma uma curtida no projeto | 200 |

### Filtro e paginação em `GET /api/projects`

Sem nenhum parâmetro, devolve a lista completa de projetos.

Com parâmetros, devolve o resultado dividido em páginas:

| Parâmetro | Para que serve | Exemplo |
|---|---|---|
| `tecnologia` | Mostra só os projetos que usam aquela tecnologia | `?tecnologia=Python` |
| `pagina` | Qual página mostrar (começa em 1) | `?pagina=2` |
| `por_pagina` | Quantos projetos por página (até 100) | `?por_pagina=5` |

```
GET /api/projects?tecnologia=Python&pagina=1&por_pagina=5
```

```json
{
  "total": 7,
  "pagina": 1,
  "por_pagina": 5,
  "total_paginas": 2,
  "projetos": [ ... ]
}
```

### Validações e códigos de erro

| Situação | Código |
|---|---|
| `name` (Profile/Technology) ou `title` (Project) ausente ou vazio | 422 |
| URL inválida (`github_url`, `linkedin_url`, `repository_url`, `demo_url`) | 422 |
| Nota (`rating`) fora do intervalo de 1 a 5 | 422 |
| Tipo errado (ex.: texto em `profile_id`) ou JSON mal escrito | 422 |
| Perfil, projeto ou tecnologia não encontrado | 404 |
| Endereço que não existe na API | 404 |
| Método errado no endereço (ex.: DELETE onde só tem GET) | 405 |
| Tecnologia com nome já cadastrado | 400 |
| Erro inesperado ou falha no banco de dados | 500 |

Os campos de URL são opcionais, mas quando informados precisam ser endereços completos (ex.: `https://github.com/usuario`).

### Tratamento global de erros

Todo erro da API sai no mesmo formato, em português:

```json
{
  "erro": "Não encontrado",
  "detalhe": "Projeto com id 999 não encontrado.",
  "codigo": 404
}
```

Nos erros de validação (422), vem também a lista de campos com problema:

```json
{
  "erro": "Dados inválidos",
  "detalhe": "Os dados enviados são inválidos.",
  "codigo": 422,
  "erros": [
    { "campo": "rating", "mensagem": "A nota precisa ser um número de 1 a 5." }
  ]
}
```

Detalhes técnicos de erros internos ficam apenas no log do servidor, nunca na resposta.

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

## Deploy em produção

A API roda na nuvem com **deploy contínuo**: a cada commit na branch `main`, o
Render publica a versão nova automaticamente.

| Parte | Serviço |
|---|---|
| Banco de dados PostgreSQL | Supabase |
| API | Render (plano gratuito) |

As credenciais **não ficam no código**. A aplicação lê a variável de ambiente
`DATABASE_URL`, configurada no painel do Render. Quando essa variável não existe
(no computador de casa), a API usa o SQLite automaticamente — ver
[app/database.py](app/database.py).

O passo a passo completo para publicar está em **GUIA_DEPLOY.pdf**.

> No plano gratuito do Render a API dorme depois de 15 minutos sem uso.
> A primeira visita depois disso demora cerca de 50 segundos para responder.

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
