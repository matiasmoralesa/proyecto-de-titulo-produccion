"""
Management command to load checklist templates from JSON file.
"""
import json
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.checklists.models import ChecklistTemplate, ChecklistTemplateItem


class Command(BaseCommand):
    help = 'Load checklist templates from JSON file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default=None,
            help='Path to the JSON file with checklist templates'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force reload templates (delete existing system templates)'
        )

    def handle(self, *args, **options):
        self.stdout.write('Cargando plantillas de checklists...')
        
        # Get the JSON file path
        if options['file']:
            json_file = options['file']
            # If relative path, make it absolute from project root
            if not os.path.isabs(json_file):
                from django.conf import settings
                json_file = os.path.join(settings.BASE_DIR.parent, json_file)
        else:
            fixtures_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                'fixtures'
            )
            json_file = os.path.join(fixtures_dir, 'checklist_templates.json')
        
        if not os.path.exists(json_file):
            self.stdout.write(self.style.ERROR(
                f'Archivo no encontrado: {json_file}'
            ))
            return
        
        # Load JSON data
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Get templates array from JSON
        templates_data = data.get('templates', [])
        
        if not templates_data:
            self.stdout.write(self.style.ERROR('No se encontraron plantillas en el archivo JSON'))
            return
        
        created_count = 0
        updated_count = 0
        
        # Process each template
        for template_data in templates_data:
            items_data = template_data.pop('items', [])
            
            with transaction.atomic():
                # Create or update template
                template, created = ChecklistTemplate.objects.update_or_create(
                    code=template_data['code'],
                    defaults=template_data
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(
                        f'✓ Creada: {template.code} - {template.name}'
                    ))
                else:
                    updated_count += 1
                    self.stdout.write(self.style.WARNING(
                        f'↻ Actualizada: {template.code} - {template.name}'
                    ))
                
                # Delete existing items if updating
                if not created:
                    template.items.all().delete()
                
                # Create items
                for item_data in items_data:
                    ChecklistTemplateItem.objects.create(
                        template=template,
                        **item_data
                    )
                
                self.stdout.write(f'  Items creados: {len(items_data)}')
        
        self.stdout.write(self.style.SUCCESS(
            f'\n✓ Proceso completado.'
        ))
        self.stdout.write(f'  Plantillas creadas: {created_count}')
        self.stdout.write(f'  Plantillas actualizadas: {updated_count}')
        self.stdout.write(f'  Total plantillas: {ChecklistTemplate.objects.count()}')
        self.stdout.write(f'  Total items: {ChecklistTemplateItem.objects.count()}')
