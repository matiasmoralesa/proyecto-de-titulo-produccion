@echo off
echo ============================================================
echo    LIMPIAR DATOS DE PRODUCCION EN RAILWAY
echo ============================================================
echo.
echo ADVERTENCIA: Esto eliminara TODOS los datos de PRODUCCION
echo.
pause

echo.
echo Ejecutando comando en Railway...
echo.

railway run python manage.py reset_and_populate --no-input

echo.
echo ============================================================
echo Proceso completado.
pause
