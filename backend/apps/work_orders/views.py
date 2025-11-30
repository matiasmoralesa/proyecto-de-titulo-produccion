"""
Views for work orders app.
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import WorkOrder
from .serializers import (
    WorkOrderListSerializer,
    WorkOrderDetailSerializer,
    WorkOrderCreateSerializer,
    WorkOrderUpdateSerializer,
    WorkOrderCompleteSerializer,
)


class WorkOrderViewSet(viewsets.ModelViewSet):
    """ViewSet for WorkOrder model."""
    queryset = WorkOrder.objects.select_related('asset', 'assigned_to', 'created_by')
    permission_classes = [IsAuthenticated]
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
    
    def get_queryset(self):
        """Filter queryset based on user role."""
        queryset = super().get_queryset()
        user = self.request.user
        
        # Operadores only see their assigned work orders
        if user.role.name == 'OPERADOR':
            queryset = queryset.filter(assigned_to=user)
        
        return queryset
    
    def perform_create(self, serializer):
        """Set created_by on creation."""
        serializer.save(created_by=self.request.user)
    
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
