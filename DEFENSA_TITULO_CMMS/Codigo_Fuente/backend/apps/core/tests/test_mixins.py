"""
Unit tests for QuerySet mixins.
Tests role-based filtering for different user roles.
"""
import pytest
from django.test import RequestFactory
from rest_framework.test import APIRequestFactory
from rest_framework import viewsets
from apps.core.mixins import (
    RoleBasedQuerySetMixin,
    OwnerFilterMixin,
    TeamFilterMixin,
    AssetAccessMixin,
)
from apps.authentication.models import Role, User
from apps.work_orders.models import WorkOrder
from apps.assets.models import Asset, Location


@pytest.fixture
def api_factory():
    """Create API request factory"""
    return APIRequestFactory()


@pytest.fixture
@pytest.mark.django_db
def test_data(roles):
    """Create test data for mixin tests"""
    # Create users
    admin = User.objects.create_user(
        username='admin',
        email='admin@test.com',
        password='testpass123',
        role=roles['admin']
    )
    
    supervisor = User.objects.create_user(
        username='supervisor',
        email='supervisor@test.com',
        password='testpass123',
        role=roles['supervisor']
    )
    
    operator1 = User.objects.create_user(
        username='operator1',
        email='operator1@test.com',
        password='testpass123',
        role=roles['operator']
    )
    
    operator2 = User.objects.create_user(
        username='operator2',
        email='operator2@test.com',
        password='testpass123',
        role=roles['operator']
    )
    
    # Create location
    location = Location.objects.create(
        name='Test Location',
        address='123 Test St'
    )
    
    # Create assets
    from django.utils import timezone
    
    asset1 = Asset.objects.create(
        name='Asset 1',
        vehicle_type=Asset.CAMION_SUPERSUCKER,
        model='Model 1',
        serial_number='SN001',
        location=location,
        status=Asset.STATUS_OPERANDO,
        installation_date=timezone.now().date(),
        created_by=admin
    )
    
    asset2 = Asset.objects.create(
        name='Asset 2',
        vehicle_type=Asset.CAMIONETA_MDO,
        model='Model 2',
        serial_number='SN002',
        location=location,
        status=Asset.STATUS_OPERANDO,
        installation_date=timezone.now().date(),
        created_by=admin
    )
    
    # Create work orders
    wo1 = WorkOrder.objects.create(
        title='WO 1',
        description='Test WO 1',
        asset=asset1,
        assigned_to=operator1,
        created_by=admin,
        scheduled_date=timezone.now()
    )
    
    wo2 = WorkOrder.objects.create(
        title='WO 2',
        description='Test WO 2',
        asset=asset2,
        assigned_to=operator2,
        created_by=admin,
        scheduled_date=timezone.now()
    )
    
    wo3 = WorkOrder.objects.create(
        title='WO 3',
        description='Test WO 3',
        asset=asset1,
        assigned_to=operator1,
        created_by=admin,
        scheduled_date=timezone.now()
    )
    
    return {
        'admin': admin,
        'supervisor': supervisor,
        'operator1': operator1,
        'operator2': operator2,
        'asset1': asset1,
        'asset2': asset2,
        'wo1': wo1,
        'wo2': wo2,
        'wo3': wo3,
    }


@pytest.mark.django_db
class TestRoleBasedQuerySetMixin:
    """Test RoleBasedQuerySetMixin"""
    
    def test_admin_sees_all_work_orders(self, api_factory, test_data):
        """Test that admin users see all work orders"""
        # Create a test ViewSet
        class TestViewSet(RoleBasedQuerySetMixin, viewsets.ModelViewSet):
            queryset = WorkOrder.objects.all()
        
        request = api_factory.get('/')
        request.user = test_data['admin']
        
        viewset = TestViewSet()
        viewset.request = request
        
        queryset = viewset.get_queryset()
        assert queryset.count() == 3
    
    def test_operator_sees_only_own_work_orders(self, api_factory, test_data):
        """Test that operators only see their assigned work orders"""
        class TestViewSet(RoleBasedQuerySetMixin, viewsets.ModelViewSet):
            queryset = WorkOrder.objects.all()
        
        request = api_factory.get('/')
        request.user = test_data['operator1']
        
        viewset = TestViewSet()
        viewset.request = request
        
        queryset = viewset.get_queryset()
        assert queryset.count() == 2  # operator1 has 2 work orders
        
        # Verify all returned work orders are assigned to operator1
        for wo in queryset:
            assert wo.assigned_to == test_data['operator1']
    
    def test_supervisor_sees_all_work_orders(self, api_factory, test_data):
        """Test that supervisors see all work orders (default implementation)"""
        class TestViewSet(RoleBasedQuerySetMixin, viewsets.ModelViewSet):
            queryset = WorkOrder.objects.all()
        
        request = api_factory.get('/')
        request.user = test_data['supervisor']
        
        viewset = TestViewSet()
        viewset.request = request
        
        queryset = viewset.get_queryset()
        assert queryset.count() == 3
    
    def test_unauthenticated_sees_nothing(self, api_factory):
        """Test that unauthenticated users see no records"""
        from django.contrib.auth.models import AnonymousUser
        
        class TestViewSet(RoleBasedQuerySetMixin, viewsets.ModelViewSet):
            queryset = WorkOrder.objects.all()
        
        request = api_factory.get('/')
        request.user = AnonymousUser()
        
        viewset = TestViewSet()
        viewset.request = request
        
        queryset = viewset.get_queryset()
        assert queryset.count() == 0


@pytest.mark.django_db
class TestOwnerFilterMixin:
    """Test OwnerFilterMixin"""
    
    def test_admin_sees_all(self, api_factory, test_data):
        """Test that admin users see all records"""
        class TestViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
            queryset = WorkOrder.objects.all()
            ownership_field = 'assigned_to'
        
        request = api_factory.get('/')
        request.user = test_data['admin']
        
        viewset = TestViewSet()
        viewset.request = request
        
        queryset = viewset.get_queryset()
        assert queryset.count() == 3
    
    def test_supervisor_sees_all(self, api_factory, test_data):
        """Test that supervisors see all records"""
        class TestViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
            queryset = WorkOrder.objects.all()
            ownership_field = 'assigned_to'
        
        request = api_factory.get('/')
        request.user = test_data['supervisor']
        
        viewset = TestViewSet()
        viewset.request = request
        
        queryset = viewset.get_queryset()
        assert queryset.count() == 3
    
    def test_operator_sees_only_own(self, api_factory, test_data):
        """Test that operators only see their own records"""
        class TestViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
            queryset = WorkOrder.objects.all()
            ownership_field = 'assigned_to'
        
        request = api_factory.get('/')
        request.user = test_data['operator1']
        
        viewset = TestViewSet()
        viewset.request = request
        
        queryset = viewset.get_queryset()
        assert queryset.count() == 2
        
        for wo in queryset:
            assert wo.assigned_to == test_data['operator1']
    
    def test_different_operators_see_different_records(self, api_factory, test_data):
        """Test that different operators see different records"""
        class TestViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
            queryset = WorkOrder.objects.all()
            ownership_field = 'assigned_to'
        
        # Operator 1
        request1 = api_factory.get('/')
        request1.user = test_data['operator1']
        
        viewset1 = TestViewSet()
        viewset1.request = request1
        
        queryset1 = viewset1.get_queryset()
        
        # Operator 2
        request2 = api_factory.get('/')
        request2.user = test_data['operator2']
        
        viewset2 = TestViewSet()
        viewset2.request = request2
        
        queryset2 = viewset2.get_queryset()
        
        # They should see different records
        assert queryset1.count() == 2
        assert queryset2.count() == 1
        
        # No overlap
        wo_ids_1 = set(queryset1.values_list('id', flat=True))
        wo_ids_2 = set(queryset2.values_list('id', flat=True))
        assert len(wo_ids_1.intersection(wo_ids_2)) == 0


@pytest.mark.django_db
class TestTeamFilterMixin:
    """Test TeamFilterMixin"""
    
    def test_admin_sees_all(self, api_factory, test_data):
        """Test that admin users see all records"""
        class TestViewSet(TeamFilterMixin, viewsets.ModelViewSet):
            queryset = WorkOrder.objects.all()
            team_field = 'assigned_to'
        
        request = api_factory.get('/')
        request.user = test_data['admin']
        
        viewset = TestViewSet()
        viewset.request = request
        
        queryset = viewset.get_queryset()
        assert queryset.count() == 3
    
    def test_supervisor_sees_team(self, api_factory, test_data):
        """Test that supervisors see their team's records"""
        class TestViewSet(TeamFilterMixin, viewsets.ModelViewSet):
            queryset = WorkOrder.objects.all()
            team_field = 'assigned_to'
        
        request = api_factory.get('/')
        request.user = test_data['supervisor']
        
        viewset = TestViewSet()
        viewset.request = request
        
        queryset = viewset.get_queryset()
        # Default implementation: supervisors see all
        assert queryset.count() == 3
    
    def test_operator_sees_only_own(self, api_factory, test_data):
        """Test that operators only see their own records"""
        class TestViewSet(TeamFilterMixin, viewsets.ModelViewSet):
            queryset = WorkOrder.objects.all()
            team_field = 'assigned_to'
        
        request = api_factory.get('/')
        request.user = test_data['operator1']
        
        viewset = TestViewSet()
        viewset.request = request
        
        queryset = viewset.get_queryset()
        assert queryset.count() == 2


@pytest.mark.django_db
class TestAssetAccessMixin:
    """Test AssetAccessMixin"""
    
    def test_admin_sees_all_assets(self, api_factory, test_data):
        """Test that admin users see all assets"""
        class TestViewSet(AssetAccessMixin, viewsets.ModelViewSet):
            queryset = Asset.objects.all()
            asset_field = 'id'  # For Asset model itself
        
        request = api_factory.get('/')
        request.user = test_data['admin']
        
        viewset = TestViewSet()
        viewset.request = request
        
        queryset = viewset.get_queryset()
        assert queryset.count() == 2
    
    def test_supervisor_sees_all_assets(self, api_factory, test_data):
        """Test that supervisors see all assets"""
        class TestViewSet(AssetAccessMixin, viewsets.ModelViewSet):
            queryset = Asset.objects.all()
            asset_field = 'id'
        
        request = api_factory.get('/')
        request.user = test_data['supervisor']
        
        viewset = TestViewSet()
        viewset.request = request
        
        queryset = viewset.get_queryset()
        assert queryset.count() == 2
    
    def test_operator_sees_only_assigned_assets(self, api_factory, test_data):
        """Test that operators only see assets from their work orders"""
        # For this test, we need a model that has an asset field
        # We'll use a mock prediction-like model
        
        # Operator1 has work orders for asset1 only
        # So they should only see asset1
        
        class TestViewSet(AssetAccessMixin, viewsets.ModelViewSet):
            queryset = Asset.objects.all()
            asset_field = 'id'
            
            def filter_by_asset_access(self, queryset, user):
                """Override to test asset filtering"""
                from apps.work_orders.models import WorkOrder
                
                if user.role.name == Role.OPERADOR:
                    # Get assets from user's work orders
                    accessible_assets = WorkOrder.objects.filter(
                        assigned_to=user
                    ).values_list('asset_id', flat=True).distinct()
                    
                    return queryset.filter(id__in=accessible_assets)
                
                return queryset
        
        request = api_factory.get('/')
        request.user = test_data['operator1']
        
        viewset = TestViewSet()
        viewset.request = request
        
        queryset = viewset.get_queryset()
        
        # Operator1 has work orders for asset1 only
        assert queryset.count() == 1
        assert queryset.first() == test_data['asset1']
    
    def test_different_operators_see_different_assets(self, api_factory, test_data):
        """Test that different operators see different assets"""
        class TestViewSet(AssetAccessMixin, viewsets.ModelViewSet):
            queryset = Asset.objects.all()
            asset_field = 'id'
            
            def filter_by_asset_access(self, queryset, user):
                from apps.work_orders.models import WorkOrder
                
                if user.role.name == Role.OPERADOR:
                    accessible_assets = WorkOrder.objects.filter(
                        assigned_to=user
                    ).values_list('asset_id', flat=True).distinct()
                    
                    return queryset.filter(id__in=accessible_assets)
                
                return queryset
        
        # Operator 1
        request1 = api_factory.get('/')
        request1.user = test_data['operator1']
        
        viewset1 = TestViewSet()
        viewset1.request = request1
        
        queryset1 = viewset1.get_queryset()
        
        # Operator 2
        request2 = api_factory.get('/')
        request2.user = test_data['operator2']
        
        viewset2 = TestViewSet()
        viewset2.request = request2
        
        queryset2 = viewset2.get_queryset()
        
        # Operator1 sees asset1, Operator2 sees asset2
        assert queryset1.count() == 1
        assert queryset2.count() == 1
        assert queryset1.first() == test_data['asset1']
        assert queryset2.first() == test_data['asset2']


@pytest.mark.django_db
class TestMixinEdgeCases:
    """Test edge cases for mixins"""
    
    def test_empty_queryset_for_operator_with_no_work_orders(self, api_factory, roles):
        """Test that operator with no work orders sees empty queryset"""
        # Create operator with no work orders
        operator = User.objects.create_user(
            username='operator_no_wo',
            email='operator_no_wo@test.com',
            password='testpass123',
            role=roles['operator']
        )
        
        class TestViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
            queryset = WorkOrder.objects.all()
            ownership_field = 'assigned_to'
        
        request = api_factory.get('/')
        request.user = operator
        
        viewset = TestViewSet()
        viewset.request = request
        
        queryset = viewset.get_queryset()
        assert queryset.count() == 0
    
    def test_invalid_ownership_field(self, api_factory, test_data):
        """Test behavior with invalid ownership field"""
        class TestViewSet(OwnerFilterMixin, viewsets.ModelViewSet):
            queryset = WorkOrder.objects.all()
            ownership_field = 'nonexistent_field'
        
        request = api_factory.get('/')
        request.user = test_data['operator1']
        
        viewset = TestViewSet()
        viewset.request = request
        
        queryset = viewset.get_queryset()
        # Should return empty queryset when field doesn't exist
        assert queryset.count() == 0
