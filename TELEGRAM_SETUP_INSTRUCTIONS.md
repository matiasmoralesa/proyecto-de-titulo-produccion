# Instrucciones para Configurar el Menú del Bot de Telegram

## Configuración del Menú de Comandos

Para que los usuarios vean el menú de comandos cuando escriben "/" en el chat, ejecuta:

```bash
# Desde el directorio backend
cd backend
python manage.py setup_telegram_menu
```

**Salida esperada**:
```
📋 Configurando menú de comandos del bot...

✅ Menú de comandos configurado exitosamente!

📱 Comandos disponibles:
   /start - 🏠 Iniciar el bot
   /workorders - 📋 Ver mis órdenes de trabajo
   /predictions - ⚠️ Ver predicciones de alto riesgo
   /assets - 🔧 Ver estado de activos
   /status - 📊 Estado general del sistema
   /myinfo - 👤 Ver mi información
   /help - ❓ Ver ayuda y comandos

💡 Los usuarios ahora verán estos comandos al escribir "/" en el chat.
```

## Verificar en Telegram

1. Abre el chat con tu bot en Telegram
2. Escribe "/" en el campo de mensaje
3. Deberías ver un menú desplegable con todos los comandos
4. Selecciona un comando para ejecutarlo

## Aplicar Cambios de Frecuencia de Alertas

Los cambios en la frecuencia de alertas (de 1 hora a 4 horas) requieren reiniciar Celery Beat:

### En Producción (Railway):

```bash
# Las tareas de Celery se reinician automáticamente con el deploy
# No se requiere acción adicional
```

### En Desarrollo Local:

**Windows**:
```bash
# Detener Celery Beat
taskkill /F /IM celery.exe

# Reiniciar
cd backend
start_celery_beat.bat
```

**Linux/Mac**:
```bash
# Detener Celery Beat
pkill -f 'celery beat'

# Reiniciar
cd backend
celery -A config beat -l info
```

## Nuevos Horarios de Alertas

Con la nueva configuración, las alertas de activos críticos se enviarán a las:
- **00:00** (medianoche)
- **04:00** (madrugada)
- **08:00** (mañana)
- **12:00** (mediodía)
- **16:00** (tarde)
- **20:00** (noche)

**Reducción**: De 24 alertas/día a 6 alertas/día (75% menos)

## Troubleshooting

### El menú no aparece

1. Verifica que el bot esté configurado:
   ```bash
   python manage.py test_telegram_bot
   ```

2. Reinicia el chat con el bot:
   - Bloquea y desbloquea el bot
   - O envía `/start` nuevamente

3. Ejecuta el comando de configuración nuevamente:
   ```bash
   python manage.py setup_telegram_menu
   ```

### Las alertas siguen llegando cada hora

1. Verifica la configuración de Celery Beat:
   ```bash
   python manage.py check_scheduled_tasks
   ```

2. Reinicia Celery Beat (ver instrucciones arriba)

3. Verifica que los cambios se aplicaron:
   ```python
   from django_celery_beat.models import PeriodicTask
   task = PeriodicTask.objects.get(name='check-critical-assets')
   print(task.crontab.hour)  # Debe mostrar '*/4'
   ```

## Comandos Útiles

```bash
# Ver todas las tareas programadas
python manage.py check_scheduled_tasks

# Probar el bot
python manage.py test_telegram_bot

# Ver actualizaciones recientes
python manage.py get_telegram_updates

# Configurar webhook
python manage.py setup_telegram_webhook --url https://tu-dominio.com/api/omnichannel/telegram/webhook/
```
