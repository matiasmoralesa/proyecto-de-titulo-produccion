"""
Management command to seed realistic data for 1 year
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from decimal import Decimal

from apps.assets.models import Asset, Location
from apps.authentication.models import User, Role
from apps.machine_status.models import AssetStatus, AssetStatusHistory
from apps.work_orders.models import WorkOrder
from apps.maintenance.models import MaintenancePlan


class Command(BaseCommand):
    help = 'Seed realistic data for 1 year period'

    def handle(self, *args, **options):
        self.stdout.write("=" * 60)
        self.stdout.write("GENERANDO DATOS REALISTAS - 1 AÑO")
        self.stdout.write("=" * 60)

        # Obtener usuarios
        try:
            admin_user = User.objects.filter(role__name=Role.ADMIN).first()
            supervisor_users = list(User.objects.filter(role__name=Role.SUPERVISOR))
            operator_users = list(User.objects.filter(role__name=Role.OPERADOR))
            
            if not admin_user:
                self.stdout.write(self.style.ERROR("❌ No hay usuario admin"))
                return
                
            self.stdout.write(self.style.SUCCESS(f"✅ Usuarios encontrados:"))
            self.stdout.write(f"   Admin: {admin_user.username}")
            self.stdout.write(f"   Supervisores: {len(supervisor_users)}")
            self.stdout.write(f"   Operadores: {len(operator_users)}")
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error: {e}"))
            return

        # Fechas
        end_date = timezone.now()
        start_date = end_date - timedelta(days=365)
        
        # Crear más activos si es necesario
        self.stdout.write("\n🚗 Verificando activos...")
        location = Location.objects.first()
        
        if not location:
            location = Location.objects.create(
                name="Sede Principal",
                address="Av. Principal 123, Santiago, Chile"
            )
            self.stdout.write(self.style.SUCCESS(f"✅ Ubicación creada"))

        # Crear activos adicionales si hay menos de 10
        assets = list(Asset.objects.all())
        if len(assets) < 10:
            additional_assets = [
                {'name': 'Camión Volvo FH16', 'vehicle_type': 'Camión', 'model': 'FH16', 'serial_number': 'CAM-VLV-001', 'license_plate': 'ABCD-12'},
                {'name': 'Grúa Liebherr LTM', 'vehicle_type': 'Grúa', 'model': 'LTM 1100', 'serial_number': 'GRU-LBH-001', 'license_plate': 'EFGH-34'},
                {'name': 'Excavadora CAT 320', 'vehicle_type': 'Excavadora', 'model': '320D', 'serial_number': 'EXC-CAT-001', 'license_plate': 'IJKL-56'},
                {'name': 'Retroexcavadora JCB 3CX', 'vehicle_type': 'Retroexcavadora', 'model': '3CX', 'serial_number': 'RET-JCB-001', 'license_plate': 'MNOP-78'},
                {'name': 'Camión Mercedes Actros', 'vehicle_type': 'Camión', 'model': 'Actros 2546', 'serial_number': 'CAM-MER-001', 'license_plate': 'QRST-90'},
                {'name': 'Montacargas Toyota 8FD', 'vehicle_type': 'Montacargas', 'model': '8FD25', 'serial_number': 'MON-TOY-001', 'license_plate': 'UVWX-11'},
                {'name': 'Bulldozer CAT D6', 'vehicle_type': 'Bulldozer', 'model': 'D6T', 'serial_number': 'BUL-CAT-001', 'license_plate': 'YZAB-22'},
                {'name': 'Camión Scania R450', 'vehicle_type': 'Camión', 'model': 'R450', 'serial_number': 'CAM-SCA-001', 'license_plate': 'CDEF-33'},
                {'name': 'Cargador Frontal CAT 950', 'vehicle_type': 'Cargador', 'model': '950M', 'serial_number': 'CAR-CAT-001', 'license_plate': 'GHIJ-44'},
                {'name': 'Compactadora Bomag BW', 'vehicle_type': 'Compactadora', 'model': 'BW 213', 'serial_number': 'COM-BOM-001', 'license_plate': 'KLMN-55'},
            ]
            
            for asset_data in additional_assets:
                if len(assets) >= 10:
                    break
                asset, created = Asset.objects.get_or_create(
                    serial_number=asset_data['serial_number'],
                    defaults={
                        **asset_data,
                        'location': location,
                        'status': 'ACTIVE',
                        'installation_date': start_date.date(),
                        'created_by': admin_user
                    }
                )
                # Agregar a la lista si no está (creado o ya existía)
                if asset not in assets:
                    assets.append(asset)
                if created:
                    self.stdout.write(self.style.SUCCESS(f"✅ Activo creado: {asset.name}"))
                else:
                    self.stdout.write(f"   ℹ️  Activo ya existe: {asset.name}")

        self.stdout.write(f"📦 Total activos: {len(assets)}")
        self.stdout.write(f"\n📅 Período: {start_date.date()} a {end_date.date()}")

        # Contadores
        status_updates = 0
        work_orders_created = 0
        maintenance_plans_created = 0

        # Para cada activo, generar datos
        for asset in assets:
            self.stdout.write(f"\n🔄 Procesando: {asset.name}")
            
            # 1. Crear plan de mantenimiento
            try:
                plan, created = MaintenancePlan.objects.get_or_create(
                    asset=asset,
                    name=f"Mantenimiento Preventivo {asset.name}",
                    defaults={
                        'description': f'Plan de mantenimiento preventivo para {asset.name}',
                        'recurrence_type': 'MONTHLY',
                        'recurrence_interval': 1,
                        'estimated_duration': Decimal('4.00'),
                        'next_due_date': end_date + timedelta(days=30),
                        'is_active': True
                    }
                )
                if created:
                    maintenance_plans_created += 1
                    self.stdout.write(f"   ✅ Plan de mantenimiento creado")
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"   ⚠️  Error plan: {e}"))

            # 2. Generar órdenes de trabajo (1-2 por mes = 12-24 al año)
            num_work_orders = random.randint(12, 24)
            
            for i in range(num_work_orders):
                try:
                    # Fecha aleatoria en el año
                    days_ago = random.randint(0, 365)
                    wo_created_date = end_date - timedelta(days=days_ago)
                    
                    # Asignar usuario
                    assigned_user = random.choice(operator_users) if operator_users else admin_user
                    
                    # Tipo de trabajo
                    work_types = [
                        ('Mantenimiento Preventivo', 'Media', 4),
                        ('Reparación Menor', 'Baja', 2),
                        ('Inspección', 'Baja', 1),
                        ('Mantenimiento Correctivo', 'Alta', 6),
                        ('Cambio de Aceite', 'Media', 2),
                        ('Revisión de Frenos', 'Alta', 3),
                        ('Cambio de Filtros', 'Baja', 1),
                        ('Reparación de Motor', 'Urgente', 12),
                    ]
                    
                    work_type = random.choice(work_types)
                    title, priority, hours = work_type
                    
                    # Calcular fechas
                    completion_days = random.randint(1, 5)
                    wo_completed_date = wo_created_date + timedelta(days=completion_days)
                    
                    # Crear orden de trabajo
                    wo = WorkOrder.objects.create(
                        asset=asset,
                        title=f"{title} - {asset.name}",
                        description=f"Trabajo de {title.lower()} programado",
                        priority=priority,
                        status='Completada',  # Todas completadas
                        assigned_to=assigned_user,
                        created_by=supervisor_users[0] if supervisor_users else admin_user,
                        scheduled_date=wo_created_date,
                        actual_hours=Decimal(str(hours + random.uniform(-0.5, 1.0))),
                        completed_date=wo_completed_date,
                        completion_notes=f"Trabajo completado satisfactoriamente. {random.choice(['Sin novedades.', 'Se reemplazaron componentes.', 'Todo en orden.'])}"
                    )
                    
                    # Actualizar created_at manualmente (Django lo establece automáticamente)
                    WorkOrder.objects.filter(id=wo.id).update(
                        created_at=wo_created_date,
                        updated_at=wo_completed_date
                    )
                    
                    work_orders_created += 1
                    
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"   ⚠️  Error WO: {e}"))

            # 3. Generar actualizaciones de estado (2-4 por mes = 24-48 al año)
            num_status_updates = random.randint(24, 48)
            
            # Estado inicial
            current_odometer = random.randint(10000, 50000)
            current_fuel = 100
            
            for i in range(num_status_updates):
                try:
                    # Fecha aleatoria
                    days_ago = random.randint(0, 365)
                    update_date = end_date - timedelta(days=days_ago)
                    
                    # Simular uso del activo
                    current_odometer += random.randint(50, 500)
                    current_fuel = max(0, current_fuel - random.randint(5, 30))
                    
                    # Si combustible bajo, recargar
                    if current_fuel < 20:
                        current_fuel = 100
                    
                    # Estado aleatorio (mayoría operando)
                    status_weights = [
                        ('OPERANDO', 70),
                        ('DETENIDA', 15),
                        ('EN_MANTENIMIENTO', 10),
                        ('FUERA_DE_SERVICIO', 5)
                    ]
                    
                    status_type = random.choices(
                        [s[0] for s in status_weights],
                        weights=[s[1] for s in status_weights]
                    )[0]
                    
                    # Notas según estado
                    notes_by_status = {
                        'OPERANDO': ['Operación normal', 'Todo en orden', 'Sin novedades', 'Funcionamiento óptimo'],
                        'DETENIDA': ['Esperando carga', 'Fin de turno', 'Pausa programada', 'Esperando instrucciones'],
                        'EN_MANTENIMIENTO': ['Mantenimiento preventivo', 'Revisión programada', 'Cambio de aceite', 'Inspección técnica'],
                        'FUERA_DE_SERVICIO': ['Reparación mayor', 'Falla mecánica', 'Esperando repuestos', 'Revisión profunda']
                    }
                    
                    condition_notes = random.choice(notes_by_status[status_type])
                    
                    # Crear historial
                    AssetStatusHistory.objects.create(
                        asset=asset,
                        status_type=status_type,
                        odometer_reading=Decimal(str(current_odometer)),
                        fuel_level=current_fuel,
                        condition_notes=condition_notes,
                        updated_by=random.choice(operator_users) if operator_users else admin_user,
                        timestamp=update_date
                    )
                    
                    status_updates += 1
                    
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"   ⚠️  Error status: {e}"))

            # 4. Actualizar estado actual del activo
            try:
                current_status, _ = AssetStatus.objects.get_or_create(
                    asset=asset,
                    defaults={
                        'status_type': 'OPERANDO',
                        'fuel_level': random.randint(50, 100),
                        'odometer_reading': Decimal(str(current_odometer)),
                        'condition_notes': 'Estado actual del activo',
                        'last_updated_by': admin_user
                    }
                )
                
                # Actualizar con valores actuales
                current_status.odometer_reading = Decimal(str(current_odometer))
                current_status.fuel_level = random.randint(50, 100)
                current_status.status_type = 'OPERANDO'
                current_status.save()
                
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"   ⚠️  Error estado actual: {e}"))

            self.stdout.write(f"   ✅ Completado: {asset.name}")

        # Resumen final
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("✅ GENERACIÓN COMPLETADA"))
        self.stdout.write("=" * 60)
        self.stdout.write(f"\n📊 RESUMEN:")
        self.stdout.write(f"   Activos procesados: {len(assets)}")
        self.stdout.write(f"   Órdenes de trabajo: {work_orders_created}")
        self.stdout.write(f"   Actualizaciones de estado: {status_updates}")
        self.stdout.write(f"   Planes de mantenimiento: {maintenance_plans_created}")
        self.stdout.write(f"\n   Total registros: {work_orders_created + status_updates + maintenance_plans_created}")
        self.stdout.write("=" * 60)
        
        # Estadísticas por activo
        self.stdout.write(f"\n📈 ESTADÍSTICAS:")
        self.stdout.write(f"   Promedio WO por activo: {work_orders_created / len(assets):.1f}")
        self.stdout.write(f"   Promedio estados por activo: {status_updates / len(assets):.1f}")
        self.stdout.write(f"   Período: 1 año ({start_date.date()} a {end_date.date()})")
