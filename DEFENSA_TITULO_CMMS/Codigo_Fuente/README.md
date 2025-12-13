# 💻 04_CODIGO_FUENTE - Código Completo del Sistema

## 📋 Contenido de esta Carpeta

Esta carpeta incluye el código fuente completo del sistema ordenado por carpetas, con la estructura generada por las herramientas de desarrollo.

### 🏗️ Estructura del Proyecto

```
04_Codigo_Fuente/
├── backend/                    # Backend Django + ML
│   ├── apps/                   # Aplicaciones Django
│   │   ├── authentication/     # Autenticación y usuarios
│   │   ├── assets/            # Gestión de activos
│   │   ├── work_orders/       # Órdenes de trabajo
│   │   ├── ml_predictions/    # Machine Learning
│   │   ├── maintenance/       # Planes de mantenimiento
│   │   ├── inventory/         # Gestión de inventario
│   │   ├── notifications/     # Sistema de notificaciones
│   │   ├── reports/          # Reportes y analytics
│   │   ├── checklists/       # Listas de verificación
│   │   ├── machine_status/   # Estado de máquinas
│   │   ├── configuration/    # Configuración del sistema
│   │   ├── omnichannel_bot/  # Bot de Telegram
│   │   └── core/            # Funcionalidades core
│   ├── config/              # Configuración Django
│   ├── ml_models/          # Modelos ML entrenados
│   ├── media/              # Archivos subidos
│   ├── requirements.txt    # Dependencias Python
│   └── manage.py          # Script de gestión Django
├── frontend/               # Frontend React + TypeScript
│   ├── src/               # Código fuente React
│   │   ├── components/    # Componentes reutilizables
│   │   ├── pages/        # Páginas principales
│   │   ├── services/     # Servicios API
│   │   ├── types/        # Definiciones TypeScript
│   │   ├── hooks/        # Custom React hooks
│   │   └── utils/        # Utilidades
│   ├── public/           # Archivos estáticos
│   ├── package.json      # Dependencias Node.js
│   └── tailwind.config.js # Configuración Tailwind
├── docs/                 # Documentación técnica
├── scripts/             # Scripts de utilidad
└── deployment/          # Configuraciones de despliegue
```

## 🔧 Tecnologías Utilizadas

### Backend
- **Framework**: Django 4.2.7
- **Lenguaje**: Python 3.11
- **Base de Datos**: PostgreSQL 15
- **API**: Django REST Framework 3.14
- **ML**: Scikit-learn 1.3.0
- **Tareas Asíncronas**: Celery 5.3.0
- **Cache/Broker**: Redis 4.6.0
- **Autenticación**: JWT (djangorestframework-simplejwt)

### Frontend
- **Framework**: React 18.2.0
- **Lenguaje**: TypeScript 5.0
- **Build Tool**: Vite 4.4.5
- **Estilos**: Tailwind CSS 3.3.0
- **Iconos**: React Icons 4.10.1
- **HTTP Client**: Axios 1.5.0
- **Routing**: React Router DOM 6.15.0

### DevOps y Despliegue
- **Backend Hosting**: Railway
- **Frontend Hosting**: Vercel
- **CI/CD**: GitHub Actions
- **Monitoreo**: Logs integrados
- **Backup**: Automático diario

## 📁 Descripción de Módulos

### Backend - Aplicaciones Django

#### 1. **authentication/** - Gestión de Usuarios
```python
# Funcionalidades principales:
- Registro y login de usuarios
- Gestión de roles (Admin, Supervisor, Operador)
- Autenticación JWT
- Perfiles de usuario
- Permisos granulares
```

#### 2. **assets/** - Gestión de Activos
```python
# Funcionalidades principales:
- CRUD de activos (vehículos, equipos)
- Gestión de ubicaciones
- Categorización de activos
- Historial de cambios
- Búsqueda y filtros avanzados
```

#### 3. **work_orders/** - Órdenes de Trabajo
```python
# Funcionalidades principales:
- Creación manual y automática de OT
- Estados: Pendiente, En Progreso, Completada
- Asignación de operadores
- Seguimiento de tiempo y costos
- Integración con predicciones ML
```

#### 4. **ml_predictions/** - Machine Learning
```python
# Funcionalidades principales:
- Entrenamiento de modelos Random Forest
- Predicciones automáticas diarias
- Clasificación de riesgo (LOW/MEDIUM/HIGH/CRITICAL)
- Integración con órdenes de trabajo
- Métricas de performance del modelo
```

#### 5. **maintenance/** - Planes de Mantenimiento
```python
# Funcionalidades principales:
- Planes de mantenimiento preventivo
- Programación automática
- Historial de mantenimientos
- Métricas de efectividad
```

#### 6. **notifications/** - Sistema de Notificaciones
```python
# Funcionalidades principales:
- Notificaciones in-app
- Integración con Telegram
- Alertas por email
- Preferencias de usuario
- Escalamiento automático
```

### Frontend - Componentes React

#### 1. **components/** - Componentes Reutilizables
```typescript
// Estructura de componentes:
├── layout/          # Layout principal, sidebar, header
├── assets/          # Componentes de gestión de activos
├── work-orders/     # Componentes de órdenes de trabajo
├── users/           # Gestión de usuarios
├── dashboard/       # Widgets del dashboard
├── forms/           # Formularios reutilizables
└── ui/             # Componentes UI básicos
```

#### 2. **pages/** - Páginas Principales
```typescript
// Páginas del sistema:
- Dashboard.tsx      # Panel principal con KPIs
- Assets.tsx         # Gestión de activos
- WorkOrders.tsx     # Órdenes de trabajo
- Users.tsx          # Gestión de usuarios
- Reports.tsx        # Reportes y analytics
- MLPredictions.tsx  # Predicciones ML
- Settings.tsx       # Configuración
```

#### 3. **services/** - Servicios API
```typescript
// Servicios para comunicación con backend:
- api.ts            # Cliente HTTP base
- authService.ts    # Autenticación
- assetService.ts   # Gestión de activos
- workOrderService.ts # Órdenes de trabajo
- mlService.ts      # Predicciones ML
```

## 🚀 Instrucciones de Instalación

### Prerrequisitos
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 6+
- Git

### Backend Setup
```bash
# 1. Clonar repositorio
git clone [repository-url]
cd backend

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con configuraciones locales

# 5. Ejecutar migraciones
python manage.py migrate

# 6. Crear superusuario
python manage.py createsuperuser

# 7. Entrenar modelo ML
python manage.py train_ml_model

# 8. Ejecutar servidor
python manage.py runserver
```

### Frontend Setup
```bash
# 1. Navegar a frontend
cd frontend

# 2. Instalar dependencias
npm install

# 3. Configurar variables de entorno
cp .env.example .env.local
# Editar .env.local con URL del backend

# 4. Ejecutar en desarrollo
npm run dev

# 5. Build para producción
npm run build
```

### Celery Setup (Opcional para desarrollo)
```bash
# Terminal 1: Redis
redis-server

# Terminal 2: Celery Worker
cd backend
celery -A config worker -l info

# Terminal 3: Celery Beat (scheduler)
celery -A config beat -l info
```

## 📊 Estructura de Archivos Clave

### Backend - Archivos Importantes
```
backend/
├── config/
│   ├── settings/
│   │   ├── base.py          # Configuración base
│   │   ├── development.py   # Configuración desarrollo
│   │   └── production.py    # Configuración producción
│   ├── urls.py             # URLs principales
│   ├── wsgi.py             # WSGI para producción
│   └── celery.py           # Configuración Celery
├── apps/ml_predictions/
│   ├── models.py           # Modelos de datos ML
│   ├── prediction_service.py # Servicio principal ML
│   ├── model_trainer.py    # Entrenamiento de modelos
│   ├── tasks.py           # Tareas Celery
│   └── views.py           # API endpoints ML
└── ml_models/
    ├── failure_prediction_model.pkl  # Modelo entrenado
    └── label_encoders.pkl           # Encoders
```

### Frontend - Archivos Importantes
```
frontend/
├── src/
│   ├── App.tsx             # Componente principal
│   ├── main.tsx           # Punto de entrada
│   ├── components/
│   │   ├── layout/MainLayout.tsx    # Layout principal
│   │   └── assets/AssetDetail.tsx   # Detalle de activos
│   ├── pages/
│   │   ├── Dashboard.tsx            # Dashboard principal
│   │   └── MLPredictions.tsx        # Predicciones ML
│   └── services/
│       ├── api.ts                   # Cliente HTTP
│       └── authService.ts           # Autenticación
├── tailwind.config.js      # Configuración Tailwind
├── vite.config.ts         # Configuración Vite
└── package.json           # Dependencias y scripts
```

## 🔒 Configuración de Seguridad

### Variables de Entorno Críticas
```bash
# Backend (.env)
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@host:port/db
REDIS_URL=redis://localhost:6379/0
JWT_SECRET_KEY=your-jwt-secret
TELEGRAM_BOT_TOKEN=your-telegram-token

# Frontend (.env.local)
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_NAME=CMMS System
```

### Configuraciones de Producción
- HTTPS obligatorio
- CORS configurado para dominios específicos
- Rate limiting en APIs críticas
- Logs de seguridad habilitados
- Backup automático de base de datos

## 📈 Métricas de Código

### Backend
- **Líneas de código**: ~15,000 líneas
- **Archivos Python**: ~120 archivos
- **Modelos Django**: 25 modelos
- **Endpoints API**: 80+ endpoints
- **Tests**: 150+ tests unitarios

### Frontend
- **Líneas de código**: ~8,000 líneas
- **Componentes React**: 45 componentes
- **Páginas**: 12 páginas principales
- **Servicios**: 8 servicios API
- **Hooks personalizados**: 6 hooks

## 🧪 Testing

### Backend Testing
```bash
# Ejecutar todos los tests
python manage.py test

# Tests con coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Frontend Testing
```bash
# Tests unitarios
npm run test

# Tests E2E
npm run test:e2e
```

## 📚 Documentación Adicional

- **API Documentation**: `/api/docs/` (Swagger UI)
- **Admin Panel**: `/admin/` (Django Admin)
- **ML Model Info**: Documentado en `ml_predictions/README.md`
- **Deployment Guide**: `deployment/README.md`

---
*Código Fuente Completo - Sistema CMMS v1.0 - Diciembre 2025*