# 🔧 Solución: Logs y Comandos de Telegram

## ✅ Problema Identificado

Los logs de Railway no mostraban los mensajes de la aplicación Django, solo las peticiones HTTP. Esto dificultaba el debugging.

## 🚀 Corrección Aplicada

He agregado configuración de logging específica para Railway en `backend/config/settings/railway.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'apps.omnichannel_bot': {
            'handlers': ['console'],
            'level': 'DEBUG',  # Nivel DEBUG para ver todos los logs
            'propagate': False,
        },
    },
}
```

## 📊 Qué Verás Ahora en los Logs

Después del despliegue (2-3 minutos), cuando envíes un comando verás:

```
INFO 2025-12-01 10:30:00 views Telegram update received: {...}
INFO 2025-12-01 10:30:00 views Message from 123456789: /help
INFO 2025-12-01 10:30:00 views User found: admin
INFO 2025-12-01 10:30:00 views Command response: 📚 *Comandos Disponibles*...
INFO 2025-12-01 10:30:00 views Message sent successfully to 123456789
```

## 🔍 Cómo Ver los Logs

### Opción 1: Railway CLI
```bash
railway logs --tail 100
```

### Opción 2: Dashboard de Railway
1. Ve a https://railway.app
2. Selecciona tu proyecto
3. Ve a la pestaña "Deployments"
4. Click en el deployment activo
5. Ve a la pestaña "Logs"

## 🧪 Pasos para Probar

### Paso 1: Esperar el Despliegue (2-3 minutos)

```bash
railway logs --tail 10
```

Busca: `Server started` o similar

### Paso 2: Enviar Comando en Telegram

Abre Telegram y envía: `/help`

### Paso 3: Ver los Logs Inmediatamente

```bash
railway logs --tail 50
```

**Logs esperados**:
```
INFO ... views Telegram update received: ...
INFO ... views Message from 123456789: /help
INFO ... views User found: admin
INFO ... views Command response: ...
INFO ... views Message sent successfully
```

### Paso 4: Identificar el Problema

#### Si ves "No user found"
```
INFO ... views Message from 123456789: /help
WARNING ... views No user found for chat_id 123456789
```

**Solución**: Vincula tu usuario
```bash
curl -X POST https://tu-app.up.railway.app/api/omnichannel/link-user/ \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "chat_id": "123456789"}'
```

#### Si ves "Failed to send message"
```
INFO ... views Command response: ...
ERROR ... views Failed to send message: Bad Request: ...
```

**Problema**: Error al enviar mensaje a Telegram
**Causa posible**: Token inválido o problema de formato

#### Si no ves ningún log
```
(No aparece nada cuando envías el comando)
```

**Problema**: Webhook no está recibiendo mensajes
**Solución**: Reconfigura el webhook

## 🔧 Soluciones Rápidas

### 1. Verificar Usuario Vinculado

```bash
curl https://tu-app.up.railway.app/api/omnichannel/link-user/
```

Si no apareces en la lista, vincúlate:

```bash
# Paso 1: Obtener tu chat_id
curl https://tu-app.up.railway.app/api/omnichannel/get-chat-id/

# Paso 2: Vincular
curl -X POST https://tu-app.up.railway.app/api/omnichannel/link-user/ \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "chat_id": "TU_CHAT_ID"}'
```

### 2. Verificar Webhook

```bash
# Reemplaza <TOKEN> con tu bot token
curl https://api.telegram.org/bot<TOKEN>/getWebhookInfo
```

Si `url` está vacío, reconfigura:
```bash
curl https://tu-app.up.railway.app/api/data-loader/setup-telegram/
```

### 3. Probar Webhook Manualmente

He creado un script de prueba: `test_telegram_webhook.py`

**Uso**:
1. Edita el script y actualiza `RAILWAY_URL`
2. Ejecuta:
```bash
python test_telegram_webhook.py
```

Esto probará:
- Estado del bot
- Chat IDs recientes
- Webhook directamente

## 📋 Checklist de Verificación

- [ ] Despliegue completado (2-3 minutos)
- [ ] Logs muestran mensajes de la aplicación
- [ ] Usuario vinculado con chat_id
- [ ] Webhook configurado
- [ ] Comando /start funciona
- [ ] Comando /help funciona
- [ ] Logs muestran "Message sent successfully"

## 🐛 Debugging Avanzado

### Ver Logs en Tiempo Real

```bash
railway logs --tail 100 --follow
```

Deja esto corriendo y envía comandos en Telegram. Verás los logs en tiempo real.

### Filtrar Logs del Bot

```bash
railway logs --tail 200 | grep "omnichannel_bot"
```

### Ver Solo Errores

```bash
railway logs --tail 200 | grep -i "error\|exception\|failed"
```

## 📝 Información para Reportar

Si el problema persiste, proporciona:

1. **Logs completos**:
```bash
railway logs --tail 100 > logs.txt
```

2. **Comando que enviaste**: Ej: `/help`

3. **Qué pasó**: 
   - ¿El bot respondió?
   - ¿Qué mensaje recibiste?
   - ¿O no recibiste nada?

4. **Usuario vinculado**:
```bash
curl https://tu-app.up.railway.app/api/omnichannel/link-user/
```

## ✅ Próximos Pasos

1. **Espera 2-3 minutos** para que Railway despliegue
2. **Envía /help** al bot en Telegram
3. **Ejecuta**: `railway logs --tail 50`
4. **Comparte** lo que ves en los logs

---

**Estado**: Configuración de logging desplegada
**Próximo paso**: Esperar despliegue y revisar logs
