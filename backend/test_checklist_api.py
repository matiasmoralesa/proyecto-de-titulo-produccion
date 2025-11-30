"""
Script to test checklist API endpoints.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.checklists.models import ChecklistTemplate, ChecklistResponse
from apps.assets.models import Asset
from apps.authentication.models import User

def test_checklist_api():
    """Test checklist API functionality."""
    
    print("=" * 60)
    print("TESTING CHECKLIST API")
    print("=" * 60)
    
    # 1. Check templates
    print("\n1. Checking Checklist Templates...")
    templates = ChecklistTemplate.objects.all()
    print(f"   Total templates: {templates.count()}")
    
    for template in templates:
        print(f"   - {template.code}: {template.name}")
        print(f"     Vehicle Type: {template.get_vehicle_type_display()}")
        print(f"     Total Items: {template.total_items()}")
        print(f"     Required Items: {template.required_items_count()}")
        print(f"     Passing Score: {template.passing_score}%")
        print()
    
    # 2. Check if we have assets
    print("\n2. Checking Assets...")
    assets = Asset.objects.all()
    print(f"   Total assets: {assets.count()}")
    
    if assets.exists():
        asset = assets.first()
        print(f"   Sample Asset: {asset.name}")
        print(f"   Vehicle Type: {asset.get_vehicle_type_display()}")
        print(f"   License Plate: {asset.license_plate}")
        
        # Find matching template
        matching_templates = ChecklistTemplate.objects.filter(
            vehicle_type=asset.vehicle_type,
            is_active=True
        )
        print(f"   Matching Templates: {matching_templates.count()}")
        
        if matching_templates.exists():
            template = matching_templates.first()
            print(f"   Using Template: {template.code} - {template.name}")
    
    # 3. Check users
    print("\n3. Checking Users...")
    users = User.objects.all()
    print(f"   Total users: {users.count()}")
    
    if users.exists():
        user = users.first()
        print(f"   Sample User: {user.username}")
        print(f"   Role: {user.role.name}")
    
    # 4. Check existing checklist responses
    print("\n4. Checking Checklist Responses...")
    responses = ChecklistResponse.objects.all()
    print(f"   Total responses: {responses.count()}")
    
    if responses.exists():
        for response in responses[:5]:  # Show first 5
            print(f"   - ID: {response.id}")
            print(f"     Template: {response.template.code}")
            print(f"     Asset: {response.asset.name}")
            print(f"     Status: {response.get_status_display()}")
            print(f"     Score: {response.score}%")
            print(f"     Completed By: {response.completed_by.get_full_name() if response.completed_by else 'N/A'}")
            print(f"     Created: {response.created_at.strftime('%Y-%m-%d %H:%M')}")
            print()
    
    print("=" * 60)
    print("TEST COMPLETED")
    print("=" * 60)
    
    # Summary
    print("\n📊 SUMMARY:")
    print(f"   ✓ Templates: {templates.count()}")
    print(f"   ✓ Assets: {assets.count()}")
    print(f"   ✓ Users: {users.count()}")
    print(f"   ✓ Checklist Responses: {responses.count()}")
    
    # API Endpoints Available
    print("\n🔗 AVAILABLE API ENDPOINTS:")
    print("   GET    /api/v1/checklists/templates/")
    print("   GET    /api/v1/checklists/templates/{id}/")
    print("   GET    /api/v1/checklists/templates/{id}/items/")
    print("   GET    /api/v1/checklists/templates/by_vehicle_type/?vehicle_type=CAMION_SUPERSUCKER")
    print("   GET    /api/v1/checklists/responses/")
    print("   POST   /api/v1/checklists/responses/")
    print("   GET    /api/v1/checklists/responses/{id}/")
    print("   POST   /api/v1/checklists/responses/complete/")
    print("   POST   /api/v1/checklists/responses/{id}/add_item_response/")
    print("   POST   /api/v1/checklists/responses/{id}/finalize/")
    print("   GET    /api/v1/checklists/responses/{id}/download_pdf/")
    print("   GET    /api/v1/checklists/responses/my_checklists/")
    print("   GET    /api/v1/checklists/responses/by_asset/?asset_id=1")

if __name__ == '__main__':
    test_checklist_api()
