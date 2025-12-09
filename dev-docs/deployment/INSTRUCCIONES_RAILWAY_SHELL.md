# 🖥️ Cómo Usar el Shell de Railway - Guía Visual

## 📍 Paso 1: Acceder a Railway

1. Abre tu navegador
2. Ve a: **https://railway.app/**
3. Inicia sesión con tu cuenta

## 📍 Paso 2: Seleccionar tu Proyecto

1. En el dashboard, verás todos tus proyectos
2. Busca tu proyecto (probablemente se llama algo como "proyecto-de-titulo-produccion")
3. Haz clic en el proyecto

## 📍 Paso 3: Seleccionar el Servicio de Backend

1. Verás varios servicios (Backend, PostgreSQL, etc.)
2. Haz clic en el servicio de **Backend** (el que tiene tu código Django)
3. NO hagas clic en PostgreSQL, necesitas el servicio de la aplicación

## 📍 Paso 4: Redeploy (Importante)

Antes de cargar datos, asegúrate de que Railway tiene los archivos más recientes:

1. Haz clic en la pestaña **"Settings"** (arriba)
2. Busca la sección **"Service"**
3. Haz clic en el botón **"Redeploy"**
4. Espera 2-3 minutos a que termine el deploy
5. Verás un indicador verde cuando esté listo

## 📍 Paso 5: Abrir el Shell

1. Haz clic en la pestaña **"Deployments"** (arriba)
2. Verás una lista de deployments
3. El deployment activo tiene un **punto verde** al lado
4. Haz clic en ese deployment (el que tiene el punto verde)
5. Busca y haz clic en el botón **"Shell"** o **"Terminal"**
   - Puede estar arriba a la derecha
   - O en un menú de 3 puntos (⋮)
6. Se abrirá una terminal negra en tu navegador

## 📍 Paso 6: Ejecutar Comandos

Ahora estás en el shell de Railway. Copia y pega estos comandos **UNO POR UNO**:

### Comando 1: Cargar Roles

```bash
python backend/manage.py loaddata backend/roles_export.json
```

**Presiona Enter**

Deberías ver algo como:
```
Installed 3 object(s) from 1 fixture(s)
```

✅ Si ves esto, ¡funcionó!

### Comando 2: Cargar Plantillas de Checklist

```bash
python backend/manage.py loaddata backend/checklist_templates_export.json
```

**Presiona Enter**

Deberías ver:
```
Installed 5 object(s) from 1 fixture(s)
```

✅ ¡5 plantillas cargadas!

### Comando 3: Cargar Prioridades

```bash
python backend/manage.py loaddata backend/priorities_export.json
```

**Presiona Enter**

### Comando 4: Cargar Tipos de Orden de Trabajo

```bash
python backend/manage.py loaddata backend/workorder_types_export.json
```

**Presiona Enter**

### Comando 5: Cargar Categorías de Activos

```bash
python backend/manage.py loaddata backend/asset_categories_export.json
```

**Presiona Enter**

### Comando 6: Cargar Ubicaciones

```bash
python backend/manage.py loaddata backend/locations_export.json
```

**Presiona Enter**

## 📍 Paso 7: Verificar que Todo se Cargó

Ejecuta este comando para verificar:

```bash
python backend/check_production_data.py
```

**Presiona Enter**

Deberías ver:

```
🔍 VERIFICACIÓN DE DATOS DE PRODUCCIÓN
========================================

📋 Roles de Usuario:
   Total: 3
   ✅ ADMIN
   ✅ SUPERVISOR
   ✅ OPERADOR

📋 Plantillas de Checklist:
   Total: 5
   ✅ SUPERSUCKER-CH01: Check List Camión Supersucker (15 items)
   ✅ F-PR-020-CH01: Check List Camionetas MDO (24 items)
   ...

✅ VERIFICACIÓN EXITOSA
   Todos los datos esenciales están presentes
```

## 📍 Paso 8: Crear Usuario Administrador

Ahora que los datos están cargados, crea tu usuario admin:

```bash
python backend/manage.py createsuperuser
```

Te pedirá:

1. **Username**: Escribe `admin` (o el nombre que quieras)
2. **Email**: Escribe tu email
3. **Password**: Escribe una contraseña segura
4. **Password (again)**: Repite la contraseña

✅ ¡Usuario creado!

## 📍 Paso 9: Probar el Sistema

1. Cierra el shell de Railway
2. Abre tu frontend en Vercel (tu URL de Vercel)
3. Inicia sesión con el usuario que acabas de crear
4. Ve a la sección de **Checklists**
5. Deberías ver las 5 plantillas disponibles

## ❌ Si Algo Sale Mal

### Error: "No such file or directory"

**Problema**: Railway no tiene los archivos JSON

**Solución**:
1. Verifica que hiciste push a GitHub: `git log --oneline -1`
2. Haz redeploy en Railway (Paso 4)
3. Espera a que termine el deploy
4. Intenta de nuevo

### Error: "Duplicate key value violates unique constraint"

**Problema**: Los datos ya están cargados

**Solución**: ¡Esto es bueno! Significa que los datos ya están ahí. Puedes ignorar este error.

### Error: "could not translate host name"

**Problema**: Estás ejecutando en tu máquina local en lugar de Railway

**Solución**: Asegúrate de estar en el **Shell de Railway**, no en tu terminal local.

### El Shell no se abre

**Problema**: A veces Railway tiene problemas con el shell

**Solución**:
1. Refresca la página
2. Intenta de nuevo
3. O usa Railway CLI: `railway shell`

## 💡 Consejos

- **Copia y pega** los comandos para evitar errores de tipeo
- **Espera** a que cada comando termine antes de ejecutar el siguiente
- **Lee los mensajes** que aparecen, te dirán si funcionó o no
- **No cierres** el shell hasta terminar todos los comandos
- Si algo falla, puedes **ejecutar los comandos de nuevo** sin problema

## 🎉 ¡Listo!

Una vez que veas "✅ VERIFICACIÓN EXITOSA", tu sistema está listo para usar.

Puedes:
- Iniciar sesión en tu frontend
- Crear activos
- Crear órdenes de trabajo
- Usar las plantillas de checklist
- Gestionar usuarios

## 📞 ¿Necesitas Ayuda?

Si algo no funciona:

1. Revisa los **logs** en Railway (pestaña "Logs")
2. Verifica que el **deploy terminó** correctamente
3. Asegúrate de estar en el **shell correcto** (Railway, no local)
4. Intenta **ejecutar los comandos uno por uno** en lugar de todos juntos
