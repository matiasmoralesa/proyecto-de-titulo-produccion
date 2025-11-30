@echo off
echo ========================================
echo   Iniciando Sistema CMMS Completo
echo ========================================
echo.

echo [1/3] Verificando Redis...
python -c "import redis; r = redis.Redis(); r.ping(); print('Redis OK')" 2>nul
if errorlevel 1 (
    echo Redis no esta corriendo. Iniciando...
    start "Redis Server" "%USERPROFILE%\redis\redis-server.exe"
    timeout /t 2 >nul
)

echo [2/3] Iniciando Celery Worker...
start "Celery Worker" cmd /k "celery -A config worker -l info --pool=solo"

echo [3/3] Iniciando Celery Beat...
start "Celery Beat" cmd /k "celery -A config beat -l info"

echo.
echo ========================================
echo   Sistema iniciado correctamente!
echo ========================================
echo.
echo Ventanas abiertas:
echo   - Redis Server
echo   - Celery Worker (ejecutor de tareas)
echo   - Celery Beat (programador)
echo.
echo Para detener: Cierra todas las ventanas
echo.
pause
