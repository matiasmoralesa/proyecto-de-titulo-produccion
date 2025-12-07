"""
Views for machine status app.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Sum, Avg, Count
from django.utils import timezone
from datetime import timedelta
from .models import AssetStatus, AssetStatusHistory
from .serializers import (
    AssetStatusSerializer,
    AssetStatusUpdateSerializer,
    AssetStatusHistorySerializer
)
from apps.authentication.models import Role
from apps.work_orders.models import WorkOrder
from apps.notifications.services import NotificationService
from apps.assets.models import Asset


class AssetStatusViewSet(viewsets.ModelViewSet):
    """
    ViewSet for asset status management.
    - OPERADOR: Can only update status for assigned assets
    - SUPERVISOR/ADMIN: Can update status for any asset
    """
    queryset = AssetStatus.objects.all().select_related('asset', 'last_updated_by')
    serializer_class = AssetStatusSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter queryset based on user role."""
        queryset = super().get_queryset()
        user = self.request.user
        
        # OPERADOR can only see status for assigned assets
        if user.role.name == Role.OPERADOR:
            # Get assets assigned to this user through active work orders
            assigned_asset_ids = WorkOrder.objects.filter(
                assigned_to=user,
                status__in=['PENDING', 'IN_PROGRESS']
            ).values_list('asset_id', flat=True)
            
            queryset = queryset.filter(asset_id__in=assigned_asset_ids)
        
        # Filter by asset if provided
        asset_id = self.request.query_params.get('asset', None)
        if asset_id:
            queryset = queryset.filter(asset_id=asset_id)
        
        # Filter by status type if provided
        status_type = self.request.query_params.get('status_type', None)
        if status_type:
            queryset = queryset.filter(status_type=status_type)
        
        return queryset
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action in ['update', 'partial_update', 'update_status']:
            return AssetStatusUpdateSerializer
        return AssetStatusSerializer
    
    def perform_update(self, serializer):
        """Update status and set last_updated_by."""
        user = self.request.user
        asset = serializer.instance.asset
        
        # Check if OPERADOR is updating an assigned asset
        if user.role.name == Role.OPERADOR:
            # Check if asset is assigned to this user
            is_assigned = WorkOrder.objects.filter(
                assigned_to=user,
                asset=asset,
                status__in=['PENDING', 'IN_PROGRESS']
            ).exists()
            
            if not is_assigned:
                raise PermissionError('You can only update status for assigned assets.')
        
        # Save with updated_by
        old_status = serializer.instance.status_type
        instance = serializer.save(last_updated_by=user)
        
        # Create alert notification if status changed to FUERA_DE_SERVICIO
        if instance.status_type == AssetStatus.FUERA_DE_SERVICIO and old_status != AssetStatus.FUERA_DE_SERVICIO:
            self._create_out_of_service_alert(instance)
    
    def update(self, request, *args, **kwargs):
        """Override update to return full serializer."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = AssetStatusUpdateSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # Return full serializer with all fields
        response_serializer = AssetStatusSerializer(instance)
        return Response(response_serializer.data)
    
    def _create_out_of_service_alert(self, asset_status):
        """Create alert notification for out of service status."""
        from apps.authentication.models import User
        
        # Get all ADMIN and SUPERVISOR users
        admin_supervisor_users = User.objects.filter(
            role__name__in=[Role.ADMIN, Role.SUPERVISOR],
            is_active=True
        )
        
        # Create notifications
        for user in admin_supervisor_users:
            NotificationService.create_notification(
                user=user,
                notification_type='ALERT',
                title='Activo Fuera de Servicio',
                message=f'El activo {asset_status.asset.name} ha sido marcado como Fuera de Servicio.',
                related_object_type='asset',
                related_object_id=asset_status.asset.id
            )
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update asset status (custom endpoint)."""
        asset_status = self.get_object()
        serializer = AssetStatusUpdateSerializer(
            asset_status,
            data=request.data,
            partial=True
        )
        
        if serializer.is_valid():
            self.perform_update(serializer)
            response_serializer = AssetStatusSerializer(asset_status)
            return Response(response_serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssetStatusHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing asset status history.
    Read-only for all authenticated users.
    """
    queryset = AssetStatusHistory.objects.all().select_related('asset', 'updated_by')
    serializer_class = AssetStatusHistorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter queryset based on query parameters."""
        queryset = super().get_queryset()
        
        # Filter by asset if provided
        asset_id = self.request.query_params.get('asset', None)
        if asset_id:
            queryset = queryset.filter(asset_id=asset_id)
        
        # Filter by status type if provided
        status_type = self.request.query_params.get('status_type', None)
        if status_type:
            queryset = queryset.filter(status_type=status_type)
        
        # Filter by date range if provided
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            queryset = queryset.filter(timestamp__gte=start_date)
        if end_date:
            queryset = queryset.filter(timestamp__lte=end_date)
        
        return queryset



class AssetHistoryPagination(PageNumberPagination):
    """Custom pagination for asset history."""
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200


class AssetHistoryViewSet(viewsets.ViewSet):
    """
    ViewSet for comprehensive asset history and KPIs.
    Aggregates all activities related to an asset.
    """
    permission_classes = [IsAuthenticated]
    pagination_class = AssetHistoryPagination
    
    @action(detail=False, methods=['get'], url_path='(?P<asset_id>[^/.]+)/complete-history')
    def complete_history(self, request, asset_id=None):
        """
        Get complete history for an asset including:
        - Status updates
        - Work orders
        - Maintenance activities
        - Checklist completions
        - Spare part usage
        """
        try:
            asset = Asset.objects.get(id=asset_id)
        except Asset.DoesNotExist:
            return Response(
                {'error': 'Asset not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get query parameters for filtering
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        activity_type = request.query_params.get('activity_type', None)
        
        # Build timeline of all activities
        timeline = []
        
        # 1. Status updates
        if not activity_type or activity_type == 'status':
            status_updates = AssetStatusHistory.objects.filter(asset=asset).select_related('updated_by')
            
            if start_date:
                status_updates = status_updates.filter(timestamp__gte=start_date)
            if end_date:
                status_updates = status_updates.filter(timestamp__lte=end_date)
            
            for update in status_updates:
                # Get display name for status
                status_display = {
                    AssetStatus.OPERANDO: 'Operando',
                    AssetStatus.DETENIDA: 'Detenida',
                    AssetStatus.EN_MANTENIMIENTO: 'En Mantenimiento',
                    AssetStatus.FUERA_DE_SERVICIO: 'Fuera de Servicio'
                }.get(update.status_type, update.status_type)
                
                timeline.append({
                    'type': 'status_update',
                    'timestamp': update.timestamp,
                    'user': {
                        'id': str(update.updated_by.id),
                        'name': update.updated_by.get_full_name() or update.updated_by.username
                    },
                    'data': {
                        'status_type': update.status_type,
                        'status_type_display': status_display,
                        'odometer_reading': update.odometer_reading,
                        'fuel_level': update.fuel_level,
                        'condition_notes': update.condition_notes
                    }
                })
        
        # 2. Work orders
        if not activity_type or activity_type == 'work_order':
            work_orders = WorkOrder.objects.filter(asset=asset).select_related('assigned_to', 'created_by')
            
            if start_date:
                work_orders = work_orders.filter(created_at__gte=start_date)
            if end_date:
                work_orders = work_orders.filter(created_at__lte=end_date)
            
            for wo in work_orders:
                # Work order creation
                timeline.append({
                    'type': 'work_order_created',
                    'timestamp': wo.created_at,
                    'user': {
                        'id': str(wo.created_by.id),
                        'name': wo.created_by.get_full_name() or wo.created_by.username
                    },
                    'data': {
                        'id': str(wo.id),
                        'work_order_number': wo.work_order_number,
                        'title': wo.title,
                        'priority': wo.priority,
                        'status': wo.status,
                        'assigned_to': wo.assigned_to.get_full_name() or wo.assigned_to.username
                    }
                })
                
                # Work order completion
                if wo.completed_date:
                    timeline.append({
                        'type': 'work_order_completed',
                        'timestamp': wo.completed_date,
                        'user': {
                            'id': str(wo.assigned_to.id),
                            'name': wo.assigned_to.get_full_name() or wo.assigned_to.username
                        },
                        'data': {
                            'id': str(wo.id),
                            'work_order_number': wo.work_order_number,
                            'title': wo.title,
                            'actual_hours': float(wo.actual_hours) if wo.actual_hours else None,
                            'completion_notes': wo.completion_notes
                        }
                    })
        
        # 3. Maintenance plans
        if not activity_type or activity_type == 'maintenance':
            from apps.maintenance.models import MaintenancePlan
            maintenance_plans = MaintenancePlan.objects.filter(asset=asset)
            
            if start_date:
                maintenance_plans = maintenance_plans.filter(created_at__gte=start_date)
            if end_date:
                maintenance_plans = maintenance_plans.filter(created_at__lte=end_date)
            
            for plan in maintenance_plans:
                timeline.append({
                    'type': 'maintenance_plan_created',
                    'timestamp': plan.created_at,
                    'user': {
                        'id': 'system',
                        'name': 'System'
                    },
                    'data': {
                        'id': str(plan.id),
                        'name': plan.name,
                        'description': plan.description,
                        'recurrence_type': plan.recurrence_type,
                        'next_due_date': plan.next_due_date.isoformat() if plan.next_due_date else None
                    }
                })
        
        # 4. Checklist completions
        if not activity_type or activity_type == 'checklist':
            from apps.checklists.models import ChecklistResponse
            checklists = ChecklistResponse.objects.filter(asset=asset).select_related('completed_by', 'template')
            
            if start_date:
                checklists = checklists.filter(completed_at__gte=start_date)
            if end_date:
                checklists = checklists.filter(completed_at__lte=end_date)
            
            for checklist in checklists:
                # Check if pdf_report field exists
                pdf_url = None
                if hasattr(checklist, 'pdf_report') and checklist.pdf_report:
                    try:
                        pdf_url = request.build_absolute_uri(checklist.pdf_report.url)
                    except:
                        pdf_url = None
                
                timeline.append({
                    'type': 'checklist_completed',
                    'timestamp': checklist.completed_at,
                    'user': {
                        'id': str(checklist.completed_by.id),
                        'name': checklist.completed_by.get_full_name() or checklist.completed_by.username
                    },
                    'data': {
                        'id': str(checklist.id),
                        'template_name': checklist.template.name,
                        'template_code': checklist.template.code,
                        'completion_percentage': getattr(checklist, 'completion_percentage', 0),
                        'pdf_report': pdf_url
                    }
                })
        
        # 5. Spare part usage
        if not activity_type or activity_type == 'spare_part':
            from apps.inventory.models import StockMovement
            
            # Get work orders for this asset
            work_order_ids = WorkOrder.objects.filter(asset=asset).values_list('id', flat=True)
            
            # Filter stock movements by work order references
            stock_movements = StockMovement.objects.filter(
                reference_type='work_order',
                reference_id__in=[str(wo_id) for wo_id in work_order_ids],
                movement_type='OUT'
            ).select_related('spare_part', 'user')
            
            if start_date:
                stock_movements = stock_movements.filter(created_at__gte=start_date)
            if end_date:
                stock_movements = stock_movements.filter(created_at__lte=end_date)
            
            for movement in stock_movements:
                # Try to get work order number
                work_order_number = None
                try:
                    wo = WorkOrder.objects.get(id=movement.reference_id)
                    work_order_number = wo.work_order_number
                except:
                    pass
                
                timeline.append({
                    'type': 'spare_part_used',
                    'timestamp': movement.created_at,
                    'user': {
                        'id': str(movement.user.id) if movement.user else 'system',
                        'name': movement.user.get_full_name() or movement.user.username if movement.user else 'System'
                    },
                    'data': {
                        'spare_part_name': movement.spare_part.name,
                        'spare_part_number': movement.spare_part.part_number,
                        'quantity': movement.quantity,
                        'work_order_number': work_order_number,
                        'notes': movement.notes
                    }
                })
        
        # Sort timeline by timestamp (most recent first)
        timeline.sort(key=lambda x: x['timestamp'], reverse=True)
        
        # Paginate results
        paginator = AssetHistoryPagination()
        page = paginator.paginate_queryset(timeline, request)
        
        return paginator.get_paginated_response(page)
    
    @action(detail=False, methods=['get'], url_path='(?P<asset_id>[^/.]+)/kpis')
    def asset_kpis(self, request, asset_id=None):
        """
        Calculate and return KPIs for a specific asset:
        - Total maintenance hours
        - Number of work orders completed
        - Average downtime
        - Total maintenance cost
        """
        try:
            asset = Asset.objects.get(id=asset_id)
        except Asset.DoesNotExist:
            return Response(
                {'error': 'Asset not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get date range for KPI calculation
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        
        # Default to last 12 months if no date range provided
        if not start_date:
            start_date = timezone.now() - timedelta(days=365)
        if not end_date:
            end_date = timezone.now()
        
        # Calculate KPIs
        work_orders = WorkOrder.objects.filter(
            asset=asset,
            created_at__gte=start_date,
            created_at__lte=end_date
        )
        
        # Total maintenance hours
        total_hours = work_orders.filter(
            status='Completada'
        ).aggregate(
            total=Sum('actual_hours')
        )['total'] or 0
        
        # Number of work orders
        total_work_orders = work_orders.count()
        completed_work_orders = work_orders.filter(status='Completada').count()
        pending_work_orders = work_orders.filter(status='Pendiente').count()
        in_progress_work_orders = work_orders.filter(status='En Progreso').count()
        
        # Calculate downtime (time in DETENIDA, EN_MANTENIMIENTO, FUERA_DE_SERVICIO status)
        status_history = AssetStatusHistory.objects.filter(
            asset=asset,
            timestamp__gte=start_date,
            timestamp__lte=end_date,
            status_type__in=[
                AssetStatus.DETENIDA,
                AssetStatus.EN_MANTENIMIENTO,
                AssetStatus.FUERA_DE_SERVICIO
            ]
        ).order_by('timestamp')
        
        # Simple downtime calculation (count of status changes to downtime states)
        downtime_events = status_history.count()
        
        # Calculate maintenance cost (from spare parts used)
        from apps.inventory.models import StockMovement
        
        # Get work orders for this asset in the date range
        work_order_ids = work_orders.values_list('id', flat=True)
        
        # Calculate cost from stock movements
        maintenance_cost = StockMovement.objects.filter(
            reference_type='work_order',
            reference_id__in=[str(wo_id) for wo_id in work_order_ids],
            movement_type='OUT'
        ).aggregate(
            total_cost=Sum('unit_cost')
        )['total_cost'] or 0
        
        # Get current status
        try:
            current_status = AssetStatus.objects.get(asset=asset)
            current_status_data = {
                'status_type': current_status.status_type,
                'status_type_display': current_status.get_status_type_display(),
                'fuel_level': current_status.fuel_level,
                'odometer_reading': current_status.odometer_reading,
                'last_updated': current_status.updated_at
            }
        except AssetStatus.DoesNotExist:
            current_status_data = None
        
        kpis = {
            'asset': {
                'id': str(asset.id),
                'name': asset.name,
                'vehicle_type': asset.vehicle_type,
                'serial_number': asset.serial_number
            },
            'current_status': current_status_data,
            'kpis': {
                'total_maintenance_hours': float(total_hours),
                'total_work_orders': total_work_orders,
                'completed_work_orders': completed_work_orders,
                'pending_work_orders': pending_work_orders,
                'in_progress_work_orders': in_progress_work_orders,
                'downtime_events': downtime_events,
                'total_maintenance_cost': float(maintenance_cost),
                'average_hours_per_work_order': float(total_hours / completed_work_orders) if completed_work_orders > 0 else 0
            },
            'date_range': {
                'start_date': start_date.isoformat() if hasattr(start_date, 'isoformat') else start_date,
                'end_date': end_date.isoformat() if hasattr(end_date, 'isoformat') else end_date
            }
        }
        
        return Response(kpis)
