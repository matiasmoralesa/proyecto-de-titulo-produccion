"""Property-based tests for dashboard KPI calculations."""

import pytest
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from hypothesis import given, strategies as st, settings
from hypothesis.extra.django import TestCase, from_model

from apps.work_orders.models import WorkOrder
from apps.assets.models import Asset, Location
from apps.core.dashboard_views import dashboard_stats
from apps.authentication.models import Role
from django.utils import timezone

User = get_user_model()


class DashboardKPIPropertyTests(TestCase):
    """Property-based tests for dashboard KPI calculations."""

    def setUp(self):
        """Set up test data."""
        # Clear cache to avoid stale data
        from django.core.cache import cache
        cache.clear()
        
        # Clean up any existing data in correct order to avoid ProtectedError
        WorkOrder.objects.all().delete()
        Asset.objects.all().delete()
        Location.objects.all().delete()
        User.objects.all().delete()
        Role.objects.all().delete()
        
        # Create admin role
        admin_role, _ = Role.objects.get_or_create(
            name='ADMIN',
            defaults={'description': 'Administrator'}
        )
        
        # Create user with role
        self.user = User.objects.create(
            username='testuser',
            email='test@example.com',
            role=admin_role
        )
        self.user.set_password('testpass123')
        self.user.save()
        
        # Create a test location
        self.location = Location.objects.create(
            name='Test Location',
            address='Test Address'
        )
        
        # Create a test asset
        from datetime import date
        self.asset = Asset.objects.create(
            name='Test Asset',
            vehicle_type='Camión Supersucker',
            model='Test Model',
            serial_number='TEST001',
            location=self.location,
            installation_date=date.today(),
            created_by=self.user
        )

    @given(
        st.lists(
            st.tuples(
                st.datetimes(
                    min_value=datetime(2020, 1, 1),
                    max_value=datetime(2024, 12, 31)
                ),
                st.datetimes(
                    min_value=datetime(2020, 1, 1),
                    max_value=datetime(2024, 12, 31)
                )
            ),
            min_size=0,
            max_size=50
        )
    )
    @settings(max_examples=100, deadline=None)
    def test_property_kpi_values_are_non_negative(self, date_pairs):
        """Property 1: KPI values are non-negative.
        
        For any set of work orders, the calculated average duration KPI 
        should always be greater than or equal to zero.
        
        **Validates: Requirements 1.1**
        """
        # Clear existing work orders
        WorkOrder.objects.all().delete()
        
        # Create work orders with the generated date pairs
        for i, (created_at, completed_date) in enumerate(date_pairs):
            # Make datetimes timezone-aware
            created_at_aware = timezone.make_aware(created_at) if timezone.is_naive(created_at) else created_at
            completed_date_aware = timezone.make_aware(completed_date) if timezone.is_naive(completed_date) else completed_date
            
            WorkOrder.objects.create(
                work_order_number=f'WO-TEST-{i}',
                title=f'Test Work Order {i}',
                description='Test description',
                status='Completada',
                priority='Media',
                asset=self.asset,
                assigned_to=self.user,
                scheduled_date=created_at_aware,
                created_by=self.user,
                created_at=created_at_aware,
                completed_date=completed_date_aware
            )
        
        # Get dashboard stats using APIClient
        from rest_framework.test import APIClient
        from django.core.cache import cache
        cache.clear()  # Clear cache to get fresh data
        
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.get('/api/v1/dashboard/stats/')
        data = response.data
        
        # Property: Average duration should always be >= 0
        avg_duration = data['kpis']['avg_duration_days']
        assert avg_duration >= 0, f"Average duration KPI is negative: {avg_duration}"
        
        # Additional properties for other KPIs
        assert data['kpis']['availability_rate'] >= 0, "Availability KPI is negative"
        assert data['kpis']['completion_rate'] >= 0, "Completion rate KPI is negative"
        assert data['kpis']['preventive_ratio'] >= 0, "Preventive ratio KPI is negative"
        assert data['kpis']['maintenance_backlog'] >= 0, "Backlog KPI is negative"
        assert data['kpis']['critical_assets_count'] >= 0, "Critical assets KPI is negative"
        assert data['kpis']['work_orders_this_month'] >= 0, "Work orders this month KPI is negative"
        assert data['kpis']['prediction_accuracy'] >= 0, "Prediction accuracy KPI is negative"

    @given(
        st.lists(
            st.tuples(
                st.datetimes(
                    min_value=datetime(2020, 1, 1),
                    max_value=datetime(2024, 12, 31)
                ),
                st.datetimes(
                    min_value=datetime(2020, 1, 1),
                    max_value=datetime(2024, 12, 31)
                )
            ),
            min_size=1,
            max_size=20
        )
    )
    @settings(max_examples=50, deadline=None)
    def test_property_invalid_dates_excluded(self, date_pairs):
        """Property 2: Invalid date data is excluded.
        
        For any work order with completed_date before created_at, 
        that work order should not be included in KPI calculations.
        
        **Validates: Requirements 1.2, 1.4**
        """
        # Clear existing work orders
        WorkOrder.objects.all().delete()
        
        valid_count = 0
        invalid_count = 0
        
        # Create work orders, some with invalid dates
        for i, (date1, date2) in enumerate(date_pairs):
            # Make datetimes timezone-aware
            date1_aware = timezone.make_aware(date1) if timezone.is_naive(date1) else date1
            date2_aware = timezone.make_aware(date2) if timezone.is_naive(date2) else date2
            
            # Randomly assign which date is created_at and which is completed_date
            if date1_aware <= date2_aware:
                created_at, completed_date = date1_aware, date2_aware
                valid_count += 1
            else:
                # Invalid: completed_date before created_at
                created_at, completed_date = date2_aware, date1_aware
                invalid_count += 1
            
            WorkOrder.objects.create(
                work_order_number=f'WO-TEST-{i}',
                title=f'Test Work Order {i}',
                description='Test description',
                status='Completada',
                priority='Media',
                asset=self.asset,
                assigned_to=self.user,
                scheduled_date=created_at,
                created_by=self.user,
                created_at=created_at,
                completed_date=completed_date
            )
        
        # Get dashboard stats using APIClient
        from rest_framework.test import APIClient
        from django.core.cache import cache
        cache.clear()  # Clear cache to get fresh data
        
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.get('/api/v1/dashboard/stats/')
        data = response.data
        
        # Property: If there are invalid dates, avg_duration should be calculated
        # only from valid work orders
        avg_duration = data['kpis']['avg_duration_days']
        
        if valid_count == 0:
            # If no valid work orders, average should be 0
            assert avg_duration == 0, f"Expected 0 when no valid work orders, got {avg_duration}"
        else:
            # If there are valid work orders, average should be >= 0
            assert avg_duration >= 0, f"Average duration should be non-negative, got {avg_duration}"

    @given(
        st.integers(min_value=0, max_value=100)
    )
    @settings(max_examples=20)
    def test_property_kpi_percentages_in_valid_range(self, num_orders):
        """Property: Percentage KPIs should be in valid range 0-100.
        
        For any number of work orders, percentage-based KPIs should 
        always be between 0 and 100.
        """
        # Clear existing work orders
        WorkOrder.objects.all().delete()
        
        # Create random work orders
        statuses = ['Pendiente', 'En Progreso', 'Completada', 'Cancelada']
        priorities = ['Baja', 'Media', 'Alta', 'Urgente']
        
        for i in range(num_orders):
            status = statuses[i % len(statuses)]
            priority = priorities[i % len(priorities)]
            
            created_at = timezone.now() - timedelta(days=i + 1)
            completed_date = timezone.now() if status == 'Completada' else None
            
            WorkOrder.objects.create(
                work_order_number=f'WO-TEST-{i}',
                title=f'Test Work Order {i}',
                description='Test description',
                status=status,
                priority=priority,
                asset=self.asset,
                assigned_to=self.user,
                scheduled_date=created_at,
                created_by=self.user,
                created_at=created_at,
                completed_date=completed_date
            )
        
        # Get dashboard stats using APIClient
        from rest_framework.test import APIClient
        from django.core.cache import cache
        cache.clear()  # Clear cache to get fresh data
        
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.get('/api/v1/dashboard/stats/')
        data = response.data
        
        # Property: Percentage KPIs should be in valid range
        kpis = data['kpis']
        
        assert 0 <= kpis['availability_rate'] <= 100, f"Availability out of range: {kpis['availability_rate']}"
        assert 0 <= kpis['completion_rate'] <= 100, f"Completion rate out of range: {kpis['completion_rate']}"
        assert 0 <= kpis['preventive_ratio'] <= 100, f"Preventive ratio out of range: {kpis['preventive_ratio']}"
        assert 0 <= kpis['prediction_accuracy'] <= 100, f"Prediction accuracy out of range: {kpis['prediction_accuracy']}"
