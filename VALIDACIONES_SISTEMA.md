# Validaciones del Sistema de Permisos por Roles

Este documento describe todas las validaciones implementadas en el sistema CMMS para garantizar la integridad de los datos y el cumplimiento de las reglas de negocio.

## 1. Validaciones de Usuarios

### Backend (`backend/apps/authentication/views.py`)

#### Creación de Usuarios
- ✅ **Solo supervisores y administradores pueden crear usuarios**
  - Los operadores no tienen acceso al endpoint de creación
  - Implementado en `UserManagementViewSet.get_permissions()`

- ✅ **Supervisores no pueden crear usuarios administradores**
  - Validación en `UserManagementViewSet.create()`
  - Retorna error 403 si un supervisor intenta crear un admin

#### Eliminación de Usuarios
- ✅ **No se puede desactivar la propia cuenta**
  - Validación en `UserManagementViewSet.destroy()` y `deactivate()`
  - Previene que un usuario se bloquee a sí mismo

### Frontend (`frontend/src/components/users/UserForm.tsx`)

- ✅ **Supervisores no ven la opción de crear administradores**
  - El rol "Administrador" no aparece en el select para supervisores
  - Mensaje informativo explicando la restricción

- ✅ **Validación de formato de email**
  - Regex para validar formato correcto de email

- ✅ **Validación de contraseña**
  - Mínimo 8 caracteres
  - Confirmación de contraseña debe coincidir

## 2. Validaciones de Órdenes de Trabajo

### Backend (`backend/apps/work_orders/serializers.py`)

#### Creación de Órdenes
- ✅ **No se pueden crear órdenes con fecha programada en el pasado**
  - Validación en `WorkOrderCreateSerializer.validate_scheduled_date()`
  - Compara con `timezone.now()`

#### Actualización de Órdenes
- ✅ **No se pueden actualizar fechas a fechas pasadas (excepto órdenes completadas)**
  - Validación en `WorkOrderUpdateSerializer.validate_scheduled_date()`
  - Permite fechas pasadas solo para órdenes con status "Completada"

- ✅ **Validación de transiciones de estado**
  - Implementado en `validate_status()`
  - Usa el método `can_transition_to()` del modelo

### Frontend (`frontend/src/components/workOrders/WorkOrderForm.tsx`)

- ✅ **Validación de fecha programada en el cliente**
  - Verifica que la fecha no sea anterior a la actual
  - Solo valida para órdenes nuevas o no completadas
  - Mensaje de error claro para el usuario

- ✅ **Campos deshabilitados según rol**
  - Operadores no pueden editar: prioridad, activo, asignación, fecha programada
  - Mensajes informativos explicando por qué están deshabilitados

## 3. Validaciones de Activos

### Backend (`backend/apps/assets/serializers.py`)

#### Creación/Actualización de Activos
- ✅ **Fecha de instalación no puede ser futura**
  - Validación en `AssetCreateUpdateSerializer.validate_installation_date()`
  - Compara con `timezone.now().date()`

- ✅ **Número de serie único**
  - Validación en `validate()` del serializer
  - Verifica que no exista otro activo con el mismo número de serie

- ✅ **Placa única (si se proporciona)**
  - Validación en `validate()` del serializer
  - Verifica que no exista otro activo con la misma placa

- ✅ **Normalización de datos**
  - Número de serie se convierte a mayúsculas automáticamente
  - Placa se convierte a mayúsculas automáticamente

### Frontend (`frontend/src/components/assets/AssetForm.tsx`)

- ✅ **Validación de fecha de instalación en el cliente**
  - Verifica que la fecha no sea posterior a hoy
  - Mensaje de error claro para el usuario

- ✅ **Campos deshabilitados según rol**
  - Operadores no pueden editar: estado, ubicación
  - Solo admins pueden editar: tipo de vehículo, número de serie
  - Mensajes informativos explicando las restricciones

## 4. Validaciones de Permisos por Rol

### Operadores
- ❌ No pueden crear usuarios
- ❌ No pueden listar usuarios
- ❌ No pueden modificar prioridad de órdenes
- ❌ No pueden reasignar órdenes
- ❌ No pueden cambiar fechas programadas
- ❌ No pueden cambiar estado de activos
- ❌ No pueden cambiar ubicación de activos
- ❌ No pueden cambiar tipo de vehículo
- ❌ No pueden cambiar número de serie
- ✅ Solo ven sus propias órdenes de trabajo
- ✅ Solo ven activos relacionados con sus órdenes

### Supervisores
- ✅ Pueden crear usuarios (excepto administradores)
- ✅ Pueden ver usuarios de su equipo
- ✅ Pueden modificar todos los campos de órdenes
- ✅ Pueden modificar estado y ubicación de activos
- ❌ No pueden cambiar tipo de vehículo de activos
- ❌ No pueden cambiar número de serie de activos
- ✅ Ven todas las órdenes de su equipo
- ✅ Ven todos los activos
- ✅ Acceso a predicciones ML
- ✅ Acceso a KPIs del equipo

### Administradores
- ✅ Acceso completo a todos los módulos
- ✅ Pueden crear cualquier tipo de usuario
- ✅ Pueden modificar todos los campos
- ✅ Ven todos los datos del sistema
- ✅ Acceso a configuración del sistema
- ✅ Acceso a logs de auditoría

## 5. Validaciones de Números Negativos

### Backend

#### Órdenes de Trabajo
- ✅ **Horas trabajadas (actual_hours) no pueden ser negativas**
  - Validación a nivel de modelo: `MinValueValidator(0.01)`
  - Validación en serializer: `WorkOrderCompleteSerializer.validate_actual_hours()`
  - Rango permitido: 0.01 a 999.99 horas
  - Mensaje de error claro si se intenta ingresar valor negativo o cero

#### Inventario
- ✅ **Cantidades en stock no pueden ser negativas**
  - Validación a nivel de modelo: `MinValueValidator(0)` en `SparePart.quantity`
  - Validación a nivel de modelo: `MinValueValidator(0)` en `SparePart.min_quantity`
  - Validación a nivel de modelo: `MinValueValidator(0)` en `SparePart.unit_cost`

- ✅ **Ajustes de stock tienen límites razonables**
  - Validación en `StockAdjustmentSerializer.validate_quantity_change()`
  - No puede ser cero
  - No puede exceder ±10,000 unidades en una sola operación
  - Previene errores de entrada de datos

#### Mantenimiento
- ✅ **Valores de uso no pueden ser negativos**
  - Validación en `MaintenancePlanCompleteSerializer.validate_usage_value()`
  - Validación en `MaintenancePlanUsageUpdateSerializer.validate_current_usage()`
  - `min_value=0` en los campos IntegerField

### Resumen de Validaciones Numéricas

| Campo | Modelo/Serializer | Validación | Rango Permitido |
|-------|------------------|------------|-----------------|
| actual_hours | WorkOrder | MinValueValidator(0.01) | 0.01 - 999.99 |
| quantity | SparePart | MinValueValidator(0) | 0 - ∞ |
| min_quantity | SparePart | MinValueValidator(0) | 0 - ∞ |
| unit_cost | SparePart | MinValueValidator(0) | 0.00 - ∞ |
| quantity_change | StockAdjustment | Custom validation | -10,000 - +10,000 (≠ 0) |
| usage_value | MaintenancePlan | MinValueValidator(0) | 0 - ∞ |
| current_usage | MaintenancePlan | MinValueValidator(0) | 0 - ∞ |

## 6. Validaciones de Integridad de Datos

### Campos Requeridos
Todos los formularios validan que los campos obligatorios estén completos antes de enviar:

**Órdenes de Trabajo:**
- Título
- Descripción
- Activo
- Usuario asignado
- Fecha programada

**Activos:**
- Nombre
- Modelo
- Número de serie
- Ubicación
- Fecha de instalación

**Usuarios:**
- Nombre de usuario
- Email
- Nombre
- Apellido
- Contraseña (solo para nuevos usuarios)
- Rol

### Validaciones de Formato
- ✅ Emails con formato válido
- ✅ Contraseñas con mínimo 8 caracteres
- ✅ Números de serie en mayúsculas
- ✅ Placas en mayúsculas
- ✅ Fechas en formato correcto

## 7. Mensajes de Error

Todos los errores de validación incluyen:
- ✅ Mensajes claros y descriptivos en español
- ✅ Indicación visual del campo con error (borde rojo)
- ✅ Explicación de por qué un campo está deshabilitado
- ✅ Indicación del rol necesario para realizar una acción

## 8. Validaciones de Seguridad

- ✅ Tokens JWT validados en cada request
- ✅ Permisos verificados en el backend (no solo frontend)
- ✅ Filtrado automático de datos según rol
- ✅ Logs de auditoría para todas las acciones
- ✅ Prevención de auto-desactivación de cuentas
- ✅ Validación de transiciones de estado

## Resumen

El sistema implementa validaciones en **múltiples capas**:

1. **Frontend**: Validación inmediata para mejor UX
2. **Backend**: Validación definitiva para seguridad
3. **Base de datos**: Constraints y validaciones a nivel de modelo

Esto garantiza que:
- Los datos siempre sean consistentes
- Los usuarios solo puedan realizar acciones autorizadas
- Las reglas de negocio se cumplan estrictamente
- La experiencia del usuario sea clara y guiada
