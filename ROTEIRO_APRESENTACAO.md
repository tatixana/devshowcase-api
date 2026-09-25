# Roteiro da Apresentação — DevShowcase API

**Duração total:** cerca de 7 minutos.
**Foco:** mostrar a API funcionando no **Postman**.

## Como organizar a gravação

- A gravação pode ser feita numa chamada (Google Meet, Teams, Zoom) com a opção de gravar.
- **Um único computador roda a API e o Postman** (sugestão: o da Tatilane). A dona desse computador compartilha a tela durante toda a demonstração.
- Quem está falando pode pedir: *"pode clicar em Send"*, e quem compartilha clica.
  Se estiverem juntas no mesmo lugar, cada uma pode clicar na sua vez.
- Deixe as 8 requisições **já montadas e salvas** no Postman, uma em cada aba (ver [GUIA_POSTMAN.md](GUIA_POSTMAN.md)).
  Assim, durante o vídeo, é só clicar na aba e em **Send**.
- Falem com calma. Não precisa decorar: pode ler a fala.

## Divisão

| Integrante | O que faz |
|---|---|
| **Lusimar** | Apresentação, introdução do projeto, entidades, Teste 1 (criar Profile) |
| **Lucilene** | Apresentação, relacionamentos, Teste 2 (buscar Profile), Testes 3 e 4 (Python e FastAPI) |
| **Raimunda** | Apresentação, banco SQLite e estrutura, Teste 5 (listar Technologies), Teste 6 (criar Project) |
| **Tatilane** | Apresentação, Teste 7 (listar Projects), Teste 8 (validação), GitHub e encerramento |

---

## PARTE 1 — Apresentação na câmera (0:00 – 0:40)

**Na tela:** as quatro integrantes com a **webcam ligada**. Ainda **sem** compartilhar a tela.

| Tempo | Integrante | Fala sugerida | Ação |
|---|---|---|---|
| 0:00 – 0:10 | **Lusimar** | "Olá, meu nome é Lusimar das Silva dos Santos." | Aparece na câmera. |
| 0:10 – 0:20 | **Lucilene** | "Olá, meu nome é Lucilene Coelho de Sousa." | Aparece na câmera. |
| 0:20 – 0:30 | **Raimunda** | "Olá, meu nome é Raimunda Maria Ribeiro dos Santos." | Aparece na câmera. |
| 0:30 – 0:40 | **Tatilane** | "Olá, meu nome é Tatilane Ribeiro de Assis. Vamos apresentar o nosso trabalho." | Aparece na câmera e **começa a compartilhar a tela**. |

---

## PARTE 2 — O projeto (0:40 – 1:10)

**Integrante:** Lusimar
**Na tela:** o README do projeto aberto no GitHub (ou no VS Code).
**Ação:** apenas mostrar a tela, sem clicar em nada.
**Duração:** 30 segundos.

**Fala sugerida:**
> "Nosso projeto se chama DevShowcase API. A proposta é criar uma API para cadastrar perfis de desenvolvedores, os projetos que eles fizeram, as tecnologias usadas e os feedbacks recebidos.
> Usamos a linguagem Python com o FastAPI para criar a API."

---

## PARTE 3 — Entidades e relacionamentos (1:10 – 1:40)

**Na tela:** a seção **Entidades** e **Relacionamentos** do README (tem o desenho das ligações).

### 1:10 – 1:25 — Entidades

**Integrante:** Lusimar
**Ação:** rolar a tela até a tabela de Entidades.
**Duração:** 15 segundos.

> "Temos quatro entidades. O Profile representa o perfil do desenvolvedor. O Project representa os projetos cadastrados. A Technology representa as tecnologias utilizadas, e o Feedback representa as opiniões sobre os projetos."

### 1:25 – 1:40 — Relacionamentos

**Integrante:** Lucilene
**Ação:** rolar até a parte de Relacionamentos.
**Duração:** 15 segundos.

> "Um perfil pode ter vários projetos. Um projeto pode usar várias tecnologias, e uma tecnologia também pode estar em vários projetos. E um projeto pode receber vários feedbacks."

---

## PARTE 4 — Banco SQLite e estrutura (1:40 – 2:00)

**Integrante:** Raimunda
**Na tela:** a pasta do projeto aberta no VS Code (mostrando `app/`, `models.py`, `schemas.py`, `routers/` e o arquivo `devshowcase.db`), e depois o terminal com a API rodando.
**Ação:** passar o mouse sobre as pastas e arquivos enquanto fala.
**Duração:** 20 segundos.

> "Para salvar os dados, usamos o SQLite, que é um banco de dados relacional simples e adequado para esse projeto. Ele fica neste arquivo, o devshowcase.db, e as tabelas são criadas sozinhas quando a API inicia.
> O código está organizado em pastas: os models são as tabelas, os schemas cuidam das validações, e os routers têm os endpoints. A API já está rodando aqui no terminal."

---

## PARTE 5 — Demonstração no Postman (2:00 – 6:20)

**Na tela:** o Postman, o tempo todo.

**Abertura** (Lusimar, 2:00 – 2:10):
> "Agora vamos demonstrar o funcionamento da nossa API utilizando o Postman."

### TESTE 1 — Criar Profile (2:10 – 2:40)

- **Integrante:** Lusimar
- **Ação:** abrir a aba do Teste 1 → mostrar o método **POST**, a URL `http://127.0.0.1:8000/api/profiles` e o JSON no Body → clicar em **Send**.
- **Na tela:** resposta com `"id": 1`, `"name": "Ana Silva"` e o status **201 Created**.
- **Duração:** 30 segundos.

> "Primeiro vamos cadastrar um perfil. Usamos o método POST e enviamos os dados da Ana Silva: nome, bio, GitHub e LinkedIn.
> *(clica em Send)*
> Como podemos ver, o perfil foi criado com sucesso. Ele recebeu o ID 1, e o status 201 significa que foi criado."

### TESTE 2 — Buscar Profile (2:40 – 3:05)

- **Integrante:** Lucilene
- **Ação:** abrir a aba do Teste 2 → mostrar **GET** e a URL `http://127.0.0.1:8000/api/profiles/1` → **Send**.
- **Na tela:** os dados da Ana Silva e o status **200 OK**.
- **Duração:** 25 segundos.

> "Agora vamos buscar esse perfil pelo ID. Usamos o método GET, e o número 1 no final do endereço é o ID do perfil.
> *(Send)*
> A API encontrou o perfil e mostrou os dados da Ana Silva, com o status 200, que quer dizer que deu certo."

### TESTE 3 — Cadastrar Python (3:05 – 3:30)

- **Integrante:** Lucilene
- **Ação:** aba do Teste 3 → **POST** `http://127.0.0.1:8000/api/technologies` com `{"name": "Python"}` → **Send**.
- **Na tela:** `{"id": 1, "name": "Python"}` e **201 Created**.
- **Duração:** 25 segundos.

> "Em seguida vamos cadastrar as tecnologias. Primeiro o Python.
> *(Send)*
> O Python foi cadastrado com o ID 1."

### TESTE 4 — Cadastrar FastAPI (3:30 – 3:50)

- **Integrante:** Lucilene
- **Ação:** aba do Teste 4 → mesmo endereço, com `{"name": "FastAPI"}` → **Send**.
- **Na tela:** `{"id": 2, "name": "FastAPI"}` e **201 Created**.
- **Duração:** 20 segundos.

> "Agora o FastAPI.
> *(Send)*
> Ele recebeu o ID 2."

### TESTE 5 — Listar Technologies (3:50 – 4:15)

- **Integrante:** Raimunda
- **Ação:** aba do Teste 5 → **GET** `http://127.0.0.1:8000/api/technologies` → **Send**.
- **Na tela:** a lista com Python e FastAPI e **200 OK**.
- **Duração:** 25 segundos.

> "Agora podemos listar as tecnologias cadastradas.
> *(Send)*
> Aparecem as duas: Python com ID 1 e FastAPI com ID 2."

### TESTE 6 — Criar Project (4:15 – 5:05)

- **Integrante:** Raimunda
- **Ação:** aba do Teste 6 → **POST** `http://127.0.0.1:8000/api/projects` → mostrar o JSON, **apontando com o mouse** para `profile_id` e `technology_ids` → **Send** → rolar a resposta até `profile` e `technologies`.
- **Na tela:** o projeto "Sistema de Biblioteca" com o perfil da Ana Silva e as tecnologias Python e FastAPI, status **201 Created**.
- **Duração:** 50 segundos.

> "Vamos cadastrar um projeto associado ao perfil e às tecnologias. O projeto se chama Sistema de Biblioteca.
> Aqui no profile_id colocamos 1, que é o perfil da Ana Silva. E no technology_ids colocamos 1 e 2, que são o Python e o FastAPI.
> *(Send)*
> O projeto foi criado. E olhem: na resposta já aparece o perfil da Ana e as duas tecnologias. Isso mostra que os relacionamentos estão funcionando."

### TESTE 7 — Listar Projects (5:05 – 5:35)

- **Integrante:** Tatilane
- **Ação:** aba do Teste 7 → **GET** `http://127.0.0.1:8000/api/projects` → **Send**.
- **Na tela:** a lista com o projeto, o perfil e as tecnologias, **200 OK**.
- **Duração:** 30 segundos.

> "Agora vamos listar os projetos cadastrados.
> *(Send)*
> Aparece o Sistema de Biblioteca, junto com a autora, Ana Silva, e as tecnologias que ele usa."

### TESTE 8 — Validação com erro (5:35 – 6:20)

- **Integrante:** Tatilane
- **Ação:** aba do Teste 8 → **POST** `http://127.0.0.1:8000/api/projects` com o JSON inválido (título vazio) → **Send**.
  *(Opcional, se sobrar tempo: aba do Teste 8B → Send → mostrar o erro 404.)*
- **Na tela:** status **422** e a mensagem `"Este campo é obrigatório e não pode ficar vazio."` no campo `title`.
- **Duração:** 45 segundos.

> "Também implementamos validações. Vamos enviar uma informação inválida propositalmente: o título está vazio, e o perfil e a tecnologia 999 não existem.
> *(Send)*
> Como podemos ver, a API identificou o problema e retornou um erro 422, avisando que o título é obrigatório. Então esse projeto não foi salvo.
> *(Opcional — Teste 8B)* E se o título estiver certo, mas o perfil não existir, a API responde com o erro 404, dizendo que o perfil não foi encontrado."

---

## PARTE 6 — GitHub e encerramento (6:20 – 7:00)

### 6:20 – 6:45 — GitHub

- **Integrante:** Tatilane
- **Ação:** abrir o navegador na página do repositório no GitHub e rolar até o README.
- **Na tela:** o repositório público `devshowcase-api` com as pastas e o README.
- **Duração:** 25 segundos.

> "O código-fonte também está disponível em um repositório público no GitHub. Aqui estão as pastas do projeto e o README, com as instruções para instalar e testar a API."

### 6:45 – 7:00 — Encerramento

- **Integrante:** Tatilane (e depois todas)
- **Ação:** parar de compartilhar a tela. Todas ligam a câmera.
- **Na tela:** as quatro integrantes na webcam.
- **Duração:** 15 segundos.

> **Tatilane:** "Com isso finalizamos a demonstração da DevShowcase API."
> **Todas juntas:** "Obrigada!"

---

## Resumo do tempo

| Parte | Tempo | Quem |
|---|---|---|
| Apresentação na câmera | 0:00 – 0:40 | Todas |
| O projeto | 0:40 – 1:10 | Lusimar |
| Entidades / Relacionamentos | 1:10 – 1:40 | Lusimar / Lucilene |
| SQLite e estrutura | 1:40 – 2:00 | Raimunda |
| Postman — Testes 1 a 8 | 2:00 – 6:20 | Lusimar → Lucilene → Raimunda → Tatilane |
| GitHub e encerramento | 6:20 – 7:00 | Tatilane e todas |

---

## Antes de gravar

- [ ] Webcam funcionando.
- [ ] Microfone funcionando.
- [ ] API iniciada.
- [ ] Terminal aberto.
- [ ] Postman aberto.
- [ ] GitHub aberto.
- [ ] URLs preparadas.
- [ ] JSONs preparados.
- [ ] Requisições testadas antes da gravação.
- [ ] IDs conferidos.
- [ ] Banco preparado.
- [ ] Não fechar o terminal durante a apresentação.

### IMPORTANTE

**Os IDs podem não ser 1 e 2 se o banco já possuir registros de testes.**

Se vocês treinarem antes (o que é recomendado!), o banco vai guardar esses cadastros de treino.
Na hora de gravar, o perfil da Ana Silva poderia ficar com ID 2 ou 3, e o Python e o FastAPI com IDs diferentes — e além disso a API **não deixa cadastrar Python e FastAPI de novo** (ela responde que a tecnologia já existe).

Por isso, **logo antes de gravar, comece com um banco novo:**

1. No terminal onde a API está rodando, aperte **Ctrl + C** para parar a API.
2. Abra a pasta do projeto `devshowcase-api` no Explorador de Arquivos.
3. Encontre o arquivo **`devshowcase.db`**, clique com o botão direito e escolha **Excluir**.
   (Ou, no terminal, digite: `del devshowcase.db`)
4. Inicie a API de novo:
   ```bash
   uvicorn app.main:app --reload
   ```
5. Um banco novo e vazio é criado sozinho. Agora os IDs começam do **1** de novo.

> Não abra o `devshowcase.db` em outro programa enquanto a API está rodando.
> Depois de apagar o banco, **não clique em Send** em nenhuma requisição até começar a gravar.
