@echo off
echo ============================================================
echo    SCRIPT DE LIMPIEZA Y POBLACION DE DATOS - CMMS
echo ============================================================
echo.
echo ADVERTENCIA: Este script eliminara TODOS los datos existentes
echo.
pause

REM Activar entorno virtual
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo ERROR: No se encontro el entorno virtual en venv\Scripts\
    echo Por favor, crea el entorno virtual primero.
    pause
    exit /b 1
)

REM Cambiar al directorio backend
cd backend

REM Ejecutar el comando de Django
python manage.py reset_and_populate --no-input

REM Verificar si hubo error
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: El script fallo con codigo de error %ERRORLEVEL%
    cd ..
    pause
    exit /b %ERRORLEVEL%
)

REM Volver al directorio raíz
cd ..

echo.
echo ============================================================
echo Proceso completado. Presiona cualquier tecla para salir.
pause
