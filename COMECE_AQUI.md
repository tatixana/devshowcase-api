# COMECE AQUI

Uma página só. Ligar a API e testar.

---

## 1. Abrir o terminal na pasta certa

Abra a pasta `devshowcase-api` (a que tem a pasta `app` dentro).
Clique na barra de endereço lá em cima, apague tudo, digite **cmd** e aperte **Enter**.

## 2. Ligar a API

**Só na primeira vez:**

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**Todas as vezes:**

```
.venv\Scripts\activate
uvicorn app.main:app --reload
```

✅ Deu certo quando aparecer `Application startup complete.`

⚠️ **Não feche essa janela preta.** Ela é a API ligada.
Para desligar: **Ctrl + C**.

## 3. Ver funcionando (2 segundos)

No navegador: **http://127.0.0.1:8000**

Apareceu `{"message":"DevShowcase API está funcionando"}`? Está pronto.

---

## 4. Testar

### Jeito rápido (sem instalar nada)

No navegador: **http://127.0.0.1:8000/docs**
Clique num endpoint → **Try it out** → **Execute**.

### No Postman (é o que vai no vídeo)

Em cada teste: clique no **+**, escolha **GET** ou **POST**, cole a URL.
Se for **POST**, vá em **Body** → marque **raw** → troque **Text** por **JSON** → cole o JSON → **Send**.

Faça **nesta ordem** (os IDs dependem disso):

**1. Criar perfil** — POST `http://127.0.0.1:8000/api/profiles`
```json
{"name": "Ana Silva", "bio": "Desenvolvedora iniciante apaixonada por tecnologia.", "github_url": "https://github.com/anasilva", "linkedin_url": "https://linkedin.com/in/anasilva"}
```
→ volta `"id": 1` e **201**

**2. Buscar perfil** — GET `http://127.0.0.1:8000/api/profiles/1`
→ volta a Ana Silva e **200**

**3. Cadastrar Python** — POST `http://127.0.0.1:8000/api/technologies`
```json
{"name": "Python"}
```
→ volta `"id": 1` e **201**

**4. Cadastrar FastAPI** — POST `http://127.0.0.1:8000/api/technologies`
```json
{"name": "FastAPI"}
```
→ volta `"id": 2` e **201**

**5. Listar tecnologias** — GET `http://127.0.0.1:8000/api/technologies`
→ volta as duas e **200**

**6. Criar projeto** — POST `http://127.0.0.1:8000/api/projects`
```json
{"title": "Sistema de Biblioteca", "description": "API para gerenciamento de uma biblioteca.", "repository_url": "https://github.com/exemplo/sistema-biblioteca", "demo_url": "https://exemplo.com", "profile_id": 1, "technology_ids": [1, 2]}
```
→ volta o projeto **com a Ana e as 2 tecnologias juntas** e **201**

**7. Listar projetos** — GET `http://127.0.0.1:8000/api/projects`
→ volta o projeto completo e **200**

**8. Erro de propósito** — POST `http://127.0.0.1:8000/api/projects`
```json
{"title": "", "description": "Projeto inválido", "profile_id": 999, "technology_ids": [999]}
```
→ volta **422** dizendo que o título é obrigatório ✅ (é isso mesmo que a gente quer mostrar)

> 💾 **Dica:** salve cada aba com **Ctrl + S**. No dia do vídeo é só clicar em **Send**.

---

## 5. Deu erro?

| Apareceu | Faça |
|---|---|
| `'python' não é reconhecido` | Instale o Python em python.org e **marque "Add python.exe to PATH"** |
| `'uvicorn' não é reconhecido` | Faltou `.venv\Scripts\activate` (precisa aparecer `(.venv)` na linha) |
| `Could not import module "app.main"` | Terminal na pasta errada. Tem que ser a pasta que tem `app` dentro |
| No Postman: `Could not send request` | A API não está ligada. Volte ao passo 2 |
| Os IDs não são 1 e 2 | Ctrl + C → apague o arquivo `devshowcase.db` → ligue de novo |

---

## Antes de gravar o vídeo

1. **Ctrl + C** no terminal
2. Apague o arquivo **`devshowcase.db`** da pasta
3. Ligue de novo: `uvicorn app.main:app --reload`
4. **Não clique em Send em nada** até a gravação começar

Assim os IDs começam do 1 e batem com o roteiro.

---

### Os outros arquivos (só se precisar)

- **[ROTEIRO_APRESENTACAO.md](ROTEIRO_APRESENTACAO.md)** — quem fala o quê no vídeo 👈 o importante
- [GUIA_POSTMAN.md](GUIA_POSTMAN.md) — o Postman explicado com calma, tela por tela
- [PASSO_A_PASSO.md](PASSO_A_PASSO.md) — instalação detalhada e mais soluções de erro
- [README.md](README.md) — descrição do trabalho (entidades, relacionamentos, endpoints)
