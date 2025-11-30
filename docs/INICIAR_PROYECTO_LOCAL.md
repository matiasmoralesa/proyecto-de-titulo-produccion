# Guía Rápida: Iniciar Proyecto Local

Esta es una guía rápida para iniciar el proyecto CMMS en tu máquina local.

## Inicio Rápido (5 minutos)

### 1. Backend (Terminal 1)
```bash
cd backend
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac
python manage.py runserver
```

### 2. Frontend (Terminal 2)
```bash
cd frontend
npm run dev
```

### 3. Celery Worker (Terminal 3) - Opcional
```bash
cd backend
venv\Scripts\activate
celery -A config worker -l info --pool=solo
```

### 4. Celery Beat (Terminal 4) - Opcional
```bash
cd backend
venv\Scripts\activate
celery -A config beat -l info
```

## Acceso al Sistema

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000/api/v1/
- **API Docs:** http://localhost:8000/api/docs/
- **Admin Django:** http://localhost:8000/admin/

## Credenciales por Defecto

- **Usuario:** admin
- **Contraseña:** admin123

## Scripts de Inicio Rápido

### Windows

Crea un archivo `start_all.bat` en la raíz del proyecto:

```batch
@echo off
echo Iniciando Sistema CMMS...

start "Django Server" cmd /k "cd backend && venv\Scripts\activate && python manage.py runserver"
timeout /t 3
start "Celery Worker" cmd /k "cd backend && venv\Scripts\activate && celery -A config worker -l info --pool=solo"
timeout /t 2
start "Celery Beat" cmd /k "cd backend && venv\Scripts\activate && celery -A config beat -l info"
timeout /t 2
start "Frontend Dev Server" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo Sistema CMMS iniciado correctamente
echo ========================================
echo.
echo Frontend: http://localhost:5173
echo Backend API: http://localhost:8000/api/v1/
echo API Docs: http://localhost:8000/api/docs/
echo.
pause
```

### Linux/Mac

Crea un archivo `start_all.sh` en la raíz del proyecto:

```bash
#!/bin/bash

echo "Iniciando Sistema CMMS..."

# Backend
cd backend
source venv/bin/activate
python manage.py runserver &
DJANGO_PID=$!

# Celery Worker
celery -A config worker -l info &
CELERY_WORKER_PID=$!

# Celery Beat
celery -A config beat -l info &
CELERY_BEAT_PID=$!

# Frontend
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "========================================"
echo "Sistema CMMS iniciado correctamente"
echo "========================================"
echo ""
echo "Frontend: http://localhost:5173"
echo "Backend API: http://localhost:8000/api/v1/"
echo "API Docs: http://localhost:8000/api/docs/"
echo ""
echo "Presiona Ctrl+C para detener todos los servicios"

# Trap Ctrl+C
trap "kill $DJANGO_PID $CELERY_WORKER_PID $CELERY_BEAT_PID $FRONTEND_PID; exit" INT

wait
```

Dar permisos de ejecución:
```bash
chmod +x start_all.sh
./start_all.sh
```

## Comandos Útiles

### Reiniciar Servicios

```bash
# Detener todos los procesos de Python
# Windows
taskkill /F /IM python.exe

# Linux/Mac
pkill -f python
pkill -f node
```

### Limpiar y Reiniciar

```bash
# Backend
cd backend
python manage.py flush --no-input
python manage.py migrate
python create_superuser.py

# Frontend
cd frontend
rm -rf node_modules
npm install
```

### Ver Logs

```bash
# Backend logs
tail -f backend/logs/cmms.log

# Celery logs
tail -f backend/logs/celery.log
```

## Generar Datos de Prueba

```bash
cd backend
python create_sample_assets.py
python create_sample_workorders.py
python create_sample_inventory.py
python create_sample_maintenance.py
python generate_predictions.py
```

## Verificación Rápida

### 1. Verificar Backend
```bash
curl http://localhost:8000/api/v1/
```

### 2. Verificar Frontend
Abre http://localhost:5173 en tu navegador

### 3. Verificar Celery
```bash
cd backend
celery -A config inspect active
```

## Detener Todo

### Windows
Cierra todas las ventanas de terminal o:
```batch
taskkill /F /IM python.exe
taskkill /F /IM node.exe
```

### Linux/Mac
```bash
pkill -f "python manage.py runserver"
pkill -f "celery"
pkill -f "npm run dev"
```

## Problemas Comunes

### Puerto en Uso
```bash
# Windows - Liberar puerto 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac - Liberar puerto 8000
lsof -ti:8000 | xargs kill -9
```

### Base de Datos Bloqueada
```bash
cd backend
rm db.sqlite3
python manage.py migrate
python create_superuser.py
```

### Módulos No Encontrados
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

## Desarrollo Diario

### Flujo de Trabajo Típico:

1. **Iniciar servicios** (usar scripts de inicio)
2. **Hacer cambios** en el código
3. **Ver cambios** (hot reload automático)
4. **Ejecutar tests** antes de commit
5. **Commit y push** cambios

### Antes de Hacer Commit:

```bash
# Backend
cd backend
pytest
black .
isort .

# Frontend
cd frontend
npm run lint
npm run test
```

## Recursos Rápidos

- 📚 [Documentación Completa](./SETUP_LOCAL.md)
- 🔧 [Guía de Optimización](./PERFORMANCE_OPTIMIZATION.md)
- 📖 [API Docs](http://localhost:8000/api/docs/)
- 🐛 [Troubleshooting](./SETUP_LOCAL.md#solución-de-problemas-comunes)

## Atajos de Teclado

### Frontend:
- `Ctrl+K` - Búsqueda global
- `ESC` - Cerrar modales
- `F5` - Recargar página

### VS Code:
- `Ctrl+Shift+P` - Command Palette
- `Ctrl+`` - Toggle Terminal
- `Ctrl+B` - Toggle Sidebar

¡Listo para desarrollar! 🚀
