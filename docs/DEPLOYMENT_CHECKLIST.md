# Checklist de Despliegue - Sistema CMMS

Este documento contiene la lista de verificación completa antes de desplegar el sistema a producción.

## ✅ Pre-Despliegue

### Seguridad
- [ ] Cambiar `SECRET_KEY` en producción
- [ ] Configurar `DEBUG=False`
- [ ] Configurar `ALLOWED_HOSTS` correctamente
- [ ] Revisar permisos de archivos y directorios
- [ ] Configurar HTTPS/SSL
- [ ] Habilitar HSTS (HTTP Strict Transport Security)
- [ ] Configurar CSP (Content Security Policy)
- [ ] Revisar configuración de CORS
- [ ] Implementar rate limiting en producción
- [ ] Configurar firewall

### Base de Datos
- [ ] Migrar de SQLite a PostgreSQL
- [ ] Ejecutar todas las migraciones
- [ ] Crear backup de base de datos
- [ ] Configurar backups automáticos
- [ ] Optimizar índices de base de datos
- [ ] Configurar connection pooling
- [ ] Verificar permisos de usuario de BD

### Archivos Estáticos y Media
- [ ] Ejecutar `collectstatic`
- [ ] Configurar CDN para archivos estáticos
- [ ] Configurar almacenamiento de media files (S3, etc.)
- [ ] Optimizar imágenes
- [ ] Configurar compresión Gzip

### Caché
- [ ] Configurar Redis para caché
- [ ] Configurar Redis para Celery
- [ ] Verificar configuración de caché
- [ ] Probar invalidación de caché

### Celery
- [ ] Configurar Celery workers
- [ ] Configurar Celery beat
- [ ] Configurar supervisord o systemd
- [ ] Verificar tareas programadas
- [ ] Configurar monitoreo de Celery

### Frontend
- [ ] Ejecutar build de producción
- [ ] Verificar bundle size
- [ ] Optimizar imágenes
- [ ] Configurar service worker (opcional)
- [ ] Verificar compatibilidad de navegadores
- [ ] Probar en dispositivos móviles

### Logging y Monitoreo
- [ ] Configurar logging en producción
- [ ] Configurar rotación de logs
- [ ] Configurar alertas de errores (Sentry, etc.)
- [ ] Configurar monitoreo de performance (New Relic, etc.)
- [ ] Configurar uptime monitoring
- [ ] Configurar alertas de disco lleno

### Testing
- [ ] Ejecutar todos los tests unitarios
- [ ] Ejecutar tests de integración
- [ ] Ejecutar tests de seguridad
- [ ] Realizar pruebas de carga
- [ ] Verificar todos los endpoints de API
- [ ] Probar flujos completos de usuario

### Documentación
- [ ] Actualizar README
- [ ] Documentar variables de entorno
- [ ] Documentar proceso de despliegue
- [ ] Crear guía de usuario
- [ ] Documentar procedimientos de backup
- [ ] Documentar procedimientos de rollback

## ✅ Despliegue

### Servidor
- [ ] Configurar servidor (Ubuntu/CentOS)
- [ ] Instalar dependencias del sistema
- [ ] Configurar Nginx/Apache
- [ ] Configurar Gunicorn/uWSGI
- [ ] Configurar SSL/TLS
- [ ] Configurar firewall (UFW/iptables)

### Base de Datos
- [ ] Crear base de datos de producción
- [ ] Crear usuario de base de datos
- [ ] Ejecutar migraciones
- [ ] Cargar datos iniciales (roles, etc.)
- [ ] Crear primer usuario admin

### Aplicación
- [ ] Clonar repositorio
- [ ] Instalar dependencias Python
- [ ] Configurar variables de entorno
- [ ] Ejecutar collectstatic
- [ ] Configurar permisos de archivos
- [ ] Iniciar servicios (Gunicorn, Celery)

### Verificación
- [ ] Verificar que el sitio carga correctamente
- [ ] Probar login
- [ ] Verificar API endpoints
- [ ] Probar creación de datos
- [ ] Verificar envío de notificaciones
- [ ] Verificar tareas de Celery
- [ ] Verificar generación de reportes
- [ ] Verificar generación de PDFs

## ✅ Post-Despliegue

### Monitoreo
- [ ] Verificar logs por errores
- [ ] Monitorear uso de CPU/RAM
- [ ] Monitorear uso de disco
- [ ] Verificar tiempos de respuesta
- [ ] Monitorear tasa de errores

### Backup
- [ ] Verificar que backups se ejecutan
- [ ] Probar restauración de backup
- [ ] Documentar procedimiento de backup

### Documentación
- [ ] Actualizar documentación con URLs de producción
- [ ] Documentar credenciales (en lugar seguro)
- [ ] Crear runbook de operaciones
- [ ] Documentar procedimientos de emergencia

### Capacitación
- [ ] Capacitar a usuarios finales
- [ ] Capacitar a administradores
- [ ] Crear videos tutoriales (opcional)
- [ ] Preparar FAQ

## 🚨 Rollback Plan

En caso de problemas críticos:

1. **Detener servicios nuevos**
   ```bash
   sudo systemctl stop gunicorn
   sudo systemctl stop celery
   ```

2. **Restaurar versión anterior**
   ```bash
   git checkout <previous-version>
   pip install -r requirements.txt
   ```

3. **Restaurar base de datos** (si es necesario)
   ```bash
   psql -U user -d database < backup.sql
   ```

4. **Reiniciar servicios**
   ```bash
   sudo systemctl start gunicorn
   sudo systemctl start celery
   ```

## 📊 Métricas de Éxito

Después del despliegue, monitorear:

- **Uptime**: > 99.9%
- **Tiempo de respuesta API**: < 200ms (p95)
- **Tasa de errores**: < 0.1%
- **Uso de CPU**: < 70%
- **Uso de RAM**: < 80%
- **Uso de disco**: < 80%

## 📞 Contactos de Emergencia

- **DevOps**: [contacto]
- **Backend Lead**: [contacto]
- **Frontend Lead**: [contacto]
- **DBA**: [contacto]

## 📝 Notas Adicionales

- Realizar despliegue en horario de bajo tráfico
- Tener plan de comunicación con usuarios
- Preparar mensaje de mantenimiento
- Tener equipo disponible durante despliegue
- Documentar cualquier problema encontrado

---

**Última actualización:** [Fecha]
**Versión:** 1.0.0
