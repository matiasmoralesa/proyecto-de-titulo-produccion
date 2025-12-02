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
    Get dashboard statistics filtered by user role.
    
    - ADMIN: See all system data
    - SUPERVISOR: See team data (currently all data, can be filtered by department)
    - OPERADOR: See only their own assigned data
    """
    user = request.user
    
    # Cache key includes user role and ID for role-based caching
    cache_key = f'dashboard_stats_{user.role.name}_{user.id}'
    cached_data = cache.get(cache_key)
    
    if cached_data is not None:
        return Response(cached_data)
    
    # Get role name for filtering
    from apps.authentication.models import Role
    role_name = user.role.name
    
    # Filter querysets based on role
    if role_name == Role.ADMIN:
        # Admins see everything
        assets_qs = Asset.objects.all()
        work_orders_qs = WorkOrder.objects.all()
        predictions_qs = FailurePrediction.objects.all()
    elif role_name == Role.SUPERVISOR:
        # Supervisors see all (can be filtered by department/area in production)
        assets_qs = Asset.objects.all()
        work_orders_qs = WorkOrder.objects.all()
        predictions_qs = FailurePrediction.objects.all()
    elif role_name == Role.OPERADOR:
        # Operators only see their assigned work orders and related assets
        work_orders_qs = WorkOrder.objects.filter(assigned_to=user)
        
        # Get assets from assigned work orders
        assigned_asset_ids = work_orders_qs.values_list('asset_id', flat=True).distinct()
        assets_qs = Asset.objects.filter(id__in=assigned_asset_ids)
        
        # Get predictions for accessible assets
        predictions_qs = FailurePrediction.objects.filter(asset_id__in=assigned_asset_ids)
    else:
        # Unknown role - return empty data
        assets_qs = Asset.objects.none()
        work_orders_qs = WorkOrder.objects.none()
        predictions_qs = FailurePrediction.objects.none()
    
    # Asset stats
    total_assets = assets_qs.count()
    operational_assets = assets_qs.filter(status='OPERATIONAL').count()
    maintenance_assets = assets_qs.filter(status='MAINTENANCE').count()
    stopped_assets = assets_qs.filter(status='OUT_OF_SERVICE').count()
    
    # Work Order stats
    total_work_orders = work_orders_qs.count()
    pending_work_orders = work_orders_qs.filter(status='Pendiente').count()
    in_progress_work_orders = work_orders_qs.filter(status='En Progreso').count()
    completed_work_orders = work_orders_qs.filter(status='Completada').count()
    
    # ML Predictions stats
    total_predictions = predictions_qs.count()
    high_risk_predictions = predictions_qs.filter(
        risk_level__in=['HIGH', 'CRITICAL']
    ).count()
    
    # KPIs Calculation
    # 1. Asset Availability Rate (% of operational assets)
    availability_rate = (operational_assets / total_assets * 100) if total_assets > 0 else 0
    
    # 2. Work Order Completion Rate
    completion_rate = (completed_work_orders / total_work_orders * 100) if total_work_orders > 0 else 0
    
    # 3. Average Work Order Duration (for completed orders)
    completed_orders = work_orders_qs.filter(status='Completada', completed_date__isnull=False)
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
    preventive_orders = work_orders_qs.filter(priority__in=['Baja', 'Media']).count()
    corrective_orders = work_orders_qs.filter(priority__in=['Alta', 'Urgente']).count()
    preventive_ratio = (preventive_orders / (preventive_orders + corrective_orders) * 100) if (preventive_orders + corrective_orders) > 0 else 0
    
    # 5. Maintenance Backlog (pending + in progress)
    maintenance_backlog = pending_work_orders + in_progress_work_orders
    
    # 6. Critical Assets (high risk predictions)
    critical_assets_count = high_risk_predictions
    
    # 7. Work Orders This Month
    first_day_of_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    work_orders_this_month = work_orders_qs.filter(created_at__gte=first_day_of_month).count()
    
    # 8. Prediction Accuracy (if we have actual failure data)
    predictions_with_outcome = predictions_qs.filter(actual_failure_occurred__isnull=False)
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
