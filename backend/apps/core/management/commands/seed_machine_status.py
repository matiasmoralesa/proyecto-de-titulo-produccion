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

        # Crear estados para activos existentes
        self.stdout.write("\n🚗 Creando estados para activos existentes...")
        
        # Obtener todos los activos
        assets = Asset.objects.all()
        
        if not assets.exists():
            self.stdout.write(self.style.WARNING("⚠️  No hay activos en la base de datos"))
            return
        
        created_count = 0
        for asset in assets:
            try:
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
                    self.stdout.write(self.style.SUCCESS(f"✅ {asset.name}: Estado creado"))
                    created_count += 1
                else:
                    self.stdout.write(f"ℹ️  {asset.name}: Estado ya existe")
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Error con {asset.name}: {e}"))

        # Resumen
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("✅ PROCESO COMPLETADO"))
        self.stdout.write(f"   Estados creados: {created_count}")
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
