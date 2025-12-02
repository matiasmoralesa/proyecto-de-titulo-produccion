"""
Generador de datos sintéticos para entrenamiento del modelo ML
"""
import random
from datetime import datetime, timedelta
from django.utils import timezone
import numpy as np


class SyntheticDataGenerator:
    """Genera datos sintéticos realistas para entrenamiento"""
    
    VEHICLE_TYPES = [
        'Camión Supersucker',
        'Camioneta MDO',
        'Retroexcavadora MDO',
        'Cargador Frontal MDO',
        'Minicargador MDO'
    ]
    
    FAILURE_TYPES = [
        'Motor',
        'Transmisión',
        'Sistema Hidráulico',
        'Sistema Eléctrico',
        'Frenos',
        'Neumáticos',
        'Sistema de Succión',
        'Bomba'
    ]
    
    def __init__(self, num_samples=1000):
        self.num_samples = num_samples
        random.seed(42)
        np.random.seed(42)
    
    def generate_training_data(self):
        """
        Genera datos de entrenamiento con patrones realistas
        
        Returns:
            list: Lista de diccionarios con features y target
        """
        data = []
        
        for i in range(self.num_samples):
            # Features básicas
            vehicle_type = random.choice(self.VEHICLE_TYPES)
            days_since_maintenance = random.randint(0, 365)
            operating_hours = random.randint(0, 5000)
            age_years = random.uniform(0, 15)
            failure_count_6m = random.randint(0, 10)
            maintenance_count_6m = random.randint(0, 12)
            
            # Patrones que aumentan probabilidad de fallo
            risk_score = 0
            
            # Días desde mantenimiento (peso alto)
            if days_since_maintenance > 180:
                risk_score += 30
            elif days_since_maintenance > 90:
                risk_score += 15
            elif days_since_maintenance > 60:
                risk_score += 5
            
            # Horas de operación
            if operating_hours > 3000:
                risk_score += 25
            elif operating_hours > 2000:
                risk_score += 15
            elif operating_hours > 1000:
                risk_score += 5
            
            # Edad del vehículo
            if age_years > 10:
                risk_score += 20
            elif age_years > 5:
                risk_score += 10
            
            # Historial de fallos
            risk_score += failure_count_6m * 5
            
            # Falta de mantenimiento
            if maintenance_count_6m < 2:
                risk_score += 15
            
            # Tipo de vehículo (algunos más propensos)
            if vehicle_type in ['Camión Supersucker', 'Retroexcavadora MDO']:
                risk_score += 10
            
            # Agregar ruido aleatorio
            risk_score += random.randint(-10, 10)
            
            # Determinar si hubo fallo (target)
            # Probabilidad basada en risk_score
            failure_probability = min(risk_score / 100, 0.95)
            will_fail = random.random() < failure_probability
            
            # Si va a fallar, determinar tipo y días hasta fallo
            if will_fail:
                failure_type = random.choice(self.FAILURE_TYPES)
                days_until_failure = max(1, int(np.random.exponential(30)))
            else:
                failure_type = None
                days_until_failure = None
            
            # Crear registro
            record = {
                'vehicle_type': vehicle_type,
                'days_since_last_maintenance': days_since_maintenance,
                'operating_hours': operating_hours,
                'age_years': age_years,
                'failure_count_last_6_months': failure_count_6m,
                'maintenance_count_last_6_months': maintenance_count_6m,
                'avg_maintenance_interval_days': (
                    180 / max(maintenance_count_6m, 1)
                ),
                'failure_rate': (
                    failure_count_6m / max(maintenance_count_6m, 1)
                ),
                'will_fail': 1 if will_fail else 0,
                'failure_type': failure_type,
                'days_until_failure': days_until_failure,
                'risk_score': risk_score
            }
            
            data.append(record)
        
        return data
    
    def generate_asset_data(self, asset):
        """
        Genera features para un activo real
        
        Args:
            asset: Instancia de Asset model
            
        Returns:
            dict: Features del activo
        """
        from apps.work_orders.models import WorkOrder
        from datetime import timedelta
        
        now = timezone.now()
        six_months_ago = now - timedelta(days=180)
        
        # Calcular features desde datos reales
        completed_work_orders = WorkOrder.objects.filter(
            asset=asset,
            status='completed',
            completed_date__gte=six_months_ago
        )
        
        maintenance_count = completed_work_orders.count()
        
        # Contar fallos (work orders con prioridad alta/crítica)
        failure_count = completed_work_orders.filter(
            priority__in=['high', 'critical']
        ).count()
        
        # Días desde último mantenimiento
        last_maintenance = completed_work_orders.order_by(
            '-completed_date'
        ).first()
        
        if last_maintenance:
            days_since_maintenance = (
                now - last_maintenance.completed_date
            ).days
        else:
            days_since_maintenance = 365  # Sin mantenimiento registrado
        
        # Edad del activo
        age_years = (
            (now.date() - asset.installation_date).days / 365.25
        )
        
        # Operating hours (estimado: 8 horas/día desde instalación)
        operating_hours = int(
            (now.date() - asset.installation_date).days * 8
        )
        
        features = {
            'vehicle_type': asset.vehicle_type,
            'days_since_last_maintenance': days_since_maintenance,
            'operating_hours': operating_hours,
            'age_years': age_years,
            'failure_count_last_6_months': failure_count,
            'maintenance_count_last_6_months': maintenance_count,
            'avg_maintenance_interval_days': (
                180 / max(maintenance_count, 1)
            ),
            'failure_rate': (
                failure_count / max(maintenance_count, 1)
            )
        }
        
        return features
