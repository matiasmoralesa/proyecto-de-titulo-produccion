# Guía de Testing - Sistema CMMS

Esta guía describe la estrategia de testing y cómo ejecutar las pruebas del sistema.

## 📋 Estrategia de Testing

### Pirámide de Testing

```
        /\
       /  \      E2E Tests (10%)
      /____\
     /      \    Integration Tests (30%)
    /________\
   /          \  Unit Tests (60%)
  /____________\
```

## 🧪 Tipos de Tests

### 1. Unit Tests (Pruebas Unitarias)
- Prueban funciones y métodos individuales
- Rápidos de ejecutar
- No requieren base de datos ni servicios externos

### 2. Integration Tests (Pruebas de Integración)
- Prueban interacción entre componentes
- Usan base de datos de prueba
- Verifican endpoints de API

### 3. Property-Based Tests
- Usan Hypothesis para generar casos de prueba
- Verifican propiedades del sistema
- Encuentran edge cases

### 4. End-to-End Tests
- Prueban flujos completos de usuario
- Usan navegador real
- Más lentos pero más completos

## 🔧 Configuración de Testing

### Backend (Python/Django)

#### Instalar Dependencias
```bash
cd backend
pip install pytest pytest-django pytest-cov hypothesis factory-boy
```

#### Configuración pytest.ini
```ini
[pytest]
DJANGO_SETTINGS_MODULE = config.settings.development
python_files = tests.py test_*.py *_tests.py
addopts = --reuse-db --nomigrations
markers =
    unit: Unit tests
    integration: Integration tests
    property: Property-based tests
    slow: Slow running tests
```

### Frontend (React/TypeScript)

#### Instalar Dependencias
```bash
cd frontend
npm install --save-dev vitest @testing-library/react @testing-library/jest-dom
```

## 🚀 Ejecutar Tests

### Backend

#### Todos los Tests
```bash
cd backend
pytest
```

#### Con Coverage
```bash
pytest --cov=apps --cov-report=html --cov-report=term
```

#### Por Tipo
```bash
# Solo unit tests
pytest -m unit

# Solo integration tests
pytest -m integration

# Solo property tests
pytest -m property
```

#### Por Aplicación
```bash
# Tests de assets
pytest apps/assets/tests.py

# Tests de work orders
pytest apps/work_orders/

# Tests de seguridad
pytest apps/core/tests/test_security.py
```

#### Tests Específicos
```bash
# Un test específico
pytest apps/assets/tests.py::TestAssetModel::test_create_asset

# Tests que coincidan con patrón
pytest -k "test_create"
```

#### Modo Verbose
```bash
pytest -v
pytest -vv  # Extra verbose
```

### Frontend

#### Todos los Tests
```bash
cd frontend
npm run test
```

#### Con Coverage
```bash
npm run test:coverage
```

#### Watch Mode
```bash
npm run test:watch
```

#### Tests Específicos
```bash
npm run test -- ProtectedRoute.test.tsx
```

## 📊 Coverage Reports

### Backend
Después de ejecutar tests con coverage:
```bash
# Ver reporte en terminal
pytest --cov=apps --cov-report=term

# Generar reporte HTML
pytest --cov=apps --cov-report=html

# Abrir reporte
# Windows
start htmlcov/index.html
# Linux/Mac
open htmlcov/index.html
```

### Frontend
```bash
npm run test:coverage
# Reporte en coverage/index.html
```

## ✅ Tests Implementados

### Backend

#### Authentication Tests
- ✅ Login con credenciales válidas
- ✅ Login con credenciales inválidas
- ✅ Refresh token
- ✅ Logout
- ✅ Permisos por rol

#### Security Tests
- ✅ Autenticación (tokens inválidos, expirados)
- ✅ Autorización (permisos por rol)
- ✅ Validación de inputs (XSS, SQL injection)
- ✅ Headers de seguridad
- ✅ CORS configuration
- ✅ Password hashing
- ✅ Rate limiting
- ✅ Audit trail

#### Assets Tests
- ✅ Crear asset
- ✅ Actualizar asset
- ✅ Eliminar asset (soft delete)
- ✅ Filtros y búsqueda
- ✅ Validación de campos únicos

#### Work Orders Tests
- ✅ Crear orden de trabajo
- ✅ Asignar orden
- ✅ Cambiar estado
- ✅ Completar orden
- ✅ Validación de transiciones de estado

### Frontend

#### Component Tests
- ✅ ProtectedRoute redirecciona si no autenticado
- ✅ Componentes renderizan correctamente

## 🎯 Casos de Prueba Críticos

### Flujo Completo: Orden de Trabajo

1. **Crear Asset**
   ```python
   def test_create_asset():
       asset = Asset.objects.create(
           name="Test Asset",
           vehicle_type="VOLQUETE",
           serial_number="TEST-001"
       )
       assert asset.id is not None
   ```

2. **Crear Orden de Trabajo**
   ```python
   def test_create_work_order():
       wo = WorkOrder.objects.create(
           title="Test WO",
           asset=asset,
           assigned_to=user
       )
       assert wo.status == "Pendiente"
   ```

3. **Cambiar Estado**
   ```python
   def test_change_status():
       wo.status = "En Progreso"
       wo.save()
       assert wo.status == "En Progreso"
   ```

4. **Completar Orden**
   ```python
   def test_complete_work_order():
       wo.status = "Completada"
       wo.completed_date = timezone.now()
       wo.save()
       assert wo.status == "Completada"
   ```

### Property-Based Tests

```python
from hypothesis import given, strategies as st

@given(st.text(min_size=1, max_size=100))
def test_asset_name_always_valid(name):
    """Property: Asset name should always be stored correctly"""
    asset = Asset.objects.create(
        name=name,
        vehicle_type="VOLQUETE",
        serial_number=f"TEST-{uuid.uuid4()}"
    )
    assert asset.name == name
```

## 🐛 Debugging Tests

### Usar pdb
```python
def test_something():
    import pdb; pdb.set_trace()
    # Tu código aquí
```

### Ver Queries SQL
```python
from django.test.utils import override_settings

@override_settings(DEBUG=True)
def test_with_queries():
    from django.db import connection
    # Tu código
    print(connection.queries)
```

### Logs en Tests
```python
import logging
logger = logging.getLogger(__name__)

def test_with_logs():
    logger.info("Test started")
    # Tu código
```

## 📈 Métricas de Calidad

### Objetivos de Coverage
- **Backend**: > 80%
- **Frontend**: > 70%
- **Funciones críticas**: 100%

### Tiempo de Ejecución
- **Unit tests**: < 1 segundo cada uno
- **Integration tests**: < 5 segundos cada uno
- **Suite completa**: < 2 minutos

## 🔄 CI/CD Integration

### GitHub Actions Example
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.12
    
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        cd backend
        pytest --cov=apps --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

## 📝 Best Practices

### 1. Nombres Descriptivos
```python
# ❌ Mal
def test_1():
    pass

# ✅ Bien
def test_create_asset_with_valid_data_succeeds():
    pass
```

### 2. Arrange-Act-Assert
```python
def test_example():
    # Arrange (preparar)
    user = create_user()
    
    # Act (actuar)
    result = user.do_something()
    
    # Assert (verificar)
    assert result == expected
```

### 3. Un Assert por Test
```python
# ❌ Mal
def test_multiple_things():
    assert user.name == "John"
    assert user.email == "john@example.com"
    assert user.is_active == True

# ✅ Bien
def test_user_name():
    assert user.name == "John"

def test_user_email():
    assert user.email == "john@example.com"
```

### 4. Usar Fixtures
```python
@pytest.fixture
def sample_asset():
    return Asset.objects.create(
        name="Test Asset",
        vehicle_type="VOLQUETE"
    )

def test_with_fixture(sample_asset):
    assert sample_asset.name == "Test Asset"
```

### 5. Limpiar Después
```python
def test_cleanup():
    asset = Asset.objects.create(name="Test")
    try:
        # Test code
        pass
    finally:
        asset.delete()
```

## 🚨 Tests de Regresión

Cuando se encuentra un bug:

1. **Escribir test que reproduzca el bug**
2. **Verificar que el test falla**
3. **Arreglar el bug**
4. **Verificar que el test pasa**
5. **Mantener el test para prevenir regresión**

## 📚 Recursos

- [Pytest Documentation](https://docs.pytest.org/)
- [Django Testing](https://docs.djangoproject.com/en/4.2/topics/testing/)
- [Hypothesis](https://hypothesis.readthedocs.io/)
- [Testing Library](https://testing-library.com/)
- [Vitest](https://vitest.dev/)

## 🎓 Conclusión

Un buen conjunto de tests:
- ✅ Da confianza para hacer cambios
- ✅ Documenta el comportamiento esperado
- ✅ Previene regresiones
- ✅ Facilita el refactoring
- ✅ Mejora la calidad del código

**¡Escribe tests, no bugs!** 🐛➡️✅
