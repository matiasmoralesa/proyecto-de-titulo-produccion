@echo off
echo ========================================
echo Desplegando correcciones del bot de Telegram
echo ========================================
echo.

echo 1. Agregando cambios a git...
git add backend/apps/omnichannel_bot/views.py
git add backend/apps/omnichannel_bot/urls.py
git add backend/link_telegram_user.py
git add SOLUCION_BOTONES_TELEGRAM.md

echo.
echo 2. Creando commit...
git commit -m "Fix: Corregir botones de Telegram y agregar vinculacion de usuarios"

echo.
echo 3. Desplegando a Railway...
git push origin main

echo.
echo ========================================
echo Despliegue completado
echo ========================================
echo.
echo Proximos pasos:
echo 1. Espera a que Railway termine el despliegue
echo 2. Vincula tu usuario con tu chat_id
echo 3. Prueba los botones en Telegram
echo.
echo Para vincular tu usuario:
echo 1. Envia /start al bot en Telegram
echo 2. Visita: https://tu-app.up.railway.app/api/omnichannel/get-chat-id/
echo 3. Usa el endpoint /api/omnichannel/link-user/ para vincular
echo.
pause
