"""
Management command to create sample locations.
"""
from django.core.management.base import BaseCommand
from apps.assets.models import Location


class Command(BaseCommand):
    help = 'Create sample locations for development'

    def handle(self, *args, **options):
        locations_data = [
            {
                'name': 'Planta Principal',
                'address': 'Av. Industrial 123, Lima',
                'coordinates': '-12.0464,-77.0428',
                'description': 'Planta principal de operaciones'
            },
            {
                'name': 'Almacén Central',
                'address': 'Jr. Los Almacenes 456, Lima',
                'coordinates': '-12.0500,-77.0500',
                'description': 'Almacén central de repuestos y equipos'
            },
            {
                'name': 'Taller de Mantenimiento',
                'address': 'Av. Talleres 789, Lima',
                'coordinates': '-12.0550,-77.0550',
                'description': 'Taller principal de mantenimiento'
            },
            {
                'name': 'Sede Norte',
                'address': 'Av. Norte 321, Lima',
                'coordinates': '-12.0400,-77.0400',
                'description': 'Sede operativa zona norte'
            },
            {
                'name': 'Sede Sur',
                'address': 'Av. Sur 654, Lima',
                'coordinates': '-12.0600,-77.0600',
                'description': 'Sede operativa zona sur'
            },
        ]
        
        created_count = 0
        for location_data in locations_data:
            location, created = Location.objects.get_or_create(
                name=location_data['name'],
                defaults={
                    'address': location_data['address'],
                    'coordinates': location_data['coordinates'],
                    'description': location_data['description']
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created location: {location.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'- Location already exists: {location.name}')
                )
        
        if created_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'\nSuccessfully created {created_count} location(s)')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('\nAll locations already exist')
            )
