"""Gera os PDFs do trabalho.

Uso:
    python gerar_pdf.py roteiro                 -> ROTEIRO.pdf (falas do video)
    python gerar_pdf.py deploy                  -> GUIA_DEPLOY.pdf (passo a passo da nuvem)
    python gerar_pdf.py entrega LINK_YT         -> ENTREGA.pdf (etapa 1: 2 links)
    python gerar_pdf.py entrega LINK_YT LINK_API-> ENTREGA.pdf (etapa 2: 3 links)
"""

import sys

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

AZUL = HexColor("#1B4F8C")
CINZA = HexColor("#555555")
CLARO = HexColor("#EEF3F9")

GITHUB = "https://github.com/tatixana/devshowcase-api"

INTEGRANTES = [
    "LUSIMAR DAS SILVA DOS SANTOS",
    "LUCILENE COELHO DE SOUSA",
    "RAIMUNDA MARIA RIBEIRO DOS SANTOS",
    "TATILANE RIBEIRO DE ASSIS",
]

estilos = getSampleStyleSheet()


def s(nome, **kw):
    return ParagraphStyle(nome, parent=estilos["Normal"], **kw)


TITULO = s("titulo", fontName="Helvetica-Bold", fontSize=24, textColor=AZUL,
           alignment=TA_CENTER, spaceAfter=6, leading=28)
SUB = s("sub", fontSize=12, textColor=CINZA, alignment=TA_CENTER, spaceAfter=20)
H1 = s("h1", fontName="Helvetica-Bold", fontSize=14, textColor=AZUL,
       spaceBefore=16, spaceAfter=8)
TXT = s("txt", fontSize=11, leading=16, spaceAfter=6)
FALA = s("fala", fontSize=11, leading=16, leftIndent=14, spaceAfter=6,
         textColor=HexColor("#1A1A1A"), fontName="Helvetica-Oblique")
PEQ = s("peq", fontSize=9, textColor=CINZA, leading=13)
CODE = s("code", fontName="Courier", fontSize=8, leading=11,
         backColor=CLARO, borderPadding=6, spaceAfter=8)


def linha():
    return HRFlowable(width="100%", thickness=1, color=HexColor("#CCCCCC"),
                      spaceBefore=10, spaceAfter=10)


# ---------------------------------------------------------------- ENTREGA


def gerar_entrega(link_youtube, link_api=None):
    doc = SimpleDocTemplate(
        "ENTREGA.pdf", pagesize=A4,
        leftMargin=2.5 * cm, rightMargin=2.5 * cm,
        topMargin=1.8 * cm, bottomMargin=1.5 * cm,
        title="DevShowcase API - Entrega", author="Grupo DevShowcase API",
    )

    hist = [
        Paragraph("DevShowcase API", TITULO),
        Paragraph("Modelagem de domínio, persistência e endpoints básicos", SUB),
        linha(),
        Paragraph("Integrantes do grupo", H1),
    ]

    for nome in INTEGRANTES:
        hist.append(Paragraph("&bull; " + nome, TXT))

    hist += [
        Spacer(1, 10),
        Paragraph("Links da entrega", H1),
    ]

    def celula(rotulo, url):
        return [Paragraph(rotulo, TXT),
                Paragraph(f'<link href="{url}"><font color="#1B4F8C">{url}</font></link>', TXT)]

    linhas = [celula("<b>Repositório no GitHub</b><br/>(código-fonte)", GITHUB)]
    if link_api:
        linhas.append(celula(
            "<b>API em produção</b><br/>(para testes online)", link_api))
    linhas.append(celula(
        "<b>Vídeo da apresentação</b><br/>(YouTube, não listado)", link_youtube))

    tabela = Table(linhas, colWidths=[5.2 * cm, 10.3 * cm])
    tabela.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BACKGROUND", (0, 0), (0, -1), CLARO),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#CCCCCC")),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    hist.append(tabela)

    hist += [
        Spacer(1, 16),
        Paragraph("O que foi entregue", H1),
        Paragraph(
            "API REST feita em Python com FastAPI, guardando os dados em um banco "
            "relacional SQLite.", TXT),
        Spacer(1, 6),
        Paragraph("<b>Entidades:</b> Profile, Project, Technology e Feedback.", TXT),
        Paragraph("<b>Relacionamentos:</b> Profile 1:N Project &nbsp;|&nbsp; "
                  "Project N:N Technology &nbsp;|&nbsp; Project 1:N Feedback.", TXT),
        Spacer(1, 6),
        Paragraph("<b>Endpoints:</b>", TXT),
    ]

    endpoints = [
        "POST /api/profiles &ndash; cadastro de perfil com validações",
        "GET /api/profiles/{id} &ndash; buscar perfil por id",
        "POST /api/technologies &ndash; cadastro de tecnologia com validações",
        "GET /api/technologies &ndash; listagem de todas as tecnologias",
        "POST /api/projects &ndash; cadastro de projeto com validações",
        "GET /api/projects &ndash; listagem de projetos, com filtro por tecnologia e paginação",
    ]
    if link_api:
        endpoints += [
            "POST /api/projects/{id}/feedbacks &ndash; nota de 1 a 5 e comentário, "
            "com cálculo da nota média do projeto",
            "PUT /api/projects/{id}/upvote &ndash; incrementa as curtidas do projeto",
            "GET /api/projects/{id}/feedbacks &ndash; feedbacks de um projeto",
        ]
    hist.append(ListFlowable(
        [ListItem(Paragraph(e, TXT), leftIndent=18) for e in endpoints],
        bulletType="bullet", start="circle", leftIndent=12))

    if link_api:
        hist += [
            Spacer(1, 10),
            Paragraph("Tratamento de erros e documentação", H1),
            Paragraph(
                "A API possui um manipulador global de exceções: todos os erros saem "
                "no mesmo formato, em português, com os campos <b>erro</b>, "
                "<b>detalhe</b> e <b>codigo</b>. São tratados os erros 400, 404, 405, "
                "422 (validação) e 500 (erro inesperado), além de falhas de banco de "
                "dados. A documentação interativa fica no Swagger, em "
                "<b>/docs</b> do endereço da API em produção.", TXT),
            Spacer(1, 10),
            Paragraph("Deploy em produção", H1),
            Paragraph(
                "O banco de dados é um <b>PostgreSQL</b> provisionado na nuvem pelo "
                "Supabase. A API está publicada no <b>Render</b>, com deploy contínuo "
                "a partir do repositório no GitHub: a cada novo commit na branch main, "
                "o Render publica a versão nova automaticamente. As credenciais do "
                "banco não ficam no código: são lidas da variável de ambiente "
                "<b>DATABASE_URL</b>, configurada no painel do Render.", TXT),
        ]

    hist += [
        Spacer(1, 10),
        Paragraph(
            "As tecnologias usadas foram Python, FastAPI, SQLAlchemy, Pydantic "
            "e Uvicorn"
            + (", com PostgreSQL em produção e SQLite no desenvolvimento. "
               if link_api else ", com banco de dados SQLite. ")
            + "O repositório é público e possui arquivo .gitignore, que impede o "
            "envio do banco local, do ambiente virtual e de qualquer credencial.", TXT),
    ]

    doc.build(hist)
    print("ENTREGA.pdf gerado com sucesso.")


# ---------------------------------------------------------------- ROTEIRO


def bloco(quem, tempo, fala, acao):
    """Monta um bloco do roteiro: quem fala, o que fala e o que faz."""
    cab = Table(
        [[Paragraph(f"<b>{quem}</b>", TXT), Paragraph(tempo, PEQ)]],
        colWidths=[11.5 * cm, 4 * cm])
    cab.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CLARO),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    itens = [cab, Spacer(1, 5), Paragraph(f'"{fala}"', FALA)]
    if acao:
        itens.append(Paragraph(f"<b>O que fazer:</b> {acao}", PEQ))
    itens.append(Spacer(1, 12))
    return itens


def gerar_roteiro():
    doc = SimpleDocTemplate(
        "ROTEIRO.pdf", pagesize=A4,
        leftMargin=2.2 * cm, rightMargin=2.2 * cm,
        topMargin=2 * cm, bottomMargin=1.8 * cm,
        title="DevShowcase API - Roteiro do vídeo", author="Grupo DevShowcase API",
    )

    h = [
        Paragraph("Roteiro do vídeo", TITULO),
        Paragraph("DevShowcase API &nbsp;|&nbsp; duração: cerca de 7 minutos", SUB),
    ]

    # --- antes de comecar ---
    h += [
        Paragraph("Antes de começar a gravar", H1),
        Paragraph(
            "1. Feche a janela azul da API.<br/>"
            "2. Clique duas vezes em <b>LIMPAR_BANCO</b>, digite <b>S</b> e Enter.<br/>"
            "3. Clique duas vezes em <b>INICIAR</b> para ligar a API.<br/>"
            "4. Abra o Postman com as 8 requisições já montadas.<br/>"
            "5. Abra o GitHub em: " + GITHUB + "<br/>"
            "6. <b>Não cliquem em Send em nada</b> antes de começar a gravar.", TXT),
        Spacer(1, 6),
        Paragraph(
            "Quem compartilha a tela é quem está com a API e o Postman abertos. "
            "As outras podem pedir para clicar, ou cada uma clica na sua vez. "
            "Podem ler as falas, não precisa decorar.", PEQ),
        linha(),
    ]

    # --- parte 1 ---
    h.append(Paragraph("Parte 1 &ndash; Todas na câmera (0:00 a 0:40)", H1))
    h.append(Paragraph("Ainda <b>sem</b> compartilhar a tela. Cada uma liga a câmera "
                       "e fala o nome completo.", PEQ))
    h.append(Spacer(1, 8))
    for nome, prim in [("LUSIMAR", "Lusimar das Silva dos Santos"),
                       ("LUCILENE", "Lucilene Coelho de Sousa"),
                       ("RAIMUNDA", "Raimunda Maria Ribeiro dos Santos")]:
        h += bloco(nome, "10 segundos",
                   f"Olá, meu nome é {prim}.", None)
    h += bloco("TATILANE", "10 segundos",
               "Olá, meu nome é Tatilane Ribeiro de Assis. "
               "Vamos apresentar o nosso trabalho.",
               "Começar a compartilhar a tela.")

    h.append(PageBreak())

    # --- parte 2 ---
    h.append(Paragraph("Parte 2 &ndash; Explicando o projeto (0:40 a 2:00)", H1))
    h += bloco("LUSIMAR", "0:40 a 1:10",
               "Nosso projeto se chama DevShowcase API. A proposta é criar uma API "
               "para cadastrar perfis de desenvolvedores, os projetos que eles fizeram, "
               "as tecnologias usadas e os feedbacks recebidos. "
               "Usamos a linguagem Python com o FastAPI.",
               "Mostrar a página do projeto no GitHub.")
    h += bloco("LUSIMAR", "1:10 a 1:25",
               "Temos quatro entidades. O Profile é o perfil do desenvolvedor. "
               "O Project são os projetos cadastrados. A Technology são as tecnologias "
               "usadas. E o Feedback são as opiniões sobre os projetos.",
               "Descer a página até a tabela de Entidades.")
    h += bloco("LUCILENE", "1:25 a 1:40",
               "Um perfil pode ter vários projetos. Um projeto pode usar várias "
               "tecnologias, e uma tecnologia também pode estar em vários projetos. "
               "E um projeto pode receber vários feedbacks.",
               "Descer até a parte de Relacionamentos.")
    h += bloco("RAIMUNDA", "1:40 a 2:00",
               "Para salvar os dados usamos o SQLite, que é um banco de dados "
               "relacional simples. Ele fica neste arquivo aqui, e as tabelas são "
               "criadas sozinhas quando a API inicia. A API já está rodando aqui.",
               "Mostrar a pasta do projeto e a janela da API ligada.")

    h.append(PageBreak())

    # --- parte 3: postman ---
    h.append(Paragraph("Parte 3 &ndash; Demonstração no Postman (2:00 a 6:20)", H1))
    h.append(Paragraph("Esta é a parte mais importante do vídeo. "
                       "Mostrar a tela do Postman o tempo todo.", PEQ))
    h.append(Spacer(1, 8))

    h += bloco("LUSIMAR", "2:00 a 2:40",
               "Agora vamos demonstrar o funcionamento da nossa API usando o Postman. "
               "Primeiro vamos cadastrar um perfil. Usamos o método POST e enviamos os "
               "dados da Ana Silva. ... Como podemos ver, o perfil foi criado com "
               "sucesso. Ele recebeu o ID 1, e o status 201 significa que foi criado.",
               "Teste 1 &rarr; POST /api/profiles &rarr; clicar em Send.")
    h += bloco("LUCILENE", "2:40 a 3:05",
               "Agora vamos buscar esse perfil pelo ID. O número 1 no final do endereço "
               "é o ID do perfil. ... A API encontrou e mostrou os dados da Ana Silva, "
               "com o status 200.",
               "Teste 2 &rarr; GET /api/profiles/1 &rarr; Send.")
    h += bloco("LUCILENE", "3:05 a 3:50",
               "Em seguida vamos cadastrar as tecnologias. Primeiro o Python. ... "
               "Ele foi cadastrado com o ID 1. Agora o FastAPI. ... "
               "Esse recebeu o ID 2.",
               "Teste 3 (Python) &rarr; Send. Depois Teste 4 (FastAPI) &rarr; Send.")
    h += bloco("RAIMUNDA", "3:50 a 4:15",
               "Agora podemos listar as tecnologias cadastradas. ... "
               "Aparecem as duas: Python com ID 1 e FastAPI com ID 2.",
               "Teste 5 &rarr; GET /api/technologies &rarr; Send.")
    h += bloco("RAIMUNDA", "4:15 a 5:05",
               "Vamos cadastrar um projeto associado ao perfil e às tecnologias. "
               "Aqui no profile_id colocamos 1, que é o perfil da Ana Silva. "
               "E no technology_ids colocamos 1 e 2, que são o Python e o FastAPI. ... "
               "O projeto foi criado. E na resposta já aparece o perfil da Ana e as duas "
               "tecnologias. Isso mostra que os relacionamentos estão funcionando.",
               "Teste 6 &rarr; POST /api/projects. Apontar o mouse no profile_id e no "
               "technology_ids antes de clicar em Send.")
    h += bloco("TATILANE", "5:05 a 5:35",
               "Agora vamos listar os projetos cadastrados. ... "
               "Aparece o Sistema de Biblioteca, junto com a autora, Ana Silva, "
               "e as tecnologias que ele usa.",
               "Teste 7 &rarr; GET /api/projects &rarr; Send.")
    h += bloco("TATILANE", "5:35 a 6:20",
               "Também implementamos validações. Vamos enviar uma informação inválida "
               "de propósito: o título está vazio. ... Como podemos ver, a API "
               "identificou o problema e retornou um erro 422, avisando que o título é "
               "obrigatório. Então esse projeto não foi salvo no banco.",
               "Teste 8 &rarr; POST /api/projects com o título vazio &rarr; Send.")

    h.append(PageBreak())

    # --- parte 4 ---
    h.append(Paragraph("Parte 4 &ndash; GitHub e encerramento (6:20 a 7:00)", H1))
    h += bloco("TATILANE", "6:20 a 6:45",
               "O código-fonte também está disponível em um repositório público no "
               "GitHub. Aqui estão as pastas do projeto e o README, com as instruções "
               "para instalar e testar a API.",
               "Abrir no navegador: " + GITHUB)
    h += bloco("TATILANE e TODAS", "6:45 a 7:00",
               "Com isso finalizamos a demonstração da DevShowcase API. "
               "(todas juntas) Obrigada!",
               "Parar de compartilhar a tela. Todas ligam a câmera de novo.")

    # --- JSONs ---
    h += [
        linha(),
        Paragraph("Os JSONs usados no Postman", H1),
        Paragraph("Para conferir antes de gravar. Cole na aba Body, "
                  "marcando <b>raw</b> e <b>JSON</b>.", PEQ),
        Spacer(1, 8),
        Paragraph("<b>Teste 1</b> &ndash; POST http://127.0.0.1:8000/api/profiles", TXT),
        Paragraph(
            '{"name": "Ana Silva", "bio": "Desenvolvedora iniciante apaixonada por '
            'tecnologia.", "github_url": "https://github.com/anasilva", '
            '"linkedin_url": "https://linkedin.com/in/anasilva"}', CODE),
        Paragraph("<b>Teste 2</b> &ndash; GET http://127.0.0.1:8000/api/profiles/1", TXT),
        Spacer(1, 6),
        Paragraph("<b>Teste 3 e 4</b> &ndash; POST http://127.0.0.1:8000/api/technologies", TXT),
        Paragraph('{"name": "Python"}          e depois          {"name": "FastAPI"}', CODE),
        Paragraph("<b>Teste 5</b> &ndash; GET http://127.0.0.1:8000/api/technologies", TXT),
        Spacer(1, 6),
        Paragraph("<b>Teste 6</b> &ndash; POST http://127.0.0.1:8000/api/projects", TXT),
        Paragraph(
            '{"title": "Sistema de Biblioteca", "description": "API para gerenciamento '
            'de uma biblioteca.", "repository_url": '
            '"https://github.com/exemplo/sistema-biblioteca", "demo_url": '
            '"https://exemplo.com", "profile_id": 1, "technology_ids": [1, 2]}', CODE),
        Paragraph("<b>Teste 7</b> &ndash; GET http://127.0.0.1:8000/api/projects", TXT),
        Spacer(1, 6),
        Paragraph("<b>Teste 8</b> (erro de propósito) &ndash; POST http://127.0.0.1:8000/api/projects", TXT),
        Paragraph(
            '{"title": "", "description": "Projeto inválido", "profile_id": 999, '
            '"technology_ids": [999]}', CODE),
    ]

    doc.build(h)
    print("ROTEIRO.pdf gerado com sucesso.")


# ---------------------------------------------------------------- DEPLOY


PASSO = s("passo", fontName="Helvetica-Bold", fontSize=12,
          textColor=HexColor("#1A1A1A"), spaceBefore=12, spaceAfter=4)
AVISO = s("aviso", fontSize=10, leading=14, leftIndent=10, spaceAfter=8,
          textColor=HexColor("#8A4B00"), backColor=HexColor("#FFF6E5"),
          borderPadding=6)


def gerar_deploy():
    doc = SimpleDocTemplate(
        "GUIA_DEPLOY.pdf", pagesize=A4,
        leftMargin=2.2 * cm, rightMargin=2.2 * cm,
        topMargin=2 * cm, bottomMargin=1.8 * cm,
        title="DevShowcase API - Guia de deploy", author="Grupo DevShowcase API",
    )

    h = [
        Paragraph("Guia de deploy", TITULO),
        Paragraph("Publicar a DevShowcase API no Render", SUB),
        Paragraph(
            "O banco de dados PostgreSQL no <b>Supabase</b> já está criado e com as "
            "tabelas prontas. Falta publicar a API no <b>Render</b>, que é gratuito "
            "e não pede cartão de crédito. Leva uns 15 minutos.", TXT),
        Paragraph(
            "Faça na ordem: primeiro pegue a senha do banco (Parte 1), depois publique "
            "a API (Parte 2). A Parte 2 precisa da senha da Parte 1.", PEQ),
        linha(),

        # ------------------------------------------------ parte 1
        Paragraph("Parte 1 &ndash; O banco no Supabase (JÁ ESTÁ PRONTO)", H1),
        Paragraph(
            "O banco de dados já foi criado e configurado. Não precisa fazer nada "
            "aqui, só pegar a senha no Passo 1.", TXT),
        Spacer(1, 4),
        Paragraph(
            "&bull; <b>Projeto:</b> devshowcase-api<br/>"
            "&bull; <b>Região:</b> South America (São Paulo)<br/>"
            "&bull; <b>Banco:</b> PostgreSQL 17<br/>"
            "&bull; <b>Tabelas criadas:</b> profiles, technologies, projects, "
            "feedbacks e project_technologies<br/>"
            "&bull; <b>Segurança:</b> RLS ligado, bloqueando o acesso direto às "
            "tabelas por fora da nossa API", TXT),

        Paragraph("Passo 1. Pegar a senha do banco", PASSO),
        Paragraph(
            "A senha do banco é secreta e não fica guardada em lugar nenhum do "
            "projeto. Vocês precisam gerar uma nova:", TXT),
        Paragraph(
            "1. Entre em <b>supabase.com</b> e abra o projeto <b>devshowcase-api</b>.<br/>"
            "2. No menu da esquerda, clique na engrenagem <b>Settings</b>.<br/>"
            "3. Clique em <b>Database</b>.<br/>"
            "4. Procure <b>Database password</b> e clique em "
            "<b>Reset database password</b>.<br/>"
            "5. Clique em <b>Generate a password</b> e depois em "
            "<b>Reset password</b>.<br/>"
            "6. <b>Copie a senha para um bloco de notas.</b> Ela não aparece de novo.", TXT),

        Paragraph("Passo 2. Montar o endereço de conexão", PASSO),
        Paragraph(
            "Ainda no Supabase, clique no botão <b>Connect</b> (no topo da página).", TXT),
        Paragraph(
            "Procure a opção <b>Session pooler</b> e copie o endereço que aparece "
            "embaixo dela. É parecido com isto:", TXT),
        Paragraph(
            "postgresql://postgres.lksrooimwlcduscjtrdk:[YOUR-PASSWORD]"
            "@aws-0-sa-east-1.pooler.supabase.com:5432/postgres", CODE),
        Paragraph(
            "Troque <b>[YOUR-PASSWORD]</b> (apagando também os colchetes) pela senha "
            "que você copiou no Passo 1. Guarde esse endereço completo: ele é a "
            "<b>DATABASE_URL</b> e vai ser usado no Passo 5.", TXT),
        Paragraph(
            "Use o <b>Session pooler</b>, não o Direct connection. O Render não "
            "consegue se conectar pelo Direct connection.", AVISO),
        Paragraph(
            "Essa senha é uma credencial: não coloquem em nenhum arquivo do projeto, "
            "não mandem para o GitHub e não deixem aparecer na tela durante o vídeo.", AVISO),

        PageBreak(),

        # ------------------------------------------------ parte 2
        Paragraph("Parte 2 &ndash; Publicar a API no Render", H1),

        Paragraph("Passo 3. Criar a conta no Render", PASSO),
        Paragraph(
            "Entre em <b>render.com</b> e clique em <b>Get Started</b>. "
            "Escolha entrar com o <b>GitHub</b>, usando a conta da Tatilane "
            "(a mesma dona do repositório).", TXT),

        Paragraph("Passo 4. Criar o serviço da API", PASSO),
        Paragraph(
            "No painel, clique em <b>Add new</b> &rarr; <b>Web Service</b>.", TXT),
        Paragraph(
            "Vai aparecer a lista dos repositórios do GitHub. Procure "
            "<b>devshowcase-api</b> e clique em <b>Connect</b>.", TXT),
        Paragraph(
            "Se o repositório não aparecer, clique em <b>Configure account</b> e "
            "autorize o Render a ver os repositórios.", PEQ),
        Paragraph(
            "O projeto já tem um arquivo <b>render.yaml</b>, então o Render preenche "
            "quase tudo sozinho. Confira se ficou assim:", TXT),
        Paragraph(
            "&bull; <b>Name:</b> devshowcase-api<br/>"
            "&bull; <b>Branch:</b> main<br/>"
            "&bull; <b>Build Command:</b> pip install -r requirements.txt<br/>"
            "&bull; <b>Start Command:</b> uvicorn app.main:app --host 0.0.0.0 --port $PORT<br/>"
            "&bull; <b>Instance Type:</b> Free", TXT),

        Paragraph("Passo 5. Colocar o endereço do banco", PASSO),
        Paragraph(
            "Ainda na mesma tela, procure <b>Environment Variables</b> "
            "(ou <b>Advanced</b> &rarr; <b>Add Environment Variable</b>) e adicione:", TXT),
        Paragraph(
            "&bull; <b>Key (nome):</b> DATABASE_URL<br/>"
            "&bull; <b>Value (valor):</b> o endereço completo que você montou no Passo 2", TXT),
        Paragraph(
            "É assim que as credenciais ficam fora do código: o endereço do banco e a "
            "senha ficam só aqui, no painel do Render.", PEQ),

        Paragraph("Passo 6. Publicar", PASSO),
        Paragraph(
            "Clique em <b>Deploy Web Service</b> e espere. A primeira publicação "
            "demora de 3 a 5 minutos. Vocês vão ver o texto do build rolando na tela.", TXT),
        Paragraph(
            "Deu certo quando aparecer <b>Live</b> em verde no topo da página, e no "
            "final do log aparecer <b>Application startup complete</b>.", TXT),

        PageBreak(),

        # ------------------------------------------------ parte 3
        Paragraph("Parte 3 &ndash; Conferir se funcionou", H1),
        Paragraph(
            "No topo da página do Render aparece o endereço público da API. "
            "É parecido com:", TXT),
        Paragraph("https://devshowcase-api.onrender.com", CODE),
        Paragraph(
            "<b>Esse é o link da API em produção que vai no PDF de entrega.</b> "
            "Copie e guarde.", TXT),
        Spacer(1, 6),
        Paragraph("Abra no navegador, um de cada vez:", TXT),
        Paragraph(
            "&bull; <b>o endereço sozinho</b> &rarr; tem que aparecer "
            "a mensagem &quot;DevShowcase API está funcionando&quot;<br/>"
            "&bull; <b>o endereço + /docs</b> &rarr; abre o Swagger com todos os "
            "endpoints<br/>"
            "&bull; <b>o endereço + /api/technologies</b> &rarr; tem que aparecer "
            "uma lista vazia: [ ]", TXT),
        Paragraph(
            "A lista vazia é o certo: o banco na nuvem começa sem nada. "
            "Os cadastros do computador de vocês não vão para lá.", PEQ),
        Spacer(1, 6),
        Paragraph(
            "Agora é só usar esse endereço no Postman no lugar de "
            "http://127.0.0.1:8000, e cadastrar os dados da demonstração direto "
            "na nuvem.", TXT),

        Paragraph("Deploy contínuo (já vem ligado)", H1),
        Paragraph(
            "A partir de agora, toda vez que o código mudar no GitHub na branch main, "
            "o Render publica a versão nova sozinho. Não precisa mexer em mais nada. "
            "Dá para ver isso na aba <b>Events</b> do Render.", TXT),

        Paragraph("Se der errado", H1),
    ]

    problemas = [
        ["O que aparece", "O que fazer"],
        ["No Render: <b>Build failed</b>",
         "Abra o log e procure a linha em vermelho. Quase sempre é o "
         "requirements.txt. Confira se o arquivo foi enviado para o GitHub."],
        ["No Render: <b>Deploy failed</b> com erro de conexão ao banco",
         "A DATABASE_URL está errada. Confira se trocou [YOUR-PASSWORD] pela senha "
         "de verdade e se usou o <b>Session pooler</b> (não o Direct connection)."],
        ["A primeira visita demora muito",
         "Normal no plano gratuito: a API dorme depois de 15 minutos parada e leva "
         "uns 50 segundos para acordar. Antes de gravar o vídeo, abra o endereço e "
         "espere carregar."],
        ["<b>password authentication failed</b>",
         "A senha do banco está errada. Gere outra em Settings &rarr; Database &rarr; "
         "Reset database password e atualize a DATABASE_URL no Render."],
        ["Mudei o código e a API não mudou",
         "Confira se o commit foi enviado com git push. Veja a aba Events do Render."],
    ]
    tabela = Table(
        [[Paragraph(f"<b>{c}</b>" if i == 0 else c, PEQ) for c in linha_]
         for i, linha_ in enumerate(problemas)],
        colWidths=[5.5 * cm, 10 * cm])
    tabela.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (-1, 0), CLARO),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#CCCCCC")),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    h.append(tabela)

    doc.build(h)
    print("GUIA_DEPLOY.pdf gerado com sucesso.")


if __name__ == "__main__":
    comando = sys.argv[1] if len(sys.argv) > 1 else "roteiro"

    if comando == "entrega":
        if len(sys.argv) < 3 or not sys.argv[2].strip():
            print("Falta o link do YouTube.")
            sys.exit(1)
        link_api = sys.argv[3].strip() if len(sys.argv) > 3 else None
        gerar_entrega(sys.argv[2].strip(), link_api or None)
    elif comando == "deploy":
        gerar_deploy()
    else:
        gerar_roteiro()
