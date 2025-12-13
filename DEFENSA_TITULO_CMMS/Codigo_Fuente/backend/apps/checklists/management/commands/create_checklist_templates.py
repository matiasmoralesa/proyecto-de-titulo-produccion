"""
Management command to create checklist templates.
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.checklists.models import ChecklistTemplate, ChecklistTemplateItem


class Command(BaseCommand):
    help = 'Create checklist templates for all vehicle types'

    def get_templates_data(self):
        """Return all templates data."""
        return [
            # 1. Camión Supersucker
            {
                'code': 'SUPERSUCKER-CH01',
                'name': 'Check List Camión Supersucker',
                'description': 'Checklist diario para Camión Supersucker',
                'vehicle_type': 'Camión Supersucker',
                'is_system_template': True,
                'passing_score': 80,
                'sections': [
                    ('Motor', [
                        'Nivel de aceite motor',
                        'Fugas de aceite',
                        'Nivel de líquido refrigerante',
                    ]),
                    ('Sistema de Vacío', [
                        'Funcionamiento del sistema de vacío',
                        'Estado de mangueras',
                    ]),
                    ('Tanque', [
                        'Estado del tanque (sin fugas)',
                    ]),
                    ('Frenos', [
                        'Funcionamiento de freno de servicio',
                        'Funcionamiento de freno de estacionamiento',
                    ]),
                    ('Neumáticos', [
                        'Presión de neumáticos',
                        'Estado de neumáticos',
                    ]),
                    ('Luces y Señalización', [
                        'Luces delanteras',
                        'Luces traseras',
                        'Luces de emergencia',
                    ]),
                    ('Seguridad', [
                        'Extintor',
                        'Botiquín',
                    ]),
                ],
            },
            # 2. Camioneta MDO
            {
                'code': 'F-PR-020-CH01',
                'name': 'Check List Camionetas MDO',
                'description': 'Checklist diario para Camionetas MDO',
                'vehicle_type': 'Camioneta MDO',
                'is_system_template': True,
                'passing_score': 80,
                'sections': [
                    ('I - Auto Evaluación del Operador', [
                        'Cumplo con descanso suficiente y condiciones para manejo seguro',
                        'Cumplo con condiciones físicas adecuadas',
                        'Estoy consciente de mi responsabilidad al conducir',
                    ]),
                    ('II - Documentación del Operador', [
                        'Licencia Municipal',
                        'Licencia interna de Faena',
                    ]),
                    ('III - Requisitos', [
                        'Permiso de Circulación',
                        'Revisión Técnica',
                        'Seguro Obligatorio',
                        'Cinturones de Seguridad en buen estado',
                        'Espejos interior y exterior en condiciones y limpios',
                        'Frenos (incluye freno de mano) en condiciones operativas',
                        'Neumáticos en buen estado (incluye dos repuestos)',
                        'Luces (Altas, Bajas, Frenos, intermitentes, retroceso)',
                        'Vidrios y parabrisas limpios',
                        'Gata y llave de rueda disponible',
                    ]),
                    ('IV - Condiciones Complementarias', [
                        'Baliza y pértiga (funcionando y en condiciones)',
                        'Radio Base funciona en todos los canales',
                        'Limpiaparabrisas funciona correctamente',
                        'Bocina en buen estado',
                        'Orden y Aseo (interior vehículo y pick up)',
                        'Estado de carrocería, parachoques, portalón',
                        'Sello caja de operación invierno en buenas condiciones',
                        'Cuñas de seguridad disponibles (2)',
                        'Aire acondicionado/calefacción',
                    ]),
                ],
            },
            # 3. Retroexcavadora MDO
            {
                'code': 'F-PR-034-CH01',
                'name': 'Check Retroexcavadora MDO',
                'description': 'Checklist diario para Retroexcavadora MDO',
                'vehicle_type': 'Retroexcavadora MDO',
                'is_system_template': True,
                'passing_score': 80,
                'sections': [
                    ('I - Auto Evaluación del Operador', [
                        'Cumplo con descanso suficiente y condiciones para manejo seguro',
                        'Cumplo con condiciones físicas adecuadas',
                        'Estoy consciente de mi responsabilidad al operar',
                    ]),
                    ('II - Documentación del Operador', [
                        'Licencia Municipal',
                        'Licencia interna de Faena',
                    ]),
                    ('III - Motor y Sistema Hidráulico', [
                        'Nivel de aceite motor',
                        'Nivel de líquido refrigerante',
                        'Nivel de aceite hidráulico',
                        'Fugas de aceite o líquidos',
                    ]),
                    ('IV - Sistema de Frenos', [
                        'Funcionamiento de freno de servicio',
                        'Funcionamiento de freno de estacionamiento',
                    ]),
                    ('V - Neumáticos y Orugas', [
                        'Presión de neumáticos',
                        'Estado de neumáticos',
                    ]),
                    ('VI - Sistema Eléctrico', [
                        'Luces delanteras',
                        'Luces traseras',
                        'Luces de emergencia',
                        'Bocina',
                    ]),
                    ('VII - Cabina y Controles', [
                        'Cinturón de seguridad',
                        'Espejos retrovisores',
                        'Controles de operación (joysticks/palancas)',
                        'Vidrios y parabrisas limpios',
                    ]),
                    ('VIII - Implementos', [
                        'Estado del brazo excavador',
                        'Estado del balde/cuchara',
                        'Estado de cilindros hidráulicos',
                        'Estado de mangueras hidráulicas',
                    ]),
                    ('IX - Seguridad', [
                        'Extintor',
                        'Botiquín',
                        'Baliza',
                    ]),
                ],
            },
            # 4. Cargador Frontal MDO
            {
                'code': 'F-PR-037-CH01',
                'name': 'Check List Cargador Frontal MDO',
                'description': 'Checklist diario para Cargador Frontal MDO',
                'vehicle_type': 'Cargador Frontal MDO',
                'is_system_template': True,
                'passing_score': 80,
                'sections': [
                    ('I - Auto Evaluación del Operador', [
                        'Cumplo con descanso suficiente y condiciones para manejo seguro',
                        'Cumplo con condiciones físicas adecuadas',
                        'Estoy consciente de mi responsabilidad al operar',
                    ]),
                    ('II - Documentación del Operador', [
                        'Licencia Municipal',
                        'Licencia interna de Faena',
                    ]),
                    ('III - Motor y Sistema Hidráulico', [
                        'Nivel de aceite motor',
                        'Nivel de líquido refrigerante',
                        'Nivel de aceite hidráulico',
                        'Fugas de aceite o líquidos',
                        'Nivel de combustible',
                    ]),
                    ('IV - Sistema de Frenos', [
                        'Funcionamiento de freno de servicio',
                        'Funcionamiento de freno de estacionamiento',
                    ]),
                    ('V - Neumáticos', [
                        'Presión de neumáticos',
                        'Estado de neumáticos',
                    ]),
                    ('VI - Sistema Eléctrico', [
                        'Luces delanteras',
                        'Luces traseras',
                        'Luces de emergencia',
                        'Bocina',
                    ]),
                    ('VII - Cabina y Controles', [
                        'Cinturón de seguridad',
                        'Espejos retrovisores',
                        'Controles de operación (joysticks/palancas)',
                        'Vidrios y parabrisas limpios',
                        'Limpiaparabrisas',
                    ]),
                    ('VIII - Implementos', [
                        'Estado del balde/cuchara',
                        'Estado de cilindros hidráulicos',
                        'Estado de mangueras hidráulicas',
                        'Estado de brazos de levante',
                    ]),
                    ('IX - Seguridad', [
                        'Extintor',
                        'Botiquín',
                        'Baliza',
                    ]),
                ],
            },
            # 5. Minicargador MDO
            {
                'code': 'F-PR-040-CH01',
                'name': 'Check List Minicargador MDO',
                'description': 'Checklist diario para Minicargador MDO',
                'vehicle_type': 'Minicargador MDO',
                'is_system_template': True,
                'passing_score': 80,
                'sections': [
                    ('I - Auto Evaluación del Operador', [
                        'Cumplo con descanso suficiente y condiciones para manejo seguro',
                        'Cumplo con condiciones físicas adecuadas',
                        'Estoy consciente de mi responsabilidad al operar',
                    ]),
                    ('II - Documentación del Operador', [
                        'Licencia Municipal',
                        'Licencia interna de Faena',
                    ]),
                    ('III - Motor y Sistema Hidráulico', [
                        'Nivel de aceite motor',
                        'Nivel de líquido refrigerante',
                        'Nivel de aceite hidráulico',
                        'Fugas de aceite o líquidos',
                        'Nivel de combustible',
                    ]),
                    ('IV - Sistema de Frenos', [
                        'Funcionamiento de freno de servicio',
                        'Funcionamiento de freno de estacionamiento',
                    ]),
                    ('V - Neumáticos u Orugas', [
                        'Presión de neumáticos (si aplica)',
                        'Estado de neumáticos u orugas',
                    ]),
                    ('VI - Sistema Eléctrico', [
                        'Luces delanteras',
                        'Luces traseras',
                        'Luces de emergencia',
                        'Bocina',
                    ]),
                    ('VII - Cabina y Controles', [
                        'Cinturón de seguridad',
                        'Barra de protección ROPS',
                        'Controles de operación (joysticks/palancas)',
                        'Vidrios limpios',
                    ]),
                    ('VIII - Implementos', [
                        'Estado del balde/cuchara',
                        'Estado de cilindros hidráulicos',
                        'Estado de mangueras hidráulicas',
                        'Estado de brazos de levante',
                        'Sistema de acople rápido',
                    ]),
                    ('IX - Seguridad', [
                        'Extintor',
                        'Botiquín',
                        'Baliza',
                    ]),
                ],
            },
        ]

    def handle(self, *args, **options):
        self.stdout.write('Creando plantillas de checklists...')
        
        templates_data = self.get_templates_data()
        created_count = 0
        updated_count = 0
        total_items = 0
        
        for template_data in templates_data:
            sections = template_data.pop('sections')
            
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
                    # Delete existing items
                    template.items.all().delete()
                    self.stdout.write(self.style.WARNING(
                        f'↻ Actualizada: {template.code} - {template.name}'
                    ))
                
                # Create items from sections
                order = 1
                section_items = 0
                for section_name, questions in sections:
                    for question in questions:
                        ChecklistTemplateItem.objects.create(
                            template=template,
                            section=section_name,
                            order=order,
                            question=question,
                            response_type='yes_no_na',
                            required=True,
                            observations_allowed=True
                        )
                        order += 1
                        section_items += 1
                
                total_items += section_items
                self.stdout.write(f'  Items creados: {section_items}')
        
        self.stdout.write(self.style.SUCCESS(
            f'\n✓ Proceso completado.'
        ))
        self.stdout.write(f'  Plantillas creadas: {created_count}')
        self.stdout.write(f'  Plantillas actualizadas: {updated_count}')
        self.stdout.write(f'  Total plantillas: {ChecklistTemplate.objects.count()}')
        self.stdout.write(f'  Total items: {total_items}')
