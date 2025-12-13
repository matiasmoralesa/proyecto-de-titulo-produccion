# 📚 06_LIBRERIAS - Dependencias y APIs del Proyecto

## 📋 Contenido de esta Carpeta

Esta carpeta incluye las librerías o APIs utilizadas en el proyecto con una breve explicación de uso de cada una de ellas.

## 🔧 Backend - Dependencias Python

### Framework Principal
- **Django 4.2.7**
  - **Uso**: Framework web principal para el backend
  - **Justificación**: Robusto, seguro, con ORM integrado y admin panel
  - **Documentación**: https://docs.djangoproject.com/

- **Django REST Framework 3.14.0**
  - **Uso**: Creación de APIs REST para comunicación frontend-backend
  - **Justificación**: Serialización automática, autenticación JWT, documentación automática
  - **Documentación**: https://www.django-rest-framework.org/

### Machine Learning
- **scikit-learn 1.3.0**
  - **Uso**: Algoritmos de Machine Learning (Random Forest Classifier)
  - **Justificación**: Biblioteca estándar, bien documentada, excelente para clasificación
  - **Documentación**: https://scikit-learn.org/

- **joblib 1.3.2**
  - **Uso**: Serialización y carga de modelos ML entrenados
  - **Justificación**: Optimizado para arrays NumPy, más eficiente que pickle para ML
  - **Documentación**: https://joblib.readthedocs.io/

- **numpy 1.24.3**
  - **Uso**: Operaciones matemáticas y arrays para ML
  - **Justificación**: Base fundamental para computación científica en Python
  - **Documentación**: https://numpy.org/

- **pandas 2.0.3**
  - **Uso**: Manipulación y análisis de datos para entrenamiento ML
  - **Justificación**: Herramienta estándar para análisis de datos estructurados
  - **Documentación**: https://pandas.pydata.org/

### Base de Datos
- **psycopg2-binary 2.9.7**
  - **Uso**: Adaptador PostgreSQL para Python/Django
  - **Justificación**: Driver oficial y más eficiente para PostgreSQL
  - **Documentación**: https://www.psycopg.org/

### Tareas Asíncronas
- **celery 5.3.0**
  - **Uso**: Ejecución de tareas asíncronas (predicciones ML, notificaciones)
  - **Justificación**: Escalable, robusto, integración perfecta con Django
  - **Documentación**: https://docs.celeryq.dev/

- **redis 4.6.0**
  - **Uso**: Broker de mensajes para Celery y cache
  - **Justificación**: Rápido, confiable, soporte nativo para Celery
  - **Documentación**: https://redis.io/

- **django-celery-beat 2.5.0**
  - **Uso**: Programación de tareas periódicas (predicciones diarias)
  - **Justificación**: Integración nativa con Django, interfaz admin
  - **Documentación**: https://django-celery-beat.readthedocs.io/

- **django-celery-results 2.5.1**
  - **Uso**: Almacenamiento de resultados de tareas Celery en BD
  - **Justificación**: Persistencia de resultados, monitoreo de tareas
  - **Documentación**: https://django-celery-results.readthedocs.io/

### Autenticación y Seguridad
- **djangorestframework-simplejwt 5.3.0**
  - **Uso**: Autenticación JWT para APIs
  - **Justificación**: Stateless, seguro, estándar de la industria
  - **Documentación**: https://django-rest-framework-simplejwt.readthedocs.io/

- **django-cors-headers 4.2.0**
  - **Uso**: Manejo de CORS para comunicación frontend-backend
  - **Justificación**: Necesario para SPAs, configuración granular
  - **Documentación**: https://github.com/adamchainz/django-cors-headers

### Configuración y Utilidades
- **python-decouple 3.8**
  - **Uso**: Gestión de variables de entorno y configuración
  - **Justificación**: Separación de configuración del código, seguridad
  - **Documentación**: https://python-decouple.readthedocs.io/

- **gunicorn 21.2.0**
  - **Uso**: Servidor WSGI para producción
  - **Justificación**: Robusto, escalable, estándar para Django en producción
  - **Documentación**: https://gunicorn.org/

### Documentación API
- **drf-spectacular 0.26.4**
  - **Uso**: Generación automática de documentación OpenAPI/Swagger
  - **Justificación**: Documentación interactiva automática de APIs
  - **Documentación**: https://drf-spectacular.readthedocs.io/

### Testing y Calidad de Código
- **pytest 7.4.3**
  - **Uso**: Framework de testing más avanzado que unittest
  - **Justificación**: Sintaxis simple, fixtures potentes, plugins extensos
  - **Documentación**: https://pytest.org/

- **pytest-django 4.5.2**
  - **Uso**: Integración de pytest con Django
  - **Justificación**: Testing optimizado para aplicaciones Django
  - **Documentación**: https://pytest-django.readthedocs.io/

- **coverage 7.3.2**
  - **Uso**: Medición de cobertura de código en tests
  - **Justificación**: Garantizar calidad y completitud de tests
  - **Documentación**: https://coverage.readthedocs.io/

- **flake8 6.1.0**
  - **Uso**: Linting y verificación de estilo de código Python
  - **Justificación**: Mantener código limpio y consistente
  - **Documentación**: https://flake8.pycqa.org/

- **black 23.9.1**
  - **Uso**: Formateador automático de código Python
  - **Justificación**: Estilo consistente, sin configuración
  - **Documentación**: https://black.readthedocs.io/

- **isort 5.12.0**
  - **Uso**: Ordenamiento automático de imports
  - **Justificación**: Organización consistente de imports
  - **Documentación**: https://pycqa.github.io/isort/

## 🎨 Frontend - Dependencias Node.js

### Framework Principal
- **React 18.2.0**
  - **Uso**: Biblioteca principal para construcción de UI
  - **Justificación**: Ecosistema maduro, componentes reutilizables, virtual DOM
  - **Documentación**: https://react.dev/

- **TypeScript 5.0.2**
  - **Uso**: Tipado estático para JavaScript
  - **Justificación**: Mejor experiencia de desarrollo, menos errores en runtime
  - **Documentación**: https://www.typescriptlang.org/

### Build Tools
- **Vite 4.4.5**
  - **Uso**: Build tool y dev server ultra-rápido
  - **Justificación**: HMR instantáneo, builds optimizados, configuración mínima
  - **Documentación**: https://vitejs.dev/

### Routing
- **React Router DOM 6.15.0**
  - **Uso**: Navegación y routing en SPA
  - **Justificación**: Estándar de facto para routing en React
  - **Documentación**: https://reactrouter.com/

### Estilos y UI
- **Tailwind CSS 3.3.0**
  - **Uso**: Framework CSS utility-first
  - **Justificación**: Desarrollo rápido, diseño consistente, altamente customizable
  - **Documentación**: https://tailwindcss.com/

- **React Icons 4.10.1**
  - **Uso**: Biblioteca de iconos para React
  - **Justificación**: Amplia colección, fácil de usar, tree-shaking
  - **Documentación**: https://react-icons.github.io/react-icons/

### HTTP Client
- **Axios 1.5.0**
  - **Uso**: Cliente HTTP para comunicación con APIs
  - **Justificación**: Interceptors, manejo de errores, cancelación de requests
  - **Documentación**: https://axios-http.com/

### Gráficos y Visualización
- **Recharts 2.8.0**
  - **Uso**: Biblioteca de gráficos para React
  - **Justificación**: Componentes declarativos, responsive, bien integrado con React
  - **Documentación**: https://recharts.org/

### Utilidades
- **date-fns 2.30.0**
  - **Uso**: Manipulación y formateo de fechas
  - **Justificación**: Modular, inmutable, soporte para i18n
  - **Documentación**: https://date-fns.org/

- **clsx 2.0.0**
  - **Uso**: Construcción condicional de clases CSS
  - **Justificación**: Pequeño, rápido, sintaxis limpia
  - **Documentación**: https://github.com/lukeed/clsx

## 🚀 DevOps y Despliegue

### Hosting y Despliegue
- **Railway**
  - **Uso**: Hosting del backend Django + PostgreSQL + Redis
  - **Justificación**: Despliegue automático desde Git, bases de datos integradas
  - **Documentación**: https://railway.app/

- **Vercel**
  - **Uso**: Hosting del frontend React
  - **Justificación**: Optimizado para SPAs, CDN global, despliegue automático
  - **Documentación**: https://vercel.com/

### CI/CD
- **GitHub Actions**
  - **Uso**: Integración continua y despliegue automático
  - **Justificación**: Integrado con GitHub, workflows flexibles
  - **Documentación**: https://docs.github.com/actions

## 📊 APIs Externas y Servicios

### Notificaciones
- **Telegram Bot API**
  - **Uso**: Envío de notificaciones por Telegram
  - **Justificación**: Gratuito, confiable, fácil integración
  - **Documentación**: https://core.telegram.org/bots/api

### Monitoreo y Logs
- **Railway Logs**
  - **Uso**: Monitoreo de aplicación en producción
  - **Justificación**: Integrado con hosting, logs en tiempo real

- **Vercel Analytics**
  - **Uso**: Métricas de performance del frontend
  - **Justificación**: Integrado con hosting, métricas de Core Web Vitals

## 🔧 Herramientas de Desarrollo

### Editores y IDEs
- **Visual Studio Code**
  - **Extensiones recomendadas**:
    - Python
    - Django
    - TypeScript
    - Tailwind CSS IntelliSense
    - Prettier
    - ESLint

### Control de Versiones
- **Git**
  - **Uso**: Control de versiones distribuido
  - **Plataforma**: GitHub para repositorio remoto

### Testing
- **Postman**
  - **Uso**: Testing manual de APIs
  - **Justificación**: Interfaz intuitiva, colecciones organizadas

## 📋 Archivo de Dependencias

### Backend (requirements.txt)
```
Django==4.2.7
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0
django-cors-headers==4.2.0
django-celery-beat==2.5.0
django-celery-results==2.5.1
drf-spectacular==0.26.4
psycopg2-binary==2.9.7
celery==5.3.0
redis==4.6.0
python-decouple==3.8
gunicorn==21.2.0
scikit-learn==1.3.0
joblib==1.3.2
numpy==1.24.3
pandas==2.0.3
pytest==7.4.3
pytest-django==4.5.2
coverage==7.3.2
flake8==6.1.0
black==23.9.1
isort==5.12.0
```

### Frontend (package.json)
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "typescript": "^5.0.2",
    "react-router-dom": "^6.15.0",
    "axios": "^1.5.0",
    "react-icons": "^4.10.1",
    "recharts": "^2.8.0",
    "date-fns": "^2.30.0",
    "clsx": "^2.0.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.15",
    "@types/react-dom": "^18.2.7",
    "@vitejs/plugin-react": "^4.0.3",
    "vite": "^4.4.5",
    "tailwindcss": "^3.3.0",
    "autoprefixer": "^10.4.14",
    "postcss": "^8.4.27"
  }
}
```

## 🎯 Criterios de Selección

### Factores Considerados:
1. **Madurez**: Librerías estables con comunidad activa
2. **Documentación**: Documentación completa y actualizada
3. **Performance**: Optimizadas para producción
4. **Seguridad**: Actualizaciones regulares de seguridad
5. **Compatibilidad**: Integración fluida entre componentes
6. **Mantenimiento**: Facilidad de actualización y mantenimiento

### Alternativas Evaluadas:
- **Flask vs Django**: Django elegido por ORM, admin panel y ecosistema
- **Vue vs React**: React por ecosistema más maduro y TypeScript
- **Bootstrap vs Tailwind**: Tailwind por flexibilidad y performance
- **Webpack vs Vite**: Vite por velocidad de desarrollo

---
*Documentación de Librerías y APIs - Sistema CMMS v1.0 - Diciembre 2025*