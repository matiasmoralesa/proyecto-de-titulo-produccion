# 🤝 Guía de Contribución

Gracias por tu interés en contribuir al proyecto CMMS. Esta guía te ayudará a entender cómo puedes colaborar efectivamente.

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [¿Cómo Puedo Contribuir?](#cómo-puedo-contribuir)
- [Proceso de Desarrollo](#proceso-de-desarrollo)
- [Estándares de Código](#estándares-de-código)
- [Commits](#commits)
- [Pull Requests](#pull-requests)
- [Reportar Bugs](#reportar-bugs)
- [Sugerir Mejoras](#sugerir-mejoras)

## 📜 Código de Conducta

Este proyecto se adhiere a un código de conducta profesional. Al participar, se espera que mantengas un ambiente respetuoso y colaborativo.

## 🚀 ¿Cómo Puedo Contribuir?

### Reportar Bugs

Si encuentras un bug:

1. Verifica que no haya sido reportado previamente en [Issues](https://github.com/tu-usuario/proyecto-de-titulo-produccion/issues)
2. Crea un nuevo issue usando la plantilla de bug report
3. Incluye:
   - Descripción clara del problema
   - Pasos para reproducir
   - Comportamiento esperado vs actual
   - Screenshots si aplica
   - Información del entorno (OS, navegador, versión)

### Sugerir Mejoras

Para sugerir nuevas funcionalidades:

1. Verifica que no exista una sugerencia similar
2. Crea un issue con la etiqueta `enhancement`
3. Describe claramente:
   - El problema que resuelve
   - La solución propuesta
   - Alternativas consideradas
   - Impacto en el sistema actual

### Contribuir con Código

1. Fork el repositorio
2. Crea una rama desde `main`
3. Realiza tus cambios
4. Asegúrate de que los tests pasen
5. Crea un Pull Request

## 🔄 Proceso de Desarrollo

### 1. Configurar el Entorno

```bash
# Clonar tu fork
git clone https://github.com/tu-usuario/proyecto-de-titulo-produccion.git
cd proyecto-de-titulo-produccion

# Agregar upstream
git remote add upstream https://github.com/original-usuario/proyecto-de-titulo-produccion.git

# Instalar dependencias
cd backend && pip install -r requirements.txt
cd ../frontend && npm install
```

### 2. Crear una Rama

```bash
# Actualizar main
git checkout main
git pull upstream main

# Crear rama descriptiva
git checkout -b feat/nueva-funcionalidad
# o
git checkout -b fix/corregir-bug
```

### 3. Desarrollar

- Escribe código limpio y documentado
- Agrega tests para nuevas funcionalidades
- Actualiza la documentación si es necesario
- Sigue los estándares de código del proyecto

### 4. Testing

```bash
# Backend
cd backend
pytest
pytest --cov=apps

# Frontend
cd frontend
npm run test
npm run lint
```

### 5. Commit

```bash
git add .
git commit -m "feat: agregar nueva funcionalidad"
```

### 6. Push y Pull Request

```bash
git push origin feat/nueva-funcionalidad
```

Luego crea un Pull Request en GitHub.

## 📝 Estándares de Código

### Backend (Python/Django)

#### Estilo

- Seguir [PEP 8](https://pep8.org/)
- Usar [Black](https://black.readthedocs.io/) para formateo
- Usar [isort](https://pycqa.github.io/isort/) para imports
- Máximo 88 caracteres por línea (Black default)

```bash
# Formatear código
black .
isort .

# Verificar estilo
flake8
```

#### Convenciones

```python
# Nombres de clases: PascalCase
class WorkOrderService:
    pass

# Nombres de funciones y variables: snake_case
def create_work_order(asset_id):
    work_order_number = generate_number()
    return work_order_number

# Constantes: UPPER_SNAKE_CASE
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

# Docstrings: Google Style
def calculate_mtbf(asset_id, start_date, end_date):
    """
    Calculate Mean Time Between Failures for an asset.
    
    Args:
        asset_id (int): ID of the asset
        start_date (datetime): Start date for calculation
        end_date (datetime): End date for calculation
    
    Returns:
        float: MTBF value in hours
    
    Raises:
        ValueError: If date range is invalid
    """
    pass
```

#### Tests

```python
# Nombres de tests: test_<lo_que_prueba>
def test_create_work_order_with_valid_data():
    pass

def test_create_work_order_fails_with_invalid_asset():
    pass

# Usar fixtures de pytest
@pytest.fixture
def sample_asset():
    return Asset.objects.create(name="Test Asset")

# Usar marcadores
@pytest.mark.unit
def test_unit_function():
    pass

@pytest.mark.integration
def test_api_endpoint():
    pass
```

### Frontend (TypeScript/React)

#### Estilo

- Seguir [Airbnb Style Guide](https://github.com/airbnb/javascript)
- Usar [Prettier](https://prettier.io/) para formateo
- Usar [ESLint](https://eslint.org/) para linting

```bash
# Formatear código
npm run format

# Verificar estilo
npm run lint
```

#### Convenciones

```typescript
// Nombres de componentes: PascalCase
const WorkOrderCard: React.FC<Props> = ({ workOrder }) => {
  return <div>{workOrder.title}</div>;
};

// Nombres de funciones y variables: camelCase
const handleSubmit = () => {
  const workOrderData = getFormData();
  submitWorkOrder(workOrderData);
};

// Constantes: UPPER_SNAKE_CASE
const MAX_FILE_SIZE = 5 * 1024 * 1024;
const API_TIMEOUT = 30000;

// Interfaces: PascalCase con prefijo I (opcional)
interface WorkOrder {
  id: number;
  title: string;
  status: WorkOrderStatus;
}

// Types: PascalCase
type WorkOrderStatus = 'PENDING' | 'IN_PROGRESS' | 'COMPLETED';

// Enums: PascalCase
enum Priority {
  LOW = 'LOW',
  MEDIUM = 'MEDIUM',
  HIGH = 'HIGH',
  CRITICAL = 'CRITICAL',
}
```

#### Componentes

```typescript
// Usar functional components con hooks
import React, { useState, useEffect } from 'react';

interface Props {
  workOrderId: number;
  onUpdate?: (workOrder: WorkOrder) => void;
}

export const WorkOrderDetail: React.FC<Props> = ({ workOrderId, onUpdate }) => {
  const [workOrder, setWorkOrder] = useState<WorkOrder | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchWorkOrder();
  }, [workOrderId]);

  const fetchWorkOrder = async () => {
    try {
      const data = await workOrderService.getById(workOrderId);
      setWorkOrder(data);
    } catch (error) {
      console.error('Error fetching work order:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <LoadingSpinner />;
  if (!workOrder) return <NotFound />;

  return (
    <div className="work-order-detail">
      <h1>{workOrder.title}</h1>
      {/* ... */}
    </div>
  );
};
```

## 💬 Commits

### Conventional Commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/) para mensajes de commit estructurados:

```
<tipo>[alcance opcional]: <descripción>

[cuerpo opcional]

[footer opcional]
```

#### Tipos

- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Cambios en documentación
- `style`: Cambios de formato (no afectan el código)
- `refactor`: Refactorización de código
- `perf`: Mejoras de rendimiento
- `test`: Agregar o modificar tests
- `chore`: Tareas de mantenimiento
- `ci`: Cambios en CI/CD
- `build`: Cambios en el sistema de build

#### Ejemplos

```bash
# Feature
git commit -m "feat: agregar filtro de búsqueda en órdenes de trabajo"
git commit -m "feat(inventory): implementar alertas de stock bajo"

# Fix
git commit -m "fix: corregir cálculo de MTBF en reportes"
git commit -m "fix(auth): resolver problema de expiración de token"

# Docs
git commit -m "docs: actualizar README con instrucciones de deployment"

# Refactor
git commit -m "refactor: simplificar lógica de asignación de órdenes"

# Breaking change
git commit -m "feat!: cambiar estructura de API de activos

BREAKING CHANGE: El endpoint /api/v1/assets/ ahora retorna
un objeto paginado en lugar de un array directo."
```

## 🔀 Pull Requests

### Checklist

Antes de crear un PR, verifica:

- [ ] El código sigue los estándares del proyecto
- [ ] Todos los tests pasan
- [ ] Se agregaron tests para nuevas funcionalidades
- [ ] La documentación está actualizada
- [ ] Los commits siguen Conventional Commits
- [ ] No hay conflictos con `main`
- [ ] El PR tiene una descripción clara

### Plantilla de PR

```markdown
## Descripción
Breve descripción de los cambios realizados.

## Tipo de Cambio
- [ ] Bug fix
- [ ] Nueva funcionalidad
- [ ] Breaking change
- [ ] Documentación

## ¿Cómo se ha probado?
Describe las pruebas realizadas.

## Checklist
- [ ] Tests pasan localmente
- [ ] Código sigue los estándares
- [ ] Documentación actualizada
- [ ] Sin conflictos con main

## Screenshots (si aplica)
Agrega capturas de pantalla si hay cambios visuales.

## Issues Relacionados
Closes #123
```

### Proceso de Revisión

1. El PR será revisado por al menos un maintainer
2. Se pueden solicitar cambios
3. Una vez aprobado, será merged a `main`
4. El deployment automático se activará

## 🐛 Reportar Bugs

### Plantilla de Bug Report

```markdown
## Descripción del Bug
Descripción clara y concisa del bug.

## Pasos para Reproducir
1. Ir a '...'
2. Hacer click en '...'
3. Scroll hasta '...'
4. Ver error

## Comportamiento Esperado
Descripción de lo que debería suceder.

## Comportamiento Actual
Descripción de lo que sucede actualmente.

## Screenshots
Si aplica, agrega screenshots.

## Entorno
- OS: [e.g. Windows 11]
- Navegador: [e.g. Chrome 120]
- Versión: [e.g. 1.0.0]

## Información Adicional
Cualquier otro contexto relevante.
```

## 💡 Sugerir Mejoras

### Plantilla de Feature Request

```markdown
## ¿El feature está relacionado con un problema?
Descripción clara del problema. Ej: "Siempre me frustra cuando [...]"

## Solución Propuesta
Descripción clara de lo que quieres que suceda.

## Alternativas Consideradas
Descripción de soluciones alternativas que consideraste.

## Contexto Adicional
Cualquier otro contexto, screenshots, etc.
```

## 📞 Contacto

Si tienes preguntas sobre cómo contribuir:

- 📧 Email: dev@ejemplo.com
- 💬 Discord: [Link al servidor]
- 📝 Discussions: [GitHub Discussions](https://github.com/tu-usuario/proyecto-de-titulo-produccion/discussions)

## 🙏 Agradecimientos

Gracias por contribuir al proyecto CMMS. Tu ayuda es muy apreciada.

---

**Última actualización**: Diciembre 2025
