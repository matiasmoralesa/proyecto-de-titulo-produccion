# Guía de Configuración Local - Sistema CMMS

Esta guía te ayudará a configurar el Sistema de Gestión de Mantenimiento Computarizado (CMMS) en tu entorno local de desarrollo.

## Requisitos Previos

### Software Requerido:
- **Python 3.12+** - [Descargar](https://www.python.org/downloads/)
- **Node.js 18+** y npm - [Descargar](https://nodejs.org/)
- **Git** - [Descargar](https://git-scm.com/)
- **Redis** (opcional, para Celery) - [Descargar](https://redis.io/download)

### Verificar Instalaciones:
```bash
python --version  # Debe ser 3.12 o superior
node --version    # Debe ser 18 o superior
npm --version
git --version
```

## Configuración del Backend (Django)

### 1. Clonar el Repositorio
```bash
git clone <repository-url>
cd proyecto-cmms
```

### 2. Crear Entorno Virtual
```bash
# Windows
cd backend
python -m venv venv
venv\Scripts\activate

# Linux/Mac
cd backend
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno
Crea un archivo `.env` en la carpeta `backend/`:

```env
# Django Settings
SECRET_KEY=tu-clave-secreta-aqui-cambiar-en-produccion
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite por defecto)
DATABASE_URL=sqlite:///db.sqlite3

# Celery (opcional)
CELERY_BROKER_URL=redis://localhost:6379/0

# Telegram Bot (opcional)
TELEGRAM_BOT_TOKEN=tu-token-aqui
TELEGRAM_CHAT_ID=tu-chat-id-aqui
```

### 5. Ejecutar Migraciones
```bash
python manage.py migrate
```

### 6. Crear Roles Iniciales
```bash
python manage.py shell -c "from apps.authentication.models import Role; Role.objects.get_or_create(name='ADMIN', defaults={'description': 'Administrator'}); Role.objects.get_or_create(name='SUPERVISOR', defaults={'description': 'Supervisor'}); Role.objects.get_or_create(name='OPERADOR', defaults={'description': 'Operator'})"
```

### 7. Crear Superusuario
```bash
python create_superuser.py
# O manualmente:
# python manage.py shell
# from apps.authentication.models import User, Role
# admin_role = Role.objects.get(name='ADMIN')
# user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
# user.role = admin_role
# user.save()
```

### 8. Cargar Datos de Ejemplo (Opcional)
```bash
# Crear ubicaciones
python create_sample_assets.py

# Crear órdenes de trabajo
python create_sample_workorders.py

# Crear inventario
python create_sample_inventory.py

# Crear planes de mantenimiento
python create_sample_maintenance.py
```

### 9. Iniciar Servidor de Desarrollo
```bash
python manage.py runserver
```

El servidor estará disponible en: `http://localhost:8000`

### 10. Iniciar Celery (Opcional)
En terminales separadas:

```bash
# Worker
celery -A config worker -l info --pool=solo

# Beat (tareas programadas)
celery -A config beat -l info
```

## Configuración del Frontend (React + Vite)

### 1. Navegar a la Carpeta Frontend
```bash
cd frontend
```

### 2. Instalar Dependencias
```bash
npm install
```

### 3. Configurar Variables de Entorno
Crea un archivo `.env` en la carpeta `frontend/`:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

### 4. Iniciar Servidor de Desarrollo
```bash
npm run dev
```

El frontend estará disponible en: `http://localhost:5173`

## Verificación de la Instalación

### 1. Verificar Backend
Abre tu navegador en `http://localhost:8000/api/docs/` para ver la documentación de la API (Swagger).

### 2. Verificar Frontend
Abre tu navegador en `http://localhost:5173` y deberías ver la página de login.

### 3. Iniciar Sesión
Usa las credenciales del superusuario que creaste:
- **Usuario:** admin
- **Contraseña:** admin123 (o la que configuraste)

## Estructura del Proyecto

```
proyecto-cmms/
├── backend/
│   ├── apps/                 # Aplicaciones Django
│   │   ├── assets/          # Gestión de activos
│   │   ├── work_orders/     # Órdenes de trabajo
│   │   ├── maintenance/     # Planes de mantenimiento
│   │   ├── inventory/       # Inventario
│   │   ├── checklists/      # Checklists
│   │   ├── notifications/   # Notificaciones
│   │   ├── reports/         # Reportes
│   │   └── ...
│   ├── config/              # Configuración Django
│   ├── media/               # Archivos subidos
│   ├── logs/                # Logs del sistema
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/      # Componentes React
│   │   ├── pages/           # Páginas
│   │   ├── services/        # Servicios API
│   │   ├── store/           # Estado global (Zustand)
│   │   └── App.tsx
│   ├── package.json
│   └── vite.config.ts
│
└── docs/                    # Documentación
```

## Scripts Útiles

### Backend:
```bash
# Ejecutar tests
pytest

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python create_superuser.py

# Limpiar base de datos
python manage.py flush

# Shell interactivo
python manage.py shell
```

### Frontend:
```bash
# Desarrollo
npm run dev

# Build para producción
npm run build

# Preview de producción
npm run preview

# Linting
npm run lint

# Tests
npm run test
```

## Solución de Problemas Comunes

### Error: "No module named 'apps'"
**Solución:** Asegúrate de estar en la carpeta `backend/` y que el entorno virtual esté activado.

### Error: "Port 8000 is already in use"
**Solución:** 
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Error: "CORS policy"
**Solución:** Verifica que el frontend esté configurado en `CORS_ALLOWED_ORIGINS` en `backend/config/settings/development.py`.

### Error: "Cannot connect to Redis"
**Solución:** Si no necesitas Celery, puedes omitir Redis. Si lo necesitas, instala y ejecuta Redis:
```bash
# Windows
# Usar install_redis.ps1 en la carpeta backend

# Linux
sudo apt-get install redis-server
redis-server

# Mac
brew install redis
redis-server
```

### Error: "Module not found" en Frontend
**Solución:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## Configuración de IDE

### VS Code (Recomendado)
Extensiones recomendadas:
- Python
- Pylance
- ESLint
- Prettier
- Tailwind CSS IntelliSense
- GitLens

### PyCharm
1. Configurar intérprete de Python al entorno virtual
2. Marcar `backend/` como Sources Root
3. Habilitar Django support

## Próximos Pasos

1. ✅ Explorar la documentación de la API en `/api/docs/`
2. ✅ Revisar el dashboard en el frontend
3. ✅ Crear algunos activos de prueba
4. ✅ Crear órdenes de trabajo
5. ✅ Explorar los reportes y analíticas

## Recursos Adicionales

- [Documentación de Django](https://docs.djangoproject.com/)
- [Documentación de React](https://react.dev/)
- [Documentación de Vite](https://vitejs.dev/)
- [Documentación de Tailwind CSS](https://tailwindcss.com/)

## Soporte

Si encuentras problemas, revisa:
1. Los logs en `backend/logs/`
2. La consola del navegador (F12)
3. La terminal donde corre el servidor

Para más ayuda, contacta al equipo de desarrollo.
