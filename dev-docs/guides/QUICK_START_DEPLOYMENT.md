# 🚀 Quick Start - Deployment Gratuito en 15 Minutos

Esta guía te permite desplegar tu proyecto CMMS **GRATIS** en menos de 15 minutos.

---

## ⚡ Opción Rápida: Railway + Vercel

### ✅ Lo que obtendrás:

- ✅ Backend Django funcionando
- ✅ Frontend React funcionando
- ✅ PostgreSQL configurado
- ✅ Redis configurado
- ✅ Celery funcionando
- ✅ ML predictions automáticas
- ✅ Bot de Telegram activo
- ✅ HTTPS automático
- ✅ $5 de crédito gratis al mes

---

## 📋 Requisitos Previos (2 minutos)

1. ✅ Cuenta de GitHub (ya la tienes)
2. ✅ Repositorios creados (ya los tienes)
3. ⬜ Cuenta de Railway (crear ahora)
4. ⬜ Cuenta de Vercel (crear ahora)

---

## 🎯 Paso 1: Backend en Railway (8 minutos)

### 1.1 Crear Cuenta (1 min)

```
1. Ve a: https://railway.app/
2. Click "Login with GitHub"
3. Autoriza Railway
4. ¡Listo! Tienes $5 de crédito gratis
```

### 1.2 Crear Proyecto (1 min)

```
1. Click "New Project"
2. Selecciona "Deploy from GitHub repo"
3. Busca: proyecto-de-titulo-produccion
4. Click en el repositorio
5. Railway empezará a deployar automáticamente
```

### 1.3 Agregar PostgreSQL (1 min)

```
1. En tu proyecto, click "+ New"
2. Selecciona "Database"
3. Click "Add PostgreSQL"
4. ¡Listo! Railway crea la DB automáticamente
```

### 1.4 Agregar Redis (1 min)

```
1. Click "+ New" otra vez
2. Selecciona "Database"
3. Click "Add Redis"
4. ¡Listo! Railway crea Redis automáticamente
```

### 1.5 Configurar Variables de Entorno (3 minutos)

```
1. Click en tu servicio Django (el primero)
2. Ve a la pestaña "Variables"
3. Click "RAW Editor"
4. Pega esto (reemplaza los valores):
```

```bash
DEBUG=False
SECRET_KEY=cambia-esto-por-una-clave-aleatoria-muy-larga-y-segura
ALLOWED_HOSTS=*.railway.app
DJANGO_SETTINGS_MODULE=config.settings.production
DATABASE_URL=${{Postgres.DATABASE_URL}}
REDIS_URL=${{Redis.REDIS_URL}}
CELERY_BROKER_URL=${{Redis.REDIS_URL}}
CELERY_RESULT_BACKEND=${{Redis.REDIS_URL}}
TELEGRAM_BOT_TOKEN=tu-token-de-telegram-aqui
TELEGRAM_ENABLED=True
```

```
5. Click "Add" o "Save"
6. Railway re-deployará automáticamente
```

### 1.6 Ejecutar Migraciones (1 min)

```
1. Espera a que el deploy termine (luz verde)
2. Click en tu servicio Django
3. Ve a la pestaña "Settings"
4. Scroll hasta "Service Domains"
5. Copia la URL (ej: https://tu-proyecto.railway.app)
6. Ve a la pestaña "Deployments"
7. Click en el deployment activo
8. Click "View Logs"
9. Busca si hay errores
```

Para ejecutar migraciones manualmente:

```bash
# Opción 1: Desde Railway CLI (si lo instalaste)
railway run python backend/manage.py migrate
railway run python backend/manage.py createsuperuser

# Opción 2: Agregar a railway.json (ya está incluido)
# Las migraciones se ejecutarán automáticamente en el próximo deploy
```

### 1.7 Crear Servicios para Celery (1 min)

```
1. Click "+ New" en tu proyecto
2. Selecciona "Empty Service"
3. Nombre: "celery-worker"
4. En Settings → Start Command:
   cd backend && celery -A config worker -l info --pool=solo
5. En Variables, copia las mismas variables del servicio Django
6. Deploy

Repite para Celery Beat:
1. Click "+ New"
2. Nombre: "celery-beat"
3. Start Command:
   cd backend && celery -A config beat -l info
4. Copia las variables
5. Deploy
```

### ✅ Backend Listo!

Tu backend estará en: `https://tu-proyecto.railway.app`

Verifica:
- API Docs: `https://tu-proyecto.railway.app/api/docs/`
- Admin: `https://tu-proyecto.railway.app/admin/`

---

## 🎨 Paso 2: Frontend en Vercel (5 minutos)

### 2.1 Crear Cuenta (1 min)

```
1. Ve a: https://vercel.com/
2. Click "Sign Up"
3. Selecciona "Continue with GitHub"
4. Autoriza Vercel
5. ¡Listo!
```

### 2.2 Importar Proyecto (1 min)

```
1. Click "Add New..." → "Project"
2. Busca: proyecto-de-titulo-produccion
3. Click "Import"
```

### 2.3 Configurar Build (2 minutos)

```
1. Framework Preset: Vite
2. Root Directory: frontend
3. Build Command: npm run build
4. Output Directory: dist
5. Install Command: npm install
```

### 2.4 Agregar Variable de Entorno (1 min)

```
1. Scroll hasta "Environment Variables"
2. Agrega:
   Name: VITE_API_URL
   Value: https://tu-proyecto.railway.app/api/v1
   (Usa la URL de Railway del Paso 1)
3. Click "Add"
```

### 2.5 Deploy (automático)

```
1. Click "Deploy"
2. Vercel construirá y desplegará automáticamente
3. Espera 2-3 minutos
```

### ✅ Frontend Listo!

Tu frontend estará en: `https://tu-proyecto.vercel.app`

---

## 🔗 Paso 3: Conectar Frontend y Backend (2 minutos)

### 3.1 Actualizar CORS en Railway

```
1. Ve a Railway
2. Click en tu servicio Django
3. Ve a Variables
4. Agrega estas variables:
```

```bash
CORS_ALLOWED_ORIGINS=https://tu-proyecto.vercel.app
ALLOWED_HOSTS=*.railway.app,tu-proyecto.vercel.app
```

```
5. Save
6. Railway re-deployará automáticamente
```

### 3.2 Verificar Conexión

```
1. Abre tu frontend: https://tu-proyecto.vercel.app
2. Intenta hacer login
3. Si funciona, ¡todo está conectado!
```

---

## ✅ ¡Deployment Completo!

### 🎉 URLs de tu Proyecto:

- **Frontend:** https://tu-proyecto.vercel.app
- **Backend API:** https://tu-proyecto.railway.app/api/v1
- **API Docs:** https://tu-proyecto.railway.app/api/docs/
- **Admin:** https://tu-proyecto.railway.app/admin/

### 📊 Servicios Activos:

- ✅ Django Backend
- ✅ PostgreSQL Database
- ✅ Redis Cache
- ✅ Celery Worker
- ✅ Celery Beat
- ✅ React Frontend

---

## 🔍 Verificación

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

# Celery
✅ Worker corriendo
✅ Beat corriendo
✅ Tareas programadas activas

# Funcionalidades
✅ Gestión de activos
✅ Órdenes de trabajo
✅ Notificaciones
✅ ML Predictions (si configuraste el modelo)
✅ Bot de Telegram (si configuraste el token)
```

---

## 🐛 Troubleshooting Rápido

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
3. Ejecuta migraciones manualmente si es necesario
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

## 📈 Monitoreo

### Railway Dashboard

```
1. Ve a tu proyecto en Railway
2. Verás métricas en tiempo real:
   - CPU usage
   - Memory usage
   - Network traffic
   - Logs en vivo
```

### Vercel Analytics

```
1. Ve a tu proyecto en Vercel
2. Click en "Analytics"
3. Verás:
   - Visitors
   - Page views
   - Performance metrics
```

---

## 💰 Costos

### Railway (Backend)

```
Plan Gratuito: $5 de crédito al mes

Uso estimado para tu proyecto:
- Django: ~$2/mes
- PostgreSQL: ~$1/mes
- Redis: ~$0.50/mes
- Celery Worker: ~$1/mes
- Celery Beat: ~$0.50/mes
Total: ~$5/mes (GRATIS con el crédito)

Si excedes $5:
- Agrega tarjeta de crédito
- Pagas solo lo que uses
- ~$0.000231 por GB-segundo
```

### Vercel (Frontend)

```
Plan Gratuito: Ilimitado

Límites:
- 100 GB bandwidth/mes
- Builds ilimitados
- Deployments ilimitados

Para tu proyecto:
- Uso estimado: ~5-10 GB/mes
- Completamente GRATIS
```

---

## 🔄 Actualizaciones

### Actualizar Backend

```bash
# Opción 1: Push a GitHub (automático)
git add .
git commit -m "Update backend"
git push produccion main
# Railway detecta el cambio y re-deploya automáticamente

# Opción 2: Manual en Railway
1. Ve a Deployments
2. Click "Deploy"
```

### Actualizar Frontend

```bash
# Push a GitHub (automático)
git add .
git commit -m "Update frontend"
git push produccion main
# Vercel detecta el cambio y re-deploya automáticamente
```

---

## 🎓 Próximos Pasos

### Optimizaciones Opcionales:

1. **Custom Domain**
   - Railway: Settings → Domains
   - Vercel: Settings → Domains

2. **Monitoreo Avanzado**
   - Agregar Sentry para error tracking
   - Configurar alertas en Railway

3. **Backups**
   - Railway hace backups automáticos de PostgreSQL
   - Configura backups adicionales si necesitas

4. **Scaling**
   - Railway escala automáticamente
   - Ajusta workers de Gunicorn si necesitas

---

## 📞 Recursos

- **Railway Docs:** https://docs.railway.app/
- **Vercel Docs:** https://vercel.com/docs
- **Guía Completa:** Ver DEPLOYMENT_GRATUITO.md
- **Troubleshooting:** Ver DEPLOYMENT_GUIDE.md

---

## ✅ Resumen

**Tiempo total:** ~15 minutos  
**Costo:** $0 (gratis con créditos)  
**Resultado:** Sistema CMMS completo en producción

### Lo que lograste:

- ✅ Backend Django en Railway
- ✅ Frontend React en Vercel
- ✅ PostgreSQL configurado
- ✅ Redis configurado
- ✅ Celery funcionando
- ✅ HTTPS automático
- ✅ Deploy automático desde GitHub
- ✅ Logs en tiempo real
- ✅ Monitoreo incluido

**¡Felicitaciones! Tu proyecto está en producción.** 🎉

---

**¿Problemas?** Consulta DEPLOYMENT_GRATUITO.md para más opciones y troubleshooting detallado.
