# 🔗 Vincular Usuario por Username

## ✅ Nueva Funcionalidad

Ahora puedes vincular usuarios usando su **username** en lugar del user_id. ¡Mucho más fácil!

## 🚀 Despliegue

✅ Código desplegado
⏱️ Espera 2-3 minutos

## 🔗 Cómo Vincular

### Opción 1: Por Username (Nuevo - Más Fácil)

**¿Cuál es tu username en el sistema?** (Ej: admin, matias, operador1, etc.)

```bash
curl -X POST https://proyecto-de-titulo-produccion-production.up.railway.app/api/omnichannel/link-user/ \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"TU_USERNAME\", \"chat_id\": \"5457419782\"}"
```

**Ejemplo con username "admin"**:
```bash
curl -X POST https://proyecto-de-titulo-produccion-production.up.railway.app/api/omnichannel/link-user/ \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"admin\", \"chat_id\": \"5457419782\"}"
```

**En PowerShell**:
```powershell
$body = @{
    username = "admin"
    chat_id = "5457419782"
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://proyecto-de-titulo-produccion-production.up.railway.app/api/omnichannel/link-user/" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"
```

**En el navegador (F12 → Console)**:
```javascript
fetch('https://proyecto-de-titulo-produccion-production.up.railway.app/api/omnichannel/link-user/', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    username: 'admin',  // Cambia esto por tu username
    chat_id: '5457419782'
  })
})
.then(r => r.json())
.then(data => {
  console.log('✅ Resultado:', data);
  alert(data.message);
})
```

### Opción 2: Por User ID (Original)

Si conoces tu user_id:

```bash
curl -X POST https://proyecto-de-titulo-produccion-production.up.railway.app/api/omnichannel/link-user/ \
  -H "Content-Type: application/json" \
  -d "{\"user_id\": 1, \"chat_id\": \"5457419782\"}"
```

## 📋 Información Necesaria

- **Tu username**: El nombre de usuario con el que inicias sesión en el sistema
- **Tu chat_id**: `5457419782` (ya lo tenemos de los logs)

## ✅ Verificar la Vinculación

```bash
curl https://proyecto-de-titulo-produccion-production.up.railway.app/api/omnichannel/link-user/
```

Respuesta esperada:
```json
{
  "success": true,
  "users": [
    {
      "user_id": 1,
      "username": "admin",
      "full_name": "Administrador",
      "chat_id": "5457419782",
      "is_enabled": true
    }
  ],
  "total": 1
}
```

## 🧪 Probar el Bot

### Paso 1: Esperar el Despliegue (2-3 minutos)

```bash
railway logs --tail 10
```

### Paso 2: Vincular Tu Usuario

Usa el comando de arriba con tu username.

### Paso 3: Probar en Telegram

1. Abre Telegram
2. Envía `/start` al bot
3. Presiona los botones
4. **¡Deberían funcionar!**

### Paso 4: Verificar en los Logs

```bash
railway logs --tail 50
```

Deberías ver:
```
INFO ... views User found: admin  ← ¡Tu username!
INFO ... views Message edited successfully
```

## 🎯 Ejemplos de Uso

### Vincular usuario "admin"
```bash
curl -X POST https://proyecto-de-titulo-produccion-production.up.railway.app/api/omnichannel/link-user/ \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"admin\", \"chat_id\": \"5457419782\"}"
```

### Vincular usuario "matias"
```bash
curl -X POST https://proyecto-de-titulo-produccion-production.up.railway.app/api/omnichannel/link-user/ \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"matias\", \"chat_id\": \"5457419782\"}"
```

### Vincular usuario "operador1"
```bash
curl -X POST https://proyecto-de-titulo-produccion-production.up.railway.app/api/omnichannel/link-user/ \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"operador1\", \"chat_id\": \"5457419782\"}"
```

## 🐛 Solución de Problemas

### Error: "Usuario con username X no encontrado"

**Causa**: El username no existe en el sistema

**Solución**: Verifica el username correcto. Puedes ver los usuarios disponibles en el panel de administración del sistema.

### Error: "chat_id es requerido"

**Causa**: Falta el chat_id en la petición

**Solución**: Asegúrate de incluir `"chat_id": "5457419782"` en el JSON

### Error: "Debes proporcionar user_id o username"

**Causa**: No se proporcionó ni user_id ni username

**Solución**: Incluye al menos uno: `"username": "admin"` o `"user_id": 1`

## ✅ Checklist

- [ ] Despliegue completado (2-3 minutos)
- [ ] Conoces tu username del sistema
- [ ] Ejecutaste el comando de vinculación
- [ ] Verificaste con `/api/omnichannel/link-user/`
- [ ] Probaste `/start` en Telegram
- [ ] Los botones funcionan correctamente

---

**Tu Chat ID**: `5457419782`
**Acción**: Ejecuta el comando con tu username
**Tiempo**: 5 minutos total
