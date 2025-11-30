# 🚀 Deployment - Sistema CMMS

## ✅ Configuración Actual

- **Repositorio:** proyecto-de-titulo-produccion
- **URL:** https://github.com/matiasmoralesa/proyecto-de-titulo-produccion
- **Estrategia:** Railway (Backend) + Vercel (Frontend)
- **Git:** Configurado para subir solo a producción

---

## 📚 Documentación de Deployment

### 🎯 Guía Principal (EMPIEZA AQUÍ)

**DEPLOYMENT_RAILWAY_PASO_A_PASO.md**
- Guía completa paso a paso
- Instrucciones detalladas
- Troubleshooting incluido
- Tiempo estimado: 15-20 minutos

### 📖 Guías Adicionales

1. **QUICK_START_DEPLOYMENT.md**
   - Versión resumida
   - Para deployment rápido

2. **DEPLOYMENT_GRATUITO.md**
   - Todas las opciones gratuitas
   - Comparación de servicios
   - Alternativas a Railway

3. **DEPLOYMENT_GUIDE.md**
   - Guía avanzada
   - Deployment en VPS
   - Configuración manual

---

## 🔧 Archivos de Configuración

### Para Railway

- **railway.json** - Configuración principal de Railway
- **Procfile** - Definición de procesos (Django, Celery)
- **nixpacks.toml** - Configuración de build

### Para Backend

- **backend/requirements-production.txt** - Dependencias de producción
- **backend/config/settings/production.py** - Settings de producción

### Para Frontend

- **frontend/.env.example** - Template de variables de entorno
- **frontend/vite.config.ts** - Configuración de Vite

---

## 🚀 Inicio Rápido

### 1. Preparación (Ya completado ✅)

- [x] Repositorio en GitHub
- [x] Código actualizado
- [x] Git configurado para producción

### 2. Deployment Backend (Railway)

```bash
1. Crear cuenta: https://railway.app/
2. Conectar GitHub
3. Seleccionar: proyecto-de-titulo-produccion
4. Agregar PostgreSQL
5. Agregar Redis
6. Configurar variables de entorno
7. Crear servicios para Celery
```

**Guía detallada:** DEPLOYMENT_RAILWAY_PASO_A_PASO.md

### 3. Deployment Frontend (Vercel)

```bash
1. Crear cuenta: https://vercel.com/
2. Importar: proyecto-de-titulo-produccion
3. Root Directory: frontend
4. Agregar VITE_API_URL
5. Deploy
```

**Guía detallada:** DEPLOYMENT_RAILWAY_PASO_A_PASO.md

---

## 📊 Servicios Desplegados

### Backend (Railway)

| Servicio | Descripción | Start Command |
|----------|-------------|---------------|
| **Django** | API Backend | `gunicorn config.wsgi:application` |
| **PostgreSQL** | Base de datos | (Automático) |
| **Redis** | Cache y Celery broker | (Automático) |
| **Celery Worker** | Procesamiento de tareas | `celery -A config worker` |
| **Celery Beat** | Tareas programadas | `celery -A config beat` |

### Frontend (Vercel)

| Servicio | Descripción |
|----------|-------------|
| **React App** | Interfaz de usuario |

---

## 🔄 Workflow de Desarrollo

### Hacer Cambios

```bash
# 1. Hacer cambios en el código
# ...

# 2. Probar localmente
cd backend
python manage.py runserver

cd frontend
npm run dev

# 3. Commit y push
git add .
git commit -m "Descripción del cambio"
git push origin main

# 4. Railway y Vercel detectan el cambio y re-deploya automáticamente
```

### Ver Logs

**Railway:**
```bash
1. Ve a tu proyecto en Railway
2. Click en el servicio
3. Ve a "Deployments"
4. Click en el deployment activo
5. Verás logs en tiempo real
```

**Vercel:**
```bash
1. Ve a tu proyecto en Vercel
2. Click en "Deployments"
3. Click en el deployment
4. Ve a "Function Logs"
```

---

## 🔐 Variables de Entorno

### Backend (Railway)

```bash
# Django Core
DEBUG=False
SECRET_KEY=tu-secret-key-generada
ALLOWED_HOSTS=*.railway.app,tu-dominio.vercel.app
DJANGO_SETTINGS_MODULE=config.settings.production

# Database
DATABASE_URL=${{Postgres.DATABASE_URL}}

# Redis
REDIS_URL=${{Redis.REDIS_URL}}
CELERY_BROKER_URL=${{Redis.REDIS_URL}}
CELERY_RESULT_BACKEND=${{Redis.REDIS_URL}}

# CORS
CORS_ALLOWED_ORIGINS=https://tu-dominio.vercel.app

# Telegram (opcional)
TELEGRAM_BOT_TOKEN=tu-token
TELEGRAM_ENABLED=True

# Email (opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password
```

### Frontend (Vercel)

```bash
VITE_API_URL=https://tu-proyecto.railway.app/api/v1
```

---

## 📈 Monitoreo

### Métricas en Railway

- CPU Usage
- Memory Usage
- Network Traffic
- Request Count
- Response Time

### Métricas en Vercel

- Page Views
- Visitors
- Performance Score
- Build Time

---

## 💰 Costos

### Railway

```
Plan Gratuito: $5/mes de crédito

Uso estimado:
- Django: ~$2/mes
- PostgreSQL: ~$1/mes
- Redis: ~$0.50/mes
- Celery Worker: ~$1/mes
- Celery Beat: ~$0.50/mes
Total: ~$5/mes (GRATIS)
```

### Vercel

```
Plan Gratuito: Ilimitado

Límites:
- 100 GB bandwidth/mes
- Builds ilimitados

Uso estimado: ~5-10 GB/mes
Total: GRATIS
```

---

## 🐛 Troubleshooting

### Problemas Comunes

1. **Application failed to start**
   - Verifica logs en Railway
   - Revisa variables de entorno
   - Verifica requirements.txt

2. **Cannot connect to backend**
   - Verifica CORS_ALLOWED_ORIGINS
   - Verifica ALLOWED_HOSTS
   - Verifica VITE_API_URL en Vercel

3. **Database connection failed**
   - Verifica que PostgreSQL esté corriendo
   - Verifica DATABASE_URL
   - Ejecuta migraciones

4. **Frontend página en blanco**
   - Verifica VITE_API_URL
   - Revisa logs en Vercel
   - Re-deploy

**Guía completa:** DEPLOYMENT_RAILWAY_PASO_A_PASO.md (Sección Troubleshooting)

---

## 📞 Recursos

### Documentación

- **Railway Docs:** https://docs.railway.app/
- **Vercel Docs:** https://vercel.com/docs
- **Django Deployment:** https://docs.djangoproject.com/en/4.2/howto/deployment/

### Soporte

- **Railway Discord:** https://discord.gg/railway
- **Vercel Discord:** https://discord.gg/vercel

### Tu Proyecto

- **Repositorio:** https://github.com/matiasmoralesa/proyecto-de-titulo-produccion
- **Issues:** https://github.com/matiasmoralesa/proyecto-de-titulo-produccion/issues

---

## ✅ Checklist de Deployment

### Pre-Deployment

- [x] Código en GitHub
- [x] Git configurado
- [x] Archivos de configuración creados
- [ ] Cuenta de Railway
- [ ] Cuenta de Vercel

### Backend (Railway)

- [ ] Proyecto creado
- [ ] PostgreSQL agregado
- [ ] Redis agregado
- [ ] Variables de entorno configuradas
- [ ] Celery Worker creado
- [ ] Celery Beat creado
- [ ] Migraciones ejecutadas
- [ ] Superusuario creado

### Frontend (Vercel)

- [ ] Proyecto importado
- [ ] Build settings configurados
- [ ] VITE_API_URL configurado
- [ ] Deploy exitoso

### Conexión

- [ ] CORS configurado
- [ ] ALLOWED_HOSTS actualizado
- [ ] Frontend conecta con backend
- [ ] Login funciona

### Verificación

- [ ] API responde
- [ ] Admin accesible
- [ ] Frontend carga
- [ ] Dashboard muestra datos
- [ ] Celery funciona

---

## 🎯 Próximos Pasos

1. **Completa el deployment** siguiendo DEPLOYMENT_RAILWAY_PASO_A_PASO.md

2. **Verifica todas las funcionalidades**

3. **Configura dominio personalizado** (opcional)

4. **Configura Bot de Telegram** (opcional)

5. **Configura monitoreo avanzado** (opcional)

---

**¡Éxito con tu deployment!** 🚀

Para empezar, abre: **DEPLOYMENT_RAILWAY_PASO_A_PASO.md**
