# Guía Rápida - Tests Selenium E2E

## 🚀 Inicio Rápido (5 minutos)

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

**Terminal 3:**
```bash
cd backend
python run_selenium_tests.py
```

O usando pytest directamente:
```bash
pytest tests_selenium/ -v
```

## 📋 Comandos Útiles

### Ejecutar todos los tests
```bash
pytest tests_selenium/ -v
```

### Ejecutar un módulo específico
```bash
pytest tests_selenium/test_auth.py -v
```

### Ejecutar un test específico
```bash
pytest tests_selenium/test_auth.py::TestAuthentication::test_successful_login -v
```

### Ejecutar con reporte HTML
```bash
pytest tests_selenium/ --html=report.html --self-contained-html
```

### Ejecutar en modo visible (sin headless)
Editar `conftest.py` y comentar:
```python
# chrome_options.add_argument("--headless")
```

## ✅ Checklist Pre-Test

- [ ] Backend ejecutándose en `http://localhost:8000`
- [ ] Frontend ejecutándose en `http://localhost:5173`
- [ ] Base de datos con datos de seed (`python seed_all_data.py`)
- [ ] Chrome instalado
- [ ] Dependencias instaladas (`pip install -r requirements-test.txt`)

## 🔑 Credenciales de Prueba

```
Admin:      admin / admin123
Supervisor: supervisor / super123
Operador:   operator1 / oper123
```

## 📊 Tests Disponibles

| Módulo | Tests | Descripción |
|--------|-------|-------------|
| `test_auth.py` | 5 | Autenticación y autorización |
| `test_dashboard.py` | 4 | Dashboard y KPIs |
| `test_assets.py` | 5 | Gestión de activos |
| `test_work_orders.py` | 5 | Órdenes de trabajo |
| `test_ml_predictions.py` | 6 | Predicciones ML |

**Total: 25 tests E2E**

## 🐛 Troubleshooting Rápido

### Error: "Connection refused"
```bash
# Verificar servicios
curl http://localhost:8000/api/v1/
curl http://localhost:5173/
```

### Error: "ChromeDriver not found"
```bash
pip install --upgrade webdriver-manager
```

### Tests muy lentos
- Ejecutar en modo headless (por defecto)
- Reducir número de tests
- Verificar recursos del sistema

### Error: "Element not found"
- Verificar que los datos de seed existan
- Aumentar timeouts en `conftest.py`
- Ejecutar en modo visible para debugging

## 📈 Resultados Esperados

```
tests_selenium/test_auth.py::TestAuthentication::test_login_page_loads PASSED
tests_selenium/test_auth.py::TestAuthentication::test_successful_login PASSED
tests_selenium/test_auth.py::TestAuthentication::test_failed_login_invalid_credentials PASSED
tests_selenium/test_auth.py::TestAuthentication::test_logout PASSED
tests_selenium/test_auth.py::TestAuthentication::test_protected_route_redirect PASSED
...

======================== 25 passed in 45.23s ========================
```

## 🎯 Próximos Pasos

1. **Revisar README.md** para documentación completa
2. **Agregar más tests** según necesidades
3. **Integrar en CI/CD** (ver README.md)
4. **Configurar reportes** automáticos

## 💡 Tips

- Usa `-k` para filtrar tests por nombre:
  ```bash
  pytest tests_selenium/ -k "login" -v
  ```

- Usa `-x` para detener en el primer fallo:
  ```bash
  pytest tests_selenium/ -x
  ```

- Usa `--lf` para ejecutar solo los tests que fallaron:
  ```bash
  pytest tests_selenium/ --lf
  ```

- Usa `--pdb` para debugging interactivo:
  ```bash
  pytest tests_selenium/ --pdb
  ```

## 📞 Soporte

- Revisar logs de Selenium
- Ejecutar en modo visible
- Verificar manualmente la funcionalidad
- Consultar README.md completo
