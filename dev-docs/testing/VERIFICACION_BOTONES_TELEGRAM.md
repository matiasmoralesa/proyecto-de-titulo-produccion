# Verificación de Botones del Bot de Telegram

## ✅ Estado de Implementación

Los botones del bot de Telegram están **correctamente implementados** en el código:

### Botones Implementados

1. **Comando `/start`**
   - 📋 Mis Órdenes
   - ⚠️ Predicciones
   - ❓ Ayuda

2. **Comando `/status`**
   - 📋 Ver OT Activas
   - ⚠️ Ver Predicciones

3. **Comando `/workorders`**
   - Botones dinámicos para cada orden de trabajo (Ver OT-XXX)

4. **Detalle de Orden de Trabajo**
   - ✅ Aceptar (si está pendiente)
   - 🔄 Iniciar (si está pendiente)
   - ✅ Completar (si está en progreso)
   - « Volver

## 🧪 Cómo Probar Localmente

```bash
cd backend
python test_telegram_buttons.py
```

Este script verifica:
- ✅ Configuración del bot
- ✅ Conexión con Telegram API
- ✅ Estructura de botones en cada comando
- ✅ Estado del webhook

## 🌐 Cómo Probar en Producción

### 1. Verificar que el webhook esté configurado

Visita en tu navegador:
```
https://tu-app.up.railway.app/api/data-loader/setup-telegram/
```

Deberías ver:
```json
{
  "success": true,
  "message": "Telegram bot configured successfully",
  "webhook_url": "https://tu-app.up.railway.app/api/omnichannel/webhook/telegram/"
}
```

### 2. Probar el bot en Telegram

1. **Abre Telegram** y busca tu bot
2. **Envía `/start`**
   - Deberías ver 3 botones: "Mis Órdenes", "Predicciones", "Ayuda"
3. **Presiona "Mis Órdenes"**
   - Debería mostrar tus órdenes de trabajo con botones para ver detalles
4. **Presiona cualquier botón "Ver OT-XXX"**
   - Debería mostrar el detalle con botones "Aceptar", "Iniciar", "Volver"
5. **Presiona "Volver"**
   - Debería regresar al menú anterior

### 3. Verificar logs en Railway

```bash
railway logs
```

Busca líneas como:
```
Telegram update received: {...}
Message from 123456789: /start
Callback from 123456789: cmd_workorders
```

## 🔧 Estructura Técnica

### Cómo funcionan los botones

1. **Definición de botones** (`bot_commands.py`):
```python
{
    'text': '📋 Mis Órdenes',
    'callback_data': 'cmd_workorders'
}
```

2. **Envío al usuario** (`telegram.py`):
```python
reply_markup = {'inline_keyboard': buttons}
```

3. **Procesamiento de callback** (`views.py`):
```python
def handle_callback(callback_query, telegram):
    callback_data = callback_query['data']
    handler.handle_callback(callback_data, user)
```

## 🐛 Solución de Problemas

### Los botones no aparecen

**Causa**: El webhook no está configurado o no está recibiendo actualizaciones

**Solución**:
1. Verifica el webhook: `https://api.telegram.org/bot<TOKEN>/getWebhookInfo`
2. Reconfigura: Visita `/api/data-loader/setup-telegram/`

### Los botones no responden

**Causa**: El callback no se está procesando correctamente

**Solución**:
1. Revisa los logs de Railway: `railway logs`
2. Busca errores en `handle_callback`
3. Verifica que el usuario esté asociado a un chat_id en `UserChannelPreference`

### Error "Usuario no identificado"

**Causa**: El chat_id del usuario no está registrado en la base de datos

**Solución**:
1. El usuario debe enviar `/start` al bot
2. El bot mostrará su chat_id
3. Un administrador debe crear un `UserChannelPreference` con ese chat_id

## 📊 Verificación de Estado

### Endpoint de estado del bot

```bash
curl https://tu-app.up.railway.app/api/omnichannel/status/
```

Respuesta esperada:
```json
{
  "status": "active",
  "channel": "TELEGRAM",
  "messages_sent": 42,
  "messages_failed": 0,
  "last_used": "2025-12-01T10:30:00Z"
}
```

## ✅ Checklist de Verificación

- [ ] Webhook configurado correctamente
- [ ] Bot responde a `/start`
- [ ] Botones aparecen en el mensaje
- [ ] Botones responden al presionarlos
- [ ] Navegación entre menús funciona
- [ ] Botones de acciones (Aceptar, Iniciar) funcionan
- [ ] Logs muestran callbacks procesados
- [ ] No hay errores en los logs

## 🎯 Comandos Disponibles con Botones

| Comando | Botones | Descripción |
|---------|---------|-------------|
| `/start` | Mis Órdenes, Predicciones, Ayuda | Menú principal |
| `/status` | Ver OT Activas, Ver Predicciones | Estado del sistema |
| `/workorders` | Ver OT-XXX (dinámico) | Lista de órdenes |
| Detalle OT | Aceptar, Iniciar, Completar, Volver | Acciones sobre OT |

## 📝 Notas Importantes

1. **Los botones son inline keyboards**: Se muestran debajo del mensaje y no desaparecen
2. **Los callbacks son procesados en tiempo real**: No requieren recargar
3. **La navegación es fluida**: Los mensajes se editan en lugar de enviar nuevos
4. **Los botones son contextuales**: Cambian según el estado de la orden de trabajo

## 🚀 Próximos Pasos

Si los botones funcionan correctamente:
1. ✅ Configura usuarios con sus chat_ids
2. ✅ Prueba el flujo completo de una orden de trabajo
3. ✅ Verifica las notificaciones automáticas
4. ✅ Documenta el uso para los operadores
