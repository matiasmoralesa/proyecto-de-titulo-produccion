"""
Management command to fix operator roles in production.
"""
from django.core.management.base import BaseCommand
from apps.authentication.models import User, Role


class Command(BaseCommand):
    help = 'Fix operator roles in production database'

    def handle(self, *args, **options):
        self.stdout.write("\n" + "="*80)
        self.stdout.write("VERIFICACIÓN DE ROLES DE USUARIOS")
        self.stdout.write("="*80 + "\n")

        # Ver todos los usuarios y sus roles
        self.stdout.write("📋 Usuarios actuales:\n")
        users = User.objects.all()
        for user in users:
            self.stdout.write(f"   {user.username:20} → Rol: {user.role.name}")

        self.stdout.write("\n" + "="*80)
        self.stdout.write("CORRECCIÓN DE ROLES")
        self.stdout.write("="*80 + "\n")

        # Obtener el rol OPERADOR
        try:
            operador_role = Role.objects.get(name='OPERADOR')
            self.stdout.write(self.style.SUCCESS(f"✅ Rol OPERADOR encontrado: {operador_role.name}\n"))
        except Role.DoesNotExist:
            self.stdout.write(self.style.ERROR("❌ Rol OPERADOR no existe en la base de datos"))
            return

        # Corregir usuarios que deberían ser operadores
        usuarios_operadores = ['operador1', 'operador2', 'operador3']

        for username in usuarios_operadores:
            try:
                user = User.objects.get(username=username)
                rol_anterior = user.role.name
                
                if rol_anterior != 'OPERADOR':
                    user.role = operador_role
                    user.save()
                    self.stdout.write(self.style.SUCCESS(
                        f"✅ {username:20} → Cambiado de {rol_anterior} a OPERADOR"
                    ))
                else:
                    self.stdout.write(f"✓  {username:20} → Ya tiene rol OPERADOR")
            except User.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"⚠️  {username:20} → Usuario no existe"))

        self.stdout.write("\n" + "="*80)
        self.stdout.write("VERIFICACIÓN FINAL")
        self.stdout.write("="*80 + "\n")

        # Verificar de nuevo
        for username in usuarios_operadores:
            try:
                user = User.objects.get(username=username)
                self.stdout.write(f"   {user.username:20} → Rol: {user.role.name}")
            except User.DoesNotExist:
                pass

        self.stdout.write("\n" + "="*80 + "\n")
        self.stdout.write(self.style.SUCCESS("✅ Proceso completado"))
