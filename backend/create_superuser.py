"""
Script to create a superuser automatically.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.authentication.models import User, Role

# Check if admin user already exists
if User.objects.filter(username='admin').exists():
    print('✓ Admin user already exists')
else:
    # Create admin user
    admin_role = Role.objects.get(name='ADMIN')
    user = User.objects.create_superuser(
        username='admin',
        email='admin@cmms.local',
        password='admin123',
        role=admin_role,
        must_change_password=False
    )
    print('✓ Created admin user')
    print('  Username: admin')
    print('  Password: admin123')
    print('  Email: admin@cmms.local')
