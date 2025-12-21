# 🏭 CMMS - Sistema de Gestión de Mantenimiento Computarizado

<div align="center">

![Status](https://img.shields.io/badge/status-production-success)
![Django](https://img.shields.io/badge/Django-4.2+-green.svg)
![React](https://img.shields.io/badge/React-18+-blue.svg)
![TypeScript](https://img.shields.io/badge/TypeScript-5+-blue.svg)
![License](https://img.shields.io/badge/license-Private-red.svg)

Sistema completo de gestión de mantenimiento para activos industriales con inteligencia artificial predictiva y bot de Telegram integrado.

[Características](#-características) •
[Demo](#-demo) •
[Instalación](#-instalación) •
[Documentación](#-documentación) •
[Tecnologías](#-tecnologías)

</div>

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Demo](#-demo)
- [Arquitectura](#-arquitectura)
- [Tecnologías](#-tecnologías)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [API](#-api)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Contribución](#-contribución)
- [Licencia](#-licencia)

---

## ✨ Características

### 🚗 Gestión de Activos
- Control completo de flota vehicular e industrial
- 5 tipos de vehículos predefinidos (Camionetas, Retroexcavadoras, Cargadores, Minicargadores, Supersuckers)
- Seguimiento de estado en tiempo real
- Historial completo de mantenimientos

### 📝 Órdenes de Trabajo
- Creación y asignación inteligente de tareas
- Seguimiento de progreso en tiempo real
- Gestión de prioridades (Baja, Media, Alta, Crítica)
- Estados configurables (Pendiente, En Progreso, Completada, Cancelada)
- Exportación a PDF y CSV

### 🔧 Mantenimiento Preventivo
- Programación automática basada en reglas
- Recurrencia configurable (diaria, semanal, mensual, anual)
- Alertas proactivas de mantenimiento
- Planes personalizados por tipo de activo

### 📦 Inventario de Repuestos
- Control de stock en tiempo real
- Alertas automáticas de stock bajo
- Seguimiento de movimientos (entradas/salidas)
- Vinculación con órdenes de trabajo
- Reportes de consumo

### ✅ Sistema de Checklists
- Plantillas predefinidas por tipo de vehículo
- Generación automática de PDFs
- Validación de inspecciones
- Historial de checklists completados

### 🔔 Notificaciones Inteligentes
- Alertas en tiempo real
- Múltiples canales (Web, Email, Telegram)
- Notificaciones personalizadas por rol
- Sistema de prioridades

### 📊 Reportes y Analytics
- **KPIs de Mantenimiento**:
  - MTBF (Mean Time Between Failures)
  - MTTR (Mean Time To Repair)
  - OEE (Overall Equipment Effectiveness)
- Dashboards interactivos con gráficos
- Reportes de consumo de repuestos
- Análisis de downtime por activo
- Cumplimiento de mantenimiento preventivo

### 🤖 Bot de Telegram
- Consulta de órdenes de trabajo
- Actualización de estados
- Notificaciones push
- Comandos interactivos con botones
- Vinculación de usuarios

### 🧠 Machine Learning
- Predicción de fallas en activos
- Análisis de patrones de mantenimiento
- Recomendaciones inteligentes
- Modelo entrenado con datos históricos

### 🔐 Control de Acceso
- **3 Roles con permisos específicos**:
  - **ADMIN**: Acceso completo, gestión de usuarios y configuración
  - **SUPERVISOR**: Gestión de órdenes, activos y reportes del equipo
  - **OPERADOR**: Acceso a órdenes asignadas y actualización de estados
- Autenticación JWT
- Permisos granulares por endpoint

---

## 🎬 Demo

### 🌐 Aplicación en Producción
- **Frontend**: [https://proyecto-de-titulo-produccion.vercel.app](https://proyecto-de-titulo-produccion.vercel.app)
- **Backend API**: [https://proyecto-de-titulo-produccion-production.up.railway.app](https://proyecto-de-titulo-produccion-production.up.railway.app)
- **API Docs**: [https://proyecto-de-titulo-produccion-production.up.railway.app/api/docs/](https://proyecto-de-titulo-produccion-production.up.railway.app/api/docs/)

### 👤 Credenciales de Demo
```
Usuario: admin
Contraseña: admin123
```

### 📱 Bot de Telegram
Busca `@tu_bot_name` en Telegram y usa el comando `/start` para comenzar.

### 🏢 Branding SOMACOR
El sistema incluye el logo corporativo de SOMACOR (50 años) integrado en:
- Página de login con mensaje institucional
- Sidebar de navegación principal
- Header del dashboard
- Favicon del navegador

---

## 🏗️ Arquitectura

```
┌─────────────────┐
│   Usuarios      │
└────────┬────────┘
         │
    ┌────▼─────┐
    │ Vercel   │ ◄── Frontend (React + TypeScript)
    │  CDN     │
    └────┬─────┘
         │
    ┌────▼─────────────┐
    │   Railway        │ ◄── Backend (Django REST)
    │  ┌──────────┐    │
    │  │ Django   │    │
    │  │ REST API │    │
    │  └────┬─────┘    │
    │       │          │
    │  ┌────▼─────┐    │
    │  │PostgreSQL│    │
    │  └──────────┘    │
    └──────┬───────────┘
           │
    ┌──────▼───────┐
    │   Telegram   │ ◄── Bot Integration
    │   Bot API    │
    └──────────────┘
```

### Componentes Principales

- **Frontend**: React 18 + TypeScript + Vite + Tailwind CSS
- **Backend**: Django 4.2 + Django REST Framework
- **Base de Datos**: PostgreSQL (Producción) / SQLite (Desarrollo)
- **Autenticación**: JWT (Simple JWT)
- **Storage**: Railway Volumes (archivos y modelo ML)
- **Bot**: python-telegram-bot
- **ML**: scikit-learn + joblib

---

## 🛠️ Tecnologías

### Backend
| Tecnología | Versión | Propósito |
|-----------|---------|-----------|
| Python | 3.11+ | Lenguaje base |
| Django | 4.2+ | Framework web |
| Django REST Framework | 3.14+ | API REST |
| PostgreSQL | 15+ | Base de datos |
| Celery | 5.3+ | Tareas asíncronas |
| Redis | 7+ | Cache y message broker |
| python-telegram-bot | 20+ | Bot de Telegram |
| scikit-learn | 1.3+ | Machine Learning |
| ReportLab | 4.0+ | Generación de PDFs |

### Frontend
| Tecnología | Versión | Propósito |
|-----------|---------|-----------|
| React | 18+ | UI Framework |
| TypeScript | 5+ | Tipado estático |
| Vite | 5+ | Build tool |
| Tailwind CSS | 3+ | Estilos |
| Zustand | 4+ | State management |
| Recharts | 2+ | Gráficos |
| Axios | 1+ | HTTP client |
| React Router | 6+ | Routing |

### DevOps
| Tecnología | Propósito |
|-----------|-----------|
| Railway | Hosting backend |
| Vercel | Hosting frontend |
| GitHub Actions | CI/CD |
| Docker | Containerización |

---

## 📦 Requisitos

- **Python**: 3.11 o superior
- **Node.js**: 18 o superior
- **PostgreSQL**: 15 o superior (producción)
- **Redis**: 7 o superior (opcional, para Celery)
- **Git**: Para control de versiones

---

## 🚀 Instalación

### 1️⃣ Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/proyecto-de-titulo-produccion.git
cd proyecto-de-titulo-produccion
```

### 2️⃣ Configurar Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Copiar archivo de configuración
cp .env.example .env

# Configurar variables de entorno en .env
# DATABASE_URL=postgresql://user:password@localhost:5432/cmms
# SECRET_KEY=tu-secret-key-aqui
# TELEGRAM_BOT_TOKEN=tu-token-de-telegram

# Ejecutar migraciones
python manage.py migrate

# Crear datos iniciales (roles, usuarios, etc.)
python manage.py seed_initial_data

# Crear superusuario (opcional)
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver
```

El backend estará disponible en `http://localhost:8000`

### 3️⃣ Configurar Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Copiar archivo de configuración
cp .env.example .env.local

# Configurar variables de entorno en .env.local
# VITE_API_URL=http://localhost:8000

# Iniciar servidor de desarrollo
npm run dev
```

El frontend estará disponible en `http://localhost:5173`

### 4️⃣ Configurar Bot de Telegram (Opcional)

```bash
# En el backend, con el entorno virtual activado
python manage.py set_telegram_webhook

# Verificar webhook
python manage.py check_telegram_webhook
```

---

## ⚙️ Configuración

### Variables de Entorno - Backend

Crear archivo `.env` en la carpeta `backend/`:

```env
# Django
SECRET_KEY=tu-secret-key-super-segura
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/cmms

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# Telegram Bot
TELEGRAM_BOT_TOKEN=tu-token-de-telegram-bot
TELEGRAM_WEBHOOK_URL=https://tu-dominio.com/api/v1/telegram/webhook/

# Celery (opcional)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Email (opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-password
```

### Variables de Entorno - Frontend

Crear archivo `.env.local` en la carpeta `frontend/`:

```env
VITE_API_URL=http://localhost:8000
```

---

## 💻 Uso

### Acceso al Sistema

1. Abre el navegador en `http://localhost:5173`
2. Inicia sesión con las credenciales:
   - Usuario: `admin`
   - Contraseña: `admin123`

### Flujo de Trabajo Típico

1. **Crear Activos**: Registra tus vehículos y equipos
2. **Configurar Planes de Mantenimiento**: Define mantenimientos preventivos
3. **Crear Órdenes de Trabajo**: Asigna tareas al equipo
4. **Actualizar Estados**: Los operadores actualizan el progreso
5. **Revisar Reportes**: Analiza KPIs y métricas
6. **Gestionar Inventario**: Controla repuestos y consumos

### Comandos Útiles

```bash
# Backend
python manage.py seed_realistic_data  # Generar datos de prueba
python manage.py train_ml_model       # Entrenar modelo ML
python manage.py generate_predictions # Generar predicciones

# Frontend
npm run build                         # Build para producción
npm run preview                       # Preview del build
npm run lint                          # Linting
npm run format                        # Formatear código
```

---

## 📚 API

### Documentación Interactiva

- **Swagger UI**: `http://localhost:8000/api/docs/`
- **ReDoc**: `http://localhost:8000/api/redoc/`
- **OpenAPI Schema**: `http://localhost:8000/api/schema/`

### Endpoints Principales

#### Autenticación
```http
POST /api/v1/auth/login/
POST /api/v1/auth/register/
POST /api/v1/auth/refresh/
POST /api/v1/auth/logout/
```

#### Activos
```http
GET    /api/v1/assets/
POST   /api/v1/assets/
GET    /api/v1/assets/{id}/
PUT    /api/v1/assets/{id}/
DELETE /api/v1/assets/{id}/
```

#### Órdenes de Trabajo
```http
GET    /api/v1/work-orders/
POST   /api/v1/work-orders/
GET    /api/v1/work-orders/{id}/
PUT    /api/v1/work-orders/{id}/
PATCH  /api/v1/work-orders/{id}/
GET    /api/v1/work-orders/{id}/export-pdf/
```

#### Reportes
```http
GET /api/v1/reports/kpis/
GET /api/v1/reports/work-order-summary/
GET /api/v1/reports/asset-downtime/
GET /api/v1/reports/spare_part_consumption/
GET /api/v1/reports/maintenance-compliance/
```

### Autenticación

Todas las peticiones requieren un token JWT en el header:

```http
Authorization: Bearer <tu-token-jwt>
```

---

## 🧪 Testing

### Backend

```bash
cd backend

# Ejecutar todos los tests
pytest

# Tests con coverage
pytest --cov=apps --cov-report=html

# Tests específicos
pytest apps/work_orders/tests/
pytest -k "test_create_work_order"

# Tests por marcadores
pytest -m unit          # Solo tests unitarios
pytest -m integration   # Solo tests de integración
pytest -m property      # Property-based tests
```

### Frontend

```bash
cd frontend

# Ejecutar tests
npm run test

# Tests con coverage
npm run test:coverage

# Tests en modo watch
npm run test:watch
```

### Coverage Actual

- **Backend**: 85%+ de cobertura
- **Frontend**: 70%+ de cobertura

---

## 🚢 Deployment

### Producción Actual

- **Frontend**: Vercel (Auto-deploy desde `main`)
- **Backend**: Railway (Auto-deploy desde `main`)
- **Base de Datos**: Railway PostgreSQL
- **Storage**: Railway Volumes

### Deploy Manual

#### Backend (Railway)

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway up
```

#### Frontend (Vercel)

```bash
# Instalar Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
cd frontend
vercel --prod
```

### Variables de Entorno en Producción

Configurar en Railway/Vercel:
- `SECRET_KEY`
- `DATABASE_URL`
- `TELEGRAM_BOT_TOKEN`
- `ALLOWED_HOSTS`
- `CORS_ALLOWED_ORIGINS`

---

## 📁 Estructura del Proyecto

```
proyecto-de-titulo-produccion/
├── backend/                    # Backend Django
│   ├── apps/                   # Aplicaciones Django
│   │   ├── authentication/     # Autenticación y usuarios
│   │   ├── assets/             # Gestión de activos
│   │   ├── work_orders/        # Órdenes de trabajo
│   │   ├── maintenance/        # Mantenimiento preventivo
│   │   ├── inventory/          # Inventario de repuestos
│   │   ├── checklists/         # Sistema de checklists
│   │   ├── notifications/      # Notificaciones
│   │   ├── reports/            # Reportes y KPIs
│   │   ├── machine_status/     # Estado de máquinas
│   │   ├── telegram_bot/       # Bot de Telegram
│   │   ├── ml_predictions/     # Machine Learning
│   │   └── core/               # Utilidades compartidas
│   ├── config/                 # Configuración Django
│   ├── media/                  # Archivos subidos
│   ├── staticfiles/            # Archivos estáticos
│   └── requirements.txt        # Dependencias Python
│
├── frontend/                   # Frontend React
│   ├── src/
│   │   ├── components/         # Componentes React
│   │   ├── pages/              # Páginas
│   │   ├── services/           # Servicios API
│   │   ├── store/              # Estado global (Zustand)
│   │   ├── types/              # Tipos TypeScript
│   │   ├── utils/              # Utilidades
│   │   └── App.tsx             # Componente principal
│   ├── public/                 # Archivos públicos
│   └── package.json            # Dependencias Node
│
├── docs/                       # Documentación
│   └── specs/                  # Especificaciones
│
├── dev-docs/                   # Documentación de desarrollo
│   ├── scripts/                # Scripts de utilidad
│   ├── deployment/             # Guías de deployment
│   ├── testing/                # Documentación de testing
│   ├── fixes/                  # Registro de fixes
│   └── guides/                 # Guías de desarrollo
│
├── .github/                    # GitHub Actions
│   └── workflows/              # CI/CD workflows
│
├── .gitignore                  # Archivos ignorados por Git
├── README.md                   # Este archivo
├── Dockerfile                  # Configuración Docker
├── railway.json                # Configuración Railway
├── vercel.json                 # Configuración Vercel
└── requirements.txt            # Dependencias Python (root)
```

---

## 🤝 Contribución

Este es un proyecto privado. Para contribuir:

1. Crea una rama desde `main`
2. Realiza tus cambios
3. Asegúrate de que los tests pasen
4. Crea un Pull Request
5. Espera la revisión del código

### Convenciones de Código

- **Backend**: Seguir PEP 8, usar Black y isort
- **Frontend**: Seguir ESLint config, usar Prettier
- **Commits**: Usar Conventional Commits
  - `feat:` Nueva funcionalidad
  - `fix:` Corrección de bug
  - `docs:` Cambios en documentación
  - `refactor:` Refactorización de código
  - `test:` Agregar o modificar tests
  - `chore:` Tareas de mantenimiento

---

## 📄 Licencia

Este proyecto es **privado y confidencial**. Todos los derechos reservados.

---

## 👥 Equipo

Desarrollado para gestión de mantenimiento industrial.

---

## 📞 Soporte

Para soporte técnico o consultas:
- 📧 Email: soporte@ejemplo.com
- 💬 Telegram: @Somacorbot
- 🐛 Issues: [GitHub Issues](https://github.com/tu-usuario/proyecto-de-titulo-produccion/issues)

---

## 🙏 Agradecimientos

- Django REST Framework por el excelente framework
- React y el equipo de Vite por las herramientas modernas
- Railway y Vercel por el hosting gratuito
- La comunidad open source

---

<div align="center">

**[⬆ Volver arriba](#-cmms---sistema-de-gestión-de-mantenimiento-computarizado)**

Hecho con ❤️ para la gestión de mantenimiento industrial

</div>
#   F o r c e   d e p l o y m e n t  
 