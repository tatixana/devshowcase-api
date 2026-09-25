@echo off
chcp 65001 >nul
cd /d "%~dp0"
title DevShowcase API
color 0B

echo.
echo  ============================================
echo     DevShowcase API
echo  ============================================
echo.

REM ---------- 1. Verificar se o Python esta instalado ----------
python --version >nul 2>&1
if errorlevel 1 goto sem_python

REM ---------- 2. Preparar o ambiente (so na primeira vez) ----------
if not exist ".venv\Scripts\python.exe" (
    echo  [1 de 3] Primeira vez aqui. Preparando tudo...
    echo           Isso demora 1 ou 2 minutos. Pode esperar.
    echo.
    python -m venv .venv
    if errorlevel 1 goto erro_venv
)

REM ---------- 3. Instalar as bibliotecas ----------
echo  [2 de 3] Conferindo as bibliotecas...
".venv\Scripts\python.exe" -m pip install -q -r requirements.txt
if errorlevel 1 goto erro_pip

REM ---------- 4. Ligar a API ----------
echo  [3 de 3] Ligando a API...
echo.
echo  ============================================
echo     PRONTO! O navegador vai abrir sozinho.
echo.
echo     NAO FECHE ESTA JANELA enquanto testar.
echo     Para desligar: feche esta janela.
echo  ============================================
echo.

start "" /min cmd /c "timeout /t 5 /nobreak >nul & start "" http://127.0.0.1:8000/docs"
".venv\Scripts\uvicorn.exe" app.main:app --reload
goto fim


:sem_python
color 0E
echo  ============================================
echo     FALTA INSTALAR O PYTHON
echo  ============================================
echo.
echo  O Python nao esta instalado neste computador.
echo.
echo  1. Vou abrir o site do Python no navegador.
echo  2. Baixe o botao amarelo "Download Python".
echo  3. Abra o arquivo baixado.
echo  4. IMPORTANTE: na primeira tela, marque a caixinha
echo     "Add python.exe to PATH" antes de clicar em Install.
echo  5. Quando terminar, REINICIE O COMPUTADOR.
echo  6. Depois e so dar dois cliques no INICIAR de novo.
echo.
pause
start "" https://www.python.org/downloads/
goto fim


:erro_venv
color 0C
echo.
echo  ============================================
echo     DEU ERRO AO PREPARAR
echo  ============================================
echo.
echo  Nao consegui criar o ambiente virtual.
echo.
echo  Tente assim:
echo  1. Apague a pasta .venv que esta aqui dentro.
echo  2. De dois cliques no INICIAR de novo.
echo.
echo  Se continuar dando erro, reinstale o Python
echo  marcando "Add python.exe to PATH".
echo.
pause
goto fim


:erro_pip
color 0C
echo.
echo  ============================================
echo     DEU ERRO AO BAIXAR AS BIBLIOTECAS
echo  ============================================
echo.
echo  Quase sempre e falta de internet.
echo.
echo  1. Confira se a internet esta funcionando.
echo  2. De dois cliques no INICIAR de novo.
echo.
pause
goto fim


:fim
