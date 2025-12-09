# Sistema CMMS - Versión de Producción

> **⚠️ IMPORTANTE:** Este es el repositorio de PRODUCCIÓN. No hacer cambios directos aquí.
> Todos los cambios deben hacerse en el repositorio de desarrollo y luego deployarse.

## 🚀 Información del Sistema

**Versión:** 1.0.0  
**Estado:** 🟢 Production Ready  
**Última Actualización:** Noviembre 2025

## 📋 Descripción

Sistema de Gestión de Mantenimiento Computarizado (CMMS) para activos industriales con:
- Gestión de activos y vehículos
- Órdenes de trabajo
- Mantenimiento preventivo
- Inventario de repuestos
- Sistema de checklists con PDFs
- Predicción de fallos con Machine Learning
- Bot de Telegram para notificaciones
- Tareas automáticas con Celery

## 🏗️ Arquitectura de Producción

```
┌─────────────────────────────────────────┐
│         Frontend (React)                 │
│    Hosted on: Vercel/Netlify/S3        │
└────────────────┬────────────────────────┘
                 │ HTTPS
                 ↓
┌─────────────────────────────────────────┐
│         Nginx (Reverse Proxy)           │
│         SSL/TLS (Let's Encrypt)         │
└────────────────┬────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────┐
│      Gunicorn + Django (Backend)        │
│         Workers: 3-5                     │
└────────────────┬────────────────────────┘
                 │
        ┌────────┴────────┐
        ↓                 ↓
┌──────────────┐  ┌──────────────┐
│  PostgreSQL  │  │    Redis     │
│   Database   │  │    Cache     │
└──────────────┘  └──────────────┘
        ↓                 ↓
┌──────────────┐  ┌──────────────┐
│ Celery Worker│  │ Celery Beat  │
│  (Tasks)     │  │ (Scheduler)  │
└──────────────┘  └──────────────┘
```

## 🔧 Stack Tecnológico

### Backend
- Python 3.12
- Django 4.2
- Django REST Framework 3.14
- PostgreSQL 15
- Redis 7
- Celery 5
- Gunicorn

### Frontend
- React 18
- TypeScript 5
- Vite 5
- Tailwind CSS

### Infraestructura
- Nginx
- Let's Encrypt (SSL)
- Systemd (Process Management)

## 📦 Deployment

### Requisitos del Servidor

- **OS:** Ubuntu 22.04 LTS o superior
- **RAM:** Mínimo 2GB (Recomendado 4GB)
- **CPU:** Mínimo 2 cores
- **Disco:** Mínimo 20GB SSD
- **Python:** 3.12+
- **PostgreSQL:** 15+
- **Redis:** 7+
- **Nginx:** Latest

### Guía Rápida de Deployment

```bash
# 1. Clonar repositorio
git clone https://github.com/TU_USUARIO/proyecto-de-titulo-produccion.git
cd proyecto-de-titulo-produccion

# 2. Ejecutar script de deployment
chmod +x deploy.sh
./deploy.sh

# 3. Configurar variables de entorno
cp .env.production.template .env.production
nano .env.production

# 4. Iniciar servicios
sudo systemctl start cmms celery-worker celery-beat
sudo systemctl enable cmms celery-worker celery-beat
```

Para deployment detallado, ver: [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)

## 🔐 Seguridad

### Configuraciones de Seguridad Implementadas

✅ HTTPS obligatorio (SSL/TLS)  
✅ CORS configurado  
✅ Security headers (CSP, HSTS, X-Frame-Options)  
✅ Rate limiting  
✅ JWT authentication  
✅ Password hashing (PBKDF2)  
✅ Input sanitization  
✅ SQL injection prevention  
✅ XSS protection  
✅ CSRF protection  

### Variables de Entorno Requeridas

```bash
# NUNCA commitear el archivo .env.production
# Usar .env.production.template como referencia

DEBUG=False
SECRET_KEY=<random-secret-key>
ALLOWED_HOSTS=<your-domain>
DATABASE_URL=<postgresql-url>
REDIS_URL=<redis-url>
# ... ver .env.production.template para lista completa
```

## 📊 Monitoreo

### Health Checks

El sistema expone endpoints de health check:

- `GET /api/v1/health/` - Estado general
- `GET /api/v1/health/db/` - Estado de PostgreSQL
- `GET /api/v1/health/redis/` - Estado de Redis
- `GET /api/v1/health/celery/` - Estado de Celery

### Logs

```bash
# Logs de Django
sudo journalctl -u cmms -f

# Logs de Celery
sudo journalctl -u celery-worker -f
sudo journalctl -u celery-beat -f

# Logs de Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Métricas

- Response time: <200ms (p95)
- Uptime: >99.9%
- Error rate: <0.1%

## 🔄 Actualización del Sistema

```bash
# 1. Conectar al servidor
ssh user@your-server

# 2. Navegar al directorio
cd /path/to/proyecto-de-titulo-produccion

# 3. Pull cambios
git pull origin main

# 4. Actualizar dependencias
source venv/bin/activate
pip install -r requirements-production.txt

# 5. Ejecutar migraciones
cd backend
python manage.py migrate
python manage.py collectstatic --noinput

# 6. Reiniciar servicios
sudo systemctl restart cmms celery-worker celery-beat
```

## 💾 Backups

### Backup Automático

Los backups se ejecutan automáticamente cada día a las 2:00 AM:

- Base de datos PostgreSQL
- Archivos media
- Configuraciones

Ubicación: `/home/cmms/backups/`  
Retención: 7 días

### Backup Manual

```bash
# Backup de base de datos
pg_dump cmms_prod > backup_$(date +%Y%m%d).sql

# Backup de archivos media
tar -czf media_backup_$(date +%Y%m%d).tar.gz backend/media/
```

## 🚨 Troubleshooting

### Servicio no inicia

```bash
# Ver logs
sudo journalctl -u cmms -n 50

# Verificar configuración
python manage.py check --deploy

# Verificar permisos
ls -la /path/to/proyecto-de-titulo-produccion
```

### Base de datos no conecta

```bash
# Verificar PostgreSQL
sudo systemctl status postgresql

# Verificar conexión
psql -U cmms_user -d cmms_prod -h localhost
```

### Celery no procesa tareas

```bash
# Verificar Redis
redis-cli ping

# Verificar Celery
celery -A config inspect active
```

## 📞 Soporte

Para problemas en producción:

1. **Revisar logs** del sistema
2. **Verificar health checks**
3. **Consultar documentación** en `/docs`
4. **Contactar al equipo** de desarrollo

## 📝 Changelog

### v1.0.0 (Noviembre 2025)
- ✅ Release inicial
- ✅ Todas las funcionalidades implementadas
- ✅ Tests pasando (>80% coverage)
- ✅ Documentación completa
- ✅ Sistema de ML operativo
- ✅ Bot de Telegram integrado
- ✅ Tareas automáticas con Celery

## 📄 Licencia

Este proyecto es privado y confidencial.

---

**🟢 Sistema en Producción**  
**Última verificación:** [Fecha]  
**Próximo mantenimiento:** [Fecha]
