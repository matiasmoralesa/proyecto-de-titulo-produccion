"""
Feature engineering service for ML predictions.
Extracts and transforms features from asset data.
"""
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Count, Avg, Sum, Max, Min
import pandas as pd
import numpy as np

from apps.assets.models import Asset
from apps.work_orders.models import WorkOrder
from apps.machine_status.models import AssetStatus, AssetStatusHistory
from apps.maintenance.models import MaintenancePlan


class FeatureEngineer:
    """
    Extracts features from asset data for ML model training and inference.
    """
    
    def __init__(self, lookback_days=180):
        """
        Initialize feature engineer.
        
        Args:
            lookback_days: Number of days to look back for historical data
        """
        self.lookback_days = lookback_days
        self.feature_names = []
    
    def extract_features_for_asset(self, asset, reference_date=None):
        """
        Extract all features for a single asset.
        
        Args:
            asset: Asset instance
            reference_date: Date to use as reference (default: now)
        
        Returns:
            dict: Feature dictionary
        """
        if reference_date is None:
            reference_date = timezone.now()
        
        features = {}
        
        # Asset basic features
        features.update(self._extract_asset_features(asset, reference_date))
        
        # Time-based features
        features.update(self._extract_time_features(asset, reference_date))
        
        # Operational features
        features.update(self._extract_operational_features(asset, reference_date))
        
        # Historical features
        features.update(self._extract_historical_features(asset, reference_date))
        
        # Status features
        features.update(self._extract_status_features(asset, reference_date))
        
        return features
    
    def extract_features_for_all_assets(self, reference_date=None):
        """
        Extract features for all active assets.
        
        Returns:
            pd.DataFrame: Features dataframe
        """
        assets = Asset.objects.filter(is_archived=False)
        
        features_list = []
        asset_ids = []
        
        for asset in assets:
            try:
                features = self.extract_features_for_asset(asset, reference_date)
                features_list.append(features)
                asset_ids.append(str(asset.id))
            except Exception as e:
                print(f"Error extracting features for {asset.name}: {e}")
                continue
        
        if not features_list:
            return pd.DataFrame()
        
        df = pd.DataFrame(features_list)
        df['asset_id'] = asset_ids
        
        return df
    
    def _extract_asset_features(self, asset, reference_date):
        """Extract basic asset characteristics."""
        features = {}
        
        # Asset age in days
        installation_date = asset.installation_date
        if isinstance(installation_date, str):
            installation_date = datetime.strptime(installation_date, '%Y-%m-%d').date()
        
        features['asset_age_days'] = (reference_date.date() - installation_date).days
        
        # Vehicle type (one-hot encoding)
        vehicle_types = [
            'Camión Supersucker',
            'Camioneta MDO',
            'Retroexcavadora MDO',
            'Cargador Frontal MDO',
            'Minicargador MDO'
        ]
        
        for vtype in vehicle_types:
            features[f'vehicle_type_{vtype.replace(" ", "_")}'] = 1 if asset.vehicle_type == vtype else 0
        
        return features
    
    def _extract_time_features(self, asset, reference_date):
        """Extract time-based features."""
        features = {}
        cutoff_date = reference_date - timedelta(days=self.lookback_days)
        
        # Days since last maintenance
        last_maintenance = WorkOrder.objects.filter(
            asset=asset,
            status='COMPLETED',
            completed_date__isnull=False
        ).order_by('-completed_date').first()
        
        if last_maintenance and last_maintenance.completed_date:
            days_since = (reference_date - last_maintenance.completed_date).days
            features['days_since_last_maintenance'] = days_since
        else:
            features['days_since_last_maintenance'] = 9999  # Large number if never maintained
        
        # Days since last failure (work order with HIGH/CRITICAL priority)
        last_failure = WorkOrder.objects.filter(
            asset=asset,
            priority__in=['HIGH', 'CRITICAL'],
            status='COMPLETED'
        ).order_by('-completed_date').first()
        
        if last_failure and last_failure.completed_date:
            days_since = (reference_date - last_failure.completed_date).days
            features['days_since_last_failure'] = days_since
        else:
            features['days_since_last_failure'] = 9999
        
        # Maintenance frequency (per month)
        maintenance_count = WorkOrder.objects.filter(
            asset=asset,
            status='COMPLETED',
            completed_date__gte=cutoff_date
        ).count()
        
        months = self.lookback_days / 30.0
        features['maintenance_frequency_per_month'] = maintenance_count / months if months > 0 else 0
        
        return features
    
    def _extract_operational_features(self, asset, reference_date):
        """Extract operational metrics."""
        features = {}
        cutoff_date = reference_date - timedelta(days=self.lookback_days)
        
        # Current odometer reading
        try:
            current_status = AssetStatus.objects.get(asset=asset)
            odometer = current_status.odometer_reading
            fuel = current_status.fuel_level
            
            features['current_odometer'] = float(odometer) if odometer is not None else 0.0
            features['current_fuel_level'] = float(fuel) if fuel is not None else 0.0
        except AssetStatus.DoesNotExist:
            features['current_odometer'] = 0.0
            features['current_fuel_level'] = 0.0
        except (ValueError, TypeError):
            features['current_odometer'] = 0.0
            features['current_fuel_level'] = 0.0
        
        # Odometer rate of change (km/day)
        try:
            status_history = AssetStatusHistory.objects.filter(
                asset=asset,
                timestamp__gte=cutoff_date,
                odometer_reading__isnull=False
            ).order_by('timestamp')
            
            if status_history.count() >= 2:
                first = status_history.first()
                last = status_history.last()
                days_diff = (last.timestamp - first.timestamp).days
                odometer_diff = float(last.odometer_reading) - float(first.odometer_reading)
                
                if days_diff > 0 and odometer_diff >= 0:
                    features['odometer_rate_of_change'] = odometer_diff / days_diff
                else:
                    features['odometer_rate_of_change'] = 0.0
            else:
                features['odometer_rate_of_change'] = 0.0
        except (ValueError, TypeError, AttributeError):
            features['odometer_rate_of_change'] = 0.0
        
        # Average fuel level (last 7 days)
        recent_cutoff = reference_date - timedelta(days=7)
        avg_fuel = AssetStatusHistory.objects.filter(
            asset=asset,
            timestamp__gte=recent_cutoff,
            fuel_level__isnull=False
        ).aggregate(avg=Avg('fuel_level'))
        
        features['avg_fuel_level_7d'] = avg_fuel['avg'] or 0
        
        # Status change frequency
        status_changes = AssetStatusHistory.objects.filter(
            asset=asset,
            timestamp__gte=cutoff_date
        ).count()
        
        features['status_change_frequency'] = status_changes / (self.lookback_days / 30.0)
        
        return features
    
    def _extract_historical_features(self, asset, reference_date):
        """Extract historical performance features."""
        features = {}
        cutoff_date = reference_date - timedelta(days=self.lookback_days)
        
        # Total work orders
        work_orders = WorkOrder.objects.filter(
            asset=asset,
            created_at__gte=cutoff_date
        )
        
        features['total_work_orders'] = work_orders.count()
        
        # Completed work orders
        completed_wo = work_orders.filter(status='COMPLETED')
        features['completed_work_orders'] = completed_wo.count()
        
        # High priority work orders (potential failures)
        high_priority_wo = work_orders.filter(priority__in=['HIGH', 'CRITICAL'])
        features['high_priority_work_orders'] = high_priority_wo.count()
        
        # Total maintenance hours
        total_hours = completed_wo.aggregate(total=Sum('actual_hours'))
        features['total_maintenance_hours'] = float(total_hours['total'] or 0)
        
        # Average repair time
        avg_hours = completed_wo.aggregate(avg=Avg('actual_hours'))
        features['avg_repair_time_hours'] = float(avg_hours['avg'] or 0)
        
        # Failure rate (high priority WOs per 1000 km)
        if features['current_odometer'] > 0:
            features['failure_rate_per_1000km'] = (features['high_priority_work_orders'] / features['current_odometer']) * 1000
        else:
            features['failure_rate_per_1000km'] = 0
        
        return features
    
    def _extract_status_features(self, asset, reference_date):
        """Extract status-related features."""
        features = {}
        cutoff_date = reference_date - timedelta(days=self.lookback_days)
        
        # Count of each status type
        status_counts = AssetStatusHistory.objects.filter(
            asset=asset,
            timestamp__gte=cutoff_date
        ).values('status_type').annotate(count=Count('id'))
        
        status_dict = {item['status_type']: item['count'] for item in status_counts}
        
        features['count_operando'] = status_dict.get('OPERANDO', 0)
        features['count_detenida'] = status_dict.get('DETENIDA', 0)
        features['count_en_mantenimiento'] = status_dict.get('EN_MANTENIMIENTO', 0)
        features['count_fuera_servicio'] = status_dict.get('FUERA_DE_SERVICIO', 0)
        
        # Percentage of time in each status
        total_status_changes = sum(status_dict.values())
        if total_status_changes > 0:
            features['pct_operando'] = (features['count_operando'] / total_status_changes) * 100
            features['pct_detenida'] = (features['count_detenida'] / total_status_changes) * 100
            features['pct_en_mantenimiento'] = (features['count_en_mantenimiento'] / total_status_changes) * 100
            features['pct_fuera_servicio'] = (features['count_fuera_servicio'] / total_status_changes) * 100
        else:
            features['pct_operando'] = 0
            features['pct_detenida'] = 0
            features['pct_en_mantenimiento'] = 0
            features['pct_fuera_servicio'] = 0
        
        # Health score (0-100)
        # Simple heuristic: based on maintenance compliance and failure rate
        health_score = 100.0
        
        # Penalize for high failure rate
        if features['failure_rate_per_1000km'] > 0.1:
            health_score -= 20
        
        # Penalize for overdue maintenance
        if features['days_since_last_maintenance'] > 90:
            health_score -= 30
        
        # Penalize for low fuel
        if features['current_fuel_level'] < 25:
            health_score -= 10
        
        # Penalize for frequent status changes (instability)
        if features['status_change_frequency'] > 10:
            health_score -= 15
        
        features['health_score'] = max(0, min(100, health_score))
        
        return features
    
    def get_feature_names(self):
        """Get list of all feature names."""
        # Generate a sample to get feature names
        sample_asset = Asset.objects.filter(is_archived=False).first()
        if sample_asset:
            features = self.extract_features_for_asset(sample_asset)
            return list(features.keys())
        return []
