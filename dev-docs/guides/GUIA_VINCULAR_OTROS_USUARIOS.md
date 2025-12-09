# 👥 Guía: Vincular Otros Usuarios con Telegram

## 🎯 3 Métodos Disponibles

### Método 1: Auto-Vinculación (Recomendado)

**El usuario se vincula solo**

**Instrucciones para el usuario**:
```
1. Abre Telegram
2. Busca el bot: @Somacorbot
3. Envía: /vincular tu_usuario tu_contraseña
```

**Ejemplo**:
```
/vincular operador1 mipassword123
```

**Ventajas**:
- ✅ No requiere intervención del admin
- ✅ Instantáneo
- ✅ Cada usuario controla su vinculación

---

### Método 2: Códigos Individuales

**Tú generas códigos para cada usuario**

#### Generar código para un usuario:

```bash
curl -X POST https://proyecto-de-titulo-produccion-production.up.railway.app/api/v1/bot/generate-code/ \
  -H "Content-Type: application/json" \
  -d '{"username": "operador1"}'
```

**Respuesta**:
```json
{
  "success": true,
  "code": "ABC123",
  "user": {
    "username": "operador1",
    "full_name": "Juan Pérez"
  },
  "expires_in_minutes": 5
}
```

#### Enviar al usuario:

```
Hola Juan,

Para vincular tu cuenta con Telegram:
1. Abre Telegram
2. Busca @Somacorbot
3. Envía: /vincular ABC123

El código expira en 5 minutos.
```

**Ventajas**:
- ✅ Más seguro (no usan contraseña)
- ✅ Tú controlas quién se vincula
- ✅ Código expira en 5 minutos

---

### Método 3: Códigos Masivos

**Genera códigos para todos los usuarios a la vez**

#### Ejecutar script:

```bash
cd backend
python generar_codigos_usuarios.py
```

**Resultado**:
```
═══════════════════════════════════════════
GENERADOR DE CÓDIGOS DE VINCULACIÓN
═══════════════════════════════════════════

📋 Usuarios encontrados: 5

✅ admin                → ABC123
✅ operador1            → XYZ789
✅ operador2            → DEF456
✅ supervisor1          → GHI012
✅ tecnico1             → JKL345

═══════════════════════════════════════════
💾 Códigos guardados en: codigos_telegram.txt
```

#### Distribuir códigos:

El archivo `codigos_telegram.txt` contiene:

```
Juan Pérez (@operador1)
Código: XYZ789
Instrucción: /vincular XYZ789
────────────────────────────────────────

María González (@operador2)
Código: DEF456
Instrucción: /vincular DEF456
────────────────────────────────────────
```

**Ventajas**:
- ✅ Genera todos los códigos a la vez
- ✅ Códigos válidos por 24 horas
- ✅ Archivo listo para distribuir

---

## 📋 Plantilla de Email/WhatsApp

```
Hola [Nombre],

Ya puedes recibir notificaciones del sistema CMMS en Telegram.

Para vincular tu cuenta:

1. Abre Telegram
2. Busca el bot: @Somacorbot
3. Envía uno de estos comandos:

   Opción A (con tu contraseña):
   /vincular [tu_usuario] [tu_contraseña]

   Opción B (con código):
   /vincular [CODIGO]

Una vez vinculado, recibirás:
• Notificaciones de órdenes de trabajo
• Alertas de predicciones de fallos
• Avisos críticos del sistema

¿Dudas? Contáctame.

Saludos,
[Tu nombre]
```

---

## 🔧 Comandos Útiles

### Generar código para un usuario específico:

```bash
# Usando el script
cd backend
python generar_codigos_usuarios.py operador1

# Usando curl
curl -X POST https://tu-app.up.railway.app/api/v1/bot/generate-code/ \
  -H "Content-Type: application/json" \
  -d '{"username": "operador1"}'
```

### Ver usuarios vinculados:

```bash
curl https://tu-app.up.railway.app/api/v1/bot/link-user/
```

### Generar códigos para todos:

```bash
cd backend
python generar_codigos_usuarios.py
```

---

## 📊 Proceso Recomendado

### Para Onboarding de Nuevos Usuarios:

1. **Crear usuario en el sistema**
2. **Generar código de vinculación**:
   ```bash
   python generar_codigos_usuarios.py nuevo_usuario
   ```
3. **Enviar código por email/WhatsApp**
4. **Usuario se vincula en Telegram**

### Para Usuarios Existentes:

**Opción A - Auto-vinculación**:
1. Enviar email con instrucciones
2. Usuarios se vinculan solos con `/vincular username password`

**Opción B - Con códigos**:
1. Generar códigos para todos
2. Distribuir códigos individualmente
3. Usuarios se vinculan con `/vincular CODIGO`

---

## ✅ Verificación

### Verificar que un usuario está vinculado:

```bash
curl https://tu-app.up.railway.app/api/v1/bot/link-user/ | grep "operador1"
```

### Probar notificaciones:

Una vez vinculado, el usuario puede probar con:
```
/status
/workorders
/predictions
```

---

## 🐛 Solución de Problemas

### Usuario dice "Credenciales incorrectas"

1. Verificar que el username sea correcto
2. Verificar que la contraseña sea correcta
3. Generar un código como alternativa

### Usuario dice "Código no encontrado"

1. Verificar que el código sea correcto (mayúsculas)
2. Verificar que no haya expirado (5 min para API, 24h para script)
3. Generar un nuevo código

### Usuario no recibe notificaciones

1. Verificar que esté vinculado:
   ```bash
   curl https://tu-app.up.railway.app/api/v1/bot/link-user/
   ```
2. Verificar que tenga órdenes de trabajo asignadas
3. Probar con `/workorders` en Telegram

---

## 📝 Resumen

| Método | Ventajas | Cuándo Usar |
|--------|----------|-------------|
| Auto-vinculación | Rápido, sin admin | Usuarios técnicos |
| Códigos individuales | Seguro, controlado | Onboarding |
| Códigos masivos | Eficiente para muchos | Despliegue inicial |

---

**Recomendación**: Usa **auto-vinculación** para usuarios técnicos y **códigos** para usuarios nuevos o menos técnicos.
