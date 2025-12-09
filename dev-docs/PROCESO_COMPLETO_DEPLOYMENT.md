# 🚀 Proceso Completo: De Local a Producción

## 📊 Estado Actual

### ✅ Completado

1. ✅ **Backend desplegado en Railway**
   - URL: https://tu-proyecto.up.railway.app
   - Base de datos PostgreSQL configurada
   - Migraciones ejecutadas

2. ✅ **Frontend desplegado en Vercel**
   - URL: https://tu-proyecto.vercel.app
   - Conectado al backend de Railway
   - CORS configurado

3. ✅ **Datos exportados de local**
   - 6 archivos JSON con datos maestros
   - Subidos a GitHub
   - Disponibles en Railway

### ⏳ Pendiente

1. ⏳ **Cargar datos en producción**
   - Plantillas de checklist
   - Roles, prioridades, categorías, etc.

2. ⏳ **Crear usuario administrador**

3. ⏳ **Configurar Celery/Flower** (opcional)

## 🎯 Próximos Pasos

### Paso 1: Cargar Datos en Railway (15 minutos)

Sigue la guía: **`RESUMEN_CARGA_DATOS.md`**

**Resumen rápido:**

1. Ve a Railway Dashboard
2. Redeploy tu servicio
3. Abre el Shell
4. Ejecuta los comandos de `loaddata`
5. Verifica con `check_production_data.py`

### Paso 2: Crear Usuario Administrador (2 minutos)

```bash
# En el shell de Railway
python backend/manage.py createsuperuser

# Te pedirá:
# - Username: admin
# - Email: tu@email.com
# - Password: (elige una contraseña segura)
```

### Paso 3: Probar el Sistema (10 minutos)

1. **Accede a tu frontend en Vercel**
   - URL: https://tu-proyecto.vercel.app

2. **Inicia sesión con el usuario admin**

3. **Verifica funcionalidades básicas:**
   - ✅ Dashboard carga correctamente
   - ✅ Puedes ver las plantillas de checklist
   - ✅ Puedes crear un activo
   - ✅ Puedes crear una orden de trabajo
   - ✅ Las notificaciones funcionan

### Paso 4: Configurar Celery (Opcional - 30 minutos)

Si necesitas tareas asíncronas y monitoreo:

1. **Configurar Redis en Railway**
   - Agregar servicio Redis
   - Configurar variable `CELERY_BROKER_URL`

2. **Configurar Flower**
   - Agregar proceso de Flower
   - Configurar autenticación
   - Acceder al dashboard de monitoreo

Ver guía detallada: **`CONFIGURAR_CELERY_FLOWER.md`** (por crear)

## 📁 Archivos de Referencia

### Guías Principales

| Archivo | Propósito |
|---------|-----------|
| `RESUMEN_CARGA_DATOS.md` | **⭐ EMPIEZA AQUÍ** - Cómo cargar datos en Railway |
| `CARGAR_DATOS_RAILWAY.md` | Guía detallada de carga de datos |
| `DEPLOYMENT_RAILWAY_PASO_A_PASO.md` | Proceso completo de deployment |
| `DEPLOYMENT_GRATUITO.md` | Opciones de deployment gratuito |

### Scripts Útiles

| Archivo | Uso |
|---------|-----|
| `backend/export_all_data.bat` | Exportar datos de local |
| `backend/check_production_data.py` | Verificar datos en producción |
| `load_all_data.sh` | Cargar todos los datos (Railway shell) |

### Datos Exportados

| Archivo | Contenido |
|---------|-----------|
| `backend/roles_export.json` | 3 roles |
| `backend/checklist_templates_export.json` | 5 plantillas |
| `backend/priorities_export.json` | 5 prioridades |
| `backend/workorder_types_export.json` | 8 tipos |
| `backend/asset_categories_export.json` | 8 categorías |
| `backend/locations_export.json` | 6 ubicaciones |

## 🔧 Comandos Útiles

### Railway

```bash
# Ver logs en tiempo real
railway logs

# Abrir shell interactivo
railway shell

# Ver variables de entorno
railway variables

# Redeploy
railway up
```

### Django en Producción

```bash
# Ejecutar migraciones
python backend/manage.py migrate

# Crear superusuario
python backend/manage.py createsuperuser

# Cargar datos
python backend/manage.py loaddata backend/archivo.json

# Verificar datos
python backend/check_production_data.py

# Abrir shell de Django
python backend/manage.py shell
```

### Git

```bash
# Ver estado
git status

# Agregar cambios
git add .

# Commit
git commit -m "mensaje"

# Push a producción
git push origin main
```

## 🐛 Troubleshooting

### Backend no responde

1. Verifica logs en Railway: `railway logs`
2. Verifica que el deploy terminó correctamente
3. Verifica variables de entorno
4. Verifica que la base de datos está conectada

### Frontend no conecta con Backend

1. Verifica CORS en `backend/config/settings/railway.py`
2. Verifica `VITE_API_URL` en Vercel
3. Verifica que el backend está respondiendo: `curl https://tu-backend.railway.app/api/v1/health/`

### Datos no se cargan

1. Verifica que los archivos JSON están en GitHub
2. Verifica que hiciste redeploy después de pushear
3. Ejecuta los comandos uno por uno
4. Revisa los logs de error

### Error de autenticación

1. Verifica que el token JWT no expiró
2. Verifica `SECRET_KEY` en Railway
3. Limpia cookies del navegador
4. Intenta login nuevamente

## 📊 Checklist de Producción

Antes de considerar el sistema "listo para producción":

- [ ] Backend desplegado y respondiendo
- [ ] Frontend desplegado y accesible
- [ ] Base de datos PostgreSQL configurada
- [ ] Datos maestros cargados (roles, plantillas, etc.)
- [ ] Usuario administrador creado
- [ ] CORS configurado correctamente
- [ ] Variables de entorno configuradas
- [ ] Logs funcionando
- [ ] Backup de base de datos configurado (Railway lo hace automático)
- [ ] SSL/HTTPS habilitado (Railway y Vercel lo hacen automático)
- [ ] Pruebas básicas realizadas:
  - [ ] Login funciona
  - [ ] Dashboard carga
  - [ ] Crear activo funciona
  - [ ] Crear orden de trabajo funciona
  - [ ] Checklists disponibles
  - [ ] Notificaciones funcionan

## 🎉 ¡Listo para Producción!

Una vez completados todos los pasos:

1. ✅ Tu sistema está desplegado
2. ✅ Los datos están cargados
3. ✅ Puedes acceder desde cualquier lugar
4. ✅ El sistema es funcional

### Próximos pasos opcionales:

- Configurar dominio personalizado
- Configurar Celery para tareas asíncronas
- Configurar monitoreo con Flower
- Configurar alertas y notificaciones
- Agregar más usuarios
- Cargar datos reales de activos

## 📞 Soporte

Si encuentras problemas:

1. Revisa los logs de Railway
2. Revisa la consola del navegador (F12)
3. Verifica las guías de troubleshooting
4. Revisa la documentación de Railway y Vercel

## 📝 Notas Finales

- Railway y Vercel tienen planes gratuitos generosos
- Los backups son automáticos
- SSL/HTTPS es automático
- Los deploys son automáticos con cada push a main
- Puedes escalar fácilmente cuando lo necesites
