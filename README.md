# CMMS - Sistema de Gestión de Mantenimiento Computarizado

Sistema completo de gestión de mantenimiento para activos industriales, desarrollado con Django REST Framework y React + TypeScript.

## 🚀 Características

- **Gestión de Vehículos y Activos**: Control completo de la flota con 5 tipos de vehículos predefinidos
- **Órdenes de Trabajo**: Creación, asignación y seguimiento de tareas de mantenimiento
- **Mantenimiento Preventivo**: Programación de planes con reglas de recurrencia
- **Inventario de Repuestos**: Control de stock con alertas automáticas
- **Checklists Específicos**: Plantillas predefinidas por tipo de vehículo con generación de PDFs
- **Sistema de Notificaciones**: Alertas en tiempo real para el equipo
- **Reportes y Analíticas**: KPIs y métricas de mantenimiento (MTBF, MTTR, OEE)
- **Control de Acceso**: 3 roles (ADMIN, SUPERVISOR, OPERADOR) con permisos específicos

## 🛠️ Stack Tecnológico

### Backend
- Django 4.2+
- Django REST Framework 3.14+
- JWT Authentication
- SQLite (desarrollo) / PostgreSQL (producción)
- ReportLab (generación de PDFs)
- Hypothesis (property-based testing)

### Frontend
- React 18+
- TypeScript 5+
- Vite 5+
- Tailwind CSS
- Zustand (state management)
- Recharts (gráficos)

## 📋 Requisitos Previos

- Python 3.9+
- Node.js 18+
- npm o yarn

## 🔧 Instalación

### Backend

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
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Iniciar servidor de desarrollo
python manage.py runserver
```

El backend estará disponible en `http://localhost:8000`

### Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```

El frontend estará disponible en `http://localhost:5173`

## 📚 Documentación de la API

Una vez iniciado el backend, la documentación interactiva de la API está disponible en:

- Swagger UI: `http://localhost:8000/api/docs/`
- Schema OpenAPI: `http://localhost:8000/api/schema/`

## 🧪 Testing

### Backend

```bash
cd backend

# Ejecutar todos los tests
pytest

# Ejecutar tests con coverage
pytest --cov=apps --cov-report=html

# Ejecutar solo tests unitarios
pytest -m unit

# Ejecutar solo property-based tests
pytest -m property
```

### Frontend

```bash
cd frontend

# Ejecutar tests
npm run test

# Ejecutar tests con coverage
npm run test:coverage
```

## 🎨 Code Quality

### Backend

```bash
# Formatear código
black .
isort .

# Linting
flake8
```

### Frontend

```bash
# Formatear código
npm run format

# Linting
npm run lint
```

## 📁 Estructura del Proyecto

```
cmms-local/
├── backend/
│   ├── apps/
│   │   ├── authentication/    # Autenticación y usuarios
│   │   ├── assets/            # Gestión de activos
│   │   ├── work_orders/       # Órdenes de trabajo
│   │   ├── maintenance/       # Planes de mantenimiento
│   │   ├── inventory/         # Inventario de repuestos
│   │   ├── checklists/        # Sistema de checklists
│   │   ├── notifications/     # Notificaciones
│   │   ├── reports/           # Reportes y analíticas
│   │   ├── machine_status/    # Estado de máquinas
│   │   └── core/              # Utilidades compartidas
│   ├── config/                # Configuración Django
│   └── media/                 # Archivos subidos
│
└── frontend/
    └── src/
        ├── components/        # Componentes React
        ├── pages/             # Páginas
        ├── services/          # Servicios API
        ├── store/             # Estado global
        ├── types/             # Tipos TypeScript
        └── utils/             # Utilidades
```

## 🔐 Roles y Permisos

- **ADMIN**: Acceso completo al sistema, gestión de usuarios y configuración
- **SUPERVISOR**: Gestión de órdenes de trabajo, activos y reportes
- **OPERADOR**: Acceso limitado a órdenes asignadas y actualización de estado de máquinas

## 🚀 Despliegue

Ver documentación detallada en:
- [Guía de Setup Local](./docs/SETUP_LOCAL.md)
- [Guía de Inicio Rápido](./docs/INICIAR_PROYECTO_LOCAL.md)

## 📝 Licencia

Este proyecto es privado y confidencial.

## 👥 Equipo de Desarrollo

Desarrollado para gestión de mantenimiento industrial.

## 📞 Soporte

Para soporte técnico, contactar al equipo de desarrollo.
