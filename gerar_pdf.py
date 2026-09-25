"""Gera os PDFs de entrega do trabalho.

Uso:
    python gerar_pdf.py roteiro          -> cria ROTEIRO.pdf
    python gerar_pdf.py entrega LINK     -> cria ENTREGA.pdf com o link do YouTube
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


def gerar_entrega(link_youtube):
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

    tabela = Table(
        [
            [Paragraph("<b>Repositório no GitHub</b><br/>(código-fonte)", TXT),
             Paragraph(f'<link href="{GITHUB}"><font color="#1B4F8C">{GITHUB}</font></link>', TXT)],
            [Paragraph("<b>Vídeo da apresentação</b><br/>(YouTube, não listado)", TXT),
             Paragraph(f'<link href="{link_youtube}"><font color="#1B4F8C">{link_youtube}</font></link>', TXT)],
        ],
        colWidths=[5.2 * cm, 10.3 * cm],
    )
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
        "GET /api/projects &ndash; listagem de projetos",
    ]
    hist.append(ListFlowable(
        [ListItem(Paragraph(e, TXT), leftIndent=18) for e in endpoints],
        bulletType="bullet", start="circle", leftIndent=12))

    hist += [
        Spacer(1, 10),
        Paragraph(
            "As tecnologias usadas foram Python, FastAPI, SQLAlchemy, Pydantic, "
            "SQLite e Uvicorn. O repositório é público e possui arquivo .gitignore, "
            "que impede o envio do banco de dados local e do ambiente virtual.", TXT),
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


if __name__ == "__main__":
    comando = sys.argv[1] if len(sys.argv) > 1 else "roteiro"

    if comando == "entrega":
        if len(sys.argv) < 3 or not sys.argv[2].strip():
            print("Falta o link do YouTube.")
            sys.exit(1)
        gerar_entrega(sys.argv[2].strip())
    else:
        gerar_roteiro()
