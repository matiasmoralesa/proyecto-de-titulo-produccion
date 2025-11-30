#!/usr/bin/env python
"""
Script to generate sample checklist responses for testing
"""
import os
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.checklists.models import ChecklistTemplate, ChecklistResponse, ChecklistItemResponse
from apps.assets.models import Asset
from apps.authentication.models import User

def generate_sample_checklists():
    """Generate sample checklist responses"""
    print("🚀 Generando checklists de ejemplo...")
    print("=" * 60)
    
    # Get available data
    templates = list(ChecklistTemplate.objects.all())
    assets = list(Asset.objects.all())
    users = list(User.objects.all())
    
    if not templates:
        print("❌ No hay plantillas disponibles")
        return
    
    if not assets:
        print("❌ No hay activos disponibles")
        return
        
    if not users:
        print("❌ No hay usuarios disponibles")
        return
    
    print(f"📋 Plantillas disponibles: {len(templates)}")
    print(f"🚛 Activos disponibles: {len(assets)}")
    print(f"👥 Usuarios disponibles: {len(users)}")
    print()
    
    # Generate 10 sample checklists
    created_count = 0
    
    for i in range(10):
        # Select random template and matching asset
        template = random.choice(templates)
        matching_assets = [a for a in assets if a.vehicle_type == template.vehicle_type]
        
        if not matching_assets:
            print(f"⚠️  No hay activos para plantilla {template.code}")
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
        
        print(f"✅ Checklist {i+1}: {template.code} - {asset.name} - {score}% - {checklist.get_status_display()}")
        created_count += 1
    
    print()
    print("=" * 60)
    print(f"🎉 Generados {created_count} checklists de ejemplo")
    
    # Show summary
    total_responses = ChecklistResponse.objects.count()
    by_status = {}
    for status_choice in ChecklistResponse.STATUS_CHOICES:
        status = status_choice[0]
        count = ChecklistResponse.objects.filter(status=status).count()
        by_status[status] = count
    
    print(f"\n📊 Resumen total:")
    print(f"   Total checklists: {total_responses}")
    for status, count in by_status.items():
        status_display = dict(ChecklistResponse.STATUS_CHOICES)[status]
        print(f"   {status_display}: {count}")
    
    print(f"\n🔗 Ve los resultados en: http://localhost:5173/checklists")

if __name__ == '__main__':
    generate_sample_checklists()
