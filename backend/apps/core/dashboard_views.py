"""
Dashboard views for providing system statistics
"""
import logging
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count, Q, Avg, F
from django.utils import timezone
from datetime import timedelta

from apps.assets.models import Asset
from apps.work_orders.models import WorkOrder
from apps.ml_predictions.models import FailurePrediction


from django.core.cache import cache

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """
    Get dashboard statistics (cached for 5 minutes)
    """
    # Try to get from cache
    cache_key = 'dashboard_stats'
    cached_data = cache.get(cache_key)
    
    if cached_data is not None:
        return Response(cached_data)
    
    # Asset stats
    total_assets = Asset.objects.count()
    operational_assets = Asset.objects.filter(status='OPERATIONAL').count()
    maintenance_assets = Asset.objects.filter(status='MAINTENANCE').count()
    stopped_assets = Asset.objects.filter(status='OUT_OF_SERVICE').count()
    
    # Work Order stats
    total_work_orders = WorkOrder.objects.count()
    pending_work_orders = WorkOrder.objects.filter(status='Pendiente').count()
    in_progress_work_orders = WorkOrder.objects.filter(status='En Progreso').count()
    completed_work_orders = WorkOrder.objects.filter(status='Completada').count()
    
    # ML Predictions stats
    total_predictions = FailurePrediction.objects.count()
    high_risk_predictions = FailurePrediction.objects.filter(
        risk_level__in=['HIGH', 'CRITICAL']
    ).count()
    
    # KPIs Calculation
    # 1. Asset Availability Rate (% of operational assets)
    availability_rate = (operational_assets / total_assets * 100) if total_assets > 0 else 0
    
    # 2. Work Order Completion Rate
    completion_rate = (completed_work_orders / total_work_orders * 100) if total_work_orders > 0 else 0
    
    # 3. Average Work Order Duration (for completed orders)
    completed_orders = WorkOrder.objects.filter(status='Completada', completed_date__isnull=False)
    avg_duration_days = 0
    if completed_orders.exists():
        valid_durations = []
        for order in completed_orders:
            # Validate that both dates exist
            if not order.completed_date or not order.created_at:
                logger.warning(
                    f"Work Order {order.work_order_number} (ID: {order.id}) has missing dates: "
                    f"completed_date={order.completed_date}, created_at={order.created_at}"
                )
                continue
            
            # Validate that completed_date is after created_at
            if order.completed_date < order.created_at:
                logger.warning(
                    f"Work Order {order.work_order_number} (ID: {order.id}) has invalid dates: "
                    f"completed_date ({order.completed_date}) is before created_at ({order.created_at})"
                )
                continue
            
            # Calculate duration and ensure it's non-negative
            duration = (order.completed_date - order.created_at).days
            if duration >= 0:
                valid_durations.append(duration)
            else:
                logger.warning(
                    f"Work Order {order.work_order_number} (ID: {order.id}) calculated negative duration: {duration} days"
                )
        
        # Calculate average only from valid durations
        avg_duration_days = sum(valid_durations) / len(valid_durations) if valid_durations else 0
        
        # Log data quality summary
        if completed_orders.count() > len(valid_durations):
            logger.info(
                f"KPI Calculation: {completed_orders.count() - len(valid_durations)} out of "
                f"{completed_orders.count()} completed work orders excluded due to invalid dates"
            )
    
    # 4. Preventive vs Corrective Maintenance Ratio
    # Since work_order_type field doesn't exist, we'll estimate based on priority
    # Low/Medium priority are likely preventive, High/Urgent are likely corrective
    preventive_orders = WorkOrder.objects.filter(priority__in=['Baja', 'Media']).count()
    corrective_orders = WorkOrder.objects.filter(priority__in=['Alta', 'Urgente']).count()
    preventive_ratio = (preventive_orders / (preventive_orders + corrective_orders) * 100) if (preventive_orders + corrective_orders) > 0 else 0
    
    # 5. Maintenance Backlog (pending + in progress)
    maintenance_backlog = pending_work_orders + in_progress_work_orders
    
    # 6. Critical Assets (high risk predictions)
    critical_assets_count = high_risk_predictions
    
    # 7. Work Orders This Month
    first_day_of_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    work_orders_this_month = WorkOrder.objects.filter(created_at__gte=first_day_of_month).count()
    
    # 8. Prediction Accuracy (if we have actual failure data)
    predictions_with_outcome = FailurePrediction.objects.filter(actual_failure_occurred__isnull=False)
    prediction_accuracy = 0
    if predictions_with_outcome.exists():
        accurate_predictions = predictions_with_outcome.filter(
            Q(actual_failure_occurred=True, risk_level__in=['HIGH', 'CRITICAL']) |
            Q(actual_failure_occurred=False, risk_level__in=['LOW', 'MEDIUM'])
        ).count()
        prediction_accuracy = (accurate_predictions / predictions_with_outcome.count() * 100)
    
    data = {
        'total_assets': total_assets,
        'operational_assets': operational_assets,
        'maintenance_assets': maintenance_assets,
        'stopped_assets': stopped_assets,
        'total_work_orders': total_work_orders,
        'pending_work_orders': pending_work_orders,
        'in_progress_work_orders': in_progress_work_orders,
        'completed_work_orders': completed_work_orders,
        'total_predictions': total_predictions,
        'high_risk_predictions': high_risk_predictions,
        # KPIs
        'kpis': {
            'availability_rate': round(availability_rate, 1),
            'completion_rate': round(completion_rate, 1),
            'avg_duration_days': round(avg_duration_days, 1),
            'preventive_ratio': round(preventive_ratio, 1),
            'maintenance_backlog': maintenance_backlog,
            'critical_assets_count': critical_assets_count,
            'work_orders_this_month': work_orders_this_month,
            'prediction_accuracy': round(prediction_accuracy, 1),
        }
    }
    
    # Cache for 5 minutes
    cache.set(cache_key, data, 300)
    
    return Response(data)
