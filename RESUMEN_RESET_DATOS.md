# 📊 Resumen: Sistema de Reset y Población de Datos

## ✅ Archivos Creados

### 1. Script Principal
**Archivo:** `backend/scripts/reset_and_populate_data.py`

Script completo en Python que:
- ✅ Elimina todos los datos de producción
- ✅ Mantiene las plantillas de checklist intactas
- ✅ Crea datos de muestra realistas para todas las secciones
- ✅ Solicita confirmación antes de proceder
- ✅ Muestra resumen detallado al finalizar

### 2. Documentación
**Archivo:** `INSTRUCCIONES_RESET_DATOS.md`

Guía completa con:
- Advertencias y requisitos previos
- Pasos detallados de ejecución
- Lista completa de datos que se crearán
- Credenciales de acceso
- Solución de problemas

### 3. Script de Ejecución Rápida
**Archivo:** `reset_datos.bat`

Script batch para Windows que:
- Activa automáticamente el entorno virtual
- Ejecuta el script de Python
- Maneja errores apropiadamente

## 📦 Datos de Muestra Incluidos

### 👥 Usuarios (6 total)
```
Admin:        admin / admin123
Supervisores: supervisor1, supervisor2 / super123
Operadores:   operador1, operador2, operador3 / oper123
```

### 📍 Ubicaciones (4)
- Planta Central
- Almacén Norte
- Taller de Mantenimiento
- Base Operativa Sur

### 🚛 Activos (7)
- 2 Camiones Supersucker (SS-001, SS-002)
- 2 Camionetas MDO (MDO-001, MDO-002)
- 1 Retroexcavadora (RE-001)
- 1 Cargador Frontal (CF-001)
- 1 Minicargador (MC-001)

Estados variados: Operando, En Mantenimiento, Detenida

### 📋 Órdenes de Trabajo (10)
**Completadas (4):**
- Mantenimiento Preventivo 5000 km
- Cambio de Neumáticos
- Cambio de Batería
- Inspección Pre-Operacional

**En Progreso (3):**
- Reparación Sistema Hidráulico
- Reparación Sistema de Frenos
- Reparación Urgente Motor

**Pendientes (3):**
- Inspección Mensual
- Mantenimiento Preventivo 10000 km
- Revisión Sistema Eléctrico

### 🔄 Planes de Mantenimiento (7)
- 2 Planes mensuales (Camiones Supersucker)
- 1 Plan semanal (Camioneta)
- 1 Plan trimestral (Retroexcavadora)
- 1 Plan por horas (Cargador Frontal - cada 250 horas)
- 1 Plan diario (Minicargador)
- 1 Plan anual (Camioneta)

### 🔧 Repuestos (10)
**Filtros:**
- Filtro de Aceite (25 unidades)
- Filtro de Aire (30 unidades)
- Filtro de Combustible (20 unidades)

**Lubricantes:**
- Aceite Motor 15W-40 (100 litros)
- Aceite Hidráulico ISO 68 (80 litros)

**Sistema de Frenos:**
- Pastillas Delanteras (12 juegos)
- Pastillas Traseras (10 juegos)

**Otros:**
- Batería 12V 100Ah (8 unidades)
- Neumático 295/80R22.5 (16 unidades)
- Manguera Hidráulica 1/2" (5 metros)

### ⚙️ Configuración
**Categorías de Activos (4):**
- Vehículos Pesados (VH)
- Vehículos Livianos (VL)
- Maquinaria Pesada (MP)
- Equipos Especializados (EE)

**Prioridades (4):**
- Urgente (Nivel 1) - Rojo
- Alta (Nivel 2) - Naranja
- Media (Nivel 3) - Amarillo
- Baja (Nivel 4) - Verde

**Tipos de Orden de Trabajo (5):**
- Mantenimiento Preventivo (MP)
- Mantenimiento Correctivo (MC)
- Reparación de Emergencia (RE) - Requiere aprobación
- Inspección (INS)
- Modificación (MOD) - Requiere aprobación

**Parámetros del Sistema (3):**
- Días de anticipación para notificaciones: 7
- Umbral de stock bajo: 10
- RBAC habilitado: true

## 🚀 Cómo Usar

### Opción 1: Script Batch (Recomendado para Windows)
```bash
reset_datos.bat
```

### Opción 2: Comando Directo
```bash
# Activar entorno virtual
venv\Scripts\activate

# Ejecutar script
python backend\scripts\reset_and_populate_data.py
```

## ⚠️ Importante

1. **Confirmación Requerida:** El script pedirá que escribas 'SI' para confirmar
2. **Backup:** Aunque es para desarrollo, considera hacer backup si tienes datos importantes
3. **Superusuarios:** Los superusuarios existentes NO se eliminan
4. **Plantillas:** Las plantillas de checklist se mantienen intactas
5. **Tiempo:** El proceso toma menos de 1 minuto

## 🎯 Casos de Uso

Este script es ideal para:
- ✅ Resetear el ambiente de desarrollo
- ✅ Crear datos de prueba consistentes
- ✅ Demostrar el sistema a clientes
- ✅ Entrenar nuevos usuarios
- ✅ Probar funcionalidades con datos realistas
- ✅ Iniciar un ambiente limpio después de pruebas

## 📈 Beneficios

1. **Datos Realistas:** Todos los datos son coherentes y representan escenarios reales
2. **Relaciones Completas:** Todos los objetos están correctamente relacionados
3. **Variedad:** Incluye diferentes estados, prioridades y tipos
4. **Roles Completos:** Datos para probar todos los roles (Admin, Supervisor, Operador)
5. **Reproducible:** Siempre genera el mismo conjunto de datos
6. **Rápido:** Ejecución en menos de 1 minuto

## 🔍 Verificación Post-Ejecución

Después de ejecutar, verifica:
1. ✅ Login con diferentes usuarios
2. ✅ Dashboard muestra datos correctos
3. ✅ Órdenes de trabajo visibles según rol
4. ✅ Activos asignados correctamente
5. ✅ Planes de mantenimiento activos
6. ✅ Inventario con stock inicial

## 📞 Soporte

Si encuentras problemas:
1. Revisa `INSTRUCCIONES_RESET_DATOS.md` para solución de problemas
2. Verifica que el entorno virtual esté activado
3. Confirma que tienes permisos en la base de datos
4. Revisa los logs de error si el script falla

---

**Creado:** Diciembre 2024  
**Versión:** 1.0  
**Compatibilidad:** Django 4.x, Python 3.8+
