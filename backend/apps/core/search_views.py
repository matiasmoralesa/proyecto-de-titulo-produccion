"""
Global search views for CMMS application
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q

from apps.assets.models import Asset
from apps.work_orders.models import WorkOrder
from apps.inventory.models import SparePart
from apps.maintenance.models import MaintenancePlan
from apps.checklists.models import ChecklistTemplate


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def global_search(request):
    """
    Global search across multiple models
    
    Query parameters:
    - q: Search query string
    - limit: Maximum results per model (default: 5)
    """
    query = request.GET.get('q', '').strip()
    limit = int(request.GET.get('limit', 5))
    
    if not query or len(query) < 2:
        return Response({
            'query': query,
            'results': {
                'assets': [],
                'work_orders': [],
                'spare_parts': [],
                'maintenance_plans': [],
                'checklists': [],
            },
            'total_count': 0,
        })
    
    # Search Assets
    assets = Asset.objects.filter(
        Q(name__icontains=query) |
        Q(serial_number__icontains=query) |
        Q(license_plate__icontains=query) |
        Q(vehicle_type__icontains=query)
    ).select_related('location')[:limit]
    
    assets_results = [{
        'id': str(asset.id),
        'type': 'asset',
        'title': asset.name,
        'subtitle': f"{asset.vehicle_type} - {asset.serial_number}",
        'status': asset.status,
        'url': f'/assets/{asset.id}',
    } for asset in assets]
    
    # Search Work Orders
    work_orders = WorkOrder.objects.filter(
        Q(work_order_number__icontains=query) |
        Q(title__icontains=query) |
        Q(description__icontains=query)
    ).select_related('asset', 'assigned_to')[:limit]
    
    work_orders_results = [{
        'id': str(wo.id),
        'type': 'work_order',
        'title': f"{wo.work_order_number} - {wo.title}",
        'subtitle': f"Activo: {wo.asset.name}",
        'status': wo.status,
        'url': f'/work-orders',
    } for wo in work_orders]
    
    # Search Spare Parts
    spare_parts = SparePart.objects.filter(
        Q(name__icontains=query) |
        Q(part_number__icontains=query) |
        Q(description__icontains=query)
    )[:limit]
    
    spare_parts_results = [{
        'id': str(sp.id),
        'type': 'spare_part',
        'title': sp.name,
        'subtitle': f"PN: {sp.part_number} - Stock: {sp.quantity}",
        'status': 'low_stock' if sp.quantity <= sp.minimum_quantity else 'in_stock',
        'url': f'/inventory',
    } for sp in spare_parts]
    
    # Search Maintenance Plans
    maintenance_plans = MaintenancePlan.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query)
    ).select_related('asset')[:limit]
    
    maintenance_plans_results = [{
        'id': str(mp.id),
        'type': 'maintenance_plan',
        'title': mp.name,
        'subtitle': f"Activo: {mp.asset.name}",
        'status': 'active' if mp.is_active else 'inactive',
        'url': f'/maintenance',
    } for mp in maintenance_plans]
    
    # Search Checklist Templates
    checklists = ChecklistTemplate.objects.filter(
        Q(name__icontains=query) |
        Q(code__icontains=query) |
        Q(description__icontains=query)
    )[:limit]
    
    checklists_results = [{
        'id': str(cl.id),
        'type': 'checklist',
        'title': cl.name,
        'subtitle': f"Código: {cl.code} - {cl.vehicle_type}",
        'status': 'active' if cl.is_active else 'inactive',
        'url': f'/checklists',
    } for cl in checklists]
    
    # Calculate total count
    total_count = (
        len(assets_results) +
        len(work_orders_results) +
        len(spare_parts_results) +
        len(maintenance_plans_results) +
        len(checklists_results)
    )
    
    return Response({
        'query': query,
        'results': {
            'assets': assets_results,
            'work_orders': work_orders_results,
            'spare_parts': spare_parts_results,
            'maintenance_plans': maintenance_plans_results,
            'checklists': checklists_results,
        },
        'total_count': total_count,
    })
