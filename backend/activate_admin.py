"""
Script para activar el usuario admin.
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.railway')
django.setup()

from apps.authentication.models import User

try:
    admin = User.objects.get(username='admin')
    admin.is_active = True
    admin.is_staff = True
    admin.is_superuser = True
    admin.save()
    print(f"✅ Usuario admin activado correctamente")
    print(f"   Username: {admin.username}")
    print(f"   Email: {admin.email}")
    print(f"   is_active: {admin.is_active}")
    print(f"   is_staff: {admin.is_staff}")
    print(f"   is_superuser: {admin.is_superuser}")
except User.DoesNotExist:
    print("❌ Usuario admin no existe")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
