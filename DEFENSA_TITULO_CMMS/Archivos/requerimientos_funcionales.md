# 📋 REQUERIMIENTOS FUNCIONALES - SISTEMA CMMS

## 1. INFORMACIÓN GENERAL

**Proyecto**: Sistema de Gestión de Mantenimiento Computarizado con ML
**Versión**: 1.0
**Fecha**: Diciembre 2025
**Autor**: [Tu Nombre]

## 2. REQUERIMIENTOS FUNCIONALES

### 2.1 Gestión de Activos (RF-01)

#### RF-01.1 Registro de Activos
- **Descripción**: El sistema debe permitir registrar activos con información completa
- **Campos obligatorios**: Nombre, número de serie, tipo de vehículo, ubicación
- **Campos opcionales**: Fabricante, modelo, año, placa, descripción
- **Validaciones**: Número de serie único, formato de placa válido

#### RF-01.2 Consulta de Activos
- **Descripción**: Visualizar lista de activos con filtros y búsqueda
- **Filtros**: Tipo de vehículo, estado, ubicación
- **Búsqueda**: Por nombre, número de serie, placa
- **Ordenamiento**: Por fecha, nombre, estado

#### RF-01.3 Actualización de Activos
- **Descripción**: Modificar información de activos existentes
- **Restricciones**: Solo usuarios autorizados
- **Auditoría**: Registro de cambios con timestamp y usuario

### 2.2 Gestión de Órdenes de Trabajo (RF-02)

#### RF-02.1 Creación de Órdenes
- **Descripción**: Crear órdenes de trabajo manuales y automáticas
- **Tipos**: Correctivo, Preventivo, Predictivo
- **Prioridades**: Baja, Media, Alta, Urgente
- **Asignación**: Manual o automática por ML

#### RF-02.2 Seguimiento de Órdenes
- **Estados**: Pendiente, En Progreso, Completada, Cancelada
- **Transiciones**: Validación de cambios de estado
- **Notificaciones**: Alertas automáticas por cambios

#### RF-02.3 Completar Órdenes
- **Información requerida**: Horas trabajadas, notas de completitud
- **Validaciones**: Campos obligatorios, formato de horas
- **Actualización automática**: Estado del activo, historial

### 2.3 Sistema de Machine Learning (RF-03)

#### RF-03.1 Predicción de Fallos
- **Descripción**: Generar predicciones automáticas de fallos
- **Frecuencia**: Diaria a las 6:00 AM
- **Algoritmo**: Random Forest Classifier
- **Métricas**: Probabilidad, nivel de riesgo, días estimados

#### RF-03.2 Clasificación de Riesgo
- **Niveles**: LOW (<40%), MEDIUM (40-59%), HIGH (60-79%), CRITICAL (≥80%)
- **Acciones automáticas**: Creación de OT para riesgo MEDIUM+
- **Notificaciones**: Alertas a supervisores para riesgo HIGH+

#### RF-03.3 Entrenamiento del Modelo
- **Comando**: `python manage.py train_ml_model`
- **Datos**: Sintéticos y reales combinados
- **Validación**: Cross-validation 5-fold
- **Métricas**: Accuracy, Precision, Recall, F1-Score

### 2.4 Gestión de Usuarios (RF-04)

#### RF-04.1 Autenticación
- **Métodos**: Usuario/contraseña, JWT tokens
- **Seguridad**: Encriptación de contraseñas, expiración de tokens
- **Validaciones**: Formato de email, complejidad de contraseña

#### RF-04.2 Autorización por Roles
- **Roles**: Admin, Supervisor, Operador
- **Permisos**: Basados en rol y contexto
- **Restricciones**: Acceso a datos según asignaciones

#### RF-04.3 Gestión de Perfiles
- **Información**: Datos personales, skills, disponibilidad
- **Actualización**: Auto-actualización y por administradores
- **Historial**: Registro de performance y trabajos

### 2.5 Sistema de Notificaciones (RF-05)

#### RF-05.1 Notificaciones Automáticas
- **Triggers**: Predicciones ML, cambios de estado, vencimientos
- **Canales**: In-app, email, Telegram
- **Personalización**: Preferencias por usuario

#### RF-05.2 Alertas Críticas
- **Condiciones**: Riesgo CRITICAL, equipos fuera de servicio
- **Escalamiento**: Notificación a supervisores
- **Seguimiento**: Confirmación de recepción

### 2.6 Reportes y Dashboard (RF-06)

#### RF-06.1 Dashboard Principal
- **KPIs**: Activos por estado, órdenes pendientes, predicciones
- **Gráficos**: Tiempo real, interactivos
- **Filtros**: Por fecha, ubicación, tipo de activo

#### RF-06.2 Reportes Automáticos
- **Frecuencia**: Diario, semanal, mensual
- **Contenido**: Resumen de actividades, métricas ML
- **Formato**: PDF, Excel, visualización web

## 3. REQUERIMIENTOS NO FUNCIONALES

### 3.1 Performance (RNF-01)
- **Tiempo de respuesta**: <2 segundos para consultas
- **Predicciones ML**: <5 minutos para todos los activos
- **Concurrencia**: Soporte para 50 usuarios simultáneos

### 3.2 Seguridad (RNF-02)
- **Autenticación**: JWT con expiración
- **Autorización**: Control granular por recursos
- **Auditoría**: Log de todas las acciones críticas

### 3.3 Usabilidad (RNF-03)
- **Interfaz**: Responsive, modo oscuro automático
- **Navegación**: Intuitiva, máximo 3 clics para funciones
- **Accesibilidad**: Cumplimiento WCAG 2.1 AA

### 3.4 Disponibilidad (RNF-04)
- **Uptime**: 99.5% disponibilidad
- **Backup**: Automático diario
- **Recuperación**: RTO <4 horas, RPO <1 hora

## 4. CASOS DE USO PRINCIPALES

### CU-01: Predicción Automática de Fallos
1. Sistema ejecuta tarea programada (6:00 AM)
2. Carga modelo ML entrenado
3. Extrae features de todos los activos activos
4. Ejecuta predicciones en lote
5. Clasifica por nivel de riesgo
6. Crea órdenes de trabajo automáticas (riesgo MEDIUM+)
7. Asigna operadores automáticamente
8. Envía notificaciones correspondientes

### CU-02: Gestión de Orden de Trabajo
1. Usuario/Sistema crea orden de trabajo
2. Sistema valida datos y asigna operador
3. Operador recibe notificación
4. Operador actualiza estado a "En Progreso"
5. Operador completa trabajo y registra información
6. Sistema actualiza estado del activo
7. Sistema registra métricas de performance

### CU-03: Consulta de Estadísticas de Activo
1. Usuario selecciona activo desde lista
2. Sistema carga información básica del activo
3. Sistema calcula estadísticas en tiempo real
4. Sistema muestra órdenes de trabajo relacionadas
5. Sistema presenta métricas de disponibilidad
6. Usuario puede generar reporte detallado

## 5. CRITERIOS DE ACEPTACIÓN

### 5.1 Funcionalidad
- ✅ Todas las funciones principales implementadas
- ✅ Validaciones de datos funcionando
- ✅ Flujos de trabajo completos

### 5.2 Machine Learning
- ✅ Modelo con accuracy ≥70%
- ✅ Predicciones automáticas funcionando
- ✅ Integración con órdenes de trabajo

### 5.3 Usabilidad
- ✅ Interfaz responsive en dispositivos móviles
- ✅ Modo oscuro automático
- ✅ Navegación intuitiva

### 5.4 Performance
- ✅ Tiempos de respuesta <2 segundos
- ✅ Carga de dashboard <3 segundos
- ✅ Predicciones ML <5 minutos

---
*Documento de Requerimientos Funcionales v1.0 - Diciembre 2025*