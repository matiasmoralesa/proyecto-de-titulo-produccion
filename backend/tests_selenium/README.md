# Selenium E2E Tests para CMMS

## Descripción

Suite de pruebas end-to-end (E2E) usando Selenium WebDriver para validar la funcionalidad completa del sistema CMMS desde la perspectiva del usuario.

## Requisitos Previos

1. **Python 3.8+** instalado
2. **Google Chrome** instalado
3. **ChromeDriver** (se instala automáticamente con webdriver-manager)
4. **Backend y Frontend** ejecutándose:
   - Backend: `http://localhost:8000`
   - Frontend: `http://localhost:5173`

## Instalación

### 1. Instalar dependencias de testing

```bash
cd backend
pip install -r requirements-test.txt
```

### 2. Verificar que el sistema esté ejecutándose

**Terminal 1 - Backend:**
```bash
cd backend
python manage.py runserver
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Terminal 3 - Ejecutar seed (si es necesario):**
```bash
cd backend
python seed_all_data.py
```

## Ejecutar Tests

### Ejecutar todos los tests

```bash
cd backend
pytest tests_selenium/ -v
```

### Ejecutar tests específicos

```bash
# Solo tests de autenticación
pytest tests_selenium/test_auth.py -v

# Solo tests de dashboard
pytest tests_selenium/test_dashboard.py -v

# Solo tests de assets
pytest tests_selenium/test_assets.py -v

# Solo tests de work orders
pytest tests_selenium/test_work_orders.py -v

# Solo tests de ML predictions
pytest tests_selenium/test_ml_predictions.py -v
```

### Ejecutar con modo visible (sin headless)

Editar `tests_selenium/conftest.py` y comentar la línea:
```python
# chrome_options.add_argument("--headless")
```

### Ejecutar un test específico

```bash
pytest tests_selenium/test_auth.py::TestAuthentication::test_successful_login -v
```

## Estructura de Tests

```
tests_selenium/
├── __init__.py                 # Inicialización del paquete
├── conftest.py                 # Configuración de fixtures de pytest
├── test_auth.py                # Tests de autenticación
├── test_dashboard.py           # Tests del dashboard
├── test_assets.py              # Tests de gestión de activos
├── test_work_orders.py         # Tests de órdenes de trabajo
├── test_ml_predictions.py      # Tests de predicciones ML
└── README.md                   # Esta documentación
```

## Tests Incluidos

### 1. Autenticación (`test_auth.py`)
- ✅ Carga de página de login
- ✅ Login exitoso
- ✅ Login fallido con credenciales inválidas
- ✅ Logout
- ✅ Redirección de rutas protegidas

### 2. Dashboard (`test_dashboard.py`)
- ✅ Carga del dashboard
- ✅ Visualización de KPIs
- ✅ Presencia del menú de navegación
- ✅ Información del usuario

### 3. Gestión de Activos (`test_assets.py`)
- ✅ Navegación a página de activos
- ✅ Carga de lista de activos
- ✅ Búsqueda de activos
- ✅ Visualización de detalles
- ✅ Filtrado por estado

### 4. Órdenes de Trabajo (`test_work_orders.py`)
- ✅ Navegación a órdenes de trabajo
- ✅ Carga de lista
- ✅ Filtrado por estado
- ✅ Visualización de detalles
- ✅ Búsqueda

### 5. Predicciones ML (`test_ml_predictions.py`)
- ✅ Navegación a predicciones
- ✅ Carga de lista de predicciones
- ✅ Indicadores de nivel de riesgo
- ✅ Filtrado por nivel de riesgo
- ✅ Visualización de detalles
- ✅ Botón de generar predicciones

## Credenciales de Prueba

Las credenciales están definidas en `conftest.py`:

```python
{
    "admin": {"username": "admin", "password": "admin123"},
    "supervisor": {"username": "supervisor", "password": "super123"},
    "operator": {"username": "operator1", "password": "oper123"}
}
```

## Configuración Avanzada

### Cambiar URLs

Editar `conftest.py`:

```python
@pytest.fixture(scope="session")
def base_url():
    return "http://localhost:5173"  # URL del frontend

@pytest.fixture(scope="session")
def api_url():
    return "http://localhost:8000"  # URL del backend
```

### Ajustar Timeouts

Los tests usan `implicitly_wait(10)` por defecto. Para ajustar:

```python
driver.implicitly_wait(20)  # Esperar hasta 20 segundos
```

### Modo Headless vs Visible

**Headless (por defecto):**
- Más rápido
- No requiere interfaz gráfica
- Ideal para CI/CD

**Visible:**
- Ver la ejecución en tiempo real
- Útil para debugging
- Comentar línea en `conftest.py`

## Troubleshooting

### Error: "ChromeDriver not found"
```bash
pip install --upgrade webdriver-manager
```

### Error: "Connection refused"
Verificar que backend y frontend estén ejecutándose:
```bash
# Verificar backend
curl http://localhost:8000/api/v1/

# Verificar frontend
curl http://localhost:5173/
```

### Tests fallan por timeouts
- Aumentar `implicitly_wait` en `conftest.py`
- Verificar que el sistema no esté sobrecargado
- Ejecutar en modo visible para ver qué está pasando

### Error: "Element not found"
- El frontend puede haber cambiado
- Actualizar los selectores CSS en los tests
- Verificar que los datos de seed existan

## Reportes

### Generar reporte HTML

```bash
pytest tests_selenium/ --html=report.html --self-contained-html
```

### Generar reporte con cobertura

```bash
pytest tests_selenium/ --cov=. --cov-report=html
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: E2E Tests

on: [push, pull_request]

jobs:
  e2e-tests:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -r backend/requirements.txt
          pip install -r backend/requirements-test.txt
      
      - name: Start backend
        run: |
          cd backend
          python manage.py migrate
          python seed_all_data.py
          python manage.py runserver &
      
      - name: Start frontend
        run: |
          cd frontend
          npm install
          npm run build
          npm run preview &
      
      - name: Run E2E tests
        run: |
          cd backend
          pytest tests_selenium/ -v
```

## Mejores Prácticas

1. **Siempre ejecutar seed antes de los tests** para tener datos consistentes
2. **Usar fixtures** para setup y teardown
3. **Usar waits explícitos** en lugar de `time.sleep()` cuando sea posible
4. **Mantener tests independientes** - cada test debe poder ejecutarse solo
5. **Usar selectores robustos** - preferir IDs y data attributes sobre clases CSS
6. **Documentar tests complejos** con comentarios claros

## Contribuir

Para agregar nuevos tests:

1. Crear archivo `test_<feature>.py` en `tests_selenium/`
2. Seguir el patrón de clase `Test<Feature>`
3. Usar fixtures de `conftest.py`
4. Documentar con docstrings
5. Ejecutar y verificar que pasen

## Soporte

Para problemas o preguntas:
- Revisar logs de Selenium
- Ejecutar en modo visible para debugging
- Verificar que el sistema esté funcionando manualmente primero
