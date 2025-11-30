"""
Script to generate sample predictions for testing.
"""
import os
import django
import sys

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.ml_predictions.prediction_service import PredictionService
from apps.assets.models import Asset

def generate_predictions():
    """Generate predictions for all active assets."""
    print("=" * 60)
    print("  GENERATING FAILURE PREDICTIONS")
    print("=" * 60)
    print()
    
    # Get all active assets (Operando status)
    assets = Asset.objects.filter(status='Operando')
    print(f"Found {assets.count()} active assets")
    print()
    
    if assets.count() == 0:
        print("No active assets found. Please create some assets first.")
        return
    
    try:
        service = PredictionService()
        print(f"Using model: {service.model_record.model_name} v{service.model_record.model_version}")
        print()
        
        predictions = []
        for i, asset in enumerate(assets, 1):
            try:
                print(f"[{i}/{assets.count()}] Predicting for {asset.name} ({asset.serial_number})...", end=" ")
                prediction = service.predict_single_asset(asset.id)
                predictions.append(prediction)
                print(f"Risk: {prediction.risk_level} ({prediction.failure_probability:.1%})")
            except Exception as e:
                print(f"ERROR: {e}")
                continue
        
        print()
        print("=" * 60)
        print("  PREDICTION SUMMARY")
        print("=" * 60)
        print(f"\nTotal predictions: {len(predictions)}")
        
        # Count by risk level
        risk_counts = {}
        for pred in predictions:
            risk_counts[pred.risk_level] = risk_counts.get(pred.risk_level, 0) + 1
        
        print("\nRisk Level Distribution:")
        for risk_level in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
            count = risk_counts.get(risk_level, 0)
            print(f"  {risk_level}: {count}")
        
        # Show high-risk assets
        high_risk = [p for p in predictions if p.risk_level in ['CRITICAL', 'HIGH']]
        if high_risk:
            print(f"\nHigh-Risk Assets ({len(high_risk)}):")
            for pred in sorted(high_risk, key=lambda x: x.failure_probability, reverse=True):
                print(f"  - {pred.asset.name}: {pred.failure_probability:.1%} ({pred.risk_level})")
                print(f"    Days to failure: {pred.estimated_days_to_failure}")
                print(f"    Estimated cost: ${pred.estimated_repair_cost:,.2f}")
        
        print()
        print("Predictions generated successfully!")
        
    except ValueError as e:
        print(f"ERROR: {e}")
        print("\nPlease train a model first by running:")
        print("  python train_ml_model.py")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    generate_predictions()
