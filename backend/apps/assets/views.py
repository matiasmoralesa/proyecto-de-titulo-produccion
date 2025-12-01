"""
Views for assets app.
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from apps.authentication.permissions import IsAdmin, IsSupervisorOrAdmin
from .models import Location, Asset, AssetDocument
from .serializers import (
    LocationSerializer,
    AssetListSerializer,
    AssetDetailSerializer,
    AssetCreateUpdateSerializer,
    AssetDocumentSerializer,
)
from .filters import AssetFilter, LocationFilter


class LocationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Location model.
    Only admins can create/update/delete locations.
    """
    queryset = Location.objects.all().prefetch_related('assets')
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = LocationFilter
    search_fields = ['name', 'address', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    def get_permissions(self):
        """Admin only for create, update, delete."""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [IsAuthenticated()]
    
    def destroy(self, request, *args, **kwargs):
        """Prevent deletion if location has assets."""
        instance = self.get_object()
        if instance.assets.exists():
            return Response(
                {'detail': 'Cannot delete location with existing assets.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)


class AssetViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Asset model with role-based access control.
    
    - ADMIN: See all assets
    - SUPERVISOR: See all assets (can be customized by area)
    - OPERADOR: See only assets from their assigned work orders
    
    Validates: Requirements 2.1, 2.2, 2.3, 2.4
    """
    queryset = Asset.objects.select_related('location', 'created_by').prefetch_related('documents')
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AssetFilter
    search_fields = ['name', 'serial_number', 'license_plate', 'model']
    ordering_fields = ['name', 'created_at', 'installation_date', 'status']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return AssetListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return AssetCreateUpdateSerializer
        return AssetDetailSerializer
    
    def get_queryset(self):
        """
        Filter queryset based on user role.
        
        Validates: Requirements 2.1, 2.2, 2.3, 2.5
        """
        from apps.authentication.models import Role
        from apps.work_orders.models import WorkOrder
        
        queryset = super().get_queryset()
        user = self.request.user
        
        # By default, exclude archived assets
        if self.request.query_params.get('include_archived') != 'true':
            queryset = queryset.filter(is_archived=False)
        
        # Apply role-based filtering
        if user.role.name == Role.ADMIN:
            # Admins see all assets
            return queryset
        
        elif user.role.name == Role.SUPERVISOR:
            # Supervisors see all assets
            # TODO: Filter by area/department when structure is implemented
            return queryset
        
        elif user.role.name == Role.OPERADOR:
            # Operators only see assets from their assigned work orders
            accessible_asset_ids = WorkOrder.objects.filter(
                assigned_to=user
            ).values_list('asset_id', flat=True).distinct()
            
            return queryset.filter(id__in=accessible_asset_ids)
        
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve asset details with permission check.
        
        Returns 404 instead of 403 to not reveal asset existence.
        Validates: Requirements 2.4
        """
        try:
            return super().retrieve(request, *args, **kwargs)
        except Exception:
            # Return 404 for any error to not reveal existence
            from rest_framework.exceptions import NotFound
            raise NotFound('Asset not found.')
    
    def perform_create(self, serializer):
        """Set created_by on creation."""
        serializer.save(created_by=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        """Soft delete by archiving the asset."""
        instance = self.get_object()
        instance.soft_delete()
        return Response(
            {'detail': 'Asset archived successfully.'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        """Restore an archived asset."""
        asset = self.get_object()
        if not asset.is_archived:
            return Response(
                {'detail': 'Asset is not archived.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        asset.is_archived = False
        asset.save()
        
        serializer = self.get_serializer(asset)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get asset statistics."""
        queryset = self.filter_queryset(self.get_queryset())
        
        stats = {
            'total': queryset.count(),
            'by_vehicle_type': {},
            'by_status': {},
            'archived': queryset.filter(is_archived=True).count(),
        }
        
        # Count by vehicle type
        for vehicle_type, _ in Asset.VEHICLE_TYPE_CHOICES:
            count = queryset.filter(vehicle_type=vehicle_type).count()
            stats['by_vehicle_type'][vehicle_type] = count
        
        # Count by status
        for status_choice, _ in Asset.STATUS_CHOICES:
            count = queryset.filter(status=status_choice).count()
            stats['by_status'][status_choice] = count
        
        return Response(stats)


class AssetDocumentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for AssetDocument model.
    """
    queryset = AssetDocument.objects.select_related('asset', 'uploaded_by')
    serializer_class = AssetDocumentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['asset', 'document_type']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']
    
    def perform_create(self, serializer):
        """Set uploaded_by on creation."""
        serializer.save(uploaded_by=self.request.user)
