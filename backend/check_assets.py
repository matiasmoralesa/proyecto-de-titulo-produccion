"""Check assets in database."""
import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.assets.models import Asset

assets = Asset.objects.all()
print(f"Total assets: {assets.count()}")
print(f"Active assets: {Asset.objects.filter(status='ACTIVE').count()}")
print(f"\nStatuses: {list(Asset.objects.values_list('status', flat=True).distinct())}")

if assets.count() > 0:
    print(f"\nFirst 5 assets:")
    for asset in assets[:5]:
        print(f"  - {asset.name} ({asset.code}) - Status: {asset.status}")
