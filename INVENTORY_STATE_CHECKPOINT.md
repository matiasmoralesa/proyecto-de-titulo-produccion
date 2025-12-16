# 📦 Inventory System State Checkpoint - Pre OT Integration

**Fecha:** 16 de Diciembre, 2025  
**Estado:** Sistema de inventario independiente antes de integración con OTs  
**Propósito:** Documentar estado actual antes de sincronización con órdenes de trabajo  

## 📊 Estado Actual del Inventario

### **Modelos Existentes:**

#### **1. SparePart (Repuestos)**
```python
# Información Básica
- part_number: str (único)          # Número de parte
- name: str                         # Nombre del repuesto
- description: text                 # Descripción detallada
- category: str                     # Categoría del repuesto
- manufacturer: str                 # Fabricante

# Stock
- quantity: int                     # Cantidad actual en stock
- min_quantity: int                 # Cantidad mínima (punto de reorden)
- unit_of_measure: str             # Unidad de medida
- unit_cost: decimal               # Costo unitario

# Ubicación y Estado
- storage_location: str            # Ubicación física
- is_active: bool                  # Estado activo/inactivo
- created_at, updated_at           # Timestamps
- created_by: User                 # Usuario creador
```

#### **2. StockMovement (Movimientos de Stock)**
```python
# Tipos de Movimiento
MOVEMENT_TYPES = [
    'IN',           # Entrada
    'OUT',          # Salida  
    'ADJUSTMENT',   # Ajuste
    'RETURN',       # Devolución
    'TRANSFER',     # Transferencia
    'INITIAL',      # Inventario inicial
]

# Campos
- spare_part: FK                   # Repuesto relacionado
- movement_type: choice            # Tipo de movimiento
- quantity: int                    # Cantidad movida
- quantity_before: int             # Stock antes del movimiento
- quantity_after: int              # Stock después del movimiento
- unit_cost: decimal              # Costo unitario en el momento
- reference_type: str             # Tipo de referencia (opcional)
- reference_id: str               # ID de referencia (opcional)
- notes: text                     # Notas adicionales
- user: FK                        # Usuario que realizó el movimiento
- created_at: datetime            # Fecha del movimiento
```

### **Funcionalidades Actuales:**

#### **Gestión de Stock:**
- ✅ Control de inventario básico
- ✅ Seguimiento de movimientos (audit trail)
- ✅ Alertas de stock bajo
- ✅ Cálculo de valor total de inventario
- ✅ Ajustes manuales de stock

#### **Métodos del Modelo SparePart:**
```python
- is_low_stock()                   # Verifica si está bajo mínimo
- stock_status()                   # Estado del stock (texto)
- total_value()                    # Valor total del stock
- adjust_stock()                   # Ajusta stock y crea movimiento
```

#### **API Endpoints Existentes:**
```python
# Repuestos
GET    /api/v1/inventory/spare-parts/     # Listar repuestos
POST   /api/v1/inventory/spare-parts/     # Crear repuesto
GET    /api/v1/inventory/spare-parts/{id}/ # Detalle repuesto
PUT    /api/v1/inventory/spare-parts/{id}/ # Actualizar repuesto
DELETE /api/v1/inventory/spare-parts/{id}/ # Eliminar repuesto

# Movimientos
GET    /api/v1/inventory/movements/       # Listar movimientos
POST   /api/v1/inventory/movements/       # Crear movimiento
```

## 🔗 Estado Actual de Work Orders

### **Modelo WorkOrder (Sin Integración con Inventario):**
```python
# Campos actuales (SIN repuestos)
- asset: FK                        # Activo relacionado
- title: str                       # Título de la OT
- description: text                # Descripción del trabajo
- priority: choice                 # Prioridad (LOW/MEDIUM/HIGH/CRITICAL)
- status: choice                   # Estado (PENDING/IN_PROGRESS/COMPLETED/CANCELLED)
- assigned_to: FK                  # Operador asignado
- estimated_hours: decimal         # Horas estimadas
- actual_hours: decimal           # Horas reales (al completar)
- scheduled_date: date            # Fecha programada
- completed_date: datetime        # Fecha de completado
- created_by: FK                  # Usuario creador
- created_at, updated_at          # Timestamps
```

### **Limitaciones Actuales:**
- ❌ No hay relación entre OTs y repuestos
- ❌ No se reservan repuestos al crear/asignar OTs
- ❌ No se descuenta stock al completar OTs
- ❌ No se calculan costos de materiales
- ❌ No hay control de disponibilidad de repuestos
- ❌ No hay trazabilidad de uso de repuestos por activo

## 🎯 Plan de Integración OTs-Inventario

### **Nuevos Modelos a Crear:**

#### **1. WorkOrderPart (Relación OT-Repuesto)**
```python
# Campos propuestos
- work_order: FK                   # Orden de trabajo
- spare_part: FK                   # Repuesto necesario
- quantity_required: int           # Cantidad requerida
- quantity_reserved: int           # Cantidad reservada
- quantity_used: int              # Cantidad realmente utilizada
- unit_cost_at_time: decimal      # Costo unitario al momento
- status: choice                   # REQUIRED/RESERVED/USED/CANCELLED
- notes: text                     # Notas sobre el uso
- created_at, updated_at          # Timestamps
```

#### **2. PartReservation (Reservas de Repuestos)**
```python
# Campos propuestos
- spare_part: FK                   # Repuesto reservado
- work_order: FK                   # OT que reserva
- quantity: int                    # Cantidad reservada
- reserved_by: FK                  # Usuario que reservó
- reserved_at: datetime           # Fecha de reserva
- expires_at: datetime            # Fecha de expiración
- status: choice                   # ACTIVE/EXPIRED/CONSUMED/CANCELLED
```

#### **3. MaintenanceCost (Costos de Mantenimiento)**
```python
# Campos propuestos
- work_order: FK                   # Orden de trabajo
- labor_cost: decimal             # Costo de mano de obra
- parts_cost: decimal             # Costo de repuestos
- other_costs: decimal            # Otros costos
- total_cost: decimal             # Costo total
- cost_breakdown: JSON            # Desglose detallado
- calculated_at: datetime         # Fecha de cálculo
```

### **Flujo de Integración Propuesto:**

#### **1. Creación de OT:**
```python
# Al crear OT
1. Definir repuestos necesarios
2. Verificar disponibilidad en stock
3. Mostrar alertas si hay stock insuficiente
4. Permitir crear OT con o sin stock completo
```

#### **2. Asignación de OT:**
```python
# Al asignar OT a operador
1. Reservar repuestos automáticamente
2. Actualizar stock disponible (quantity - reserved)
3. Crear registros de reserva
4. Notificar si no hay stock suficiente
```

#### **3. Ejecución de OT:**
```python
# Durante la ejecución
1. Permitir ajustar cantidades requeridas
2. Registrar cantidades realmente utilizadas
3. Manejar devoluciones de repuestos no usados
```

#### **4. Completado de OT:**
```python
# Al completar OT
1. Descontar del stock las cantidades utilizadas
2. Liberar reservas no utilizadas
3. Crear movimientos de stock (OUT)
4. Calcular costos totales de mantenimiento
5. Actualizar métricas de consumo por activo
```

### **Nuevos Endpoints API:**
```python
# Gestión de repuestos en OTs
POST   /api/v1/work-orders/{id}/parts/           # Agregar repuesto a OT
GET    /api/v1/work-orders/{id}/parts/           # Listar repuestos de OT
PUT    /api/v1/work-orders/{id}/parts/{part_id}/ # Actualizar cantidad
DELETE /api/v1/work-orders/{id}/parts/{part_id}/ # Remover repuesto

# Reservas
POST   /api/v1/work-orders/{id}/reserve-parts/   # Reservar repuestos
POST   /api/v1/work-orders/{id}/release-parts/   # Liberar reservas

# Costos
GET    /api/v1/work-orders/{id}/costs/           # Obtener costos
POST   /api/v1/work-orders/{id}/calculate-costs/ # Calcular costos

# Reportes
GET    /api/v1/inventory/consumption-by-asset/   # Consumo por activo
GET    /api/v1/inventory/cost-analysis/          # Análisis de costos
```

## 📊 Métricas Actuales (Pre-Integración)

### **Inventario:**
- Total de repuestos únicos: Por definir
- Valor total del inventario: Por definir
- Repuestos con stock bajo: Por definir
- Movimientos promedio por mes: Por definir

### **Work Orders:**
- OTs completadas por mes: Por definir
- Tiempo promedio de completado: Por definir
- Costo de mano de obra: Calculado por horas
- Costo de materiales: ❌ No disponible

## 🔒 Preservación del Estado Actual

### **No Modificar Durante Integración:**
- ✅ Modelos `SparePart` y `StockMovement` existentes
- ✅ API endpoints actuales de inventario
- ✅ Funcionalidad básica de gestión de stock
- ✅ Audit trail de movimientos

### **Modificaciones Permitidas:**
- ✅ Agregar nuevos modelos de relación
- ✅ Crear nuevos endpoints para integración
- ✅ Agregar campos calculados (no modificar existentes)
- ✅ Implementar servicios de sincronización

---

**🔒 Este checkpoint documenta el estado independiente actual de inventario y OTs antes de su integración.**

**Próximo paso:** Implementar modelos de relación y servicios de sincronización manteniendo la funcionalidad existente intacta.