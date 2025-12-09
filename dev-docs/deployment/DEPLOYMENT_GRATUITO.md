# 🆓 Guía de Deployment Gratuito - Sistema CMMS

Esta guía te muestra cómo desplegar tu proyecto CMMS completamente **GRATIS** usando servicios en la nube.

---

## 📋 Tabla de Contenidos

1. [Opciones Disponibles](#opciones-disponibles)
2. [Opción Recomendada: Railway + Vercel](#opción-recomendada-railway--vercel)
3. [Alternativa 1: Render + Vercel](#alternativa-1-render--vercel)
4. [Alternativa 2: PythonAnywhere + Vercel](#alternativa-2-pythonanywhere--vercel)
5. [Alternativa 3: Fly.io + Vercel](#alternativa-3-flyio--vercel)
6. [Comparación de Opciones](#comparación-de-opciones)

---

## 🎯 Opciones Disponibles

### Servicios Gratuitos para Backend (Django)

| Servicio | Plan Gratuito | PostgreSQL | Redis | Celery | Recomendado |
|----------|---------------|------------|-------|--------|-------------|
| **Railway** | $5 crédito/mes | ✅ | ✅ | ✅ | ⭐⭐⭐⭐⭐ |
| **Render** | 750 hrs/mes | ✅ | ❌ | ⚠️ | ⭐⭐⭐⭐ |
| **Fly.io** | 3 VMs gratis | ✅ | ✅ | ✅ | ⭐⭐⭐⭐ |
| **PythonAnywhere** | 1 app gratis | ❌ SQLite | ❌ | ❌ | ⭐⭐⭐ |
| **Heroku** | Ya no gratis | - | - | - | ❌ |

### Servicios Gratuitos para Frontend (React)

| Servicio | Plan Gratuito | Build Time | Bandwidth | Recomendado |
|----------|---------------|------------|-----------|-------------|
| **Vercel** | Ilimitado | ✅ | 100GB/mes | ⭐⭐⭐⭐⭐ |
| **Netlify** | Ilimitado | ✅ | 100GB/mes | ⭐⭐⭐⭐⭐ |
| **Cloudflare Pages** | Ilimitado | ✅ | Ilimitado | ⭐⭐⭐⭐ |
| **GitHub Pages** | Ilimitado | ✅ | 100GB/mes | ⭐⭐⭐ |

---

## ⭐ Opción Recomendada: Railway + Vercel

**Mejor opción para tu proyecto CMMS completo con todas las funcionalidades.**

### ✅ Ventajas

- ✅ PostgreSQL incluido
- ✅ Redis incluido (para Celery)
- ✅ Celery Worker y Beat funcionan
- ✅ Variables de entorno fáciles
- ✅ Deploy automático desde GitHub
- ✅ Logs en tiempo real
- ✅ $5 de crédito gratis al mes
- ✅ Fácil de configurar

### ⚠️ Limitaciones

- $5/mes de crédito (suficiente para desarrollo/demo)
- Después de $5, necesitas agregar tarjeta

---

### 🚀 Paso a Paso: Railway + Vercel

#### Parte 1: Backend en Railway

**1. Crear cuenta en Railway**
- Ve a: https://railway.app/
- Regístrate con GitHub
- Obtienes $5 de crédito gratis

**2. Crear nuevo proyecto**
```bash
# En Railway Dashboard:
1. Click "New Project"
2. Selecciona "Deploy from GitHub repo"
3. Conecta tu cuenta de GitHub
4. Selecciona: proyecto-de-titulo-produccion
```

**3. Agregar PostgreSQL**
```bash
# En tu proyecto Railway:
1. Click "+ New"
2. Selecciona "Database"
3. Selecciona "PostgreSQL"
4. Railway creará la base de datos automáticamente
```

**4. Agregar Redis**
```bash
# En tu proyecto Railway:
1. Click "+ New"
2. Selecciona "Database"
3. Selecciona "Redis"
4. Railway creará Redis automáticamente
```

**5. Configurar Variables de Entorno**

En Railway, ve a tu servicio Django → Variables:

```bash
# Django
DEBUG=False
SECRET_KEY=tu-secret-key-super-segura-generada-aleatoriamente
ALLOWED_HOSTS=*.railway.app
DJANGO_SETTINGS_MODULE=config.settings.production

# Database (Railway lo genera automáticamente)
DATABASE_URL=${{Postgres.DATABASE_URL}}

# Redis (Railway lo genera automáticamente)
REDIS_URL=${{Redis.REDIS_URL}}

# Celery
CELERY_BROKER_URL=${{Redis.REDIS_URL}}
CELERY_RESULT_BACKEND=${{Redis.REDIS_URL}}

# Telegram Bot
TELEGRAM_BOT_TOKEN=tu-token-de-telegram
TELEGRAM_ENABLED=True

# Email (opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password
```

**6. Crear archivo railway.json**

Crea este archivo en la raíz del proyecto:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install -r backend/requirements-production.txt && python backend/manage.py collectstatic --noinput"
  },
  "deploy": {
    "startCommand": "cd backend && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

**7. Crear Procfile para Celery**

Necesitas crear servicios adicionales para Celery:

**Servicio 1: Django (ya configurado)**
```
Start Command: cd backend && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

**Servicio 2: Celery Worker**
```bash
# En Railway, duplica el servicio Django
# Cambia el Start Command a:
cd backend && celery -A config worker -l info
```

**Servicio 3: Celery Beat**
```bash
# En Railway, duplica el servicio Django
# Cambia el Start Command a:
cd backend && celery -A config beat -l info
```

**8. Ejecutar Migraciones**

```bash
# En Railway, ve a tu servicio Django
# Click en "Deploy" → "Run Command"
python backend/manage.py migrate
python backend/manage.py createsuperuser
```

**9. Obtener URL del Backend**

Railway te dará una URL como:
```
https://tu-proyecto.railway.app
```

---

#### Parte 2: Frontend en Vercel

**1. Crear cuenta en Vercel**
- Ve a: https://vercel.com/
- Regístrate con GitHub

**2. Importar proyecto**
```bash
1. Click "Add New" → "Project"
2. Importa: proyecto-de-titulo-produccion
3. Selecciona el directorio: frontend
```

**3. Configurar Build Settings**

```bash
Framework Preset: Vite
Build Command: npm run build
Output Directory: dist
Install Command: npm install
Root Directory: frontend
```

**4. Configurar Variables de Entorno**

En Vercel → Settings → Environment Variables:

```bash
VITE_API_URL=https://tu-proyecto.railway.app/api/v1
```

**5. Deploy**

```bash
Click "Deploy"
Vercel construirá y desplegará tu frontend automáticamente
```

**6. Obtener URL del Frontend**

Vercel te dará una URL como:
```
https://tu-proyecto.vercel.app
```

**7. Actualizar CORS en Backend**

Vuelve a Railway y agrega a las variables de entorno:

```bash
ALLOWED_HOSTS=*.railway.app,tu-proyecto.vercel.app
CORS_ALLOWED_ORIGINS=https://tu-proyecto.vercel.app
```

---

### ✅ Verificación

1. **Backend:** https://tu-proyecto.railway.app/api/docs/
2. **Frontend:** https://tu-proyecto.vercel.app
3. **Admin:** https://tu-proyecto.railway.app/admin/

---

## 🔄 Alternativa 1: Render + Vercel

**Buena opción si Railway no funciona para ti.**

### ✅ Ventajas

- ✅ 750 horas gratis al mes
- ✅ PostgreSQL incluido
- ✅ Deploy automático
- ✅ SSL gratis
- ✅ No requiere tarjeta de crédito

### ⚠️ Limitaciones

- ❌ No incluye Redis (Celery no funcionará)
- ⚠️ El servicio "duerme" después de 15 min de inactividad
- ⚠️ Tarda ~30 segundos en "despertar"

---

### 🚀 Paso a Paso: Render + Vercel

#### Parte 1: Backend en Render

**1. Crear cuenta en Render**
- Ve a: https://render.com/
- Regístrate con GitHub

**2. Crear Web Service**
```bash
1. Click "New +" → "Web Service"
2. Conecta GitHub
3. Selecciona: proyecto-de-titulo-produccion
4. Configuración:
   - Name: cmms-backend
   - Region: Oregon (US West)
   - Branch: main
   - Root Directory: backend
   - Runtime: Python 3
   - Build Command: pip install -r requirements-production.txt && python manage.py collectstatic --noinput
   - Start Command: gunicorn config.wsgi:application
```

**3. Crear PostgreSQL Database**
```bash
1. Click "New +" → "PostgreSQL"
2. Name: cmms-db
3. Database: cmms_prod
4. User: cmms_user
5. Region: Oregon (US West)
6. Plan: Free
```

**4. Configurar Variables de Entorno**

En tu Web Service → Environment:

```bash
DEBUG=False
SECRET_KEY=tu-secret-key-generada
ALLOWED_HOSTS=*.onrender.com
DATABASE_URL=postgresql://user:pass@host:5432/db
DJANGO_SETTINGS_MODULE=config.settings.production
TELEGRAM_BOT_TOKEN=tu-token
TELEGRAM_ENABLED=True
```

**5. Conectar Database**

Render te dará la URL de PostgreSQL, agrégala a `DATABASE_URL`

**6. Ejecutar Migraciones**

```bash
# En Render Shell (dentro del servicio):
python manage.py migrate
python manage.py createsuperuser
```

#### Parte 2: Frontend en Vercel

(Mismo proceso que con Railway)

---

## 🐍 Alternativa 2: PythonAnywhere + Vercel

**Opción más simple pero con limitaciones.**

### ✅ Ventajas

- ✅ Completamente gratis
- ✅ Fácil de configurar
- ✅ No requiere tarjeta
- ✅ Consola web incluida

### ⚠️ Limitaciones

- ❌ Solo SQLite (no PostgreSQL)
- ❌ No Redis (no Celery)
- ❌ No ML predictions automáticas
- ❌ No Bot de Telegram automático
- ⚠️ Funcionalidad limitada

---

### 🚀 Paso a Paso: PythonAnywhere

**1. Crear cuenta**
- Ve a: https://www.pythonanywhere.com/
- Regístrate (plan gratuito)

**2. Subir código**
```bash
# En PythonAnywhere Console:
git clone https://github.com/matiasmoralesa/proyecto-de-titulo-produccion.git
cd proyecto-de-titulo-produccion/backend
```

**3. Crear virtualenv**
```bash
mkvirtualenv --python=/usr/bin/python3.10 cmms-env
pip install -r requirements.txt
```

**4. Configurar Web App**
```bash
1. Web → Add a new web app
2. Manual configuration
3. Python 3.10
4. Configurar WSGI file
```

**5. Configurar WSGI**

Edita el archivo WSGI:

```python
import os
import sys

path = '/home/tu-usuario/proyecto-de-titulo-produccion/backend'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.production'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**6. Configurar Static Files**
```bash
URL: /static/
Directory: /home/tu-usuario/proyecto-de-titulo-produccion/backend/staticfiles/
```

**7. Ejecutar Migraciones**
```bash
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
```

---

## ✈️ Alternativa 3: Fly.io + Vercel

**Opción avanzada con más control.**

### ✅ Ventajas

- ✅ 3 VMs gratis
- ✅ PostgreSQL incluido
- ✅ Redis incluido
- ✅ Celery funciona
- ✅ Más control

### ⚠️ Limitaciones

- ⚠️ Requiere tarjeta de crédito (no cobra)
- ⚠️ Configuración más técnica

---

### 🚀 Paso a Paso: Fly.io

**1. Instalar Fly CLI**
```bash
# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex

# Mac/Linux
curl -L https://fly.io/install.sh | sh
```

**2. Login**
```bash
fly auth login
```

**3. Crear fly.toml**

En la raíz del proyecto:

```toml
app = "cmms-backend"

[build]
  builder = "paketobuildpacks/builder:base"
  buildpacks = ["gcr.io/paketo-buildpacks/python"]

[env]
  PORT = "8000"
  DJANGO_SETTINGS_MODULE = "config.settings.production"

[[services]]
  http_checks = []
  internal_port = 8000
  processes = ["app"]
  protocol = "tcp"
  script_checks = []

  [services.concurrency]
    hard_limit = 25
    soft_limit = 20
    type = "connections"

  [[services.ports]]
    force_https = true
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443

  [[services.tcp_checks]]
    grace_period = "1s"
    interval = "15s"
    restart_limit = 0
    timeout = "2s"
```

**4. Crear PostgreSQL**
```bash
fly postgres create --name cmms-db
fly postgres attach cmms-db
```

**5. Crear Redis**
```bash
fly redis create --name cmms-redis
```

**6. Deploy**
```bash
fly deploy
```

---

## 📊 Comparación de Opciones

### Funcionalidades Soportadas

| Funcionalidad | Railway | Render | PythonAnywhere | Fly.io |
|---------------|---------|--------|----------------|--------|
| **Django Backend** | ✅ | ✅ | ✅ | ✅ |
| **PostgreSQL** | ✅ | ✅ | ❌ SQLite | ✅ |
| **Redis** | ✅ | ❌ | ❌ | ✅ |
| **Celery Worker** | ✅ | ❌ | ❌ | ✅ |
| **Celery Beat** | ✅ | ❌ | ❌ | ✅ |
| **ML Predictions** | ✅ | ⚠️ Manual | ⚠️ Manual | ✅ |
| **Bot Telegram** | ✅ | ⚠️ Limitado | ❌ | ✅ |
| **Auto-scaling** | ✅ | ✅ | ❌ | ✅ |
| **SSL/HTTPS** | ✅ | ✅ | ✅ | ✅ |
| **Custom Domain** | ✅ | ✅ | ❌ | ✅ |

### Facilidad de Uso

| Aspecto | Railway | Render | PythonAnywhere | Fly.io |
|---------|---------|--------|----------------|--------|
| **Setup** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Configuración** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Deploy** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Mantenimiento** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

### Costos

| Servicio | Plan Gratuito | Límites | Después de Límite |
|----------|---------------|---------|-------------------|
| **Railway** | $5/mes crédito | ~500 hrs | $0.000231/GB-s |
| **Render** | 750 hrs/mes | Duerme después 15 min | $7/mes |
| **PythonAnywhere** | 1 app | Limitaciones | $5/mes |
| **Fly.io** | 3 VMs | 160GB transfer | $1.94/VM/mes |
| **Vercel** | Ilimitado | 100GB bandwidth | $20/mes |

---

## 🎯 Recomendación Final

### Para Proyecto Completo (Todas las Funcionalidades)

**🥇 Opción 1: Railway + Vercel**
- ✅ Todas las funcionalidades funcionan
- ✅ Fácil de configurar
- ✅ $5 gratis al mes (suficiente para demo)
- ✅ PostgreSQL + Redis incluidos
- ✅ Celery funciona
- ✅ ML predictions automáticas
- ✅ Bot de Telegram funciona

### Para Demo/Presentación Simple

**🥈 Opción 2: Render + Vercel**
- ✅ Gratis sin tarjeta
- ⚠️ Sin Celery (tareas manuales)
- ⚠️ Sin ML automático
- ✅ Funcionalidades principales funcionan

### Para Prueba Rápida

**🥉 Opción 3: PythonAnywhere + Vercel**
- ✅ Completamente gratis
- ❌ Funcionalidad muy limitada
- ✅ Bueno para mostrar UI

---

## 📝 Próximos Pasos

1. **Elige una opción** según tus necesidades
2. **Sigue la guía paso a paso** de la opción elegida
3. **Configura las variables de entorno**
4. **Haz el deploy**
5. **Prueba tu aplicación**

---

## 🆘 Troubleshooting

### Error: "Application failed to start"
```bash
# Verifica logs en el servicio
# Asegúrate que requirements.txt esté correcto
# Verifica que DATABASE_URL esté configurado
```

### Error: "Database connection failed"
```bash
# Verifica que DATABASE_URL esté correcto
# Asegúrate que PostgreSQL esté corriendo
# Verifica que las migraciones se ejecutaron
```

### Error: "Static files not found"
```bash
# Ejecuta collectstatic
python manage.py collectstatic --noinput

# Verifica STATIC_ROOT en settings
```

---

## 📞 Recursos Adicionales

- **Railway Docs:** https://docs.railway.app/
- **Render Docs:** https://render.com/docs
- **Vercel Docs:** https://vercel.com/docs
- **Fly.io Docs:** https://fly.io/docs/
- **PythonAnywhere Docs:** https://help.pythonanywhere.com/

---

**¡Éxito con tu deployment gratuito!** 🚀
