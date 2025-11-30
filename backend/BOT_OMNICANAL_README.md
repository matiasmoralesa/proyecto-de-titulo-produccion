# Bot Omnicanal - Sistema CMMS

## 🎯 Descripción

Sistema de notificaciones multicanal que permite enviar alertas y mensajes a los usuarios a través de múltiples plataformas:

- ✅ **Telegram** (Implementado)
- 🔜 WhatsApp Business API
- 🔜 Email (SMTP)
- 🔜 SMS (Twilio)
- ✅ In-App (Sistema existente)

## 📦 Instalación

### 1. Instalar dependencias

```bash
pip install requests python-telegram-bot
```

### 2. Crear bot de Telegram

1. Abre Telegram y busca **@BotFather**
2. Envía el comando `/newbot`
3. Sigue las instrucciones:
   - Nombre del bot: `CMMS Notifications Bot`
   - Username: `tu_empresa_cmms_bot` (debe terminar en `_bot`)
4. Copia el **token** que te proporciona

### 3. Configurar el bot

Opción A: Usando variable de entorno (recomendado)

```bash
# Agregar en .env
TELEGRAM_BOT_TOKEN=tu_token_aqui
```

```bash
python manage.py setup_telegram_bot --enable
```

Opción B: Usando parámetro

```bash
python manage.py setup_telegram_bot --token TU_TOKEN_AQUI --enable
```

## 🚀 Uso

### Configurar usuario para recibir notificaciones

1. El usuario debe iniciar chat con el bot en Telegram:
   - Buscar el bot por su username
   - Enviar `/start`

2. Obtener el `chat_id` del usuario:
   - El usuario envía cualquier mensaje al bot
   - Visita: `https://api.telegram.org/botTU_TOKEN/getUpdates`
   - Busca el `chat.id` en la respuesta

3. Configurar en Django Admin:
   - Ir a **Omnichannel Bot > User Channel Preferences**
   - Crear nueva preferencia:
     - User: Seleccionar usuario
     - Channel type: TELEGRAM
     - Is enabled: ✓
     - Channel user id: Pegar el `chat_id`
     - Notify work orders: ✓
     - Notify predictions: ✓

### Probar el bot

```bash
# Enviar mensaje de prueba a un usuario
python manage.py test_telegram_bot --username admin

# Enviar mensaje directo a un chat_id
python manage.py test_telegram_bot --chat-id 123456789
```

## 📝 Uso Programático

### Enviar mensaje a un usuario

```python
from apps.omnichannel_bot.message_router import MessageRouter
from apps.authentication.models import User

router = MessageRouter()
user = User.objects.get(username='operador1')

results = router.send_to_user(
    user=user,
    title='Nueva Orden de Trabajo',
    message='Se te ha asignado la OT-12345 para el Camión 001',
    message_type='work_order_assigned',
    priority='high',
    related_object_type='work_order',
    related_object_id='uuid-de-la-ot'
)

print(results)  # {'TELEGRAM': True}
```

### Broadcast a un rol

```python
from apps.omnichannel_bot.message_router import MessageRouter

router = MessageRouter()

stats = router.broadcast_to_role(
    role_name='OPERATOR',
    title='Mantenimiento Programado',
    message='Mañana habrá mantenimiento general de 8:00 a 12:00',
    priority='normal'
)

print(stats)  # {'total': 10, 'success': 9, 'failed': 1}
```

## 🔧 Integración con Sistema ML

El sistema ML ya está integrado automáticamente. Cuando se detecta una predicción de riesgo MEDIUM/HIGH/CRITICAL:

1. ✅ Se crea una orden de trabajo
2. ✅ Se asigna un operador
3. ✅ Se envía notificación in-app
4. ✅ **Se envía notificación por Telegram** (si está configurado)

## 📊 Monitoreo

### Ver estadísticas de canales

Django Admin > Omnichannel Bot > Channel Configs

- Mensajes enviados
- Mensajes fallidos
- Último uso

### Ver log de mensajes

Django Admin > Omnichannel Bot > Message Logs

- Historial completo de mensajes
- Estado de entrega
- Errores

## 🔐 Seguridad

- El token del bot debe mantenerse **secreto**
- Usar variables de entorno, no hardcodear
- Los `chat_id` son únicos por usuario
- Solo usuarios autenticados pueden recibir notificaciones

## 🎨 Personalización

### Agregar nuevos tipos de mensajes

Editar `apps/omnichannel_bot/channels/telegram.py`:

```python
emoji_map = {
    'work_order_assigned': '📋',
    'critical_alert': '🚨',
    'prediction_high_risk': '⚠️',
    'maintenance_reminder': '🔧',
    'tu_nuevo_tipo': '🎯',  # Agregar aquí
}
```

### Agregar botones interactivos

```python
notification_data = {
    'title': 'Nueva OT',
    'message': 'OT-12345 asignada',
    'type': 'work_order_assigned',
    'actions': [
        {
            'text': '✅ Aceptar',
            'callback_data': 'accept_wo_12345'
        },
        {
            'text': '❌ Rechazar',
            'callback_data': 'reject_wo_12345'
        }
    ]
}

router.send_notification(user, notification_data)
```

## 🐛 Troubleshooting

### El bot no envía mensajes

1. Verificar que el canal esté habilitado:
   ```bash
   python manage.py shell
   >>> from apps.omnichannel_bot.models import ChannelConfig
   >>> ChannelConfig.objects.get(channel_type='TELEGRAM').is_enabled
   True
   ```

2. Verificar que el usuario tenga preferencias:
   ```bash
   >>> from apps.omnichannel_bot.models import UserChannelPreference
   >>> UserChannelPreference.objects.filter(user__username='admin')
   ```

3. Verificar el token:
   ```bash
   python manage.py setup_telegram_bot
   ```

### Error: "Chat not found"

- El usuario no ha iniciado chat con el bot
- El `chat_id` es incorrecto
- El bot fue bloqueado por el usuario

### Error: "Unauthorized"

- El token del bot es incorrecto
- El token expiró o fue revocado

## 📚 Próximos Pasos

1. **WhatsApp Business API**
   - Requiere cuenta de negocio verificada
   - Proceso de aprobación de Meta
   - Templates de mensajes pre-aprobados

2. **Email (SMTP)**
   - Configurar servidor SMTP
   - Templates HTML
   - Adjuntar PDFs de órdenes

3. **SMS (Twilio)**
   - Cuenta de Twilio
   - Solo para alertas críticas
   - Rate limiting

4. **WebSocket (Real-time)**
   - Notificaciones push en el frontend
   - Sin necesidad de refresh

## 🎯 Estado Actual

✅ **Fase 1: Telegram Bot** - COMPLETADO
- Modelos de datos
- Canal de Telegram
- Message Router
- Integración con ML
- Comandos de management
- Admin interface

⏳ **Fase 2: Otros Canales** - PENDIENTE
⏳ **Fase 3: Frontend Dashboard** - PENDIENTE
⏳ **Fase 4: Bot Interactivo** - PENDIENTE (comandos, callbacks)

## 📞 Soporte

Para más información, consulta:
- `apps/omnichannel_bot/models.py` - Modelos de datos
- `apps/omnichannel_bot/message_router.py` - Lógica de enrutamiento
- `apps/omnichannel_bot/channels/telegram.py` - Implementación de Telegram
