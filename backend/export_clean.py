"""
Export data with clean UTF-8 encoding (no BOM)
"""
import os
import sys
import django
import subprocess

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

models = [
    ('authentication.Role', 'roles_export.json'),
    ('checklists.ChecklistTemplate', 'checklist_templates_export.json'),
    ('configuration.Priority', 'priorities_export.json'),
    ('configuration.WorkOrderType', 'workorder_types_export.json'),
    ('configuration.AssetCategory', 'asset_categories_export.json'),
    ('assets.Location', 'locations_export.json'),
]

for model, filename in models:
    print(f"Exporting {model}...")
    result = subprocess.run(
        [sys.executable, 'manage.py', 'dumpdata', model, '--indent', '2'],
        capture_output=True,
        text=False  # Get bytes
    )
    
    # Write as UTF-8 without BOM
    with open(filename, 'wb') as f:
        f.write(result.stdout)
    
    print(f"  ✅ {filename}")

print("\n✅ All files exported successfully!")
