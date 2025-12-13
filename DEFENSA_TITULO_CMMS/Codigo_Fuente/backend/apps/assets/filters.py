"""
Filters for assets app.
"""
import django_filters
from .models import Asset, Location


class AssetFilter(django_filters.FilterSet):
    """Filter for Asset model."""
    name = django_filters.CharFilter(lookup_expr='icontains')
    vehicle_type = django_filters.ChoiceFilter(choices=Asset.VEHICLE_TYPE_CHOICES)
    status = django_filters.ChoiceFilter(choices=Asset.STATUS_CHOICES)
    location = django_filters.ModelChoiceFilter(queryset=Location.objects.all())
    serial_number = django_filters.CharFilter(lookup_expr='icontains')
    license_plate = django_filters.CharFilter(lookup_expr='icontains')
    is_archived = django_filters.BooleanFilter()
    installation_date_from = django_filters.DateFilter(
        field_name='installation_date',
        lookup_expr='gte'
    )
    installation_date_to = django_filters.DateFilter(
        field_name='installation_date',
        lookup_expr='lte'
    )
    
    class Meta:
        model = Asset
        fields = [
            'name', 'vehicle_type', 'status', 'location',
            'serial_number', 'license_plate', 'is_archived'
        ]


class LocationFilter(django_filters.FilterSet):
    """Filter for Location model."""
    name = django_filters.CharFilter(lookup_expr='icontains')
    address = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Location
        fields = ['name', 'address']
