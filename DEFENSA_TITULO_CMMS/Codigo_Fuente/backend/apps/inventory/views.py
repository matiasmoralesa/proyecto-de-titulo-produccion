"""
Views for inventory app.
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Sum, F
from .models import SparePart, StockMovement
from .serializers import (
    SparePartSerializer,
    SparePartListSerializer,
    StockMovementSerializer,
    StockAdjustmentSerializer,
    LowStockAlertSerializer,
)
from apps.authentication.permissions import IsSupervisorOrAdmin


class SparePartViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing spare parts.
    
    Provides CRUD operations and additional actions for stock management.
    """
    queryset = SparePart.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active', 'manufacturer']
    search_fields = ['part_number', 'name', 'description', 'category']
    ordering_fields = ['name', 'part_number', 'quantity', 'created_at']
    ordering = ['name']
    
    def get_serializer_class(self):
        """Return appropriate serializer class."""
        if self.action == 'list':
            return SparePartListSerializer
        return SparePartSerializer
    
    def get_queryset(self):
        """Filter queryset based on query parameters."""
        queryset = super().get_queryset()
        
        # Filter by low stock
        low_stock = self.request.query_params.get('low_stock', None)
        if low_stock == 'true':
            queryset = queryset.filter(quantity__lte=F('min_quantity'))
        
        # Filter by out of stock
        out_of_stock = self.request.query_params.get('out_of_stock', None)
        if out_of_stock == 'true':
            queryset = queryset.filter(quantity=0)
        
        return queryset
    
    def perform_create(self, serializer):
        """Set created_by when creating a spare part."""
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'], url_path='adjust-stock')
    def adjust_stock(self, request, pk=None):
        """
        Adjust stock quantity for a spare part.
        
        POST /api/spare-parts/{id}/adjust-stock/
        Body: {
            "quantity_change": 10,  # positive for in, negative for out
            "movement_type": "IN",
            "notes": "Received from supplier",
            "reference_type": "purchase_order",
            "reference_id": "PO-123"
        }
        """
        spare_part = self.get_object()
        serializer = StockAdjustmentSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                movement = spare_part.adjust_stock(
                    quantity_change=serializer.validated_data['quantity_change'],
                    movement_type=serializer.validated_data['movement_type'],
                    user=request.user,
                    notes=serializer.validated_data.get('notes', '')
                )
                
                # Update reference information if provided
                if serializer.validated_data.get('reference_type'):
                    movement.reference_type = serializer.validated_data['reference_type']
                if serializer.validated_data.get('reference_id'):
                    movement.reference_id = serializer.validated_data['reference_id']
                movement.save()
                
                # Return updated spare part and movement
                spare_part_serializer = SparePartSerializer(spare_part)
                movement_serializer = StockMovementSerializer(movement)
                
                return Response({
                    'spare_part': spare_part_serializer.data,
                    'movement': movement_serializer.data,
                    'message': 'Stock ajustado exitosamente'
                }, status=status.HTTP_200_OK)
                
            except ValueError as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'], url_path='stock-history')
    def stock_history(self, request, pk=None):
        """
        Get stock movement history for a spare part.
        
        GET /api/spare-parts/{id}/stock-history/
        """
        spare_part = self.get_object()
        movements = spare_part.stock_movements.all()
        
        # Apply date filtering if provided
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if start_date:
            movements = movements.filter(created_at__gte=start_date)
        if end_date:
            movements = movements.filter(created_at__lte=end_date)
        
        # Apply movement type filtering
        movement_type = request.query_params.get('movement_type')
        if movement_type:
            movements = movements.filter(movement_type=movement_type)
        
        serializer = StockMovementSerializer(movements, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='low-stock-alerts')
    def low_stock_alerts(self, request):
        """
        Get list of spare parts with low stock.
        
        GET /api/spare-parts/low-stock-alerts/
        """
        spare_parts = self.get_queryset().filter(
            quantity__lte=F('min_quantity'),
            is_active=True
        ).order_by('quantity')
        
        serializer = LowStockAlertSerializer(spare_parts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='statistics')
    def statistics(self, request):
        """
        Get inventory statistics.
        
        GET /api/spare-parts/statistics/
        """
        queryset = self.get_queryset().filter(is_active=True)
        
        total_parts = queryset.count()
        low_stock_count = queryset.filter(quantity__lte=F('min_quantity')).count()
        out_of_stock_count = queryset.filter(quantity=0).count()
        
        total_value = queryset.aggregate(
            total=Sum(F('quantity') * F('unit_cost'))
        )['total'] or 0
        
        # Get category breakdown
        categories = queryset.values('category').annotate(
            count=Sum('quantity'),
            value=Sum(F('quantity') * F('unit_cost'))
        ).order_by('-count')
        
        return Response({
            'total_parts': total_parts,
            'low_stock_count': low_stock_count,
            'out_of_stock_count': out_of_stock_count,
            'total_inventory_value': float(total_value),
            'categories': list(categories),
        })
    
    @action(detail=False, methods=['post'], url_path='seed-spare-parts-usage', permission_classes=[IsSupervisorOrAdmin])
    def seed_spare_parts_usage(self, request):
        """
        Seed spare parts usage data for testing/demo purposes.
        
        POST /api/v1/inventory/spare-parts/seed-spare-parts-usage/
        """
        from django.core.management import call_command
        from io import StringIO
        
        # Capture command output
        out = StringIO()
        
        try:
            call_command('seed_spare_parts_usage', stdout=out)
            output = out.getvalue()
            
            return Response({
                'message': 'Datos de uso de repuestos generados exitosamente',
                'output': output
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': str(e),
                'message': 'Error al generar datos de uso de repuestos'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StockMovementViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing stock movements (read-only).
    
    Stock movements are created through the adjust_stock action on SparePartViewSet.
    """
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['spare_part', 'movement_type', 'user']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter queryset based on query parameters."""
        queryset = super().get_queryset()
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        
        return queryset
    
    @action(detail=False, methods=['get'], url_path='summary')
    def summary(self, request):
        """
        Get summary of stock movements.
        
        GET /api/stock-movements/summary/
        """
        queryset = self.get_queryset()
        
        # Get movement type breakdown
        by_type = {}
        for movement_type, display_name in StockMovement.MOVEMENT_TYPES:
            count = queryset.filter(movement_type=movement_type).count()
            total_quantity = queryset.filter(movement_type=movement_type).aggregate(
                total=Sum('quantity')
            )['total'] or 0
            
            by_type[movement_type] = {
                'display_name': display_name,
                'count': count,
                'total_quantity': total_quantity,
            }
        
        total_movements = queryset.count()
        
        return Response({
            'total_movements': total_movements,
            'by_type': by_type,
        })
