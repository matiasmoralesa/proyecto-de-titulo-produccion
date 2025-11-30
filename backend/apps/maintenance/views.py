"""
Views for maintenance app.
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import MaintenancePlan
from .serializers import (
    MaintenancePlanListSerializer,
    MaintenancePlanDetailSerializer,
    MaintenancePlanCreateUpdateSerializer,
    MaintenancePlanPauseSerializer,
    MaintenancePlanCompleteSerializer,
    MaintenancePlanUsageUpdateSerializer,
)


class MaintenancePlanViewSet(viewsets.ModelViewSet):
    """ViewSet for MaintenancePlan model."""
    queryset = MaintenancePlan.objects.select_related(
        'asset', 'assigned_to', 'created_by', 'paused_by'
    )
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'recurrence_type', 'asset', 'assigned_to', 'is_paused']
    search_fields = ['name', 'description', 'asset__name']
    ordering_fields = ['next_due_date', 'created_at', 'name']
    ordering = ['next_due_date', '-created_at']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return MaintenancePlanListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return MaintenancePlanCreateUpdateSerializer
        elif self.action == 'pause_resume':
            return MaintenancePlanPauseSerializer
        elif self.action == 'complete':
            return MaintenancePlanCompleteSerializer
        elif self.action == 'update_usage':
            return MaintenancePlanUsageUpdateSerializer
        return MaintenancePlanDetailSerializer
    
    def perform_create(self, serializer):
        """Set created_by on creation."""
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def pause_resume(self, request, pk=None):
        """Pause or resume a maintenance plan."""
        plan = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        action_type = serializer.validated_data['action']
        
        if action_type == 'pause':
            if plan.is_paused:
                return Response(
                    {'detail': 'Maintenance plan is already paused.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            plan.pause(request.user)
            message = 'Maintenance plan paused successfully.'
        else:  # resume
            if not plan.is_paused:
                return Response(
                    {'detail': 'Maintenance plan is not paused.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            plan.resume()
            message = 'Maintenance plan resumed successfully.'
        
        return Response(
            {
                'detail': message,
                'data': MaintenancePlanDetailSerializer(plan).data
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark maintenance as completed."""
        plan = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        completion_date = serializer.validated_data.get('completion_date')
        usage_value = serializer.validated_data.get('usage_value')
        
        try:
            plan.complete_maintenance(
                completion_date=completion_date,
                usage_value=usage_value
            )
        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(
            {
                'detail': 'Maintenance completed successfully.',
                'data': MaintenancePlanDetailSerializer(plan).data
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'])
    def update_usage(self, request, pk=None):
        """Update usage value for usage-based plans."""
        plan = self.get_object()
        
        if not plan.is_usage_based():
            return Response(
                {'detail': 'This is not a usage-based maintenance plan.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        current_usage = serializer.validated_data['current_usage']
        plan.update_usage(current_usage)
        
        return Response(
            {
                'detail': 'Usage updated successfully.',
                'data': MaintenancePlanDetailSerializer(plan).data
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['get'])
    def calculate_next_due(self, request, pk=None):
        """Calculate next due date for a maintenance plan."""
        plan = self.get_object()
        
        if plan.is_usage_based():
            return Response(
                {'detail': 'Usage-based plans do not have a specific due date.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        next_due = plan.calculate_next_due_date()
        
        return Response(
            {
                'next_due_date': next_due,
                'current_next_due_date': plan.next_due_date
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'])
    def due_soon(self, request):
        """Get maintenance plans due soon (within 7 days)."""
        from datetime import timedelta
        
        today = timezone.now().date()
        week_from_now = today + timedelta(days=7)
        
        queryset = self.get_queryset().filter(
            status=MaintenancePlan.STATUS_ACTIVE,
            is_paused=False,
            next_due_date__lte=week_from_now,
            next_due_date__gte=today
        )
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = MaintenancePlanListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = MaintenancePlanListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get overdue maintenance plans."""
        today = timezone.now().date()
        
        queryset = self.get_queryset().filter(
            status=MaintenancePlan.STATUS_ACTIVE,
            is_paused=False,
            next_due_date__lt=today
        )
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = MaintenancePlanListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = MaintenancePlanListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get maintenance plan statistics."""
        queryset = self.filter_queryset(self.get_queryset())
        
        stats = {
            'total': queryset.count(),
            'active': queryset.filter(status=MaintenancePlan.STATUS_ACTIVE, is_paused=False).count(),
            'paused': queryset.filter(is_paused=True).count(),
            'due_soon': queryset.filter(
                status=MaintenancePlan.STATUS_ACTIVE,
                is_paused=False,
                next_due_date__lte=timezone.now().date() + timezone.timedelta(days=7)
            ).count(),
            'overdue': queryset.filter(
                status=MaintenancePlan.STATUS_ACTIVE,
                is_paused=False,
                next_due_date__lt=timezone.now().date()
            ).count(),
            'by_recurrence_type': {},
        }
        
        for recurrence_type, _ in MaintenancePlan.RECURRENCE_CHOICES:
            count = queryset.filter(recurrence_type=recurrence_type).count()
            stats['by_recurrence_type'][recurrence_type] = count
        
        return Response(stats)
