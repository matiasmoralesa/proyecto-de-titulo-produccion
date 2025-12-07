@echo off
echo ============================================================
echo EJECUTANDO SEED DE DATOS EN RAILWAY
echo ============================================================
echo.
echo Conectando a Railway y ejecutando comando...
echo.
railway run python backend/manage.py seed_machine_status
echo.
echo ============================================================
echo PROCESO COMPLETADO
echo ============================================================
pause
