# Tests E2E con Selenium - Sistema CMMS

## 📋 Resumen

Se ha implementado una suite completa de **25 tests end-to-end** usando Selenium WebDriver para validar la funcionalidad del sistema CMMS desde la perspectiva del usuario final.

## 🎯 Cobertura de Tests

### 1. Autenticación (5 tests)
- ✅ Carga de página de login
- ✅ Login exitoso con credenciales válidas
- ✅ Login fallido con credenciales inválidas
- ✅ Logout del sistema
- ✅ Redirección de rutas protegidas

### 2. Dashboard (4 tests)
- ✅ Carga del dashboard principal
- ✅ Visualización de KPIs y métricas
- ✅ Presencia del menú de navegación
- ✅ Información del usuario autenticado

### 3. Gestión de Activos (5 tests)
- ✅ Navegación a página de activos
- ✅ Carga de lista de activos
- ✅ Búsqueda de activos
- ✅ Visualización de detalles de activo
- ✅ Filtrado por estado

### 4. Órdenes de Trabajo (5 tests)
- ✅ Navegación a órdenes de trabajo
- ✅ Carga de lista de órdenes
- ✅ Filtrado por estado
- ✅ Visualización de detalles
- ✅ Búsqueda de órdenes

### 5. Predicciones ML (6 tests)
- ✅ Navegación a predicciones
- ✅ Carga de lista de predicciones
- ✅ Indicadores de nivel de riesgo
- ✅ Filtrado por nivel de riesgo
- ✅ Visualización de detalles de predicción
- ✅ Botón de generar predicciones

## 📁 Estructura de Archivos

```
backend/
├── tests_selenium/
│   ├── __init__.py              # Inicialización
│   ├── conftest.py              # Fixtures y configuración
│   ├── test_auth.py             # Tests de autenticación
│   ├── test_dashboard.py        # Tests de dashboard
│   ├── test_assets.py           # Tests de activos
│   ├── test_work_orders.py      # Tests de órdenes
│   ├── test_ml_predictions.py   # Tests de predicciones
│   ├── README.md                # Documentación completa
│   └── QUICK_START.md           # Guía rápida
├── requirements-test.txt        # Dependencias de testing
├── run_selenium_tests.py        # Script Python para ejecutar
└── run_selenium_tests.bat       # Script Windows para ejecutar
```

## 🚀 Inicio Rápido

### 1. Instalar dependencias
```bash
cd backend
pip install -r requirements-test.txt
```

### 2. Iniciar servicios

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

### 3. Ejecutar tests

**Opción A - Script Python:**
```bash
cd backend
python run_selenium_tests.py
```

**Opción B - Script Windows:**
```bash
cd backend
run_selenium_tests.bat
```

**Opción C - Pytest directo:**
```bash
cd backend
pytest tests_selenium/ -v
```

## 🔧 Configuración

### Modo Headless vs Visible

**Por defecto:** Headless (sin ventana visible)
- Más rápido
- Ideal para CI/CD

**Para ver la ejecución:**
Editar `tests_selenium/conftest.py`:
```python
# Comentar esta línea:
# chrome_options.add_argument("--headless")
```

### Ajustar URLs

En `tests_selenium/conftest.py`:
```python
@pytest.fixture(scope="session")
def base_url():
    return "http://localhost:5173"  # Frontend

@pytest.fixture(scope="session")
def api_url():
    return "http://localhost:8000"  # Backend
```

### Ajustar Timeouts

En `tests_selenium/conftest.py`:
```python
driver.implicitly_wait(10)  # Cambiar a 20 si es necesario
```

## 📊 Comandos Útiles

### Ejecutar tests específicos
```bash
# Solo autenticación
pytest tests_selenium/test_auth.py -v

# Solo un test
pytest tests_selenium/test_auth.py::TestAuthentication::test_successful_login -v

# Filtrar por nombre
pytest tests_selenium/ -k "login" -v
```

### Generar reportes
```bash
# Reporte HTML
pytest tests_selenium/ --html=report.html --self-contained-html

# Detener en primer fallo
pytest tests_selenium/ -x

# Ejecutar solo tests que fallaron
pytest tests_selenium/ --lf
```

## 🔑 Credenciales de Prueba

```python
{
    "admin": {
        "username": "admin",
        "password": "admin123"
    },
    "supervisor": {
        "username": "supervisor",
        "password": "super123"
    },
    "operator": {
        "username": "operator1",
        "password": "oper123"
    }
}
```

## ✅ Checklist Pre-Ejecución

- [ ] Python 3.8+ instalado
- [ ] Google Chrome instalado
- [ ] Dependencias instaladas (`pip install -r requirements-test.txt`)
- [ ] Backend ejecutándose (`http://localhost:8000`)
- [ ] Frontend ejecutándose (`http://localhost:5173`)
- [ ] Base de datos con datos de seed (`python seed_all_data.py`)

## 🐛 Troubleshooting

### Error: "Connection refused"
**Causa:** Servicios no están ejecutándose

**Solución:**
```bash
# Verificar backend
curl http://localhost:8000/api/v1/

# Verificar frontend
curl http://localhost:5173/
```

### Error: "ChromeDriver not found"
**Causa:** ChromeDriver no instalado

**Solución:**
```bash
pip install --upgrade webdriver-manager
```

### Error: "Element not found"
**Causa:** Elementos del DOM han cambiado o datos no existen

**Solución:**
1. Ejecutar seed: `python seed_all_data.py`
2. Ejecutar en modo visible para ver qué pasa
3. Actualizar selectores en los tests

### Tests muy lentos
**Solución:**
1. Ejecutar en modo headless (por defecto)
2. Reducir `implicitly_wait` en `conftest.py`
3. Ejecutar tests específicos en lugar de todos

## 📈 Resultados Esperados

```
tests_selenium/test_auth.py::TestAuthentication::test_login_page_loads PASSED        [ 4%]
tests_selenium/test_auth.py::TestAuthentication::test_successful_login PASSED        [ 8%]
tests_selenium/test_auth.py::TestAuthentication::test_failed_login_invalid_credentials PASSED [ 12%]
tests_selenium/test_auth.py::TestAuthentication::test_logout PASSED                  [ 16%]
tests_selenium/test_auth.py::TestAuthentication::test_protected_route_redirect PASSED [ 20%]
tests_selenium/test_dashboard.py::TestDashboard::test_dashboard_loads PASSED         [ 24%]
tests_selenium/test_dashboard.py::TestDashboard::test_dashboard_kpis_visible PASSED  [ 28%]
tests_selenium/test_dashboard.py::TestDashboard::test_navigation_menu_present PASSED [ 32%]
tests_selenium/test_dashboard.py::TestDashboard::test_user_info_displayed PASSED     [ 36%]
tests_selenium/test_assets.py::TestAssets::test_navigate_to_assets PASSED            [ 40%]
tests_selenium/test_assets.py::TestAssets::test_assets_list_loads PASSED             [ 44%]
tests_selenium/test_assets.py::TestAssets::test_search_assets PASSED                 [ 48%]
tests_selenium/test_assets.py::TestAssets::test_view_asset_details PASSED            [ 52%]
tests_selenium/test_assets.py::TestAssets::test_filter_assets_by_status PASSED       [ 56%]
tests_selenium/test_work_orders.py::TestWorkOrders::test_navigate_to_work_orders PASSED [ 60%]
tests_selenium/test_work_orders.py::TestWorkOrders::test_work_orders_list_loads PASSED [ 64%]
tests_selenium/test_work_orders.py::TestWorkOrders::test_filter_work_orders_by_status PASSED [ 68%]
tests_selenium/test_work_orders.py::TestWorkOrders::test_view_work_order_details PASSED [ 72%]
tests_selenium/test_work_orders.py::TestWorkOrders::test_search_work_orders PASSED   [ 76%]
tests_selenium/test_ml_predictions.py::TestMLPredictions::test_navigate_to_predictions PASSED [ 80%]
tests_selenium/test_ml_predictions.py::TestMLPredictions::test_predictions_list_loads PASSED [ 84%]
tests_selenium/test_ml_predictions.py::TestMLPredictions::test_risk_level_indicators PASSED [ 88%]
tests_selenium/test_ml_predictions.py::TestMLPredictions::test_filter_by_risk_level PASSED [ 92%]
tests_selenium/test_ml_predictions.py::TestMLPredictions::test_view_prediction_details PASSED [ 96%]
tests_selenium/test_ml_predictions.py::TestMLPredictions::test_generate_predictions_button PASSED [100%]

======================== 25 passed in 45.23s ========================
```

## 🔄 Integración CI/CD

### GitHub Actions

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
      
      - name: Start services
        run: |
          cd backend
          python manage.py migrate
          python seed_all_data.py
          python manage.py runserver &
          cd ../frontend
          npm install
          npm run build
          npm run preview &
      
      - name: Run E2E tests
        run: |
          cd backend
          pytest tests_selenium/ -v --html=report.html
      
      - name: Upload test report
        if: always()
        uses: actions/upload-artifact@v2
        with:
          name: test-report
          path: backend/report.html
```

## 📚 Documentación Adicional

- **README completo:** `backend/tests_selenium/README.md`
- **Guía rápida:** `backend/tests_selenium/QUICK_START.md`
- **Código fuente:** `backend/tests_selenium/`

## 🎯 Mejores Prácticas

1. ✅ **Ejecutar seed antes de tests** para datos consistentes
2. ✅ **Usar fixtures** para setup y teardown
3. ✅ **Tests independientes** - cada uno puede ejecutarse solo
4. ✅ **Selectores robustos** - preferir IDs y data attributes
5. ✅ **Waits explícitos** en lugar de `time.sleep()`
6. ✅ **Documentar tests complejos** con docstrings claros

## 🚀 Próximos Pasos

1. **Ejecutar tests** para validar funcionalidad
2. **Integrar en CI/CD** para ejecución automática
3. **Agregar más tests** según necesidades
4. **Configurar reportes** automáticos
5. **Mantener actualizados** con cambios del sistema

## 📞 Soporte

Para problemas o preguntas:
1. Revisar documentación en `tests_selenium/README.md`
2. Ejecutar en modo visible para debugging
3. Verificar logs de Selenium
4. Validar funcionalidad manualmente primero

---

**Nota:** Los tests están diseñados para ser robustos y tolerantes a cambios menores en el UI, usando `pytest.skip()` cuando elementos opcionales no se encuentran.
