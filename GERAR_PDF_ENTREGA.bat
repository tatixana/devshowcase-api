@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Gerar PDF de entrega - DevShowcase API
color 0B

echo.
echo  ============================================
echo     GERAR O PDF DE ENTREGA
echo  ============================================
echo.
echo  Use isto DEPOIS de subir o video no YouTube.
echo.
echo  Lembre: o video tem que estar como
echo  "Nao listado" nas configuracoes do YouTube.
echo.
echo  --------------------------------------------
echo  Cole aqui o link do video e aperte Enter:
echo  (para colar: clique com o botao direito)
echo.

set "link="
set /p link=  Link:

if "%link%"=="" goto sem_link

if not exist ".venv\Scripts\python.exe" goto sem_ambiente

echo.
echo  Preparando (pode demorar um pouco na primeira vez)...
".venv\Scripts\python.exe" -c "import reportlab" >nul 2>&1
if errorlevel 1 (
    ".venv\Scripts\python.exe" -m pip install -q reportlab
    if errorlevel 1 goto sem_internet
)

echo  Gerando...
".venv\Scripts\python.exe" gerar_pdf.py entrega "%link%"
if errorlevel 1 goto erro

color 0A
echo.
echo  ============================================
echo     PRONTO!
echo.
echo     O arquivo ENTREGA.pdf foi criado
echo     nesta mesma pasta.
echo.
echo     E esse arquivo que voces enviam
echo     na tarefa.
echo  ============================================
echo.
echo  Vou abrir o PDF para voces conferirem.
echo.
pause
start "" "ENTREGA.pdf"
goto fim


:sem_link
color 0E
echo.
echo  Nenhum link foi colado. Nada foi gerado.
echo.
echo  Tente de novo: copie o link do YouTube,
echo  de dois cliques aqui e cole com o botao direito.
echo.
pause
goto fim


:sem_ambiente
color 0E
echo.
echo  Precisa ligar a API pelo menos uma vez antes.
echo.
echo  1. De dois cliques em INICIAR e espere abrir.
echo  2. Feche a janela azul.
echo  3. De dois cliques aqui de novo.
echo.
pause
goto fim


:sem_internet
color 0C
echo.
echo  Nao consegui baixar o que precisa para gerar o PDF.
echo  Confira a internet e tente de novo.
echo.
pause
goto fim


:erro
color 0C
echo.
echo  Nao consegui gerar o PDF.
echo.
echo  Confira se o ENTREGA.pdf nao esta aberto
echo  em outro programa e tente de novo.
echo.
pause


:fim
