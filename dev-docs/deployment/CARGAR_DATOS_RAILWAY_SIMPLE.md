# Cargar Datos en Railway - Método Simple

## 🎯 Problema
La view de Estado de Máquina está vacía porque no hay datos en la base de datos.

## ✅ Solución Rápida

### Método 1: Usar Railway Shell (RECOMENDADO)

1. **Abrir Railway Shell:**
   ```bash
   railway shell
   ```

2. **Ejecutar el script de seed:**
   ```bash
   cd backend
   python seed_all_data.py
   ```

3. **Salir del shell:**
   ```bash
   exit
   ```

### Método 2: Cargar desde Backup

1. **Abrir Railway Shell:**
   ```bash
   railway shell
   ```

2. **Cargar datos:**
   ```bash
   python backend/manage.py loaddata backend/data_backup.json
   ```

3. **Salir:**
   ```bash
   exit
   ```

### Método 3: Crear Datos Manualmente

Si los métodos anteriores no funcionan, puedes crear datos básicos:

1. **Abrir Railway Shell:**
   ```bash
   railway shell
   ```

2. **Abrir Python shell:**
   ```bash
   python backend/manage.py shell
   ```

3. **Ejecutar este código:**
   ```python
   from apps.assets.models import Asset, Location
   from apps.authentication.models import User
   from apps.machine_status.models import AssetStatus
   
   # Crear ubicación
   location, _ = Location.objects.get_or_create(
       name="Sede Principal",
       defaults={
           'address': 'Av. Principal 123',
           'city': 'Santiago',
           'country': 'Chile'
       }
   )
   
   # Crear activos
   assets_data = [
       {'name': 'Camión 1', 'vehicle_type': 'Camión', 'model': 'Volvo FH16', 'serial_number': 'CAM001'},
       {'name': 'Grúa 1', 'vehicle_type': 'Grúa', 'model': 'Liebherr LTM', 'serial_number': 'GRU001'},
       {'name': 'Excavadora 1', 'vehicle_type': 'Excavadora', 'model': 'CAT 320', 'serial_number': 'EXC001'},
   ]
   
   for asset_data in assets_data:
       asset, created = Asset.objects.get_or_create(
           serial_number=asset_data['serial_number'],
           defaults={
               **asset_data,
               'location': location,
               'status': 'ACTIVE'
           }
       )
       
       # Crear estado inicial
       if created:
           AssetStatus.objects.create(
               asset=asset,
               status_type='OPERANDO',
               fuel_level=100,
               odometer_reading=0,
               condition_notes='Estado inicial',
               last_updated_by=User.objects.filter(is_superuser=True).first()
           )
           print(f"✅ Creado: {asset.name}")
   
   print("\n✅ Datos creados exitosamente!")
   ```

4. **Salir:**
   ```python
   exit()
   ```
   ```bash
   exit
   ```

## 🔍 Verificar que Funcionó

Después de cargar los datos, ejecuta:

```bash
python test_machine_status_endpoint.py
```

Deberías ver:
```
✅ Estados obtenidos: 3 activos (o más)
✅ Historial obtenido: X registros
```

## 📝 Notas

- El método 3 (manual) es el más confiable si los scripts no funcionan
- Puedes agregar más activos repitiendo el código
- Los estados se crean automáticamente para cada activo

## 🚀 Después de Cargar los Datos

1. Accede a la aplicación web
2. Ve a "Estado de Máquina"
3. Deberías ver todos los activos con sus estados
4. Puedes actualizar el estado de cualquier activo

## ⚠️ Si Sigue Sin Funcionar

1. Verifica que estés conectado a la base de datos correcta
2. Revisa los logs de Railway: `railway logs`
3. Verifica que el usuario admin exista
4. Contacta al equipo de desarrollo
