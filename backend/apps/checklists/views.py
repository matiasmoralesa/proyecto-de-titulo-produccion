"""
Views for checklists app.
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from django.utils import timezone

from apps.checklists.models import (
    ChecklistTemplate,
    ChecklistTemplateItem,
    ChecklistResponse,
    ChecklistItemResponse
)
from apps.checklists.serializers import (
    ChecklistTemplateSerializer,
    ChecklistTemplateItemSerializer,
    ChecklistResponseSerializer,
    ChecklistResponseDetailSerializer,
    ChecklistItemResponseSerializer,
    ChecklistCompletionSerializer
)
from apps.checklists.models import ChecklistTemplateItem
from apps.authentication.permissions import IsAdmin, IsSupervisorOrAdmin, IsOperadorOrAbove


class ChecklistTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for ChecklistTemplate model.
    System templates are read-only.
    """
    queryset = ChecklistTemplate.objects.filter(is_active=True).prefetch_related('items')
    serializer_class = ChecklistTemplateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['vehicle_type', 'is_system_template']
    search_fields = ['code', 'name', 'description']
    ordering_fields = ['code', 'name', 'vehicle_type', 'created_at']
    ordering = ['vehicle_type', 'code']
    
    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        """Get all items for a specific template."""
        template = self.get_object()
        items = template.items.all()
        serializer = ChecklistTemplateItemSerializer(items, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_vehicle_type(self, request):
        """Get templates grouped by vehicle type."""
        vehicle_type = request.query_params.get('vehicle_type')
        if not vehicle_type:
            return Response(
                {'error': 'vehicle_type parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        templates = self.queryset.filter(vehicle_type=vehicle_type)
        serializer = self.get_serializer(templates, many=True)
        return Response(serializer.data)


class ChecklistResponseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for ChecklistResponse model.
    Handles checklist completion and management.
    """
    queryset = ChecklistResponse.objects.all().select_related(
        'template',
        'asset',
        'work_order',
        'completed_by'
    ).prefetch_related('item_responses__template_item')
    serializer_class = ChecklistResponseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'asset', 'work_order', 'completed_by', 'template']
    search_fields = ['asset__name', 'template__name', 'template__code']
    ordering_fields = ['created_at', 'completed_at', 'score']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'retrieve':
            return ChecklistResponseDetailSerializer
        elif self.action == 'complete':
            return ChecklistCompletionSerializer
        return ChecklistResponseSerializer
    
    def get_queryset(self):
        """Filter queryset based on user role."""
        user = self.request.user
        queryset = super().get_queryset()
        
        # Operators can only see their own checklists
        if user.role.name == 'OPERADOR':
            queryset = queryset.filter(completed_by=user)
        
        return queryset
    
    @action(detail=False, methods=['post'])
    def complete(self, request):
        """
        Complete a checklist with all responses at once.
        Creates ChecklistResponse and all ChecklistItemResponses.
        """
        serializer = ChecklistCompletionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        validated_data = serializer.validated_data
        template = validated_data['template']
        asset = validated_data['asset']
        work_order_id = validated_data.get('work_order_id')
        signature_data = validated_data.get('signature_data', '')
        item_responses_data = validated_data['item_responses']
        
        # Create ChecklistResponse
        checklist_response = ChecklistResponse.objects.create(
            template=template,
            asset=asset,
            work_order_id=work_order_id,
            completed_by=request.user,
            signature_data=signature_data,
            status=ChecklistResponse.STATUS_IN_PROGRESS
        )
        
        # Create ChecklistItemResponses
        for item_data in item_responses_data:
            ChecklistItemResponse.objects.create(
                checklist_response=checklist_response,
                template_item_id=item_data['template_item_id'],
                response_value=item_data.get('response_value', ''),
                observations=item_data.get('observations', ''),
                photo=item_data.get('photo')
            )
        
        # Update score and status
        checklist_response.update_score_and_status()
        
        # Generate PDF automatically when completing checklist
        from apps.checklists.services import generate_checklist_pdf
        try:
            pdf_file = generate_checklist_pdf(checklist_response)
            checklist_response.pdf_file = pdf_file
            checklist_response.save()
        except Exception as e:
            # Log the error but don't fail the completion
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error generating PDF for checklist {checklist_response.id}: {str(e)}")
        
        # Return the created checklist response
        response_serializer = ChecklistResponseDetailSerializer(
            checklist_response,
            context={'request': request}
        )
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def add_item_response(self, request, pk=None):
        """Add or update a single item response."""
        checklist_response = self.get_object()
        
        # Check if checklist is still in progress
        if checklist_response.status != ChecklistResponse.STATUS_IN_PROGRESS:
            return Response(
                {'error': 'No se pueden modificar checklists completados.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = ChecklistItemResponseSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        
        # Check if response already exists
        template_item_id = serializer.validated_data['template_item_id']
        existing_response = checklist_response.item_responses.filter(
            template_item_id=template_item_id
        ).first()
        
        if existing_response:
            # Update existing response
            for key, value in serializer.validated_data.items():
                if key != 'template_item_id':
                    setattr(existing_response, key, value)
            existing_response.save()
            item_response = existing_response
        else:
            # Create new response
            item_response = ChecklistItemResponse.objects.create(
                checklist_response=checklist_response,
                **serializer.validated_data
            )
        
        # Update score and status
        checklist_response.update_score_and_status()
        
        response_serializer = ChecklistItemResponseSerializer(
            item_response,
            context={'request': request}
        )
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def finalize(self, request, pk=None):
        """
        Finalize a checklist and generate PDF.
        """
        checklist_response = self.get_object()
        
        # Check if checklist is in progress
        if checklist_response.status != ChecklistResponse.STATUS_IN_PROGRESS:
            return Response(
                {'error': 'Este checklist ya ha sido finalizado.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update signature if provided
        signature_data = request.data.get('signature_data')
        if signature_data:
            checklist_response.signature_data = signature_data
        
        # Update score and status
        checklist_response.update_score_and_status()
        
        # Generate PDF
        from apps.checklists.services import generate_checklist_pdf
        pdf_file = generate_checklist_pdf(checklist_response)
        checklist_response.pdf_file = pdf_file
        checklist_response.save()
        
        serializer = ChecklistResponseDetailSerializer(
            checklist_response,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def download_pdf(self, request, pk=None):
        """Download the PDF for a completed checklist."""
        checklist_response = self.get_object()
        
        if not checklist_response.pdf_file:
            return Response(
                {'error': 'PDF no disponible para este checklist.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return FileResponse(
            checklist_response.pdf_file.open('rb'),
            as_attachment=True,
            filename=f'checklist_{checklist_response.id}.pdf'
        )
    
    @action(detail=False, methods=['get'])
    def my_checklists(self, request):
        """Get checklists completed by the current user."""
        queryset = self.get_queryset().filter(completed_by=request.user)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_asset(self, request):
        """Get checklists for a specific asset."""
        asset_id = request.query_params.get('asset_id')
        if not asset_id:
            return Response(
                {'error': 'asset_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.get_queryset().filter(asset_id=asset_id)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
