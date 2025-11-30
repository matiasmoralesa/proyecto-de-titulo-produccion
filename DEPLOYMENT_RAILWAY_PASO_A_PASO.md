# 🚀 Deployment con Railway - Guía Paso a Paso

Esta es tu guía personalizada para desplegar el Sistema CMMS en Railway + Vercel.

---

## ✅ Configuración Actual

- **Repositorio:** proyecto-de-titulo-produccion
- **URL GitHub:** https://github.com/matiasmoralesa/proyecto-de-titulo-produccion
- **Git configurado:** ✅ Solo sube a producción

---

## 📋 Checklist Pre-Deployment

Antes de empezar, asegúrate de tener:

- [x] Repositorio en GitHub (proyecto-de-titulo-produccion)
- [x] Código actualizado en el repositorio
- [ ] Cuenta de Railway (crear ahora)
- [ ] Cuenta de Vercel (crear ahora)
- [ ] Token de Telegram Bot (si quieres notificaciones)

---

## 🎯 PARTE 1: Backend en Railway (10 minutos)

### Paso 1: Crear Cuenta en Railway (2 minutos)

1. **Abre tu navegador** y ve a: https://railway.app/

2. **Click en "Login"** (arriba a la derecha)

3. **Selecciona "Login with GitHub"**

4. **Autoriza Railway** para acceder a tu cuenta de GitHub

5. **¡Listo!** Recibes $5 de crédito gratis al mes

---

### Paso 2: Crear Proyecto desde GitHub (2 minutos)

1. **En Railway Dashboard**, click en **"New Project"**

2. **Selecciona "Deploy from GitHub repo"**

3. **Busca y selecciona:** `proyecto-de-titulo-produccion`

4. **Click en el repositorio**

5. Railway empezará a deployar automáticamente
   - Verás logs en tiempo real
   - Espera a que termine (luz verde)

---

### Paso 3: Agregar PostgreSQL (1 minuto)

1. **En tu proyecto Railway**, click en **"+ New"** (arriba a la derecha)

2. **Selecciona "Database"**

3. **Click en "Add PostgreSQL"**

4. **¡Listo!** Railway crea la base de datos automáticamente
   - Se conectará automáticamente a tu servicio Django

---

### Paso 4: Agregar Redis (1 minuto)

1. **Click en "+ New"** otra vez

2. **Selecciona "Database"**

3. **Click en "Add Redis"**

4. **¡Listo!** Railway crea Redis automáticamente
   - Se conectará automáticamente a tu servicio Django

---

### Paso 5: Configurar Variables de Entorno (3 minutos)

1. **Click en tu servicio Django** (el primero que se creó)

2. **Ve a la pestaña "Variables"**

3. **Click en "RAW Editor"** (arriba a la derecha)

4. **Borra todo** y pega esto:

```bash
# Django Core
DEBUG=False
SECRET_KEY=django-insecure-cambia-esto-por-una-clave-muy-larga-y-aleatoria-de-50-caracteres-minimo
ALLOWED_HOSTS=*.railway.app
DJANGO_SETTINGS_MODULE=config.settings.production

# Database (Railway lo genera automáticamente)
DATABASE_URL=${{Postgres.DATABASE_URL}}

# Redis (Railway lo genera automáticamente)
REDIS_URL=${{Redis.REDIS_URL}}

# Celery
CELERY_BROKER_URL=${{Redis.REDIS_URL}}
CELERY_RESULT_BACKEND=${{Redis.REDIS_URL}}

# Telegram Bot (opcional - si no lo tienes, déjalo así)
TELEGRAM_BOT_TOKEN=tu-token-aqui-o-dejalo-vacio
TELEGRAM_ENABLED=False

# Email (opcional - para notificaciones por email)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password
```

5. **IMPORTANTE:** Cambia `SECRET_KEY` por una clave aleatoria
   - Puedes generarla aquí: https://djecrety.ir/
   - O usa: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

6. **Click "Add"** o presiona **Ctrl+S**

7. Railway **re-deployará automáticamente**
   - Espera a que termine (luz verde)

---

### Paso 6: Obtener URL del Backend (1 minuto)

1. **En tu servicio Django**, ve a la pestaña **"Settings"**

2. **Scroll hasta "Networking"**

3. **Click en "Generate Domain"**

4. Railway generará una URL como:
   ```
   https://proyecto-de-titulo-produccion-production.up.railway.app
   ```

5. **Copia esta URL** - la necesitarás para Vercel

6. **Verifica que funciona:**
   - Abre: `https://tu-url.railway.app/api/docs/`
   - Deberías ver la documentación de la API

---

### Paso 7: Crear Servicios para Celery (2 minutos)

#### Celery Worker

1. **Click "+ New"** en tu proyecto

2. **Selecciona "Empty Service"**

3. **Nombre:** `celery-worker`

4. **En Settings → Start Command:**
   ```bash
   cd backend && celery -A config worker -l info --pool=solo
   ```

5. **En Variables**, click "RAW Editor" y pega las **mismas variables** del servicio Django

6. **Deploy**

#### Celery Beat

1. **Click "+ New"** otra vez

2. **Selecciona "Empty Service"**

3. **Nombre:** `celery-beat`

4. **En Settings → Start Command:**
   ```bash
   cd backend && celery -A config beat -l info
   ```

5. **En Variables**, copia las **mismas variables** del servicio Django

6. **Deploy**

---

### ✅ Backend Completado!

Tu backend ahora está corriendo en Railway con:
- ✅ Django
- ✅ PostgreSQL
- ✅ Redis
- ✅ Celery Worker
- ✅ Celery Beat

**URL del Backend:** `https://tu-proyecto.railway.app`

**Verifica:**
- API Docs: `https://tu-proyecto.railway.app/api/docs/`
- Health Check: `https://tu-proyecto.railway.app/api/v1/health/`

---

## 🎨 PARTE 2: Frontend en Vercel (5 minutos)

### Paso 1: Crear Cuenta en Vercel (1 minuto)

1. **Abre tu navegador** y ve a: https://vercel.com/

2. **Click en "Sign Up"**

3. **Selecciona "Continue with GitHub"**

4. **Autoriza Vercel** para acceder a tu cuenta de GitHub

5. **¡Listo!**

---

### Paso 2: Importar Proyecto (1 minuto)

1. **En Vercel Dashboard**, click en **"Add New..."** → **"Project"**

2. **Busca:** `proyecto-de-titulo-produccion`

3. **Click en "Import"**

---

### Paso 3: Configurar Build Settings (2 minutos)

1. **Framework Preset:** Selecciona **"Vite"**

2. **Root Directory:** Click en "Edit" y escribe: `frontend`

3. **Build Command:** (debería estar automático)
   ```bash
   npm run build
   ```

4. **Output Directory:** (debería estar automático)
   ```bash
   dist
   ```

5. **Install Command:** (debería estar automático)
   ```bash
   npm install
   ```

---

### Paso 4: Agregar Variable de Entorno (1 minuto)

1. **Scroll hasta "Environment Variables"**

2. **Agrega:**
   - **Name:** `VITE_API_URL`
   - **Value:** `https://tu-proyecto.railway.app/api/v1`
     (Usa la URL de Railway que copiaste antes)

3. **Click "Add"**

---

### Paso 5: Deploy (automático)

1. **Click "Deploy"**

2. Vercel construirá y desplegará automáticamente
   - Verás logs en tiempo real
   - Espera 2-3 minutos

3. **¡Listo!** Vercel te dará una URL como:
   ```
   https://proyecto-de-titulo-produccion.vercel.app
   ```

---

### ✅ Frontend Completado!

Tu frontend ahora está corriendo en Vercel.

**URL del Frontend:** `https://tu-proyecto.vercel.app`

---

## 🔗 PARTE 3: Conectar Frontend y Backend (2 minutos)

### Paso 1: Actualizar CORS en Railway

1. **Ve a Railway**

2. **Click en tu servicio Django**

3. **Ve a la pestaña "Variables"**

4. **Agrega estas dos variables:**

```bash
CORS_ALLOWED_ORIGINS=https://tu-proyecto.vercel.app
ALLOWED_HOSTS=*.railway.app,tu-proyecto.vercel.app
```

5. **Reemplaza** `tu-proyecto.vercel.app` con tu URL real de Vercel

6. **Save** (Railway re-deployará automáticamente)

---

### Paso 2: Verificar Conexión

1. **Abre tu frontend:** `https://tu-proyecto.vercel.app`

2. **Intenta hacer login:**
   - Si no tienes usuario, primero créalo en el admin de Railway

3. **Si funciona, ¡todo está conectado!** 🎉

---

## 🔧 PARTE 4: Configuración Inicial (5 minutos)

### Crear Superusuario

Necesitas crear un usuario administrador para acceder al sistema.

**Opción 1: Desde Railway Dashboard**

1. **Ve a Railway**

2. **Click en tu servicio Django**

3. **Ve a la pestaña "Deployments"**

4. **Click en el deployment activo** (el que tiene luz verde)

5. **Scroll hasta abajo** y verás una sección de "Shell" o "Console"

6. **Ejecuta:**
   ```bash
   cd backend && python manage.py createsuperuser
   ```

7. **Sigue las instrucciones:**
   - Username: admin
   - Email: tu-email@ejemplo.com
   - Password: (elige una contraseña segura)

**Opción 2: Desde Railway CLI (si lo instalaste)**

```bash
railway run python backend/manage.py createsuperuser
```

---

### Ejecutar Migraciones (si es necesario)

Si ves errores de base de datos:

```bash
# En Railway Shell:
cd backend && python manage.py migrate
```

---

### Cargar Datos Iniciales (opcional)

Si quieres datos de prueba:

```bash
# En Railway Shell:
cd backend && python manage.py create_roles
cd backend && python manage.py create_sample_locations
```

---

## ✅ ¡DEPLOYMENT COMPLETADO!

### 🎉 URLs de tu Proyecto:

- **Frontend:** https://tu-proyecto.vercel.app
- **Backend API:** https://tu-proyecto.railway.app/api/v1
- **API Docs:** https://tu-proyecto.railway.app/api/docs/
- **Admin:** https://tu-proyecto.railway.app/admin/

### 📊 Servicios Activos:

- ✅ Django Backend (Railway)
- ✅ PostgreSQL Database (Railway)
- ✅ Redis Cache (Railway)
- ✅ Celery Worker (Railway)
- ✅ Celery Beat (Railway)
- ✅ React Frontend (Vercel)

---

## 🔍 Verificación Final

### Checklist de Funcionalidades:

```bash
# Backend
✅ API responde: https://tu-proyecto.railway.app/api/v1/health/
✅ Admin accesible: https://tu-proyecto.railway.app/admin/
✅ API Docs: https://tu-proyecto.railway.app/api/docs/

# Frontend
✅ Página carga: https://tu-proyecto.vercel.app
✅ Login funciona
✅ Dashboard muestra datos

# Base de Datos
✅ PostgreSQL conectado
✅ Migraciones ejecutadas
✅ Superusuario creado

# Celery
✅ Worker corriendo
✅ Beat corriendo
✅ Tareas programadas activas
```

---

## 🔄 Actualizaciones Futuras

Ahora que Git está configurado para el repositorio de producción:

```bash
# Hacer cambios en el código
# ...

# Commit y push
git add .
git commit -m "Descripción del cambio"
git push origin main

# Railway y Vercel detectarán el cambio y re-deployarán automáticamente
```

---

## 📊 Monitoreo

### Railway Dashboard

1. **Ve a tu proyecto en Railway**

2. **Verás métricas en tiempo real:**
   - CPU usage
   - Memory usage
   - Network traffic
   - Logs en vivo

3. **Para ver logs:**
   - Click en cualquier servicio
   - Ve a "Deployments"
   - Click en el deployment activo
   - Verás logs en tiempo real

### Vercel Analytics

1. **Ve a tu proyecto en Vercel**

2. **Click en "Analytics"**

3. **Verás:**
   - Visitors
   - Page views
   - Performance metrics

---

## 💰 Costos

### Railway

```
Plan Gratuito: $5 de crédito al mes

Uso estimado:
- Django: ~$2/mes
- PostgreSQL: ~$1/mes
- Redis: ~$0.50/mes
- Celery Worker: ~$1/mes
- Celery Beat: ~$0.50/mes
Total: ~$5/mes (GRATIS con el crédito)
```

### Vercel

```
Plan Gratuito: Ilimitado

Límites:
- 100 GB bandwidth/mes
- Builds ilimitados

Para tu proyecto: ~5-10 GB/mes
Completamente GRATIS
```

---

## 🐛 Troubleshooting

### Error: "Application failed to start"

```bash
# En Railway:
1. Ve a Deployments
2. Click en el deployment fallido
3. Lee los logs
4. Busca el error específico

# Errores comunes:
- Falta SECRET_KEY → Agrégala en Variables
- Falta DATABASE_URL → Verifica que PostgreSQL esté conectado
- Error en requirements.txt → Verifica que el archivo exista
```

### Error: "Cannot connect to backend"

```bash
# Verifica:
1. Backend está corriendo (luz verde en Railway)
2. VITE_API_URL en Vercel es correcto
3. CORS_ALLOWED_ORIGINS en Railway incluye tu URL de Vercel
4. ALLOWED_HOSTS en Railway incluye ambas URLs
```

### Error: "Database connection failed"

```bash
# En Railway:
1. Verifica que PostgreSQL esté corriendo
2. Verifica que DATABASE_URL esté en Variables
3. Ejecuta migraciones manualmente:
   cd backend && python manage.py migrate
```

### Frontend muestra página en blanco

```bash
# En Vercel:
1. Ve a Deployments
2. Click en el deployment
3. Ve a "Function Logs"
4. Busca errores

# Solución común:
1. Verifica que VITE_API_URL esté configurado
2. Re-deploy el frontend
```

---

## 📞 Recursos

- **Railway Docs:** https://docs.railway.app/
- **Vercel Docs:** https://vercel.com/docs
- **Tu Repositorio:** https://github.com/matiasmoralesa/proyecto-de-titulo-produccion

---

## ✅ Próximos Pasos

1. **Prueba todas las funcionalidades** del sistema

2. **Configura el Bot de Telegram** (si quieres):
   - Obtén un token de @BotFather
   - Agrégalo a las variables de Railway
   - Cambia `TELEGRAM_ENABLED=True`

3. **Personaliza tu dominio** (opcional):
   - Railway: Settings → Domains
   - Vercel: Settings → Domains

4. **Configura backups** (Railway hace backups automáticos de PostgreSQL)

---

**¡Felicitaciones! Tu Sistema CMMS está en producción.** 🎉

**¿Problemas?** Revisa la sección de Troubleshooting o consulta los logs en Railway/Vercel.
