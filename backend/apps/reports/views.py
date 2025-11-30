"""
Views for reports app.
"""
import csv
from datetime import datetime, timedelta
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.reports.services import ReportService
from apps.reports.serializers import (
    DateRangeSerializer,
    KPISerializer,
    WorkOrderSummarySerializer,
    AssetDowntimeSerializer,
    SparePartConsumptionSerializer,
    MaintenanceComplianceSerializer
)


class ReportViewSet(viewsets.ViewSet):
    """
    ViewSet for report generation and KPI calculations.
    """
    permission_classes = [IsAuthenticated]
    
    def _parse_date_params(self, request):
        """Parse and validate date parameters from request."""
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')
        asset_id = request.query_params.get('asset_id')
        
        start_date = None
        end_date = None
        
        if start_date_str:
            try:
                start_date = datetime.fromisoformat(start_date_str.replace('Z', '+00:00'))
            except ValueError:
                pass
        
        if end_date_str:
            try:
                end_date = datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))
            except ValueError:
                pass
        
        # Default to last 30 days if not specified
        if not start_date:
            start_date = timezone.now() - timedelta(days=30)
        
        if not end_date:
            end_date = timezone.now()
        
        return start_date, end_date, asset_id
    
    @action(detail=False, methods=['get'])
    def kpis(self, request):
        """Get all KPIs (MTBF, MTTR, OEE)."""
        start_date, end_date, asset_id = self._parse_date_params(request)
        
        kpis = {
            'mtbf': ReportService.calculate_mtbf(
                asset_id=asset_id,
                start_date=start_date,
                end_date=end_date
            ),
            'mttr': ReportService.calculate_mttr(
                asset_id=asset_id,
                start_date=start_date,
                end_date=end_date
            ),
            'oee': ReportService.calculate_oee(
                asset_id=asset_id,
                start_date=start_date,
                end_date=end_date
            ),
        }
        
        serializer = KPISerializer(kpis)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def work_order_summary(self, request):
        """Get work order summary report."""
        start_date, end_date, asset_id = self._parse_date_params(request)
        
        summary = ReportService.get_work_order_summary(
            start_date=start_date,
            end_date=end_date,
            asset_id=asset_id
        )
        
        serializer = WorkOrderSummarySerializer(summary)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def asset_downtime(self, request):
        """Get asset downtime report."""
        start_date, end_date, _ = self._parse_date_params(request)
        
        downtime_data = ReportService.get_asset_downtime_report(
            start_date=start_date,
            end_date=end_date
        )
        
        serializer = AssetDowntimeSerializer(downtime_data, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def spare_part_consumption(self, request):
        """Get spare part consumption report."""
        start_date, end_date, _ = self._parse_date_params(request)
        
        consumption_data = ReportService.get_spare_part_consumption_report(
            start_date=start_date,
            end_date=end_date
        )
        
        serializer = SparePartConsumptionSerializer(consumption_data, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def maintenance_compliance(self, request):
        """Get maintenance compliance report."""
        start_date, end_date, _ = self._parse_date_params(request)
        
        compliance_data = ReportService.get_maintenance_compliance_report(
            start_date=start_date,
            end_date=end_date
        )
        
        serializer = MaintenanceComplianceSerializer(compliance_data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Get all KPIs and summaries for dashboard."""
        start_date, end_date, _ = self._parse_date_params(request)
        
        dashboard_data = ReportService.get_dashboard_kpis(
            start_date=start_date,
            end_date=end_date
        )
        
        return Response(dashboard_data)
    
    @action(detail=False, methods=['get'])
    def export_work_orders(self, request):
        """Export work order summary as CSV."""
        start_date, end_date, asset_id = self._parse_date_params(request)
        
        summary = ReportService.get_work_order_summary(
            start_date=start_date,
            end_date=end_date,
            asset_id=asset_id
        )
        
        # Create CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="work_orders_{start_date.date()}_{end_date.date()}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Work Order Summary Report'])
        writer.writerow(['Date Range', f'{start_date.date()} to {end_date.date()}'])
        writer.writerow([])
        
        writer.writerow(['Metric', 'Value'])
        writer.writerow(['Total Work Orders', summary['total']])
        writer.writerow(['Total Hours Worked', summary['total_hours_worked']])
        writer.writerow(['Avg Completion Time (hours)', summary['avg_completion_time']])
        writer.writerow([])
        
        writer.writerow(['Status', 'Count'])
        for status, data in summary['by_status'].items():
            writer.writerow([data['label'], data['count']])
        writer.writerow([])
        
        writer.writerow(['Priority', 'Count'])
        for priority, data in summary['by_priority'].items():
            writer.writerow([data['label'], data['count']])
        writer.writerow([])
        
        writer.writerow(['Type', 'Count'])
        for wo_type, data in summary['by_type'].items():
            writer.writerow([data['label'], data['count']])
        
        return response
    
    @action(detail=False, methods=['get'])
    def export_asset_downtime(self, request):
        """Export asset downtime report as CSV."""
        start_date, end_date, _ = self._parse_date_params(request)
        
        downtime_data = ReportService.get_asset_downtime_report(
            start_date=start_date,
            end_date=end_date
        )
        
        # Create CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="asset_downtime_{start_date.date()}_{end_date.date()}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Asset Downtime Report'])
        writer.writerow(['Date Range', f'{start_date.date()} to {end_date.date()}'])
        writer.writerow([])
        
        writer.writerow(['Asset ID', 'Asset Name', 'Vehicle Type', 'Total Downtime (hours)', 'Work Order Count'])
        for item in downtime_data:
            writer.writerow([
                item['asset__id'],
                item['asset__name'],
                item['asset__vehicle_type'],
                item['total_downtime'],
                item['work_order_count']
            ])
        
        return response
