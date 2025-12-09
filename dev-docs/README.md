# 📚 Documentación de Desarrollo

Esta carpeta contiene documentación interna, scripts de utilidad y guías de desarrollo que no son parte de la documentación principal del proyecto.

## 📁 Estructura

### `/scripts`
Scripts de Python, Bash y Batch para tareas de desarrollo y mantenimiento:
- Scripts de seeding de datos
- Scripts de verificación
- Scripts de limpieza
- Scripts de deployment manual

### `/deployment`
Documentación relacionada con el proceso de deployment:
- Guías de deployment a Railway
- Instrucciones de carga de datos en producción
- Configuración de permisos
- Troubleshooting de deployment

### `/testing`
Documentación de testing y verificación:
- Resultados de tests
- Checklists de validación
- Scripts de verificación
- Reportes de testing

### `/fixes`
Registro de correcciones y soluciones:
- Documentación de bugs corregidos
- Soluciones implementadas
- Debug logs
- Correcciones de producción

### `/guides`
Guías de desarrollo y uso:
- Instrucciones paso a paso
- Guías de configuración
- Manuales de usuario
- Quick start guides

### Archivos en la raíz
Resúmenes, checkpoints y documentación general de desarrollo.

## 🔒 Nota Importante

Esta documentación es para uso interno del equipo de desarrollo. No debe ser incluida en la documentación pública del proyecto.

## 📝 Convenciones

- Los archivos con prefijo `RESUMEN_` contienen resúmenes de implementaciones
- Los archivos con prefijo `INSTRUCCIONES_` son guías paso a paso
- Los archivos con prefijo `VERIFICAR_` son checklists de validación
- Los archivos `.py` son scripts ejecutables
- Los archivos `.sh` y `.bat` son scripts de shell

## 🗑️ Limpieza

Si necesitas limpiar archivos antiguos o innecesarios:

```bash
# Revisar archivos por fecha
ls -lt scripts/

# Eliminar archivos específicos
rm scripts/archivo_antiguo.py

# Archivar documentación antigua
mkdir archive
mv RESUMEN_ANTIGUO.md archive/
```

## 📌 Mantenimiento

- Revisar y actualizar esta documentación regularmente
- Eliminar scripts obsoletos
- Archivar documentación de versiones antiguas
- Mantener solo lo relevante para el desarrollo actual
