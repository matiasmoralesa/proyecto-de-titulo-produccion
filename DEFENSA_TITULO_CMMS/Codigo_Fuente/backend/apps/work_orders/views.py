"""
Views for work orders app.
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from apps.core.permissions import IsOperadorOrAbove, IsOwnerOrSupervisor
from apps.core.mixins import RoleBasedQuerySetMixin
from apps.authentication.models import Role
from .models import WorkOrder
from .serializers import (
    WorkOrderListSerializer,
    WorkOrderDetailSerializer,
    WorkOrderCreateSerializer,
    WorkOrderUpdateSerializer,
    WorkOrderCompleteSerializer,
)


class WorkOrderViewSet(RoleBasedQuerySetMixin, viewsets.ModelViewSet):
    """ViewSet for WorkOrder model with role-based access control."""
    queryset = WorkOrder.objects.select_related('asset', 'assigned_to', 'created_by')
    permission_classes = [IsAuthenticated, IsOperadorOrAbove]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'asset', 'assigned_to']
    search_fields = ['work_order_number', 'title', 'description']
    ordering_fields = ['created_at', 'scheduled_date', 'priority']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return WorkOrderListSerializer
        elif self.action == 'create':
            return WorkOrderCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return WorkOrderUpdateSerializer
        elif self.action == 'complete':
            return WorkOrderCompleteSerializer
        return WorkOrderDetailSerializer
    
    def filter_by_role(self, queryset, user):
        """
        Apply role-based filtering to work orders.
        
        - ADMIN: See all work orders
        - SUPERVISOR: See all work orders (can be customized by team/area)
        - OPERADOR: See only assigned work orders
        """
        if user.role.name == Role.SUPERVISOR:
            # Supervisors see all work orders
            # TODO: Filter by team/area when team structure is implemented
            return queryset
        
        elif user.role.name == Role.OPERADOR:
            # Operators only see their assigned work orders
            return queryset.filter(assigned_to=user)
        
        return queryset
    
    def get_permissions(self):
        """
        Set permissions based on action.
        
        - create: Any authenticated user with valid role
        - update/partial_update: Owner or supervisor/admin
        - destroy: Admin only (inherited from IsOperadorOrAbove + object check)
        """
        if self.action in ['update', 'partial_update', 'complete', 'transition_status']:
            return [IsAuthenticated(), IsOwnerOrSupervisor()]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        """
        Set created_by on creation.
        
        Validates: Requirements 1.4, 7.3
        """
        # All authenticated users with valid roles can create work orders
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        """
        Validate permissions before updating.
        
        Validates: Requirements 1.4, 7.4
        """
        # Permission check is handled by get_permissions() -> IsOwnerOrSupervisor
        # This ensures only the assigned user, supervisors, or admins can update
        serializer.save()
    
    def perform_destroy(self, instance):
        """
        Validate permissions before deleting.
        Only admins can delete work orders.
        
        Validates: Requirements 7.5
        """
        user = self.request.user
        
        # Only admins can delete work orders
        if user.role.name != Role.ADMIN:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Only administrators can delete work orders.')
        
        instance.delete()
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Complete a work order."""
        work_order = self.get_object()
        
        if work_order.status == WorkOrder.STATUS_COMPLETED:
            return Response(
                {'detail': 'Work order is already completed.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            work_order.complete(
                completion_notes=serializer.validated_data['completion_notes'],
                actual_hours=serializer.validated_data['actual_hours']
            )
        except ValueError as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(
            WorkOrderDetailSerializer(work_order).data,
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'])
    def transition_status(self, request, pk=None):
        """Transition work order to a new status."""
        work_order = self.get_object()
        new_status = request.data.get('new_status')
        
        if not new_status:
            return Response(
                {'error': 'new_status is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not work_order.can_transition_to(new_status):
            return Response(
                {'error': f'Cannot transition from {work_order.status} to {new_status}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        work_order.status = new_status
        work_order.save()
        
        return Response(
            WorkOrderDetailSerializer(work_order).data,
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'])
    def my_assignments(self, request):
        """Get work orders assigned to current user."""
        queryset = self.get_queryset().filter(assigned_to=request.user)
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = WorkOrderListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = WorkOrderListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get work order statistics."""
        queryset = self.filter_queryset(self.get_queryset())
        
        stats = {
            'total': queryset.count(),
            'by_status': {},
            'by_priority': {},
        }
        
        for status_choice, _ in WorkOrder.STATUS_CHOICES:
            count = queryset.filter(status=status_choice).count()
            stats['by_status'][status_choice] = count
        
        for priority_choice, _ in WorkOrder.PRIORITY_CHOICES:
            count = queryset.filter(priority=priority_choice).count()
            stats['by_priority'][priority_choice] = count
        
        return Response(stats)
