# Mejoras en Alertas y Menú del Bot de Telegram

## Resumen

Se implementaron dos mejoras importantes en el bot de Telegram:
1. **Frecuencia de alertas reducida**: De cada 1 hora a cada 4 horas
2. **Menú de comandos persistente**: Los usuarios ven los comandos disponibles al escribir "/"

---

## 1. Frecuencia de Alertas Reducida

### Problema

Las alertas de activos críticos se enviaban cada hora, lo que podía resultar en notificaciones excesivas y molestas para los usuarios.

### Solución

Cambiar la frecuencia de la tarea `check-critical-assets` de cada 1 hora a cada 4 horas.

### Cambios Implementados

**Archivo**: `backend/config/celery.py`

#### Antes:
```python
# Verificar activos críticos cada hora
'check-critical-assets': {
    'task': 'apps.assets.tasks.check_critical_assets',
    'schedule': crontab(minute=0),  # Cada hora en punto
},
```

#### Después:
```python
# Verificar activos críticos cada 4 horas
'check-critical-assets': {
    'task': 'apps.assets.tasks.check_critical_assets',
    'schedule': crontab(minute=0, hour='*/4'),  # Cada 4 horas (0, 4, 8, 12, 16, 20)
},
```

### Horarios de Ejecución

Con la nueva configuración, las alertas se enviarán a las:
- **00:00** (medianoche)
- **04:00** (madrugada)
- **08:00** (mañana)
- **12:00** (mediodía)
- **16:00** (tarde)
- **20:00** (noche)

### Beneficios

✅ **Menos notificaciones molestas**: Los usuarios no serán bombardeados con alertas cada hora
✅ **Información más relevante**: Las alertas cada 4 horas son suficientes para activos críticos
✅ **Mejor experiencia de usuario**: Reduce la fatiga de notificaciones
✅ **Menor carga del servidor**: Menos ejecuciones de tareas programadas

---

## 2. Menú de Comandos Persistente

### Problema

Los usuarios no sabían qué comandos estaban disponibles y tenían que recordarlos o buscar en /help.

### Solución

Configurar el menú de comandos de Telegram para que aparezca automáticamente cuando el usuario escribe "/" en el chat.

### Cambios Implementados

#### A. Función para Configurar el Menú

**Archivo**: `backend/apps/omnichannel_bot/views.py`

```python
def setup_bot_commands(bot_token: str) -> bool:
    """
    Configura el menú de comandos del bot de Telegram
    """
    commands = [
        {"command": "start", "description": "🏠 Iniciar el bot"},
        {"command": "workorders", "description": "📋 Ver mis órdenes de trabajo"},
        {"command": "predictions", "description": "⚠️ Ver predicciones de alto riesgo"},
        {"command": "assets", "description": "🔧 Ver estado de activos"},
        {"command": "status", "description": "📊 Estado general del sistema"},
        {"command": "myinfo", "description": "👤 Ver mi información"},
        {"command": "help", "description": "❓ Ver ayuda y comandos"},
    ]
    
    response = requests.post(
        f"https://api.telegram.org/bot{bot_token}/setMyCommands",
        json={"commands": commands},
        timeout=10
    )
    
    return response.status_code == 200
```

#### B. Configuración Automática en Webhook

El menú se configura automáticamente la primera vez que el bot recibe un mensaje:

```python
@csrf_exempt
@require_http_methods(["POST", "GET"])
def telegram_webhook(request):
    # ...
    
    # Configurar menú de comandos si no está configurado
    if bot_token and not hasattr(telegram_webhook, '_commands_configured'):
        setup_bot_commands(bot_token)
        telegram_webhook._commands_configured = True
    
    # ...
```

#### C. Comando de Management

**Archivo**: `backend/apps/omnichannel_bot/management/commands/setup_telegram_menu.py`

Comando para configurar el menú manualmente:

```bash
python manage.py setup_telegram_menu
```

**Salida**:
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

### Comandos Disponibles en el Menú

| Comando | Descripción | Emoji |
|---------|-------------|-------|
| `/start` | Iniciar el bot | 🏠 |
| `/workorders` | Ver mis órdenes de trabajo | 📋 |
| `/predictions` | Ver predicciones de alto riesgo | ⚠️ |
| `/assets` | Ver estado de activos | 🔧 |
| `/status` | Estado general del sistema | 📊 |
| `/myinfo` | Ver mi información | 👤 |
| `/help` | Ver ayuda y comandos | ❓ |

### Cómo se Ve para el Usuario

Cuando el usuario escribe "/" en el chat de Telegram, verá un menú desplegable con todos los comandos disponibles y sus descripciones:

```
/start 🏠 Iniciar el bot
/workorders 📋 Ver mis órdenes de trabajo
/predictions ⚠️ Ver predicciones de alto riesgo
/assets 🔧 Ver estado de activos
/status 📊 Estado general del sistema
/myinfo 👤 Ver mi información
/help ❓ Ver ayuda y comandos
```

### Beneficios

✅ **Descubrimiento fácil**: Los usuarios ven todos los comandos disponibles
✅ **Mejor UX**: No necesitan memorizar comandos
✅ **Acceso rápido**: Un toque para seleccionar el comando
✅ **Descripciones claras**: Cada comando tiene una descripción con emoji
✅ **Estándar de Telegram**: Usa la funcionalidad nativa de Telegram

---

## Configuración Manual

### 1. Configurar Menú de Comandos

```bash
# Desde el directorio backend
python manage.py setup_telegram_menu
```

### 2. Verificar Configuración de Celery

```bash
# Ver tareas programadas
python manage.py check_scheduled_tasks

# Reiniciar Celery Beat para aplicar cambios
# Windows:
taskkill /F /IM celery.exe
start_celery_beat.bat

# Linux/Mac:
pkill -f 'celery beat'
celery -A config beat -l info
```

### 3. Probar el Menú

1. Abre el chat con el bot en Telegram
2. Escribe "/" en el campo de mensaje
3. Deberías ver el menú de comandos desplegable
4. Selecciona un comando para ejecutarlo

---

## Testing

### Prueba 1: Verificar Frecuencia de Alertas

```python
# Verificar configuración de Celery Beat
from django_celery_beat.models import PeriodicTask

task = PeriodicTask.objects.get(name='check-critical-assets')
print(f"Tarea: {task.name}")
print(f"Crontab: {task.crontab}")
print(f"Hora: {task.crontab.hour}")  # Debe ser '*/4'
print(f"Minuto: {task.crontab.minute}")  # Debe ser '0'
```

### Prueba 2: Verificar Menú de Comandos

```bash
# Ejecutar comando de configuración
python manage.py setup_telegram_menu

# Verificar en Telegram:
# 1. Abrir chat con el bot
# 2. Escribir "/"
# 3. Verificar que aparece el menú con 7 comandos
```

### Prueba 3: Probar Comandos del Menú

```
1. /start → Debe mostrar mensaje de bienvenida
2. /workorders → Debe mostrar órdenes de trabajo
3. /predictions → Debe mostrar predicciones
4. /assets → Debe mostrar estado de activos
5. /status → Debe mostrar estado del sistema
6. /myinfo → Debe mostrar información del usuario
7. /help → Debe mostrar ayuda
```

---

## Impacto

### Frecuencia de Alertas

- **Usuarios afectados**: Todos los usuarios con notificaciones de Telegram habilitadas
- **Reducción de notificaciones**: 75% menos (de 24 alertas/día a 6 alertas/día)
- **Breaking changes**: Ninguno
- **Mejora de UX**: Alta - Menos notificaciones molestas

### Menú de Comandos

- **Usuarios afectados**: Todos los usuarios del bot de Telegram
- **Breaking changes**: Ninguno
- **Mejora de UX**: Alta - Descubrimiento fácil de comandos
- **Facilidad de uso**: Mejorada significativamente

---

## Configuración Adicional

### Personalizar Horarios de Alertas

Si quieres cambiar los horarios específicos, edita `backend/config/celery.py`:

```python
# Ejemplo: Alertas solo en horario laboral (8:00, 12:00, 16:00)
'check-critical-assets': {
    'task': 'apps.assets.tasks.check_critical_assets',
    'schedule': crontab(minute=0, hour='8,12,16'),
},
```

### Agregar Más Comandos al Menú

Edita la lista de comandos en `setup_bot_commands()`:

```python
commands = [
    # ... comandos existentes ...
    {"command": "report", "description": "📊 Generar reporte"},
    {"command": "settings", "description": "⚙️ Configuración"},
]
```

---

## Troubleshooting

### El menú no aparece en Telegram

**Solución 1**: Ejecutar comando manual
```bash
python manage.py setup_telegram_menu
```

**Solución 2**: Reiniciar el chat
- Bloquear y desbloquear el bot
- O enviar /start nuevamente

**Solución 3**: Verificar token del bot
```bash
python manage.py test_telegram_bot
```

### Las alertas siguen llegando cada hora

**Solución**: Reiniciar Celery Beat
```bash
# Windows
taskkill /F /IM celery.exe
start_celery_beat.bat

# Linux/Mac
pkill -f 'celery beat'
celery -A config beat -l info
```

### Verificar que los cambios se aplicaron

```python
from django_celery_beat.models import CrontabSchedule, PeriodicTask

# Ver todas las tareas programadas
for task in PeriodicTask.objects.all():
    print(f"{task.name}: {task.crontab}")
```

---

## Commits

```bash
git commit -m "feat: Mejorar alertas y menú del bot de Telegram

- Reducir frecuencia de alertas de 1 hora a 4 horas
- Agregar menú de comandos persistente en Telegram
- Crear comando setup_telegram_menu para configuración manual
- Configuración automática del menú en primer mensaje
- Horarios de alertas: 00:00, 04:00, 08:00, 12:00, 16:00, 20:00
- 7 comandos disponibles en el menú con emojis descriptivos"
```

---

## Referencias

- Celery Configuration: `backend/config/celery.py`
- Bot Views: `backend/apps/omnichannel_bot/views.py`
- Bot Commands: `backend/apps/omnichannel_bot/bot_commands.py`
- Setup Menu Command: `backend/apps/omnichannel_bot/management/commands/setup_telegram_menu.py`
- Telegram Bot API: https://core.telegram.org/bots/api#setmycommands
