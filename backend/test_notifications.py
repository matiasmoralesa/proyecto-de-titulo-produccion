"""
Script to test notification creation with work orders.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.utils import timezone
from apps.authentication.models import User
from apps.assets.models import Asset
from apps.work_orders.models import WorkOrder
from apps.notifications.models import Notification

# Get users
try:
    admin_user = User.objects.filter(role__name='ADMIN').first()
    operator_user = User.objects.filter(role__name='OPERADOR').first()
    
    if not admin_user or not operator_user:
        print("❌ Error: No se encontraron usuarios ADMIN u OPERADOR")
        exit(1)
    
    # Get an asset
    asset = Asset.objects.first()
    if not asset:
        print("❌ Error: No se encontraron activos")
        exit(1)
    
    print(f"✓ Admin user: {admin_user.username}")
    print(f"✓ Operator user: {operator_user.username}")
    print(f"✓ Asset: {asset.name}")
    
    # Count notifications before
    notifications_before = Notification.objects.count()
    print(f"\n📊 Notificaciones antes: {notifications_before}")
    
    # Create a work order
    work_order = WorkOrder.objects.create(
        title="Prueba de Notificaciones",
        description="Esta es una orden de trabajo de prueba para verificar las notificaciones",
        priority=WorkOrder.PRIORITY_HIGH,
        status=WorkOrder.STATUS_PENDING,
        asset=asset,
        assigned_to=operator_user,
        scheduled_date=timezone.now() + timezone.timedelta(days=1),
        created_by=admin_user
    )
    
    print(f"\n✓ Orden de trabajo creada: {work_order.work_order_number}")
    
    # Count notifications after
    notifications_after = Notification.objects.count()
    print(f"📊 Notificaciones después: {notifications_after}")
    print(f"📊 Nuevas notificaciones: {notifications_after - notifications_before}")
    
    # Show created notifications
    new_notifications = Notification.objects.filter(
        related_object_type='work_order',
        related_object_id=work_order.id
    )
    
    print(f"\n📬 Notificaciones creadas:")
    for notif in new_notifications:
        print(f"  - Para: {notif.user.username}")
        print(f"    Tipo: {notif.notification_type}")
        print(f"    Título: {notif.title}")
        print(f"    Mensaje: {notif.message}")
        print()
    
    # Test reassignment
    print("🔄 Probando reasignación...")
    supervisor_user = User.objects.filter(role__name='SUPERVISOR').first()
    if supervisor_user:
        notifications_before_reassign = Notification.objects.count()
        work_order.assigned_to = supervisor_user
        work_order.save()
        
        notifications_after_reassign = Notification.objects.count()
        print(f"📊 Notificaciones después de reasignación: {notifications_after_reassign}")
        print(f"📊 Nuevas notificaciones: {notifications_after_reassign - notifications_before_reassign}")
    
    # Test completion
    print("\n✅ Probando completación...")
    notifications_before_complete = Notification.objects.count()
    work_order.complete(
        completion_notes="Trabajo completado exitosamente",
        actual_hours=2.5
    )
    
    notifications_after_complete = Notification.objects.count()
    print(f"📊 Notificaciones después de completación: {notifications_after_complete}")
    print(f"📊 Nuevas notificaciones: {notifications_after_complete - notifications_before_complete}")
    
    print("\n✅ Prueba completada exitosamente!")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
