# Passo a passo — Como rodar a DevShowcase API no Windows

Guia para quem está começando. Faça um passo de cada vez e só vá para o próximo quando o anterior der certo.

---

## Passo 0 — Pegar o projeto

**Opção A — pelo GitHub (sem Git):**
1. Abra a página do repositório no GitHub.
2. Clique no botão verde **Code** → **Download ZIP**.
3. Extraia o ZIP (botão direito → **Extrair tudo**).

**Opção B — com Git:**

```bash
git clone https://github.com/USUARIO/devshowcase-api.git
```

(troque `USUARIO` pelo usuário do GitHub onde o projeto foi publicado)

---

## Passo 1 — Abrir o terminal na pasta do projeto

1. Abra a pasta `devshowcase-api` no Explorador de Arquivos.
   Dentro dela você deve ver a pasta `app` e o arquivo `requirements.txt`.
2. Clique na barra de endereço lá em cima, apague o que estiver escrito, digite `cmd` e aperte **Enter**.
3. Vai abrir uma janela preta (o terminal) já dentro da pasta certa.

> Também dá para usar o terminal do VS Code: **Terminal → New Terminal**.

---

## Passo 2 — Verificar o Python

```bash
python --version
```

Deve aparecer algo como `Python 3.13.x`. Qualquer versão **3.10 ou mais nova** funciona.

Se aparecer erro, veja **"SE ALGO DER ERRADO"** no final.

---

## Passo 3 — Criar o ambiente virtual (só na primeira vez)

O ambiente virtual é uma "caixinha" onde ficam as bibliotecas deste projeto.

```bash
python -m venv .venv
```

Vai aparecer uma pasta nova chamada `.venv`. Isso é normal.

---

## Passo 4 — Ativar o ambiente virtual (sempre que abrir um terminal novo)

```bash
.venv\Scripts\activate
```

Deu certo quando aparecer **`(.venv)`** no começo da linha do terminal:

```
(.venv) C:\...\devshowcase-api>
```

---

## Passo 5 — Instalar as dependências (só na primeira vez)

```bash
pip install -r requirements.txt
```

Espere terminar. No final aparece `Successfully installed ...`.

---

## Passo 6 — Iniciar a API

```bash
uvicorn app.main:app --reload
```

Deu certo quando aparecer:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

Nesse momento o arquivo **`devshowcase.db`** (o banco de dados) é criado na pasta do projeto, com todas as tabelas.

> ⚠️ **Não feche esse terminal.** Enquanto ele estiver aberto, a API está funcionando.
> Para parar a API: clique no terminal e aperte **Ctrl + C**.

---

## Passo 7 — Conferir no navegador

Abra o navegador e acesse:

- http://127.0.0.1:8000 → deve aparecer `{"message":"DevShowcase API está funcionando"}`
- http://127.0.0.1:8000/docs → abre o **Swagger**, uma página com todos os endpoints da API.

No Swagger também dá para testar: clique em um endpoint → **Try it out** → preencha → **Execute**.

---

## Passo 8 — Abrir o Postman

1. Se ainda não tiver, baixe em https://www.postman.com/downloads/ e instale.
2. Abra o Postman. Se ele pedir para criar conta, você pode criar uma conta gratuita
   (ou procurar a opção de continuar sem conta, se aparecer).
3. Clique no **+** para abrir uma nova requisição.
4. Siga o guia **[GUIA_POSTMAN.md](GUIA_POSTMAN.md)**, do Teste 1 ao Teste 8.

---

## Resumo — dia a dia

Da segunda vez em diante, só precisa de:

```bash
.venv\Scripts\activate
uvicorn app.main:app --reload
```

---

## Começar com o banco vazio (IDs a partir do 1)

1. Pare a API: **Ctrl + C** no terminal.
2. Apague o arquivo **`devshowcase.db`** da pasta do projeto (botão direito → Excluir).
   Ou, no terminal: `del devshowcase.db`
3. Inicie a API de novo: `uvicorn app.main:app --reload`

Um banco novo e vazio é criado automaticamente.

---

## SE ALGO DER ERRADO

| O que aparece | O que fazer |
|---|---|
| `'python' não é reconhecido...` ou `Python não foi encontrado; executar sem argumentos para instalar do Microsoft Store` | O Python não está instalado. Baixe em https://www.python.org/downloads/ e, **na primeira tela do instalador, marque "Add python.exe to PATH"**. Depois feche e abra o terminal de novo. |
| `python --version` mostra versão 3.9 ou mais antiga | Instale uma versão nova pelo site acima. |
| No PowerShell: `...activate.ps1 não pode ser carregado porque a execução de scripts foi desabilitada` | Use o terminal **cmd** (Passo 1), ou rode uma vez: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` e confirme com `S`. |
| `'uvicorn' não é reconhecido...` ou `No module named ...` | O ambiente virtual não está ativado (falta `(.venv)` no começo da linha). Rode `.venv\Scripts\activate` e depois `pip install -r requirements.txt`. |
| `Error loading ASGI app. Could not import module "app.main"` | O terminal está na pasta errada. Entre na pasta `devshowcase-api` (a que tem a pasta `app` dentro). |
| `[WinError 10048]` / `address already in use` | Já existe uma API rodando em outro terminal. Feche o outro terminal ou aperte Ctrl + C nele. |
| Mudei o código e a API não atualizou | Aperte **Ctrl + C** e inicie de novo com `uvicorn app.main:app --reload`. |
| Postman: `Could not send request` / `ECONNREFUSED` | A API não está rodando. Volte ao Passo 6. |
| Os IDs não são 1 e 2 | O banco já tinha dados. Use os IDs que apareceram ou comece com o banco vazio (seção acima). |
| `pip install` com erro de internet/SSL | Confira a internet e tente de novo. |
