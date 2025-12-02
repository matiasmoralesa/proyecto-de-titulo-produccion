# 🔄 Instrucciones para Resetear y Poblar Datos

Este documento explica cómo limpiar completamente los datos de producción y crear datos de muestra nuevos.

## ⚠️ ADVERTENCIA

**Este proceso eliminará TODOS los datos existentes en la base de datos**, incluyendo:
- Usuarios (excepto superusuarios)
- Activos
- Órdenes de trabajo
- Planes de mantenimiento
- Repuestos e inventario
- Ubicaciones
- Configuraciones
- Logs de auditoría y acceso

**Las plantillas de checklist se mantendrán intactas.**

## 📋 Requisitos Previos

1. Tener el entorno virtual activado
2. Tener acceso a la base de datos
3. Tener permisos de administrador

## 🚀 Pasos para Ejecutar

### Opción 1: Desde la raíz del proyecto

```bash
# Activar entorno virtual (si no está activado)
venv\Scripts\activate

# Ejecutar el script
python backend/scripts/reset_and_populate_data.py
```

### Opción 2: Desde el directorio backend

```bash
# Activar entorno virtual (si no está activado)
..\venv\Scripts\activate

# Ejecutar el script
python scripts/reset_and_populate_data.py
```

## 📊 Datos que se Crearán

### 👥 Usuarios (6 usuarios)

**Administrador:**
- Usuario: `admin`
- Password: `admin123`
- Rol: Administrador

**Supervisores (2):**
- Usuario: `supervisor1` / Password: `super123`
- Usuario: `supervisor2` / Password: `super123`
- Rol: Supervisor

**Operadores (3):**
- Usuario: `operador1` / Password: `oper123`
- Usuario: `operador2` / Password: `oper123`
- Usuario: `operador3` / Password: `oper123`
- Rol: Operador

### 📍 Ubicaciones (4 ubicaciones)
- Planta Central
- Almacén Norte
- Taller de Mantenimiento
- Base Operativa Sur

### 🚛 Activos (7 activos)
- 2 Camiones Supersucker
- 2 Camionetas MDO
- 1 Retroexcavadora
- 1 Cargador Frontal
- 1 Minicargador

### 📋 Órdenes de Trabajo (10 órdenes)
- 4 Completadas
- 3 En Progreso
- 3 Pendientes
- Variedad de prioridades (Urgente, Alta, Media, Baja)

### 🔄 Planes de Mantenimiento (7 planes)
- Planes diarios, semanales, mensuales, trimestrales y anuales
- Planes basados en horas de uso
- Todos activos y asignados

### 🔧 Repuestos (10 repuestos)
- Filtros (aceite, aire, combustible)
- Lubricantes (aceite motor, aceite hidráulico)
- Sistema de frenos (pastillas delanteras y traseras)
- Sistema eléctrico (batería)
- Neumáticos
- Mangueras hidráulicas

### ⚙️ Configuración
- 4 Categorías de activos
- 4 Niveles de prioridad
- 5 Tipos de órdenes de trabajo
- 3 Parámetros del sistema

## ✅ Verificación

Después de ejecutar el script, verás un resumen como este:

```
✅ PROCESO COMPLETADO EXITOSAMENTE
============================================================

📊 RESUMEN DE DATOS CREADOS:
  • Usuarios: 6
  • Ubicaciones: 4
  • Activos: 7
  • Órdenes de Trabajo: 10
  • Planes de Mantenimiento: 7
  • Repuestos: 10
  • Movimientos de Stock: 10
  • Categorías: 4
  • Prioridades: 4
  • Tipos de Orden: 5
```

## 🔐 Acceso al Sistema

Una vez completado el proceso, puedes acceder al sistema con cualquiera de las credenciales listadas arriba.

**Recomendación:** Comienza con el usuario `admin` para verificar que todo se haya creado correctamente.

## 🐛 Solución de Problemas

### Error: "No module named 'apps'"
**Solución:** Asegúrate de ejecutar el script desde la raíz del proyecto o desde el directorio backend.

### Error: "Database is locked"
**Solución:** Cierra todas las conexiones a la base de datos y vuelve a intentar.

### Error: "Permission denied"
**Solución:** Asegúrate de tener permisos de escritura en la base de datos.

## 📝 Notas Importantes

1. **Backup:** Aunque este script está diseñado para entornos de desarrollo, siempre es buena práctica hacer un backup antes de ejecutarlo.

2. **Plantillas de Checklist:** Las plantillas de checklist NO se eliminan con este script.

3. **Superusuarios:** Los superusuarios existentes NO se eliminan.

4. **Confirmación:** El script pedirá confirmación antes de proceder. Debes escribir 'SI' (en mayúsculas) para continuar.

5. **Tiempo de Ejecución:** El script debería completarse en menos de 1 minuto.

## 🔄 Restaurar Datos de Producción

Si necesitas restaurar datos de producción después de ejecutar este script:

1. Restaura el backup de la base de datos
2. O ejecuta las migraciones y carga los datos desde un dump SQL
3. O vuelve a ingresar los datos manualmente

## 📞 Soporte

Si encuentras algún problema al ejecutar este script, contacta al equipo de desarrollo.
