"""
Serializers for reports app.
"""
from rest_framework import serializers


class DateRangeSerializer(serializers.Serializer):
    """Serializer for date range filters."""
    start_date = serializers.DateTimeField(required=False, allow_null=True)
    end_date = serializers.DateTimeField(required=False, allow_null=True)
    asset_id = serializers.IntegerField(required=False, allow_null=True)


class KPISerializer(serializers.Serializer):
    """Serializer for KPI data."""
    mtbf = serializers.FloatField(allow_null=True)
    mttr = serializers.FloatField()
    oee = serializers.FloatField()


class WorkOrderSummarySerializer(serializers.Serializer):
    """Serializer for work order summary."""
    total = serializers.IntegerField()
    by_status = serializers.DictField()
    by_priority = serializers.DictField()
    by_type = serializers.DictField()
    avg_completion_time = serializers.FloatField()
    total_hours_worked = serializers.FloatField()


class AssetDowntimeSerializer(serializers.Serializer):
    """Serializer for asset downtime data."""
    asset__id = serializers.IntegerField()
    asset__name = serializers.CharField()
    asset__vehicle_type = serializers.CharField()
    total_downtime = serializers.FloatField()
    work_order_count = serializers.IntegerField()


class SparePartConsumptionSerializer(serializers.Serializer):
    """Serializer for spare part consumption data."""
    spare_part__id = serializers.IntegerField()
    spare_part__name = serializers.CharField()
    spare_part__part_number = serializers.CharField()
    total_quantity = serializers.IntegerField()
    movement_count = serializers.IntegerField()


class MaintenanceComplianceSerializer(serializers.Serializer):
    """Serializer for maintenance compliance data."""
    total_plans = serializers.IntegerField()
    overdue_plans = serializers.IntegerField()
    upcoming_plans = serializers.IntegerField()
    compliance_rate = serializers.FloatField()
    on_schedule = serializers.IntegerField()
