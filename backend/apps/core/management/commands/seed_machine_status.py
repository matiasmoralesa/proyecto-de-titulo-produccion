"""
Management command to seed machine status data
"""
from django.core.management.base import BaseCommand
from apps.assets.models import Asset, Location
from apps.authentication.models import User
from apps.machine_status.models import AssetStatus


class Command(BaseCommand):
    help = 'Seed machine status data for all assets'

    def handle(self, *args, **options):
        self.stdout.write("=" * 60)
        self.stdout.write("CREANDO DATOS DE ESTADO DE MÁQUINA")
        self.stdout.write("=" * 60)

        # Obtener usuario admin
        try:
            admin_user = User.objects.filter(is_superuser=True).first()
            if not admin_user:
                self.stdout.write(self.style.ERROR("❌ No se encontró usuario admin"))
                return
            self.stdout.write(self.style.SUCCESS(f"✅ Usuario admin: {admin_user.username}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error: {e}"))
            return

        # Crear ubicación
        self.stdout.write("\n📍 Creando ubicación...")
        try:
            location, created = Location.objects.get_or_create(
                name="Sede Principal",
                defaults={
                    'address': 'Av. Principal 123, Santiago, Chile',
                    'description': 'Ubicación principal de operaciones'
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Ubicación creada: {location.name}"))
            else:
                self.stdout.write(f"ℹ️  Ubicación ya existe: {location.name}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error: {e}"))
            return

        # Crear activos
        self.stdout.write("\n🚗 Creando activos...")
        assets_data = [
            {
                'name': 'Camión Volvo 1',
                'vehicle_type': 'Camión',
                'model': 'Volvo FH16',
                'serial_number': 'CAM001',
                'license_plate': 'ABC-123'
            },
            {
                'name': 'Grúa Liebherr 1',
                'vehicle_type': 'Grúa',
                'model': 'Liebherr LTM 1100',
                'serial_number': 'GRU001',
                'license_plate': 'DEF-456'
            },
            {
                'name': 'Excavadora CAT 1',
                'vehicle_type': 'Excavadora',
                'model': 'CAT 320',
                'serial_number': 'EXC001',
                'license_plate': 'GHI-789'
            },
            {
                'name': 'Retroexcavadora JCB 1',
                'vehicle_type': 'Retroexcavadora',
                'model': 'JCB 3CX',
                'serial_number': 'RET001',
                'license_plate': 'JKL-012'
            },
            {
                'name': 'Montacargas Toyota 1',
                'vehicle_type': 'Montacargas',
                'model': 'Toyota 8FG25',
                'serial_number': 'MON001',
                'license_plate': 'MNO-345'
            }
        ]

        created_count = 0
        for asset_data in assets_data:
            try:
                asset, created = Asset.objects.get_or_create(
                    serial_number=asset_data['serial_number'],
                    defaults={
                        **asset_data,
                        'location': location,
                        'status': 'ACTIVE',
                        'purchase_date': '2023-01-01',
                        'manufacturer': asset_data['model'].split()[0]
                    }
                )
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f"✅ Activo creado: {asset.name}"))
                    created_count += 1
                else:
                    self.stdout.write(f"ℹ️  Activo ya existe: {asset.name}")
                
                # Crear o verificar estado
                status, status_created = AssetStatus.objects.get_or_create(
                    asset=asset,
                    defaults={
                        'status_type': 'OPERANDO',
                        'fuel_level': 100,
                        'odometer_reading': 0,
                        'condition_notes': 'Estado inicial del activo',
                        'last_updated_by': admin_user
                    }
                )
                
                if status_created:
                    self.stdout.write(f"   ✅ Estado creado: OPERANDO (100% combustible)")
                else:
                    self.stdout.write(f"   ℹ️  Estado ya existe")
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Error con {asset_data['name']}: {e}"))

        # Resumen
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("✅ PROCESO COMPLETADO"))
        self.stdout.write(f"   Activos nuevos: {created_count}")
        self.stdout.write(f"   Total activos: {Asset.objects.count()}")
        self.stdout.write(f"   Total estados: {AssetStatus.objects.count()}")
        self.stdout.write("=" * 60)

        # Mostrar resumen
        self.stdout.write("\n📊 RESUMEN DE ACTIVOS:")
        for asset in Asset.objects.all():
            try:
                status = AssetStatus.objects.get(asset=asset)
                self.stdout.write(f"   {asset.name}: {status.status_type} ({status.fuel_level}% combustible)")
            except AssetStatus.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"   {asset.name}: SIN ESTADO"))
