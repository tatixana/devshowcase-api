@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Limpar banco - DevShowcase API
color 0E

echo.
echo  ============================================
echo     LIMPAR O BANCO DE DADOS
echo  ============================================
echo.
echo  Isso apaga TODOS os cadastros de teste.
echo  Os IDs voltam a comecar do 1.
echo.
echo  Use isto logo ANTES de gravar o video.
echo.
echo  ATENCAO: feche a janela da API antes
echo  (aquela azul que fica aberta).
echo.

if not exist "devshowcase.db" goto ja_limpo

set /p resposta=  Pode apagar? Digite S e aperte Enter:
if /i not "%resposta%"=="S" goto cancelado

del "devshowcase.db" >nul 2>&1
if exist "devshowcase.db" goto em_uso

color 0A
echo.
echo  ============================================
echo     PRONTO! Banco limpo.
echo.
echo     Agora de dois cliques no INICIAR
echo     e os IDs vao comecar do 1.
echo  ============================================
echo.
pause
goto fim


:ja_limpo
color 0A
echo  O banco ja esta limpo. Nao precisa fazer nada.
echo.
echo  Pode dar dois cliques no INICIAR:
echo  os IDs vao comecar do 1.
echo.
pause
goto fim


:em_uso
color 0C
echo.
echo  NAO CONSEGUI APAGAR.
echo.
echo  A API ainda esta ligada.
echo  Feche a janela azul da API e tente de novo.
echo.
pause
goto fim


:cancelado
echo.
echo  Cancelado. Nada foi apagado.
echo.
pause


:fim
