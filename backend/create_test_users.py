"""
Script to create test users for different roles.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.authentication.models import User, Role

# Get roles
admin_role = Role.objects.get(name='ADMIN')
supervisor_role = Role.objects.get(name='SUPERVISOR')
operator_role = Role.objects.get(name='OPERADOR')

# Create supervisor user
supervisor, created = User.objects.get_or_create(
    username='supervisor',
    defaults={
        'email': 'supervisor@cmms.local',
        'first_name': 'Juan',
        'last_name': 'Supervisor',
        'role': supervisor_role,
        'is_staff': False,
        'is_superuser': False
    }
)
if created:
    supervisor.set_password('supervisor123')
    supervisor.save()
    print(f"✓ Usuario supervisor creado: {supervisor.username}")
else:
    print(f"✓ Usuario supervisor ya existe: {supervisor.username}")

# Create operator users
operators_data = [
    {
        'username': 'operador1',
        'email': 'operador1@cmms.local',
        'first_name': 'Carlos',
        'last_name': 'Operador'
    },
    {
        'username': 'operador2',
        'email': 'operador2@cmms.local',
        'first_name': 'María',
        'last_name': 'Operadora'
    }
]

for op_data in operators_data:
    operator, created = User.objects.get_or_create(
        username=op_data['username'],
        defaults={
            'email': op_data['email'],
            'first_name': op_data['first_name'],
            'last_name': op_data['last_name'],
            'role': operator_role,
            'is_staff': False,
            'is_superuser': False
        }
    )
    if created:
        operator.set_password('operador123')
        operator.save()
        print(f"✓ Usuario operador creado: {operator.username}")
    else:
        print(f"✓ Usuario operador ya existe: {operator.username}")

print("\n✅ Usuarios de prueba creados exitosamente!")
print("\nCredenciales:")
print("  - supervisor / supervisor123")
print("  - operador1 / operador123")
print("  - operador2 / operador123")
