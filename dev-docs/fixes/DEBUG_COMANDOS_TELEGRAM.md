# 🔍 Debug: Comandos de Telegram No Funcionan

## ✅ Corrección Desplegada

He corregido dos problemas potenciales:

1. **Formato de mensajes**: El método `format_message` ahora maneja correctamente títulos vacíos
2. **Logging mejorado**: Agregado logging detallado para diagnosticar problemas

## 🚀 Cambios Realizados

### 1. Corrección en `telegram.py`

**Antes**:
```python
def format_message(self, title: str, message: str) -> str:
    return f"*{title}*\n\n{message}"  # Problema: si title está vacío, genera "**\n\n"
```

**Ahora**:
```python
def format_message(self, title: str, message: str) -> str:
    if title:
        return f"*{title}*\n\n{message}"
    return message  # Retorna solo el mensaje si no hay título
```

### 2. Mejoras en `views.py`

- ✅ Agregado logging de usuario encontrado
- ✅ Agregado logging de respuesta del comando
- ✅ Agregado logging de éxito/error al enviar mensaje
- ✅ Agregado manejo de excepciones completo
- ✅ Agregado traceback en logs para debugging

## 🔍 Cómo Diagnosticar el Problema

### Paso 1: Ver los Logs

```bash
railway logs --tail 100
```

Busca líneas como estas cuando envíes un comando:

```
Message from 123456789: /help
User found: admin
Command response: 📚 *Comandos Disponibles*...
Message sent successfully to 123456789
```

### Paso 2: Identificar el Problema

#### Si ves "No user found"
```
Message from 123456789: /help
No user found for chat_id 123456789
```

**Problema**: Usuario no vinculado
**Solución**: Vincula el usuario con `/api/omnichannel/link-user/`

#### Si ves "Failed to send message"
```
Message from 123456789: /help
Command response: ...
Failed to send message: Bad Request: can't parse entities
```

**Problema**: Error de formato Markdown
**Solución**: Ya corregido en el último despliegue

#### Si no ves ningún log
```
(No aparece nada cuando envías el comando)
```

**Problema**: Webhook no está recibiendo mensajes
**Solución**: Reconfigura el webhook

### Paso 3: Verificar el Webhook

```bash
# Obtener info del webhook
curl https://api.telegram.org/bot<TU_BOT_TOKEN>/getWebhookInfo
```

Deberías ver:
```json
{
  "ok": true,
  "result": {
    "url": "https://tu-app.up.railway.app/api/omnichannel/webhook/telegram/",
    "has_custom_certificate": false,
    "pending_update_count": 0,
    "last_error_date": 0
  }
}
```

**Si `url` está vacío**: Webhook no configurado
**Si `pending_update_count` > 0**: Hay mensajes pendientes
**Si `last_error_date` > 0**: Hubo un error reciente

## 🔧 Soluciones Comunes

### Problema 1: Webhook No Configurado

**Síntoma**: Los comandos no llegan al servidor

**Solución**:
```bash
curl https://tu-app.up.railway.app/api/data-loader/setup-telegram/
```

### Problema 2: Usuario No Vinculado

**Síntoma**: Ves "No user found" en los logs

**Solución**:
1. Obtén tu chat_id:
```bash
curl https://tu-app.up.railway.app/api/omnichannel/get-chat-id/
```

2. Vincula tu usuario:
```bash
curl -X POST https://tu-app.up.railway.app/api/omnichannel/link-user/ \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "chat_id": "TU_CHAT_ID"}'
```

### Problema 3: Error de Formato Markdown

**Síntoma**: Ves "can't parse entities" en los logs

**Solución**: Ya corregido en el último despliegue. Espera 2-3 minutos.

### Problema 4: Comandos No Reconocidos

**Síntoma**: El bot responde "Comando no reconocido"

**Causa**: El comando no está en la lista de comandos disponibles

**Comandos válidos**:
- `/start`
- `/help`
- `/status`
- `/workorders`
- `/predictions`
- `/assets`
- `/myinfo`

## 🧪 Pruebas Paso a Paso

### 1. Verificar que el despliegue terminó

```bash
railway logs --tail 10
```

Busca: `Server started successfully` o similar

### 2. Enviar comando /start

En Telegram, envía: `/start`

**Resultado esperado**: Mensaje de bienvenida con botones

### 3. Enviar comando /help

En Telegram, envía: `/help`

**Resultado esperado**: Lista de comandos disponibles

### 4. Revisar logs

```bash
railway logs --tail 50
```

**Logs esperados**:
```
Message from 123456789: /help
User found: admin
Command response: 📚 *Comandos Disponibles*...
Message sent successfully to 123456789
```

## 📊 Checklist de Verificación

- [ ] Despliegue completado (espera 2-3 minutos)
- [ ] Webhook configurado correctamente
- [ ] Usuario vinculado con chat_id
- [ ] Comando /start funciona
- [ ] Comando /help funciona
- [ ] Otros comandos funcionan
- [ ] Logs muestran mensajes enviados exitosamente
- [ ] No hay errores en los logs

## 🐛 Si Aún No Funciona

### Opción 1: Revisar Logs Detallados

```bash
railway logs --tail 200 | grep -i "error\|exception\|failed"
```

### Opción 2: Probar el Webhook Manualmente

```bash
curl -X POST https://tu-app.up.railway.app/api/omnichannel/webhook/telegram/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": {
      "chat": {"id": 123456789},
      "from": {"id": 123456789, "first_name": "Test"},
      "text": "/help"
    }
  }'
```

**Resultado esperado**: `{"ok": true}`

### Opción 3: Verificar Configuración del Bot

```bash
curl https://tu-app.up.railway.app/api/omnichannel/status/
```

**Resultado esperado**:
```json
{
  "status": "active",
  "channel": "TELEGRAM",
  "messages_sent": 10,
  "messages_failed": 0
}
```

## 📝 Información para Reportar

Si el problema persiste, proporciona:

1. **Logs del servidor**:
```bash
railway logs --tail 100 > logs.txt
```

2. **Info del webhook**:
```bash
curl https://api.telegram.org/bot<TOKEN>/getWebhookInfo > webhook_info.json
```

3. **Estado del bot**:
```bash
curl https://tu-app.up.railway.app/api/omnichannel/status/ > bot_status.json
```

4. **Usuarios vinculados**:
```bash
curl https://tu-app.up.railway.app/api/omnichannel/link-user/ > users.json
```

5. **Qué comando enviaste** y **qué respuesta obtuviste** (o si no obtuviste respuesta)

## ✅ Próximos Pasos

1. **Espera 2-3 minutos** para que Railway termine el despliegue
2. **Envía /start** al bot en Telegram
3. **Envía /help** al bot
4. **Revisa los logs**: `railway logs --tail 50`
5. **Reporta** lo que ves en los logs

---

**Última actualización**: Corrección de formato de mensajes desplegada
**Estado**: Esperando verificación
