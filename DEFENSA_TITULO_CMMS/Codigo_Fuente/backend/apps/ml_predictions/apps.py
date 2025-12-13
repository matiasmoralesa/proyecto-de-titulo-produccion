from django.apps import AppConfig


class MlPredictionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.ml_predictions'
    verbose_name = 'ML Predictions'
    
    def ready(self):
        import apps.ml_predictions.signals
