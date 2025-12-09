# Guía de Deployment - Sistema CMMS

Esta guía explica cómo desplegar el sistema CMMS en producción.

## 📋 Tabla de Contenidos

1. [Arquitectura de Repositorios](#arquitectura-de-repositorios)
2. [Preparación para Producción](#preparación-para-producción)
3. [Deployment a Producción](#deployment-a-producción)
4. [Configuración de Servicios](#configuración-de-servicios)
5. [Monitoreo y Mantenimiento](#monitoreo-y-mantenimiento)

---

## Arquitectura de Repositorios

### Repositorio 1: `proyecto-de-titulo-local`
- **Propósito:** Desarrollo y testing
- **Base de datos:** SQLite
- **Contenido:** Código completo con datos de prueba
- **Uso:** Desarrollo local, testing, demos

### Repositorio 2: `proyecto-de-titulo-produccion`
- **Propósito:** Producción
- **Base de datos:** PostgreSQL
- **Contenido:** Código optimizado para producción
- **Uso:** Sistema en vivo para usuarios finales

---

## Preparación para Producción

### 1. Diferencias entre Local y Producción

| Aspecto | Local | Producción |
|---------|-------|------------|
| Base de datos | SQLite | PostgreSQL |
| Debug | True | False |
| Archivos estáticos | Local | S3/CDN |
| Caché | Local | Redis |
| Servidor web | Django dev | Gunicorn + Nginx |
| HTTPS | No | Sí (Let's Encrypt) |
| Logs | Console | Archivos + Sentry |
| Backups | Manual | Automático |

### 2. Archivos de Configuración

Crear archivo `.env.production`:

```bash
# Django
DEBUG=False
SECRET_KEY=tu-secret-key-super-segura-aqui
ALLOWED_HOSTS=tudominio.com,www.tudominio.com

# Database
DATABASE_URL=postgresql://usuario:password@localhost:5432/cmms_prod

# Redis
REDIS_URL=redis://localhost:6379/0

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1

# Email (para notificaciones)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password

# Telegram Bot
TELEGRAM_BOT_TOKEN=tu-token-de-telegram
TELEGRAM_ENABLED=True

# AWS S3 (opcional, para archivos)
AWS_ACCESS_KEY_ID=tu-access-key
AWS_SECRET_ACCESS_KEY=tu-secret-key
AWS_STORAGE_BUCKET_NAME=cmms-media
AWS_S3_REGION_NAME=us-east-1

# Sentry (opcional, para error tracking)
SENTRY_DSN=tu-sentry-dsn
```

### 3. Preparar Código para Producción

Ejecuta el script de preparación:

```bash
python prepare_for_production.py
```

Este script:
- ✅ Verifica configuraciones de seguridad
- ✅ Optimiza archivos estáticos
- ✅ Genera requirements.txt de producción
- ✅ Crea archivo de deployment

---

## Deployment a Producción

### Opción 1: Servidor VPS (DigitalOcean, AWS EC2, etc.)

#### Paso 1: Configurar Servidor

```bash
# Conectar al servidor
ssh root@tu-servidor-ip

# Actualizar sistema
apt update && apt upgrade -y

# Instalar dependencias
apt install -y python3.12 python3-pip python3-venv postgresql nginx redis-server

# Crear usuario para la aplicación
adduser cmms
usermod -aG sudo cmms
su - cmms
```

#### Paso 2: Clonar Repositorio

```bash
# Clonar repositorio de producción
git clone https://github.com/TU_USUARIO/proyecto-de-titulo-produccion.git
cd proyecto-de-titulo-produccion

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements-production.txt
```

#### Paso 3: Configurar Base de Datos

```bash
# Crear base de datos PostgreSQL
sudo -u postgres psql
CREATE DATABASE cmms_prod;
CREATE USER cmms_user WITH PASSWORD 'tu-password-segura';
GRANT ALL PRIVILEGES ON DATABASE cmms_prod TO cmms_user;
\q

# Ejecutar migraciones
cd backend
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

#### Paso 4: Configurar Gunicorn

Crear archivo `/etc/systemd/system/cmms.service`:

```ini
[Unit]
Description=CMMS Gunicorn daemon
After=network.target

[Service]
User=cmms
Group=www-data
WorkingDirectory=/home/cmms/proyecto-de-titulo-produccion/backend
ExecStart=/home/cmms/proyecto-de-titulo-produccion/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/home/cmms/proyecto-de-titulo-produccion/cmms.sock \
          config.wsgi:application

[Install]
WantedBy=multi-user.target
```

Iniciar servicio:
```bash
sudo systemctl start cmms
sudo systemctl enable cmms
```

#### Paso 5: Configurar Nginx

Crear archivo `/etc/nginx/sites-available/cmms`:

```nginx
server {
    listen 80;
    server_name tudominio.com www.tudominio.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /home/cmms/proyecto-de-titulo-produccion/backend/staticfiles/;
    }

    location /media/ {
        alias /home/cmms/proyecto-de-titulo-produccion/backend/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/cmms/proyecto-de-titulo-produccion/cmms.sock;
    }
}
```

Activar sitio:
```bash
sudo ln -s /etc/nginx/sites-available/cmms /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

#### Paso 6: Configurar HTTPS con Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d tudominio.com -d www.tudominio.com
```

#### Paso 7: Configurar Celery

Crear archivo `/etc/systemd/system/celery-worker.service`:

```ini
[Unit]
Description=Celery Worker
After=network.target

[Service]
Type=forking
User=cmms
Group=www-data
WorkingDirectory=/home/cmms/proyecto-de-titulo-produccion/backend
ExecStart=/home/cmms/proyecto-de-titulo-produccion/venv/bin/celery -A config worker -l info

[Install]
WantedBy=multi-user.target
```

Crear archivo `/etc/systemd/system/celery-beat.service`:

```ini
[Unit]
Description=Celery Beat
After=network.target

[Service]
Type=simple
User=cmms
Group=www-data
WorkingDirectory=/home/cmms/proyecto-de-titulo-produccion/backend
ExecStart=/home/cmms/proyecto-de-titulo-produccion/venv/bin/celery -A config beat -l info

[Install]
WantedBy=multi-user.target
```

Iniciar servicios:
```bash
sudo systemctl start celery-worker celery-beat
sudo systemctl enable celery-worker celery-beat
```

---

### Opción 2: Docker (Recomendado para facilidad)

Ver archivo `docker-compose.production.yml` incluido en el repositorio.

```bash
# Construir y levantar contenedores
docker-compose -f docker-compose.production.yml up -d

# Ver logs
docker-compose -f docker-compose.production.yml logs -f
```

---

## Configuración de Servicios

### Frontend (React)

```bash
cd frontend

# Instalar dependencias
npm install

# Configurar variables de entorno
echo "VITE_API_URL=https://api.tudominio.com/api/v1" > .env.production

# Build para producción
npm run build

# Los archivos estarán en frontend/dist
# Súbelos a un hosting estático (Vercel, Netlify, S3, etc.)
```

### Backups Automáticos

Crear script `/home/cmms/backup.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/home/cmms/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup de base de datos
pg_dump cmms_prod > $BACKUP_DIR/db_$DATE.sql

# Backup de archivos media
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /home/cmms/proyecto-de-titulo-produccion/backend/media

# Eliminar backups antiguos (más de 7 días)
find $BACKUP_DIR -type f -mtime +7 -delete
```

Agregar a crontab:
```bash
crontab -e
# Agregar línea:
0 2 * * * /home/cmms/backup.sh
```

---

## Monitoreo y Mantenimiento

### Logs

```bash
# Ver logs de Django
sudo journalctl -u cmms -f

# Ver logs de Celery
sudo journalctl -u celery-worker -f
sudo journalctl -u celery-beat -f

# Ver logs de Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Actualizar Código

```bash
cd /home/cmms/proyecto-de-titulo-produccion
git pull origin main
source venv/bin/activate
pip install -r requirements-production.txt
cd backend
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart cmms celery-worker celery-beat
```

### Monitoreo de Salud

El sistema incluye endpoints de health check:

- `/api/v1/health/` - Estado general
- `/api/v1/health/db/` - Estado de base de datos
- `/api/v1/health/redis/` - Estado de Redis
- `/api/v1/health/celery/` - Estado de Celery

Configura un servicio de monitoreo (UptimeRobot, Pingdom, etc.) para verificar estos endpoints.

---

## Checklist de Deployment

- [ ] Repositorios creados en GitHub
- [ ] Servidor configurado (VPS o Docker)
- [ ] PostgreSQL instalado y configurado
- [ ] Redis instalado y configurado
- [ ] Código clonado y dependencias instaladas
- [ ] Variables de entorno configuradas
- [ ] Migraciones ejecutadas
- [ ] Archivos estáticos recolectados
- [ ] Gunicorn configurado y corriendo
- [ ] Nginx configurado y corriendo
- [ ] HTTPS configurado (Let's Encrypt)
- [ ] Celery Worker corriendo
- [ ] Celery Beat corriendo
- [ ] Frontend buildeado y deployado
- [ ] Backups automáticos configurados
- [ ] Monitoreo configurado
- [ ] DNS apuntando al servidor
- [ ] Superusuario creado
- [ ] Datos de prueba cargados (opcional)
- [ ] Tests de producción ejecutados

---

## Soporte

Para problemas o dudas:
1. Revisar logs del sistema
2. Consultar documentación en `/docs`
3. Verificar health checks
4. Revisar configuración de servicios

---

**¡Sistema listo para producción!** 🚀
