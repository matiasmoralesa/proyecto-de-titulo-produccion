"""
Script to check existing users.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.authentication.models import User, Role

print("📊 Roles disponibles:")
roles = Role.objects.all()
for role in roles:
    print(f"  - {role.name}: {role.description}")

print("\n📊 Usuarios existentes:")
users = User.objects.all()
for user in users:
    role_name = user.role.name if user.role else "Sin rol"
    print(f"  - {user.username} ({user.email}) - Rol: {role_name}")

print(f"\nTotal usuarios: {users.count()}")
print(f"Total roles: {roles.count()}")
