# Guia do Postman — DevShowcase API

Este guia é para quem **nunca usou o Postman**. Siga com calma, um teste de cada vez, na ordem.

> Antes de tudo, a API precisa estar rodando (veja o [PASSO_A_PASSO.md](PASSO_A_PASSO.md)).
> No terminal deve aparecer: `Uvicorn running on http://127.0.0.1:8000`.
> **Não feche esse terminal** enquanto estiver testando.

---

## Como fazer uma requisição no Postman

O Postman é um programa que envia pedidos (requisições) para a API e mostra a resposta.

### 1. Abrir uma nova requisição

Clique no botão **+** (ao lado das abas, na parte de cima). Uma aba nova, em branco, vai abrir.

### 2. Escolher GET ou POST

À esquerda da barra de endereço existe uma caixinha escrita **GET**.
Clique nela e escolha:

- **GET** → quando queremos **buscar/listar** informações;
- **POST** → quando queremos **cadastrar** algo novo.

### 3. Colocar a URL

Clique na barra grande ao lado (onde está escrito *Enter URL or paste text*) e cole a URL do teste.
Exemplo: `http://127.0.0.1:8000/api/profiles`

### 4. Colocar o JSON (só nos testes com POST)

1. Logo abaixo da URL, clique na aba **Body**.
2. Marque a opção **raw**.
3. No final da mesma linha aparece uma caixinha escrita **Text**. Clique nela e troque para **JSON**.
4. Clique na área grande em branco e **cole o JSON** do teste.

> Nos testes com **GET** não precisa mexer no Body.

### 5. Enviar

Clique no botão azul **Send**.

### 6. Ver a resposta

A resposta aparece na parte de baixo da tela. Olhe duas coisas:

- o **conteúdo** (o JSON que a API devolveu);
- o **Status**, no canto direito (ex.: `201 Created`, `200 OK`, `422 Unprocessable Content`).

| Status | Significado simples |
|---|---|
| 200 OK | Deu certo (busca/listagem). |
| 201 Created | Deu certo e algo novo foi cadastrado. |
| 400 Bad Request | Pedido não permitido (ex.: tecnologia repetida). |
| 404 Not Found | O registro procurado não existe. |
| 422 Unprocessable Content | Os dados enviados estão errados (validação). |

> **Dica:** faça cada teste em uma aba separada (botão **+**) e salve com **Ctrl + S**. Assim, na hora de gravar o vídeo, está tudo pronto — é só clicar em **Send**.

---

## Os 8 testes (na ordem da apresentação)

> Os IDs abaixo (1 e 2) são os esperados quando o banco começa vazio.
> Se aparecerem outros números, veja a seção **"Os IDs não são 1 e 2"** no final.

---

### TESTE 1 — Criar Profile

- **Método:** POST
- **URL:** `http://127.0.0.1:8000/api/profiles`
- **Body → raw → JSON:**

```json
{
  "name": "Ana Silva",
  "bio": "Desenvolvedora iniciante apaixonada por tecnologia.",
  "github_url": "https://github.com/anasilva",
  "linkedin_url": "https://linkedin.com/in/anasilva"
}
```

- **Resposta esperada:** Status **201 Created**

```json
{
  "id": 1,
  "name": "Ana Silva",
  "bio": "Desenvolvedora iniciante apaixonada por tecnologia.",
  "github_url": "https://github.com/anasilva",
  "linkedin_url": "https://linkedin.com/in/anasilva"
}
```

- **Fala sugerida:** *"Primeiro vamos cadastrar um perfil. Como podemos ver, o perfil foi criado com sucesso, recebeu o ID 1 e o status foi 201, que significa criado."*

---

### TESTE 2 — Buscar Profile

- **Método:** GET
- **URL:** `http://127.0.0.1:8000/api/profiles/1`
- **Body:** não precisa.
- **Resposta esperada:** Status **200 OK**

```json
{
  "id": 1,
  "name": "Ana Silva",
  "bio": "Desenvolvedora iniciante apaixonada por tecnologia.",
  "github_url": "https://github.com/anasilva",
  "linkedin_url": "https://linkedin.com/in/anasilva"
}
```

- **Fala sugerida:** *"Agora vamos buscar esse perfil pelo ID. O número 1 no final do endereço é o ID do perfil. A API encontrou e devolveu os dados da Ana Silva."*

---

### TESTE 3 — Cadastrar Python

- **Método:** POST
- **URL:** `http://127.0.0.1:8000/api/technologies`
- **Body → raw → JSON:**

```json
{
  "name": "Python"
}
```

- **Resposta esperada:** Status **201 Created**

```json
{
  "id": 1,
  "name": "Python"
}
```

- **Fala sugerida:** *"Em seguida vamos cadastrar as tecnologias. Primeiro o Python, que recebeu o ID 1."*

---

### TESTE 4 — Cadastrar FastAPI

- **Método:** POST
- **URL:** `http://127.0.0.1:8000/api/technologies`
- **Body → raw → JSON:**

```json
{
  "name": "FastAPI"
}
```

- **Resposta esperada:** Status **201 Created**

```json
{
  "id": 2,
  "name": "FastAPI"
}
```

- **Fala sugerida:** *"Agora o FastAPI, que recebeu o ID 2."*

> Se clicar em **Send** duas vezes, a API responde **400** dizendo que a tecnologia já está cadastrada. Isso é esperado: ela não deixa repetir.

---

### TESTE 5 — Listar Technologies

- **Método:** GET
- **URL:** `http://127.0.0.1:8000/api/technologies`
- **Body:** não precisa.
- **Resposta esperada:** Status **200 OK**

```json
[
  {
    "id": 1,
    "name": "Python"
  },
  {
    "id": 2,
    "name": "FastAPI"
  }
]
```

- **Fala sugerida:** *"Agora podemos listar as tecnologias cadastradas. Aparecem o Python e o FastAPI, que acabamos de cadastrar."*

---

### TESTE 6 — Criar Project

- **Método:** POST
- **URL:** `http://127.0.0.1:8000/api/projects`
- **Body → raw → JSON:**

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

- **Resposta esperada:** Status **201 Created**

```json
{
  "id": 1,
  "title": "Sistema de Biblioteca",
  "description": "API para gerenciamento de uma biblioteca.",
  "repository_url": "https://github.com/exemplo/sistema-biblioteca",
  "demo_url": "https://exemplo.com",
  "profile_id": 1,
  "profile": {
    "id": 1,
    "name": "Ana Silva",
    "bio": "Desenvolvedora iniciante apaixonada por tecnologia.",
    "github_url": "https://github.com/anasilva",
    "linkedin_url": "https://linkedin.com/in/anasilva"
  },
  "technologies": [
    { "id": 1, "name": "Python" },
    { "id": 2, "name": "FastAPI" }
  ]
}
```

- **Fala sugerida:** *"Vamos cadastrar um projeto associado ao perfil e às tecnologias. O profile_id 1 liga o projeto à Ana Silva, e o technology_ids 1 e 2 liga o projeto ao Python e ao FastAPI. Na resposta já aparecem o perfil e as tecnologias do projeto."*

---

### TESTE 7 — Listar Projects

- **Método:** GET
- **URL:** `http://127.0.0.1:8000/api/projects`
- **Body:** não precisa.
- **Resposta esperada:** Status **200 OK** — uma lista (entre `[ ]`) com o projeto "Sistema de Biblioteca", o perfil da Ana Silva e as tecnologias Python e FastAPI (mesmo conteúdo do Teste 6).

- **Fala sugerida:** *"Agora vamos listar os projetos cadastrados. Aparece o Sistema de Biblioteca, com o perfil da Ana Silva e as tecnologias Python e FastAPI. Isso mostra os relacionamentos funcionando."*

---

### TESTE 8 — Demonstrar uma validação (erro proposital)

- **Método:** POST
- **URL:** `http://127.0.0.1:8000/api/projects`
- **Body → raw → JSON:**

```json
{
  "title": "",
  "description": "Projeto inválido",
  "profile_id": 999,
  "technology_ids": [999]
}
```

- **Resposta esperada:** Status **422 Unprocessable Content**

```json
{
  "detail": "Os dados enviados são inválidos.",
  "erros": [
    {
      "campo": "title",
      "mensagem": "Este campo é obrigatório e não pode ficar vazio."
    }
  ]
}
```

- **Fala sugerida:** *"Também implementamos validações. Vamos enviar uma informação inválida propositalmente: o título está vazio. Como podemos ver, a API identificou o problema e retornou o erro 422, explicando que o título é obrigatório. Nada foi salvo no banco."*

#### TESTE 8B (opcional) — Perfil que não existe

Mesma URL e método. Agora o título está preenchido, mas o perfil 999 não existe:

```json
{
  "title": "Projeto Teste",
  "profile_id": 999,
  "technology_ids": [1]
}
```

- **Resposta esperada:** Status **404 Not Found**

```json
{
  "detail": "Perfil com id 999 não encontrado."
}
```

- **Fala sugerida:** *"E se o perfil não existir, a API também avisa, com o erro 404."*

> Com `"profile_id": 1` e `"technology_ids": [999]`, a resposta é **404** com
> `"Tecnologia(s) com id [999] não encontrada(s)."`

**Por que o Teste 8 mostra só o erro do título?** A API primeiro confere se os dados estão bem preenchidos (título, URLs, tipos). Só depois, se estiver tudo certo, ela procura o perfil e as tecnologias no banco. Por isso o Teste 8B existe: para mostrar essa segunda verificação.

---

## Outras validações que podem ser mostradas (opcional)

| O que enviar | Onde | Resposta |
|---|---|---|
| `{"name": ""}` | POST /api/technologies | 422 — campo obrigatório |
| `{"name": "Ana", "github_url": "github-ana"}` | POST /api/profiles | 422 — URL inválida |
| `{"bio": "sem nome"}` | POST /api/profiles | 422 — `name` é obrigatório |
| GET `/api/profiles/999` | — | 404 — perfil não encontrado |

---

## Os IDs não são 1 e 2?

Se o banco já tinha registros de testes anteriores, os IDs continuam a contagem (3, 4, 5...).
Você pode:

- **usar os IDs que apareceram** (troque o `1` da URL do Teste 2 e os números do Teste 6); ou
- **começar um banco novo**: pare a API (Ctrl + C no terminal), apague o arquivo `devshowcase.db` da pasta do projeto e inicie a API de novo. Os IDs voltam a começar do 1.

## Problemas comuns no Postman

| Problema | Solução |
|---|---|
| `Could not send request` / `ECONNREFUSED` | A API não está rodando. Inicie com `uvicorn app.main:app --reload`. |
| `404 Not Found` com `"detail": "Not Found"` | URL digitada errada. Confira `/api/` e o plural (`profiles`, `technologies`, `projects`). |
| `405 Method Not Allowed` | Método errado. Confira se escolheu GET ou POST. |
| `422` com `"campo": "Body"` | O JSON não foi enviado. Confira se está na aba **Body**, com **raw** e **JSON** selecionados. |
| `422` com `"campo": "JSON"` | Falta ou sobra vírgula/aspas no JSON. Copie o JSON do guia novamente. |
