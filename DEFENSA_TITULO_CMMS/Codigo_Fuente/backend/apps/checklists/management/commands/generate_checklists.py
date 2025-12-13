from django.core.management.base import BaseCommand
from apps.checklists.models import ChecklistTemplate, ChecklistResponse, ChecklistItemResponse
from apps.assets.models import Asset
from apps.authentication.models import User
import random
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Generate sample checklist responses'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of checklists to generate'
        )

    def handle(self, *args, **options):
        count = options['count']
        
        self.stdout.write("🚀 Generando checklists de ejemplo...")
        self.stdout.write("=" * 60)
        
        # Get available data
        templates = list(ChecklistTemplate.objects.all())
        assets = list(Asset.objects.all())
        users = list(User.objects.all())
        
        if not templates:
            self.stdout.write(self.style.ERROR("❌ No hay plantillas disponibles"))
            return
        
        if not assets:
            self.stdout.write(self.style.ERROR("❌ No hay activos disponibles"))
            return
            
        if not users:
            self.stdout.write(self.style.ERROR("❌ No hay usuarios disponibles"))
            return
        
        self.stdout.write(f"📋 Plantillas disponibles: {len(templates)}")
        self.stdout.write(f"🚛 Activos disponibles: {len(assets)}")
        self.stdout.write(f"👥 Usuarios disponibles: {len(users)}")
        self.stdout.write("")
        
        # Generate sample checklists
        created_count = 0
        
        for i in range(count):
            # Select random template and matching asset
            template = random.choice(templates)
            matching_assets = [a for a in assets if a.vehicle_type == template.vehicle_type]
            
            if not matching_assets:
                self.stdout.write(self.style.WARNING(f"⚠️  No hay activos para plantilla {template.code}"))
                continue
                
            asset = random.choice(matching_assets)
            user = random.choice(users)
            
            # Create checklist response
            checklist = ChecklistResponse.objects.create(
                template=template,
                asset=asset,
                completed_by=user,
                status=random.choice(['COMPLETED', 'APPROVED', 'REJECTED']),
                signature_data='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=='
            )
            
            # Set random completion date (last 30 days)
            days_ago = random.randint(1, 30)
            checklist.completed_at = datetime.now() - timedelta(days=days_ago)
            
            # Generate responses for all items
            total_items = 0
            positive_responses = 0
            
            for item in template.items.all():
                total_items += 1
                
                if item.response_type == 'yes_no_na':
                    # 80% chance of positive response
                    if random.random() < 0.8:
                        response_value = 'yes'
                        positive_responses += 1
                    elif random.random() < 0.9:
                        response_value = 'no'
                    else:
                        response_value = 'na'
                        positive_responses += 0.5  # NA counts as half positive
                elif item.response_type == 'text':
                    response_value = random.choice([
                        'Correcto', 'En buen estado', 'Funcionando', 'OK',
                        'Necesita revisión', 'Regular', 'Aceptable'
                    ])
                    positive_responses += 1
                elif item.response_type == 'numeric':
                    response_value = str(random.randint(50, 100))
                    positive_responses += 1
                else:
                    response_value = 'OK'
                    positive_responses += 1
                
                # Add observations sometimes
                observations = ''
                if random.random() < 0.3:  # 30% chance of observations
                    observations = random.choice([
                        'Todo en orden',
                        'Requiere limpieza menor',
                        'Funcionamiento normal',
                        'Sin novedades',
                        'Revisar en próxima inspección',
                        'Desgaste normal por uso'
                    ])
                
                ChecklistItemResponse.objects.create(
                    checklist_response=checklist,
                    template_item=item,
                    response_value=response_value,
                    observations=observations
                )
            
            # Calculate score
            if total_items > 0:
                score = int((positive_responses / total_items) * 100)
                checklist.score = score
                
                # Adjust status based on score
                if score >= template.passing_score:
                    if checklist.status == 'REJECTED':
                        checklist.status = random.choice(['COMPLETED', 'APPROVED'])
                else:
                    if checklist.status == 'APPROVED':
                        checklist.status = random.choice(['COMPLETED', 'REJECTED'])
            
            checklist.save()
            
            self.stdout.write(self.style.SUCCESS(
                f"✅ Checklist {i+1}: {template.code} - {asset.name} - {score}% - {checklist.get_status_display()}"
            ))
            created_count += 1
        
        self.stdout.write("")
        self.stdout.write("=" * 60)
        self.stdout.write(self.style.SUCCESS(f"🎉 Generados {created_count} checklists de ejemplo"))
        
        # Show summary
        total_responses = ChecklistResponse.objects.count()
        by_status = {}
        for status_choice in ChecklistResponse.STATUSES:
            status = status_choice[0]
            count = ChecklistResponse.objects.filter(status=status).count()
            by_status[status] = count
        
        self.stdout.write("\n📊 Resumen total:")
        self.stdout.write(f"   Total checklists: {total_responses}")
        for status, count in by_status.items():
            status_display = dict(ChecklistResponse.STATUSES)[status]
            self.stdout.write(f"   {status_display}: {count}")
        
        self.stdout.write("\n🔗 Ve los resultados en: http://localhost:5173/checklists")
