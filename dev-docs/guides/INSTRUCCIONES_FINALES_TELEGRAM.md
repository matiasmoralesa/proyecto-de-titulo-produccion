# 🔍 Instrucciones Finales: Debugging del Bot de Telegram

## ✅ Logging Detallado Desplegado

He agregado logging extremadamente detallado en el método `send_message` que mostrará:

1. ✅ Si el bot token está configurado
2. ✅ Si el canal está configurado
3. ✅ El mensaje que se está enviando
4. ✅ La URL de la API de Telegram
5. ✅ El payload completo
6. ✅ El status code de la respuesta
7. ✅ La respuesta completa de Telegram
8. ✅ Cualquier error o excepción

## 🚀 Despliegue

✅ Código desplegado
⏱️ Espera 2-3 minutos

## 🔍 Qué Hacer Ahora

### Paso 1: Esperar el Despliegue

```bash
railway logs --tail 10
```

Busca algo como: `Server started` o que los logs se actualicen

### Paso 2: Enviar Comando

Abre Telegram y envía: `/help`

### Paso 3: Ver Logs Detallados

```bash
railway logs --tail 100
```

Ahora verás logs como estos:

```
INFO ... telegram [TELEGRAM] Intentando enviar mensaje a chat_id: 123456789
INFO ... telegram [TELEGRAM] Bot token configurado: True
INFO ... telegram [TELEGRAM] Canal configurado: True
INFO ... telegram [TELEGRAM] Mensaje formateado (primeros 100 chars): 📚 *Comandos Disponibles*...
INFO ... telegram [TELEGRAM] URL de API: https://api.telegram.org/bot<TOKEN>/sendMessage
INFO ... telegram [TELEGRAM] Payload: {'chat_id': '123456789', 'text': '...', 'parse_mode': 'Markdown'}
INFO ... telegram [TELEGRAM] Enviando petición POST a Telegram API...
INFO ... telegram [TELEGRAM] Status code de respuesta: 200
INFO ... telegram [TELEGRAM] Respuesta completa: {"ok":true,"result":{...}}
INFO ... telegram [TELEGRAM] ✅ Mensaje enviado exitosamente. Message ID: 12345
```

## 🐛 Posibles Problemas y Soluciones

### Problema 1: "Bot token configurado: False"

```
INFO ... telegram [TELEGRAM] Bot token configurado: False
ERROR ... telegram [TELEGRAM] Canal no configurado correctamente
```

**Causa**: El bot token no está en la configuración
**Solución**: Verifica que el token esté en la base de datos

```bash
# Verificar configuración
curl https://tu-app.up.railway.app/api/omnichannel/status/
```

### Problema 2: "Error 401 Unauthorized"

```
INFO ... telegram [TELEGRAM] Status code de respuesta: 401
ERROR ... telegram [TELEGRAM] ❌ Error al enviar mensaje: Unauthorized
```

**Causa**: Bot token inválido
**Solución**: Reconfigura el bot con el token correcto

### Problema 3: "Error 400 Bad Request: can't parse entities"

```
INFO ... telegram [TELEGRAM] Status code de respuesta: 400
ERROR ... telegram [TELEGRAM] ❌ Error al enviar mensaje: Bad Request: can't parse entities
```

**Causa**: Markdown inválido en el mensaje
**Solución**: Ya corregido, pero si persiste, desactiva Markdown temporalmente

### Problema 4: "Timeout al conectar con Telegram"

```
ERROR ... telegram [TELEGRAM] ❌ Timeout al enviar mensaje a Telegram API
```

**Causa**: Problema de red o Telegram API caído
**Solución**: Espera unos minutos y reintenta

### Problema 5: Status 200 pero no llega el mensaje

```
INFO ... telegram [TELEGRAM] Status code de respuesta: 200
INFO ... telegram [TELEGRAM] ✅ Mensaje enviado exitosamente
```

**Causa**: El mensaje se envió pero a un chat_id incorrecto
**Solución**: Verifica que el chat_id sea el correcto

```bash
# Ver tu chat_id
curl https://tu-app.up.railway.app/api/omnichannel/get-chat-id/
```

## 📋 Checklist de Verificación

Después de enviar `/help`, verifica en los logs:

- [ ] "Bot token configurado: True"
- [ ] "Canal configurado: True"
- [ ] "Mensaje formateado" aparece
- [ ] "Enviando petición POST" aparece
- [ ] "Status code de respuesta: 200"
- [ ] "✅ Mensaje enviado exitosamente"
- [ ] El chat_id en los logs coincide con tu chat_id real

## 🎯 Acción Inmediata

1. **Espera 2-3 minutos**
2. **Envía `/help`** al bot en Telegram
3. **Ejecuta**: `railway logs --tail 100`
4. **Copia TODOS los logs** que veas (especialmente los que dicen `[TELEGRAM]`)
5. **Compártelos** para que pueda diagnosticar el problema exacto

## 📝 Formato para Compartir Logs

Cuando compartas los logs, incluye:

```
=== LOGS COMPLETOS ===

[Pega aquí todos los logs que veas después de enviar /help]

=== INFO ADICIONAL ===

1. Comando enviado: /help
2. ¿Recibiste respuesta en Telegram?: Sí/No
3. Tu chat_id (de /api/omnichannel/get-chat-id/): 123456789
4. ¿Estás vinculado? (de /api/omnichannel/link-user/): Sí/No
```

## 🔧 Comandos Útiles

```bash
# Ver logs en tiempo real
railway logs --tail 100 --follow

# Ver solo logs del bot
railway logs --tail 200 | grep "\[TELEGRAM\]"

# Ver tu chat_id
curl https://tu-app.up.railway.app/api/omnichannel/get-chat-id/

# Ver usuarios vinculados
curl https://tu-app.up.railway.app/api/omnichannel/link-user/

# Ver estado del bot
curl https://tu-app.up.railway.app/api/omnichannel/status/
```

## ✅ Resultado Esperado

Si todo funciona correctamente, verás:

1. En los logs:
```
INFO ... [TELEGRAM] ✅ Mensaje enviado exitosamente. Message ID: 12345
```

2. En Telegram:
```
📚 Comandos Disponibles

/start - Iniciar el bot
/help - Ver esta ayuda
/status - Estado general del sistema
...
```

---

**Estado**: Logging detallado desplegado
**Próximo paso**: Enviar `/help` y compartir logs completos
