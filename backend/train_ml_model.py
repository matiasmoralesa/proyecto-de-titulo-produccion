"""
Script to train the failure prediction ML model.
Run this script to train a new model with current data.
"""
import os
import django
import sys

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.ml_predictions.model_trainer import train_failure_prediction_model

if __name__ == '__main__':
    print("=" * 60)
    print("  FAILURE PREDICTION MODEL TRAINING")
    print("=" * 60)
    print()
    
    try:
        model = train_failure_prediction_model()
        
        print()
        print("=" * 60)
        print("  TRAINING COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print(f"\nModel ID: {model.id}")
        print(f"Version: {model.model_version}")
        print(f"Accuracy: {model.accuracy:.2%}")
        print(f"Precision: {model.precision:.2%}")
        print(f"Recall: {model.recall:.2%}")
        print(f"F1 Score: {model.f1_score:.2%}")
        print(f"\nModel is now active and ready for predictions!")
        
    except Exception as e:
        print()
        print("=" * 60)
        print("  TRAINING FAILED!")
        print("=" * 60)
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
