"""
Management command para ejecutar predicciones en todos los activos activos
"""
from django.core.management.base import BaseCommand
from apps.assets.models import Asset
from apps.ml_predictions.prediction_service import PredictionService


class Command(BaseCommand):
    help = 'Ejecuta predicciones ML para todos los activos activos'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--asset-id',
            type=str,
            help='ID de un activo específico (opcional)'
        )
        parser.add_argument(
            '--vehicle-type',
            type=str,
            help='Filtrar por tipo de vehículo'
        )
    
    def handle(self, *args, **options):
        asset_id = options.get('asset_id')
        vehicle_type = options.get('vehicle_type')
        
        self.stdout.write(
            self.style.SUCCESS('\n=== Ejecución de Predicciones ML ===\n')
        )
        
        # Filtrar activos
        if asset_id:
            assets = Asset.objects.filter(id=asset_id, is_archived=False)
            if not assets.exists():
                self.stdout.write(
                    self.style.ERROR(f'Activo {asset_id} no encontrado')
                )
                return
        else:
            assets = Asset.objects.filter(
                is_archived=False,
                status__in=['Operando', 'En Mantenimiento']
            )
            
            if vehicle_type:
                assets = assets.filter(vehicle_type=vehicle_type)
        
        total_assets = assets.count()
        self.stdout.write(f'Activos a analizar: {total_assets}\n')
        
        if total_assets == 0:
            self.stdout.write(self.style.WARNING('No hay activos para analizar'))
            return
        
        # Ejecutar predicciones
        prediction_service = PredictionService()
        
        predictions_created = 0
        high_risk_count = 0
        errors = 0
        
        for i, asset in enumerate(assets, 1):
            try:
                self.stdout.write(
                    f'[{i}/{total_assets}] Analizando: {asset.name}...',
                    ending=''
                )
                
                prediction = prediction_service.predict_single_asset(asset)
                predictions_created += 1
                
                if prediction.risk_level in ['high', 'critical']:
                    high_risk_count += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f' ⚠️  {prediction.risk_level.upper()} '
                            f'({prediction.failure_probability:.1%})'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f' ✓ {prediction.risk_level} '
                            f'({prediction.failure_probability:.1%})'
                        )
                    )
            
            except Exception as e:
                errors += 1
                self.stdout.write(
                    self.style.ERROR(f' ✗ Error: {str(e)}')
                )
        
        # Resumen
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('\nResumen:'))
        self.stdout.write(f'  Total predicciones: {predictions_created}')
        self.stdout.write(
            self.style.WARNING(f'  Alto riesgo: {high_risk_count}')
        )
        if errors > 0:
            self.stdout.write(self.style.ERROR(f'  Errores: {errors}'))
        
        self.stdout.write(
            self.style.SUCCESS('\n✓ Predicciones completadas!\n')
        )
