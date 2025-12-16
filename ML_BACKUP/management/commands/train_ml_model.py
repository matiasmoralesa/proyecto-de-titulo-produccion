from django.core.management.base import BaseCommand
from apps.ml_predictions.data_generator import SyntheticDataGenerator
from apps.ml_predictions.model_trainer import FailurePredictionTrainer


class Command(BaseCommand):
    help = 'Entrena el modelo de prediccion de fallos con datos sinteticos'
    
    def add_arguments(self, parser):
        parser.add_argument('--samples', type=int, default=1000, help='Numero de muestras')
    
    def handle(self, *args, **options):
        num_samples = options['samples']
        self.stdout.write(self.style.SUCCESS('\n=== Entrenamiento del Modelo ML ===\n'))
        
        self.stdout.write('1. Generando datos sinteticos...')
        generator = SyntheticDataGenerator(num_samples=num_samples)
        data = generator.generate_training_data()
        self.stdout.write(self.style.SUCCESS(f'   OK {len(data)} muestras generadas\n'))
        
        self.stdout.write('2. Entrenando modelo Random Forest...')
        trainer = FailurePredictionTrainer()
        metrics = trainer.train(data)
        
        self.stdout.write(self.style.SUCCESS('\n3. Metricas del modelo:'))
        self.stdout.write(f'   Accuracy:  {metrics["accuracy"]:.3f}')
        self.stdout.write(f'   Precision: {metrics["precision"]:.3f}')
        self.stdout.write(f'   Recall:    {metrics["recall"]:.3f}')
        self.stdout.write(f'   F1 Score:  {metrics["f1_score"]:.3f}')
        self.stdout.write(f'   CV F1:     {metrics["cv_f1_mean"]:.3f} (+/- {metrics["cv_f1_std"]:.3f})\n')
        
        self.stdout.write('4. Importancia de features:')
        for feature, importance in sorted(metrics['feature_importance'].items(), key=lambda x: x[1], reverse=True):
            self.stdout.write(f'   {feature:30}: {importance:.3f}')
        
        self.stdout.write('\n5. Guardando modelo...')
        trainer.save_model()
        
        self.stdout.write(self.style.SUCCESS('\nModelo entrenado y guardado exitosamente!\n'))
