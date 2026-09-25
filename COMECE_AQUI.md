# COMECE AQUI

## Ligar a API: dois cliques

Abra a pasta do projeto e dê **dois cliques** no arquivo:

# 🔵 `INICIAR`

Pronto. Ele faz tudo sozinho.

- Na **primeira vez** demora 1 ou 2 minutos (está preparando tudo). Pode esperar.
- Nas outras vezes abre em segundos.
- O navegador abre sozinho no final.

⚠️ **Não feche a janela azul** que ficar aberta. Ela é a API ligada.
Para desligar, é só fechar essa janela.

> Se aparecer um aviso do Windows sobre "proteger o computador":
> clique em **Mais informações** → **Executar assim mesmo**.
> Isso acontece porque o arquivo veio da internet.

---

## Testar

### Jeito rápido — o navegador que abriu sozinho

Ele já abre em **http://127.0.0.1:8000/docs**

Clique num endpoint → **Try it out** → **Execute**. Pronto, testou.

### No Postman — é o que vai no vídeo

Em cada teste: clique no **+**, escolha **GET** ou **POST**, cole a URL.
Se for **POST**: aba **Body** → marque **raw** → troque **Text** por **JSON** → cole → **Send**.

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

## Antes de gravar o vídeo

Os cadastros dos ensaios ficam salvos. Se não limpar, os IDs não vão ser 1 e 2.

1. Feche a **janela azul** da API
2. Dois cliques em **`LIMPAR_BANCO`** → digite **S** → Enter
3. Dois cliques em **`INICIAR`** de novo
4. **Não clique em Send em nada** até a gravação começar

Agora os IDs começam do 1 e batem com o roteiro.

---

## Deu erro?

| Apareceu | Faça |
|---|---|
| Janela dizendo **"FALTA INSTALAR O PYTHON"** | Ela abre o site sozinha. Baixe, instale **marcando "Add python.exe to PATH"**, reinicie o computador e clique no INICIAR de novo |
| Janela dizendo **"DEU ERRO AO BAIXAR AS BIBLIOTECAS"** | É falta de internet. Confira a conexão e clique no INICIAR de novo |
| Aviso do Windows sobre proteger o computador | **Mais informações** → **Executar assim mesmo** |
| No Postman: `Could not send request` | A API não está ligada. Dois cliques no INICIAR |
| Os IDs não são 1 e 2 | Use o **LIMPAR_BANCO** (seção acima) |
| O LIMPAR_BANCO diz que não conseguiu apagar | A API ainda está ligada. Feche a janela azul e tente de novo |

---

### Os outros arquivos (só se precisar)

- **[ROTEIRO_APRESENTACAO.md](ROTEIRO_APRESENTACAO.md)** — quem fala o quê no vídeo 👈 o importante
- [GUIA_POSTMAN.md](GUIA_POSTMAN.md) — o Postman explicado com calma, tela por tela
- [PASSO_A_PASSO.md](PASSO_A_PASSO.md) — como fazer pelos comandos, sem o INICIAR
- [README.md](README.md) — descrição do trabalho (entidades, relacionamentos, endpoints)
