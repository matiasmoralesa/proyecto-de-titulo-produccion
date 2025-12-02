#!/bin/bash
# Script para aplicar sistema de permisos en Railway

echo "🔐 Aplicando Sistema de Permisos en Producción"
echo "=============================================="
echo ""

# Cambiar al directorio backend
cd backend

echo "📋 Paso 1: Verificar migraciones..."
python manage.py showmigrations configuration

echo ""
echo "📋 Paso 2: Aplicar migraciones pendientes..."
python manage.py migrate

echo ""
echo "📋 Paso 3: Crear roles si no existen..."
python manage.py create_roles

echo ""
echo "📋 Paso 4: Asignar rol ADMIN a usuarios sin rol..."
python manage.py shell << EOF
from apps.authentication.models import User, Role

admin_role = Role.objects.get(name='ADMIN')
users_without_role = User.objects.filter(role__isnull=True)

print(f"Usuarios sin rol: {users_without_role.count()}")

for user in users_without_role:
    user.role = admin_role
    user.save()
    print(f"✅ Rol ADMIN asignado a: {user.username}")

print(f"✅ Todos los usuarios tienen rol asignado")
EOF

echo ""
echo "📋 Paso 5: Verificar que AccessLog existe..."
python manage.py shell << EOF
from apps.configuration.models import AccessLog
print(f"✅ Tabla AccessLog existe")
print(f"Registros actuales: {AccessLog.objects.count()}")
EOF

echo ""
echo "✅ Sistema de permisos aplicado correctamente"
echo ""
echo "📊 Resumen:"
echo "  - Migraciones aplicadas"
echo "  - Roles creados"
echo "  - Usuarios con roles asignados"
echo "  - AccessLog funcionando"
echo ""
echo "🎉 ¡Listo! El sistema de permisos está activo."
