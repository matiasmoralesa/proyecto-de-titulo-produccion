"""
Management command to create initial roles.
"""
from django.core.management.base import BaseCommand
from apps.authentication.models import Role


class Command(BaseCommand):
    help = 'Create initial roles for the system'

    def handle(self, *args, **options):
        roles_data = [
            {
                'name': Role.ADMIN,
                'description': 'Administrador del sistema con acceso completo'
            },
            {
                'name': Role.SUPERVISOR,
                'description': 'Supervisor de mantenimiento con acceso a gestión de órdenes y reportes'
            },
            {
                'name': Role.OPERADOR,
                'description': 'Operador con acceso limitado a órdenes asignadas'
            },
        ]
        
        created_count = 0
        for role_data in roles_data:
            role, created = Role.objects.get_or_create(
                name=role_data['name'],
                defaults={'description': role_data['description']}
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created role: {role.get_name_display()}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'- Role already exists: {role.get_name_display()}')
                )
        
        if created_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'\nSuccessfully created {created_count} role(s)')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('\nAll roles already exist')
            )
