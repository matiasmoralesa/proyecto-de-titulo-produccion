"""
Services for report generation and KPI calculations.
"""
from datetime import datetime, timedelta
from django.db.models import Count, Avg, Sum, Q, F, ExpressionWrapper, DurationField
from django.utils import timezone
from apps.work_orders.models import WorkOrder
from apps.assets.models import Asset
from apps.inventory.models import SparePart, StockMovement
from apps.maintenance.models import MaintenancePlan


class ReportService:
    """Service for generating reports and calculating KPIs."""
    
    @staticmethod
    def calculate_mtbf(asset_id=None, start_date=None, end_date=None, user_id=None):
        """
        Calculate Mean Time Between Failures (MTBF).
        MTBF = Total Operating Time / Number of Failures
        """
        filters = Q(status=WorkOrder.STATUS_COMPLETED)
        
        if asset_id:
            filters &= Q(asset_id=asset_id)
        
        if start_date:
            filters &= Q(completed_date__gte=start_date)
        
        if end_date:
            filters &= Q(completed_date__lte=end_date)
        
        if user_id:
            filters &= Q(assigned_to_id=user_id)
        
        # Get completed work orders (as failures proxy)
        failures = WorkOrder.objects.filter(filters).count()
        
        if failures == 0:
            return None
        
        # Calculate total operating time (in hours)
        # For simplicity, we'll use the time range
        if start_date and end_date:
            total_hours = (end_date - start_date).total_seconds() / 3600
        else:
            # Default to 30 days if no range specified
            total_hours = 30 * 24
        
        mtbf = total_hours / failures if failures > 0 else 0
        return round(mtbf, 2)
    
    @staticmethod
    def calculate_mttr(asset_id=None, start_date=None, end_date=None, user_id=None):
        """
        Calculate Mean Time To Repair (MTTR).
        MTTR = Total Repair Time / Number of Repairs
        """
        filters = Q(status=WorkOrder.STATUS_COMPLETED)
        
        if asset_id:
            filters &= Q(asset_id=asset_id)
        
        if user_id:
            filters &= Q(assigned_to_id=user_id)
        
        if start_date:
            filters &= Q(completed_date__gte=start_date)
        
        if end_date:
            filters &= Q(completed_date__lte=end_date)
        
        # Get average hours worked on completed work orders
        avg_hours = WorkOrder.objects.filter(filters).aggregate(
            avg_hours=Avg('actual_hours')
        )['avg_hours']
        
        return round(avg_hours, 2) if avg_hours else 0
    
    @staticmethod
    def calculate_oee(asset_id=None, start_date=None, end_date=None, user_id=None):
        """
        Calculate Overall Equipment Effectiveness (OEE).
        OEE = Availability × Performance × Quality
        
        Simplified calculation:
        Availability = (Total Time - Downtime) / Total Time
        """
        filters = Q()
        
        if asset_id:
            filters &= Q(asset_id=asset_id)
        
        if start_date:
            filters &= Q(created_at__gte=start_date)
        
        if end_date:
            filters &= Q(created_at__lte=end_date)
        
        if user_id:
            filters &= Q(assigned_to_id=user_id)
        
        # Calculate total downtime from work orders
        downtime_hours = WorkOrder.objects.filter(
            filters,
            status=WorkOrder.STATUS_COMPLETED
        ).aggregate(
            total_downtime=Sum('actual_hours')
        )['total_downtime']
        
        # Convert to float
        downtime_hours = float(downtime_hours) if downtime_hours else 0.0
        
        # Calculate total available time
        if start_date and end_date:
            total_hours = (end_date - start_date).total_seconds() / 3600
        else:
            total_hours = 30 * 24  # Default 30 days
        
        # Availability calculation
        availability = ((total_hours - downtime_hours) / total_hours) * 100 if total_hours > 0 else 0
        
        # Simplified OEE (assuming 100% performance and quality for now)
        oee = availability
        
        return round(oee, 2)
    
    @staticmethod
    def get_work_order_summary(start_date=None, end_date=None, asset_id=None, user_id=None):
        """Generate work order summary report."""
        filters = Q()
        
        if user_id:
            filters &= Q(assigned_to_id=user_id)
        
        if start_date:
            filters &= Q(created_at__gte=start_date)
        
        if end_date:
            filters &= Q(created_at__lte=end_date)
        
        if asset_id:
            filters &= Q(asset_id=asset_id)
        
        # Get work orders
        work_orders = WorkOrder.objects.filter(filters)
        
        # Summary statistics
        summary = {
            'total': work_orders.count(),
            'by_status': {},
            'by_priority': {},
            'by_type': {},
            'avg_completion_time': 0,
            'total_hours_worked': 0,
        }
        
        # Count by status
        for status_choice in WorkOrder.STATUS_CHOICES:
            status = status_choice[0]
            count = work_orders.filter(status=status).count()
            summary['by_status'][status] = {
                'count': count,
                'label': status_choice[1]
            }
        
        # Count by priority
        for priority_choice in WorkOrder.PRIORITY_CHOICES:
            priority = priority_choice[0]
            count = work_orders.filter(priority=priority).count()
            summary['by_priority'][priority] = {
                'count': count,
                'label': priority_choice[1]
            }
        
        # Count by type - Skip since work_order_type doesn't exist in this model
        # summary['by_type'] will remain empty
        
        # Calculate average completion time
        completed_orders = work_orders.filter(
            status=WorkOrder.STATUS_COMPLETED,
            completed_date__isnull=False
        )
        
        if completed_orders.exists():
            # Calculate time difference
            avg_time = completed_orders.annotate(
                completion_time=ExpressionWrapper(
                    F('completed_date') - F('created_at'),
                    output_field=DurationField()
                )
            ).aggregate(
                avg=Avg('completion_time')
            )['avg']
            
            if avg_time:
                summary['avg_completion_time'] = round(avg_time.total_seconds() / 3600, 2)  # in hours
        
        # Total hours worked
        total_hours = work_orders.aggregate(
            total=Sum('actual_hours')
        )['total'] or 0
        summary['total_hours_worked'] = round(float(total_hours) if total_hours else 0, 2)
        
        return summary
    
    @staticmethod
    def get_asset_downtime_report(start_date=None, end_date=None):
        """Generate asset downtime report."""
        filters = Q(status=WorkOrder.STATUS_COMPLETED)
        
        if start_date:
            filters &= Q(completed_date__gte=start_date)
        
        if end_date:
            filters &= Q(completed_date__lte=end_date)
        
        # Get downtime by asset
        downtime_data = WorkOrder.objects.filter(filters).values(
            'asset__id',
            'asset__name',
            'asset__vehicle_type'
        ).annotate(
            total_downtime=Sum('actual_hours'),
            work_order_count=Count('id')
        ).order_by('-total_downtime')
        
        return list(downtime_data)
    
    @staticmethod
    def get_spare_part_consumption_report(start_date=None, end_date=None):
        """Generate spare part consumption report."""
        filters = Q(movement_type=StockMovement.MOVEMENT_OUT)
        
        if start_date:
            filters &= Q(created_at__gte=start_date)
        
        if end_date:
            filters &= Q(created_at__lte=end_date)
        
        # Get consumption by spare part
        consumption_data = StockMovement.objects.filter(filters).values(
            'spare_part__id',
            'spare_part__name',
            'spare_part__part_number'
        ).annotate(
            total_quantity=Sum('quantity'),
            movement_count=Count('id')
        ).order_by('-total_quantity')
        
        return list(consumption_data)
    
    @staticmethod
    def get_maintenance_compliance_report(start_date=None, end_date=None):
        """Generate maintenance compliance report."""
        filters = Q()
        
        if start_date:
            filters &= Q(created_at__gte=start_date)
        
        if end_date:
            filters &= Q(created_at__lte=end_date)
        
        # Get all active maintenance plans
        plans = MaintenancePlan.objects.filter(filters)
        
        total_plans = plans.count()
        overdue_plans = plans.filter(next_due_date__lt=timezone.now()).count()
        upcoming_plans = plans.filter(
            next_due_date__gte=timezone.now(),
            next_due_date__lte=timezone.now() + timedelta(days=7)
        ).count()
        
        compliance_rate = ((total_plans - overdue_plans) / total_plans * 100) if total_plans > 0 else 100
        
        return {
            'total_plans': total_plans,
            'overdue_plans': overdue_plans,
            'upcoming_plans': upcoming_plans,
            'compliance_rate': round(compliance_rate, 2),
            'on_schedule': total_plans - overdue_plans
        }
    
    @staticmethod
    def get_dashboard_kpis(start_date=None, end_date=None, user_id=None):
        """
        Get all KPIs for dashboard filtered by user role.
        
        Args:
            start_date: Start date for filtering
            end_date: End date for filtering
            user_id: User ID for filtering (None for ADMIN/SUPERVISOR, user_id for OPERADOR)
        
        Returns:
            Dictionary with all KPIs and summaries
        """
        if not start_date:
            start_date = timezone.now() - timedelta(days=30)
        
        if not end_date:
            end_date = timezone.now()
        
        return {
            'mtbf': ReportService.calculate_mtbf(start_date=start_date, end_date=end_date, user_id=user_id),
            'mttr': ReportService.calculate_mttr(start_date=start_date, end_date=end_date, user_id=user_id),
            'oee': ReportService.calculate_oee(start_date=start_date, end_date=end_date, user_id=user_id),
            'work_order_summary': ReportService.get_work_order_summary(start_date=start_date, end_date=end_date, user_id=user_id),
            'maintenance_compliance': ReportService.get_maintenance_compliance_report(start_date=start_date, end_date=end_date),
        }
