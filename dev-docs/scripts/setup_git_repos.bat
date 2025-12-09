@echo off
REM ============================================
REM Script para crear repositorios en GitHub
REM ============================================

echo.
echo ========================================
echo   SETUP DE REPOSITORIOS GITHUB
echo ========================================
echo.

REM Verificar si gh CLI está instalado
where gh >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: GitHub CLI no esta instalado
    echo.
    echo Por favor instala GitHub CLI desde:
    echo https://cli.github.com/
    echo.
    echo O usa el metodo manual que se encuentra en GITHUB_SETUP_MANUAL.md
    pause
    exit /b 1
)

echo [1/6] Verificando autenticacion de GitHub...
gh auth status
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo No estas autenticado en GitHub CLI
    echo Ejecutando autenticacion...
    gh auth login
)

echo.
echo [2/6] Inicializando repositorio Git local...
git init
git branch -M main

echo.
echo [3/6] Agregando archivos al staging...
git add .

echo.
echo [4/6] Creando commit inicial...
git commit -m "Initial commit: Sistema CMMS completo con ML, Bot Telegram y Celery"

echo.
echo [5/6] Creando repositorio 'proyecto-de-titulo-local' en GitHub...
gh repo create proyecto-de-titulo-local --private --source=. --remote=origin --push

echo.
echo [6/6] Creando repositorio 'proyecto-de-titulo-produccion' en GitHub...
gh repo create proyecto-de-titulo-produccion --private

echo.
echo ========================================
echo   SETUP COMPLETADO EXITOSAMENTE
echo ========================================
echo.
echo Repositorios creados:
echo   1. proyecto-de-titulo-local (con codigo)
echo   2. proyecto-de-titulo-produccion (vacio, listo para deployment)
echo.
echo Proximos pasos:
echo   - Ver repositorio local: gh repo view --web
echo   - Configurar deployment: Ver DEPLOYMENT_GUIDE.md
echo.
pause
