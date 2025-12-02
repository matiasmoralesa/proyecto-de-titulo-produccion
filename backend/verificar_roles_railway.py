"""
Script para verificar y corregir roles de usuarios en Railway.
"""
from apps.authentication.models import User, Role

print("\n" + "="*80)
print("VERIFICACIÓN DE ROLES DE USUARIOS")
print("="*80 + "\n")

# Ver todos los usuarios y sus roles
print("📋 Usuarios actuales:\n")
users = User.objects.all()
for user in users:
    print(f"   {user.username:20} → Rol: {user.role.name}")

print("\n" + "="*80)
print("CORRECCIÓN DE ROLES")
print("="*80 + "\n")

# Obtener el rol OPERADOR
try:
    operador_role = Role.objects.get(name='OPERADOR')
    print(f"✅ Rol OPERADOR encontrado: {operador_role.name}\n")
except Role.DoesNotExist:
    print("❌ Rol OPERADOR no existe en la base de datos")
    exit(1)

# Corregir usuarios que deberían ser operadores
usuarios_operadores = ['operador1', 'operador2', 'operador3']

for username in usuarios_operadores:
    try:
        user = User.objects.get(username=username)
        rol_anterior = user.role.name
        
        if rol_anterior != 'OPERADOR':
            user.role = operador_role
            user.save()
            print(f"✅ {username:20} → Cambiado de {rol_anterior} a OPERADOR")
        else:
            print(f"✓  {username:20} → Ya tiene rol OPERADOR")
    except User.DoesNotExist:
        print(f"⚠️  {username:20} → Usuario no existe")

print("\n" + "="*80)
print("VERIFICACIÓN FINAL")
print("="*80 + "\n")

# Verificar de nuevo
for username in usuarios_operadores:
    try:
        user = User.objects.get(username=username)
        print(f"   {user.username:20} → Rol: {user.role.name}")
    except User.DoesNotExist:
        pass

print("\n" + "="*80 + "\n")
