import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.ml_predictions.models import FailurePrediction

count = FailurePrediction.objects.count()
print(f'Predicciones en BD: {count}')

if count > 0:
    print('\nÚltimas 3 predicciones:')
    for p in FailurePrediction.objects.all()[:3]:
        print(f'  - {p.asset.name}: {p.risk_level} ({p.failure_probability:.1%})')
