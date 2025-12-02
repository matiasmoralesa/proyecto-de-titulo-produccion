"""
Script para eliminar modelo viejo y reentrenar desde cero.
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.ml_predictions.model_trainer import FailurePredictionTrainer
from apps.ml_predictions.data_generator import SyntheticDataGenerator
import pandas as pd

def main():
    print("=" * 60)
    print("  LIMPIEZA Y REENTRENAMIENTO DEL MODELO ML")
    print("=" * 60)
    print()
    
    try:
        # Paso 1: Eliminar modelos viejos
        print("🗑️  Eliminando modelos viejos...")
        trainer = FailurePredictionTrainer()
        
        if os.path.exists(trainer.model_path):
            os.remove(trainer.model_path)
            print(f"  ✓ Eliminado: {trainer.model_path}")
        
        if os.path.exists(trainer.encoders_path):
            os.remove(trainer.encoders_path)
            print(f"  ✓ Eliminado: {trainer.encoders_path}")
        
        # Paso 2: Generar datos sintéticos
        print("\n📊 Generando datos de entrenamiento...")
        generator = SyntheticDataGenerator(num_samples=2000)
        data = generator.generate_training_data()
        
        print(f"  ✓ {len(data)} muestras generadas")
        
        # Mostrar distribución
        df = pd.DataFrame(data)
        print(f"\n📋 Tipos de vehículos en los datos:")
        print(df['vehicle_type'].value_counts())
        
        # Paso 3: Entrenar modelo
        print("\n🤖 Entrenando modelo...")
        metrics = trainer.train(data)
        
        print("\n" + "=" * 60)
        print("  ✅ ENTRENAMIENTO COMPLETADO")
        print("=" * 60)
        print(f"\n📊 Métricas del modelo:")
        print(f"  • Accuracy:  {metrics['accuracy']:.3f}")
        print(f"  • Precision: {metrics['precision']:.3f}")
        print(f"  • Recall:    {metrics['recall']:.3f}")
        print(f"  • F1 Score:  {metrics['f1_score']:.3f}")
        
        print(f"\n💾 Modelo guardado en:")
        print(f"  {trainer.model_path}")
        print(f"  {trainer.encoders_path}")
        
        return 0
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("  ❌ ERROR")
        print("=" * 60)
        print(f"\n{str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
